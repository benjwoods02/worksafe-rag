# worksafe-rag - Final Baseline

A retrieval-augmented generation system over New Zealand workplace health and
safety guidance, built and improved across five measured stages.

Every change was evaluated against a frozen golden set before adoption. Two
interventions were adopted, two were rejected, and one was adopted then retired
by a later stage. This document is the summary; the per-stage records are
[stage-1-vector-baseline.md](stage-1-vector-baseline.md) through [stage-5-chunk-representation.md](stage-5-chunk-representation.md).

---

## 1. Final system

```
gather.py   facet-partitioned scrape of the WorkSafe publications catalogue
            -> urls.jsonl   1,975 of 2,281 documents (87%) with type/topic metadata

fetch.py    resumable download, %PDF- magic-byte validation, retry on 429/5xx
            -> data/raw/    1,913 PDFs, 1.6 GB

rag.py      load    PyMuPDF, sorted, pages joined on form feed
            chunk   page-bounded, 300 words / 50 overlap, min 20
                    -> 41,594 chunks
            embed   bge-small-en-v1.5, unit-normalised   -> (41594, 384) float32, 64 MB
            search  vector (brute force) + BM25 (SQLite FTS5), fused by RRF,
                    top 50 reranked by ms-marco-MiniLM-L-6-v2 cross-encoder
            answer  claude-haiku-4-5, grounded prompt, forced citations,
                    refusal when unsupported, max_tokens 1000
```

Performance

| | conceptual | identifier | aggregate |
|---|---|---|---|
| hit@1 | 0.700 | 0.600 | 0.657 |
| hit@5 | 0.950 | 0.800 | 0.886 |
| MRR | 0.815 | 0.698 | 0.765 |

Retrieval 9 ms, +201 ms for reranking. Generation ~$0.004/query.
Full index rebuild ~10 minutes on an RTX 2060.

---

## 2. Results across five stages

```
                     stage 1   stage 2   stage 3   stage 4   stage 5
                     vector    hybrid    routed    +rerank   headers
aggregate  hit@5      0.543     0.686     0.714     0.886    rejected
aggregate  hit@1      0.143     0.286     0.371     0.657    rejected
aggregate  MRR        0.293     0.459     0.510     0.765    rejected
conceptual hit@1      0.200     0.450     0.450     0.700    rejected
identifier hit@5      0.067     0.400     0.467     0.800    rejected
```

| Stage | Intervention | Outcome |
|---|---|---|
| 1 | vector-only baseline | - |
| 2 | BM25 + RRF hybrid | adopted |
| 2b | contextual headers | rejected |
| 3 | query routing to BM25 | adopted, then retired in stage 4 |
| 4 | cross-encoder reranking | adopted |
| 5 | contextual headers, retested | rejected again |

Identifier retrieval went from 1-in-15 to 12-in-15 and aggregate MRR more than
doubled.

---

## 3. Statistical honesty

The stages are compared on the same 45 questions, so the correct test is a
paired one. McNemar's test on `hit@5`, n = 35 answerable:

| Transition | b | c | delta | p | |
|---|---|---|---|---|---|
| stage 1 -> 2 (hybrid) | 1 | 6 | +0.143 | 0.125 | not significant |
| stage 2 -> 3 (routing) | 1 | 2 | +0.029 | 1.000 | not significant |
| stage 3 -> 4 (reranking) | 1 | 7 | +0.171 | 0.070 | not significant |
| stage 1 -> 4 (cumulative) | 1 | 13 | +0.343 | 0.0018 | significant |

No individual stage clears p < 0.05, however the cumulative improvement does so
comfortably.

This is the most important number in the project and it should be reported
alongside every other figure. The golden set can detect that the system as a
whole got substantially better; it cannot reliably attribute that to any single
change. Stage 3 in particular (p = 1.000) is indistinguishable from noise.

95% Wilson intervals at current size show why:

```
aggregate hit@5    n=35   0.886   [0.741, 0.955]   width 0.214
conceptual hit@5   n=20   0.950   [0.764, 0.991]   width 0.227
identifier hit@5   n=15   0.800   [0.548, 0.930]   width 0.381
```

An identifier `hit@5` of 0.800 has a plausible range from 0.55 to 0.93. Every
per-stage figure in this project should be read with that in mind.

What this does not undermine: the direction and magnitude of the total
improvement, which is solid. What it does undermine: any claim that a
specific stage delivered a specific amount.

---

## 4. What worked, and what didn't

All of the measured gains came from retrieval architecture rather than from chunk
representation.

Hybrid search and reranking did the work. Contextual headers were tested in two
variants under two different architectures across four rebuilds and never beat
plain text, and the reason changed between architectures (recall damage
under vector-only, ranking damage under reranking) while the verdict did not.

Query routing is the instructive case. It was justified by a real measured gap
(RRF diluting the keyword signal), delivered a real improvement, and was then
made actively harmful by the stage 4 reranker - routing shrinks the
candidate pool, and a cross-encoder would rather have more candidates and sort
them itself. Retired, with the code kept for reproducibility.


---

## 5. Method

Ground truth independent of the system under test. Labels came from literal
string matching or from reading the PDF and looking up chunks by page - never
from running `search()` and labelling what came back, which builds a test the
system passes by construction.

Segmented reporting. Aggregate `hit@5` moved 0.543 -> 0.686 when BM25 was
added. That single number conceals a 6x improvement in one segment and none in
the other. A single average would have made the largest result in the project
look like a modest 26% gain.

Stopping rules set before runs. Stage 5's adoption threshold was fixed in
advance; without it, `title+heading` would have been adopted on the strength of
conceptual `hit@5` reaching 1.000 while ignoring the MRR drop.

Controls for confounds. Stage 2's header experiment accidentally changed
text extraction as well as adding headers. A control run (new extraction,
headers off) reproduced the baseline exactly, proving the extraction change was
inert and the delta was attributable to headers alone.

Three methodology failures, recorded rather than hidden: a confound
introduced one stage after warning against confounds; a cheap similarity proxy
that predicted the wrong winner twice; and `python ... | grep` masking a crashed
build behind grep's exit status.

---

## 6. Limitations

BLOCKING - retrieval cannot signal failure. Cosine similarity always returns
a top-k; there is no "no results". The system refuses only because the prompt
instructs it to. A similarity threshold is not available: unanswerable queries
scored higher (0.732) than answerable identifier queries (0.702) at stage 1,
and the score scale has since changed four times (cosine -> BM25 -> RRF ->
cross-encoder logits). No threshold survives a change of retrieval method.

BLOCKING - generation has never been measured. Retrieval went 0.543 ->
0.886. Answer quality has no numbers attached at all and is plausibly now the
weaker half.

KNOWN - everything measured is synthetic. The golden set, the router probe
and the realistic-query set were all written by the person who built the system.

KNOWN - 3 of 15 identifier questions still fail, against a candidate-pool
ceiling of 0.933.

KNOWN - chunk size never varied. 300/50 was chosen in stage 1 relative to
the median page and never tested. The most obvious untested variable.

KNOWN - `top_gap` is not scale-free and is meaningless across stages.

ACCEPTED - chunks and vectors coupled by position. Nothing enforces that row
i of the embedding array corresponds to `chunks[i]`.

ACCEPTED - no access control. Every chunk is visible to every caller. Any
multi-user deployment must push identity-derived filters into the search
query, never apply them after the model has seen content. A correctness
requirement, not an optimisation.

---

## 7. Improving the golden set

The golden set is the instrument, and §3 shows it is now the binding constraint:
it can no longer resolve the size of change the system produces per stage.
Further retrieval tuning without a better instrument is not measurable.

### 7.1 Size - the first-order problem

At n = 35 answerable questions, one question flipping is worth 0.029 on the
aggregate. A rough power calculation for detecting a 0.05 change at 80% power
around p = 0.886 gives ~600 questions. That is a target, not a requirement - 
but the direction is clear, and 150 to 200 would already halve the current
interval widths.

Cheapest route to scale: the corpus contains 7,936 question-shaped sentences
already written by WorkSafe authors, each sitting in the chunk that answers it.
`golden.py mine` surfaces them. They must be rephrased before use (verbatim they
hand BM25 a free lexical match), but that is minutes per question, not hours.

### 7.2 Continuous metrics have more statistical power

`hit@5` is binary, which wastes information: a question whose answer moved from
rank 8 to rank 6 counts as a zero both times. MRR and nDCG are continuous, and a
paired Wilcoxon signed-rank test on per-question MRR would detect smaller
changes than McNemar on `hit@5` at the same n.

Reporting per-stage significance on MRR rather than `hit@5` is free and should
be done first, before adding a single question.

### 7.3 Missing segments

Currently conceptual (20), identifier (15), unanswerable (10). Absent:

- Procedural - "how do I safely do X". Different retrieval profile: answers
  are usually step lists rather than definitions.
- Multi-hop - answers spanning two or more documents. Nothing currently
  measures multi-document reasoning, and it is the segment most likely to expose
  weaknesses in the current architecture.
- Messy/realistic - short fragments (`"asbestos ppe"`), typos, acronyms
  (SWMS, JSA), conversational follow-ups. Every existing question is a
  well-formed sentence, so nothing measures what real users type.
- Near-miss negatives - questions the corpus almost answers, to test
  whether the system over-claims on partial evidence.

### 7.4 Ground truth quality

Literal phrase matching is biased. A question labelled on the phrase
"available within ten seconds" has ground truth consisting only of chunks
containing that phrase. A chunk that answers the question in different words
is scored as a miss, which systematically penalises the vector channel and
flatters BM25. The `find_by_page` workflow (read the PDF, ground on the page)
avoids this and should be the default for new questions.

Graded relevance instead of binary. Marking chunks 0 / 1 / 2 (irrelevant /
partially useful / fully answers) would let nDCG distinguish "found a related
passage" from "found the answer". Currently both score identically.

Ground-truth set sizes distort recall. Identifier questions have 7 to 8 correct
chunks each, capping `recall@5` near 0.6 regardless of retrieval quality. Either
cap ground truth at ~5 chunks or report `hit@k` and nDCG only for those
segments.

### 7.5 Independence

Single annotator. Every question was written by one person, who also built
the system and knew its weaknesses. Questions written by a domain expert with no
knowledge of the implementation would be harder and more representative.

Inter-annotator agreement. Have a second person label ground truth for 30
questions and report Cohen's kappa. If two people disagree about what answers a
question, the metric has a noise floor that no amount of tuning can beat - and
knowing that floor is more useful than another decimal place.

Match the evaluation set to the component under test. The identifier
segment was auto-generated from regex patterns, so the stage 3 regex router
matched it by construction. Any component whose logic overlaps with how the
questions were generated needs its own held-out set -- which is what
`router_probe.jsonl` provides.

### 7.6 Versioning discipline

`golden_set_v1.jsonl` stayed frozen across all five stages, which is what makes
the stage comparisons valid at all. Additions should create `v2` with a
changelog, and any figure quoted should name the set version alongside the index
fingerprint.

### 7.7 The real gap

Query logs. Everything above improves a synthetic instrument. Fifty real
questions from actual duty holders would be worth more than five hundred
invented ones, because they carry the distribution - what people actually ask,
how they phrase it, and how often the answer isn't in the corpus at all.

Until then, every number in this project should be read as *"on questions we
wrote ourselves"*.

---
