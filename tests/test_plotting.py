import numpy as np

from src.plotting import plot_recognition_rate


def test_recognition_plot_prints_curve_distances_and_slopes(tmp_path, capsys):
    filepath = tmp_path / "recognition.pdf"
    plot_recognition_rate(
        {
            "A": np.array([0.1, 0.3, 0.7]),
            "B": np.array([0.2, 0.4, 0.5]),
        },
        [0.1, 0.2, 0.4],
        filepath,
    )

    output = capsys.readouterr().out
    assert "Mean absolute gap A vs B: 0.1333" in output
    assert "Mean gap across all pairs: 0.1333" in output
    assert "Mean derivative of A with respect to f: 2.0000" in output
    assert "Mean derivative of B with respect to f: 1.2500" in output
    assert filepath.is_file()
