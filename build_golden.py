"""Generate golden_set_v1.jsonl.

Ground truth is established by LITERAL STRING MATCH against a distinctive
phrase from the answering passage -- never by running search() and labelling
what came back. That independence is the whole point: a set labelled from the
system's own output is a test it passes by construction.

Conceptual questions are seeded from question headings WorkSafe authors wrote
in their own documents, then REPHRASED. Used verbatim they would hand BM25 a
free lexical match and overstate what keyword search buys in stage 3.

    python build_golden.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import golden

OUT = Path(__file__).resolve().parent / "eval" / "golden_set_v1.jsonl"

# (rephrased question, distinctive phrase from the answer, doc_id restriction)
CONCEPTUAL = [
    ("if I am encapsulating asbestos rather than removing it, what category of work is that",
     "asbestos-related work is any work involving asbestos permitted under regulation 7", None),
    ("what information must be reachable within ten seconds for someone handling a gas cylinder",
     "available within ten seconds", None),
    ("a lagged pipe has burst unexpectedly, can asbestos removal start straight away",
     "Removal work may start immediately", None),
    ("when must air monitoring be carried out for airborne asbestos",
     "Duty to carry out air monitoring", None),
    ("do workers doing ongoing asbestos removal need health monitoring",
     "health monitoring is provided to its workers", None),
    ("must a certified handler be physically present when highly hazardous gases are in use",
     "The handler must be present and available", None),
    ("what should I look at when choosing a contractor from a health and safety perspective",
     "Choosing a capable contractor", None),
    ("what weight can different ground types support under a scaffold base",
     "Load-bearing capacity of different ground conditions", None),
    ("an excavation face looked stable yesterday, is that enough to rely on",
     "can appear stable for 24 hours", None),
    ("what protective equipment should be planned for a confined space emergency response",
     "Take care when selecting the right PPE for an emergency response", None),
    ("after crane repairs, who must be satisfied before a new inspection certificate issues",
     "to the satisfaction of an equipment inspector", None),
    ("if I hire out forklifts what must I tell customers about exhaust fumes",
     "RISK OF CARBON MONOXIDE POISONING", None),
    ("does someone only passing briefly through a hearing protector area need protection",
     "designated hearing protector area must wear", None),
    ("is notification needed before a quarantine fumigation using methyl bromide",
     "Modified requirements applying to quarantine or pre-shipment fumigation", None),
    ("how far must a fixed barrier sit from a robot arm reach",
     "500 mm from the robot work envelope", None),
    ("what properties make a substance hazardous in welding work",
     "explosive, flammable, oxidising, toxic, corrosive", None),
    ("when is a ladder actually the right tool for a task",
     "Is a ladder the right tool", None),
    ("how should I identify hazards for work at height alongside my workers",
     "Step 1: Identify the hazards", "20109"),
    ("what must a PCBU provide so workers are protected from health and safety risks",
     "providing any information, training, instruction or supervision that is necessary", None),
    ("what should be considered when selecting air monitoring sites for a fumigation",
     "factors should be considered when selecting monitoring sites", None),
]

# Plausible questions a duty holder might ask that this corpus does NOT answer.
# Deliberately workplace-adjacent rather than absurd -- an absurd question tests
# nothing. Each was checked against the corpus for accidental coverage.
UNANSWERABLE = [
    "what is the current adult minimum wage in New Zealand",
    "what is the Reserve Bank official cash rate",
    "how do I apply for a New Zealand work visa",
    "how do I register a company with the Companies Office",
    "how do I lodge a personal grievance for unfair dismissal",
    "what qualifications make someone a licensed building practitioner",
    "how do I claim ACC weekly compensation after an injury",
    "what notice period must I give when resigning from a job",
    "what is the maximum residential tenancy bond a landlord can require",
    "how do I dispute a parking infringement notice",
]

MAX_GROUND_TRUTH = 10   # beyond this, recall@5 is bounded so low it misleads


def main() -> int:
    rows, warnings = [], []

    for n, (question, phrase, doc_id) in enumerate(CONCEPTUAL, start=1):
        matches = golden.find_by_text(phrase)
        if doc_id:
            matches = [m for m in matches if m["doc_id"] == doc_id]
        ids = sorted(m["chunk_id"] for m in matches)
        if not ids:
            warnings.append(f"c{n:03d}: NO MATCH for {phrase!r} -- dropped")
            continue
        if len(ids) > MAX_GROUND_TRUTH:
            warnings.append(f"c{n:03d}: {len(ids)} ground-truth chunks (recall@k will be bounded)")
        rows.append({
            "id": f"c{n:03d}",
            "question": question,
            "relevant_chunk_ids": ids,
            "segment": "conceptual",
            "source": "mined from document question headings, rephrased",
            "notes": f"ground truth: literal match on {phrase!r}",
        })

    for n, question in enumerate(UNANSWERABLE, start=1):
        rows.append({
            "id": f"u{n:03d}",
            "question": question,
            "relevant_chunk_ids": [],
            "segment": "unanswerable",
            "source": "written; checked for accidental corpus coverage",
            "notes": "retrieval always returns a top-k; this measures how "
                     "confidently it returns junk, and whether generation refuses",
        })

    rows.extend(golden.build_identifier_questions(15))

    OUT.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n",
                   encoding="utf-8")

    from collections import Counter
    segments = Counter(r["segment"] for r in rows)
    print(f"wrote {len(rows)} questions -> {OUT.name}")
    for name, count in sorted(segments.items()):
        print(f"  {count:>3}  {name}")
    if warnings:
        print("\nwarnings:")
        for w in warnings:
            print(f"  ! {w}")
    print("\nStill to add by hand: procedural (~10) and multi-hop (~5).")
    print("Use `python golden.py page <doc_id> <page>` after reading a PDF --")
    print("that keeps ground truth independent of retrieval.")
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
