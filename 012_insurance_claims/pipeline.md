# Insurance: Claims Fraud Detection & Risk Assessment
## Metadata
| Field | Value |
|---|---|
| **Pipeline ID** | `insurance_claims` |
| **Domain** | Insurance |
| **Steps** | 15 |
| **Type** | ML Pipeline (End-to-End) |

## Executive Summary
Detects fraudulent insurance claims using historical claims data, policyholder information, and claim patterns. Predicts claim severity and identifies anomalous claims for investigation.

## Business Context
Insurance fraud costs the industry $80B+ annually in the US alone. Manual fraud detection catches only 5-10% of fraudulent claims. ML-based fraud detection improves catch rates to 30-40%, saving $10-20M per year for a mid-size insurer. Additionally, accurate severity prediction improves reserve setting and reduces unexpected loss ratios by 15%.

## Steps
### Step 1: Data Loading & Profiling
Load claims CSV. Profile: claim type distribution, status breakdown, amount statistics. Analyze fraud rate by type. Check for missing values, duplicates, data entry errors in amounts and dates.

### Step 2: Data Cleaning & Standardization
Standardize claim types and statuses. Handle missing settlement amounts for pending claims. Convert date columns. Create fraud_flag from is_fraudulent. Cap claim amounts at 99.5th percentile.

### Step 3: Feature Engineering: Claim Characteristics
Create features: claim_amount_log, settlement_ratio (settlement/claimed), investigation_duration, claim_day_of_week, claim_month, days_since_policy_start, amount_zscore_by_type, velocity (claims per policy in 90 days).

### Step 4: Feature Engineering: Behavioral Patterns
Create fraud indicators: round_amount_flag (claim ending in 000), weekend_claim_flag, high_amount_short_investigation, multiple_claims_same_day, amount_exceeds_income_ratio, inconsistent_details_score.

### Step 5: Exploratory Data Analysis
Analyze fraud rate by claim type, amount range, investigation duration, month. Distribution analysis of claim amounts by fraud status. Identify anomalies in settlement patterns.

### Step 6: Data Visualization: Fraud Patterns
Create dashboard: (1) Fraud rate by claim type bar chart, (2) Claim amount distribution by fraud status violin plot, (3) Investigation days vs fraud rate scatter, (4) Monthly fraud rate trend, (5) Settlement ratio histogram, (6) Fraud indicator correlation heatmap.

### Step 7: Statistical Analysis
Chi-square tests: claim type, day_of_week, round_amount vs fraud. T-tests: claim amount, investigation days by fraud status. Logistic regression univariate: odds ratios for each fraud indicator. Benford's Law analysis on claim amounts.

### Step 8: Data Preparation for Modeling
Encode categoricals: one-hot for claim_type, status. Scale numerical features with RobustScaler. Handle class imbalance (fraud ~15%) with SMOTE + Tomek links. Split 70/15/15 stratified.

### Step 9: Model Training: Fraud Detection
Train baseline: LogisticRegression, RandomForest. Train advanced: XGBoost, LightGBM with class_weight='balanced'. 5-fold stratified CV. Optimize for F2-score (prioritize recall). Log experiments.

### Step 10: Model Optimization & Threshold Tuning
Hyperparameter tune best model with Optuna (50 trials). Find optimal threshold balancing precision-recall (cost matrix: false positive = investigation cost $500, false negative = claim payout $50K). Plot profit curve.

### Step 11: Anomaly Detection
Implement Isolation Forest and Local Outlier Factor for unsupervised fraud detection. Compare with supervised model. Identify claims flagged by both methods. Generate anomaly investigation priority list.

### Step 12: Model Explainability
SHAP analysis: global feature importance, dependence plots, force plots for individual claims. Generate investigation reason codes. Build what-if analysis tool for adjusters.

### Step 13: Claim Severity Prediction
Train regression models (XGBoost, LightGBM) to predict claim settlement amount. Features: claim_type, amount, investigation_days, fraud_probability, policyholder demographics. Evaluate with MAPE, RMSE. Use for reserve optimization.

### Step 14: Fairness Assessment
Test model for bias across claim types and amount ranges. Compute disparate impact ratios. Verify model doesn't systematically flag certain claim types. Generate fairness_report.json.

### Step 15: Final Synthesis & Fraud Playbook
Compile: Fraud Detection Model Performance, Top Fraud Indicators, Investigation Prioritization Framework, Severity Prediction Accuracy, Expected Savings from ML Adoption ($X/year), Claims Adjuster Decision Support Tool Spec, Model Monitoring & Retraining Schedule.

