"""Download the PDFs listed in urls.jsonl into data/raw/.

Resumable: files that already exist are skipped, so an interrupted run can be
restarted without re-fetching anything. Failures are written to failed.jsonl
so you can retry just those instead of the whole catalogue.

    python fetch.py --limit 10        # ALWAYS smoke test first
    python fetch.py --guidance-only   # the 750 guidance docs (~0.5 GB)
    python fetch.py                   # everything (~1,913 PDFs, ~1.6 GB, ~1 hour)
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from urllib.parse import unquote, urlparse

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Anchor paths to this file, not the current working directory, so the script
# behaves the same regardless of where it is invoked from.
ROOT = Path(__file__).resolve().parent
RAW = ROOT / "data" / "raw"
DELAY_SECONDS = 1.5
USER_AGENT = "worksafe-rag personal learning project"

# Publication types that actually state duties, hazards and controls.
# ACOP and Safe Work Instrument carry legal force under HSWA.
GUIDANCE_TYPES = {
    "Fact sheet", "Quick guide", "Guide", "Good practice guide", "ACOP", "Alert",
    "Safe Work Instrument", "Bulletin", "Interpretative guide", "WorkSafe position",
    "Case study", "Poster",
}

# Windows caps paths at 260 characters and some slugs run past 130. The doc_id
# prefix already guarantees uniqueness, so the slug can be truncated safely.
MAX_SLUG = 100


def filename_for(record: dict) -> str:
    """Derive a stable filename from the document URL.

    URLs end in '/latest/', so the final path segment is always the useless
    literal 'latest' -- the slug is the segment before it.
    """
    segments = [s for s in urlparse(record["url"]).path.split("/") if s]
    slug = segments[-2] if segments and segments[-1] == "latest" else segments[-1]
    slug = unquote(slug)[:MAX_SLUG].rstrip("-")
    return f"{slug}.pdf" if slug else f"{record['doc_id']}.pdf"


def build_session() -> requests.Session:
    """Retry transient failures automatically.

    Over ~1,900 requests a handful will fail for reasons that resolve on their
    own. Retrying 429/5xx with backoff turns those into successes instead of
    entries in failed.jsonl.
    """
    session = requests.Session()
    session.headers["User-Agent"] = USER_AGENT
    retry = Retry(
        total=3,
        backoff_factor=1.0,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=frozenset(["GET"]),
    )
    session.mount("https://", HTTPAdapter(max_retries=retry))
    return session


def human(n_bytes: float) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if n_bytes < 1024 or unit == "GB":
            return f"{n_bytes:.1f} {unit}"
        n_bytes /= 1024
    return f"{n_bytes:.1f} GB"


def load_records(path: Path, guidance_only: bool) -> list[dict]:
    records = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        if row.get("file_type") != "PDF":
            continue
        if guidance_only and not (set(row.get("facet_types", [])) & GUIDANCE_TYPES):
            continue
        records.append(row)
    return records


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--urls", default=ROOT / "data" / "urls.jsonl", type=Path)
    parser.add_argument("--out", default=RAW, type=Path)
    parser.add_argument("--failed", default=ROOT / "failed.jsonl", type=Path)
    parser.add_argument("--limit", type=int, default=0, help="stop after N downloads")
    parser.add_argument("--guidance-only", action="store_true",
                        help="only publication types that state duties and controls")
    args = parser.parse_args(argv)

    if not args.urls.exists():
        print(f"{args.urls} not found -- run gather.py first.", file=sys.stderr)
        return 1

    records = load_records(args.urls, args.guidance_only)
    args.out.mkdir(parents=True, exist_ok=True)
    session = build_session()

    downloaded = skipped = failed = 0
    total_bytes = 0
    failures: list[dict] = []
    started = time.time()

    print(f"{len(records)} PDFs to consider -> {args.out}")

    for index, record in enumerate(records, start=1):
        if args.limit and downloaded >= args.limit:
            print(f"\nreached --limit {args.limit}")
            break

        destination = args.out / filename_for(record)
        if destination.exists():
            skipped += 1
            continue

        try:
            response = session.get(record["url"], timeout=60)
            response.raise_for_status()
            content = response.content

            # A 200 can still be an HTML error page. Validating the magic bytes
            # here turns silent corruption into a visible failure now, rather
            # than a baffling parse error two stages later.
            if not content.startswith(b"%PDF-"):
                raise ValueError(f"not a PDF (starts with {content[:16]!r})")

            destination.write_bytes(content)
            downloaded += 1
            total_bytes += len(content)

            elapsed = time.time() - started
            remaining = len(records) - index
            eta = (elapsed / downloaded) * remaining if downloaded else 0
            print(f"[{index:>5}/{len(records)}] {destination.name[:58]:<58} "
                  f"{human(len(content)):>9}  eta {eta / 60:.0f}m")

        except (requests.RequestException, ValueError, OSError) as exc:
            failed += 1
            failures.append({**record, "error": str(exc)})
            print(f"  ! {record['doc_id']}: {exc}", file=sys.stderr)

        time.sleep(DELAY_SECONDS)

    if failures:
        args.failed.write_text(
            "\n".join(json.dumps(f, ensure_ascii=False) for f in failures) + "\n",
            encoding="utf-8")

    print(f"\ndownloaded {downloaded}  skipped {skipped}  failed {failed}")
    print(f"  {human(total_bytes)} in {(time.time() - started) / 60:.1f} min")
    if failures:
        print(f"  failures -> {args.failed} (re-run to retry them)")

    # Non-zero exit if a meaningful share failed, so it is not missed.
    return 1 if downloaded and failed > downloaded * 0.05 else 0


if __name__ == "__main__":
    sys.exit(main())
