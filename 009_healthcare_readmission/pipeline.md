# Healthcare: Patient Readmission Risk Prediction

## Metadata
| Field | Value |
|---|---|
| **Pipeline ID** | `healthcare_readmission` |
| **Domain** | Healthcare |
| **Total Steps** | 15 |
| **Input Files** | 4 |
| **Pipeline Type** | ML Pipeline (End-to-End) |

---

## Executive Summary

Predicts 30-day hospital readmission risk for discharged patients 
by integrating electronic health records, lab results, admission history, and patient 
demographics. Enables care management teams to prioritize high-risk patients for 
post-discharge follow-up interventions.

---

## Business Context & Need

Hospitals face Medicare penalties for excess readmissions under 
the Hospital Readmissions Reduction Program (HRRP). Each preventable readmission costs 
$15,000-$25,000. A predictive model identifying at-risk patients enables targeted 
transitional care programs, reducing readmission rates by 15-20% and saving $2-5M annually 
for a mid-size hospital system.

---

## Data Sources

- **`patients.csv`** — Input data file
- **`admissions.json`** — Input data file
- **`lab_results.json`** — Input data file
- **`medications.xlsx`** — Input data file

---

## Pipeline Architecture

```
  Input Data ──▶ [Step 1: Data Loading & Profiling]
                  │
                  ▼
               [Step 2: Data Merging & Integration]
                  │
                  ▼
               [Step 3: Data Cleaning & Standardizatio]
                  │
                  ▼
               [Step 4: Data Validation & Quality Repo]
                  │
                  ▼
               [Step 5: Feature Engineering]
                  │
                  ▼
               [Step 6: Exploratory Data Analysis]
                  │
                  ▼
               [Step 7: Data Visualization: Demographi]
                  │
                  ▼
               [Step 8: Data Visualization: Clinical F]
                  │
                  ▼
               [Step 9: Statistical Analysis & Hypothe]
                  │
                  ▼
               [Step 10: Data Preparation for Modeling]
                  │
                  ▼
               [Step 11: Model Training: Baseline]
                  │
                  ▼
               [Step 12: Model Training: Advanced & Tun]
                  │
                  ▼
               [Step 13: Model Evaluation & Interpretat]
                  │
                  ▼
               [Step 14: Fairness & Bias Assessment]
                  │
                  ▼
               [Step 15: Final Synthesis & Reporting] ──▶ Final Output
```

---

## Step Details

### Step 1: Data Loading & Profiling

**Description:** Load all four data sources (patients CSV, admissions JSON, lab results JSON, medications Excel). Profile each: shape, dtypes, missing values, descriptive stats. Print schemas and identify data quality issues.

**Script:** `scripts/step_01_data-loading-profiling.py`

---

### Step 2: Data Merging & Integration

**Description:** Merge patients with admissions on patient_id (left join). Merge lab results with patients on patient_id. Merge medications with patients on patient_id. Create a unified patient-level feature table. Handle duplicate column names with suffixes.

**Script:** `scripts/step_02_data-merging-integration.py`

---

### Step 3: Data Cleaning & Standardization

**Description:** Standardize categorical fields: gender (M/F → Male/Female), insurance_provider (normalize variants). Handle missing values: impute numerical with median, categorical with mode. Convert date columns to datetime. Create age from DOB.

**Script:** `scripts/step_03_data-cleaning-standardization.py`

---

### Step 4: Data Validation & Quality Report

**Description:** Validate referential integrity (all admission patient_ids exist in patients table). Check for impossible values (negative LOS, future dates). Generate a data_quality_report.json with completeness, uniqueness, validity metrics per column.

**Script:** `scripts/step_04_data-validation-quality-report.py`

---

### Step 5: Feature Engineering

**Description:** Create derived features: age_group (18-30, 31-50, 51-70, 71+), comorbidity_index, admission_frequency (count of prior admissions), avg_los, abnormal_lab_ratio, polypharmacy_flag (>5 medications), season_of_admission.

**Script:** `scripts/step_05_feature-engineering.py`

---

### Step 6: Exploratory Data Analysis

**Description:** Compute univariate statistics for all features. Analyze readmission rate by demographics, department, admission reason. Cross-tabulate comorbidities with outcomes. Compute correlation matrix for numerical features.

**Script:** `scripts/step_06_exploratory-data-analysis.py`

---

### Step 7: Data Visualization: Demographics

**Description:** Create a 2x2 dashboard: (1) Readmission rate by age group bar chart, (2) Readmission by gender pie chart, (3) Length of stay distribution histogram by outcome, (4) Comorbidity count vs readmission boxplot. Save as png.

**Script:** `scripts/step_07_data-visualization--demographics.py`

---

### Step 8: Data Visualization: Clinical Factors

**Description:** Create visualizations: (1) Top 10 admission reasons by readmission rate horizontal bar, (2) Lab abnormality heatmap by department, (3) Readmission rate by insurance provider grouped bar, (4) Medication count vs readmission violin plot.

**Script:** `scripts/step_08_data-visualization--clinical-factors.py`

---

### Step 9: Statistical Analysis & Hypothesis Testing

**Description:** Perform chi-square tests for categorical predictors (gender, department, insurance) vs readmission. Run t-tests for numerical predictors (age, LOS, lab values) between readmitted and non-readmitted groups. Apply Bonferroni correction.

**Script:** `scripts/step_09_statistical-analysis-hypothesis-testing.py`

---

### Step 10: Data Preparation for Modeling

**Description:** Encode categorical variables: one-hot for department, admission_reason, insurance; label encode for gender, blood_type. Scale numerical features with StandardScaler. Split data 70/15/15 train/val/test with stratification. Save preprocessor as pickle.

**Script:** `scripts/step_10_data-preparation-for-modeling.py`

---

### Step 11: Model Training: Baseline

**Description:** Train baseline models: Logistic Regression, Decision Tree, Random Forest with default params. Use 5-fold cross-validation. Report accuracy, precision, recall, F1, ROC-AUC for each. Identify best baseline model.

**Script:** `scripts/step_11_model-training--baseline.py`

---

### Step 12: Model Training: Advanced & Tuning

**Description:** Train XGBoost and GradientBoosting classifiers. Perform hyperparameter tuning with RandomizedSearchCV (n_iter=50, cv=5) optimizing for ROC-AUC. Compare all models. Save best model as pickle. Log all parameters and scores.

**Script:** `scripts/step_12_model-training--advanced-tuning.py`

---

### Step 13: Model Evaluation & Interpretation

**Description:** Evaluate on holdout test set: confusion matrix, classification report, ROC curve, Precision-Recall curve. Generate SHAP summary plot for top 20 features. Create a feature importance bar chart. Identify top 5 drivers of readmission.

**Script:** `scripts/step_13_model-evaluation-interpretation.py`

---

### Step 14: Fairness & Bias Assessment

**Description:** Compute model performance across demographic subgroups (gender, age_group, insurance). Calculate disparate impact ratio, equal opportunity difference. Flag any subgroups with significant performance gaps. Generate fairness_report.json.

**Script:** `scripts/step_14_fairness-bias-assessment.py`

---

### Step 15: Final Synthesis & Reporting

**Description:** Compile comprehensive analysis report: Executive Summary, Data Overview, Methodology, Key Findings (top predictors, model performance, fairness assessment), Business Recommendations (which patients to target, expected ROI), Limitations.

**Script:** `scripts/step_15_final-synthesis-reporting.py`

---


## How to Run

### Local Execution
```bash
cd custom_pipelines/healthcare_readmission
pip install pandas numpy matplotlib seaborn scikit-learn xgboost lightgbm optuna shap

# Run steps sequentially
python scripts/step_01_data-loading-profiling.py --data_dir data/ --output_dir output/
python scripts/step_02_data-merging-integration.py --data_dir data/ --output_dir output/
python scripts/step_03_data-cleaning-standardization.py --data_dir data/ --output_dir output/
python scripts/step_04_data-validation-quality-report.py --data_dir data/ --output_dir output/
python scripts/step_05_feature-engineering.py --data_dir data/ --output_dir output/
python scripts/step_06_exploratory-data-analysis.py --data_dir data/ --output_dir output/
python scripts/step_07_data-visualization--demographics.py --data_dir data/ --output_dir output/
python scripts/step_08_data-visualization--clinical-factors.py --data_dir data/ --output_dir output/
python scripts/step_09_statistical-analysis-hypothesis-testing.py --data_dir data/ --output_dir output/
python scripts/step_10_data-preparation-for-modeling.py --data_dir data/ --output_dir output/
python scripts/step_11_model-training--baseline.py --data_dir data/ --output_dir output/
python scripts/step_12_model-training--advanced-tuning.py --data_dir data/ --output_dir output/
python scripts/step_13_model-evaluation-interpretation.py --data_dir data/ --output_dir output/
python scripts/step_14_fairness-bias-assessment.py --data_dir data/ --output_dir output/
python scripts/step_15_final-synthesis-reporting.py --data_dir data/ --output_dir output/
```

### Argo Workflow
```bash
argo submit custom_pipelines/healthcare_readmission/pipeline.yaml
argo watch @latest
argo logs @latest
```
