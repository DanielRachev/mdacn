"""Centralized plotting configurations and helper functions for the report."""
import math
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

def plot_recognition_rate(recognition_rates: dict[str, Any], eval_fractions: list[float | int], filepath: Path, grid_display: bool = False) -> None:
    """

    Args:
        recognition_rates: dict of labels and recognition rates
        eval_fractions: fractions the values were computed for
        filepath: Full path to save the plot to (.pdf)
        grid_display: Display the plots as a square grid (optional)
    """

    rates_len = len(recognition_rates)
    rates_len_isqrt = math.isqrt(rates_len)
    if rates_len_isqrt ** 2 == rates_len and grid_display:
        fig, ax = plt.subplots(rates_len_isqrt, rates_len_isqrt, figsize=(11.0, 6.0), sharex=True, sharey=True)
        fig.suptitle("Recognition rate per f-value")

        for axis, (label, rates) in zip(ax.flat, recognition_rates.items()):
            axis.plot(eval_fractions, rates, marker="o", label=label)
            axis.set_title(label)
            axis.set_xlabel("Top fraction $f$")
            axis.set_ylabel("Recognition rate $r_{RX}(f)$")
            axis.tick_params(labelbottom=True, labelleft=True)
    else:
        fig, ax = plt.subplots(figsize=(5.5, 3.0))

        for label, rates in recognition_rates.items():
            plt.plot(eval_fractions, rates, marker="o", label=label)
        plt.title("Recognition rate per f-value")
        plt.xlabel("Top fraction $f$")
        plt.ylabel("Recognition rate $r_{RX}(f)$")
        plt.legend()

    save_figure(fig, filepath)

def plot_recognition_rates_gdata_vs_g2(gdata_recognition_rates: dict[str, Any], g2_recognition_rates: dict[str, Any], eval_fractions: list[float | int], filepath: Path) -> None:
    """

    Args:
        gdata_recognition_rates: dict of labels and recognition rates of gdata
        g2_recognition_rates: dict of labels and recognition rates of g2
        eval_fractions: fractions the values were computed for
        filepath: Full path to save the plot to (.pdf)
    """

    shared_keys = gdata_recognition_rates.keys() & g2_recognition_rates.keys()
    rates_len = len(shared_keys)
    rates_len_isqrt = math.isqrt(rates_len)
    if rates_len_isqrt ** 2 == rates_len:
        fig, ax = plt.subplots(rates_len_isqrt, rates_len_isqrt, figsize=(11.0, 6.0), sharex=True, sharey=True)
        fig.suptitle("Recognition rate per f-value")

        for axis, label in zip(ax.flat, shared_keys):
            axis.plot(eval_fractions, gdata_recognition_rates[label], marker="o", label="$G_{data}$")
            axis.plot(eval_fractions, g2_recognition_rates[label], marker="o", label="$G_2$")
            axis.set_title(label)
            axis.set_xlabel("Top fraction $f$")
            axis.set_ylabel("Recognition rate $r_{RX}(f)$")
            axis.tick_params(labelbottom=True, labelleft=True)

        h, l = ax.flat[0].get_legend_handles_labels()
        fig.legend(h, l)
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
