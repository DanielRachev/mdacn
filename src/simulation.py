"""Discrete temporal Susceptible-Infected (SI) simulation engine (Q8, Q11a)."""


import numpy as np
import pandas as pd


class TemporalSISimulator:
    """Simulates discrete temporal SI spreading on a contact network.

    Transmission rules:
        - At t = 0, exactly one seed node s is infected.
        - If an infected node i contacts a susceptible node j at step t, j becomes infected at t.
        - Node j can only transmit infection to others starting at step t + 1.
        - Infected nodes remain infected forever.
    """

    def __init__(self, contacts_df: pd.DataFrame, total_time_steps: int = 3259):
        """Pre-process contacts by time step for temporal lookups.

        Args:
            contacts_df: Temporal contacts DataFrame with columns ['u', 'v', 't'].
            total_time_steps: Total duration T.
        """
        self.total_time_steps = total_time_steps

        self.nodes = np.sort(
            np.unique(
                np.concatenate(
                    [
                        contacts_df["u"].to_numpy(),
                        contacts_df["v"].to_numpy(),
                    ]
                )
            )
        )

        self.contacts_by_time = {
            int(t): group[["u", "v"]].to_numpy(dtype=int)
            for t, group in contacts_df.groupby("t")
        }

    def run_single_seed(self, seed_node: int) -> np.ndarray:
        """Run the SI spreading process for a single seed node over [0, T].

        Args:
            seed_node: ID of the node infected at t = 0.

        Returns:
            1D array of shape (T + 1,) containing total infected count I(t) at each step t.
        """
        if seed_node not in self.nodes:
            raise ValueError(f"Unknown seed node: {seed_node}")

        infected = {int(seed_node)}

        trajectory = np.empty(self.total_time_steps + 1, dtype=int)
        trajectory[0] = 1

        for t in range(1, self.total_time_steps + 1):
            contacts = self.contacts_by_time.get(t)

            if contacts is not None:
                infected_before_t = infected.copy()
                newly_infected = set()

                for u, v in contacts:
                    if u in infected_before_t and v not in infected_before_t:
                        newly_infected.add(int(v))
                    elif v in infected_before_t and u not in infected_before_t:
                        newly_infected.add(int(u))

                infected.update(newly_infected)

            trajectory[t] = len(infected)

        return trajectory

    def run_all_seeds(self) -> np.ndarray:
        """Simulate spreading starting from every unique node as the seed.

        Returns:
            2D array of shape (N, T + 1) storing infection trajectories I_i(t).
        """
        trajectories = np.empty(
            (len(self.nodes), self.total_time_steps + 1),
            dtype=int,
        )

        for i, seed_node in enumerate(self.nodes):
            trajectories[i] = self.run_single_seed(int(seed_node))

        return trajectories

    @staticmethod
    def compute_mean_and_std(
            trajectories: np.ndarray,
    ) -> tuple[np.ndarray, np.ndarray]:
        """Calculate E[I(t)] and sqrt(Var[I(t)]) across all seed trajectories.

        Args:
            trajectories: 2D array of shape (N, T + 1).

        Returns:
            Tuple of (mean_I_t, std_I_t).
        """
        mean_I_t = np.mean(trajectories, axis=0)
        std_I_t = np.std(trajectories, axis=0)

        return mean_I_t, std_I_t