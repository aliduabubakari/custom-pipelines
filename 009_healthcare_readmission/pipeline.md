# Healthcare: Patient Readmission Risk Prediction

## Metadata
| Field | Value |
|---|---|
| **Pipeline ID** | `healthcare_readmission` |
| **Domain** | Healthcare |
| **Total Steps** | 6 |
| **Input Files** | 4 |
| **Pipeline Type** | ML Pipeline (End-to-End) |

---

## Executive Summary

Predicts hospital readmission risk using patient demographics, admission records, lab results, and medication history. Integrates four clinical data sources to build a RandomForest classifier for identifying high-risk patients.

---

## Business Context & Need

Hospital readmissions cost the US healthcare system $26B annually, with $17B from potentially preventable cases. CMS penalties for excess readmissions reach 3% of Medicare reimbursements. An ML readmission prediction model reduces readmissions by 10-20%, saving $500K-$2M per hospital annually while improving patient outcomes.

---

## Data Sources

- **`patients.csv`** — Patient demographics and history (500 records, 12 columns)
- **`admissions.json`** — Admission records (1,289 records, 10 columns)
- **`lab_results.json`** — Laboratory test results (7,660 records, 6 columns)
- **`medications.xlsx`** — Medication orders (5,850 records, 5 columns)

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
**Description:** Load all four clinical data sources. Profile patient demographics, admission statistics, lab result distributions, and medication patterns.
**Script:** `scripts/step_01_load.py`

### Step 2: Data Cleaning & Standardization
**Description:** Handle missing clinical values, cap outlier measurements, and standardize categorical fields (conditions, medications, test names).
**Script:** `scripts/step_02_clean.py`

### Step 3: Feature Engineering
**Description:** Create age groups (<30, 30-50, 50-65, 65-80, 80+) from patient age data for risk stratification.
**Script:** `scripts/step_03_features.py`

### Step 4: Exploratory Data Analysis & Visualization
**Description:** Generate distribution histograms and correlation analysis. Visualize readmission patterns by age, conditions, and length of stay.
**Script:** `scripts/step_04_eda.py`

### Step 5: Model Training
**Description:** Auto-detect readmission target. Train RandomForest classifier with class balancing for imbalanced readmission data. Evaluate with ROC-AUC.
**Script:** `scripts/step_05_model.py`

### Step 6: Final Report
**Description:** Compile final synthesis with readmission risk factors, model performance, and clinical recommendations for reducing readmissions.
**Script:** `scripts/step_06_report.py`

---


## How to Run

### Local Execution
```bash
cd 009_healthcare_readmission
pip install pandas numpy matplotlib seaborn scikit-learn openpyxl

for script in scripts/step_*.py; do
  python "$script" --data_dir data/ --output_dir output/
done
```

### Argo Workflow
```bash
argo submit 009_healthcare_readmission/pipeline.yaml
argo watch @latest
argo logs @latest
```
