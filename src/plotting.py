"""Centralized plotting configurations and helper functions for the report."""

from itertools import combinations
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


def set_report_style():
    """Configure matplotlib with compact publication-style settings."""
    plt.rcParams.update(
        {
            "font.size": 8,
            "axes.labelsize": 8,
            "legend.fontsize": 7,
            "xtick.labelsize": 7,
            "ytick.labelsize": 7,
            "figure.autolayout": True,
            "lines.linewidth": 1.2,
        }
    )


def save_figure(fig: plt.Figure, filepath: Path):
    """Save a figure as a compact PDF."""
    filepath.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(filepath, format="pdf", dpi=300, bbox_inches="tight")
    plt.close(fig)


def plot_spreading_curve(mean_I: np.ndarray, std_I: np.ndarray, filepath: Path):
    """Plot E[I(t)] together with ±1 standard deviation for Q8."""

    time = np.arange(len(mean_I))

    lower = np.maximum(mean_I - std_I, 0)
    upper = mean_I + std_I

    fig, ax = plt.subplots(figsize=(5.5, 3.0))
    ax.plot(time, mean_I, label="Mean infected")
    ax.fill_between(time, lower, upper, alpha=0.25, label="±1 standard deviation")

    ax.set_xlabel("Time step")
    ax.set_ylabel("Number of infected nodes")
    ax.legend()

    save_figure(fig, filepath)

def plot_influence(influence_array: np.ndarray, filepath: Path) -> None:
    """
    Plot the sorted influence at T_LONG vs node_id
    Args:
        filepath: Full path to save the plot to (.pdf)
        influence_array: 2D array (N, 2)
    """

    influences = influence_array[:, 1]
    fig, ax = plt.subplots(figsize=(5.5, 3.0))
    ax.plot(influences, label="Influence at t=1200")

    ax.set_xlabel("Influence rank")
    ax.set_ylabel("Influence")
    ax.set_xlim(1, len(influences))
    ax.legend()

    save_figure(fig, filepath)

def plot_recognition_rate(recognition_rates: dict[str, Any], eval_fractions: list[float | int], filepath: Path) -> None:
    """

    Args:
        recognition_rates: dict of labels and recognition rates
        eval_fractions: fractions the values were computed for
        filepath: Full path to save the plot to (.pdf)

    Prints mean absolute vertical gaps at sampled fractions and mean slopes
    between adjacent fractions.
    """

    fig, ax = plt.subplots(figsize=(5.5, 3.0))

    for label, rates in recognition_rates.items():
        ax.plot(eval_fractions, rates, marker="o", label=label)
    ax.set_title("Recognition rate per f-value")
    ax.set_xlabel("Top fraction $f$")
    ax.set_ylabel("Recognition rate $r_{RX}(f)$")
    ax.legend()

    save_figure(fig, filepath)

    print("Recognition rate curve summary:")
    pairwise_distances = []
    for (first_label, first_rates), (second_label, second_rates) in combinations(
        recognition_rates.items(), 2
    ):
        distance = float(
            np.mean(np.abs(np.asarray(first_rates) - np.asarray(second_rates)))
        )
        pairwise_distances.append(distance)
        print(f"  Mean absolute gap {first_label} vs {second_label}: {distance:.4f}")
    if pairwise_distances:
        print(f"  Mean gap across all pairs: {np.mean(pairwise_distances):.4f}")

    fraction_steps = np.diff(eval_fractions)
    for label, rates in recognition_rates.items():
        average_derivative = np.mean(np.diff(rates) / fraction_steps)
        print(f"  Mean derivative of {label} with respect to f: {average_derivative:.4f}")
