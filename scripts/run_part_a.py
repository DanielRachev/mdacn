"""Execution pipeline for Part A: Static Network Properties (Daniel & Polly)."""

from src.config import G_DATA_PATH
from src.data_loader import load_temporal_edgelist
from src.static_network import aggregate_temporal_network, compute_topological_metrics


def main():
    print("Loading empirical temporal network G_data...")
    df = load_temporal_edgelist(G_DATA_PATH)

    print("Aggregating network over [1, 3259]...")
    G = aggregate_temporal_network(df, t_start=1, t_end=3259)

    print("Computing topological metrics (Q1, Q3, Q4, Q5)...")
    metrics = compute_topological_metrics(G)
    for k, v in metrics.items():
        print(f"  {k}: {v}")

    # TODO (Daniel): Plot degree distribution P(k) (Q2)
    # TODO (Polly): Run small-world analysis (Q6)
    # TODO (Polly): Compute and plot link weight PDF f_W(x) (Q7)


if __name__ == "__main__":
    main()
