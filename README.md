# Run the analysis

Run these commands from the root directory, in this order:

```powershell
uv run python scripts/run_part_a.py
uv run python scripts/run_part_b_sim.py
uv run python scripts/run_part_b_pred.py
```

The simulation step creates the trajectory files required by the prediction step.

## Generated outputs

- `figures/`: all generated PDF plots.
- `data/processed/`: reproducible numerical results, including trajectory archives (`.npz`) and influence tables (`.csv`).

## Tests

```powershell
uv run pytest -q
```
