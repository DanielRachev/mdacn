"""Execution pipeline for SI spreading simulations on G_data and G_2 (Antreas & Georgi)."""

from src.config import G_2_PATH, G_DATA_PATH
from src.data_loader import load_temporal_edgelist
from src.simulation import TemporalSISimulator


def main():
    print("Running SI simulations on G_data (Antreas)...")
    df_data = load_temporal_edgelist(G_DATA_PATH)
    sim_data = TemporalSISimulator(df_data)
    trajectories_data = sim_data.run_all_seeds()
    # TODO (Antreas): Save trajectories_data to data/processed/trajectories_gdata.npz
    # TODO (Antreas): Plot E[I(t)] +/- std (Q8)

    print("Running SI simulations on G_2 (Georgi)...")
    df_g2 = load_temporal_edgelist(G_2_PATH)
    sim_g2 = TemporalSISimulator(df_g2)
    trajectories_g2 = sim_g2.run_all_seeds()
    # TODO (Georgi): Save trajectories_g2 to data/processed/trajectories_g2.npz
    # TODO (Georgi): Plot comparative spreading curves G_data vs G_2 (Q11a)


if __name__ == "__main__":
    main()
