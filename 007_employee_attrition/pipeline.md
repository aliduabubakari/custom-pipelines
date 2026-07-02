# HR Analytics: Employee Attrition Prediction & Retention Strategy

## Metadata
| Field | Value |
|---|---|
| **Pipeline ID** | `employee_attrition` |
| **Domain** | Human Resources |
| **Total Steps** | 6 |
| **Input Files** | 3 |
| **Pipeline Type** | ML Pipeline (End-to-End) |

---

## Executive Summary

Predicts employee attrition risk using demographic data, engagement surveys, and performance reviews. Integrates three data sources to build a RandomForest classifier that identifies employees likely to leave.

---

## Business Context & Need

Employee turnover costs organizations 50-200% of annual salary per departure. A predictive attrition model enables proactive retention interventions, reducing turnover by 15-25% and saving millions in recruitment and training costs. For a 1,000-employee company with 15% attrition, a 25% reduction saves $2-5M annually.

---

## Data Sources

- **`employees.csv`** — Employee profiles (500 records, 19 columns)
- **`engagement_surveys.json`** — Survey results (970 records, 7 columns)
- **`performance_reviews.xlsx`** — Annual reviews (2,099 records, 7 columns)

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
**Description:** Load employees CSV, engagement surveys JSON, and performance reviews Excel. Profile each source for row counts, column types, and attrition statistics.
**Script:** `scripts/step_01_load.py`

### Step 2: Data Cleaning & Standardization
**Description:** Handle missing values, cap outliers, and standardize categorical fields across all three data sources.
**Script:** `scripts/step_02_clean.py`

### Step 3: Feature Engineering
**Description:** Create derived features: tenure years, tenure groups (<1yr through 10yr+), and experience-level categories.
**Script:** `scripts/step_03_features.py`

### Step 4: Exploratory Data Analysis & Visualization
**Description:** Generate distribution histograms for key numerical features. Analyze attrition patterns by department, tenure, and performance.
**Script:** `scripts/step_04_eda.py`

### Step 5: Model Training
**Description:** Auto-detect target variable (is_attrited/left_company). Train RandomForest classifier with class balancing. Evaluate with ROC-AUC and accuracy.
**Script:** `scripts/step_05_model.py`

### Step 6: Final Report
**Description:** Compile final synthesis with attrition drivers, model performance metrics, and retention strategy recommendations.
**Script:** `scripts/step_06_report.py`

---


## How to Run

### Local Execution
```bash
cd 007_employee_attrition
pip install pandas numpy matplotlib seaborn scikit-learn openpyxl

for script in scripts/step_*.py; do
  python "$script" --data_dir data/ --output_dir output/
done
```

### Argo Workflow
```bash
argo submit 007_employee_attrition/pipeline.yaml
argo watch @latest
argo logs @latest
```
