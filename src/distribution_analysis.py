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

    node_count = G.number_of_nodes()
    edge_count = G.number_of_edges()
    if node_count == 0 or edge_count == 0:
        return {"C": 0.0, "C_rand": 0.0, "L": 0.0, "L_rand": 0.0, "sigma": 0.0}

    clustering = float(nx.average_clustering(G))

    if nx.is_connected(G):
        path_length = float(nx.average_shortest_path_length(G))
    else:
        path_lengths: list[float] = []
        for component_nodes in nx.connected_components(G):
            component = G.subgraph(component_nodes)
            if len(component) < 2:
                continue
            for source in component.nodes():
                lengths = nx.shortest_path_length(component, source)
                for target, distance in lengths.items():
                    if source < target:
                        path_lengths.append(float(distance))
        path_length = float(np.mean(path_lengths)) if path_lengths else 0.0

    avg_degree = (2.0 * edge_count) / node_count
    if node_count <= 1:
        c_rand = 0.0
        l_rand = 0.0
    else:
        c_rand = avg_degree / (node_count - 1)
        if avg_degree > 2.0:
            l_rand = float(np.log(node_count) / np.log(max(avg_degree - 1.0, 1.0)))
        else:
            l_rand = float("inf")

    sigma = 0.0
    if c_rand > 0.0 and path_length > 0.0 and np.isfinite(l_rand) and l_rand > 0.0:
        sigma = (clustering / c_rand) / (path_length / l_rand)

    return {
        "C": clustering,
        "C_rand": c_rand,
        "L": path_length,
        "L_rand": l_rand,
        "sigma": float(sigma),
    }


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

    required_columns = {"u", "v", "t"}
    missing_columns = required_columns.difference(df.columns)
    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"df is missing required columns: {missing}")

    filtered = df.loc[df["t"].between(t_start, t_end, inclusive="both"), ["u", "v"]]
    if filtered.empty:
        return np.array([], dtype=float), np.array([], dtype=float)

    pair_keys = filtered.apply(lambda row: tuple(sorted((row["u"], row["v"]))), axis=1)
    weights = pair_keys.value_counts().to_numpy(dtype=float)
    if weights.size == 0:
        return np.array([], dtype=float), np.array([], dtype=float)

    positive_weights = weights[weights > 0]
    if positive_weights.size == 0:
        return np.array([], dtype=float), np.array([], dtype=float)

    weight_min = float(positive_weights.min())
    weight_max = float(positive_weights.max())
    if weight_min == weight_max:
        width = max(weight_min / 2.0, 1.0)
        centers = np.array([weight_min - width / 2.0, weight_min + width / 2.0], dtype=float)
        density = np.array([1.0 / max(width, 1e-9), 1.0 / max(width, 1e-9)], dtype=float)
        area = float(np.trapezoid(density, centers))
        if area > 0.0:
            density = density / area
        return centers, density

    bin_edges = np.geomspace(weight_min, weight_max, num=max(20, min(60, 2 * positive_weights.size + 1)))
    density, bin_edges = np.histogram(positive_weights, bins=bin_edges, density=True)
    centers = 0.5 * (bin_edges[:-1] + bin_edges[1:])
    area = float(np.trapezoid(density, centers))
    if area > 0.0:
        density = density / area
    return centers, density


def plot_link_weight_distribution(
    df: pd.DataFrame, t_start: int = 1, t_end: int = 3259, output_path: Path | str | None = None
) -> plt.Figure:
    """Plot the empirical link-weight PDF for the aggregated contact network."""
    centers, density = compute_link_weight_pdf(df, t_start=t_start, t_end=t_end)
    figure, axis = plt.subplots()

    if centers.size and density.size:
        axis.plot(centers, density, marker="o", linestyle="-", color="tab:green")
        axis.set_xscale("log")
        axis.set_yscale("log")

    axis.set_xlabel("Link weight $W$")
    axis.set_ylabel("Probability density $f_W(W)$")
    axis.set_title("Empirical link-weight distribution")
    axis.grid(True, which="both", alpha=0.25)

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
