# Education: Analysis Pipeline

## Metadata
| Field | Value |
|---|---|
| **Pipeline ID** | `student_performance` |
| **Domain** | Education |
| **Total Steps** | 6 |
| **Input Files** | 1 |
| **Pipeline Type** | ML Pipeline (End-to-End) |
| **Techniques** | Analysis |

---

## Executive Summary

This pipeline performs analysis analysis on education data. 
It encompasses the full ML lifecycle: data loading, cleaning, feature engineering, 
exploratory analysis with visualization, model training, and final synthesis.

---

## Business Context & Need

Education organizations require rigorous data analysis to derive actionable insights. 
This pipeline demonstrates how analysis techniques can be applied to 
education datasets to uncover patterns, make predictions, and support 
data-driven decision-making.

---

## Data Sources

- **`data.csv`** — Synthetically generated education dataset (10 columns)

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
               [Step 5: Model Training: Analysis]
                  │
                  ▼
               [Step 6: Final Synthesis & Report] ──▶ Final Output
```

---

## Step Details

### Step 1: Data Loading & Profiling
**Description:** Load education dataset. Profile row counts, column types, null percentages, and basic statistics.
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
**Description:** Apply analysis techniques. Train and evaluate machine learning models with cross-validation.
**Script:** `scripts/step_05_model.py`

### Step 6: Final Report
**Description:** Compile final synthesis with key findings, model metrics, and business recommendations.
**Script:** `scripts/step_06_report.py`

---

## Column Reference (10 columns)

- **`student_id`**
- **`major`**
- **`year`**
- **`age`**
- **`study_hours_per_week`**
- **`attendance_pct`**
- **`previous_gpa`**
- **`current_gpa`**
- **`assignments_completed`**
- **`extracurricular_hours`**


---

## How to Run

```bash
cd 054_student_performance
pip install pandas numpy matplotlib seaborn scikit-learn

for step in scripts/step_*.py; do
  python "$step" --data_dir data/ --output_dir output/
done
```

### Argo Workflow
```bash
argo submit 054_student_performance/pipeline.yaml
```
