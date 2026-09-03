# Stage 4 - Cross-Encoder Reranking

Rescores the top 50 retrieved candidates with a cross-encoder before returning
the top k. Compare against [stage-3-query-routing.md](stage-3-query-routing.md) (routing),
[stage-2-hybrid-retrieval.md](stage-2-hybrid-retrieval.md) (hybrid) and [stage-1-vector-baseline.md](stage-1-vector-baseline.md) (vector).

Measured on the frozen `golden_set_v1.jsonl` - 45 questions, 20 conceptual,
15 identifier, 10 unanswerable. Index unchanged since stage 2: 1,913 documents,
41,594 chunks, fingerprint `5a3e0e1883e9ecb3`. No re-embedding.

This stage also retires the stage 3 router, for the reasons set out in §3.

## Progression

| | stage 1 | stage 2 | stage 3 | stage 4 |
|---|---|---|---|---|
| | vector | hybrid | routed | hybrid + rerank |
| conceptual hit@1 | 0.200 | 0.450 | 0.450 | 0.700 |
| conceptual hit@5 | 0.900 | 0.900 | 0.900 | 0.950 |
| conceptual MRR | 0.463 | 0.629 | 0.629 | 0.815 |
| identifier hit@1 | 0.067 | 0.067 | 0.267 | 0.600 |
| identifier hit@5 | 0.067 | 0.400 | 0.467 | 0.800 |
| identifier MRR | 0.067 | 0.233 | 0.350 | 0.698 |
| aggregate hit@1 | 0.143 | 0.286 | 0.371 | 0.657 |
| aggregate hit@5 | 0.543 | 0.686 | 0.714 | 0.886 |
| aggregate MRR | 0.293 | 0.459 | 0.510 | 0.765 |

Largest single improvement in the project. Identifier retrieval has gone from
1-in-15 to 12-in-15 across four stages.

---

## 1. How it works

The retriever is a bi-encoder: query and chunk are embedded separately and
never meet, so each chunk was compressed into 384 numbers *without knowing the
question*. That separation is what makes scanning 41,594 chunks a single matrix
multiply, and what makes the scores cluster (`top_gap` 0.014, barely
discriminating).

A cross-encoder feeds query and chunk through a transformer together, so
attention runs across both. It answers "does this passage answer this question"
rather than "are these two vectors close". Far more accurate, and far too slow
for the whole corpus: one forward pass per pair, nothing precomputable.

```
hybrid retrieval  ->  top 50 candidates     cheap, approximate, high recall
cross-encoder     ->  rescore all 50        expensive, accurate, high precision
                  ->  re-sort, take top k
```

Model: `cross-encoder/ms-marco-MiniLM-L-6-v2` (~90 MB, 6 layers),
`K_RERANK = 50`.

Score separation: cross-encoder logits now span roughly 3 to 7 on real queries
against a `top_gap` of 0.014 before. The ranking finally means something.

---

## 2. Why the ceiling was there to reach

A reranker only reorders what retrieval handed it, so its ceiling is recall at
the candidate depth. Measured under stage 3 retrieval before building it:

```
    k      all   conceptual   identifier
    1    0.371        0.450        0.267   <- stage 3
    5    0.714        0.900        0.467
   50    0.971        1.000        0.933   <- ceiling
```

Headroom on both segments, which is why this stage was chosen over
multi-granularity chunking or weighted RRF.

---

## 3. The router is retired

`stage-3-query-routing.md` §4 predicted the reranker might subsume routing. It did - and
routing turned out to be actively harmful once a reranker was present:

| | conceptual hit@5 | identifier hit@5 | identifier MRR |
|---|---|---|---|
| routed + rerank | 0.950 | 0.733 | 0.666 |
| hybrid + rerank | 0.950 | 0.800 | 0.698 |

Routing discards the vector channel on identifier queries, shrinking the
candidate pool from ~100 fused results to ~50 keyword-only ones. Stage 3 needed
that restriction because RRF diluted the keyword signal; the reranker fixes the
dilution properly, by rescoring rather than by pre-selecting. Once it can
sort good from bad itself, it simply wants more candidates.

`RETRIEVAL_MODE` is now `"hybrid"`. The router code and `router_probe.jsonl`
are kept - set `RETRIEVAL_MODE = "auto"` to reproduce stage 3, but it is no
longer in the default path.

Stage 3's value was real and temporary: aggregate `hit@5` 0.686 -> 0.714,
superseded one stage later. Recorded rather than quietly deleted, because a
component being retired by a better one is a normal outcome that write-ups
rarely show.

---

## 4. Control: reranking is a ranking fix, not a recall fix

| | conceptual hit@5 | identifier hit@5 |
|---|---|---|
| vector + rerank | 0.900 | 0.267 |
| hybrid + rerank | 0.950 | 0.800 |

With BM25 removed, the reranker cannot recover identifier chunks. It can only
reorder what was fetched, and vector retrieval never fetches them. BM25 is still
doing the essential work of finding; the cross-encoder does the work of
ordering. Neither substitutes for the other.

---

## 5. Cost

| | latency |
|---|---|
| retrieval only | 9 ms |
| retrieval + rerank | 210 ms |

23x slower, for +0.286 aggregate `hit@1`. Still comfortably interactive, but
this is the first change in the project with a real latency cost, and the first
that would need a GPU in production - the cross-encoder runs 50 forward passes
per query.

---

## 6. Limitations

### KNOWN - 3 of 15 identifier questions still fail

`hit@5` 0.800 against a candidate-pool ceiling of 0.933. Some headroom remains
in ranking; the rest needs better retrieval.

### KNOWN - `recall@5` stays low where ground truth is large

Identifier `recall@5` is 0.258 against `hit@5` of 0.800. Those questions have
7 to 8 correct chunks each, so `recall@5` is mathematically capped near 0.6.
`hit@5` is the metric that matters for generation - the model needs one correct
chunk in the prompt, not all of them.

### BLOCKING - retrieval still cannot signal failure

Unchanged across four stages, and reranking has made the score scale change
again: cross-encoder logits now, having been RRF (~0.03), BM25 (~22) and cosine
(0 to 1) at earlier stages. No threshold has ever survived a change of retrieval
method, and four have now occurred.

The unanswerable segment remains the only instrument for this, and it measures
generation-side refusal rather than retrieval-side detection.

### KNOWN - `top_gap` still not scale-free

Now reports ~1.2 (cross-encoder logits). Comparable within a stage, meaningless
across stages. Still needs normalising.

### KNOWN - golden set has no procedural or multi-hop segment

Unchanged. 45 questions, three segments, nothing measuring multi-document
reasoning. Also: every question is a well-formed sentence, so nothing measures
the short, typo-ridden, acronym-heavy queries real users write.

### ACCEPTED - chunks and vectors coupled by position

Unchanged.

### ACCEPTED - no access control

Unchanged. A correctness requirement for any multi-user deployment.

---

## 7. Stage 5 candidates

Corpus curation. Cheapest remaining experiment: build an index over the 750
guidance documents only and compare against all 1,913. Does administrative noise
(sentencing notes, exemptions, corporate reporting) hurt retrieval on guidance
questions? No new models, no new code - filter the chunk list and re-run. The
most distinctive finding available, and nobody else's write-up has it.

Metadata filtering. Restrict legal questions to the 59 ACOPs and 40 Safe
Work Instruments using `facet_types` from the harvest. Pairs naturally with
curation.

A larger reranker. `bge-reranker-base` is ~1.1 GB against the current 90 MB.
Would need care on a 6 GB card alongside the bi-encoder, and latency would rise
from 210 ms.

Generation-side evaluation. Retrieval is now good enough that answer quality
is plausibly the weaker half, and it has never been measured. Requires
hand-labelling groundedness on ~30 answers - the LLM-as-judge alternative needs
calibrating against human labels first.

Metric hygiene. Normalise `top_gap`, add `hit@6` to match the actual
`top_k` used by `answer()`.

Real query logs. Still the single biggest gap. Everything measured here is
synthetic and written by the same person who built the system.

---
