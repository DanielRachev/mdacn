import networkx as nx
import pandas as pd

from src.static_network import aggregate_temporal_network, compute_topological_metrics


def test_aggregation_filters_inclusive_interval_and_deduplicates_edges():
    contacts = pd.DataFrame(
        {
            "u": [1, 2, 1, 3, 4],
            "v": [2, 1, 3, 4, 5],
            "t": [1, 2, 3, 4, 5],
        }
    )

    graph = aggregate_temporal_network(contacts, t_start=1, t_end=4)

    assert set(graph.nodes) == {1, 2, 3, 4}
    assert {frozenset(edge) for edge in graph.edges} == {
        frozenset((1, 2)),
        frozenset((1, 3)),
        frozenset((3, 4)),
    }


def test_topological_metrics_use_population_degree_std_and_finite_pairs():
    graph = nx.path_graph([1, 2, 3, 4])

    metrics = compute_topological_metrics(graph)

    assert metrics["N"] == 4
    assert metrics["p"] == 0.5
    assert metrics["sqrt_var_degree"] == 0.5
    assert metrics["C"] == 0.0
    assert metrics["E_H"] == 5 / 3
    assert metrics["H_max"] == 3
