"""Execution pipeline for Part A: Static Network Properties (Daniel & Polly)."""

import numpy as np

from src.config import FIGURES_DIR, G_DATA_PATH
from src.data_loader import load_temporal_edgelist
from src.distribution_analysis import (
    evaluate_small_world_property,
    plot_degree_distribution,
    plot_link_weight_distribution,
)
from src.plotting import save_figure, set_report_style
from src.static_network import aggregate_temporal_network, compute_topological_metrics


def main():
    set_report_style()
    print("Loading empirical temporal network G_data...")
    df = load_temporal_edgelist(G_DATA_PATH)

    print("Aggregating network over [1, 3259]...")
    G = aggregate_temporal_network(df, t_start=1, t_end=3259)

    print("Computing topological metrics (Q1, Q3, Q4, Q5)...")
    metrics = compute_topological_metrics(G)
    for k, v in metrics.items():
        print(f"  {k}: {v}")

    degrees = np.fromiter((degree for _, degree in G.degree()), dtype=float)
    er_degree_std = np.sqrt((len(G) - 1) * metrics["p"] * (1 - metrics["p"]))
    print("Values used for degree-distribution comparison:")
    print(f"  M: {G.number_of_edges()}")
    print(f"  mean_degree: {degrees.mean():.12g}")
    print(f"  max_degree: {int(degrees.max())}")
    print(f"  ER_expected_degree_std: {er_degree_std:.12g}")
    ratio = metrics["sqrt_var_degree"] / er_degree_std
    print(f"  observed_to_ER_degree_std_ratio: {ratio:.12g}")

    print("Plotting degree distribution P(k) (Q2)...")
    figure = plot_degree_distribution(G)
    output_path = FIGURES_DIR / "degree_distribution.pdf"
    save_figure(figure, output_path)
    print(f"  Saved: {output_path}")

    print("Evaluating small-world benchmark (Q6)...")
    small_world = evaluate_small_world_property(G)
    for key, value in small_world.items():
        print(f"  {key}: {value}")

    print("Computing and plotting link-weight PDF f_W(x) (Q7)...")
    weight_figure = plot_link_weight_distribution(df, t_start=1, t_end=3259)
    weight_output = FIGURES_DIR / "link_weight_distribution.pdf"
    save_figure(weight_figure, weight_output)
    print(f"  Saved: {weight_output}")


if __name__ == "__main__":
    main()
