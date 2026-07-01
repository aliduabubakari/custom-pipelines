# Sports: Cleaning, Recovery, Visualization Pipeline

## Metadata
| Field | Value |
|---|---|
| **Pipeline ID** | `sports_visualization_cleaning_recovery_v2` |
| **Domain** | Sports |
| **Total Steps** | 6 |
| **Input Files** | 1 |
| **Pipeline Type** | ML Pipeline (End-to-End) |
| **Techniques** | cleaning, recovery, visualization |

---

## Executive Summary

This pipeline performs cleaning, recovery, visualization analysis on sports data. 
It encompasses the full ML lifecycle: data loading, cleaning, feature engineering, 
exploratory analysis with visualization, model training, and final synthesis.

---

## Business Context & Need

Sports organizations require rigorous data analysis to derive actionable insights. 
This pipeline demonstrates how cleaning, recovery, visualization techniques can be applied to 
sports datasets to uncover patterns, make predictions, and support 
data-driven decision-making.

---

## Data Sources

- **`data.csv`** — Synthetically generated sports dataset (11 columns)

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
               [Step 5: Model Training: cleaning, recovery, visualization]
                  │
                  ▼
               [Step 6: Final Synthesis & Report] ──▶ Final Output
```

---

## Step Details

### Step 1: Data Loading & Profiling
**Description:** Load sports dataset. Profile row counts, column types, null percentages, and basic statistics.
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
**Description:** Apply cleaning, recovery, visualization techniques. Train and evaluate machine learning models with cross-validation.
**Script:** `scripts/step_05_model.py`

### Step 6: Final Report
**Description:** Compile final synthesis with key findings, model metrics, and business recommendations.
**Script:** `scripts/step_06_report.py`

---

## Column Reference (11 columns)

- **`player_id`**
- **`team`**
- **`position`**
- **`games_played`**
- **`points_per_game`**
- **`assists_per_game`**
- **`rebounds_per_game`**
- **`minutes_per_game`**
- **`age`**
- **`experience_years`**
- **`salary_millions`**


---

## How to Run

```bash
cd 046_sports_visualization_cleaning_recovery_v2
pip install pandas numpy matplotlib seaborn scikit-learn

for step in scripts/step_*.py; do
  python "$step" --data_dir data/ --output_dir output/
done
```

### Argo Workflow
```bash
argo submit 046_sports_visualization_cleaning_recovery_v2/pipeline.yaml
```
