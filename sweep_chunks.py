"""Chunk-size sweep -- the last untested variable.

CHUNK_WORDS/CHUNK_OVERLAP were chosen in stage 1 relative to the median page
(262 words) and never varied. Every later stage held them fixed.

Changing chunk size moves every chunk ID, so the golden set's pointers must be
regenerated per variant. The QUESTIONS stay byte-identical -- only the ground
truth is re-resolved, by the same literal-match method that created it. That
keeps the comparison honest: the same 45 questions, re-pointed at whatever
chunking is in play.

Two caveats this cannot remove, both reported alongside the numbers:
  - ground-truth set sizes shift with chunk size, which changes what recall@k
    means. hit@k is the more robust comparison.
  - at fixed k the model receives a different amount of context per variant.
    A fixed-token-budget comparison is also printed (k scaled inversely).

    python sweep_chunks.py
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import golden
import metrics
import rag

BASE_DIR = Path(__file__).resolve().parent
OUT = BASE_DIR / "eval" / "chunk_sweep.json"

# (words, overlap, k at a fixed ~1800-word budget)
CONFIGS = [(150, 25, 12), (300, 50, 6), (600, 100, 3)]

PHRASE = re.compile(r"literal match on '(.*)'")
REF = re.compile(r"chunks reference '(.*?)'")


def reground(gold: list[dict]) -> tuple[list[dict], dict]:
    """Re-resolve every question's ground truth against the current index.

    Questions are untouched. Only the chunk IDs move.
    """
    golden._chunks = None          # force a re-read of the rebuilt index
    regrounded, sizes, lost = [], [], []

    for g in gold:
        item = dict(g)
        notes = g.get("notes", "")
        if g["segment"] == "unanswerable":
            item["relevant_chunk_ids"] = []
        elif (m := PHRASE.search(notes)):
            item["relevant_chunk_ids"] = sorted(
                c["chunk_id"] for c in golden.find_by_text(m.group(1)))
        elif (m := REF.search(notes)):
            item["relevant_chunk_ids"] = sorted(
                c["chunk_id"] for c in golden.find_by_ref(m.group(1)))
        else:
            lost.append(g["id"])
            continue
        if g["segment"] != "unanswerable":
            if not item["relevant_chunk_ids"]:
                lost.append(g["id"])
                continue
            sizes.append(len(item["relevant_chunk_ids"]))
        regrounded.append(item)

    return regrounded, {"median_gt": sorted(sizes)[len(sizes) // 2] if sizes else 0,
                        "max_gt": max(sizes) if sizes else 0,
                        "unresolvable": lost}


def evaluate(gold: list[dict], chunks, vectors, k: int) -> dict:
    rows = []
    for g in gold:
        hits = rag.search(g["question"], vectors, chunks, top_k=max(k, 10))
        rows.append({"retrieved": [h["chunk_id"] for h in hits],
                     "scores": [h["score"] for h in hits],
                     "relevant": set(g["relevant_chunk_ids"]),
                     "segment": g["segment"]})
    return {"agg": metrics.aggregate(rows, (1, k, 5)),
            "seg": metrics.by_segment(rows, (1, k, 5))}


def main() -> int:
    base_gold = golden.load_golden()
    results = []

    for words, overlap, budget_k in CONFIGS:
        print(f"\n{'=' * 62}\nCHUNK {words}/{overlap}\n{'=' * 62}")
        rag.CHUNK_WORDS, rag.CHUNK_OVERLAP = words, overlap
        rag._by_id_cache = None
        rag._fts = None
        chunks, vectors = rag.build_index(force=True)

        gold, gt = reground(base_gold)
        print(f"reground: {len(gold)}/{len(base_gold)} questions, "
              f"median ground truth {gt['median_gt']} chunks, max {gt['max_gt']}")
        if gt["unresolvable"]:
            print(f"  ! unresolvable: {gt['unresolvable']}")

        fixed = evaluate(gold, chunks, vectors, 5)          # fixed k
        budget = evaluate(gold, chunks, vectors, budget_k)  # fixed token budget

        results.append({
            "chunk_words": words, "chunk_overlap": overlap, "budget_k": budget_k,
            "n_chunks": len(chunks), "n_questions": len(gold),
            "median_ground_truth": gt["median_gt"],
            "fixed_k5": fixed, "fixed_budget": budget,
        })
        print(f"  n_chunks {len(chunks)}   hit@5 {fixed['agg']['hit@5']:.3f}   "
              f"hit@{budget_k} {budget['agg'][f'hit@{budget_k}']:.3f}")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(results, indent=2, default=str), encoding="utf-8")

    print(f"\n\n{'=' * 74}\nCHUNK SIZE SWEEP -- fixed k=5\n{'=' * 74}")
    print(f"{'config':<14}{'chunks':>9}{'gt':>5}{'hit@1':>9}{'hit@5':>9}"
          f"{'mrr':>9}{'concept':>10}{'ident':>9}")
    for r in results:
        a, s = r["fixed_k5"]["agg"], r["fixed_k5"]["seg"]
        print(f"{r['chunk_words']}/{r['chunk_overlap']:<10}{r['n_chunks']:>9}"
              f"{r['median_ground_truth']:>5}{a['hit@1']:>9.3f}{a['hit@5']:>9.3f}"
              f"{a['mrr']:>9.3f}{s['conceptual']['hit@5']:>10.3f}"
              f"{s['identifier']['hit@5']:>9.3f}")

    print(f"\n{'=' * 74}\nFIXED TOKEN BUDGET (~1800 words to the model)\n{'=' * 74}")
    for r in results:
        k = r["budget_k"]
        a = r["fixed_budget"]["agg"]
        print(f"  {r['chunk_words']}/{r['chunk_overlap']:<8} k={k:<4} "
              f"hit@{k} {a[f'hit@{k}']:.3f}   mrr {a['mrr']:.3f}")

    print(f"\nwrote {OUT.relative_to(BASE_DIR)}")
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
