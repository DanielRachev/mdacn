import networkx as nx
import numpy as np
import pandas as pd

from src.distribution_analysis import (
    compute_degree_distribution,
    compute_link_weight_pdf,
    evaluate_small_world_property,
)


def test_degree_distribution_is_normalized_and_includes_isolates():
    graph = nx.Graph([(1, 2), (2, 3)])
    graph.add_node(4)

    degrees, probabilities = compute_degree_distribution(graph)

    np.testing.assert_array_equal(degrees, np.array([0, 1, 2]))
    np.testing.assert_allclose(probabilities, np.array([0.25, 0.5, 0.25]))


def test_small_world_property_returns_finite_benchmark_metrics():
    graph = nx.watts_strogatz_graph(20, 4, 0.1, seed=42)

    metrics = evaluate_small_world_property(graph)

    assert set(metrics) == {"C", "C_rand", "L", "L_rand", "sigma"}
    assert np.isfinite(metrics["C"])
    assert np.isfinite(metrics["C_rand"])
    assert np.isfinite(metrics["L"])
    assert np.isfinite(metrics["L_rand"])
    assert np.isfinite(metrics["sigma"])
    assert metrics["sigma"] > 0.0


def test_link_weight_pdf_is_normalized_for_repeated_contacts():
    df = pd.DataFrame(
        {
            "u": [1, 1, 1, 2, 2, 3],
            "v": [2, 2, 2, 3, 3, 4],
            "t": [1, 2, 5, 1, 2, 3],
        }
    )

    centers, pdf, bin_edges = compute_link_weight_pdf(df)

    assert centers.size == pdf.size
    assert centers.size > 0
    assert np.all(np.isfinite(centers))
    assert np.all(np.isfinite(pdf))
    assert np.all(pdf >= 0)

    bin_widths = np.diff(bin_edges)
    assert np.isclose(np.sum(pdf * bin_widths), 1.0, atol=1e-12)
