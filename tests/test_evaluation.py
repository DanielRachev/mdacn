import numpy as np

from src.evaluation import compute_recognition_rate, evaluate_recognition_curve


def test_recognition_rate_is_one_without_ties():
    scores = np.array([4, 3, 2, 1])

    assert compute_recognition_rate(scores, scores, f=0.5) == 1.0


def test_recognition_rate_samples_independent_ties():
    scores = np.array([3, 1, 1, 1])

    rate = compute_recognition_rate(
        scores, scores, f=0.5, num_iterations=12000, seed=42
    )

    # Node 0 is always selected. One of the other three tied nodes is chosen
    # independently by each ranking, so expected overlap is (1 + 1/3) / 2.
    assert abs(rate - (2 / 3)) < 0.02
    assert rate == compute_recognition_rate(
        scores, scores, f=0.5, num_iterations=12000, seed=42
    )


def test_recognition_curve_returns_one_value_per_fraction():
    ground_truth = np.array([4, 3, 2, 1])
    predictor = np.array([4, 2, 3, 1])

    curve = evaluate_recognition_curve(ground_truth, predictor, [0.25, 0.5])

    assert curve.shape == (2,)
    assert np.all((curve >= 0.0) & (curve <= 1.0))
