"""Data loading module for the Excel temporal contact networks."""

from pathlib import Path

import pandas as pd


def load_temporal_edgelist(filepath: Path) -> pd.DataFrame:
    """Read an Excel contact file and return columns ``u``, ``v``, and ``t``.

    Args:
        filepath: Path to the raw Excel file. Input file use fixed headers: ``node1``, ``node2``, and ``timestamp``.

    Returns:
        DataFrame with standardized columns ['u', 'v', 't'], sorted by time step t.
    """
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(path)

    data = pd.read_excel(path)
    required_columns = {"node1", "node2", "timestamp"}
    missing_columns = required_columns.difference(data.columns)
    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Excel file is missing required columns: {missing}")

    data = data.rename(columns={"node1": "u", "node2": "v", "timestamp": "t"})
    if data[["u", "v", "t"]].isna().any().any():
        raise ValueError("Excel file contains missing contact values")

    data["t"] = pd.to_numeric(data["t"], errors="raise").astype(int)
    return data[["u", "v", "t"]].sort_values("t", kind="stable").reset_index(drop=True)
