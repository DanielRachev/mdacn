"""Execution pipeline for influence predictability and recognition curves (Jacek & PERSON-6)."""

import numpy as np
import pandas as pd

from src.config import (
    DATA_PROCESSED_DIR,
    T_LONG,
    T_SHORT,
    FIGURES_DIR
)

from src.plotting import set_report_style
from src.predictors import extract_influence_vector
from src.evaluation import sorted_node_indexed_influence
from src.plotting import plot_influence

def main():
    set_report_style()

    print("Running Influence computation (Jacek)...")

    saved_data = np.load(
        DATA_PROCESSED_DIR / "trajectories_gdata.npz"
    )

    nodes = saved_data.f.nodes
    trajectories = saved_data.f.trajectories

    long_influence_vector = extract_influence_vector(trajectories, T_LONG)
    long_influence_array = sorted_node_indexed_influence(long_influence_vector, nodes)

    short_influence_vector = extract_influence_vector(trajectories, T_SHORT)
    short_influence_array = sorted_node_indexed_influence(long_influence_vector, nodes)

    plot_influence(long_influence_array, FIGURES_DIR / "q9_influence.pdf")

    # TODO (PERSON-4): Compute centralities d^1200, d^600, Z, and R' on G_data
    # TODO (PERSON-4): Run tie-breaker and plot 4 recognition curves on G_data (Q9, Q10)

    # TODO (PERSON-6): Load trajectories_g2.npz
    # TODO (PERSON-6): Compute centralities d^1200, d^600, Z, and R' on G_2
    # TODO (PERSON-6): Run tie-breaker and plot 4 recognition curves on G_2 (Q11b)
    pass


if __name__ == "__main__":
    main()
