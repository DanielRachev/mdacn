"""Execution pipeline for influence predictability and recognition curves (Jacek & Jakub)."""

import numpy as np
import pandas as pd

from src.config import (
    DATA_PROCESSED_DIR,
    T_LONG,
    T_SHORT,
    FIGURES_DIR,
    G_DATA_PATH,
    G_2_PATH,
    EVAL_FRACTIONS
)

from src.plotting import set_report_style
from src.predictors import extract_influence_vector, compute_first_contact_time_predictor, compute_aggregated_degree_predictor
from src.evaluation import sorted_node_indexed_value, compute_recognition_rate
from src.plotting import plot_influence, plot_recognition_rate, plot_recognition_rates_gdata_vs_g2
from src.static_network import aggregate_temporal_network
from src.data_loader import load_temporal_edgelist

def main():
    set_report_style()

    # Effectively, the same set of operations is performed on two datasets
    datasets = [
        ("trajectories_gdata.npz", G_DATA_PATH, "gdata", "Jacek"),
        ("trajectories_g2.npz", G_2_PATH, "g2", "Jakub")
    ]
    datasets_recognition_rates = {}

    for dataset_processed, dataset_raw, dataset_id, author in datasets:
        print(f"Running Influence computation ({author})...")

        saved_data = np.load(
            DATA_PROCESSED_DIR / dataset_processed
        )

        nodes = saved_data.f.nodes
        trajectories = saved_data.f.trajectories

        long_influence_vector = extract_influence_vector(trajectories, T_LONG)
        long_influence_array = sorted_node_indexed_value(long_influence_vector, nodes, ascending=False)

        short_influence_vector = extract_influence_vector(trajectories, T_SHORT)

        plot_influence(long_influence_array, FIGURES_DIR / f"influence_{dataset_id}.pdf")

        g = load_temporal_edgelist(dataset_raw)

        degree_long = compute_aggregated_degree_predictor(g, T_LONG, nodes)
        degree_short = compute_aggregated_degree_predictor(g, T_SHORT, nodes)

        first_contact = compute_first_contact_time_predictor(g, nodes)

        predictors = {
            "$d^{1200}$": degree_long,
            "$d^{600}$": degree_short,
            "$-Z$": -first_contact,  # Earlier contact means a higher score
            "$R'$": short_influence_vector,
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

        datasets_recognition_rates[dataset_id] = recognition_rates

        plot_recognition_rate(recognition_rates, EVAL_FRACTIONS, FIGURES_DIR / f"recognition_rates_{dataset_id}.pdf", dataset_id == "g2") # G2 check is used to separate plots, because they coincide too much

    plot_recognition_rates_gdata_vs_g2(datasets_recognition_rates["gdata"], datasets_recognition_rates["g2"], EVAL_FRACTIONS, FIGURES_DIR / "recognition_rates_comparison.pdf")
    pass


if __name__ == "__main__":
    main()
