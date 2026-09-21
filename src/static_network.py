"""Topological metric computation and aggregation utilities for Part A (Q1, Q3, Q4, Q5)."""

from typing import Any

import networkx as nx
import numpy as np
import pandas as pd


def aggregate_temporal_network(
    df: pd.DataFrame, t_start: int = 1, t_end: int = 3259
) -> nx.Graph:
    """Aggregate temporal contacts over [t_start, t_end] into an unweighted graph.

    (Used for Q1 over [1, T], Q9b over [1, 600], Q9a over [1, 1200], and Q11b).

    Args:
        df: Temporal contacts DataFrame with columns ['u', 'v', 't'].
        t_start: Inclusive start time step.
        t_end: Inclusive end time step.

    Returns:
        Unweighted NetworkX Graph containing all nodes that contacted within the window.
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("df must be a pandas DataFrame")
    if t_start > t_end:
        raise ValueError("t_start must be less than or equal to t_end")

    required_columns = {"u", "v", "t"}
    missing_columns = required_columns.difference(df.columns)
    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"df is missing required columns: {missing}")

    contacts = df.loc[df["t"].between(t_start, t_end), ["u", "v"]]

    graph = nx.Graph()
    if contacts.empty:
        return graph

    # add_edges_from also adds endpoints, so nodes with multiple contacts are
    # represented once and duplicate temporal contacts collapse to one edge.
    graph.add_edges_from(contacts.itertuples(index=False, name=None))
    return graph


def compute_topological_metrics(G: nx.Graph) -> dict[str, Any]:
    """Computes all summary topological metrics for the static aggregated graph G.

    Maps to:
        - Q1: N, link density p, standard deviation of degree sqrt(Var[D])
        - Q3: Degree assortativity rho_D
        - Q4: Clustering coefficient C
        - Q5: Average shortest path hopcount E[H] and diameter H_max

    Args:
        G: The aggregated NetworkX graph.

    Returns:
        Dictionary mapping metric names to their scalar numerical values.
    """
    if not isinstance(G, nx.Graph):
        raise TypeError("G must be a NetworkX graph")

    node_count = len(G)
    degrees = np.asarray([degree for _, degree in G.degree()], dtype=float)

    # np.std uses population variance (ddof=0), matching the degree
    # distribution of the complete observed node set.
    degree_std = float(np.std(degrees, ddof=0)) if node_count else 0.0

    if node_count < 2 or G.number_of_edges() == 0:
        assortativity = float("nan")
    else:
        assortativity = float(nx.degree_assortativity_coefficient(G))

    average_hopcount, diameter = _finite_pair_shortest_path_metrics(G)

    return {
        "N": node_count,
        "p": float(nx.density(G)),
        "sqrt_var_degree": degree_std,
        "rho_D": assortativity,
        "C": float(nx.average_clustering(G)) if node_count else 0.0,
        "E_H": average_hopcount,
        "H_max": diameter,
    }


def _finite_pair_shortest_path_metrics(G: nx.Graph) -> tuple[float, int]:
    """Return average and maximum finite hopcount across graph components.

    Cross-component node pairs have no finite shortest path. They are excluded
    from the average, while the diameter is the largest finite component
    diameter. This keeps Q5 defined for partially disconnected observations.
    """
    pair_count = 0
    distance_sum = 0
    diameter = 0

    for component_nodes in nx.connected_components(G):
        component = G.subgraph(component_nodes)
        component_size = len(component)
        if component_size < 2:
            continue

        component_nodes = list(component.nodes())
        component_distances = dict(nx.all_pairs_shortest_path_length(component))
        for source_index, source in enumerate(component_nodes[:-1]):
            distances = component_distances[source]
            for target in component_nodes[source_index + 1 :]:
                distance = distances[target]
                pair_count += 1
                distance_sum += distance
                diameter = max(diameter, distance)

    if pair_count == 0:
        return 0.0, 0
    return float(distance_sum / pair_count), int(diameter)
