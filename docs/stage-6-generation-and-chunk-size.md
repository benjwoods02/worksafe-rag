# Stage 6 - Generation Quality and Chunk Size

Two final measurements, closing the project's two largest gaps: generation had
never been scored at all, and chunk size had never been varied.

Both were measured against the frozen `golden_set_v1.jsonl` (45 questions) on
the stage 4 system - hybrid retrieval, cross-encoder reranking,
`claude-haiku-4-5` generation.

---

## Part 1 - Generation quality

45 answers generated for $0.1448 and labelled on six dimensions.

```
grounded    35/35  (100%)    conceptual 20/20   identifier 15/15
citations   32/35  ( 91%)    conceptual 17/20   identifier 15/15
modality    18/20  ( 90%)    conceptual 15/17
complete    22/23  ( 96%)
drift       43/45  ( 96%)
refusal     22/22  (100%)    identifier 12/12   unanswerable 10/10
```

### Labelling method

Answers were scored by an LLM judge against the six dimensions above, then
spot-checked by hand. Human review agreed with the judge on 6 of 7 items
(86%) and corrected it on the seventh.

The review moved `grounded` from 97% to 100%: four of the judge's flags turned
out to be artifacts of the 400-character source excerpts shown in the
labelling sheet rather than model errors, so the judge was over-cautious on the
dimension where it had least evidence.

Independent labelling by a domain expert, over more than seven items, would be
stronger. Recorded as future work.

### The failures

Modality (2) - the domain-critical one. WorkSafe explicitly defines "must"
as a legal requirement and "should" as recommended practice.

- `c015`: source reads *"fixed barriers should be at least 500 mm from the
  robot work envelope"; the answer states "must be at least 500 mm"*.
- `c012`: source reads *"You should provide your customers with
  information"; the answer headlines it "Information you must provide"*.

Recommended practice reported as legal obligation. No retrieval metric can
detect this - retrieval fetched exactly the right chunk both times.

Drift (2). `c006` asked whether a certified handler must be present for
highly hazardous gases. Source [1] answers directly - *"Highly hazardous
gases must be under the control of a certified handler. The handler must be
present"*, and the answer ignored it, pivoted to fumigants and explosives from
adjacent sources, and concluded a handler is not always required. Every
claim sourced, every citation valid; it answered a different question.

Human review confirmed the failure and added that the source wording across
documents is itself confusing and partly contradictory, so some of it is
attributable to the corpus rather than the model.

Citations (3). Claims attached to a source whose text does not support them
while a supporting source sits in the same result set.

### Findings from human review that the judge missed

Chunk overlap creates citation ambiguity. If a sentence spans two chunks,
"which chunk is the citation" is ill-defined. It does not explain `c009` - those
chunks are p31 and p36, and page-bounded chunking means overlap only ever occurs
within a page, but it is a real risk for same-page pairs, and a consequence of
`CHUNK_OVERLAP = 50` invisible to every retrieval metric.

Source-layout explanations are noise. Several refusals explain why the
answer is unavailable by describing what the retrieved chunks contain. A user
never sees the sources, so this leaks implementation detail instead of
answering. A one-line prompt change would fix it. Not applied - recorded as
future work.

### Prompt violations not caught by any dimension

Four of ten refusals redirect outside the corpus - "contact Immigration NZ",
"the Building Act 2004", "contact ACC directly", *"contact the relevant
local authority". `SYSTEM_PROMPT` says "Use ONLY the sources given. Do not add
outside knowledge."*

Refusal behaviour is 100%; instruction-following on those items is 60%. None
of it is a substantive claim about safety law, so it is benign, but it is
happening by accident rather than by design.

### What this says about the golden set

12 of 15 identifier answers are refusals, and they are correct refusals.
`id001` identified three different Regulation 47s across separate instruments;
`id003` the same for Regulation 84; `id004` and `id006`-`id010` each noted the
corpus cites a regulation without ever stating what it requires.

That is the structural point: guidance documents reference regulations, they
do not reproduce them, so "what does Regulation 47 require" is unanswerable
from this corpus even when retrieval works perfectly. Identifier `hit@5` of
0.800 measures something real - finding chunks that mention a reference - but
the question text asks for something the corpus cannot supply.

`id014` is the clean counter-example: a genuine retrieval miss, where eight
ground-truth chunks contain Table 27 and retrieval surfaced none.

---

## Part 2 - Chunk size

The last untested variable. `300/50` was chosen in stage 1 relative to the
median page (262 words) and held fixed through every stage since.

Changing chunk size moves every chunk ID, so ground truth was re-resolved per
variant by the same literal-match method that created it. Questions stayed
byte-identical. The regrounder was validated first: at unchanged chunk size it
reproduced 44/45 of the stored ground truth exactly.

### Fixed k = 5

```
config          chunks   gt   hit@1   hit@5     mrr   concept   ident
150/25           71808    8   0.600   0.771   0.671     0.950   0.533
300/50           41594    7   0.657   0.886   0.765     0.950   0.800
600/100          27526    7   0.571   0.857   0.693     1.000   0.667
```

### Fixed token budget (~1800 words to the model)

```
  150/25   k=12   hit@12 0.829   mrr 0.677
  300/50   k=6    hit@6  0.886   mrr 0.765
  600/100  k=3    hit@3  0.771   mrr 0.693
```

Both comparisons are reported because neither alone is fair: at fixed `k` the
model receives different amounts of context, and at fixed budget `hit@12` and
`hit@3` are not comparable to each other.

### Result: 300/50 scores highest, but no difference is significant

```
300 vs 150:  31 vs 27 of 35.  BEST-CASE two-sided p = 0.125
300 vs 600:  31 vs 30 of 35.  BEST-CASE two-sided p = 1.000
```

Per-question results were not saved during the sweep, a design miss - so
McNemar could only be bounded rather than computed, by assuming the smaller
success set is a strict subset of the larger (`b = 0`, maximum discordance).
Even under that most generous assumption neither difference reaches p < 0.05.

Chunk size was varied across a 4x range and no configuration significantly
outperformed another. Chunking receives a lot of attention in RAG writing relative to the evidence
for it, so this is worth recording.

Two effects that are not about retrieval quality but are real:

- 150-word chunks hurt identifier retrieval most (`hit@5` 0.533 against
  0.800), the largest single swing in the table. Plausibly BM25 length
  normalisation, but unmeasured.
- 600-word chunks reached conceptual `hit@5` of 1.000 - the only
  configuration to do so - while losing on identifiers.

`300/50` is retained as the adopted configuration: highest on both aggregate
comparisons, and no evidence to justify a change.

---

## Limitations of this stage

The generation labels are LLM-scored with a human spot-check, not
independently hand-labelled throughout. 86% agreement on seven items is the
calibration; a larger sample and an independent labeller would strengthen it.

Six dimensions were scored; more exist. Instruction-following (the redirect
violations) had no dimension and was caught only in free-text notes.

The chunk sweep could only bound significance rather than compute it, since
per-question results were not retained.

45 questions cannot resolve differences of this size. Every result in this
stage sits inside the interval widths established in
[results-summary.md](results-summary.md) §3.

---

## Future work

Deliberately not attempted, in rough order of value:

1. Real query logs. Everything measured across six stages is synthetic and
   written by the system's author.
2. Independent generation labelling by a domain expert, and Cohen's kappa
   against it on more than seven items.
3. Rebuild the identifier segment. "What does Regulation N require" is
   unanswerable from guidance documents. Questions should ask what the
   guidance says about a regulation, not what the regulation itself contains.
4. A prompt fix for source-layout narration and outside-corpus redirects.
5. Access control, deployment, monitoring - see
   [results-summary.md](results-summary.md) §8.
6. Azure reimplementation.

---
