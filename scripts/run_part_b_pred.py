"""Execution pipeline for influence predictability and recognition curves (Jacek & PERSON-6)."""

import numpy as np
import pandas as pd

from src.config import (
    DATA_PROCESSED_DIR,
    T_LONG,
    T_SHORT,
    FIGURES_DIR,
    G_DATA_PATH,
    EVAL_FRACTIONS
)

from src.plotting import set_report_style
from src.predictors import extract_influence_vector
from src.evaluation import sorted_node_indexed_value, compute_recognition_rate
from src.plotting import plot_influence, plot_recognition_rate
from src.static_network import aggregate_temporal_network
from src.data_loader import load_temporal_edgelist

def main():
    set_report_style()

    print("Running Influence computation (Jacek)...")

    saved_data = np.load(
        DATA_PROCESSED_DIR / "trajectories_gdata.npz"
    )

    nodes = saved_data.f.nodes
    trajectories = saved_data.f.trajectories

    long_influence_vector = extract_influence_vector(trajectories, T_LONG)
    long_influence_array = sorted_node_indexed_value(long_influence_vector, nodes, ascending=False)

    short_influence_vector = extract_influence_vector(trajectories, T_SHORT)

    plot_influence(long_influence_array, FIGURES_DIR / "q9_influence.pdf")

    g_data = load_temporal_edgelist(G_DATA_PATH)

    temporal_network_long = aggregate_temporal_network(g_data, t_start=1, t_end=T_LONG)
    temporal_network_short = aggregate_temporal_network(g_data, t_start=1, t_end=T_SHORT)

    degree_long_by_node = dict(temporal_network_long.degree())
    degree_short_by_node = dict(temporal_network_short.degree())

    degree_long = np.asarray([degree_long_by_node.get(node, 0) for node in nodes])
    degree_short = np.asarray([degree_short_by_node.get(node, 0) for node in nodes])

    contacts = pd.concat(
        [
            g_data[["u", "t"]].rename(columns={"u": "node"}),
            g_data[["v", "t"]].rename(columns={"v": "node"}),
        ],
        ignore_index=True,
    )
    first_contact_by_node = contacts.groupby("node")["t"].min()

    first_contact = np.asarray([first_contact_by_node.get(node, np.inf) for node in nodes])

    predictors = {
        "d^1200": degree_long,
        "d^600": degree_short,
        "-Z": -first_contact,  # Earlier contact means a higher score
        "R'": short_influence_vector,
    }
    recognition_rates = {label: [] for label in predictors}

    for f in EVAL_FRACTIONS:
        for label, predictor_scores in predictors.items():
            rate = compute_recognition_rate(
                ground_truth_ranks=long_influence_vector,
                predictor_scores=predictor_scores,
                f=f,
            )
            recognition_rates[label].append(rate)

    for label in recognition_rates:
        recognition_rates[label] = np.asarray(recognition_rates[label])

    plot_recognition_rate(recognition_rates, EVAL_FRACTIONS, FIGURES_DIR / "q10_recognition_rates.pdf")

    # TODO (PERSON-6): Load trajectories_g2.npz
    # TODO (PERSON-6): Compute centralities d^1200, d^600, Z, and R' on G_2
    # TODO (PERSON-6): Run tie-breaker and plot 4 recognition curves on G_2 (Q11b)
    pass


if __name__ == "__main__":
    main()
