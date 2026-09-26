"""Execution pipeline for SI spreading simulations on G_data and G_2 (Antreas & Georgi)."""

import numpy as np
import pandas as pd

from src.config import (
    DATA_PROCESSED_DIR,
    G_2_PATH,
    G_DATA_PATH,
    T_LONG,
    T_SHORT,
    TOTAL_TIME_STEPS,
    FIGURES_DIR,
)
from src.data_loader import load_temporal_edgelist
from src.plotting import (
    plot_comparative_spreading_curves,
    plot_spreading_curve,
    set_report_style,
)
from src.simulation import TemporalSISimulator


def main():
    set_report_style()
    DATA_PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    print("Running SI simulations on G_data (Antreas)...")

    df_data = load_temporal_edgelist(G_DATA_PATH)
    sim_data = TemporalSISimulator(df_data, total_time_steps=TOTAL_TIME_STEPS)
    trajectories_data = sim_data.run_all_seeds()

    np.savez_compressed(
        DATA_PROCESSED_DIR / "trajectories_gdata.npz",
        nodes=sim_data.nodes,
        trajectories=trajectories_data,
    )

    influences_data = pd.DataFrame(
        {
            "seed": sim_data.nodes,
            f"I_{T_SHORT}": trajectories_data[:, T_SHORT],
            f"I_{T_LONG}": trajectories_data[:, T_LONG],
        }
    )

    influences_data.to_csv(DATA_PROCESSED_DIR / "influence_gdata.csv", index=False)

    mean_data, std_data = sim_data.compute_mean_and_std(trajectories_data)

    plot_spreading_curve(mean_data, std_data, FIGURES_DIR / "q8_spreading_gdata.pdf")

    print("Finished G_data simulation (Antreas).")

    print("Running SI simulations on G_2 (Georgi)...")
    df_g2 = load_temporal_edgelist(G_2_PATH)
    sim_g2 = TemporalSISimulator(df_g2, total_time_steps=TOTAL_TIME_STEPS)
    if not np.array_equal(sim_data.nodes, sim_g2.nodes):
        raise ValueError("G_data and G_2 must contain the same nodes in the same seed order")

    trajectories_g2 = sim_g2.run_all_seeds()
    np.savez_compressed(
        DATA_PROCESSED_DIR / "trajectories_g2.npz",
        nodes=sim_g2.nodes,
        trajectories=trajectories_g2,
    )

    influences_g2 = pd.DataFrame(
        {
            "seed": sim_g2.nodes,
            f"I_{T_SHORT}": trajectories_g2[:, T_SHORT],
            f"I_{T_LONG}": trajectories_g2[:, T_LONG],
        }
    )
    influences_g2.to_csv(DATA_PROCESSED_DIR / "influence_g2.csv", index=False)

    mean_g2, std_g2 = sim_g2.compute_mean_and_std(trajectories_g2)
    plot_comparative_spreading_curves(
        mean_data,
        std_data,
        mean_g2,
        std_g2,
        FIGURES_DIR / "q11a_spreading_comparison.pdf",
    )

    print("Finished G_2 simulation and Q11a comparison (Georgi).")


if __name__ == "__main__":
    main()
