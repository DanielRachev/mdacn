"""Degree and weight distribution analysis, and small-world testing (Q2, Q6, Q7)."""

from typing import Dict, Tuple
import networkx as nx
import numpy as np
import pandas as pd


def compute_degree_distribution(G: nx.Graph) -> Tuple[np.ndarray, np.ndarray]:
    """Computes empirical degree distribution P(k) for Q2.

    Args:
        G: Aggregated static graph.

    Returns:
        Tuple of (degrees, probabilities).
    """
    # TODO (PERSON-1): Extract degree sequence and compute normalized degree frequencies
    pass


def evaluate_small_world_property(G: nx.Graph) -> Dict[str, float]:
    """Quantitatively tests the small-world property using criteria from Lecture 2 (Q6).

    Compares empirical clustering C and average path length L against an equivalent
    Erdős–Rényi random graph baseline: C_rand = <k>/N, L_rand ~ ln(N)/ln(<k>).

    Args:
        G: Aggregated static graph.

    Returns:
        Dictionary containing empirical and random benchmark metrics (C, C_rand, L, L_rand, sigma).
    """
    # TODO (PERSON-2): Compute empirical C and L
    # TODO (PERSON-2): Compute theoretical or simulated random graph baselines (C_rand, L_rand)
    # TODO (PERSON-2): Calculate small-world ratio sigma = (C / C_rand) / (L / L_rand)
    pass


def compute_link_weight_pdf(
    df: pd.DataFrame, t_start: int = 1, t_end: int = 3259
) -> Tuple[np.ndarray, np.ndarray]:
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
    # TODO (PERSON-2): Group by pairs (u, v) to count interaction occurrences
    # TODO (PERSON-2): Select appropriate logarithmic or custom binning
    # TODO (PERSON-2): Compute normalized PDF values dividing probability by bin width dx
    pass
