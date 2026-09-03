"""Tools for building and running the golden set.

The golden set is the instrument. If it is biased, every number after it is
decoration -- so the one rule is:

    GROUND TRUTH MUST COME FROM A METHOD OTHER THAN THE SYSTEM UNDER TEST.

Running search(), eyeballing the results and labelling whichever looks right
builds a test the system passes by construction. Recall will be near 1.0 and it
will mean nothing.

Two independent methods are provided:
  find_by_text()  -- literal string match, no embeddings involved
  find_by_page()  -- read the PDF, note the page, look up chunks by page

    python golden.py mine 40           # candidate questions to rephrase
    python golden.py identifiers 15    # auto-generate the identifier segment
    python golden.py text "Regulation 14"
    python golden.py page 20109 16
    python golden.py run               # evaluate against the golden set
    python golden.py probe             # router accuracy on held-out queries
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
INDEX_PATH = BASE_DIR / "data" / "index"
GOLDEN_PATH = BASE_DIR / "eval" / "golden_set_v1.jsonl"

_chunks = None


def load_chunks() -> list[dict]:
    """Read the cached index. Requires rag.py to have built it."""
    global _chunks
    if _chunks is None:
        path = INDEX_PATH / "chunks.json"
        if not path.exists():
            raise SystemExit("No index. Run:  python rag.py")
        _chunks = json.loads(path.read_text(encoding="utf-8"))
    return _chunks


# --------------------------------------------------------------- ground truth

def find_by_text(literal: str, case_sensitive: bool = False) -> list[dict]:
    """Chunks containing a literal string.

    Independent of embeddings, so it is valid ground truth. This is how the
    identifier segment is built: a chunk containing "Regulation 14" genuinely
    IS relevant to a question about Regulation 14.
    """
    needle = literal if case_sensitive else literal.lower()
    return [c for c in load_chunks()
            if needle in (c["text"] if case_sensitive else c["text"].lower())]


def find_by_page(doc_id: str, page: int) -> list[dict]:
    """Chunks on one page of one document.

    The gold-standard workflow: read the PDF, find the answer on page 14, and
    ground the question on that page's chunks. Completely independent of
    retrieval -- and only possible because chunking is page-bounded.
    """
    return [c for c in load_chunks()
            if c["doc_id"] == str(doc_id) and c["page"] == int(page)]


def find_docs(name_fragment: str) -> list[tuple[str, str]]:
    """(doc_id, filename) pairs whose filename contains a fragment."""
    seen = {}
    for c in load_chunks():
        if name_fragment.lower() in c["filename"].lower():
            seen[c["doc_id"]] = c["filename"]
    return sorted(seen.items())


# --------------------------------------------------------------- mining

QUESTION = re.compile(
    r"(?<![.?!])\b((?:What|How|When|Who|Why|Where|Which|Do|Does|Must|Can|Should|Is|Are)"
    r"\b[^.?!]{12,110}\?)")


def mine_questions(limit: int = 40) -> list[dict]:
    """Question headings already written in the documents, deduplicated.

    WorkSafe authors write in question headings, and each sits in the chunk
    that answers it. These are seeds ONLY -- see the warning in rephrase notes:
    used verbatim they hand BM25 a free lexical match and would overstate what
    keyword search buys you. Rephrase every one.
    """
    found: dict[str, list[str]] = defaultdict(list)
    for c in load_chunks():
        for match in QUESTION.finditer(c["text"]):
            question = " ".join(match.group(1).split())
            found[question].append(c["chunk_id"])

    ranked = sorted(found.items(), key=lambda kv: (-len(kv[1]), kv[0]))
    return [{"seed": q, "chunk_ids": ids[:6], "n_chunks": len(ids)}
            for q, ids in ranked[:limit]]


# --------------------------------------------------------------- identifiers

REF_PATTERNS = [
    (r"\bregulation\s+\d+[A-Z]?\b", "what does {ref} require"),
    (r"\bsection\s+\d+[A-Z]?\b", "what is set out in {ref}"),
    (r"\btable\s+[A-Z]?\d+\b", "{ref}"),
]


def find_by_ref(ref: str) -> list[dict]:
    """Chunks containing an exact reference, respecting word boundaries.

    A plain substring search is WRONG here: "regulation 52" is a substring of
    "regulation 52A" and of "regulation 520", so it silently drags unrelated
    chunks into the ground truth -- inflating recall on the very segment the
    project is trying to measure.
    """
    pattern = re.compile(r"\b" + re.escape(ref).replace(r"\ ", r"\s+") + r"\b", re.I)
    return [c for c in load_chunks() if pattern.search(c["text"])]


def build_identifier_questions(count: int = 15, min_chunks: int = 2,
                               max_chunks: int = 8) -> list[dict]:
    """Auto-generate the identifier segment with mechanical ground truth.

    Only refs appearing in a handful of CHUNKS are used -- counting occurrences
    instead would let a ref repeated inside one chunk pass the filter. A ref in
    200 chunks is not a precise target; one in a single chunk may be a typo.
    """
    chunks = load_chunks()
    questions, used_patterns = [], Counter()

    for pattern, template in REF_PATTERNS:
        # distinct chunks per ref, not raw occurrences
        chunk_counts: dict[str, set[str]] = defaultdict(set)
        for c in chunks:
            for m in re.finditer(pattern, c["text"], re.I):
                chunk_counts[m.group(0).lower()].add(c["chunk_id"])

        targets = sorted((ref for ref, ids in chunk_counts.items()
                          if min_chunks <= len(ids) <= max_chunks),
                         key=lambda r: -len(chunk_counts[r]))
        for ref in targets:
            if len(questions) >= count:
                break
            # cap per pattern so the segment is not all regulations
            if used_patterns[pattern] >= max(1, count // len(REF_PATTERNS) + 1):
                break
            matching = find_by_ref(ref)
            if not (min_chunks <= len(matching) <= max_chunks):
                continue        # boundary match disagreed with the scan
            used_patterns[pattern] += 1
            questions.append({
                "id": f"id{len(questions) + 1:03d}",
                "question": template.format(ref=ref.title()),
                "relevant_chunk_ids": sorted(c["chunk_id"] for c in matching),
                "segment": "identifier",
                "source": "auto: word-boundary regex match",
                "notes": f"{len(matching)} chunks reference '{ref}'",
            })
    return questions


# --------------------------------------------------------------- run

def probe_router() -> None:
    """Measure router accuracy on queries it was NOT built from.

    The frozen golden set cannot measure this: its identifier segment was
    auto-generated from the same regex patterns the router detects, so a regex
    router matches it by construction. The 'realistic' set is the meaningful
    number.
    """
    import rag

    path = BASE_DIR / "eval" / "router_probe.jsonl"
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()]

    groups: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        groups[row.get("set", "unlabelled")].append(row)

    for name, items in sorted(groups.items()):
        misses = [(i, rag.route(i["query"])) for i in items
                  if rag.route(i["query"]) != i["expect"]]
        ok = len(items) - len(misses)
        print(f"\n[{name}] {ok}/{len(items)} ({100 * ok / len(items):.0f}%)")
        for item, got in misses:
            print(f"    expected {item['expect']:<8} got {got:<8} {item['query'][:56]}")
            print(f"        {item['note']}")


def load_golden(path: Path | None = None) -> list[dict]:
    path = path or GOLDEN_PATH
    if not path.exists():
        raise SystemExit(f"No golden set at {path.name}.")
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()]
    if not rows:
        raise SystemExit(f"{path.name} is empty.")
    return rows


def run(top_k: int = 10) -> None:
    """Evaluate the current retriever against the golden set."""
    import metrics
    import rag

    golden = load_golden()
    chunks, vectors = rag.build_index()

    results = []
    for item in golden:
        hits = rag.search(item["question"], vectors, chunks, top_k=top_k)
        results.append({
            "retrieved": [h["chunk_id"] for h in hits],
            "scores": [h["score"] for h in hits],
            "relevant": set(item.get("relevant_chunk_ids", [])),
            "segment": item.get("segment", "unlabelled"),
        })

    manifest = json.loads((INDEX_PATH / "manifest.json").read_text(encoding="utf-8"))
    print(f"\nconfig: {rag.RETRIEVAL_MODE} · {manifest['n_chunks']} chunks · {manifest['embed_model']} · "
          f"chunk {manifest['chunk_words']}/{manifest['chunk_overlap']} · "
          f"top_k {top_k} · [{manifest['fingerprint']}]")
    print(metrics.format_report(metrics.aggregate(results),
                                metrics.by_segment(results)))


# --------------------------------------------------------------- cli

def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(__doc__)
        return 1
    command, args = argv[1], argv[2:]

    if command == "mine":
        for item in mine_questions(int(args[0]) if args else 40):
            print(f"[{item['n_chunks']:>3} chunks] {item['seed']}")
            print(f"            {', '.join(item['chunk_ids'][:4])}")

    elif command == "identifiers":
        for item in build_identifier_questions(int(args[0]) if args else 15):
            print(json.dumps(item, ensure_ascii=False))

    elif command == "text":
        for c in find_by_text(args[0])[:25]:
            print(f"{c['chunk_id']:<16} p{c['page']:<4} {c['filename'][:52]}")

    elif command == "page":
        for c in find_by_page(args[0], args[1]):
            print(f"{c['chunk_id']:<16} {c['text'][:150]}")

    elif command == "docs":
        for doc_id, filename in find_docs(args[0]):
            print(f"{doc_id:<8} {filename}")

    elif command == "run":
        run(int(args[0]) if args else 10)

    elif command == "probe":
        probe_router()

    else:
        print(__doc__)
        return 1
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main(sys.argv))
