# Transportation: Prediction, Validation Pipeline

## Metadata
| Field | Value |
|---|---|
| **Pipeline ID** | `transportation_prediction_validation_v2` |
| **Domain** | Transportation |
| **Total Steps** | 6 |
| **Input Files** | 1 |
| **Pipeline Type** | ML Pipeline (End-to-End) |
| **Techniques** | prediction, validation |

---

## Executive Summary

This pipeline performs prediction, validation analysis on transportation data. 
It encompasses the full ML lifecycle: data loading, cleaning, feature engineering, 
exploratory analysis with visualization, model training, and final synthesis.

---

## Business Context & Need

Transportation organizations require rigorous data analysis to derive actionable insights. 
This pipeline demonstrates how prediction, validation techniques can be applied to 
transportation datasets to uncover patterns, make predictions, and support 
data-driven decision-making.

---

## Data Sources

- **`data.csv`** — Synthetically generated transportation dataset (13 columns)

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
               [Step 4: EDA & Visualization]
                  │
                  ▼
               [Step 5: Model Training: prediction, validation]
                  │
                  ▼
               [Step 6: Final Synthesis & Report] ──▶ Final Output
```

---

## Step Details

### Step 1: Data Loading & Profiling
**Description:** Load transportation dataset. Profile row counts, column types, null percentages, and basic statistics.
**Script:** `scripts/step_01_load.py`

### Step 2: Data Cleaning & Standardization
**Description:** Handle missing values, cap outliers, standardize categorical values, and trim whitespace.
**Script:** `scripts/step_02_clean.py`

### Step 3: Feature Engineering
**Description:** Create derived features including categories, ratios, and domain-specific transformations.
**Script:** `scripts/step_03_features.py`

### Step 4: EDA & Visualization
**Description:** Generate multi-panel dashboard: histograms, correlation heatmap, and distribution analysis.
**Script:** `scripts/step_04_eda.py`

### Step 5: Model Training
**Description:** Apply prediction, validation techniques. Train and evaluate machine learning models with cross-validation.
**Script:** `scripts/step_05_model.py`

### Step 6: Final Report
**Description:** Compile final synthesis with key findings, model metrics, and business recommendations.
**Script:** `scripts/step_06_report.py`

---

## Column Reference (13 columns)

- **`trip_id`**
- **`route`**
- **`vehicle_type`**
- **`departure_hour`**
- **`distance_km`**
- **`passengers`**
- **`fare_amount`**
- **`delay_minutes`**
- **`day_of_week`**
- **`is_holiday`**
- **`weather_condition`**
- **`is_delayed`**
- **`cancellation_risk`**


---

## How to Run

```bash
cd 075_transportation_prediction_validation_v2
pip install pandas numpy matplotlib seaborn scikit-learn

for step in scripts/step_*.py; do
  python "$step" --data_dir data/ --output_dir output/
done
```

### Argo Workflow
```bash
argo submit 075_transportation_prediction_validation_v2/pipeline.yaml
```
