# Insurance: Claims Fraud Detection & Risk Assessment

## Metadata
| Field | Value |
|---|---|
| **Pipeline ID** | `insurance_claims` |
| **Domain** | Insurance |
| **Total Steps** | 6 |
| **Input Files** | 1 |
| **Pipeline Type** | ML Pipeline (End-to-End) |

---

## Executive Summary

Detects fraudulent insurance claims using policyholder characteristics and claim patterns. Trains a RandomForest classifier to identify suspicious claims from claim amount, incident details, and customer history features.

---

## Business Context & Need

Insurance fraud costs the industry $80B+ annually in the US alone. Manual fraud investigation is slow and expensive, catching only 20% of fraudulent claims. ML-based fraud detection improves catch rates to 40-60% while reducing investigation costs by 70%. A 10% improvement in fraud detection saves $5-10M annually for a mid-size insurer.

---

## Data Sources

- **`claims.csv`** — Insurance claims data (1,000 records, 18 columns)

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
**Description:** Load claims CSV. Profile claim volumes, amount distributions, fraud rates, and feature statistics.
**Script:** `scripts/step_01_load.py`

### Step 2: Data Cleaning & Standardization
**Description:** Handle missing values, cap outliers at 99th percentile, and standardize categorical fields.
**Script:** `scripts/step_02_clean.py`

### Step 3: Feature Engineering
**Description:** Create claim size categories (Small/Medium/Large/Catastrophic) and age groups (Young/Middle/Senior/Elderly) for risk stratification.
**Script:** `scripts/step_03_features.py`

### Step 4: Exploratory Data Analysis & Visualization
**Description:** Generate distribution histograms and correlation heatmap. Analyze fraud patterns by claim type, amount, and demographics.
**Script:** `scripts/step_04_eda.py`

### Step 5: Model Training
**Description:** Auto-detect fraud target variable. Train RandomForest classifier with class balancing for imbalanced fraud data. Evaluate with ROC-AUC and accuracy.
**Script:** `scripts/step_05_model.py`

### Step 6: Final Report
**Description:** Compile final synthesis with fraud indicators, model performance, and recommendations for claims investigation prioritization.
**Script:** `scripts/step_06_report.py`

---


## How to Run

### Local Execution
```bash
cd 012_insurance_claims
pip install pandas numpy matplotlib seaborn scikit-learn

for script in scripts/step_*.py; do
  python "$script" --data_dir data/ --output_dir output/
done
```

### Argo Workflow
```bash
argo submit 012_insurance_claims/pipeline.yaml
argo watch @latest
argo logs @latest
```
