# Energy: Consumption Forecasting & Grid Optimization

## Metadata
| Field | Value |
|---|---|
| **Pipeline ID** | `energy_forecasting` |
| **Domain** | Energy / Utilities |
| **Total Steps** | 6 |
| **Input Files** | 2 |
| **Pipeline Type** | ML Pipeline (End-to-End) |

---

## Executive Summary

Forecasts energy consumption using historical usage patterns and weather covariates. Trains RandomForest regression model to predict consumption from temperature, humidity, and temporal features.

---

## Business Context & Need

Energy demand forecasting errors cost utilities $1-5M annually per GW of capacity. Over-forecasting leads to excess generation; under-forecasting causes blackouts or expensive spot-market purchases. ML forecasting reduces MAPE from 8-12% to 2-4%, saving $2-10M/year for a mid-size utility.

---

## Data Sources

- **`energy_consumption.csv`** — Hourly consumption data (8,760 records, 7 columns)
- **`weather.csv`** — Daily weather observations (365 records, 8 columns)

---

## Pipeline Architecture

```
  Input Data ──▶ [Step 1: Data Loading & Profiling]
                  │
                  ▼
               [Step 2: Data Cleaning & Standardizatio]
                  │
                  ▼
               [Step 3: Feature Engineering]
                  │
                  ▼
               [Step 4: Exploratory Data Analysis & Vis]
                  │
                  ▼
               [Step 5: Model Training: Regression]
                  │
                  ▼
               [Step 6: Final Synthesis & Report] ──▶ Final Output
```

---

## Step Details

### Step 1: Data Loading & Profiling
**Description:** Load energy consumption CSV and weather CSV. Profile row counts, date ranges, consumption statistics, and weather patterns.
**Script:** `scripts/step_01_load.py`

### Step 2: Data Cleaning & Standardization
**Description:** Handle missing values, cap outliers, and standardize numerical features for modeling.
**Script:** `scripts/step_02_clean.py`

### Step 3: Feature Engineering
**Description:** Extract temporal features: month, quarter, day of week, weekend flag. Create weather-consumption interaction features.
**Script:** `scripts/step_03_features.py`

### Step 4: Exploratory Data Analysis & Visualization
**Description:** Generate distribution histograms and correlation heatmap. Analyze consumption patterns by time and weather conditions.
**Script:** `scripts/step_04_eda.py`

### Step 5: Model Training
**Description:** Train RandomForest regressor to predict energy consumption. Evaluate with MAE and R² metrics. Compare against baseline.
**Script:** `scripts/step_05_model.py`

### Step 6: Final Report
**Description:** Compile final synthesis with model performance, consumption patterns, and recommendations for grid optimization.
**Script:** `scripts/step_06_report.py`

---


## How to Run

### Local Execution
```bash
cd 008_energy_forecasting
pip install pandas numpy matplotlib seaborn scikit-learn

for script in scripts/step_*.py; do
  python "$script" --data_dir data/ --output_dir output/
done
```

### Argo Workflow
```bash
argo submit 008_energy_forecasting/pipeline.yaml
argo watch @latest
argo logs @latest
```
