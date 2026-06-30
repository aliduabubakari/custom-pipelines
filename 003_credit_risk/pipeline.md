# Finance: Credit Risk Assessment & Loan Default Prediction

## Metadata
| Field | Value |
|---|---|
| **Pipeline ID** | `credit_risk` |
| **Domain** | Finance |
| **Total Steps** | 16 |
| **Input Files** | 3 |
| **Pipeline Type** | ML Pipeline (End-to-End) |

---

## Executive Summary

Builds a credit risk scoring model to predict loan default probability 
for consumer credit applications. Integrates application data, credit bureau history, and 
derived risk features to support automated underwriting decisions.

---

## Business Context & Need

Financial institutions lose $50B+ annually to consumer credit defaults. 
Manual underwriting processes have 40% error rates and cost $500-2000 per application. An ML-driven 
scoring system reduces default losses by 25-35%, cuts underwriting costs by 60%, and enables 
real-time decisions for 80% of applications. Regulatory compliance (ECOA, FCRA) requires 
transparent, fair models with explainable decisions.

---

## Data Sources

- **`applications.csv`** — Input data file
- **`credit_history.json`** — Input data file
- **`bureau_data.xlsx`** — Input data file

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
               [Step 4: Data Validation & Compliance C]
                  │
                  ▼
               [Step 5: Feature Engineering]
                  │
                  ▼
               [Step 6: Exploratory Data Analysis]
                  │
                  ▼
               [Step 7: Data Visualization: Risk Profi]
                  │
                  ▼
               [Step 8: Data Visualization: Credit Beh]
                  │
                  ▼
               [Step 9: Statistical Analysis & Hypothe]
                  │
                  ▼
               [Step 10: Data Preparation for Modeling]
                  │
                  ▼
               [Step 11: Model Training: Baseline Model]
                  │
                  ▼
               [Step 12: Model Training: Advanced Ensem]
                  │
                  ▼
               [Step 13: Model Evaluation & Threshold O]
                  │
                  ▼
               [Step 14: Model Explainability (SHAP & L]
                  │
                  ▼
               [Step 15: Fairness & Regulatory Assessme]
                  │
                  ▼
               [Step 16: Final Synthesis & Business Rec] ──▶ Final Output
```

---

## Step Details

### Step 1: Data Loading & Profiling

**Description:** Load applications CSV, credit_history JSON, bureau_data Excel. Profile each: row counts, column types, null percentages, basic statistics. Identify target variable: derive 'default_flag' from credit history (any 90+ day delinquency or charge-off within 24 months).

**Script:** `scripts/step_01_data-loading-profiling.py`

---

### Step 2: Data Merging & Integration

**Description:** Aggregate credit history per application: count of accounts by type, average balance, max delinquency, total late payments (12m), average utilization. Merge aggregated history with applications. Merge bureau data with applications. Resolve column conflicts.

**Script:** `scripts/step_02_data-merging-integration.py`

---

### Step 3: Data Cleaning & Standardization

**Description:** Handle missing values: median for numerical, 'Unknown' for categorical. Standardize employment_status categories. Cap outliers at 99th percentile. Create consistent date formats. Validate that all merged records have matching keys.

**Script:** `scripts/step_03_data-cleaning-standardization.py`

---

### Step 4: Data Validation & Compliance Check

**Description:** Validate data against regulatory requirements: check for required fields (SSN format, DOB validity). Flag applications with missing mandatory data. Generate compliance_report.json with completeness and SOC 2 relevant metrics.

**Script:** `scripts/step_04_data-validation-compliance-check.py`

---

### Step 5: Feature Engineering

**Description:** Create risk features: DTI_category (Low/Medium/High/Very High), FICO_band (Poor/Fair/Good/Very Good/Exceptional), employment_stability (tenure/age), credit_utilization, inquiry_velocity (inquiries per month), account_age_diversity, payment_consistency_score.

**Script:** `scripts/step_05_feature-engineering.py`

---

### Step 6: Exploratory Data Analysis

**Description:** Analyze default rate by FICO band, loan purpose, employment status, home ownership. Compute correlation matrix. Identify multicollinearity with VIF. Plot distribution of loan amounts by default status. Analyze DTI vs default rate.

**Script:** `scripts/step_06_exploratory-data-analysis.py`

---

### Step 7: Data Visualization: Risk Profiles

**Description:** Create dashboard: (1) Default rate heatmap by FICO band × DTI category, (2) Loan amount distribution by purpose with default overlay, (3) Employment length vs default rate scatter with trend line, (4) Geographic default rate choropleth (by zip prefix).

**Script:** `scripts/step_07_data-visualization--risk-profiles.py`

---

### Step 8: Data Visualization: Credit Behavior

**Description:** Visualize credit behavior patterns: (1) Utilization ratio histogram by default status, (2) Payment history timeline for defaulted vs non-defaulted, (3) Account type composition stacked bar, (4) Inquiry count vs default rate with confidence intervals.

**Script:** `scripts/step_08_data-visualization--credit-behavior.py`

---

### Step 9: Statistical Analysis & Hypothesis Testing

**Description:** Test hypotheses: H1: FICO score significantly differs between defaulted/non-defaulted (t-test). H2: DTI ratio > 0.43 increases default odds (chi-square). H3: Employment length < 2 years increases risk (proportions z-test). Report effect sizes.

**Script:** `scripts/step_09_statistical-analysis-hypothesis-testing.py`

---

### Step 10: Data Preparation for Modeling

**Description:** Encode categoricals: one-hot for loan_purpose, employment_status; ordinal for FICO_band, DTI_category. Scale numerical features (RobustScaler for skewed distributions). Create 70/15/15 stratified split. Save preprocessing pipeline as pickle.

**Script:** `scripts/step_10_data-preparation-for-modeling.py`

---

### Step 11: Model Training: Baseline Models

**Description:** Train LogisticRegression, RandomForest, and LightGBM with default parameters. Use StratifiedKFold (k=5). Compute ROC-AUC, Precision-Recall AUC, Brier Score. Select top performer. Log all results to model_registry.json.

**Script:** `scripts/step_11_model-training--baseline-models.py`

---

### Step 12: Model Training: Advanced Ensemble

**Description:** Train XGBoost with hyperparameter tuning via Optuna (50 trials, optimizing ROC-AUC). Train a StackingClassifier combining RF, XGBoost, and LogisticRegression with a meta-learner. Compare all models. Save best model and calibration curve.

**Script:** `scripts/step_12_model-training--advanced-ensemble.py`

---

### Step 13: Model Evaluation & Threshold Optimization

**Description:** Evaluate on test set: ROC curve, confusion matrix at optimal threshold (maximizing F2-score to prioritize recall). Calculate expected loss at different approval thresholds. Plot profit curve (approved loans × interest - defaults × loss).

**Script:** `scripts/step_13_model-evaluation-threshold-optimization.py`

---

### Step 14: Model Explainability (SHAP & LIME)

**Description:** Generate global SHAP summary plot. Create SHAP dependence plots for top 5 features. Run LIME explanations on 10 individual decisions (5 approved, 5 denied). Generate adverse action reason codes for declined applications (ECOA compliance).

**Script:** `scripts/step_14_model-explainability--shap-lime.py`

---

### Step 15: Fairness & Regulatory Assessment

**Description:** Compute fairness metrics across protected classes (age, gender proxies, zip code): statistical parity difference, equal opportunity difference, disparate impact. Generate fairness_report.json. Verify model meets regulatory thresholds (<0.8 or >1.25 disparate impact triggers review).

**Script:** `scripts/step_15_fairness-regulatory-assessment.py`

---

### Step 16: Final Synthesis & Business Recommendations

**Description:** Compile final report: Model Performance Summary, Risk Tier Definitions (Prime/Near-Prime/Subprime), Recommended Approval Thresholds, Expected Portfolio Performance, Monitoring Plan (PSI, feature drift), Implementation Roadmap.

**Script:** `scripts/step_16_final-synthesis-business-recommendations.py`

---


## How to Run

### Local Execution
```bash
cd custom_pipelines/credit_risk
pip install pandas numpy matplotlib seaborn scikit-learn xgboost lightgbm optuna shap

# Run steps sequentially
python scripts/step_01_data-loading-profiling.py --data_dir data/ --output_dir output/
python scripts/step_02_data-merging-integration.py --data_dir data/ --output_dir output/
python scripts/step_03_data-cleaning-standardization.py --data_dir data/ --output_dir output/
python scripts/step_04_data-validation-compliance-check.py --data_dir data/ --output_dir output/
python scripts/step_05_feature-engineering.py --data_dir data/ --output_dir output/
python scripts/step_06_exploratory-data-analysis.py --data_dir data/ --output_dir output/
python scripts/step_07_data-visualization--risk-profiles.py --data_dir data/ --output_dir output/
python scripts/step_08_data-visualization--credit-behavior.py --data_dir data/ --output_dir output/
python scripts/step_09_statistical-analysis-hypothesis-testing.py --data_dir data/ --output_dir output/
python scripts/step_10_data-preparation-for-modeling.py --data_dir data/ --output_dir output/
python scripts/step_11_model-training--baseline-models.py --data_dir data/ --output_dir output/
python scripts/step_12_model-training--advanced-ensemble.py --data_dir data/ --output_dir output/
python scripts/step_13_model-evaluation-threshold-optimization.py --data_dir data/ --output_dir output/
python scripts/step_14_model-explainability--shap-lime.py --data_dir data/ --output_dir output/
python scripts/step_15_fairness-regulatory-assessment.py --data_dir data/ --output_dir output/
python scripts/step_16_final-synthesis-business-recommendations.py --data_dir data/ --output_dir output/
```

### Argo Workflow
```bash
argo submit custom_pipelines/credit_risk/pipeline.yaml
argo watch @latest
argo logs @latest
```
