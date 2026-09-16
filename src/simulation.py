"""Discrete temporal Susceptible-Infected (SI) simulation engine (Q8, Q11a)."""

from typing import Tuple
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
        """Pre-processes contacts by time step for high-throughput temporal lookups.

        Args:
            contacts_df: Temporal contacts DataFrame with columns ['u', 'v', 't'].
            total_time_steps: Total duration T.
        """
        # TODO (PERSON-3): Store total_time_steps and extract sorted unique node list
        # TODO (PERSON-3): Group contacts by time step t into an indexed lookup table/dict
        pass

    def run_single_seed(self, seed_node: int) -> np.ndarray:
        """Runs the SI spreading process for a single seed node over [0, T].

        Args:
            seed_node: ID of the node infected at t = 0.

        Returns:
            1D array of shape (T + 1,) containing total infected count I(t) at each step t.
        """
        # TODO (PERSON-3): Initialize infected status boolean array
        # TODO (PERSON-3): Step through t = 1 to T:
        #                   - Retrieve contacts at step t
        #                   - Transmit infection only from nodes infected at or before t - 1
        #                   - Record cumulative infected count I(t)
        pass

    def run_all_seeds(self) -> np.ndarray:
        """Simulates the spreading process starting from every unique node i in [1, N].

        Returns:
            2D array of shape (N, T + 1) storing infection trajectories I_i(t) for every seed.
        """
        # TODO (PERSON-3): Loop over all N nodes as seeds
        # TODO (PERSON-3): Populate trajectory matrix
        pass

    @staticmethod
    def compute_mean_and_std(
        trajectories: np.ndarray,
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Calculates E[I(t)] and sqrt(Var[I(t)]) across all seed trajectories (Q8, Q11a).

        Args:
            trajectories: 2D array of shape (N, T + 1).

        Returns:
            Tuple of (mean_I_t, std_I_t).
        """
        # TODO (PERSON-3): Return mean and standard deviation of of trajectories
        pass
    