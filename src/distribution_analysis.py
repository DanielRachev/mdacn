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


def evaluate_small_world_property(
    G: nx.Graph, num_random_graphs: int = 10, seed: int = 0
) -> dict[str, float]:
    """Compare the empirical graph to matched Erdős-Rényi random graphs (Q6).

    The asymptotic formula from lecture notes is not reliable for a relatively dense
    network. To obtain a faithful baseline, we sample multiple G(n, m) graphs with
    the same node and edge counts as the observed network and compare the empirical
    clustering coefficient and average path length against the random-graph mean.

    Args:
        G: Aggregated static graph.
        num_random_graphs: Number of random-graph realizations to sample.
        seed: Base random seed for reproducibility.

    Returns:
        Dictionary containing empirical and random benchmark metrics:
        C, C_rand, L, L_rand, and sigma.
    """
    if not isinstance(G, nx.Graph):
        raise TypeError("G must be a NetworkX graph")

    node_count = G.number_of_nodes()
    edge_count = G.number_of_edges()
    if node_count == 0 or edge_count == 0:
        return {"C": 0.0, "C_rand": 0.0, "L": 0.0, "L_rand": 0.0, "sigma": 0.0}

    clustering = float(nx.average_clustering(G))
    path_length = _average_shortest_path_length(G)

    rng = np.random.default_rng(seed)
    random_clusterings: list[float] = []
    random_path_lengths: list[float] = []

    for _ in range(max(1, num_random_graphs)):
        random_seed = int(rng.integers(0, 2**31 - 1))
        random_graph = nx.gnm_random_graph(node_count, edge_count, seed=random_seed)
        random_clusterings.append(float(nx.average_clustering(random_graph)))
        random_path_lengths.append(_average_shortest_path_length(random_graph))

    c_rand = float(np.mean(random_clusterings)) if random_clusterings else 0.0
    l_rand = float(np.mean(random_path_lengths)) if random_path_lengths else 0.0

    sigma = 0.0
    if c_rand > 0.0 and path_length > 0.0 and l_rand > 0.0:
        sigma = (clustering / c_rand) / (path_length / l_rand)

    return {
        "C": clustering,
        "C_rand": c_rand,
        "L": path_length,
        "L_rand": l_rand,
        "sigma": float(sigma),
    }


def _average_shortest_path_length(G: nx.Graph) -> float:
    """Return the average shortest path length of the largest connected component."""
    if G.number_of_nodes() == 0:
        return 0.0

    if nx.is_connected(G):
        return float(nx.average_shortest_path_length(G))

    components = sorted(nx.connected_components(G), key=len, reverse=True)
    largest = components[0] if components else set()
    if len(largest) < 2:
        return 0.0

    return float(nx.average_shortest_path_length(G.subgraph(largest)))


def plot_small_world_comparison(
    G: nx.Graph, output_path: Path | str | None = None, num_random_graphs: int = 10, seed: int = 0
) -> plt.Figure:
    """Plot empirical clustering and path length against matched random graphs."""
    metrics = evaluate_small_world_property(G, num_random_graphs=num_random_graphs, seed=seed)
    figure, (axis_c, axis_l) = plt.subplots(1, 2, figsize=(7.5, 3.2))

    labels = ["Empirical", "Matched ER"]
    cluster_values = [metrics["C"], metrics["C_rand"]]
    path_values = [metrics["L"], metrics["L_rand"]]

    axis_c.bar(labels, cluster_values, color=["tab:blue", "tab:orange"])
    axis_c.set_title("Clustering")
    axis_c.set_ylabel("$C$")

    axis_l.bar(labels, path_values, color=["tab:blue", "tab:orange"])
    axis_l.set_title("Average path length")
    axis_l.set_ylabel("$L$")

    figure.tight_layout()

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


def compute_link_weight_pdf(
    df: pd.DataFrame, t_start: int = 1, t_end: int = 3259
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
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
        return centers, density

    # bin_edges = np.geomspace(weight_min, weight_max, num=max(20, min(60, 2 * positive_weights.size + 1)))
    # density, bin_edges = np.histogram(positive_weights, bins=bin_edges, density=True)
    # centers = 0.5 * (bin_edges[:-1] + bin_edges[1:])
    # return centers, density, bin_edges

    raw_edges = np.geomspace(weight_min, weight_max + 1, num=30)
    bin_edges = np.unique(np.floor(raw_edges).astype(int))

    if bin_edges[0] > weight_min:
        bin_edges = np.insert(bin_edges, 0, weight_min)

    if bin_edges[-1] <= weight_max:
        bin_edges = np.append(bin_edges, weight_max + 1)

    density, bin_edges = np.histogram(positive_weights, bins=bin_edges, density=True)
    centers = np.sqrt(bin_edges[:-1] * bin_edges[1:])

    return centers, density, bin_edges


def plot_link_weight_distribution(
    df: pd.DataFrame, t_start: int = 1, t_end: int = 3259, output_path: Path | str | None = None
) -> plt.Figure:
    """Plot the empirical link-weight PDF for the aggregated contact network."""
    centers, density, _ = compute_link_weight_pdf(df, t_start=t_start, t_end=t_end)
    figure, axis = plt.subplots()

    if centers.size and density.size:
        # plot_density = np.where(density > 0, density, np.nan)
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
