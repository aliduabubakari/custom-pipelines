# Marketing: Customer Churn Prediction & Retention Strategy

## Metadata
| Field | Value |
|---|---|
| **Pipeline ID** | `customer_churn` |
| **Domain** | Marketing / SaaS |
| **Total Steps** | 16 |
| **Input Files** | 2 |
| **Pipeline Type** | ML Pipeline (End-to-End) |

---

## Executive Summary

Predicts customer churn probability for a subscription-based business 
by analyzing customer demographics, transaction history, engagement patterns, and support 
interactions. Identifies at-risk customers for proactive retention campaigns.

---

## Business Context & Need

SaaS companies lose 20-30% of revenue annually to churn. Acquiring a new 
customer costs 5-7× more than retaining an existing one. A predictive churn model enables 
targeted retention offers, reducing churn by 15-25% and increasing customer LTV by 20-40%. 
For a company with 100K subscribers at $50/month, a 5% churn reduction saves $3M/year.

---

## Data Sources

- **`customers.csv`** — Input data file
- **`transactions.json`** — Input data file

---

## Pipeline Architecture

```
  Input Data ──▶ [Step 1: Data Loading & Profiling]
                  │
                  ▼
               [Step 2: Data Aggregation: Customer Met]
                  │
                  ▼
               [Step 3: Data Merging & Integration]
                  │
                  ▼
               [Step 4: Data Cleaning & Standardizatio]
                  │
                  ▼
               [Step 5: Feature Engineering]
                  │
                  ▼
               [Step 6: Exploratory Data Analysis]
                  │
                  ▼
               [Step 7: Data Visualization: Churn Patt]
                  │
                  ▼
               [Step 8: Data Visualization: Behavioral]
                  │
                  ▼
               [Step 9: Statistical Analysis]
                  │
                  ▼
               [Step 10: Cohort Analysis]
                  │
                  ▼
               [Step 11: Data Preparation for Modeling]
                  │
                  ▼
               [Step 12: Model Training: Multi-Model Co]
                  │
                  ▼
               [Step 13: Model Optimization & Ensemblin]
                  │
                  ▼
               [Step 14: Model Evaluation & Business Im]
                  │
                  ▼
               [Step 15: Customer Segmentation for Rete]
                  │
                  ▼
               [Step 16: Final Synthesis & Retention Pl] ──▶ Final Output
```

---

## Step Details

### Step 1: Data Loading & Profiling

**Description:** Load customer profiles CSV and transactions JSON. Profile: customer count by segment, transaction volume by month, missing rates, duplicate checks. Identify target: is_churned flag from customer data.

**Script:** `scripts/step_01_data-loading-profiling.py`

---

### Step 2: Data Aggregation: Customer Metrics

**Description:** Aggregate transactions to customer level: total_spend, avg_order_value, purchase_frequency, days_since_last_purchase, items_per_order_avg, return_rate, discount_usage_rate, category_diversity (unique categories).

**Script:** `scripts/step_02_data-aggregation--customer-metrics.py`

---

### Step 3: Data Merging & Integration

**Description:** Merge aggregated transaction metrics with customer profiles on customer_id. Create unified customer analysis table. Verify merge completeness (all customers have transaction data or flag as zero-transaction).

**Script:** `scripts/step_03_data-merging-integration.py`

---

### Step 4: Data Cleaning & Standardization

**Description:** Handle missing values: zero for numerical aggregates of customers without transactions, 'Unknown' for categorical. Standardize channel and payment_method categories. Normalize city names. Create consistency checks.

**Script:** `scripts/step_04_data-cleaning-standardization.py`

---

### Step 5: Feature Engineering

**Description:** Create behavioral features: recency_score (days since last purchase, binned), frequency_score (purchases per month), monetary_score (avg spend per month), engagement_score (composite of frequency × category_diversity), churn_risk_signals (declining frequency trend, increased returns, support contact surge).

**Script:** `scripts/step_05_feature-engineering.py`

---

### Step 6: Exploratory Data Analysis

**Description:** Analyze churn rate by segment, acquisition channel, tenure, city/state. Identify patterns: do premium customers churn differently? Is there a tenure cliff? Compare LTV distribution of churned vs retained. Compute correlation with churn.

**Script:** `scripts/step_06_exploratory-data-analysis.py`

---

### Step 7: Data Visualization: Churn Patterns

**Description:** Create 3x2 dashboard: (1) Churn rate by customer segment bar chart, (2) Tenure vs churn probability with LOESS curve, (3) Monthly spend trend for churned vs retained (6 months prior), (4) Acquisition channel churn heatmap by segment, (5) LTV distribution boxplot, (6) Geographic churn choropleth.

**Script:** `scripts/step_07_data-visualization--churn-patterns.py`

---

### Step 8: Data Visualization: Behavioral Analysis

**Description:** Visualize behavioral indicators: (1) Recency-Frequency-Monetary 3D scatter colored by churn, (2) Return rate vs churn scatter with quadrants, (3) Discount dependency vs churn bar chart, (4) Category diversity radar chart for churned vs retained.

**Script:** `scripts/step_08_data-visualization--behavioral-analysis.py`

---

### Step 9: Statistical Analysis

**Description:** Chi-square tests for categorical features (segment, channel, city vs churn). ANOVA for numerical features by churn status. Kaplan-Meier survival curves by segment and acquisition channel. Cox proportional hazards for tenure analysis.

**Script:** `scripts/step_09_statistical-analysis.py`

---

### Step 10: Cohort Analysis

**Description:** Create monthly retention cohorts by signup month. Calculate retention rates at 1, 3, 6, 12 months. Identify cohorts with unusual churn patterns. Build cohort retention matrix heatmap.

**Script:** `scripts/step_10_cohort-analysis.py`

---

### Step 11: Data Preparation for Modeling

**Description:** Encode categoricals: one-hot for segment, channel, city; target encode for high-cardinality features. Scale numerical features with RobustScaler. Handle class imbalance with SMOTE (synthetic minority oversampling). Split 70/15/15 stratified.

**Script:** `scripts/step_11_data-preparation-for-modeling.py`

---

### Step 12: Model Training: Multi-Model Comparison

**Description:** Train 5 models: LogisticRegression, RandomForest, XGBoost, LightGBM, CatBoost. 5-fold stratified CV. Compare: ROC-AUC, Precision-Recall AUC, F2-score, calibration error. Select top 2.

**Script:** `scripts/step_12_model-training--multi-model-comparison.py`

---

### Step 13: Model Optimization & Ensembling

**Description:** Hyperparameter tune top 2 models with Bayesian optimization (Optuna, 50 trials). Create weighted ensemble. Calibrate probabilities with isotonic regression. Save final model. Log all experiments to MLflow tracking.

**Script:** `scripts/step_13_model-optimization-ensembling.py`

---

### Step 14: Model Evaluation & Business Impact

**Description:** Evaluate ensemble on test set. Generate lift curve, cumulative gains chart. Calculate expected ROI: retention campaign cost vs prevented churn revenue at different probability thresholds. Identify optimal intervention threshold maximizing net profit.

**Script:** `scripts/step_14_model-evaluation-business-impact.py`

---

### Step 15: Customer Segmentation for Retention

**Description:** Cluster at-risk customers (churn prob > threshold) using K-Means on behavioral features. Profile each cluster: demographics, behaviors, churn drivers. Assign personalized retention strategies per cluster (discount, feature education, account review, loyalty upgrade).

**Script:** `scripts/step_15_customer-segmentation-for-retention.py`

---

### Step 16: Final Synthesis & Retention Playbook

**Description:** Compile comprehensive report: Executive Summary, Churn Driver Analysis, Model Performance, Customer Risk Segments with recommended interventions, Expected ROI by segment, A/B test design for retention campaigns, Monitoring dashboard specification (PSI, feature drift, model decay alerts).

**Script:** `scripts/step_16_final-synthesis-retention-playbook.py`

---


## How to Run

### Local Execution
```bash
cd custom_pipelines/customer_churn
pip install pandas numpy matplotlib seaborn scikit-learn xgboost lightgbm optuna shap

# Run steps sequentially
python scripts/step_01_data-loading-profiling.py --data_dir data/ --output_dir output/
python scripts/step_02_data-aggregation--customer-metrics.py --data_dir data/ --output_dir output/
python scripts/step_03_data-merging-integration.py --data_dir data/ --output_dir output/
python scripts/step_04_data-cleaning-standardization.py --data_dir data/ --output_dir output/
python scripts/step_05_feature-engineering.py --data_dir data/ --output_dir output/
python scripts/step_06_exploratory-data-analysis.py --data_dir data/ --output_dir output/
python scripts/step_07_data-visualization--churn-patterns.py --data_dir data/ --output_dir output/
python scripts/step_08_data-visualization--behavioral-analysis.py --data_dir data/ --output_dir output/
python scripts/step_09_statistical-analysis.py --data_dir data/ --output_dir output/
python scripts/step_10_cohort-analysis.py --data_dir data/ --output_dir output/
python scripts/step_11_data-preparation-for-modeling.py --data_dir data/ --output_dir output/
python scripts/step_12_model-training--multi-model-comparison.py --data_dir data/ --output_dir output/
python scripts/step_13_model-optimization-ensembling.py --data_dir data/ --output_dir output/
python scripts/step_14_model-evaluation-business-impact.py --data_dir data/ --output_dir output/
python scripts/step_15_customer-segmentation-for-retention.py --data_dir data/ --output_dir output/
python scripts/step_16_final-synthesis-retention-playbook.py --data_dir data/ --output_dir output/
```

### Argo Workflow
```bash
argo submit custom_pipelines/customer_churn/pipeline.yaml
argo watch @latest
argo logs @latest
```
