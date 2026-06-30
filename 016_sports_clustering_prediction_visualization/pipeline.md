# Pipeline: Data Cleaning & Validation Workflow

## Metadata
| Field | Value |
|---|---|
| **Case ID** | `5145` |
| **Difficulty** | N/A/5 |
| **Quality** | N/A/5 |
| **Abilities** |  |
| **Total Steps** | 14 |
| **Input Files** | 0 |
| **Output Files** | 0 |

---

## Executive Summary

Data cleaning and validation pipeline for multi-table integration.

---

## Business Context & Implications

This pipeline addresses a **data quality and integration challenge** commonly faced by
organizations managing multi-source operational data. The scenario involves two related
datasets — a **driver registry** (HR/employee data) and a **school bus assignment log**
(operational data) — that must be cleaned, validated, and cross-referenced before they
can be used for reporting, analytics, or downstream system integration.

### Key Business Implications

1. **Regulatory Compliance**: Clean, validated driver records are essential for
   transportation safety audits. Cross-table referential integrity ensures no driver
   is assigned to a bus without being properly registered.

2. **Operational Efficiency**: Standardized categorical fields (party affiliation,
   employment status) enable accurate reporting and dashboarding. Inconsistent values
   lead to misleading analytics.

3. **Data Governance**: The entity resolution and geospatial normalization create a
   foundation for future data integration — connecting driver records to other
   municipal datasets (tax records, licensing, payroll).

4. **Audit Readiness**: The generated `data_quality_report.json` serves as an audit
   trail documenting all transformations applied, critical for compliance reviews.

5. **Scalability**: The pipeline pattern (load → profile → clean → standardize →
   validate → report) is reusable across any multi-table data integration scenario.

---

## Pipeline Architecture

```
┌──────────────┐     ┌──────────────────┐     ┌─────────────────────┐
│  Raw Data    │────▶│  STEP 1          │────▶│  initial_*_sample   │
│  driver.xlsx │     │  Load & Profile  │     │  .csv               │
│  school_bus  │     └──────────────────┘     └─────────┬───────────┘
│  .json       │                                        │
└──────────────┘                                        ▼
                                              ┌──────────────────┐
                                              │  STEP 2          │
                                              │  Clean &         │
                                              │  Standardize     │
                                              └─────────┬────────┘
                                                        │
                                                        ▼
                                              ┌──────────────────┐     ┌─────────────────────┐
                                              │  STEP 3          │────▶│  final_*_data.csv   │
                                              │  Normalize &     │────▶│  data_quality_      │
                                              │  Validate        │     │  report.json        │
                                              └──────────────────┘     └─────────────────────┘
```

---

## Step Details

### Step 1: Data Visualization

**Inputs:** `batting_postseason.csv`, `manager_award_vote.csv`
**Outputs:** Console output only
**Script:** `scripts/step_01_data-visualization.py`

**Purpose:**
To begin this comprehensive analysis of baseball postseason batting performance and manager award voting data, I will first develop a structured approach to understanding and analyzing these datasets. The task requires a multi-faceted examination that combines data exploration, statistical analysis, visualization, and potentially predictive modeling. Here's my detailed analytical plan:

First Phase - Data Understanding:
1. Initial Data Inspection:
   - Load both CSV files using pandas
   - Exami

---

### Step 2: Based on the initial data exploration results, I can now develop a more targeted analysis plan. The 

**Inputs:** None (reads raw data)
**Outputs:** Console output only
**Script:** `scripts/step_02_based-on-the-initial-data-exploration-re.py`

**Purpose:**
Based on the initial data exploration results, I can now develop a more targeted analysis plan. The datasets reveal several interesting characteristics that warrant deeper investigation:

1. Batting Postseason Data Insights:
   - The dataset spans from 1884-2015 with 11,690 records
   - Contains 22 columns with several missing values (10.68% max in SF column)
   - Key performance metrics show:
     * Average postseason games per player: 3.28
     * Average hits per postseason: 2.15
     * Home r

---

### Step 3: Data Loading & Profiling

**Inputs:** `batting_postseason.csv`, `manager_award_vote.csv`
**Outputs:** `enhanced_batting_postseason.csv`, `enhanced_manager_award.csv`
**Script:** `scripts/step_03_data-loading-profiling.py`

**Purpose:**
The error encountered reveals a fundamental issue with variable scope and data persistence between code executions. The root cause analysis indicates:

1. Error Identification:
   - The NameError indicates 'batting_post' is not defined when trying to call enhance_batting_data()
   - This occurs because the original data loading code was executed in a separate context
   - The variables from the initial exploration weren't preserved for subsequent operations

2. Impact Assessment:
   - This preve

---

### Step 4: Geospatial Normalization & Entity Resolution

**Inputs:** `batting_postseason.csv`, `manager_award_vote.csv`
**Outputs:** `enhanced_batting_postseason.csv`, `enhanced_manager_award.csv`
**Script:** `scripts/step_04_geospatial-normalization-entity-resoluti.py`

**Purpose:**
The execution results reveal two distinct issues that need to be addressed:

1. Primary Error Analysis:
   - The "incompatible index" error occurs during the groupby-normalization operation in enhance_manager_data()
   - Root cause: The MinMaxScaler transformation creates a numpy array that doesn't maintain the original DataFrame index
   - Impact: Prevents successful creation of the normalized_points column

2. Warning Analysis:
   - Multiple FutureWarnings about chained assignment with inplace

---

### Step 5: Data Visualization (Phase 2)

**Inputs:** `enhanced_batting_postseason.csv`, `enhanced_manager_award.csv`
**Outputs:** `analyzed_manager.csv`, `analyzed_batting.csv`
**Script:** `scripts/step_05_data-visualization-phase-2.py`

**Purpose:**
The execution results show successful data processing with some remaining warnings to address. Here's the detailed analysis:

1. Current Status:
   - Data processing completed successfully
   - Enhanced datasets saved properly
   - Visualizations generated
   - Sample outputs show expected transformed data

2. Outstanding Issues:
   - FutureWarning about DataFrameGroupBy.apply behavior
   - Need to optimize groupby operations
   - Should verify visualization outputs

3. Data Quality Observations

---

### Step 6: Cluster Analysis

**Inputs:** `enhanced_batting_postseason.csv`, `enhanced_manager_award.csv`
**Outputs:** `analyzed_manager.csv`, `analyzed_batting.csv`, `cluster_interpretation.csv`
**Script:** `scripts/step_06_cluster-analysis.py`

**Purpose:**
The error encountered reveals a critical data alignment issue during the clustering operation. Here's the detailed analysis:

1. Error Diagnosis:
   - ValueError indicates mismatch between values length (9275) and index length (11690)
   - Root cause: KMeans clustering is performed on a subset of data (after dropna()) but trying to assign results to full DataFrame
   - Impact: Cannot directly assign cluster labels due to size mismatch

2. Data Quality Assessment:
   - Original batting data has 1

---

### Step 7: Cluster Analysis (Phase 2)

**Inputs:** `award_feature_importance.csv`, `analyzed_manager.csv`, `analyzed_batting.csv`, `cluster_interpretation.csv`
**Outputs:** `award_feature_importance.csv`
**Script:** `scripts/step_07_cluster-analysis-phase-2.py`

**Purpose:**
The successful execution provides valuable insights that warrant deeper exploration. Here's the comprehensive analysis of current results and next steps:

1. Current State Assessment:
   - Cluster analysis successfully identified 4 distinct performance groups:
     * Cluster 0: Low Performers (BA .140, OPS .357)
     * Cluster 1: Power Hitters (HR 0.81, RBI 3.67)
     * Cluster 2: Balanced Hitters (OPS .749)
     * Cluster 3: Elite Performers (OPS 1.109, RBI 6.93)
   - Temporal trends visualizat

---

### Step 8: Cluster Analysis (Phase 3)

**Inputs:** `analyzed_manager.csv`, `analyzed_batting.csv`
**Outputs:** `model_interpretation.csv`
**Script:** `scripts/step_08_cluster-analysis-phase-3.py`

**Purpose:**
The successful execution reveals several valuable insights that can be further expanded upon. Here's a detailed analysis of the current state and opportunities for deeper investigation:

1. Current Findings Assessment:
   - Award prediction model shows strong performance (93% accuracy)
   - Feature importance reveals nearly equal weighting between vote_pct and normalized_points
   - Temporal cluster trends visualization captures historical patterns
   - Time series decomposition shows interestin

---

### Step 9: Model Training & Prediction

**Inputs:** `analyzed_manager.csv`, `analyzed_batting.csv`
**Outputs:** `model_interpretation.csv`
**Script:** `scripts/step_09_model-training-prediction.py`

**Purpose:**
The error encountered reveals a critical oversight in the code implementation. Here's the detailed analysis:

1. Error Diagnosis:
   - NameError indicates 'RandomForestClassifier' is not defined
   - Root cause: Missing import statement for RandomForestClassifier from sklearn.ensemble
   - Impact: Prevents model instantiation and all subsequent analysis

2. Code Structure Assessment:
   - Current imports include other sklearn components but not RandomForestClassifier
   - SHAP analysis depends o

---

### Step 10: Model Training & Prediction (Phase 2)

**Inputs:** `analyzed_manager.csv`
**Outputs:** `enhanced_features.csv`
**Script:** `scripts/step_10_model-training-prediction-phase-2.py`

**Purpose:**
The successful execution provides a solid foundation for deeper analysis. Here's a comprehensive examination of the current results and opportunities for further investigation:

1. Current Findings Assessment:
   - Both Random Forest and Gradient Boosting models show strong performance (~89% accuracy)
   - Feature importance reveals nearly identical weighting between normalized_points and vote_pct
   - SHAP values confirm consistent feature importance across different interpretation methods
   -

---

### Step 11: Error Recovery & Robust Loading

**Inputs:** `analyzed_manager.csv`
**Outputs:** `enhanced_features.csv`, `league_performance.csv`
**Script:** `scripts/step_11_error-recovery-robust-loading.py`

**Purpose:**
The error indicates a missing import for RandomForestClassifier, despite it being included in previous code blocks. This suggests either:

1. Execution Context Issue:
   - The code may be running in an environment where previous imports aren't preserved
   - The analysis functions may be executing in isolated contexts

2. Code Structure Problem:
   - Import statements may not be properly scoped
   - Function dependencies may not be properly managed

3. Solution Strategy:
   - Ensure all required

---

### Step 12: Error Recovery & Robust Loading (Phase 2)

**Inputs:** `analyzed_manager.csv`
**Outputs:** `enhanced_features.csv`, `league_performance.csv`
**Script:** `scripts/step_12_error-recovery-robust-loading-phase-2.py`

**Purpose:**
The persistent error indicates a fundamental scoping issue with the RandomForestClassifier import that requires careful resolution. This situation calls for a comprehensive analysis of the execution environment and code structure:

1. Error Root Cause:
- The error suggests the import statement exists but isn't properly scoped within the function context
- Python's variable scoping rules are causing the imported class to be unavailable when needed
- The try-except block may be interfering with pr

---

### Step 13: Model Training & Prediction (Phase 3)

**Inputs:** `analyzed_manager.csv`
**Outputs:** `league_performance.csv`
**Script:** `scripts/step_13_model-training-prediction-phase-3.py`

**Purpose:**
The error reveals a critical data type mismatch in our modeling pipeline that requires systematic resolution. Here's a comprehensive analysis:

1. Error Diagnosis:
- ValueError indicates failure to convert 'AL' (string) to float
- Root cause: League_id categorical variable included in numeric feature matrix
- Impact: All model fits fail due to incompatible data types

2. Data Flow Analysis:
- Original data contains mixed numeric and categorical features
- PolynomialFeatures creates numeric inter

---

### Step 14: Error Recovery & Robust Loading (Phase 3)

**Inputs:** `analyzed_manager.csv`
**Outputs:** `league_performance.csv`
**Script:** `scripts/step_14_error-recovery-robust-loading-phase-3.py`

**Purpose:**
The error indicates a missing import for the 'sys' module, which was referenced in the error handling but not properly imported. This reveals several important considerations:

1. Error Context:
- The NameError occurs when trying to use sys.stderr without importing sys
- The error appears in the exception handling path
- Impacts the error reporting functionality but not core analysis

2. Code Structure Issues:
- Inconsistent import management across code blocks
- Missing critical imports for err

---


## Final Output & Deliverables

# Comprehensive Analysis of Postseason Batting Performance and Manager Award Voting Patterns in Major League Baseball

## Introduction and Research Context

The analysis of postseason batting performance and manager award voting patterns in Major League Baseball (MLB) provides valuable insights into the complex dynamics of professional baseball. This comprehensive study examines two critical datasets: postseason batting statistics spanning from 1884 to 2015, and manager award voting records from 1983 to 2015. The research combines advanced statistical modeling, temporal trend analysis, and machine learning techniques to uncover patterns and relationships that illuminate the factors contributing to postseason success and managerial recognition. The temporal validation accuracy of 0.875 (±0.050) and stacking model accuracy of 0.903 (±0.025) demonstrate the robustness of our analytical approach, while the league-specific analysis reveals subtle but important differences between the American League (AL) and National League (NL) with mean accuracies of 0.897 and 0.891 respectively.

The methodology employed in this research incorporates multiple analytical dimensions, including feature engineering, temporal validation, and ensemble modeling. By preprocessing the data to properly handle mixed numeric and categorical features through polynomial feature generation and one-hot encoding, we ensure the integrity of our modeling pipeline. The league performance analysis, based on sample sizes of 213 (AL) and 201 (NL) observations, provides statistically significant insights into the predictive patterns across different baseball leagues. Our approach addresses several challenges in sports analytics, including handling missing data (approximately 10.68% in some batting metrics), managing class imbalance in award outcomes, and interpreting complex feature interactions.

The significance of this research extends beyond academic interest, offering practical applications for team management, player evaluation, and award forecasting. The temporal validation framework, utilizing TimeSeriesSplit with 5 splits, captures the evolving nature of baseball performance metrics over time. The stacking ensemble model, combining Random Forest and Gradient Boosting classifiers with a Logistic Regression meta-learner, demonstrates superior predictive performance compared to individual models. These methodological innovations contribute to the growing body of sabermetrics research while providing new tools for baseball analysts and decision-makers.

## Data Preparation and Feature Engineering

The initial data preparation phase involved comprehensive cleaning and transformation of both batting and manager award datasets. For the postseason batting data, we addressed missing values through median imputation for continuous variables and mode imputation for categorical variables, ensuring minimal distortion of the underlying distributions. The batting dataset, containing 11,690 reco


---

## How to Run

### Local Execution
```bash
# Install dependencies
pip install pandas openpyxl

# Run each step sequentially
cd case_5145_12658
python scripts/step_01_load_profile.py     --driver_xlsx data/driver.xlsx     --school_bus_json data/school_bus.json

python scripts/step_02_clean_standardize.py     --initial_driver_sample_csv initial_driver_sample.csv     --initial_school_bus_sample_csv initial_school_bus_sample.csv     --cleaned_driver_data_csv cleaned_driver_data.csv     --cleaned_school_bus_data_csv cleaned_school_bus_data.csv

python scripts/step_03_normalize_resolve.py     --cleaned_driver_data_csv cleaned_driver_data.csv     --cleaned_school_bus_data_csv cleaned_school_bus_data.csv     --final_driver_data_csv final_driver_data.csv     --final_school_bus_data_csv final_school_bus_data.csv     --data_quality_report_json data_quality_report.json
```

### Argo Workflow
```bash
# Submit to Argo Workflows cluster
argo submit pipeline.yaml

# Monitor
argo watch @latest
argo logs @latest
```
