"""Execution pipeline for Part A: Static Network Properties (Daniel & Polly)."""

from src.config import DATA_PROCESSED_DIR, G_DATA_PATH
from src.data_loader import load_temporal_edgelist
from src.distribution_analysis import plot_degree_distribution
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

    print("Plotting degree distribution P(k) (Q2)...")
    figure = plot_degree_distribution(G)
    output_path = DATA_PROCESSED_DIR / "degree_distribution.pdf"
    save_figure(figure, output_path)
    print(f"  Saved: {output_path}")

    # TODO (Polly): Run small-world analysis (Q6)
    # TODO (Polly): Compute and plot link weight PDF f_W(x) (Q7)


if __name__ == "__main__":
    main()
