# Stage 1 Baseline - worksafe-rag

Working end-to-end RAG pipeline over New Zealand workplace health and safety
guidance. Local retrieval, hosted generation, grounded citations to an exact page.

This is the measured baseline that every later change gets compared against.

Measured on 38 documents / 2,611 chunks. Hardware: RTX 2060 (6 GB, Turing),
Ryzen 7 9800X3D, 32 GB DDR5.

| | |
|---|---|
| chunks indexed | 2,611 |
| documents | 38 of ~750 guidance PDFs |
| retrieval latency | 7 to 16 ms |
| cost per answered query | ~$0.004 |
| embedding dims | 384 |

---

## 1. Pipeline

Two scripts build the corpus; one module runs the pipeline. Retrieval is entirely
local and free - only the final generation step calls a hosted model.

### 00 - Harvest (`gather.py`)

Scrapes the WorkSafe publications catalogue. The plain listing caps at 1,000
results, so each facet value (publication type, topic, industry) is paged
separately and the union deduplicated on `doc_id`.

Recovered 1,975 of 2,281 catalogued documents (87%).

```
-> urls.jsonl
   {url, doc_id, title, file_type, file_size, type, topic, description,
    facet_types, facet_topics, facet_industries}
```

### 01 - Download (`fetch.py`)

Fetches PDFs with a 1.5 s delay, automatic retry on 429/5xx, resume on restart.
Validates the `%PDF-` magic bytes rather than trusting the status code, a 200
can still be an HTML error page.

```
-> data/raw/*.pdf
```

### 02 - Load (`load()`)

PyMuPDF text extraction, files read in sorted order. Pages joined with a form
feed (`\f`) so page boundaries stay recoverable.

```
-> [{doc_id, filename, n_pages, text}]
   1,877 pages, 3.0 MB text, 473,697 words
```

### 03 - Chunk (`chunk()`)

Page-bounded windows of 300 words with 50 overlap. Pages under 20 words dropped
as covers and dividers. Chunk IDs zero-padded and stable across rebuilds.

```
-> [{chunk_id, doc_id, filename, page, text}]
   2,611 chunks, median 200 words, 80 near-empty pages dropped
```

### 04 - Embed (`embed()`)

`BAAI/bge-small-en-v1.5` on the GPU, unit-normalised so a dot product is cosine
similarity. Counts and reports chunks exceeding the 512-token limit rather than
letting them truncate silently.

```
-> ndarray(2611, 384) float32, 4.0 MB
```

### 05 - Search (`search()`)

One matrix multiply against every vector, then `argpartition` for the top-k.
Exact, not approximate. Only the query carries the BGE prefix.

```
-> [{...chunk, score}] ,  top_k = 6
```

### 06 - Answer (`answer()`)

Numbered sources with real document titles joined from the harvest metadata, a
grounding prompt requiring citations and refusal, hard output ceiling.

```
-> {text, hits, usage, cost}
```

---

## 2. Measured performance

Warm timings, excluding model load.

| Stage | Time | Rate | Notes |
|---|---|---|---|
| PDF parse | 2.1 s | 55 ms/file | ~41 s projected for 750 docs |
| Chunk | <1 s | - | string operations only |
| Embed (GPU) | 16.1 s | 162 chunks/s | 8.1x faster than CPU |
| Embed (CPU) | - | 20 chunks/s | a silent CUDA fallback = 43 min at full corpus |
| Search | 7 to 16 ms | - | exact brute force over 4 MB of vectors |
| Answer | ~3 s | - | 2,077 in / 340 out tokens, $0.0038 |

Projected at 750 documents: ~51,000 chunks, 75 MB vectors, ~6 min full
rebuild, retrieval still 50 to 100 ms.

---

## 3. Decisions and what they cost

Each was a fork with a real alternative. The trade-off matters more than the choice.

### Page-bounded chunking, joined on `\f`

Pages joined with a form feed at load time, split again at chunk time, so every
chunk knows its exact page. Citations read *"Approved Code of Practice for
Cranes, p. 75"* rather than naming a 288-page file.

Cost: a definition spanning pages 12 to 13 gets cut in half. Unmeasured so far.

### 300 words, 50 overlap

Chosen relative to the corpus, not by taste: median page is 262 words, so a
300-word target means most pages become exactly one chunk and the sliding-window
path rarely fires.

Cost: page-bounding rounds every page up to at least one chunk - 2,611 chunks
rather than the ~1,916 continuous windowing would give.

### Sorted file order

`glob` order is filesystem-dependent. Chunk IDs from an unstable document order
would silently point at different text between runs, invalidating any eval set
keyed to them - wrong results, no error. Verified stable by hashing the full ID
sequence across two runs.

Cost: none.

### Brute-force search, no ANN index

2,611 x 384 float32 is 4 MB - small enough to sit in CPU cache, where an
exhaustive scan is both exact and faster than a graph walk.

Cost: none at this scale. Revisit past ~500,000 chunks.

### Unit-normalised embeddings

Normalising at encode time makes the dot product identical to cosine similarity,
so the entire search is one matrix multiply with no per-query normalisation.

Cost: none.

### `doc_id` carried through every stage

Filename prefix is the join key back to harvest metadata, which supplies real
titles, publication types and topics. Also enables filtering the index by
document type later without re-scraping.

Cost: one extra field per chunk.

### Local retrieval, hosted generation

Retrieval is 90% of the work and runs free on the GPU. Only generation calls an
API, so retrieval experiments cost nothing. A small local model would be adequate
for extraction but is measurably worse at declining when sources don't support an
answer - the behaviour that matters most here.

Cost: ~$0.004 per answered query; retrieval evaluation stays free.

### Hard output ceiling 1,000 tokens, thinking disabled

Output bills at 5x input. `max_tokens` is a genuine per-call spend cap. Adaptive
thinking is both a Claude 4.6+ feature that Haiku 4.5 rejects and pure cost for
what is grounded extraction rather than reasoning.

Cost: answers longer than ~700 words would truncate. None observed.

---

## 4. Models

| Role | Model | Location | Cost |
|---|---|---|---|
| Embedding | `BAAI/bge-small-en-v1.5` | local GPU, 384 dims | free |
| Generation | `claude-haiku-4-5` | Anthropic API | $1 / $5 per Mtok |
| Reranking | - | not implemented | - |
| Keyword search | - | not implemented | - |

---

## 5. Known limitations

Every item is reproducible on the current build.

### BLOCKING - Exact identifiers are unretrievable

Vector search cannot rank section numbers, regulation numbers or table
references. Embeddings place `Regulation 9` and `Regulation 13` at nearly the
same point because they occur in near-identical linguistic contexts. The
distinguishing feature is an arbitrary integer, and semantic similarity has no
purchase on arbitrary integers.

```
query "Regulation 9"  ->  6 chunks contain the literal string
                      ->  0 appear in the top 20
top scores 0.674 / 0.673 / 0.670  - a flat cluster, i.e. no discrimination
```

### BLOCKING - Retrieval cannot signal failure

Cosine similarity always returns a top-k. There is no "no results" - something is
always most similar, however irrelevant. Asked about the minimum wage, retrieval
confidently returned codes of practice on isocyanates, tractor safety and sulphur
fires. The system refused correctly, but only because the prompt instructed it
to. Refusal is a property of one prompt instruction, not of the architecture.

Candidate fix: a similarity floor below which `search()` returns nothing. Good
query scores ~0.87; junk query scores materially lower. Threshold unvalidated.

### KNOWN - Chunks do not know where they sit

No contextual header is prepended before embedding, so a chunk reading "This does
not apply where subsection (2) is satisfied" is retrievable and useless.

Visible in results: a query about a PCBU's duties at height returned an example
scenario, a passage on casual volunteers, and the introduction, scoring 0.792,
0.792 and 0.791.

### KNOWN - Contents pages survive the junk filter

Tables of contents pass the 20-word minimum but tokenise catastrophically - dot
leaders produce 18.5 tokens per word against a normal 1.3.

```
26 of 2,611 chunks exceed 512 tokens
worst case 4,486 tokens from 242 words
```

### OUTSTANDING (stage 1) - Corpus is 5% downloaded

38 of ~750 guidance PDFs on disk. Harvest itself reached 1,975 of 2,281
catalogued documents; the missing 306 have no facet at all and fall beyond the
listing's 1,000-result cap. They skew administrative. See §6.

### ACCEPTED - Chunks and vectors coupled by position

Row i of the embedding array corresponds to `chunks[i]` and nothing enforces
it. Reordering one without the other produces silently wrong results with no
error. Acceptable in a single-file baseline; first thing to fix on refactor.

### OUTSTANDING (stage 1) - No index caching

Every run re-parses and re-embeds the whole corpus: 35 s at 38 documents,
projected ~6 min at 750. Deferred deliberately so the cost of the rebuild loop
was felt before it was engineered away. Now due - see §6.

### ACCEPTED - No access control

Every chunk is visible to every caller. Not a defect in a single-user prototype,
but any multi-user deployment must push identity-derived filters into the
search query rather than applying them after the model has seen the content.
This is a correctness requirement, not an optimisation.

### VERIFIED - Grounded refusal works

Asked a question entirely outside the corpus, the system declined and
characterised what it did have, rather than answering from model weights. Given
the corpus includes 59 Approved Codes of Practice and 40 Safe Work Instruments - 
instruments carrying legal force - this is the behaviour that matters most.

---

## 6. Stage 1 - outstanding

Stage 1 is not complete. Four pieces of work remain, and the order matters.

1. Complete the corpus download.
38 of ~750 guidance PDFs are on disk. Everything in §2 is measured against 5% of
the corpus and will move substantially once the rest lands.

2. Cache the index.
the rebuild loop stops costing minutes. Needs a real invalidation signal - 
hash the sorted filenames plus `CHUNK_WORDS`, `CHUNK_OVERLAP` and `EMBED_MODEL`,
and rebuild when that hash moves. A naive cache serves a stale index forever
after the corpus grows, and a stale index gives wrong answers with no error.

3. Build the golden set and metrics harness.
50 to 100 real questions with known-correct chunk IDs, segmented by kind
(identifier / conceptual / multi-hop / unanswerable), plus recall@k, MRR and
nDCG. This is the instrument and the largest remaining piece: hours of
genuine labelling work, not an afternoon of scripting.

Must come after the download. Chunk IDs are stable, but a question labelled
against a 38-document index can only reference chunks from those 38 files, and
the correct answer for most questions lives in a document not yet on disk.

4. Take the baseline measurement.

---

## 7. Staged improvement plan

Measurement is not a stage. It is what closes every stage.

| Stage | Work | Closes with |
|---|---|---|
| 1 | pipeline, corpus, cache, harness | baseline numbers |
| 2 | hybrid retrieval - contextual headers, BM25, RRF | measurement vs stage 1 |
| 3 | cross-encoder reranking over fused candidates | measurement vs stage 2 |
| 4 | corpus curation - guidance-only vs all 1,913 docs | measurement vs stage 3 |

Each stage produces one row of the improvement table and one document
(`stage-1-vector-baseline.md`, `stage-2-hybrid-retrieval.md`, …). The diff between consecutive documents is
the improvement story.

### Disciplines

One intervention per stage. If a stage adds contextual headers and BM25
and RRF and recall jumps 15 points, it is not possible to say which did it, and "we added
three things and it got better" is what every other write-up says. If changes are
bundled, measure incrementally within the stage so attribution survives.

Freeze the golden set before stage 2. Editing questions between runs
invalidates every comparison. Version it (`golden_set_v1.jsonl`); treat edits as
creating v2 with a note on what changed and why.

Record the full config with every measurement. Chunk size, overlap,
embedding model, top_k, corpus size. A bare `recall@5 = 0.71` is uninterpretable
in three months, and these are numbers worth quoting later.

### Why segmentation matters

Adding keyword search will barely move aggregate recall, because most questions
are conceptual and already handled, but on identifier queries it should move
recall from roughly zero to near one. Reported as a single average, the best
improvement in the project would look like noise.

Every retrieval metric is computed without calling any model, so the entire
measurement programme is free.

---

## Notes

<!-- space for your own notes below -->
