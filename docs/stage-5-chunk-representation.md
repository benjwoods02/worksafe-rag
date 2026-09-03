# Stage 5 — Chunk Representation Retested (negative result)

Contextual headers were rejected in stage 2 under vector-only retrieval. The
retrieval architecture has changed completely since — hybrid search plus a
cross-encoder reranker — so the rejection was retested rather than assumed.

**Result: rejected again. No header variant beats plain text under any
architecture tested.**

Measured on the frozen `golden_set_v1.jsonl`. Index: 1,913 documents,
41,594 chunks, `bge-small-en-v1.5`, chunk 300/50, hybrid + rerank.
Configuration restored to `HEADER_MODE = "none"`, fingerprint `5a3e0e1883e9ecb3`.

## Result

```
                     stage 4      title+heading    heading only
                    (no header)
conceptual hit@1       0.700         0.700            0.700
conceptual hit@5       0.950         1.000            0.950
conceptual mrr         0.815         0.812            0.817
identifier hit@1       0.600         0.533            0.533
identifier hit@5       0.800         0.800            0.667
identifier mrr         0.698         0.622            0.578
aggregate  hit@1       0.657         0.629            0.629
aggregate  hit@5       0.886         0.914            0.829
aggregate  mrr         0.765         0.731            0.714
```

### Stopping rule, set before the run

> Adopt if aggregate MRR or `hit@1` improves by >= 0.02 with no `hit@5`
> regression. Reject otherwise.

`title+heading`: MRR **fell** 0.034, `hit@1` **fell** 0.028. Reject.
`heading` only: worse on almost everything. Reject.

The threshold was fixed in advance deliberately. With 45 questions, one question
flipping is worth ~0.022 on a segment, so anything smaller is noise — and
without a pre-set rule it would have been tempting to adopt `title+heading` on
the strength of conceptual `hit@5` reaching 1.000 while ignoring the MRR drop.

---

## 1. Why it was worth retesting

The stage 2 rejection rested on a specific, measured mechanism: headers raised
intra-document chunk similarity from 0.748 to 0.817, which crowded the top-5
with neighbours from the same document. Three things changed after stage 2 that
bear directly on that mechanism:

1. **Retrieval now fetches 50 candidates and reranks to 6.** A crowded top-5 is
   an intermediate state the reranker can undo, not the output.
2. **A cross-encoder can read the header literally**, rather than having it
   compressed into 384 numbers alongside 300 words of body text.
3. **BM25 now indexes the header too.** Stage 2 measured headers with no keyword
   channel at all, and document titles and section names are exactly the rare,
   discriminating terms BM25 rewards.

## 2. The mechanism changed; the verdict did not

This is the informative part.

| | vector-only (stage 2) | hybrid + rerank (stage 5) |
|---|---|---|
| `title+heading` | `hit@5` 0.900 -> 0.750 | `hit@5` 0.886 -> 0.914, MRR 0.765 -> 0.731 |
| `heading` only | `hit@5` 0.900 -> 0.800 | `hit@5` 0.886 -> 0.829 |

Under vector-only, headers **hurt recall** — the clustering effect crowded out
correct chunks. Under hybrid + rerank that damage is gone: conceptual `hit@5`
actually rises to 1.000. The reranker neutralised the stage 2 mechanism exactly
as predicted.

What remains is a different and smaller effect: **headers hurt ranking rather
than recall.** Prefixing ~10 identical tokens to all 50 candidates gives the
cross-encoder the same information in every option, which is noise for the
discrimination it is trying to make. Identifier MRR fell hardest, 0.698 -> 0.622.

Same conclusion, different cause, two architectures apart. A negative result
that survives a change of architecture is considerably more robust than one that
does not.

## 3. A prediction that failed twice

Before both stage 2 variant D and stage 5 variant 2, the prediction was that
**`heading` only would beat `title+heading`**, because section headings vary
within a document while titles are identical across it. In stage 2 that came
from a measured diagnostic (intra-document similarity 0.767 vs 0.817, section
discrimination 0.064 vs 0.044).

It was wrong both times, and by a wide margin the second time — `heading` only
was the worst configuration tested.

Recorded because it is the clearest evidence in the project that **intuition
about chunk representation is unreliable, and cheap proxies for retrieval
quality do not substitute for running the evaluation.** Four rebuilds, roughly
40 minutes of GPU time, and the golden set was the only thing that ever settled
the question.

---

## 4. What this says about the project

All measured gains came from **retrieval architecture**, none from chunk
representation:

```
                     stage 1   stage 2   stage 3   stage 4   stage 5
                     vector    hybrid    routed    +rerank   headers
aggregate  hit@5      0.543     0.686     0.714     0.886    rejected
aggregate  mrr        0.293     0.459     0.510     0.765    rejected
identifier hit@5      0.067     0.400     0.467     0.800    rejected
conceptual hit@1      0.200     0.450     0.450     0.700    rejected
```

Hybrid search and reranking did the work. Headers did nothing, twice. Routing
helped, then was retired by the reranker. Chunk size and page-bounding were
never revisited after stage 1 and remain untested variables.

For anyone building a similar system, the actionable version: **spend effort on
retrieval architecture before chunk engineering.** Chunking gets disproportionate
attention in RAG writing relative to what it delivered here.

---

## 5. Limitations of this conclusion

**Only two header variants were tested**, both prepend-style. Untested: LLM-
generated contextual summaries per chunk (Anthropic's contextual retrieval — far
beyond budget at 41,594 chunks), parent-document retrieval, and sentence-level
indexing. "Contextual headers do not help" is supported; "chunk representation
never matters" is not.

**The instrument is near its resolution limit.** At 45 questions, two questions
of movement is ~0.045 on a segment. Conceptual `hit@5` is 0.950 and identifier
0.800 against a candidate-pool ceiling of 0.933 — there is very little left to
win, and most further changes would be indistinguishable from noise. A larger
golden set would be needed to measure anything smaller.

**Chunk size and page-bounding were never tested.** 300/50 was chosen in stage 1
relative to the median page and never varied. That is the most obvious untested
chunk-representation variable, and this negative result does not cover it.

---

## 6. Where the project stands

Retrieval is close to its measurable ceiling on this golden set. Two gaps
remain, neither of which is more retrieval tuning:

**Generation has never been measured.** Retrieval went 0.543 -> 0.886 on
`hit@5`. Answer quality is plausibly now the weaker half and has no numbers
attached at all. Requires hand-labelling groundedness on ~30 answers; an
LLM-as-judge would need calibrating against those human labels first.

**Everything measured is synthetic.** The golden set, the router probe, the
realistic-query set — all written by the same person who built the system. Real
query logs remain the single largest gap in the project, and no amount of
further tuning against synthetic questions closes it.

---

## Notes

<!-- space for your own notes below -->
