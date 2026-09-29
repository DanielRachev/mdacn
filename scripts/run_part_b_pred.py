"""Execution pipeline for influence predictability and recognition curves (Jacek & Jakub)."""

import numpy as np

from src.config import (
    DATA_PROCESSED_DIR,
    FIGURES_DIR,
    G_DATA_PATH,
    G_2_PATH,
    EVAL_FRACTIONS,
    T_LONG,
    T_SHORT,
    TIE_BREAK_ITERATIONS,
    RANDOM_SEED,
)
from src.evaluation import compute_recognition_rate, sorted_node_indexed_value
from src.plotting import (
    plot_influence,
    plot_recognition_rate,
    plot_recognition_rates_gdata_vs_g2,
    set_report_style,
)
from src.predictors import (
    compute_aggregated_degree_predictor,
    compute_first_contact_time_predictor,
    extract_influence_vector,
)
from src.data_loader import load_temporal_edgelist


def print_influence_values(label, nodes, influence, first_contact):
    """Print influence and first-contact values."""
    values, counts = np.unique(influence, return_counts=True)
    print(
        f"Values for {label} at t={T_LONG}: "
        f"min={int(influence.min())}, median={np.median(influence):.6g}, "
        f"max={int(influence.max())}"
    )
    print(
        "  influence counts (value: node_count): "
        + ", ".join(f"{int(value)}:{int(count)}" for value, count in zip(values, counts))
    )

    ranked_influence = np.sort(influence)[::-1]
    ranks = sorted({1, 250, 370, len(nodes)})
    print(
        "  influence at ranks (rank: value): "
        + ", ".join(f"{rank}:{int(ranked_influence[rank - 1])}" for rank in ranks)
    )
    print(f"  median first-contact time: {np.median(first_contact):.6g}")

    late_contact_indices = np.flatnonzero(first_contact > T_LONG)
    if late_contact_indices.size:
        late_contacts = ", ".join(
            f"node {int(nodes[index])}:t={int(first_contact[index])},I={int(influence[index])}"
            for index in late_contact_indices
        )
        print(f"  nodes first contacting after t={T_LONG}: {late_contacts}")


def print_recognition_values(label, recognition_rates, fractions, influence):
    """Print every recognition value plotted and mean baseline gap."""
    fraction_values = np.asarray(fractions, dtype=float)
    tie_counts = np.unique(influence, return_counts=True)[1]
    dominant_tie_count = int(tie_counts.max())
    print(
        f"Recognition rates for {label} "
        f"({TIE_BREAK_ITERATIONS} tie samples, seed {RANDOM_SEED}):"
    )
    for index, fraction in enumerate(fraction_values):
        row = ", ".join(
            f"{metric}={rates[index]:.6f}"
            for metric, rates in recognition_rates.items()
        )
        if label == "G_2":
            top_k = round(float(fraction) * len(influence))
            row += (
                f", k={top_k}, tie-only expectation "
                f"k/{dominant_tie_count}={top_k / dominant_tie_count:.6f}"
            )
        print(f"  f={fraction:.2f}: {row}")

    print("  mean absolute distance from random baseline r(f)=f:")
    for metric, rates in recognition_rates.items():
        distance = np.mean(np.abs(rates - fraction_values))
        print(f"    {metric}: {distance:.6f}")


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
        long_influence_array = sorted_node_indexed_value(
            long_influence_vector, nodes, ascending=False
        )

        short_influence_vector = extract_influence_vector(trajectories, T_SHORT)

        plot_influence(
            long_influence_array, FIGURES_DIR / f"influence_{dataset_id}.pdf"
        )

        g = load_temporal_edgelist(dataset_raw)

        degree_long = compute_aggregated_degree_predictor(g, T_LONG, nodes)
        degree_short = compute_aggregated_degree_predictor(g, T_SHORT, nodes)

        first_contact = compute_first_contact_time_predictor(g, nodes)
        network_label = "G_data" if dataset_id == "gdata" else "G_2"
        print_influence_values(
            network_label, nodes, long_influence_vector, first_contact
        )

        predictors = {
            "$d^{1200}$": degree_long,
            "$d^{600}$": degree_short,
            "$-Z$": -first_contact,  # Earlier contact means a higher score
            "$R'$": short_influence_vector,
        }
        recognition_rates = {label: [] for label in predictors}

        for f in EVAL_FRACTIONS:
            for metric_label, predictor_scores in predictors.items():
                rate = compute_recognition_rate(
                    ground_truth_ranks=long_influence_vector,
                    predictor_scores=predictor_scores,
                    f=f,
                    num_iterations=TIE_BREAK_ITERATIONS,
                    seed=RANDOM_SEED,
                )
                recognition_rates[metric_label].append(rate)

        for metric_label in recognition_rates:
            recognition_rates[metric_label] = np.asarray(
                recognition_rates[metric_label]
            )

        datasets_recognition_rates[dataset_id] = recognition_rates
        print_recognition_values(
            network_label, recognition_rates, EVAL_FRACTIONS, long_influence_vector
        )

        if dataset_id == "gdata":
            comparison_index = EVAL_FRACTIONS.index(0.4)
            difference = (
                recognition_rates["$R'$"][comparison_index]
                - recognition_rates["$-Z$"][comparison_index]
            )
            print(f"  R' minus -Z at f=0.40: {difference:.6f}")

        plot_recognition_rate(
            recognition_rates,
            EVAL_FRACTIONS,
            FIGURES_DIR / f"recognition_rates_{dataset_id}.pdf",
            dataset_id == "g2",
        )

    plot_recognition_rates_gdata_vs_g2(
        datasets_recognition_rates["gdata"],
        datasets_recognition_rates["g2"],
        EVAL_FRACTIONS,
        FIGURES_DIR / "recognition_rates_comparison.pdf",
    )


if __name__ == "__main__":
    main()
