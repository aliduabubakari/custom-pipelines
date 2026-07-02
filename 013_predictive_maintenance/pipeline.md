# Manufacturing: Predictive Maintenance & Failure Detection

## Metadata
| Field | Value |
|---|---|
| **Pipeline ID** | `predictive_maintenance` |
| **Domain** | Manufacturing / Industry 4.0 |
| **Total Steps** | 6 |
| **Input Files** | 1 |
| **Pipeline Type** | ML Pipeline (End-to-End) |

---

## Executive Summary

Predicts equipment failure from IoT sensor readings including temperature, vibration, pressure, and runtime metrics. Trains a RandomForest classifier to identify machines requiring preventive maintenance before failure occurs.

---

## Business Context & Need

Unplanned equipment downtime costs manufacturers $50B annually. Reactive maintenance is 3-9× more expensive than planned maintenance. ML-based predictive maintenance reduces downtime by 30-50%, extends equipment life by 20-40%, and saves $500K-$2M per production line annually.

---

## Data Sources

- **`sensor_readings.csv`** — IoT sensor data (21,600 records, 13 columns)

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
               [Step 5: Model Training: Classification]
                  │
                  ▼
               [Step 6: Final Synthesis & Report] ──▶ Final Output
```

---

## Step Details

### Step 1: Data Loading & Profiling
**Description:** Load sensor readings CSV. Profile machine counts, sensor value ranges, failure rates, and temporal patterns.
**Script:** `scripts/step_01_load.py`

### Step 2: Data Cleaning & Standardization
**Description:** Handle missing sensor readings, cap outliers, and standardize measurement scales across sensor types.
**Script:** `scripts/step_02_clean.py`

### Step 3: Feature Engineering
**Description:** Create derived features: temperature-to-vibration ratio and runtime days from runtime hours for operational context.
**Script:** `scripts/step_03_features.py`

### Step 4: Exploratory Data Analysis & Visualization
**Description:** Generate distribution histograms and correlation heatmap. Analyze failure patterns by sensor readings and operating conditions.
**Script:** `scripts/step_04_eda.py`

### Step 5: Model Training
**Description:** Auto-detect failure target variable. Train RandomForest classifier with class balancing for rare failure events. Evaluate with ROC-AUC and accuracy.
**Script:** `scripts/step_05_model.py`

### Step 6: Final Report
**Description:** Compile final synthesis with failure predictors, model performance, and maintenance scheduling recommendations.
**Script:** `scripts/step_06_report.py`

---


## How to Run

### Local Execution
```bash
cd 013_predictive_maintenance
pip install pandas numpy matplotlib seaborn scikit-learn

for script in scripts/step_*.py; do
  python "$script" --data_dir data/ --output_dir output/
done
```

### Argo Workflow
```bash
argo submit 013_predictive_maintenance/pipeline.yaml
argo watch @latest
argo logs @latest
```
