"""Tie-breaking and ranking evaluation metrics (Q9, Q10, Q11b)."""

import numpy as np


def compute_recognition_rate(
    ground_truth_ranks: np.ndarray,
    predictor_scores: np.ndarray,
    f: float,
    num_iterations: int = 1000,
    seed: int = 42,
) -> float:
    """Compute top-f recognition rate with randomized tie-breaking.

    If multiple nodes share the same ranking score, R_f or D_f is sampled uniformly
    at random from the possible choices over `num_iterations` iterations, and the
    resulting overlap fraction is averaged.

    Args:
        ground_truth_ranks: Influence scores or target ranks (for example, R at t=1200).
        predictor_scores: Predictor centrality scores (for example, degree or R').
        f: Target top fraction (e.g., 0.05, 0.10, ..., 0.50).
        num_iterations: Number of randomized resamples (default: 1000).
        seed: Random seed for deterministic reproducibility.

    Returns:
        Average recognition rate r(f) in [0.0, 1.0].

    Notes:
        Values are interpreted as scores, so larger values rank higher. Pass
        ``-first_contact_time`` for a predictor where smaller values are better.
        Ties at the top-k boundary are sampled uniformly and independently for
        the ground-truth and predictor arrays.
    """
    ground_truth = _as_score_array(ground_truth_ranks, "ground_truth_ranks")
    predictor = _as_score_array(predictor_scores, "predictor_scores")
    if ground_truth.size != predictor.size:
        raise ValueError(
            "ground_truth_ranks and predictor_scores must have equal length"
        )
    if ground_truth.size == 0:
        raise ValueError("recognition rate is undefined for empty arrays")
    if not np.isfinite(f) or not 0.0 < f <= 1.0:
        raise ValueError("f must be in the interval (0, 1]")
    if not isinstance(num_iterations, (int, np.integer)) or isinstance(
        num_iterations, bool
    ):
        raise TypeError("num_iterations must be an integer")
    if num_iterations < 1:
        raise ValueError("num_iterations must be positive")

    node_count = ground_truth.size
    top_k = round(float(f) * node_count)
    if top_k < 1:
        raise ValueError("f is too small to select at least one node")
    top_k = min(top_k, node_count)

    rng = np.random.default_rng(seed)
    overlaps = np.empty(num_iterations, dtype=float)
    for iteration in range(num_iterations):
        ground_truth_top = _sample_top_k(ground_truth, top_k, rng)
        predictor_top = _sample_top_k(predictor, top_k, rng)
        overlaps[iteration] = len(ground_truth_top.intersection(predictor_top)) / top_k

    return float(overlaps.mean())


def evaluate_recognition_curve(
    ground_truth_ranks: np.ndarray,
    predictor_scores: np.ndarray,
    fractions: list[float],
    num_iterations: int = 1000,
    seed: int = 42,
) -> np.ndarray:
    """Evaluates the recognition rate across a list of fractions f in [0.05, 0.50]."""
    return np.asarray(
        [
            compute_recognition_rate(
                ground_truth_ranks,
                predictor_scores,
                f,
                num_iterations=num_iterations,
                seed=seed,
            )
            for f in fractions
        ],
        dtype=float,
    )


def _as_score_array(values: np.ndarray, name: str) -> np.ndarray:
    """Convert one-dimensional ranking scores to float, treating NaN as lowest."""
    array = np.asarray(values)
    if array.ndim != 1:
        raise ValueError(f"{name} must be one-dimensional")
    try:
        scores = array.astype(float, copy=True)
    except (TypeError, ValueError) as exc:
        raise TypeError(f"{name} must contain numeric scores") from exc
    scores[np.isnan(scores)] = -np.inf
    return scores


def _sample_top_k(scores: np.ndarray, top_k: int, rng: np.random.Generator) -> set[int]:
    """Sample one uniformly random top-k set induced by score ties."""
    order = np.argsort(-scores, kind="stable")
    selected: list[int] = []
    position = 0

    while len(selected) < top_k:
        group_end = position + 1
        while (
            group_end < scores.size
            and scores[order[group_end]] == scores[order[position]]
        ):
            group_end += 1

        group = order[position:group_end]
        needed = min(top_k - len(selected), group.size)
        if needed == group.size:
            selected.extend(int(index) for index in group)
        else:
            sampled = rng.choice(group, size=needed, replace=False)
            selected.extend(int(index) for index in sampled)
        position = group_end

    return set(selected)
