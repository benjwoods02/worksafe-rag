import hashlib
import json
import os
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

import numpy as np
import pymupdf


BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "raw"

# Read .env so ANTHROPIC_API_KEY is available from the VS Code Run button as
# well as the terminal. The Run button starts a fresh process and will NOT see
# a session-only variable exported in some other shell.
try:
    from dotenv import load_dotenv
    load_dotenv(BASE_DIR / ".env")
except ImportError:
    pass

# Form feed. Joining pages with this keeps the page boundaries RECOVERABLE:
# text.split(PAGE_SEPARATOR) gives the page list back, which is what makes
# page-level citations possible later. A plain newline join destroys them.
PAGE_SEPARATOR = "\f"


HEADING_RATIO = 1.15      # a line this much larger than body text is a heading
MAX_HEADING_CHARS = 90    # longer than this and it is a paragraph, not a title


def extract_pages(doc):
    """Page texts plus the section heading in effect on each page.

    Headings are found by FONT SIZE, not by regex. Numbered-heading patterns
    only cover ~21% of this corpus and pick up contents-page lines, whereas the
    size contrast is consistent: body text is 8.5pt and headings 10-14pt across
    otherwise unrelated publications. Absolute sizes vary between documents, so
    body size is computed per document and headings are found relative to it.

    Two levels are tracked. The most recent heading carries forward onto later
    pages until another replaces it, so a page of pure body text still knows
    which section it belongs to.
    """
    weights = Counter()          # size -> characters, to find the body size
    pages_seen = defaultdict(set)  # size -> pages it appears on
    page_lines = []

    for page_index, page in enumerate(doc):
        lines = []
        for block in page.get_text("dict")["blocks"]:
            # Merge consecutive same-size lines within a block. A heading
            # wrapped over two lines would otherwise be truncated to its tail
            # ("...removal?") instead of the whole title.
            for line in block.get("lines", []):
                text = "".join(span["text"] for span in line["spans"]).strip()
                if not text:
                    continue
                size = round(max(span["size"] for span in line["spans"]), 1)
                if lines and lines[-1][0] == size:
                    lines[-1] = (size, f"{lines[-1][1]} {text}")
                else:
                    lines.append((size, text))
                weights[size] += len(text)
                pages_seen[size].add(page_index)
        page_lines.append(lines)

    if not weights:
        return ["" for _ in page_lines], ["" for _ in page_lines]

    body = weights.most_common(1)[0][0]

    # A real heading level RECURS through the document. Cover-page display type
    # is the largest size in the file but appears on one page only -- taking the
    # two largest sizes made every page inherit the cover title.
    min_pages = max(3, len(page_lines) // 20)
    structural = [s for s in weights
                  if s >= body * HEADING_RATIO and len(pages_seen[s]) >= min_pages]
    heading_sizes = sorted(structural, reverse=True)
    level1 = heading_sizes[0] if heading_sizes else None
    level2 = heading_sizes[1] if len(heading_sizes) > 1 else None

    texts, headings = [], []
    current1 = current2 = ""
    for lines in page_lines:
        page_heading = " > ".join(p for p in (current1, current2) if p)
        for size, text in lines:
            if not (3 < len(text) <= MAX_HEADING_CHARS):
                continue
            if level1 is not None and size >= level1:
                current1, current2 = text, ""       # a new section resets the sub-section
            elif level2 is not None and size >= level2:
                current2 = text
            else:
                continue
            if not page_heading:                    # first heading seen on this page
                page_heading = " > ".join(p for p in (current1, current2) if p)
        headings.append(page_heading)
        texts.append("\n".join(text for _, text in lines))

    return texts, headings


def load():
    """Read every PDF in data/raw into memory.

    Returns a list of dicts. The doc_id is the filename prefix
    (73224-remote-and-isolated-work-safety-alert.pdf -> "73224"), which is the
    join key back to urls.jsonl for title, publication type and topics.

    `headings[i]` is the section heading in effect on page i+1.
    """
    documents = []
    failed = []

    # sorted() is load-bearing: glob order is filesystem-dependent, and chunk
    # IDs derived from an unstable document order would silently invalidate the
    # golden set between runs -- wrong answers, no error.
    for path in sorted(DATA_PATH.glob("*.pdf")):
        try:
            with pymupdf.open(path) as doc:
                n_pages = doc.page_count
                # Extract inside the with block; the Document is dead after it.
                page_texts, headings = extract_pages(doc)
                text = PAGE_SEPARATOR.join(page_texts)
        except Exception as exc:  # a corrupt file must not kill the whole run
            failed.append((path.name, str(exc)))
            continue

        documents.append({
            "doc_id": path.stem.split("-", 1)[0],
            "filename": path.name,
            "n_pages": n_pages,
            "text": text,
            "headings": headings,
        })

    if failed:
        print(f"! {len(failed)} file(s) failed to parse:")
        for name, error in failed[:5]:
            print(f"    {name}: {error}")

    pages = sum(d["n_pages"] for d in documents)
    chars = sum(len(d["text"]) for d in documents)
    print(f"loaded {len(documents)} documents, {pages} pages, {chars / 1e6:.1f} MB text")
    return documents



CHUNK_WORDS = 300       # just above the median page (262 words), so most
CHUNK_OVERLAP = 50      # pages become exactly one chunk and windowing is rare
MIN_CHUNK_WORDS = 20    # below this it is a cover page or a section divider

# Stage 2. Prepend context before embedding so a chunk carries its own position
# in the document. Targets the baseline failure where both conceptual misses were
# the RIGHT document but the WRONG page.
#
#   "none"           control
#   "title+heading"  REJECTED: raised intra-document similarity 0.748 -> 0.817
#                    while leaving section discrimination unchanged at 0.044.
#                    Pure clustering cost. conceptual hit@5 fell 0.900 -> 0.750.
#   "heading"        a quarter of the clustering cost (0.748 -> 0.767) and 45%
#                    more section discrimination (0.044 -> 0.064).
HEADER_MODE = "none"      # REJECTED twice -- see BASELINE-2.md and BASELINE-5.md


def chunk(documents):
    """Split documents into a flat list of chunks, page by page.

    Page-bounded: a chunk never spans a page break, so `page` is exact and a
    citation can name it. Pages longer than CHUNK_WORDS are windowed with
    overlap, so an answer is not severed at a chunk boundary.

    Returns a FLAT list. Its index is the row number in the array embed()
    produces -- search() gets row indices back and looks them up here.
    """
    chunks = []
    dropped = 0

    titles = load_titles()

    for document in documents:
        ordinal = 0
        pages = document["text"].split(PAGE_SEPARATOR)
        headings = document.get("headings") or [""] * len(pages)
        # Real title from the harvest metadata, falling back to the filename.
        title = titles.get(document["doc_id"]) or document["filename"]

        for page_number, page_text in enumerate(pages, start=1):
            words = page_text.split()

            # 4% of pages are near-empty. They still produce an embedding, and
            # a near-empty vector matches every query weakly -- pure noise.
            if len(words) < MIN_CHUNK_WORDS:
                dropped += 1
                continue

            for start in range(0, len(words), CHUNK_WORDS - CHUNK_OVERLAP):
                window = words[start:start + CHUNK_WORDS]

                # A trailing scrap is already covered by the previous window's
                # overlap. Only reachable if the size/overlap ratio changes.
                if start > 0 and len(window) < MIN_CHUNK_WORDS:
                    break

                body = " ".join(window)
                heading = headings[page_number - 1] if page_number <= len(headings) else ""
                if HEADER_MODE == "title+heading":
                    header = " > ".join(p for p in (title, heading) if p)
                elif HEADER_MODE == "heading":
                    header = heading
                else:
                    header = ""

                chunks.append({
                    # Zero-padded so ids sort lexically. This is what the
                    # golden set references, so it must survive a rebuild --
                    # which is why load() sorts its files.
                    "chunk_id": f"{document['doc_id']}-{ordinal:05d}",
                    "doc_id": document["doc_id"],
                    "filename": document["filename"],
                    "page": page_number,
                    "heading": heading,
                    "body": body,
                    # `text` is what gets EMBEDDED and searched; `body` stays raw
                    # for the prompt. Separating them means the header helps
                    # retrieval without padding every source in the LLM context.
                    "text": f"{header}\n\n{body}" if header else body,
                })
                ordinal += 1

                if start + CHUNK_WORDS >= len(words):
                    break

    sizes = sorted(len(c["text"].split()) for c in chunks)
    median = sizes[len(sizes) // 2] if sizes else 0
    print(f"chunked {len(chunks)} chunks from {len(documents)} documents "
          f"(median {median} words, dropped {dropped} near-empty pages)")
    return chunks



EMBED_MODEL = "BAAI/bge-small-en-v1.5"   # 384 dims, ~130 MB, 512-token limit

# bge models are ASYMMETRIC: queries take this prefix, passages take nothing.
# Get it wrong and there is no error, just quietly worse retrieval.
QUERY_PREFIX = "Represent this sentence for searching relevant passages: "

_model = None


def get_model():
    """Load the embedding model once and reuse it.

    Loading costs several seconds, so search() must not pay it per query.
    The imports are deliberately lazy -- sentence_transformers is slow to
    import, and `import rag` should stay cheap.
    """
    global _model
    if _model is None:
        import torch
        from sentence_transformers import SentenceTransformer

        device = "cuda" if torch.cuda.is_available() else "cpu"
        _model = SentenceTransformer(EMBED_MODEL, device=device)
        print(f"loaded {EMBED_MODEL} on {device}")
    return _model


def embed(chunks):
    """Encode chunk texts into an (n_chunks, 384) float32 array.

    normalize_embeddings=True is what lets search() use a plain dot product:
    for unit vectors the dot product IS cosine similarity, so the entire
    search is one matrix multiply.

    Row i corresponds to chunks[i]. The two are coupled by position only --
    reorder one without the other and every result is silently wrong.
    """
    model = get_model()
    texts = [c["text"] for c in chunks]     # passages: no QUERY_PREFIX

    # Anything past the model's token limit is truncated SILENTLY. Better to
    # know how much of the corpus is affected than to wonder later.
    limit = model.max_seq_length
    lengths = [len(ids) for ids in model.tokenizer(texts)["input_ids"]]
    truncated = sum(1 for n in lengths if n > limit)
    if truncated:
        print(f"! {truncated}/{len(texts)} chunks exceed {limit} tokens "
              f"and will be truncated (max {max(lengths)})")

    vectors = model.encode(
        texts,
        batch_size=128,
        normalize_embeddings=True,
        show_progress_bar=True,
        convert_to_numpy=True,
    ).astype(np.float32)

    print(f"embedded {vectors.shape[0]} chunks -> {vectors.shape[1]} dims, "
          f"{vectors.nbytes / 1e6:.1f} MB")
    return vectors



INDEX_PATH = BASE_DIR / "data" / "index"


def corpus_fingerprint():
    """Hash of everything that makes an existing index invalid.

    Computed from filenames and sizes via stat() -- no PDF parsing -- so the
    cache check itself costs milliseconds even at 1,913 documents.

    Settings are folded in alongside the file list. Changing CHUNK_WORDS or
    EMBED_MODEL moves the fingerprint, so a stale index is rebuilt rather than
    silently served. That failure mode -- right code, wrong vectors, no error --
    is why this is a hash and not a file count.
    """
    files = sorted((p.name, p.stat().st_size) for p in DATA_PATH.glob("*.pdf"))
    payload = {
        "files": files,
        "chunk_words": CHUNK_WORDS,
        "chunk_overlap": CHUNK_OVERLAP,
        "min_chunk_words": MIN_CHUNK_WORDS,
        "header_mode": HEADER_MODE,
        "embed_model": EMBED_MODEL,
        "page_separator": PAGE_SEPARATOR,
    }
    blob = json.dumps(payload, sort_keys=True).encode()
    return hashlib.sha256(blob).hexdigest()[:16]


def build_index(force=False):
    """Return (chunks, vectors), from cache when it is still valid.

    Turns a ~10 minute rebuild at 1,913 documents into 0.06 s.
    """
    fingerprint = corpus_fingerprint()
    manifest_path = INDEX_PATH / "manifest.json"

    if not force and manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if manifest.get("fingerprint") != fingerprint:
            print(f"index stale ({manifest.get('fingerprint')} -> {fingerprint}) "
                  f"-- rebuilding")
        else:
            chunks = json.loads((INDEX_PATH / "chunks.json").read_text(encoding="utf-8"))
            vectors = np.load(INDEX_PATH / "vectors.npy")
            # chunks and vectors are coupled by position only. If the counts
            # disagree the cache is corrupt and every result would be wrong.
            if len(chunks) == vectors.shape[0]:
                print(f"index cache hit: {len(chunks)} chunks [{fingerprint}]")
                # The BM25 index is derived from the same chunks but lives in a
                # separate file, so it can go missing independently of the cache.
                if not FTS_PATH.exists():
                    build_fts(chunks)
                return chunks, vectors
            print("! cache corrupt (chunk/vector count mismatch) -- rebuilding")

    documents = load()
    chunks = chunk(documents)
    vectors = embed(chunks)

    INDEX_PATH.mkdir(parents=True, exist_ok=True)
    (INDEX_PATH / "chunks.json").write_text(
        json.dumps(chunks, ensure_ascii=False), encoding="utf-8")
    np.save(INDEX_PATH / "vectors.npy", vectors)
    build_fts(chunks)
    manifest_path.write_text(json.dumps({
        "fingerprint": fingerprint,
        "built_at": datetime.now().isoformat(timespec="seconds"),
        "n_documents": len(documents),
        "n_chunks": len(chunks),
        # The full config travels with the index. A recall figure without the
        # settings that produced it is uninterpretable three months later.
        "embed_model": EMBED_MODEL,
        "embed_dim": int(vectors.shape[1]),
        "chunk_words": CHUNK_WORDS,
        "chunk_overlap": CHUNK_OVERLAP,
        "min_chunk_words": MIN_CHUNK_WORDS,
        "header_mode": HEADER_MODE,
    }, indent=2), encoding="utf-8")

    print(f"index cached -> {INDEX_PATH.relative_to(BASE_DIR)} [{fingerprint}]")
    return chunks, vectors


FTS_PATH = INDEX_PATH / "fts.sqlite"

K_VECTOR = 50      # candidates drawn from each channel before fusion
K_KEYWORD = 50
RRF_K = 60         # the constant in 1/(k + rank); 60 is the standard default

RETRIEVAL_MODE = "hybrid"      # "vector" | "keyword" | "hybrid" | "auto"

# RETIRED IN STAGE 4 -- kept for reproducibility, no longer the default.
#
# Stage 3 routed identifier-shaped queries to BM25 alone, because RRF weighted
# both channels equally and the vector channel's confident garbage dragged good
# keyword results down (identifier hit@5 0.400 hybrid vs 0.467 keyword-only).
# Routing recovered that: 0.400 -> 0.467.
#
# The stage 4 cross-encoder made it not merely redundant but HARMFUL:
#
#     routed + rerank   identifier hit@5  0.733
#     hybrid + rerank   identifier hit@5  0.800
#
# Routing discards the vector channel and so shrinks the candidate pool. Once a
# reranker is doing the discriminating it can sort good from bad itself, and
# simply wants more candidates. Set RETRIEVAL_MODE = "auto" to re-enable.
#
# Deliberately permissive on abbreviations -- real users write "reg 47", "s36",
# "cl 5.2" far more often than "Regulation 47".
IDENTIFIER_QUERY = re.compile(
    r"\b(?:reg|regs|regulation|regulations"
    r"|s|ss|sec|section|sections"
    r"|cl|cls|clause|clauses"
    # longest-first: 'sch' would match inside 'sched' and strand the rest
    r"|schedules|schedule|scheds|sched|sch|subparts|subpart|parts|part"
    r"|table|figure|fig|appendix|app)"
    r"\.?\s*[A-Za-z]?\d+[A-Za-z]?\b",
    re.I,
)


RERANK_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"   # ~90 MB, 6 layers
K_RERANK = 50            # candidates handed to the cross-encoder
USE_RERANKER = True      # stage 4

_reranker = None


def get_reranker():
    global _reranker
    if _reranker is None:
        import torch
        from sentence_transformers import CrossEncoder

        device = "cuda" if torch.cuda.is_available() else "cpu"
        _reranker = CrossEncoder(RERANK_MODEL, device=device)
        print(f"loaded {RERANK_MODEL} on {device}")
    return _reranker


def apply_reranker(query, hits, top_k):
    """Rescore candidates with a cross-encoder and re-sort.

    The retriever is a BI-encoder: query and chunk are embedded separately and
    never meet, so each chunk was compressed into 384 numbers without knowing
    the question. That is what makes it fast enough to scan 41,594 chunks, and
    what makes its scores cluster (top_gap 0.014 -- barely discriminating).

    A CROSS-encoder feeds query and chunk through a transformer TOGETHER, so
    attention runs across both. Far more accurate, and far too slow to run over
    the whole corpus -- one forward pass per pair, no precomputation possible.

    Hence: bi-encoder for cheap recall over everything, cross-encoder for
    expensive precision over the survivors. Its ceiling is recall at K_RERANK --
    it can only reorder what retrieval handed it.
    """
    if not hits:
        return []
    model = get_reranker()
    scores = model.predict([(query, h["text"]) for h in hits])
    order = sorted(range(len(hits)), key=lambda i: -scores[i])[:top_k]
    # Scores are now cross-encoder logits (roughly -10..+10), not cosine or RRF.
    # Anything comparing raw score values across stages must account for this.
    return [{**hits[i], "score": float(scores[i])} for i in order]


def route(query):
    """Pick a retrieval mode for this query.

    A hard switch, not a blend: when it is right you get the best channel for
    the query, when it is wrong you get the worst one. Router accuracy caps the
    entire benefit, which is why it is measured separately on paraphrased
    queries the pattern was not built from -- see router_probe.jsonl.
    """
    return "keyword" if IDENTIFIER_QUERY.search(query) else "hybrid"

_TOKEN = re.compile(r"[A-Za-z0-9]+")


def build_fts(chunks):
    """Build the BM25 keyword index over the same chunks.

    This is the channel that catches exact identifiers. Embeddings place
    "Regulation 47" and "Regulation 92" at nearly the same point because they
    occur in identical linguistic contexts -- the distinguishing feature is an
    arbitrary integer, and semantic similarity has no purchase on those.
    BM25 scores by term rarity, which is exactly what a rare integer has.
    """
    import sqlite3

    FTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    FTS_PATH.unlink(missing_ok=True)
    con = sqlite3.connect(FTS_PATH)
    con.execute("CREATE VIRTUAL TABLE chunks_fts USING fts5("
                "chunk_id UNINDEXED, text, tokenize='porter unicode61')")
    con.executemany("INSERT INTO chunks_fts (chunk_id, text) VALUES (?, ?)",
                    ((c["chunk_id"], c["text"]) for c in chunks))
    con.commit()
    con.close()
    print(f"built BM25 index over {len(chunks)} chunks")


_fts = None


def fts_connection():
    global _fts
    if _fts is None:
        import sqlite3
        if not FTS_PATH.exists():
            raise SystemExit("No BM25 index. Run:  python rag.py --rebuild")
        _fts = sqlite3.connect(FTS_PATH, check_same_thread=False)
    return _fts


def to_match_query(query):
    """FTS5 MATCH is a query language, not raw text.

    Unescaped punctuation is a syntax error, so tokenise to alphanumerics,
    quote each term and OR them together.
    """
    terms = _TOKEN.findall(query)
    return " OR ".join(f'"{t}"' for t in terms) if terms else '""'


def keyword_search(query, k=K_KEYWORD):
    """BM25 over FTS5. Returns [(chunk_id, score)], higher score is better."""
    import sqlite3
    try:
        rows = fts_connection().execute(
            "SELECT chunk_id, bm25(chunks_fts) AS score FROM chunks_fts "
            "WHERE chunks_fts MATCH ? ORDER BY score LIMIT ?",
            (to_match_query(query), k),
        ).fetchall()
    except sqlite3.OperationalError:
        return []
    # bm25() returns negative values, more negative being better. Flip the sign
    # so "higher is better" matches the vector channel.
    return [(chunk_id, -float(score)) for chunk_id, score in rows]


def rrf(ranked_lists, k=RRF_K):
    """Reciprocal Rank Fusion.

    The two channels produce incomparable scales -- cosine sits around 0-1,
    BM25 is unbounded. RRF discards the scores entirely and uses only rank
    position, so it needs no calibration or tuning:

        score(chunk) = sum over lists of  1 / (k + rank_in_that_list)

    Anything ranking well in BOTH channels floats to the top.
    """
    scores = defaultdict(float)
    for ranking in ranked_lists:
        for rank, chunk_id in enumerate(ranking, start=1):
            scores[chunk_id] += 1.0 / (k + rank)
    return sorted(scores.items(), key=lambda kv: -kv[1])


def search(query, vectors, chunks, top_k=6, mode=None, rerank=None):
    """Return the top_k chunks most similar to the query.

    The vectors are unit-normalised, so a dot product IS cosine similarity and
    the whole search is one matrix multiply: (n_chunks, 384) @ (384,).

    At 41,594 chunks that is 64 MB of arithmetic -- ~9 ms, and EXACT.
    An approximate index (HNSW, FAISS) only starts earning its complexity
    somewhere past ~500k chunks.
    """
    if not chunks or vectors.shape[0] == 0:
        return []
    mode = mode or RETRIEVAL_MODE
    if mode == "auto":
        mode = route(query)

    # With reranking on, retrieve a deeper candidate pool and let the
    # cross-encoder pick from it. K_RERANK is the reranker's recall ceiling.
    use_rerank = USE_RERANKER if rerank is None else rerank
    fetch_k = max(top_k, K_RERANK) if use_rerank else top_k

    def vector_ranked(k):
        model = get_model()
        # Queries take QUERY_PREFIX; passages did not. bge models were trained
        # on that asymmetry -- omitting it degrades results with no error.
        query_vector = model.encode(
            QUERY_PREFIX + query,
            normalize_embeddings=True,
            convert_to_numpy=True,
        ).astype(np.float32)
        scores = vectors @ query_vector
        # argpartition finds the top k without fully sorting: O(n) not O(n log n).
        k = min(k, len(scores))
        top = np.argpartition(-scores, k - 1)[:k]
        top = top[np.argsort(-scores[top])]
        return [(chunks[i]["chunk_id"], float(scores[i])) for i in top]

    if mode == "vector":
        ranked = vector_ranked(fetch_k)
    elif mode == "keyword":
        ranked = keyword_search(query, fetch_k)
    else:
        vector_hits = vector_ranked(max(K_VECTOR, fetch_k))
        keyword_hits = keyword_search(query, max(K_KEYWORD, fetch_k))
        ranked = rrf([[cid for cid, _ in vector_hits],
                      [cid for cid, _ in keyword_hits]])[:fetch_k]

    by_id = _chunk_index(chunks)
    # Copy rather than mutate. Attaching "score" to the shared chunk dicts
    # would leak one query's scores into the results of the next.
    results = [{**chunks[by_id[cid]], "score": float(score)}
               for cid, score in ranked if cid in by_id]

    if use_rerank:
        return apply_reranker(query, results, top_k)
    return results[:top_k]


_by_id_cache = None


def _chunk_index(chunks):
    """chunk_id -> position. Built once; the chunk list does not change."""
    global _by_id_cache
    if _by_id_cache is None or len(_by_id_cache) != len(chunks):
        _by_id_cache = {c["chunk_id"]: i for i, c in enumerate(chunks)}
    return _by_id_cache



GENERATION_MODEL = "claude-haiku-4-5"   # $1 / $5 per Mtok -- ~$0.005 a query.
                                        # Pricier: claude-sonnet-5 $2/$10,
                                        #          claude-opus-5   $5/$25
# max_tokens is a HARD per-call ceiling on output, and output is the expensive
# half. A grounded answer needs ~300 tokens, so 1000 caps the worst case at
# about half a cent instead of letting a runaway response cost 8x that.
MAX_TOKENS = 1000

SYSTEM_PROMPT = """You answer questions about New Zealand workplace health and \
safety using ONLY the numbered sources provided in the user message.

Rules:
- Cite the source number for every factual claim, like [2]. Several: [1][3].
- Use ONLY the sources given. Do not add outside knowledge.
- If the sources do not answer the question, say so plainly and stop.
  Do not guess and do not pad.
- If they answer only part of it, answer that part and state what is missing.
- Quote exact wording where the precise phrasing carries legal weight.
- You are not giving legal advice. Report what the sources say."""

_titles = None


def load_titles():
    """doc_id -> real document title, from the harvest metadata.

    Turns "410-approved-code-of-practice-for-cranes.pdf p75" into
    "Approved Code of Practice for Cranes, p. 75". Citation quality is most of
    what makes the output credible, and this is the payoff for carrying doc_id
    through load() and chunk().
    """
    global _titles
    if _titles is None:
        _titles = {}
        path = BASE_DIR / "data" / "urls.jsonl"
        if path.exists():
            for line in path.read_text(encoding="utf-8").splitlines():
                if line.strip():
                    row = json.loads(line)
                    _titles[row["doc_id"]] = row["title"]
    return _titles


def format_sources(hits):
    """Number the retrieved chunks. The number is what the model cites."""
    titles = load_titles()
    return "\n\n".join(
        f"[{n}] {titles.get(hit['doc_id']) or hit['filename']}, p. {hit['page']}\n"
        f"{hit['text']}"
        for n, hit in enumerate(hits, start=1)
    )


def answer(query, hits, model=GENERATION_MODEL):
    """Generate a grounded answer from retrieved chunks.

    Returns a dict with the text, the hits it was built from, and token usage
    so cost can be tracked per query.
    """
    # No context means nothing to ground on. Refuse locally rather than paying
    # for a call that could only answer from the model's own weights.
    if not hits:
        return {
            "text": "No relevant sources were retrieved, so this question "
                    "cannot be answered from the corpus.",
            "hits": [],
            "usage": None,
        }

    if not os.getenv("ANTHROPIC_API_KEY"):
        raise SystemExit(
            "ANTHROPIC_API_KEY is not set. Retrieval works without it; only "
            "answer() needs a key."
        )

    import anthropic

    response = anthropic.Anthropic().messages.create(
        model=model,
        max_tokens=MAX_TOKENS,
        system=SYSTEM_PROMPT,
        # No thinking parameter.
        messages=[{
            "role": "user",
            "content": f"{format_sources(hits)}\n\nQuestion: {query}",
        }],
    )

    # response.content is a LIST OF BLOCKS, not a string
    text = "".join(b.text for b in response.content if b.type == "text")

    global SPEND_USD
    cost = cost_usd(model, response.usage)
    SPEND_USD += cost

    return {"text": text, "hits": hits, "usage": response.usage, "cost": cost}


# $ per million tokens: (input, output)
PRICES = {
    "claude-haiku-4-5": (1.00, 5.00),
    "claude-sonnet-5": (2.00, 10.00),
    "claude-opus-5": (5.00, 25.00),
}

SPEND_USD = 0.0    # running total for this process


def cost_usd(model, usage):
    """Dollar cost of one call. Output tokens are 5x input -- watch those."""
    price_in, price_out = PRICES.get(model, (0.0, 0.0))
    return (usage.input_tokens / 1e6) * price_in + (usage.output_tokens / 1e6) * price_out


RETRIEVAL_TESTS = [
    "check for asbestos before high pressure spraying roofs",
    "what are a PCBU's duties when workers are working at height",
    "Regulation 9",     # known failure: vector search cannot rank identifiers
]

# One answerable, one deliberately outside the corpus. The second is the real
# test -- a grounded system must refuse rather than answer from model weights.
GENERATION_TESTS = [
    "check for asbestos before high pressure spraying roofs",
    "what is the minimum wage in New Zealand",
]


def show(question, hits):
    print(f"\nQUERY: {question}")
    for n, hit in enumerate(hits, start=1):
        title = load_titles().get(hit["doc_id"]) or hit["filename"]
        print(f"  [{n}] {hit['score']:.3f}  {title[:52]}, p.{hit['page']}")
        print(f"      {hit['text'][:120]}")


if __name__ == "__main__":
    # PDF text contains arrows and en-dashes; the Windows console is cp1252 and
    # would raise UnicodeEncodeError on printing. Force UTF-8 output.
    sys.stdout.reconfigure(encoding="utf-8")

    # pass --rebuild to force a fresh index regardless of the cache
    chunks, embeddings = build_index(force="--rebuild" in sys.argv)

    print("\n" + "=" * 68 + "\nRETRIEVAL\n" + "=" * 68)
    for question in RETRIEVAL_TESTS:
        show(question, search(question, embeddings, chunks, top_k=3))

    print("\n" + "=" * 68 + "\nGENERATION\n" + "=" * 68)
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("ANTHROPIC_API_KEY not set -- skipping (retrieval needs no key).")
    else:
        for question in GENERATION_TESTS:
            hits = search(question, embeddings, chunks, top_k=6)
            result = answer(question, hits)
            print(f"\nQUERY: {question}\n{result['text']}")
            print(f"  [{result['usage'].input_tokens} in / "
                  f"{result['usage'].output_tokens} out  ${result['cost']:.4f}]")
        print(f"\nsession total: ${SPEND_USD:.4f}")