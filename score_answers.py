"""Score the filled-in generation labelling sheet.

Reports per-segment rates for each dimension, and lists every item that failed
so the failures can be read rather than just counted.

    python score_answers.py
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SHEET = BASE_DIR / "eval" / "label_sheet.md"
ANSWERS = BASE_DIR / "eval" / "answers.jsonl"

BLOCK = re.compile(r"```yaml\n(.*?)```", re.S)
# [ \t]* and NOT \s* -- \s matches newlines, so a blank field would swallow the
# NEXT line as its value, and every unreviewed item scored as if it were labelled.
FIELD = re.compile(r"^(\w+):[ \t]*([^#\n]*?)[ \t]*(?:#.*)?$", re.M)

# value -> counts toward the numerator of that dimension's rate
GOOD = {
    "grounded": {"yes"},
    "citations": {"valid"},
    "modality": {"correct"},
    "complete": {"yes"},
    "drift": {"none"},
    "refusal": {"correct"},
    "human": {"agree"},
}


def parse_labels() -> dict[str, dict]:
    if not SHEET.exists():
        raise SystemExit(f"No {SHEET.name}. Run: python generate_answers.py")
    labels = {}
    for block in BLOCK.findall(SHEET.read_text(encoding="utf-8")):
        fields = {k: v.strip() for k, v in FIELD.findall(block) if v.strip()}
        if "id" in fields:
            labels[fields.pop("id")] = fields
    return labels


def main() -> int:
    labels = parse_labels()
    answers = {json.loads(line)["id"]: json.loads(line)
               for line in ANSWERS.read_text(encoding="utf-8").splitlines() if line.strip()}

    labelled = {k: v for k, v in labels.items() if any(f != "notes" for f in v)}
    print(f"labelled {len(labelled)} of {len(labels)} answers")
    if not labelled:
        print("\nNothing labelled yet. Fill in the yaml blocks in eval/label_sheet.md.")
        return 0

    by_segment: dict[str, list[tuple[str, dict]]] = defaultdict(list)
    for qid, fields in labelled.items():
        by_segment[answers.get(qid, {}).get("segment", "?")].append((qid, fields))

    for dimension in ("grounded", "citations", "modality", "complete", "drift", "refusal", "human"):
        rows = []
        for segment, items in sorted(by_segment.items()):
            scored = [(q, f[dimension]) for q, f in items
                      if dimension in f and f[dimension] != "na"]
            if not scored:
                continue
            good = sum(1 for _, v in scored if v in GOOD[dimension])
            rows.append((segment, good, len(scored)))
        if not rows:
            continue
        total_good = sum(g for _, g, _ in rows)
        total_n = sum(n for _, _, n in rows)
        print(f"\n{dimension:<12} {total_good}/{total_n}  ({100 * total_good / total_n:.0f}%)")
        for segment, good, n in rows:
            print(f"    {segment:<14} {good}/{n}")

    print("\n--- failures ---")
    any_fail = False
    for qid, fields in sorted(labelled.items()):
        bad = {d: v for d, v in fields.items()
               if d in GOOD and v not in GOOD[d] and v != "na"}
        if bad:
            any_fail = True
            record = answers.get(qid, {})
            print(f"\n  {qid} [{record.get('segment', '?')}] {record.get('question', '')[:62]}")
            for d, v in bad.items():
                print(f"      {d}: {v}")
            if fields.get("notes"):
                print(f"      note: {fields['notes']}")
    if not any_fail:
        print("  none")

    counts = Counter(v for f in labelled.values() for k, v in f.items() if k in GOOD)
    print(f"\nlabel distribution: {dict(counts.most_common())}")
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
