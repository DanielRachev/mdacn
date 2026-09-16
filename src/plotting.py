"""Centralized plotting configurations and helper functions for the report."""

from pathlib import Path
import matplotlib.pyplot as plt


def set_report_style():
    """Configures matplotlib with publication-grade font sizing and compact margins."""
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
    """Saves figure in PDF format at 300 DPI."""
    filepath.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(filepath, format="pdf", dpi=300, bbox_inches="tight")
    plt.close(fig)
