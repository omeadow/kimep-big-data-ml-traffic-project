# Traffic Forecasting Project

## Environment and Dependency Management (`uv`)

This project uses [`uv`](https://docs.astral.sh/uv/) for Python dependency management.

### Setup

1. Install `uv` (if not already installed).
2. Sync dependencies from `pyproject.toml` and `uv.lock`:

```bash
uv sync
```

### Run the project

Run the main script:

```bash
uv run python main.py
```

Start Jupyter for notebook work:

```bash
uv run jupyter notebook
```

## Project Goal

This project predicts the **number of vehicles one hour ahead** for a traffic junction.

The dataset contains hourly traffic observations for 4 junctions and about 48,000 rows.

This is a **time series regression** project, not a classification project.

Target:

- predict `Vehicles` at time `t+1 hour`

Example:

- if a row is for `10:00`, the model should predict traffic for `11:00`

---

## Dataset Schema

Expected columns:

- `DateTime` — timestamp of the observation
- `Junction` — junction identifier
- `Vehicles` — number of vehicles observed at that hour
- `ID` — row identifier if present

Important:
- data must be sorted by `Junction` and `DateTime`
- all forecasting logic must respect time order
- no future leakage is allowed

---

## Problem Framing

For each junction, use historical traffic and time-based patterns to estimate the vehicle count one hour later.

This is essentially:

- input: current and past traffic information
- output: next hour vehicle count

The project should focus on **practical tabular/time-series ML**, not deep learning.

Do **not** use:
- LSTM
- RNN
- Transformers
unless explicitly requested later

Preferred first approach:
- lag-based feature engineering
- tree-based regression model such as XGBoost
- simple baselines first

---

## Modeling Strategy

Start simple and build in stages.

### Stage 1 — Data audit
Verify:
- datetime parsing is correct
- no broken timestamps
- duplicates
- missing values
- hourly continuity per junction

### Stage 2 — Baseline
Build a naive baseline:

- predict next hour vehicles = current hour vehicles

This baseline is important. Any ML model should beat it.

### Stage 3 — Feature engineering
Create features using **past data only**.

Required feature types:

#### Time features
- hour
- day of week
- is weekend
- month if useful

#### Lag features
Per junction:
- `lag_1`
- `lag_2`
- `lag_3`
- `lag_6`
- `lag_12`
- `lag_24`
- `lag_48`
- `lag_168` if enough history exists

#### Rolling features
Per junction, using only past values:
- rolling mean over 3 hours
- rolling mean over 6 hours
- rolling mean over 24 hours
- rolling std over 24 hours

### Stage 4 — Model
Preferred first model:
- `XGBoost Regressor`

Fallback if XGBoost is unavailable:
- `RandomForestRegressor`
- `GradientBoostingRegressor`
- `LinearRegression` as a simple benchmark

### Stage 5 — Evaluation
Use chronological split only.

Do **not** use random train/test split.

Preferred evaluation metrics:
- MAE
- RMSE

Report:
- overall performance
- per-junction performance

---

## Target Construction

The target should be created per junction:

- `target = Vehicles shifted by -1 within each Junction group`

Meaning:
- current row contains information available at time `t`
- target is `Vehicles` at time `t+1`

Any rows with missing target after shifting should be dropped.

---

## Data Leakage Rules

This project must avoid leakage.

Rules:
- never use future rows to build current-row features
- all lag features must come from past values only
- rolling features must be shifted so they do not include the current target hour
- validation/test data must come after training data in time

If a feature might contain future information, do not use it.

---

## Project Priorities

Priority order:

1. correctness
2. no leakage
3. clear code
4. solid baseline
5. practical model
6. readable outputs

Do not overengineer.

Keep the first version small and working.

---

## Suggested Repository Structure

```text
data/
notebooks/
src/
models/
outputs/
README.md
