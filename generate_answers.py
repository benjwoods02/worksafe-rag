"""Generate answers for the golden set and write a labelling sheet.

Retrieval has been measured across five stages; generation never has. This
produces the material to fix that: one answer per golden-set question, with the
sources it was built from, and a label block to fill in.

Labels are scored by an LLM judge and calibrated against human spot-checks.
The `human` field on each block records agreement, so the judge's reliability
is reported alongside its output rather than assumed.

    python generate_answers.py              # all 45 questions  (~$0.17)
    python generate_answers.py --limit 10   # smoke test
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import golden
import rag

BASE_DIR = Path(__file__).resolve().parent
ANSWERS = BASE_DIR / "eval" / "answers.jsonl"
SHEET = BASE_DIR / "eval" / "label_sheet.md"

HEADER = """# Generation quality — labelling sheet

Fill in the `yaml` block under each answer. Then run:

    python score_answers.py

## Label definitions

| Field | Values | Meaning |
|---|---|---|
| `grounded` | `yes` / `partial` / `no` | Is EVERY factual claim supported by the cited sources? One unsupported claim makes it `partial`. |
| `citations` | `valid` / `some_invalid` | Does each citation point to a source that actually supports the claim attached to it? |
| `modality` | `correct` / `wrong` / `na` | WorkSafe defines "must" as a legal requirement and "should" as recommended practice. Did the answer preserve the distinction? `na` if neither appears. |
| `complete` | `yes` / `missing` / `na` | Does it capture the qualifications a duty holder would need? `missing` if it omits an exception, condition or duty that changes what someone should do. |
| `drift` | `none` / `adjacent` | Did it build an answer out of topically-NEAR sources that do not address the question? `adjacent` answers pass every other check -- grounded, validly cited, no hallucination -- which is what makes them dangerous. |
| `refusal` | `correct` / `over_refused` / `failed` / `na` | Unanswerable questions: did it decline? `over_refused` = declined when the answer was there. `na` for answerable questions it answered. |

| `human` | `agree` / `disagree` | Human review of the LLM judge's labels for this item. Left blank until reviewed. |

Leave a field blank to skip it. `notes` is free text.

---
"""


def build_sheet(records: list[dict]) -> str:
    parts = [HEADER]
    for n, r in enumerate(records, start=1):
        parts.append(f"## {n}. `{r['id']}` [{r['segment']}]\n")
        parts.append(f"**Q:** {r['question']}\n")
        parts.append(f"### Answer\n\n{r['answer']}\n")
        parts.append("### Sources given to the model\n")
        for i, s in enumerate(r["sources"], start=1):
            parts.append(f"**[{i}]** `{s['chunk_id']}` — {s['label']}, p.{s['page']}  \n"
                         f"> {s['excerpt']}\n")
        parts.append(f"""```yaml
id: {r['id']}
grounded:      # yes | partial | no
citations:     # valid | some_invalid
modality:      # correct | wrong | na
complete:      # yes | missing | na
drift:         # none | adjacent
refusal:       # correct | over_refused | failed | na
human:         # agree | disagree
notes:
```

---
""")
    return "\n".join(parts)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--top-k", type=int, default=6)
    args = parser.parse_args(argv)

    gold = golden.load_golden()
    if args.limit:
        gold = gold[: args.limit]

    chunks, vectors = rag.build_index()
    titles = rag.load_titles()
    records = []

    for n, g in enumerate(gold, start=1):
        hits = rag.search(g["question"], vectors, chunks, top_k=args.top_k)
        result = rag.answer(g["question"], hits)
        records.append({
            "id": g["id"],
            "segment": g["segment"],
            "question": g["question"],
            "answer": result["text"],
            "sources": [{
                "chunk_id": h["chunk_id"],
                "label": titles.get(h["doc_id"]) or h["filename"],
                "page": h["page"],
                # enough to check a claim against without reprinting the corpus
                "excerpt": " ".join((h.get("body") or h["text"]).split())[:400],
            } for h in hits],
            "relevant_chunk_ids": g.get("relevant_chunk_ids", []),
            "cost": result.get("cost", 0.0),
        })
        print(f"[{n}/{len(gold)}] {g['id']:<7} ${result.get('cost', 0):.4f}")

    ANSWERS.parent.mkdir(parents=True, exist_ok=True)
    ANSWERS.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in records) + "\n",
                       encoding="utf-8")
    SHEET.write_text(build_sheet(records), encoding="utf-8")

    print(f"\n{len(records)} answers -> {ANSWERS.name} and {SHEET.name}")
    print(f"total cost: ${sum(r['cost'] for r in records):.4f}")
    print(f"\nNow label {SHEET.relative_to(BASE_DIR)}, then run: python score_answers.py")
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
