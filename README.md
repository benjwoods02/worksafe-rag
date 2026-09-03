# worksafe-rag

A retrieval-augmented generation system over New Zealand workplace health and
safety guidance, built and improved across five measured stages.

Answers questions about WorkSafe's published guidance with citations to an exact
document and page, and declines when the corpus does not support an answer.

Corpus: 1,913 PDFs harvested from the public
[WorkSafe publications catalogue](https://www.worksafe.govt.nz/publications-and-resources/),
including 59 Approved Codes of Practice and 40 Safe Work Instruments —
instruments carrying legal force under HSWA 2015.

### Full write-up: [results-summary.md](docs/results-summary.md) · per-stage records: [stage-1-vector-baseline.md](docs/stage-1-vector-baseline.md) → [stage-5-chunk-representation.md](docs/stage-5-chunk-representation.md)

---

## Key results

| | conceptual | identifier | aggregate |
|---|---|---|---|
| hit@1 | 0.700 | 0.600 | 0.657 |
| hit@5 | 0.950 | 0.800 | **0.886** |
| MRR | 0.815 | 0.698 | 0.765 |

Across five stages, aggregate `hit@5` went **0.543 → 0.886** and identifier
retrieval went from **1-in-15 to 12-in-15** questions answered.

**The caveat that matters.** McNemar paired tests on the same 45 questions show
that *no individual stage* clears p < 0.05 — but the cumulative stage 1 → 4
change does, at **p = 0.0018**. The evaluation set can detect that the system
improved overall; it cannot reliably attribute that to any single change. Every
per-stage figure below should be read with that in mind.

**The headline finding.** All measured gains came from **retrieval
architecture** — hybrid search and reranking. None came from **chunk
representation**: contextual headers were tested in two variants under two
different architectures, across four rebuilds, and never beat plain text.

---

## How it works

### Corpus acquisition

**`gather.py`** — the publications listing caps at 1,000 results (`?start=1000`
returns nothing) despite advertising 2,281. Each facet value (publication type,
topic, industry) is paged separately through
`/publications-and-resources/FilterSearchForm/` and the union deduplicated on
`doc_id`, recovering **1,975 of 2,281** documents. Harvesting per facet has a
second payoff: it establishes each document's types, topics and industries
authoritatively, including for the ~17% where the listing text omits them.

**`fetch.py`** — downloads with a 1.5 s delay, automatic retry on 429/5xx via
`HTTPAdapter`, and resume-on-restart. Validates the `%PDF-` **magic bytes**
rather than the status code: a 200 can still be an HTML error page, and without
this check corruption surfaces as a baffling parse failure two stages later.

### Indexing — `rag.py`

**`load()`** — PyMuPDF extraction, files read in `sorted()` order. Sorting is
load-bearing: `glob` order is filesystem-dependent, and chunk IDs derived from an
unstable document order would silently point at different text between runs,
invalidating the evaluation set with no error. Pages are joined with a **form
feed**, which keeps page boundaries *recoverable* — `text.split("\f")` gives the
page list back, and that is what makes page-level citation possible.

**`chunk()`** — page-bounded windows of 300 words with 50 overlap, dropping
pages under 20 words (covers, dividers — 4% of pages). Page-bounded means a
chunk never spans a page break, so `page` is exact. 300 words was chosen
relative to the corpus, not by taste: the median page is 262 words, so most
pages become exactly one chunk and the sliding-window path rarely fires. Chunk
IDs are zero-padded (`{doc_id}-{ordinal:05d}`) and verified stable across
rebuilds by hashing the full ID sequence.

**`embed()`** — `bge-small-en-v1.5`, 384 dims, `normalize_embeddings=True`.
Unit vectors mean the dot product *is* cosine similarity, so search is one matrix
multiply with no per-query normalisation. BGE models are **asymmetric**: queries
take a prefix, passages take none — omitting it degrades retrieval with no
error. The function also counts chunks exceeding the 512-token limit rather than
letting them truncate silently (1,554 do, almost all contents pages whose dot
leaders tokenise at ~18 tokens/word against a normal 1.3).

**`build_index()`** — caches `chunks.json`, `vectors.npy`, `fts.sqlite` and a
`manifest.json`. The cache key is a **fingerprint** hashing filenames and sizes
(via `stat()`, so the check costs milliseconds) *together with* `CHUNK_WORDS`,
`CHUNK_OVERLAP`, `MIN_CHUNK_WORDS`, `EMBED_MODEL` and `HEADER_MODE`. A file
count would catch a growing corpus but not "I changed chunk size and forgot" —
which fails silently, with plausible-looking results. Turns a 10-minute rebuild
into 0.06 s.

### Retrieval

```
query
 ├─ vector search   brute-force cosine over (41594, 384), argpartition top 50
 └─ BM25            SQLite FTS5, porter unicode61, top 50
        ↓
   RRF fusion       score = Σ 1/(60 + rank)
        ↓
   cross-encoder    ms-marco-MiniLM-L-6-v2 rescores all 50
        ↓
   top 6
```

**Brute force, not ANN.** 41,594 × 384 float32 is 64 MB — small enough that an
exhaustive scan is exact *and* faster than a graph walk. An approximate index
only earns its complexity past roughly 500k chunks. Benchmarked at ~9 ms.

**RRF** fuses channels whose scores are incomparable (cosine 0–1, BM25 unbounded
and reaching 22). It discards the scores entirely and uses only rank position,
so it needs no calibration.

**The cross-encoder** is where the ranking comes from. The retriever is a
*bi-encoder*: query and chunk are embedded separately and never meet, so each
chunk was compressed into 384 numbers without knowing the question — fast, but
its scores clustered 0.014 apart, barely discriminating. A cross-encoder feeds
query and chunk through a transformer *together*, so attention runs across both.
Far more accurate, far too slow for the whole corpus. Hence: bi-encoder for cheap
recall over everything, cross-encoder for expensive precision over the survivors.

### Generation

`claude-haiku-4-5` with a grounded prompt: cite a source number for every claim,
use only the supplied sources, say plainly when they do not contain the answer.
`max_tokens=1000` acts as a hard per-call spend cap (output bills at 5× input).
Empty retrieval returns a refusal **without calling the API** — no context means
the model could only answer from its own weights, which is the failure mode the
system exists to avoid.

Citations resolve to real document titles by joining `doc_id` back to the
harvest metadata, so sources read *"Approved Code of Practice for Cranes,
p. 75"* rather than a filename.

---

## The staged iteration

Every change was measured against a frozen 45-question golden set before
adoption, and each stage produced its own record.

| Stage | Intervention | Outcome | aggregate hit@5 |
|---|---|---|---|
| 1 | vector-only baseline | — | 0.543 |
| 2 | BM25 + RRF hybrid | **adopted** | 0.686 |
| 2b | contextual headers | rejected | — |
| 3 | query routing to BM25 | adopted, later **retired** | 0.714 |
| 4 | cross-encoder reranking | **adopted** | **0.886** |
| 5 | contextual headers, retested | rejected again | — |

**Stage 1 — [stage-1-vector-baseline.md](docs/stage-1-vector-baseline.md).** Vector-only. Segmented reporting
immediately exposed a system that was excellent at one thing and broken at
another: conceptual `hit@5` 0.900, identifier `hit@5` 0.067. Asked *"what does
Regulation 47 require"*, six chunks contained the literal string and **none
appeared in the top 20** — embeddings place `Regulation 47` and `Regulation 92`
at nearly the same point because the distinguishing feature is an arbitrary
integer, and semantic similarity has no purchase on those.

**Stage 2 — [stage-2-hybrid-retrieval.md](docs/stage-2-hybrid-retrieval.md).** BM25 + RRF. Identifier `hit@5`
0.067 → 0.400. Aggregate moved only 0.543 → 0.686, which *massively*
understates it — the strongest argument in the project for segmented reporting.
Contextual headers were tested in the same stage and **rejected**: they raised
intra-document similarity 0.748 → 0.817, crowding the top-5 with neighbours from
the same document.

**Stage 3 — [stage-3-query-routing.md](docs/stage-3-query-routing.md).** Query routing. Stage 2 revealed a
crossover — keyword-only *beat* hybrid on identifiers (0.467 vs 0.400) because
RRF weights both channels equally, so the vector channel's confident garbage
dragged good results down. A regex router sent identifier-shaped queries to BM25
alone, recovering the gap. Router accuracy was measured on a **separate probe
set**, since the golden set's identifier segment was auto-generated from the
same pattern class and would match by construction. Accuracy on realistic messy
queries: **80%**.

**Stage 4 — [stage-4-reranking.md](docs/stage-4-reranking.md).** Cross-encoder reranking. The
largest gain in the project: aggregate `hit@1` 0.371 → 0.657, identifier `hit@5`
0.467 → 0.800. It also **retired the stage 3 router**, which had been predicted
in the previous document and turned out to be worse than predicted — routing was
not merely redundant but *harmful* (identifier `hit@5` 0.733 routed vs 0.800
unrouted), because it shrinks the candidate pool and a reranker would rather
have more candidates and sort them itself.

**Stage 5 — [stage-5-chunk-representation.md](docs/stage-5-chunk-representation.md).** Contextual headers retested, since
the stage 2 rejection was measured under a retrieval architecture that no longer
existed. Rejected again — and informatively: the *mechanism* changed (recall
damage under vector-only, ranking damage under reranking) while the verdict did
not. A negative result surviving an architecture change is considerably more
robust than one that does not.

### Method

- **Ground truth independent of the system under test** — labels come from
  literal string matching or from reading the PDF and looking up chunks by page,
  never from running `search()` and labelling what came back.
- **Stopping rules set before runs.** Stage 5's threshold was fixed in advance;
  without it, `title+heading` would have been adopted on the strength of
  conceptual `hit@5` reaching 1.000 while ignoring an MRR drop.
- **Controls for confounds.** Stage 2's header experiment accidentally changed
  text extraction as well. A control run reproduced the baseline *exactly*,
  proving the extraction change was inert.
- **Failures recorded, not hidden** — a confound introduced one stage after
  warning against confounds; a cheap similarity proxy that predicted the wrong
  winner twice; `python … | grep` masking a crashed build behind grep's exit
  status.

---

## Running it

```bash
py -3.13 -m venv .venv
.venv/Scripts/python.exe -m pip install torch --index-url https://download.pytorch.org/whl/cu124
.venv/Scripts/python.exe -m pip install -r requirements.txt
```

Copy `.env.example` to `.env` and add `ANTHROPIC_API_KEY` (retrieval needs no
key — only `answer()` does).

```bash
python gather.py                      # harvest the catalogue -> urls.jsonl (~9 min)
python fetch.py --guidance-only       # download PDFs (~20 min)
python rag.py                         # build index + demo queries
python rag.py --rebuild               # force a rebuild

python golden.py run                  # evaluate against the golden set
python golden.py probe                # router accuracy on held-out queries
python golden.py text "Regulation 14" # find chunks containing a literal
python golden.py page 20109 16        # find chunks on a page
python build_golden.py                # regenerate the golden set
```

Hardware used: RTX 2060 (6 GB), Ryzen 7 9800X3D. Embedding runs at ~162
chunks/sec on GPU against 20/sec on CPU. Full rebuild ~10 minutes; cached load
0.06 s.

---

## Layout

```
rag.py                 load / chunk / embed / index / hybrid search / rerank / answer
gather.py              facet-partitioned catalogue scrape
fetch.py               resumable PDF download with magic-byte validation
metrics.py             recall@k, hit@k, MRR, nDCG@k, segmented reporting
golden.py              ground-truth lookup, question mining, eval runner, router probe
build_golden.py        regenerates the golden set
generate_answers.py    generates answers + labelling sheet for generation eval
score_answers.py       scores the filled-in labelling sheet
sweep_chunks.py        chunk-size sweep with per-variant reground

docs/
  stage-1-vector-baseline.md          vector-only baseline
  stage-2-hybrid-retrieval.md         BM25 + RRF          (adopted)
  stage-3-query-routing.md            query routing       (adopted, later retired)
  stage-4-reranking.md                cross-encoder       (adopted)
  stage-5-chunk-representation.md     contextual headers  (rejected)
  stage-6-generation-and-chunk-size.md generation quality + chunk sweep
  results-summary.md                  cross-stage summary and limitations

eval/
  golden_set_v1.jsonl    45 questions: 20 conceptual, 15 identifier, 10 unanswerable
  router_probe.jsonl     35 held-out queries for router accuracy
  answers.jsonl          45 generated answers with their sources
  label_sheet.md         generation labels, one block per answer
  chunk_sweep.json       chunk-size sweep results

data/
  urls.jsonl             1,975 documents with type/topic/industry metadata (committed)
  raw/                   1,913 PDFs, 1.6 GB          (gitignored, rebuildable)
  index/                 chunks, vectors, BM25, manifest — 272 MB (gitignored)
```

---

## Limitations

Full accounting in [results-summary.md](docs/results-summary.md) §6–8. The ones that
matter most:

**Retrieval cannot signal failure.** Cosine similarity always returns a top-k —
there is no "no results". The system refuses only because the prompt instructs
it to. A similarity threshold is unavailable: unanswerable queries scored
*higher* (0.732) than answerable identifier queries (0.702), and the score scale
has changed four times across stages.

**Generation has never been measured.** Retrieval went 0.543 → 0.886; answer
quality has no numbers attached and is plausibly now the weaker half.

**Everything measured is synthetic.** The golden set, the router probe and the
realistic-query set were all written by the person who built the system. Real
query logs remain the single largest gap.

**No access control.** Every chunk is visible to every caller. Any multi-user
deployment must push identity-derived filters *into* the search query, never
apply them after the model has seen content. A correctness requirement, not an
optimisation.

**Nothing is deployed**, and chunk size was never varied from the stage 1 choice.

---

Corpus is WorkSafe New Zealand published guidance, harvested from the public
catalogue. Most NZ government content is released under
[NZGOAL](https://www.data.govt.nz/toolkit/policies/nzgoal/) (CC BY).
