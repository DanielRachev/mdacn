"""Data loading module for temporal contact networks."""

from pathlib import Path
import pandas as pd


def load_temporal_edgelist(filepath: Path) -> pd.DataFrame:
    """Reads a temporal network file formatted as 'a b t' (undirected contact at step t).

    Args:
        filepath: Path to the raw txt file.

    Returns:
        DataFrame with standardized columns ['u', 'v', 't'], sorted by time step t.
    """
    # TODO: Load whitespace/tab separated file into DataFrame
    # Columns: ['u', 'v', 't']
    pass
