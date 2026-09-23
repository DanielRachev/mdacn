"""Centralized plotting configurations and helper functions for the report."""

from pathlib import Path

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


def plot_comparative_spreading_curves(
    mean_data: np.ndarray,
    std_data: np.ndarray,
    mean_g2: np.ndarray,
    std_g2: np.ndarray,
    filepath: Path,
) -> None:
    """Plot mean SI spreading and ±1 standard deviation for G_data and G_2."""
    curves = (mean_data, std_data, mean_g2, std_g2)
    if any(curve.ndim != 1 for curve in curves):
        raise ValueError("Spreading means and standard deviations must be 1D arrays")
    if len({curve.shape for curve in curves}) != 1:
        raise ValueError("Both networks must have matching spreading time horizons")

    time = np.arange(len(mean_data))
    lower_data = np.maximum(mean_data - std_data, 0)
    upper_data = mean_data + std_data
    lower_g2 = np.maximum(mean_g2 - std_g2, 0)
    upper_g2 = mean_g2 + std_g2

    fig, ax = plt.subplots(figsize=(5.5, 3.0))
    (data_line,) = ax.plot(time, mean_data, label="$G_{data}$ mean")
    ax.fill_between(
        time,
        lower_data,
        upper_data,
        color=data_line.get_color(),
        alpha=0.2,
        label="$G_{data}$ ±1 SD",
    )
    (g2_line,) = ax.plot(time, mean_g2, label="$G_2$ mean")
    ax.fill_between(
        time,
        lower_g2,
        upper_g2,
        color=g2_line.get_color(),
        alpha=0.2,
        label="$G_2$ ±1 SD",
    )

    ax.set_xlabel("Time step")
    ax.set_ylabel("Number of infected nodes")
    ax.legend()

    save_figure(fig, filepath)
