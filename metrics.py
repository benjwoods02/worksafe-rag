"""Retrieval metrics.

Measure retrieval SEPARATELY from generation. recall@k is an upper bound on the
fraction of questions the whole system can possibly answer correctly -- if the
right chunk is never retrieved, no amount of prompt tuning recovers it.

None of this calls a model, so the entire measurement programme is free.
"""
from __future__ import annotations

import math
from collections import defaultdict


def recall_at_k(retrieved: list[str], relevant: set[str], k: int) -> float:
    """Fraction of the relevant chunks that appear in the top k."""
    if not relevant:
        return float("nan")      # unanswerable questions: see refusal_rate
    return len(set(retrieved[:k]) & relevant) / len(relevant)


def hit_at_k(retrieved: list[str], relevant: set[str], k: int) -> float:
    """1.0 if ANY relevant chunk is in the top k.

    Often the metric that matters more than recall: a generator usually needs
    one good chunk, not all of them.
    """
    if not relevant:
        return float("nan")
    return 1.0 if set(retrieved[:k]) & relevant else 0.0


def mrr(retrieved: list[str], relevant: set[str]) -> float:
    """Reciprocal of the rank of the first relevant chunk. Rewards ranking."""
    if not relevant:
        return float("nan")
    for rank, chunk_id in enumerate(retrieved, start=1):
        if chunk_id in relevant:
            return 1.0 / rank
    return 0.0


def ndcg_at_k(retrieved: list[str], relevant: set[str], k: int) -> float:
    """Discounted gain, normalised against a perfect ranking.

    Unlike recall it cares WHERE the hits landed, so it separates "found it at
    rank 1" from "found it at rank 5".
    """
    if not relevant:
        return float("nan")
    dcg = sum(1.0 / math.log2(rank + 1)
              for rank, cid in enumerate(retrieved[:k], start=1) if cid in relevant)
    ideal = sum(1.0 / math.log2(rank + 1)
                for rank in range(1, min(len(relevant), k) + 1))
    return dcg / ideal if ideal else float("nan")


def top_score_gap(scores: list[float]) -> float:
    """score[0] - score[1]. A flat top of the ranking means the retriever
    could not discriminate, which is invisible in recall alone."""
    return (scores[0] - scores[1]) if len(scores) >= 2 else float("nan")


def _mean(values: list[float]) -> float:
    real = [v for v in values if not math.isnan(v)]
    return sum(real) / len(real) if real else float("nan")


def aggregate(rows: list[dict], ks=(1, 3, 5, 10)) -> dict:
    """rows: [{"retrieved": [...], "relevant": {...}, "scores": [...]}, ...]

    Questions with empty ground truth (the unanswerable segment) are excluded
    from recall-style metrics -- there is nothing to recall -- and reported
    separately as a false-retrieval rate.
    """
    answerable = [r for r in rows if r["relevant"]]
    unanswerable = [r for r in rows if not r["relevant"]]

    out: dict[str, float] = {"n": len(rows), "n_answerable": len(answerable)}
    for k in ks:
        out[f"recall@{k}"] = _mean([recall_at_k(r["retrieved"], r["relevant"], k) for r in answerable])
        out[f"hit@{k}"] = _mean([hit_at_k(r["retrieved"], r["relevant"], k) for r in answerable])
        out[f"ndcg@{k}"] = _mean([ndcg_at_k(r["retrieved"], r["relevant"], k) for r in answerable])
    out["mrr"] = _mean([mrr(r["retrieved"], r["relevant"]) for r in answerable])
    out["top_gap"] = _mean([top_score_gap(r.get("scores", [])) for r in rows])

    if unanswerable:
        # Retrieval always returns a top-k, so this is not "did it return
        # nothing" -- it is how confidently it returned junk. Track the mean
        # top score; a good system should score these lower than real queries.
        out["unanswerable_n"] = len(unanswerable)
        out["unanswerable_top_score"] = _mean(
            [r["scores"][0] for r in unanswerable if r.get("scores")])
    return out


def by_segment(rows: list[dict], ks=(1, 5)) -> dict[str, dict]:
    """Per-segment breakdown.

    This is the point of the whole exercise. Keyword search will barely move
    aggregate recall -- most questions are conceptual and already handled --
    but should take identifier queries from near zero to near one. Reported as
    a single average, the best improvement in the project looks like noise.
    """
    groups: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        groups[row.get("segment", "unlabelled")].append(row)
    return {name: aggregate(group, ks) for name, group in sorted(groups.items())}


def format_report(result: dict, segments: dict | None = None) -> str:
    lines = ["", f"n={result['n']}  answerable={result['n_answerable']}", "-" * 52]
    for key, value in result.items():
        if key.startswith("n") and not key.startswith("ndcg"):
            continue
        lines.append(f"  {key:<24} {value:.3f}" if not math.isnan(value)
                     else f"  {key:<24}     --")
    if segments:
        for name, scores in segments.items():
            lines.append(f"\n  [{name}]  n={scores['n']}")
            for key, value in scores.items():
                if key.startswith("n") and not key.startswith("ndcg"):
                    continue
                lines.append(f"    {key:<22} {value:.3f}" if not math.isnan(value)
                             else f"    {key:<22}     --")
    return "\n".join(lines)
