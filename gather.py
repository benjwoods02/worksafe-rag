"""Harvest the WorkSafe publications catalogue into urls.jsonl.

The catalogue claims ~2,280 documents but the plain listing caps out at 1,000
(`?start=1000` returns nothing). To get past that, this harvests each facet
value separately through the filter form:

    /publications-and-resources/FilterSearchForm/?PublicationTypes=ACOP&start=0

Every facet partition is well under the 1,000 cap, so the union covers the
whole catalogue. Documents are deduplicated on doc_id.

Harvesting per facet has a second payoff: it tells you each document's types,
topics and industries authoritatively, even where the listing text omits them.
Those land in facet_types / facet_topics / facet_industries and are far more
reliable than the scraped `type` / `topic` strings.

    python gather.py                      # full run, ~420 requests, ~9 minutes
    python gather.py --facets types       # types only, much faster
    python gather.py --max-partitions 3   # smoke test
"""
from __future__ import annotations

import argparse
import base64
import binascii
import json
import re
import sys
import time
from collections import Counter
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import requests
from bs4 import BeautifulSoup

BASE = "https://www.worksafe.govt.nz"
LISTING = f"{BASE}/publications-and-resources/"
FILTER = f"{LISTING}FilterSearchForm/"
PAGE_SIZE = 40
START_CAP = 1000          # the site returns nothing beyond this
DELAY_SECONDS = 1.2
USER_AGENT = "worksafe-rag personal learning project"

FILE_SUFFIX = re.compile(r"\s*\(([A-Z]+)\s+([\d.]+\s*[KMG]B)\)\s*$")
DOC_ID = re.compile(r"/dmsdocument/(\d+)")

PUBLICATION_TYPES = [
    "Annual report", "ACOP", "Alert", "Briefing to incoming minister", "Bulletin",
    "Case study", "Consultation", "Complaint", "Corporate", "Decision document",
    "Enforceable undertaking", "Exemption", "Fact sheet", "Form", "Formal warning",
    "Good practice guide", "Guide", "Installation fault notice", "Interpretative guide",
    "Policy", "Poster", "Presentation", "Quarterly report", "Quick guide", "Register",
    "Report", "Safe Work Instrument", "Sentencing notes", "Statement of intent",
    "Statement of performance expectation", "Template", "WorkSafe position",
]

INDUSTRIES = [
    "Administration and support services", "Adventure activities", "Agriculture",
    "Arts and recreation", "Building and construction", "Consumer",
    "Education and training", "Energy", "Extractives", "Fishing, hunting, and trapping",
    "Forestry", "Geothermal", "Health care and social assistance", "High hazards",
    "Hospitality", "Major hazard facilities", "Manufacturing", "Mining",
    "Occupational diving", "Other services", "Ports", "Petroleum",
    "Postal, transport, and warehousing", "Public administration and safety",
    "Public sector", "Quarrying", "Rental, hiring, and real estate", "Retail",
    "Tunnelling", "Waste services", "Water services", "Wholesale trade",
]


def decode_link(href: str) -> str | None:
    """Listing links wrap the real path in a base64 JSON blob.

    The payload often has its '=' padding stripped, which makes b64decode
    raise -- hence the manual re-padding.
    """
    encoded = (parse_qs(urlparse(href).query).get("searchResult") or [None])[0]
    if not encoded:
        return None
    try:
        return json.loads(base64.b64decode(encoded + "=" * (-len(encoded) % 4))).get("link")
    except (binascii.Error, ValueError, UnicodeDecodeError):
        return None


def attribute_value(article, label: str) -> str:
    """Text following a <span class="attributes">TYPE:</span> marker.

    Walking siblings rather than regexing the article text matters: the
    description shares a parent, so a greedy regex swallows it too.
    """
    for span in article.select("span.attributes"):
        if span.get_text(strip=True).upper().startswith(label):
            parts = []
            for sibling in span.next_siblings:
                if getattr(sibling, "name", None) in ("br", "div", "span"):
                    break
                parts.append(sibling if isinstance(sibling, str) else sibling.get_text(" "))
            return " ".join(parts).replace("\xa0", " ").strip(" ,\t\n")
    return ""


def parse_article(article) -> dict | None:
    anchor = article.select_one('a[href*="searchResult="]')
    if anchor is None:
        return None
    link = decode_link(anchor["href"])
    if not link:
        return None

    raw_title = " ".join(anchor.get_text(" ").split())
    suffix = FILE_SUFFIX.search(raw_title)
    description = article.select_one('[itemprop="description"]')
    match = DOC_ID.search(link)

    return {
        "url": BASE + link,
        "doc_id": match.group(1) if match else "",
        "title": FILE_SUFFIX.sub("", raw_title),
        "file_type": suffix.group(1) if suffix else "",
        "file_size": suffix.group(2) if suffix else "",
        "type": attribute_value(article, "TYPE"),
        "topic": attribute_value(article, "TOPIC"),
        "description": " ".join(description.get_text(" ").split()) if description else "",
        "facet_types": [],
        "facet_topics": [],
        "facet_industries": [],
    }


TOTAL_HINT = re.compile(r"Found\s*(?:<[^>]*>)?\s*([\d,]+)")


def fetch_page(session, params: dict, start: int) -> tuple[list[dict], int | None]:
    query = {**params, "Search": "", "action_resultsWithFilter": "", "start": start}
    url = FILTER if params else LISTING
    response = session.get(url, params=query if params else {"start": start}, timeout=60)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "lxml")
    rows = [r for r in (parse_article(a) for a in soup.select("article.publication-item")) if r]
    hint = TOTAL_HINT.search(response.text)
    return rows, int(hint.group(1).replace(",", "")) if hint else None


def harvest_partition(session, params: dict, label: str) -> list[dict]:
    """Page through one facet value until a page comes back empty.

    Do NOT stop on a short page. Some pages yield 39 parseable articles rather
    than 40 (an item without a usable anchor), and treating that as the end of
    the list silently truncates the partition at page one.
    """
    found: list[dict] = []
    expected: int | None = None
    for start in range(0, START_CAP, PAGE_SIZE):
        try:
            rows, hint = fetch_page(session, params, start)
        except requests.RequestException as exc:
            print(f"    ! {label} start={start} failed: {exc}", file=sys.stderr)
            break
        if expected is None:
            expected = hint
        if not rows:
            break
        found.extend(rows)
        time.sleep(DELAY_SECONDS)
    else:
        print(f"    ! {label} hit the {START_CAP} cap -- may be truncated", file=sys.stderr)

    # Self-check: the page tells us how many it thinks there are.
    if expected is not None and len(found) < expected:
        print(f"    ? {label}: got {len(found)} of {expected} reported", file=sys.stderr)
    return found


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", default=Path("data") / "urls.jsonl", type=Path)
    parser.add_argument("--facets", default="types,topics,industries",
                        help="comma-separated subset of: types,topics,industries")
    parser.add_argument("--max-partitions", type=int, default=0,
                        help="stop after N partitions (smoke testing)")
    args = parser.parse_args(argv)

    session = requests.Session()
    session.headers["User-Agent"] = USER_AGENT
    wanted = {f.strip() for f in args.facets.split(",")}

    # Topics are read live so the list can't drift out of date.
    topics: list[str] = []
    if "topics" in wanted:
        soup = BeautifulSoup(session.get(LISTING, timeout=60).text, "lxml")
        topics = [o.get("value") for o in soup.select("#Topics option") if o.get("value")]
        print(f"discovered {len(topics)} topics")

    partitions: list[tuple[str, dict]] = [("(unfiltered)", {})]
    if "types" in wanted:
        partitions += [(f"type={t}", {"PublicationTypes": t}) for t in PUBLICATION_TYPES]
    if "topics" in wanted:
        partitions += [(f"topic={t}", {"Topics": t}) for t in topics]
    if "industries" in wanted:
        partitions += [(f"industry={i}", {"Industries": i}) for i in INDUSTRIES]
    if args.max_partitions:
        partitions = partitions[: args.max_partitions]

    # Resume: fold in anything already harvested.
    records: dict[str, dict] = {}
    if args.out.exists():
        for line in args.out.read_text(encoding="utf-8").splitlines():
            if line.strip():
                row = json.loads(line)
                records[row["doc_id"]] = row
        print(f"resuming from {len(records)} existing records")

    facet_key = {"PublicationTypes": "facet_types", "Topics": "facet_topics",
                 "Industries": "facet_industries"}

    for index, (label, params) in enumerate(partitions, start=1):
        before = len(records)
        for row in harvest_partition(session, params, label):
            existing = records.setdefault(row["doc_id"], row)
            for param, key in facet_key.items():
                value = params.get(param)
                if value and value not in existing[key]:
                    existing[key].append(value)
        print(f"[{index:>3}/{len(partitions)}] {label:<48} "
              f"+{len(records) - before:<4} total {len(records)}")

        # Write as we go so an interrupted run is not wasted.
        args.out.write_text(
            "\n".join(json.dumps(r, ensure_ascii=False) for r in records.values()) + "\n",
            encoding="utf-8")

    if not records:
        print("Nothing harvested.", file=sys.stderr)
        return 1

    files = Counter(r["file_type"] or "?" for r in records.values())
    kinds = Counter(t for r in records.values() for t in (r["facet_types"] or ["(untyped)"]))
    print(f"\nwrote {len(records)} documents -> {args.out}")
    print("  file types:", ", ".join(f"{k} {v}" for k, v in files.most_common()))
    print("  publication types:")
    for kind, n in kinds.most_common():
        print(f"    {n:>5}  {kind}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
