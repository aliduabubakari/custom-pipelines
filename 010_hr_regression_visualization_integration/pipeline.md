# HR Analytics: HR Salary Regression & Workforce Visualization

## Metadata
| Field | Value |
|---|---|
| **Pipeline ID** | `hr_regression_visualization_integration` |
| **Domain** | HR Analytics |
| **Total Steps** | 6 |
| **Input Files** | 2 |
| **Pipeline Type** | ML Pipeline (End-to-End) |

---

## Executive Summary

Analyzes employee salary determinants across departments using regression modeling and integrated workforce data. Combines employee records with department-level metrics (headcount, budget) to identify salary drivers, detect pay equity patterns, and visualize workforce composition across the organization.

---

## Business Context & Need

Modern analytics requires robust statistical integration of heterogeneous data sources. This pipeline serves as a benchmark for evaluating statistical methods across different data distributions, group assignments, and outcome variables. It provides a reproducible framework for experimental design analysis.

---

## Data Sources

- **`employees.csv`** — Input data file
- **`departments.csv`** — Input data file


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
               [Step 5: Statistical Analysis & Model Tr]
                  │
                  ▼
               [Step 6: Model Evaluation & Final Report] ──▶ Final Output
```

---

## Step Details

### Step 1: Data Loading & Profiling

**Description:** Load and profile all data sources. Check row counts, column types, null percentages, basic statistics. Identify target variable and key features.

**Script:** `scripts/step_01_load.py`

---

### Step 2: Data Cleaning & Standardization

**Description:** Handle missing values (median for numerical, 'Unknown' for categorical). Cap outliers at 99th percentile. Standardize categorical values. Trim whitespace.

**Script:** `scripts/step_02_clean.py`

---

### Step 3: Feature Engineering

**Description:** Create domain-specific derived features: categories, ratios, temporal features, and interaction terms relevant to hr analytics analytics.

**Script:** `scripts/step_03_features.py`

---

### Step 4: Exploratory Data Analysis & Visualization

**Description:** Generate multi-panel EDA dashboard. Analyze distributions, correlations, and segment patterns. Identify key relationships and anomalies.

**Script:** `scripts/step_04_eda.py`

---

### Step 5: Statistical Analysis & Model Training

**Description:** Perform hypothesis tests and train machine learning models. Compare multiple algorithms and select best performer based on relevant metrics.

**Script:** `scripts/step_05_model.py`

---

### Step 6: Model Evaluation & Final Report

**Description:** Evaluate model on test data. Generate final report with key findings, business recommendations, and monitoring guidelines.

**Script:** `scripts/step_06_report.py`

---


## How to Run

### Local Execution
```bash
cd 010_hr_regression_visualization_integration
pip install pandas numpy matplotlib seaborn scikit-learn

# Run steps sequentially
python scripts/step_01_load.py --data_dir data/ --output_dir output/
python scripts/step_02_clean.py --data_dir data/ --output_dir output/
python scripts/step_03_features.py --data_dir data/ --output_dir output/
python scripts/step_04_eda.py --data_dir data/ --output_dir output/
python scripts/step_05_model.py --data_dir data/ --output_dir output/
python scripts/step_06_report.py --data_dir data/ --output_dir output/
```

### Argo Workflow
```bash
argo submit 010_hr_regression_visualization_integration/pipeline.yaml
argo watch @latest
argo logs @latest
```
