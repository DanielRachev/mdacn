"""Global project constants and configuration parameters."""

from pathlib import Path

# Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_RAW_DIR = PROJECT_ROOT / "data" / "raw"
DATA_PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

G_DATA_PATH = DATA_RAW_DIR / "G_data.xlsx"
G_2_PATH = DATA_RAW_DIR / "G_2.xlsx"

FIGURES_DIR = PROJECT_ROOT / "figures"

# Temporal Spreading Horizons
TOTAL_TIME_STEPS = 3259  # T
T_SHORT = 600  # t^(s)
T_LONG = 1200  # t^(l)

# Evaluation Settings
TIE_BREAK_ITERATIONS = 1000
EVAL_FRACTIONS = [round(f * 0.05, 2) for f in range(1, 11)]  # [0.05, ..., 0.50]
RANDOM_SEED = 42
