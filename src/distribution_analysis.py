"""Degree and weight distribution analysis, and small-world testing (Q2, Q6, Q7)."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd


def compute_degree_distribution(G: nx.Graph) -> tuple[np.ndarray, np.ndarray]:
    """Computes empirical degree distribution P(k) for Q2.

    Args:
        G: Aggregated static graph.

    Returns:
        Tuple of (degrees, probabilities).
    """
    if not isinstance(G, nx.Graph):
        raise TypeError("G must be a NetworkX graph")

    degree_sequence = np.asarray([degree for _, degree in G.degree()], dtype=int)
    if degree_sequence.size == 0:
        return np.array([], dtype=int), np.array([], dtype=float)

    degrees, counts = np.unique(degree_sequence, return_counts=True)
    probabilities = counts.astype(float) / degree_sequence.size
    return degrees, probabilities


def plot_degree_distribution(
    G: nx.Graph, output_path: Path | str | None = None
) -> plt.Figure:
    """Plot empirical degree probabilities on logarithmic axes.

    Zero-degree nodes cannot appear on a logarithmic x-axis. They are reported
    in the plot annotation while positive degrees are shown as log-log points.
    The figure is returned for callers that need further formatting or testing.
    """
    degrees, probabilities = compute_degree_distribution(G)
    figure, axis = plt.subplots()

    positive = (degrees > 0) & (probabilities > 0)
    if np.any(positive):
        axis.loglog(
            degrees[positive],
            probabilities[positive],
            marker="o",
            linestyle="-",
            label="Empirical $P(k)$",
        )
    elif degrees.size:
        axis.text(
            0.5,
            0.5,
            "Only zero-degree nodes",
            ha="center",
            va="center",
            transform=axis.transAxes,
        )

    zero_probability = 0.0
    if degrees.size and degrees[0] == 0:
        zero_probability = float(probabilities[0])
    if zero_probability:
        axis.annotate(
            f"$P(0)={zero_probability:.3g}$",
            xy=(0.03, 0.97),
            xycoords="axes fraction",
            ha="left",
            va="top",
        )

    axis.set_xlabel("Degree $k$")
    axis.set_ylabel("Probability $P(k)$")
    axis.set_title("Empirical degree distribution")
    axis.grid(True, which="both", alpha=0.25)
    if np.any(positive):
        axis.legend()

    if output_path is not None:
        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        figure.savefig(
            output,
            format=output.suffix.lstrip(".") or "pdf",
            dpi=300,
            bbox_inches="tight",
        )

    return figure


def evaluate_small_world_property(G: nx.Graph) -> dict[str, float]:
    """Quantitatively tests the small-world property using criteria from Lecture 2 (Q6).

    Compares empirical clustering C and average path length L against an equivalent
    Erdős-Rényi random graph baseline: C_rand = <k>/N, L_rand ~ ln(N)/ln(<k>).

    Args:
        G: Aggregated static graph.

    Returns:
        Dictionary containing empirical and random benchmark metrics:
        C, C_rand, L, L_rand, and sigma.
    """
    # TODO (Polly): Compute empirical C and L
    # TODO (Polly): Compute theoretical or simulated random graph baselines
    # (C_rand, L_rand)
    # TODO (Polly): Calculate small-world ratio sigma = (C / C_rand) / (L / L_rand)
    pass


def compute_link_weight_pdf(
    df: pd.DataFrame, t_start: int = 1, t_end: int = 3259
) -> tuple[np.ndarray, np.ndarray]:
    """Computes the probability density function f_W(x) of link weights for Q7.

    Link weight W is the total contact count per connected node pair over [1, T].
    Uses normalized bins such that f_W(x) = Pr[x < W <= x + dx] / dx.

    Args:
        df: Temporal contacts DataFrame.
        t_start: Start step (default: 1).
        t_end: End step (default: 3259).

    Returns:
        Tuple of (bin_centers, normalized_density_values).
    """
    # TODO (Polly): Group by pairs (u, v) to count interaction occurrences
    # TODO (Polly): Select appropriate logarithmic or custom binning
    # TODO (Polly): Compute normalized PDF values dividing probability by bin width dx
    pass
