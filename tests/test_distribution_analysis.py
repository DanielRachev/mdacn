import networkx as nx
import numpy as np

from src.distribution_analysis import compute_degree_distribution


def test_degree_distribution_is_normalized_and_includes_isolates():
    graph = nx.Graph([(1, 2), (2, 3)])
    graph.add_node(4)

    degrees, probabilities = compute_degree_distribution(graph)

    np.testing.assert_array_equal(degrees, np.array([0, 1, 2]))
    np.testing.assert_allclose(probabilities, np.array([0.25, 0.5, 0.25]))
