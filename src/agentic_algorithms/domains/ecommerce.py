"""E-commerce algorithms: ranking, retrieval, bandits, metrics."""

from __future__ import annotations

import math
import random
from collections import defaultdict


def recall_at_k(relevant: set[str], ranked: list[str], k: int) -> float:
    """Recall@K for recommendation evaluation. Time O(k), space O(1)."""
    if not relevant:
        return 0.0
    hits = sum(1 for item in ranked[:k] if item in relevant)
    return hits / len(relevant)


def ndcg_at_k(relevance: dict[str, float], ranked: list[str], k: int) -> float:
    """NDCG@K with graded relevance. Time O(k), space O(1)."""

    def dcg(items: list[str]) -> float:
        score = 0.0
        for index, item in enumerate(items):
            rel = relevance.get(item, 0.0)
            score += (2**rel - 1) / math.log2(index + 2)
        return score

    ideal = dcg(sorted(relevance.keys(), key=lambda key: relevance[key], reverse=True)[:k])
    if ideal == 0:
        return 0.0
    return dcg(ranked[:k]) / ideal


def item_item_cf_scores(
    interactions: list[tuple[str, str]],
    target_item: str,
    *,
    top_k: int = 10,
) -> list[tuple[str, float]]:
    """Item-item collaborative filtering via co-occurrence. Time O(n), space O(n)."""
    users_by_item: dict[str, set[str]] = defaultdict(set)
    for user, item in interactions:
        users_by_item[item].add(user)
    target_users = users_by_item.get(target_item, set())
    if not target_users:
        return []
    scores: dict[str, float] = defaultdict(float)
    for item, users in users_by_item.items():
        if item == target_item:
            continue
        overlap = len(target_users & users)
        if overlap:
            scores[item] = overlap / math.sqrt(len(target_users) * len(users))
    ranked = sorted(scores.items(), key=lambda pair: pair[1], reverse=True)
    return ranked[:top_k]


def wide_deep_linear_score(
    features: dict[str, float],
    weights: dict[str, float],
    bias: float = 0.0,
) -> float:
    """Wide linear component (logit) for CTR models. Time O(f), space O(1)."""
    total = bias
    for key, value in features.items():
        total += weights.get(key, 0.0) * value
    return 1 / (1 + math.exp(-total))


def din_attention_weights(
    candidate_embedding: list[float],
    history_embeddings: list[list[float]],
) -> list[float]:
    """Simplified DIN attention over behavior history. Time O(h * d), space O(h)."""
    if not history_embeddings:
        return []
    weights: list[float] = []
    for embedding in history_embeddings:
        dot = sum(a * b for a, b in zip(candidate_embedding, embedding, strict=False))
        weights.append(dot)
    max_weight = max(weights)
    exp_weights = [math.exp(weight - max_weight) for weight in weights]
    total = sum(exp_weights)
    return [weight / total for weight in exp_weights]


def epsilon_greedy_select(
    arms: list[str],
    rewards: dict[str, list[float]],
    *,
    epsilon: float,
    rng: random.Random | None = None,
) -> str:
    """Epsilon-greedy bandit arm selection. Time O(a), space O(1)."""
    randomizer = rng or random.Random()
    if randomizer.random() < epsilon:
        return randomizer.choice(arms)
    best_arm = arms[0]
    best_mean = -math.inf
    for arm in arms:
        samples = rewards.get(arm, [])
        mean = sum(samples) / len(samples) if samples else 0.0
        if mean > best_mean:
            best_mean = mean
            best_arm = arm
    return best_arm


def thompson_sampling_select(
    arms: list[str],
    successes: dict[str, int],
    failures: dict[str, int],
    *,
    rng: random.Random | None = None,
) -> str:
    """Thompson sampling for Bernoulli bandits. Time O(a), space O(1)."""
    randomizer = rng or random.Random()
    best_arm = arms[0]
    best_sample = -1.0
    for arm in arms:
        alpha = successes.get(arm, 0) + 1
        beta = failures.get(arm, 0) + 1
        sample = randomizer.betavariate(alpha, beta)
        if sample > best_sample:
            best_sample = sample
            best_arm = arm
    return best_arm


def allocate_bandit_arm(
    context_key: str,
    arms: list[str],
    policy_store: dict[str, dict[str, list[float]]],
    *,
    epsilon: float = 0.1,
) -> str:
    """Context-keyed epsilon-greedy for pricing/creative slots. Time O(a)."""
    rewards = policy_store.setdefault(context_key, {arm: [] for arm in arms})
    return epsilon_greedy_select(arms, rewards, epsilon=epsilon)


def logistic_ctr_calibration(raw_scores: list[float]) -> list[float]:
    """Platt-style sigmoid calibration passthrough. Time O(n)."""
    return [1 / (1 + math.exp(-score)) for score in raw_scores]
