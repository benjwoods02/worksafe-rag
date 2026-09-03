# Stage 3 - Query Routing

Routes queries naming an exact reference to the BM25 channel alone, and
everything else to hybrid. Compare against [stage-2-hybrid-retrieval.md](stage-2-hybrid-retrieval.md)
(hybrid everywhere) and [stage-1-vector-baseline.md](stage-1-vector-baseline.md) (vector only).

Measured on the frozen `golden_set_v1.jsonl` - 45 questions, 20 conceptual,
15 identifier, 10 unanswerable. Index unchanged from stage 2: 1,913 documents,
41,594 chunks, `bge-small-en-v1.5`, chunk 300/50, fingerprint `5a3e0e1883e9ecb3`.
No re-embedding - this stage changes only dispatch.

## Progression

| | stage 1 | stage 2 | stage 3 |
|---|---|---|---|
| | vector | hybrid | routed |
| conceptual hit@1 | 0.200 | 0.450 | 0.450 |
| conceptual hit@5 | 0.900 | 0.900 | 0.900 |
| identifier hit@1 | 0.067 | 0.067 | 0.267 |
| identifier hit@5 | 0.067 | 0.400 | 0.467 |
| identifier MRR | 0.067 | 0.233 | 0.350 |
| aggregate hit@5 | 0.543 | 0.686 | 0.714 |
| aggregate MRR | 0.293 | 0.459 | 0.510 |

Routing recovered the entire identifier gap that RRF was costing - `hit@5`
0.400 -> 0.467, `hit@1` quadrupled - while conceptual held exactly.

---

## 1. Why routing

Stage 2 measured a crossover: keyword-only beat hybrid on identifier queries
(`hit@5` 0.467 vs 0.400) while losing on conceptual (0.800 vs 0.900). RRF
weights both channels equally, so on an identifier query the vector channel's
confident garbage drags good keyword results down. No fixed mode wins both.

```
strategy                   hit@5 all   conceptual   identifier
always vector                 0.543       0.900        0.067
always keyword                0.657       0.800        0.467
always hybrid                 0.686       0.900        0.400
ROUTED                        0.714       0.900        0.467
ORACLE (best per question)    0.800       1.000        0.533
```

The oracle row matters: 0.800 is what a perfect router achieves, and routing
between these three modes cannot reach it. The remaining 0.086 needs better
retrieval, not better dispatch. That is the reranking case.

## 2. Implementation

A regex on the query, deliberately permissive on abbreviations because real
users write "reg 47" and "s36" far more often than "Regulation 47":

```python
IDENTIFIER_QUERY = re.compile(
    r"\b(?:reg|regs|regulation|regulations"
    r"|s|ss|sec|section|sections"
    r"|cl|cls|clause|clauses"
    r"|schedules|schedule|scheds|sched|sch|subparts|subpart|parts|part"
    r"|table|figure|fig|appendix|app)"
    r"\.?\s*[A-Za-z]?\d+[A-Za-z]?\b", re.I)

def route(query):
    return "keyword" if IDENTIFIER_QUERY.search(query) else "hybrid"
```

`RETRIEVAL_MODE = "auto"` activates it. One bug found during testing: `sched 3`
failed because `sch` matched first in the alternation and stranded `ed 3`.
Alternations must be ordered longest-first.

---

## 3. Router accuracy - the number that actually matters

Routing's benefit is capped by router accuracy, so it is measured separately in
`router_probe.jsonl` via `python golden.py probe`.

| Set | Accuracy | What it proves |
|---|---|---|
| frozen golden set | 45/45 | nothing - circular, see below |
| `designed` (20) | 20/20 | pattern handles abbreviations and hard negatives |
| `realistic` (15) | 12/15 (80%) | the honest number |

### Why the frozen-set figure is not the headline

The identifier segment was auto-generated from regex patterns, so a regex router
matches it by construction. The `realistic` set is the meaningful measure, which
is why router accuracy is reported from a separate probe file.

One genuine signal does come from the frozen set: 0 false positives across the
30 conceptual and unanswerable questions, which were written in natural
language rather than generated.

### The three realistic failures

`"regualtion 47"` -> hybrid. A typo in the reference word blinds the regex.
Employees typo constantly. Fixable with fuzzy matching on the trigger word.

`"47"` -> hybrid. A bare identifier with no context word. Not fixable by
regex without catastrophic false positives - every "5 metres" and "85 db" would
route to keyword.

`"we are doing asbestos removal, does regulation 47 apply to us and what PPE
do we need"` -> keyword. The important one. The query is mostly conceptual and
happens to contain a reference, so keyword-only will do badly on the PPE half.

That third case is not a bug, it is the fundamental limitation of hard
routing: a query can be both kinds at once, and a switch forces a binary
choice on something that is not binary. Weighted RRF would lean toward keyword
while keeping the vector channel alive, and would not have this failure mode.

---

## 4. Production assessment

Is rule-based routing used in production RAG? Yes, for structured identifier
lookups, language detection and obvious intent classes, and in regulated
domains it is often preferred because it is deterministic and auditable.

However, production systems rarely stop there. They layer rules for high-confidence
patterns with a classifier or LLM for the rest, and invest more in query
understanding generally (rewriting, decomposition, metadata extraction) than in
channel selection.

A caveat worth testing: many production systems do not route at all. They
run hybrid always and let a cross-encoder reranker sort it out - the reranker
reads query and chunk together, so it can judge whether a BM25 hit is genuinely
relevant rather than guessing from the query's shape. Routing is partly a
cheap approximation of what a reranker does, and the stage 4 reranker may
subsume this gain entirely. That is a prediction to measure, not assume.

Would it survive real employee queries? Partially. Beyond the three failures
above, real queries are much shorter (`"asbestos ppe"`), full of industry
acronyms (SWMS, JSA, H&S rep), frequently conversational and dependent on a
prior turn ("what about for contractors?"), often multi-part, and sometimes
not questions at all. The golden set contains none of that - every question is a
well-formed sentence because it was written that way.

To make this production-ready: real query logs (the biggest gap - everything
here is synthetic), fuzzy matching for typos, a length heuristic so long mixed
queries stay hybrid, and logging of every routing decision so misroutes are
auditable after the fact.

---

## 5. Limitations

### KNOWN - router accuracy is 80% on realistic input, unmeasured on real input

Everything in `router_probe.jsonl` is synthetic and written by the same person
who wrote the router. An independent query set would be stronger evidence.
20 designed + 15 realistic is a small sample.

### KNOWN, a hard switch cannot serve a query that is both kinds

See §3. Weighted RRF is the structural fix and is the obvious alternative
stage to run.

### BLOCKING - retrieval still cannot signal failure

Unchanged since stage 1 and now harder, because score scales are mode-dependent
and routing makes the scale vary per query. A query routed to keyword returns
BM25 scores (~22); one routed to hybrid returns RRF scores (~0.03). There is no
threshold that works across both.

### KNOWN - `top_gap` is now meaningless in aggregate

It reports 0.216 for stage 3, which averages across three different score scales
(RRF ~0.001, BM25 ~0.645). Per-segment it is still readable; aggregated it is
noise. The metric needs normalising before it can be reported at all.

### KNOWN - golden set has no procedural or multi-hop segment

Unchanged. Still 45 questions across three segments; nothing measures
multi-document reasoning.

### ACCEPTED - chunks and vectors coupled by position

Unchanged.

### ACCEPTED - no access control

Unchanged. A correctness requirement for any multi-user deployment, not an
optimisation.

---

## 6. Stage 4

Cross-encoder reranking. A reranker can only reorder what retrieval handed
it, so its ceiling is recall at the candidate depth. Measured under the current
routed retrieval:

```
    k      all   conceptual   identifier
    1    0.371        0.450        0.267   <- current
    5    0.714        0.900        0.467
   20    0.914        1.000        0.800
   50    0.971        1.000        0.933   <- reranking ceiling
```

Headroom is large on both segments: conceptual 0.450 -> 1.000, identifier
0.267 -> 0.933.

> Correction. An earlier draft of this section stated a reranker could not
> help identifiers, citing `hit@100` of 0.533. That figure was measured under
> stage 1 vector-only retrieval. Under routed retrieval BM25 does find those
> chunks. It simply ranks them badly, so identifier `hit@50` is 0.933, not
> 0.267. Reranking is a ranking fix, and identifier retrieval is now a ranking
> problem rather than a recall problem.

Two things to measure at the same time:

1. Whether the reranker subsumes routing (§4). If routed and always-hybrid
   converge once a reranker is applied, drop the router. It is complexity that
   stopped paying.
2. Whether the gain is larger on conceptual or identifier queries. Both have
   headroom now, and they may not benefit equally.

Also outstanding:

- Weighted RRF as an alternative to hard routing (§3).
- Corpus curation - guidance-only index vs all 1,913 documents. Cheap: filter
  the chunk list and re-run, no new models.
- Metadata filtering using `facet_types` - restrict legal questions to the 59
  ACOPs and 40 Safe Work Instruments.
- Normalising `top_gap` and `unanswerable_top_score` so they survive a change of
  retrieval mode.

Deprioritised - hierarchical / multi-granularity chunking. Its rationale was
that identifier chunks were absent from the candidate pool at any depth. Stage 3
removed that motivation: identifier `hit@50` is 0.933. Sentence-level indexing
would cost ~500k vectors and hours of embedding to address a recall gap that no
longer exists. Recorded because a stage removing the reason for a planned stage
is a legitimate outcome.

---
