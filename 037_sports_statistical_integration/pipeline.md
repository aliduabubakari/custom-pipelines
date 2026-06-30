# Pipeline: Data Cleaning & Validation Workflow

## Metadata
| Field | Value |
|---|---|
| **Case ID** | `5098` |
| **Difficulty** | N/A/5 |
| **Quality** | N/A/5 |
| **Abilities** |  |
| **Total Steps** | 14 |
| **Input Files** | 0 |
| **Output Files** | 0 |

---

## Executive Summary

This comprehensive study examines the relationship between All-Star player selections and team performance metrics in Major League Baseball (MLB) from historical data spanning multiple decades. Through rigorous statistical analysis and machine learning techniques, we uncover significant patterns and predictive relationships that illuminate how individual player recognition correlates with team success. The analysis incorporates 1,889 team-seasons of data, featuring 5 key performance metrics, and achieves 71.7% accuracy in predicting championship outcomes. Our methodology combines traditional statistical approaches with advanced machine learning techniques, including Random Forest classification and SHAP value interpretation, to provide both predictive power and explanatory insights into the complex dynamics of baseball team performance.

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

### Step 1: Data Loading & Profiling

**Inputs:** `all_star.csv`, `team.csv`
**Outputs:** Console output only
**Script:** `scripts/step_01_data-loading-profiling.py`

**Purpose:**
To begin this comprehensive data analysis project, I will first need to understand the structure and content of both datasets (all_star.csv and team.csv). The analysis will proceed through several logical phases:

1. Initial Data Exploration:
   - Load and examine both datasets
   - Check basic statistics, data types, and missing values
   - Identify key variables and potential relationships between datasets

2. Data Cleaning and Preparation:
   - Handle missing values and inconsistencies
   - S

---

### Step 2: Statistical Analysis & Hypothesis Testing

**Inputs:** None (reads raw data)
**Outputs:** `position_distribution_by_decade.csv`, `merged_team_all_star_data.csv`
**Script:** `scripts/step_02_statistical-analysis-hypothesis-testing.py`

**Purpose:**
Next steps for deeper analysis:

1. Data Cleaning and Enhancement:
   - Handle missing values in starting_pos by imputing or creating position categories
   - Create decade-based time periods for trend analysis
   - Calculate derived metrics like win percentage for teams

2. Temporal Analysis:
   - Examine how all-star selections per team vary by decade
   - Analyze changes in positional distribution over time
   - Compare with team performance trends

3. Team Performance Correlation:
   - Creat

---

### Step 3: Data Loading & Profiling (Phase 2)

**Inputs:** `all_star.csv`, `team.csv`
**Outputs:** `position_distribution_by_decade.csv`, `merged_team_all_star_data.csv`
**Script:** `scripts/step_03_data-loading-profiling-phase-2.py`

**Purpose:**
To fix this issue and ensure robust analysis, we need to:

1. Reload the datasets at the beginning of the analysis code
2. Maintain consistent variable naming throughout
3. Consider adding error handling for file loading
4. Structure the code to be self-contained and executable independently

The corrected approach should:
- Explicitly load both datasets first
- Verify successful loading before proceeding
- Include all necessary imports
- Maintain the original analysis logic while ensuring prope

---

### Step 4: Data Merging & Integration

**Inputs:** `all_star.csv`, `team.csv`
**Outputs:** `position_distribution_by_decade.csv`, `merged_team_all_star_data.csv`
**Script:** `scripts/step_04_data-merging-integration.py`

**Purpose:**
To resolve this issue and improve the analysis, we should:

1. Ensure the 'decade' column is properly propagated through all merge operations
2. Verify all required columns exist before visualization attempts
3. Add data validation checks before plotting
4. Consider restructuring the merge operations to maintain all relevant columns
5. Add more informative error handling for data validation

The corrected approach should:
- Explicitly include 'decade' in all relevant merge operations
- Add valid

---

### Step 5: Statistical Analysis & Hypothesis Testing (Phase 2)

**Inputs:** `position_distribution_by_decade.csv`, `merged_team_all_star_data.csv`
**Outputs:** `enhanced_team_all_star_data.csv`
**Script:** `scripts/step_05_statistical-analysis-hypothesis-testing-.py`

**Purpose:**
Next steps for deeper analysis:

1. Advanced Statistical Analysis:
   - Regression modeling to predict wins from all-star counts
   - Hypothesis testing for differences between championship/non-championship teams
   - Time series decomposition of all-star trends

2. Enhanced Visualizations:
   - Interactive plots for exploring team trajectories
   - Small multiples by position over time
   - Geospatial mapping of team performance

3. Feature Engineering:
   - Create lagged variables for time-bas

---

### Step 6: Error Recovery & Robust Loading

**Inputs:** `position_distribution_by_decade.csv`, `merged_team_all_star_data.csv`, `team.csv`
**Outputs:** `enhanced_team_all_star_data.csv`
**Script:** `scripts/step_06_error-recovery-robust-loading.py`

**Purpose:**
To resolve this issue and ensure robust execution, we should:

1. Restructure the code to include all necessary imports at the beginning
2. Verify all required modules are imported before any operations
3. Maintain consistent import practices throughout the script
4. Consider adding import error handling
5. Ensure the code is self-contained and executable independently

The corrected approach should:
- Group all imports at the top of the script
- Include all required modules (pandas, numpy, matp

---

### Step 7: Cluster Analysis

**Inputs:** `enhanced_team_all_star_data.csv`
**Outputs:** `final_analysis_data.csv`
**Script:** `scripts/step_07_cluster-analysis.py`

**Purpose:**
Next steps for deeper analysis:

1. Model Enhancement:
   - Feature importance analysis for championship prediction
   - Cross-validation of model performance
   - Alternative model architectures (random forest, gradient boosting)

2. Cluster Interpretation:
   - Profile analysis of team clusters
   - Historical trends in cluster membership
   - Performance characteristics by cluster

3. Advanced Time Series:
   - ARIMA modeling of all-star trends
   - Change point detection in historical patter

---

### Step 8: Error Recovery & Robust Loading (Phase 2)

**Inputs:** `all_star.csv`, `enhanced_team_all_star_data.csv`, `team.csv`
**Outputs:** `final_analysis_data.csv`
**Script:** `scripts/step_08_error-recovery-robust-loading-phase-2.py`

**Purpose:**
To resolve this issue comprehensively and prevent future occurrences, we should:

1. Implement a centralized import management system
2. Add explicit import verification checks
3. Include error handling for missing dependencies
4. Maintain import consistency across all code segments
5. Document all dependencies clearly

The corrected approach will:
- Group all imports in a dedicated section at the start
- Verify essential imports before execution
- Provide meaningful error messages
- Maintain al

---

### Step 9: Data Cleaning & Standardization

**Inputs:** None (reads raw data)
**Outputs:** `final_analysis_data_clean.csv`
**Script:** `scripts/step_09_data-cleaning-standardization.py`

**Purpose:**
To resolve this issue and improve data handling, we should:

1. Separate numeric and non-numeric columns during cleaning
2. Implement type-specific missing value imputation
3. Add data type validation before statistical operations
4. Preserve categorical variables while cleaning numeric data
5. Implement more robust data preprocessing

The corrected approach will:
- Identify numeric columns explicitly
- Handle missing values separately for numeric and non-numeric data
- Maintain original data st

---

### Step 10: Data Validation & Quality Report

**Inputs:** None (reads raw data)
**Outputs:** `final_analysis_data_clean.csv`
**Script:** `scripts/step_10_data-validation-quality-report.py`

**Purpose:**
To create a robust, self-contained analysis script, we need to:

1. Ensure all required data is loaded at the start
2. Implement proper error handling for file operations
3. Maintain a clear data loading and validation workflow
4. Structure the code to be execution-independent
5. Include verification steps for loaded data

The corrected approach will:
- Explicitly load all required data files
- Add validation checks for successful loading
- Implement proper error handling
- Maintain analysis fun

---

### Step 11: Data Visualization

**Inputs:** `optimized_model.pkl`
**Outputs:** `optimized_model.pkl`, `final_enhanced_data.csv`
**Script:** `scripts/step_11_data-visualization.py`

**Purpose:**
Next steps for deeper analysis:

1. Model Interpretation:
   - SHAP values for feature importance explanation
   - Partial dependence plots
   - Decision tree visualization

2. Performance Enhancement:
   - Hyperparameter tuning
   - Feature engineering experiments
   - Ensemble methods

3. Advanced Visualization:
   - Interactive model explanation dashboards
   - Time-series decomposition of key metrics
   - Geospatial team performance mapping

4. Deployment Preparation:
   - Model serializatio

---

### Step 12: Model Training & Prediction

**Inputs:** `final_model.pkl`
**Outputs:** `feature_analysis.csv`, `model_metadata.csv`, `final_model.pkl`
**Script:** `scripts/step_12_model-training-prediction.py`

**Purpose:**
To create a robust, end-to-end analysis pipeline, we need to:

1. Implement proper model persistence
2. Maintain state between analysis segments
3. Add model validation checks
4. Include proper error handling
5. Document model parameters

The corrected approach will:
- Initialize models in a dedicated section
- Validate model objects before use
- Include proper error handling
- Maintain all analysis functionality
- Ensure reproducibility

---

### Step 13: Data Validation & Quality Report (Phase 2)

**Inputs:** `enhanced_team_all_star_data.csv`, `final_model.pkl`
**Outputs:** `feature_analysis.csv`, `final_model.pkl`
**Script:** `scripts/step_13_data-validation-quality-report-phase-2.py`

**Purpose:**
To create a fully self-contained and robust analysis script, we need to:

1. Implement complete data loading and preprocessing
2. Explicitly define feature and target variables
3. Maintain proper variable scoping
4. Include validation checks for all critical variables
5. Structure the code as an end-to-end pipeline

The corrected approach will:
- Load all required data at the start
- Perform necessary preprocessing
- Explicitly define X and y
- Include validation checks
- Maintain all analysis f

---

### Step 14: Data Validation & Quality Report (Phase 3)

**Inputs:** `enhanced_team_all_star_data.csv`, `final_model.pkl`
**Outputs:** `shap_feature_importance.csv`, `feature_analysis.csv`, `final_model.pkl`
**Script:** `scripts/step_14_data-validation-quality-report-phase-3.py`

**Purpose:**
To resolve this issue and ensure robust SHAP analysis, we need to:

1. Properly handle SHAP values for binary classification
2. Validate SHAP values dimensions before processing
3. Implement more flexible feature importance calculation
4. Add error handling for SHAP analysis
5. Maintain compatibility with different SHAP versions

The corrected approach will:
- Check SHAP values structure before processing
- Handle both binary and multi-class cases
- Include validation checks
- Maintain all analy

---


## Final Output & Deliverables

# Comprehensive Analysis of All-Star Players and Team Performance in Major League Baseball

## Executive Summary

This comprehensive study examines the relationship between All-Star player selections and team performance metrics in Major League Baseball (MLB) from historical data spanning multiple decades. Through rigorous statistical analysis and machine learning techniques, we uncover significant patterns and predictive relationships that illuminate how individual player recognition correlates with team success. The analysis incorporates 1,889 team-seasons of data, featuring 5 key performance metrics, and achieves 71.7% accuracy in predicting championship outcomes. Our methodology combines traditional statistical approaches with advanced machine learning techniques, including Random Forest classification and SHAP value interpretation, to provide both predictive power and explanatory insights into the complex dynamics of baseball team performance.

## Data Sources and Preparation

The study utilizes two primary datasets: the All-Star player records and comprehensive team statistics. The All-Star dataset contains 5,069 entries spanning from 1933 to 2015, documenting individual player selections with associated team affiliations and positional information. The team statistics dataset comprises 2,805 team-season records from 1871 to 2015, featuring 48 distinct performance metrics ranging from basic win-loss records to advanced sabermetric measurements. Through an extensive data cleaning and feature engineering process, we merged these datasets to create an enhanced analytical framework that connects individual player recognition with team outcomes.

Data preprocessing involved several critical steps to ensure analytical validity. Missing value imputation was performed using median values for continuous variables and mode for categorical variables. We created derived metrics such as win percentage (calculated as wins divided by total games played) and standardized all numerical features to comparable scales. Temporal variables were binned into decade-long periods to facilitate longitudinal analysis while maintaining sufficient sample sizes within each period. The final analytical dataset contains complete records for all 1,889 team-seasons in the modern era (post-1960), with no missing values in the key predictive features.

## Key Statistical Findings

Our analysis reveals several statistically significant relationships between All-Star representation and team performance. The Random Forest classifier achieved a mean cross-validation accuracy of 71.7% in predicting championship outcomes, with individual fold accuracies ranging from 66.9% to 77.8%. Feature importance analysis shows that attendance (SHAP mean absolute value = 0.067) and All-Star count (0.066) emerge as the most impactful predictors, followed closely by win percentage (0.063) and ERA (0.056). Interestingly, raw win totals showed relatively lower predictive importance (0.036), suggesti


---

## How to Run

### Local Execution
```bash
# Install dependencies
pip install pandas openpyxl

# Run each step sequentially
cd case_5098_12534
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
