from pathlib import Path

import pandas as pd

from src.data_loader import load_temporal_edgelist


def test_load_temporal_edgelist_renames_and_sorts_excel_columns(monkeypatch):
    input_path = Path(__file__).resolve().parents[1] / "data" / "raw" / "G_data.xlsx"
    source = pd.DataFrame(
        {
            "node1": [2, 1],
            "node2": [3, 2],
            "timestamp": [2, 1],
        }
    )
    monkeypatch.setattr(pd, "read_excel", lambda path: source)

    result = load_temporal_edgelist(input_path)

    expected = pd.DataFrame(
        {
            "u": [1, 2],
            "v": [2, 3],
            "t": [1, 2],
        }
    )
    pd.testing.assert_frame_equal(result, expected)
