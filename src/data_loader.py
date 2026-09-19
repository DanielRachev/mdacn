"""Data loading module for temporal contact networks."""

from pathlib import Path

import pandas as pd


def load_temporal_edgelist(filepath: Path) -> pd.DataFrame:
    """Load a temporal network with columns (u, v, t)."""

    if filepath.suffix.lower() in {".xlsx", ".xls"}:
        df = pd.read_excel(filepath)
        df = df.iloc[:, :3]
        df.columns = ["u", "v", "t"]
    else:
        df = pd.read_csv(filepath, sep=r"\s+", header=None, names=["u", "v", "t"])

    df = df[["u", "v", "t"]].dropna()
    df = df.astype({"u": int, "v": int, "t": int})
    df = df.sort_values("t").reset_index(drop=True)

    return df