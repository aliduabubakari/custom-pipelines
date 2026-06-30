# HR Analytics: Employee Attrition Prediction & Retention Strategy

## Metadata
| Field | Value |
|---|---|
| **Pipeline ID** | `employee_attrition` |
| **Domain** | Human Resources |
| **Total Steps** | 16 |
| **Input Files** | 3 |
| **Pipeline Type** | ML Pipeline (End-to-End) |

---

## Executive Summary

Predicts employee attrition risk using HR data including demographics, 
compensation, performance reviews, engagement surveys, and work patterns. Enables proactive 
retention interventions for high-value at-risk employees.

---

## Business Context & Need

Voluntary turnover costs organizations 50-200% of annual salary per 
employee (recruiting, onboarding, productivity loss). A 10,000-employee company with 15% 
attrition loses $75M-$150M annually. ML-driven early warning reduces unwanted attrition by 
20-30%, prioritizes retention spending on high-value roles, and improves workforce planning 
accuracy. Additionally supports DEI analysis to identify disproportionate attrition in 
underrepresented groups.

---

## Data Sources

- **`employees.csv`** — Input data file
- **`engagement_surveys.json`** — Input data file
- **`performance_reviews.xlsx`** — Input data file

---

## Pipeline Architecture

```
  Input Data ──▶ [Step 1: Data Loading & Profiling]
                  │
                  ▼
               [Step 2: Data Aggregation: Surveys]
                  │
                  ▼
               [Step 3: Data Aggregation: Performance]
                  │
                  ▼
               [Step 4: Data Merging & Integration]
                  │
                  ▼
               [Step 5: Data Cleaning & Standardizatio]
                  │
                  ▼
               [Step 6: Feature Engineering]
                  │
                  ▼
               [Step 7: Data Validation & Quality Repo]
                  │
                  ▼
               [Step 8: Exploratory Data Analysis]
                  │
                  ▼
               [Step 9: Data Visualization: Attrition ]
                  │
                  ▼
               [Step 10: Data Visualization: Engagement]
                  │
                  ▼
               [Step 11: Statistical Analysis]
                  │
                  ▼
               [Step 12: Data Preparation for Modeling]
                  │
                  ▼
               [Step 13: Model Training & Comparison]
                  │
                  ▼
               [Step 14: Model Optimization]
                  │
                  ▼
               [Step 15: Model Explainability & Retenti]
                  │
                  ▼
               [Step 16: Final Synthesis & Retention St] ──▶ Final Output
```

---

## Step Details

### Step 1: Data Loading & Profiling

**Description:** Load employees CSV, engagement_surveys JSON, performance_reviews Excel. Profile each: headcount by department/role/location, survey response rates, review completion rates. Identify target: is_attrited column. Check for data skew and class imbalance.

**Script:** `scripts/step_01_data-loading-profiling.py`

---

### Step 2: Data Aggregation: Surveys

**Description:** Aggregate engagement surveys to employee level: average_score, score_trend (recent - historical), lowest_dimension (which question scored lowest), survey_response_count, days_since_last_survey. Pivot survey questions to features (satisfaction_score, wlb_score, etc.).

**Script:** `scripts/step_02_data-aggregation--surveys.py`

---

### Step 3: Data Aggregation: Performance

**Description:** Aggregate performance reviews: avg_rating, rating_trend, goal_achievement_avg, promotion_recommendation_count, pip_flag (ever on PIP), manager_rating_avg, peer_rating_avg. Compute performance_momentum (recent rating - overall avg).

**Script:** `scripts/step_03_data-aggregation--performance.py`

---

### Step 4: Data Merging & Integration

**Description:** Merge aggregated surveys and performance metrics with employees. Left join to preserve all employees. Flag employees with no survey or review data. Create a comprehensive employee_analytics table.

**Script:** `scripts/step_04_data-merging-integration.py`

---

### Step 5: Data Cleaning & Standardization

**Description:** Handle missing survey/performance data (employees without data flagged separately). Standardize department and role names. Encode education levels ordinally. Handle salary outliers (cap at 99th percentile). Normalize bonus percentages.

**Script:** `scripts/step_05_data-cleaning-standardization.py`

---

### Step 6: Feature Engineering

**Description:** Create derived features: tenure_years (from hire_date), salary_ratio (salary / department_median), promotion_velocity (promotions per year), engagement_gap (max_score - min_score across survey dimensions), flight_risk_indicators (declining performance + declining engagement + no recent promotion), manager_span (count of direct reports for managers).

**Script:** `scripts/step_06_feature-engineering.py`

---

### Step 7: Data Validation & Quality Report

**Description:** Validate data integrity: all manager_ids reference valid employees, review dates are after hire dates, survey scores within 1-5 range, salary within reasonable bounds. Generate validation report with flagged anomalies.

**Script:** `scripts/step_07_data-validation-quality-report.py`

---

### Step 8: Exploratory Data Analysis

**Description:** Analyze attrition rate by department, role, location (on-site/hybrid/remote), education, tenure bucket. Identify patterns: is there a tenure-attrition curve? Do certain departments have systemic issues? Compute correlation matrix for all numerical features vs attrition.

**Script:** `scripts/step_08_exploratory-data-analysis.py`

---

### Step 9: Data Visualization: Attrition Patterns

**Description:** Create 3x2 dashboard: (1) Attrition rate by department bar chart with error bars, (2) Tenure histogram overlaid with attrition density, (3) Salary distribution by attrition status boxplot, (4) Work location attrition heatmap by department, (5) Attrition rate trend by month (if temporal), (6) Manager attrition rate distribution (identify managers with high team churn).

**Script:** `scripts/step_09_data-visualization--attrition-patterns.py`

---

### Step 10: Data Visualization: Engagement & Performance

**Description:** Visualize people analytics: (1) Engagement score vs attrition scatter with quadrants (Engaged/Disengaged × Stayed/Left), (2) Performance rating distribution by attrition, (3) Survey dimension radar chart for attrited vs retained, (4) Salary ratio vs attrition rate curve, (5) Promotion velocity by department and attrition.

**Script:** `scripts/step_10_data-visualization--engagement-performance.py`

---

### Step 11: Statistical Analysis

**Description:** Chi-square tests: department, role, education, location vs attrition. T-tests: salary, tenure, engagement_score, performance_score by attrition status. Logistic regression univariate analysis: odds ratios with confidence intervals for each feature. Identify most predictive individual factors.

**Script:** `scripts/step_11_statistical-analysis.py`

---

### Step 12: Data Preparation for Modeling

**Description:** Encode categoricals: one-hot for department, role, education, location. Scale numerical with StandardScaler. Handle class imbalance with SMOTE (minority=attrited). Split 70/15/15 with stratification. Save preprocessing pipeline.

**Script:** `scripts/step_12_data-preparation-for-modeling.py`

---

### Step 13: Model Training & Comparison

**Description:** Train LogisticRegression (L1 and L2), RandomForest, XGBoost, LightGBM. 5-fold stratified CV. Evaluate: ROC-AUC, Precision-Recall AUC, F2-score (prioritize recall for retention targeting). Select top 2. Plot learning curves.

**Script:** `scripts/step_13_model-training-comparison.py`

---

### Step 14: Model Optimization

**Description:** Hyperparameter tune via Optuna (50 trials each for top 2 models). Calibrate probabilities. Create soft voting ensemble. Evaluate calibration with reliability diagram. Save final model, parameters, and calibration curve.

**Script:** `scripts/step_14_model-optimization.py`

---

### Step 15: Model Explainability & Retention Insights

**Description:** SHAP analysis: global feature importance, dependence plots for top 10 features. Identify attrition archetypes via SHAP clustering. Calculate counterfactual: what changes would flip prediction for borderline employees? Generate individual retention recommendations.

**Script:** `scripts/step_15_model-explainability-retention-insights.py`

---

### Step 16: Final Synthesis & Retention Strategy

**Description:** Compile comprehensive HR analytics report: Executive Summary, 
Attrition Driver Analysis (top factors and their impact), High-Risk Employee Profiles with 
recommended interventions (compensation adjustment, role change, manager coaching, development 
opportunity), Retention Program ROI (cost of intervention vs cost of replacement), DEI Impact 
Assessment (attrition patterns by demographic groups), Manager Scorecard, Implementation 
Roadmap with HRIS integration plan, and Quarterly Model Refresh Protocol.

**Script:** `scripts/step_16_final-synthesis-retention-strategy.py`

---


## How to Run

### Local Execution
```bash
cd custom_pipelines/employee_attrition
pip install pandas numpy matplotlib seaborn scikit-learn xgboost lightgbm optuna shap

# Run steps sequentially
python scripts/step_01_data-loading-profiling.py --data_dir data/ --output_dir output/
python scripts/step_02_data-aggregation--surveys.py --data_dir data/ --output_dir output/
python scripts/step_03_data-aggregation--performance.py --data_dir data/ --output_dir output/
python scripts/step_04_data-merging-integration.py --data_dir data/ --output_dir output/
python scripts/step_05_data-cleaning-standardization.py --data_dir data/ --output_dir output/
python scripts/step_06_feature-engineering.py --data_dir data/ --output_dir output/
python scripts/step_07_data-validation-quality-report.py --data_dir data/ --output_dir output/
python scripts/step_08_exploratory-data-analysis.py --data_dir data/ --output_dir output/
python scripts/step_09_data-visualization--attrition-patterns.py --data_dir data/ --output_dir output/
python scripts/step_10_data-visualization--engagement-performance.py --data_dir data/ --output_dir output/
python scripts/step_11_statistical-analysis.py --data_dir data/ --output_dir output/
python scripts/step_12_data-preparation-for-modeling.py --data_dir data/ --output_dir output/
python scripts/step_13_model-training-comparison.py --data_dir data/ --output_dir output/
python scripts/step_14_model-optimization.py --data_dir data/ --output_dir output/
python scripts/step_15_model-explainability-retention-insights.py --data_dir data/ --output_dir output/
python scripts/step_16_final-synthesis-retention-strategy.py --data_dir data/ --output_dir output/
```

### Argo Workflow
```bash
argo submit custom_pipelines/employee_attrition/pipeline.yaml
argo watch @latest
argo logs @latest
```
