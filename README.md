# worksafe-rag

A retrieval-augmented generation system over New Zealand workplace health and safety guidance, built and improved across six measured stages.

It answers questions about WorkSafe's published guidance with citations to an exact document and page, and declines when the corpus does not support an answer.

Corpus: 1,913 PDFs harvested from the public [WorkSafe publications catalogue](https://www.worksafe.govt.nz/publications-and-resources/), including 59 Approved Codes of Practice and 40 Safe Work Instruments, which carry legal force under HSWA 2015.

### Full write-up: [docs/results-summary.md](docs/results-summary.md), per-stage records in [docs/](docs/)

---

## Key results

| | conceptual | identifier | aggregate |
|---|---|---|---|
| hit@1 | 0.700 | 0.600 | 0.657 |
| hit@5 | 0.950 | 0.800 | 0.886 |
| MRR | 0.815 | 0.698 | 0.765 |

Across six stages, aggregate hit@5 went from 0.543 to 0.886 and identifier retrieval went from 1-in-15 to 12-in-15 questions answered.

- No individual stage is statistically significant. McNemar paired tests on the same 45 questions give p = 0.125, 1.000 and 0.070 for the three adopted changes. The cumulative stage 1 to stage 4 change gives p = 0.0018. The evaluation set can detect that the system improved overall but cannot attribute that to any single change, and every per-stage figure should be read that way.
- All measured gains came from retrieval architecture. None came from chunk representation. Contextual headers were tested in two variants under two different architectures and never beat plain text. Chunk size was varied across a 4x range with no significant difference.
- Query routing was adopted in stage 3 and retired in stage 4. Reranking did not merely make it redundant, it made it harmful: identifier hit@5 was 0.733 routed against 0.800 unrouted, because routing shrinks the candidate pool a reranker would rather sort itself.
- Generation quality was measured separately and had never been scored before stage 6: grounded 100%, citations 91%, modality 90%, refusal 100%. The two modality failures report a source's "should" as a "must", which is materially wrong in a corpus where WorkSafe defines the difference as legal requirement versus recommended practice, and which no retrieval metric can detect.

---

## How it works

### Corpus acquisition

`gather.py`. The publications listing caps at 1,000 results despite advertising 2,281, so each facet value (publication type, topic, industry) is paged separately through `/publications-and-resources/FilterSearchForm/` and the union deduplicated on doc_id. That recovers 1,975 of 2,281 documents. Harvesting per facet also establishes each document's types, topics and industries authoritatively, including for the roughly 17% where the listing text omits them.

`fetch.py`. Downloads with a 1.5 s delay, automatic retry on 429/5xx via HTTPAdapter, and resume on restart. It validates the `%PDF-` magic bytes rather than the status code, because a 200 can still be an HTML error page and without that check corruption surfaces as a parse failure two stages later.

### Indexing, in rag.py

`load()` uses PyMuPDF and reads files in sorted order. Sorting matters: glob order is filesystem-dependent, and chunk IDs derived from an unstable document order would point at different text between runs, invalidating the evaluation set with no error. Pages are joined with a form feed so page boundaries stay recoverable, which is what makes page-level citation possible.

`chunk()` produces page-bounded windows of 300 words with 50 overlap, dropping pages under 20 words. Page-bounded means a chunk never spans a page break, so the page number is exact. 300 words was chosen relative to the corpus rather than by taste: the median page is 262 words, so most pages become exactly one chunk and the sliding-window path rarely fires. Chunk IDs are zero-padded and were verified stable across rebuilds by hashing the full ID sequence.

`embed()` uses bge-small-en-v1.5 at 384 dimensions with `normalize_embeddings=True`. Unit vectors mean the dot product is cosine similarity, so search is one matrix multiply. BGE models are asymmetric: queries take a prefix and passages take none, and omitting it degrades retrieval with no error. The function also counts chunks exceeding the 512-token limit rather than letting them truncate silently. 1,554 do, almost all contents pages whose dot leaders tokenise at around 18 tokens per word against a normal 1.3.

`build_index()` caches chunks, vectors, the BM25 index and a manifest. The cache key is a fingerprint hashing filenames and sizes via `stat()`, together with chunk size, overlap, minimum chunk words, the embedding model and the header mode. A file count would catch a growing corpus but not a changed chunk size, which fails silently with plausible-looking results. Caching turns a 10 minute rebuild into 0.06 s.

### Retrieval

```
query
 |- vector search   brute-force cosine over (41594, 384), argpartition top 50
 |- BM25            SQLite FTS5, porter unicode61, top 50
        v
   RRF fusion       score = sum of 1/(60 + rank)
        v
   cross-encoder    ms-marco-MiniLM-L-6-v2 rescores all 50
        v
   top 6
```

Brute force rather than an approximate index. 41,594 x 384 float32 is 64 MB, small enough that an exhaustive scan is exact and faster than a graph walk. An ANN index only earns its complexity past roughly 500k chunks. Measured at about 9 ms.

RRF fuses two channels whose scores are incomparable, cosine sitting in 0 to 1 and BM25 unbounded and reaching 22 on these queries. It discards the scores and uses only rank position, so it needs no calibration.

The cross-encoder is where the ranking comes from. The retriever is a bi-encoder: query and chunk are embedded separately and never meet, so each chunk was compressed into 384 numbers without knowing the question. That is what makes it fast, and it is also why its scores clustered 0.014 apart and barely discriminated. A cross-encoder feeds query and chunk through a transformer together so attention runs across both. It is far more accurate and far too slow for the whole corpus, so the pattern is bi-encoder for cheap recall over everything and cross-encoder for expensive precision over the survivors.

### Generation

`claude-haiku-4-5` with a grounded prompt: cite a source number for every claim, use only the supplied sources, say plainly when they do not contain the answer. `max_tokens=1000` acts as a hard per-call spend cap since output bills at 5x input. Empty retrieval returns a refusal without calling the API, because no context means the model could only answer from its own weights, which is the failure mode the system exists to avoid.

Citations resolve to real document titles by joining doc_id back to the harvest metadata, so a source reads "Approved Code of Practice for Cranes, p. 75" rather than a filename.

---

## The staged iteration

Every change was measured against a frozen 45-question golden set before adoption, and each stage produced its own record.

| Stage | Intervention | Outcome | aggregate hit@5 |
|---|---|---|---|
| 1 | vector-only baseline | | 0.543 |
| 2 | BM25 + RRF hybrid | adopted | 0.686 |
| 2b | contextual headers | rejected | |
| 3 | query routing to BM25 | adopted, later retired | 0.714 |
| 4 | cross-encoder reranking | adopted | 0.886 |
| 5 | contextual headers, retested | rejected again | |
| 6 | generation quality, chunk size sweep | no change adopted | |

[Stage 1](docs/stage-1-vector-baseline.md) established the vector-only baseline. Segmented reporting immediately exposed a system that was strong at one thing and broken at another: conceptual hit@5 0.900, identifier hit@5 0.067. Asked what Regulation 47 requires, six chunks contained the literal string and none appeared in the top 20. Embeddings place Regulation 47 and Regulation 92 at nearly the same point because the distinguishing feature is an arbitrary integer.

[Stage 2](docs/stage-2-hybrid-retrieval.md) added BM25 and RRF, taking identifier hit@5 from 0.067 to 0.400. Aggregate moved only 0.543 to 0.686, which understates it badly and is the strongest argument in the project for segmented reporting. Contextual headers were tested in the same stage and rejected: they raised intra-document similarity from 0.748 to 0.817, crowding the top-5 with neighbours from the same document.

[Stage 3](docs/stage-3-query-routing.md) added query routing. Stage 2 had revealed a crossover where keyword-only beat hybrid on identifiers, 0.467 against 0.400, because RRF weights both channels equally and the vector channel's confident but irrelevant results dragged good ones down. A regex router sent identifier-shaped queries to BM25 alone and recovered the gap. Router accuracy was measured on a separate probe set, since the golden set's identifier segment was auto-generated from the same pattern class and would match by construction. Accuracy on realistic messy queries was 80%.

[Stage 4](docs/stage-4-reranking.md) added cross-encoder reranking, the largest gain in the project: aggregate hit@1 from 0.371 to 0.657, identifier hit@5 from 0.467 to 0.800. It also retired the stage 3 router, which had been predicted in the previous document and turned out worse than predicted.

[Stage 5](docs/stage-5-chunk-representation.md) retested contextual headers, since the stage 2 rejection had been measured under a retrieval architecture that no longer existed. Rejected again, and informatively: the mechanism changed from recall damage under vector-only to ranking damage under reranking, while the verdict did not.

[Stage 6](docs/stage-6-generation-and-chunk-size.md) measured generation quality for the first time and swept chunk size across 150/25, 300/50 and 600/100. 300/50 scored highest but no difference was significant even under the most generous assumption.

### Method

- Ground truth is independent of the system under test. Labels come from literal string matching or from reading the PDF and looking up chunks by page, never from running `search()` and labelling what came back.
- Stopping rules were set before runs. Stage 5's adoption threshold was fixed in advance; without it, one variant would have been adopted on the strength of conceptual hit@5 reaching 1.000 while ignoring a drop in MRR.
- Confounds got controls. Stage 2's header experiment accidentally changed text extraction as well as adding headers. A control run reproduced the baseline exactly, proving the extraction change was inert.
- Three methodology failures are recorded rather than hidden: a confound introduced one stage after warning against confounds, a cheap similarity proxy that predicted the wrong winner twice, and `python ... | grep` masking a crashed build behind grep's exit status.

---

## Running it

```bash
py -3.13 -m venv .venv
.venv/Scripts/python.exe -m pip install torch --index-url https://download.pytorch.org/whl/cu124
.venv/Scripts/python.exe -m pip install -r requirements.txt
```

Copy `.env.example` to `.env` and add `ANTHROPIC_API_KEY`. Retrieval needs no key, only `answer()` does.

```bash
python gather.py                      # harvest the catalogue, ~9 min
python fetch.py --guidance-only       # download PDFs, ~20 min
python rag.py                         # build index and run demo queries
python rag.py --rebuild               # force a rebuild

python golden.py run                  # evaluate against the golden set
python golden.py probe                # router accuracy on held-out queries
python golden.py text "Regulation 14" # find chunks containing a literal
python golden.py page 20109 16        # find chunks on a page
python build_golden.py                # regenerate the golden set
python generate_answers.py            # generate answers and a labelling sheet
python score_answers.py               # score the filled-in sheet
python sweep_chunks.py                # chunk size sweep
```

Hardware used: RTX 2060 (6 GB), Ryzen 7 9800X3D. Embedding runs at about 162 chunks/sec on GPU against 20/sec on CPU. A full rebuild takes about 10 minutes; a cached load takes 0.06 s.

---

## Layout

```
rag.py                 load / chunk / embed / index / hybrid search / rerank / answer
gather.py              facet-partitioned catalogue scrape
fetch.py               resumable PDF download with magic-byte validation
metrics.py             recall@k, hit@k, MRR, nDCG@k, segmented reporting
golden.py              ground-truth lookup, question mining, eval runner, router probe
build_golden.py        regenerates the golden set
generate_answers.py    generates answers and a labelling sheet for generation eval
score_answers.py       scores the filled-in labelling sheet
sweep_chunks.py        chunk-size sweep with per-variant reground

docs/
  stage-1-vector-baseline.md            vector-only baseline
  stage-2-hybrid-retrieval.md           BM25 + RRF          (adopted)
  stage-3-query-routing.md              query routing       (adopted, later retired)
  stage-4-reranking.md                  cross-encoder       (adopted)
  stage-5-chunk-representation.md       contextual headers  (rejected)
  stage-6-generation-and-chunk-size.md  generation quality and chunk sweep
  results-summary.md                    cross-stage summary and limitations

eval/
  golden_set_v1.jsonl    45 questions: 20 conceptual, 15 identifier, 10 unanswerable
  router_probe.jsonl     35 held-out queries for router accuracy
  answers.jsonl          45 generated answers with their sources
  label_sheet.md         generation labels, one block per answer
  chunk_sweep.json       chunk-size sweep results

data/
  urls.jsonl             1,975 documents with type/topic/industry metadata (committed)
  raw/                   1,913 PDFs, 1.6 GB          (gitignored, rebuildable)
  index/                 chunks, vectors, BM25, manifest, 272 MB (gitignored)
```

---

## Limitations

Full accounting in [docs/results-summary.md](docs/results-summary.md). The ones that matter most:

Retrieval cannot signal failure. Cosine similarity always returns a top-k, so there is no "no results" state. The system refuses only because the prompt instructs it to. A similarity threshold is not available: unanswerable queries scored higher (0.732) than answerable identifier queries (0.702), and the score scale has changed four times across stages.

Everything measured is synthetic. The golden set, the router probe and the realistic-query set were all written by the person who built the system. Real query logs remain the largest gap.

Generation labels are LLM-scored with a human spot-check rather than independently hand-labelled throughout. Agreement was 6 of 7 items.

No access control. Every chunk is visible to every caller. Any multi-user deployment must push identity-derived filters into the search query rather than applying them after the model has seen content. This is a correctness requirement, not an optimisation.

Nothing is deployed, and the golden set at 45 questions cannot resolve differences of the size the later stages produce.

---

Corpus is WorkSafe New Zealand published guidance, harvested from the public catalogue. Most NZ government content is released under [NZGOAL](https://www.data.govt.nz/toolkit/policies/nzgoal/) (CC BY).
