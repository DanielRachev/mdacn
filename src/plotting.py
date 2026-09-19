"""Centralized plotting configurations and helper functions for the report."""

from pathlib import Path

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