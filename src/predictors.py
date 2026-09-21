"""Nodal centrality and influence feature extraction (Q9, Q10, Q11b)."""

import numpy as np
import pandas as pd
from src.static_network import aggregate_temporal_network


def extract_influence_vector(trajectories: np.ndarray, t_target: int) -> np.ndarray:
    """Extracts nodal influence at a specified time horizon t_target (Q9, Q10).

    Influence of node i is the total number of infected nodes at t_target when i is the seed.

    Args:
        trajectories: Matrix of shape (N, T + 1).
        t_target: Target time step (e.g., t^(l)=1200 for Q9, t^(s)=600 for Q10).

    Returns:
        1D array of influence values for all nodes.
    """

    node_count = len(trajectories)
    result = np.zeros(node_count)

    for i in range(node_count):
        if i > len(trajectories) or i < 0:
            raise Exception(f"Wrong i value {i}")
        if t_target > len(trajectories[i]):
            raise Exception(f"Wrong t_target: {t_target} for trajectories")

        result[i] = trajectories[i][t_target]

    return result


def compute_aggregated_degree_predictor(
    contacts_df: pd.DataFrame, t_end: int, node_list: np.ndarray
) -> np.ndarray:
    """Computes degrees of all nodes in network aggregated over [1, t_end] (Q9a, Q9b, Q11b).

    Args:
        contacts_df: Temporal contacts DataFrame.
        t_end: Horizon (600 or 1200).
        node_list: Ordered list of all graph nodes.

    Returns:
        1D array of degrees aligned with node_list.
    """
    # TODO (Jacek): Use aggregate_temporal_network(contacts_df, 1, t_end)
    # TODO (Jacek): Extract degree for each node in node_list (0 for inactive nodes)
    pass


def compute_first_contact_time_predictor(
    contacts_df: pd.DataFrame, node_list: np.ndarray, default_time: int = 3260
) -> np.ndarray:
    """Computes the first-contact time Z_i for each node (Q9c, Q11b).

    Note: Smaller Z_i implies higher rank, so scores should be inverted (-Z_i)
    when passed to ranking functions.

    Args:
        contacts_df: Temporal contacts DataFrame.
        node_list: Ordered list of all nodes.
        default_time: Value assigned if a node never participates in a contact.

    Returns:
        1D array of first interaction times aligned with node_list.
    """
    # TODO (Jacek): Identify minimum time step t where each node appears in ['u', 'v']
    pass
