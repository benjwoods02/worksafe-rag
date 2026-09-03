# Stage 2 - Hybrid Retrieval

Adds a BM25 keyword channel fused with vector search by Reciprocal Rank Fusion.
Compare against [stage-1-vector-baseline.md](stage-1-vector-baseline.md) (stage 1, vector only).

Measured on the frozen `golden_set_v1.jsonl` - 45 questions, 20 conceptual,
15 identifier, 10 unanswerable. Index: 1,913 documents, 41,594 chunks,
`bge-small-en-v1.5`, chunk 300/50, `header_mode: none`, fingerprint
`5a3e0e1883e9ecb3`.

## Headline

| | stage 1 | stage 2 | |
|---|---|---|---|
| conceptual hit@1 | 0.200 | 0.450 | +125% |
| conceptual hit@5 | 0.900 | 0.900 | held |
| identifier hit@5 | 0.067 | 0.400 | 6x |
| aggregate hit@5 | 0.543 | 0.686 | +26% |
| aggregate MRR | 0.293 | 0.459 | +57% |

Identifier retrieval went from 1 of 15 questions to 6 of 15, and conceptual
ranking more than doubled at rank 1 without losing anything at rank 5.

---

## 1. What changed

BM25 keyword index over the same chunks, via SQLite FTS5 (`porter unicode61`).
Chosen over `rank_bm25` because it is standard library, has `bm25()` built in,
and persists to disk beside the vector index - 98 MB, builds in 1.8 s.

Reciprocal Rank Fusion to combine the two channels:

```
score(chunk) = Σ over channels of  1 / (k + rank_in_that_channel)      k = 60
```

The channels produce incomparable scales - cosine sits in 0 to 1, BM25 is
unbounded and reached 22 on these queries. RRF discards the scores entirely and
uses only rank position, so no calibration or weighting is needed. Anything
ranking well in both channels floats to the top.

Config: `K_VECTOR = 50`, `K_KEYWORD = 50` candidates per channel before
fusion; `RRF_K = 60`; `RETRIEVAL_MODE = "hybrid"`.

Query escaping. FTS5 `MATCH` is a query language rather than raw text, and unescaped
punctuation is a syntax error. Queries are tokenised to alphanumerics, each term
quoted, and ORed. `bm25()` returns negative values (more negative is better), so
the sign is flipped to match the vector channel's convention.

---

## 2. Full results

```
                          vector     keyword      hybrid
[conceptual]  n=20
  hit@1                    0.200       0.400       0.450
  hit@5                    0.900       0.800       0.900
  recall@5                 0.505       0.567       0.556
  ndcg@5                   0.408       0.546       0.520
  mrr                      0.463       0.592       0.629

[identifier]  n=15
  hit@1                    0.067       0.267       0.067
  hit@5                    0.067       0.467       0.400
  recall@5                 0.025       0.158       0.083
  ndcg@5                   0.047       0.262       0.133
  mrr                      0.067       0.350       0.233

[aggregate]   n=45
  hit@1                    0.143       0.343       0.286
  hit@5                    0.543       0.657       0.686
  recall@5                 0.299       0.392       0.354
  ndcg@5                   0.253       0.424       0.354
  mrr                      0.293       0.488       0.459
```

Hybrid is adopted. It wins or ties every conceptual metric, takes identifier
`hit@5` from 0.067 to 0.400, and gives the best aggregate `hit@5`. Keyword-only
sacrifices conceptual `hit@5` (0.900 -> 0.800), which matters most for generation
 - the model needs a correct chunk in the prompt.

### Segmentation vindicated

Aggregate `hit@5` moved 0.543 -> 0.686. That single number conceals a 6x
improvement in one segment and no change in the other. Reported as an average,
the largest result in the project would have read as a modest 26% gain.

---

## 3. Finding: RRF dilutes the keyword signal on identifiers

Keyword-only beats hybrid on identifier queries - `hit@5` 0.467 vs 0.400,
`hit@1` 0.267 vs 0.067.

RRF weights both channels equally. On an identifier query the vector channel
returns confident garbage, and fusing garbage with good results drags the good
results down. On conceptual queries the reverse holds and fusion helps.

Neither mode dominates. This was not predicted, and it is the clearest target
for stage 3: weighted RRF, or routing the query to a channel based on whether it
contains an exact identifier.

---

## 4. Rejected: contextual headers

Prepending document/section context to chunk text before embedding. Tested in
two variants against a control, all on the same frozen golden set.

| Config | conceptual hit@5 | conceptual hit@1 | identifier hit@5 |
|---|---|---|---|
| A baseline | 0.900 | 0.200 | 0.067 |
| B control (new extraction, no headers) | 0.900 | 0.200 | 0.067 |
| C `title + heading` | 0.750 | 0.250 | 0.133 |
| D `heading` only | 0.800 | 0.200 | 0.067 |

Neither variant beats the baseline on `hit@5` or `nDCG@5`, so both were rejected.

Heading detection itself works well and was kept - by font size, not regex
(numbered-heading patterns covered only 21% of chunks and picked up
contents-page lines). Body text is consistently 8.5 pt with headings at 10 to 14 pt
across unrelated publications, so body size is computed per document and
headings found relative to it.

Two bugs worth recording, both caught by inspection rather than by the metrics:

- Cover-page display type became level 1. The largest size in every file is
  the 49 pt cover title, so every page inherited it. Fixed by requiring a
  heading level to recur - appear on at least `max(3, pages/20)` distinct
  pages, which excludes one-off display type.
- Headings split across lines were truncated to their tail. *"What are the
  duties for unlicensed asbestos removal?" became "removal?"*. Fixed by
  merging consecutive same-size lines within a block.

What survived: `heading` is still extracted and attached to every chunk, and
`format_sources` uses it. Citations now read *"Interpretive guidelines > 12.0
What are the duties for asbestos-related work?, p.90"* instead of a filename and
page. Better attribution, independent of the retrieval question.

---

## 5. Methodology notes

### A confound was introduced and caught

The first header experiment changed two things: it added headers, and it
switched text extraction from `get_text()` to a `get_text("dict")`
reconstruction needed for font sizes. Extracted text dropped 51.1 MB -> 49.9 MB.

Run B - new extraction, headers off - reproduced the stage 1 numbers exactly,
proving the extraction change had zero retrieval effect and the entire delta was
attributable to headers. Without that control the 15-point `hit@5` drop was
unattributable.

This violated the "one intervention per stage" rule from
[stage-1-vector-baseline.md](stage-1-vector-baseline.md) §7, one stage after stating it.

### A cheap proxy pointed the wrong way

Before rebuilding for variant D, a 30-second diagnostic measured intra-document
chunk similarity and section discrimination:

```
variant            intra-doc   same-sect  cross-sect    gap
plain (control)      0.748       0.786      0.742      0.044
title + heading      0.817       0.855      0.811      0.044
heading only         0.767       0.822      0.758      0.064
```

It predicted heading-only would win: a quarter of the clustering cost, 45% more
section discrimination. It lost on every metric.

The diagnostic measured within-document geometry only. Retrieval quality
depends on how queries match chunks across all 41,594, and the document title
was evidently doing real work at the document level, which a within-document
measurement cannot see.

A cheap proxy for retrieval quality therefore does not substitute for running the
evaluation itself.

### A silent failure mode in the tooling

`python rag.py | grep ...` reports grep's exit status, not Python's. A build
crashed with a `NameError` and the task still reported success. Same class of
error as trusting an HTTP 200 without checking the `%PDF-` bytes: a success
signal that is not measuring the thing you care about. Fixed with
`set -o pipefail` and an explicit `${PIPESTATUS[0]}` check.

---

## 6. Limitations

### RESOLVED - Exact identifiers are unretrievable

Was blocking in stage 1: 6 chunks contained "Regulation 9", 0 appeared in the
top 20. Identifier `hit@5` is now 0.400 under hybrid, 0.467 under keyword-only.
Not solved - 8 of 15 identifier questions still fail, but no longer a total
failure, and the remaining gap has a clear target (§3).

### BLOCKING - Retrieval still cannot signal failure

Unchanged from stage 1, and stage 2 made it harder to fix. Score scales are
now mode-dependent:

```
mean top-1 score on unanswerable queries
  vector    0.732        (cosine, 0-1)
  keyword  22.452        (BM25, unbounded)
  hybrid    0.029        (RRF, ~1/60)
```

A similarity threshold was already dead because unanswerable queries (0.732)
scored higher than answerable identifier queries (0.702). It is now dead a
second way: no threshold survives a change of retrieval method.

### KNOWN - `top_gap` and `unanswerable_top_score` are not scale-free

Both were added as diagnostics in stage 1 and are only meaningful within a
retrieval mode. Comparing 0.014 (vector) against 1.362 (keyword) against 0.002
(hybrid) is meaningless. They need normalising, or restricting to within-mode
comparison, before they can be reported.

### KNOWN - golden set has no procedural or multi-hop segment

Still 45 questions across three segments. Procedural (~10) and multi-hop (~5)
were never added, so nothing measures multi-document reasoning.

### ACCEPTED - chunks and vectors coupled by position

Unchanged. Row i of the embedding array corresponds to `chunks[i]` and nothing
enforces it. The BM25 channel keys on `chunk_id` instead, so hybrid retrieval is
slightly more robust to this than pure vector search was.

### ACCEPTED - no access control

Unchanged. Any multi-user deployment must push identity-derived filters into
the search query. A correctness requirement, not an optimisation.

---

## 7. Stage 3

Primary target, from §3: recover the identifier gap between hybrid (0.400)
and keyword-only (0.467). Two candidate interventions, one per stage:

1. Weighted RRF - give the keyword channel more weight, or weight per
   channel by score confidence.
2. Query routing - detect exact identifiers in the query (regex on
   regulation/section/table references) and route to the keyword channel alone.

Routing is more interpretable and cheaper to explain; weighted RRF is more
general. Test one, measure, then the other.

Also outstanding:

- Cross-encoder reranking. Conceptual `hit@50` was 0.950 at stage 1, against
  `hit@1` of 0.450 now - large remaining headroom in ranking, and a reranker
  is the standard fix.
- Hierarchical / multi-granularity chunking, deferred from stage 2. Sentence-level
  indexing is the slice with the clearest hypothesis: `"Regulation 47"` is two
  tokens diluted across 300 words, and a sentence has far less to dilute it.
  Note this changes `recall@k` semantics when a phrase appears in both a
  sentence chunk and its parent.
- Corpus curation - guidance-only index vs all 1,913 documents.

---

## Notes

<!-- space for your own notes below -->
