"""Centralized plotting configurations and helper functions for the report."""

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

    order = np.argsort(-influence_array[:, 1], kind="stable")
    ranked = influence_array[order]
    influences = ranked[:, 1]
    ranks = np.arange(1, len(ranked) + 1)

    fig, ax = plt.subplots(figsize=(5.5, 3.0))
    ax.plot(ranks, influences, label="Influence at t=1200")

    ax.set_xlabel("Influence rank")
    ax.set_ylabel("Influence")
    ax.set_xlim(1, len(ranked))
    ax.legend()

    save_figure(fig, filepath)

def plot_recognition_rate(recognition_rates: dict[str, Any], eval_fractions: list[float | int], filepath: Path) -> None:
    """

    Args:
        recognition_rates: dict of labels and recognition rates
        eval_fractions: fractions the values were computed for
        filepath: Full path to save the plot to (.pdf)
    """

    fig, ax = plt.subplots(figsize=(5.5, 3.0))

    for label, rates in recognition_rates.items():
        plt.plot(eval_fractions, rates, marker="o", label=label)
    plt.title("Recognition rate per f-value")
    plt.xlabel("Top fraction $f$")
    plt.ylabel("Recognition rate $r_{RX}(f)$")
    plt.legend()

    save_figure(fig, filepath)