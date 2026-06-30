# Pipeline: Data Cleaning & Validation Workflow

## Metadata
| Field | Value |
|---|---|
| **Case ID** | `5516` |
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

### Step 1: Data Loading & Profiling

**Inputs:** `appearances.csv`, `postseason.csv`
**Outputs:** `appearances_sample.csv`, `postseason_sample.csv`
**Script:** `scripts/step_01_data-loading-profiling.py`

**Purpose:**
To begin this comprehensive data science report, I'll first need to understand the structure and content of both datasets. The analysis will proceed through several key phases:

1. Data Inspection and Cleaning:
   - First examine the structure of appearances.csv (5.7MB) and postseason.csv (8.9KB)
   - Check for missing values, data types, and basic statistics
   - Handle any data quality issues (missing values, inconsistencies)
   - Filter for modern era (post-2000) while preserving pre-1950 dat

---

### Step 2: Data Cleaning & Standardization

**Inputs:** None (reads raw data)
**Outputs:** `postseason_clean.csv`, `team_position_metrics.csv`, `appearances_clean.csv`
**Script:** `scripts/step_02_data-cleaning-standardization.py`

**Purpose:**
Next steps for deeper analysis:

1. Data Cleaning:
- Handle missing values in gs, g_dh, g_ph, g_pr
- Verify and potentially impute g_all and g_defense missing values
- Filter for modern era while preserving pre-1950 data

2. Feature Engineering:
- Calculate positional versatility metrics:
  * Count of positions played (non-zero g_* columns)
  * Positional diversity index
- Create role classifications:
  * Primary position for each player
  * Offensive/defensive specialization
- Compute team-leve

---

### Step 3: Data Validation & Quality Report

**Inputs:** `appearances.csv`, `postseason.csv`
**Outputs:** `postseason_clean.csv`, `team_position_metrics.csv`, `appearances_clean.csv`
**Script:** `scripts/step_03_data-validation-quality-report.py`

**Purpose:**
To address this issue and ensure continuity in our analysis, we need to:

1. Restructure the code to maintain data continuity:
   - Reload the original data files at the start of each execution
   - Ensure all necessary preprocessing steps are included
   - Maintain consistent variable naming

2. Implement defensive programming:
   - Verify data existence before operations
   - Include error handling for file operations
   - Validate data structures before processing

3. Improve code organizatio

---

### Step 4: Data Merging & Integration

**Inputs:** `postseason_clean.csv`, `team_position_metrics.csv`
**Outputs:** `full_analysis_dataset.csv`
**Script:** `scripts/step_04_data-merging-integration.py`

**Purpose:**
Next steps for comprehensive analysis:

1. Data Integration:
- Merge team_position metrics with postseason outcomes
- Create unified analysis dataset with:
  * Team composition metrics
  * Postseason participation flags
  * Postseason performance metrics

2. Comparative Analysis:
- Contrast modern era (post-2000) with historical patterns
- Identify significant changes in successful team compositions

3. Advanced Visualizations:
- Heatmaps of successful team positional distributions
- Time-series

---

### Step 5: Error Recovery & Robust Loading

**Inputs:** `postseason_clean.csv`, `team_position_metrics.csv`
**Outputs:** `full_analysis_dataset.csv`
**Script:** `scripts/step_05_error-recovery-robust-loading.py`

**Purpose:**
To ensure reliable execution, we need to:

1. Restructure the code to be self-contained:
   - Include all necessary imports at the start of each executable block
   - Verify all required modules are available
   - Maintain functional independence between code blocks

2. Implement robust initialization:
   - Import all required libraries upfront
   - Include error handling for missing imports
   - Verify file existence before operations

3. Maintain analysis continuity:
   - Preserve all planned 

---

### Step 6: Regression Modeling

**Inputs:** None (reads raw data)
**Outputs:** `postseason_feature_importance.csv`, `modeling_dataset.csv`
**Script:** `scripts/step_06_regression-modeling.py`

**Purpose:**
Next steps for advanced analysis:

1. Statistical Modeling:
- Build logistic regression models predicting postseason qualification
- Develop ordinal regression for series win counts
- Implement feature importance analysis

2. Comparative Analysis:
- Contrast championship team compositions across eras
- Analyze trends in positional specialization over time

3. Strategic Insights:
- Identify optimal position distributions for postseason success
- Quantify value of player versatility
- Develop team

---

### Step 7: Model Training & Prediction

**Inputs:** `full_analysis_dataset.csv`
**Outputs:** `model_feature_importance.csv`
**Script:** `scripts/step_07_model-training-prediction.py`

**Purpose:**
To ensure robust execution, we need to:

1. Restructure the modeling code to:
   - Load all required data from saved files
   - Maintain identical feature engineering steps
   - Preserve all analysis components

2. Enhance reproducibility:
   - Explicitly load intermediate datasets
   - Verify data consistency
   - Include all necessary preprocessing

3. Maintain analysis continuity:
   - Keep the same modeling approach
   - Preserve feature selection
   - Ensure consistent evaluation metrics

T

---

### Step 8: Data Visualization

**Inputs:** None (reads raw data)
**Outputs:** Console output only
**Script:** `scripts/step_08_data-visualization.py`

**Purpose:**
Next steps for deeper insights:

1. Model Enhancement:
- Address class imbalance with advanced techniques (SMOTE, class weights)
- Try ensemble methods (Random Forest, XGBoost) for better performance
- Include interaction terms between positions

2. Strategic Analysis:
- Investigate why versatility negatively impacts postseason chances
- Analyze optimal position distributions for each era
- Study catcher role evolution across eras

3. Advanced Visualization:
- Create era-comparison radar charts 

---

### Step 9: Model Training & Prediction (Phase 2)

**Inputs:** `full_analysis_dataset.csv`
**Outputs:** Console output only
**Script:** `scripts/step_09_model-training-prediction-phase-2.py`

**Purpose:**
To ensure robust and reproducible analysis, we need to:

1. Restructure the code to be fully self-contained:
   - Include all data loading and preprocessing steps
   - Maintain consistent feature engineering
   - Preserve the full modeling pipeline

2. Implement comprehensive data flow:
   - Load raw data from files
   - Recreate all preprocessing steps
   - Verify intermediate outputs

3. Enhance model robustness:
   - Include proper train-test splitting
   - Maintain feature scaling
   - Handl

---

### Step 10: Data Visualization (Phase 2)

**Inputs:** `full_analysis_dataset.csv`
**Outputs:** Console output only
**Script:** `scripts/step_10_data-visualization-phase-2.py`

**Purpose:**
To resolve this issue and ensure robust visualization, we need to:

1. Maintain consistent feature naming:
   - Preserve feature names through scaling operations
   - Verify feature name integrity at each step
   - Ensure proper mapping between numpy arrays and feature names

2. Improve visualization robustness:
   - Validate feature existence before plotting
   - Handle feature name conversions explicitly
   - Add error checking for visualization steps

3. Enhance code structure:
   - Separate 

---

### Step 11: Model Training & Prediction (Phase 3)

**Inputs:** None (reads raw data)
**Outputs:** Console output only
**Script:** `scripts/step_11_model-training-prediction-phase-3.py`

**Purpose:**
Next steps for deeper insights:

1. Model Interpretation:
- Analyze why pitcher percentage is most predictive
- Investigate the relationship between defensive specialization and success
- Examine feature interaction effects

2. Strategic Recommendations:
- Develop optimal position allocation guidelines
- Quantify tradeoffs between pitcher usage and other positions
- Create era-specific roster construction strategies

3. Advanced Techniques:
- Implement SHAP values for better feature interpretati

---

### Step 12: Cluster Analysis

**Inputs:** `full_analysis_dataset.csv`
**Outputs:** `final_analysis_dataset.csv`
**Script:** `scripts/step_12_cluster-analysis.py`

**Purpose:**
To resolve this issue and enable comprehensive model interpretation, we need to:

1. Restructure the code to maintain model continuity:
   - Include model training within the same execution block as interpretation
   - Preserve all model artifacts needed for analysis
   - Verify model availability before interpretation steps

2. Enhance model interpretability:
   - Implement SHAP values for feature importance
   - Include partial dependence plots
   - Add cluster analysis of position distributio

---

### Step 13: Data Visualization (Phase 3)

**Inputs:** `full_analysis_dataset.csv`
**Outputs:** `final_analysis_dataset.csv`
**Script:** `scripts/step_13_data-visualization-phase-3.py`

**Purpose:**
To resolve this issue and enable proper SHAP analysis, we need to:

1. Correct SHAP value handling:
   - Explicitly specify which class probabilities to explain
   - Verify matrix dimensions before plotting
   - Handle binary classification outputs appropriately

2. Enhance model interpretation:
   - Include both global and local explanation methods
   - Add feature interaction analysis
   - Incorporate decision plot visualization

3. Maintain analysis integrity:
   - Preserve all previous analy

---

### Step 14: Cluster Analysis (Phase 2)

**Inputs:** `full_analysis_dataset.csv`
**Outputs:** `final_analysis_dataset.csv`
**Script:** `scripts/step_14_cluster-analysis-phase-2.py`

**Purpose:**
To resolve this issue while maintaining comprehensive model interpretation, we will:

1. Adjust visualization strategy:
   - Generate force plots for single observations only
   - Use alternative explanation methods for global patterns
   - Maintain all other analytical components

2. Enhance interpretability:
   - Focus on representative individual predictions
   - Include decision plots as alternatives
   - Preserve cluster analysis and feature importance

3. Ensure robust output:
   - Validat

---


## Final Output & Deliverables

# The Relationship Between Regular Season Player Appearances and Postseason Success in Modern Baseball

## Introduction and Background

The analysis of baseball performance metrics has evolved significantly in the sabermetrics era, with increasing attention paid to the relationship between regular season player deployment and postseason outcomes. This comprehensive study examines 100,951 player appearances from 1871 to 2015, focusing particularly on the modern era (post-2000) while maintaining comparative analysis with pre-1950 trends. The dataset captures detailed positional information through various metrics including games played by position (g_p, g_c, g_1b, etc.), defensive appearances (g_defense), and batting appearances (g_batting), providing a rich foundation for understanding how roster construction and player utilization correlate with postseason success.

Methodologically, this investigation employs advanced machine learning techniques including Random Forest classification and SHAP value interpretation, complemented by traditional statistical analysis. The modeling approach achieved a 62% accuracy rate with ROC AUC of 0.637 in predicting postseason qualification based on positional deployment patterns, demonstrating significant predictive power. Particularly noteworthy is the model's ability to identify subtle patterns in position specialization that correlate with postseason success, while controlling for era-specific trends in baseball strategy and roster construction.

The analytical framework was designed to address several key research questions: How does positional versatility impact postseason success? What are the optimal position distributions for championship-caliber teams? How have these relationships evolved across different eras of baseball? To answer these questions, the study incorporates multiple analytical perspectives including cluster analysis of team composition, era-specific comparisons, and predictive modeling of postseason outcomes based on regular season deployment patterns.

## Key Findings and Positional Analysis

The analysis reveals several compelling relationships between regular season position deployment and postseason success. Pitcher usage (g_p_pct) emerges as the most significant predictor of postseason qualification with an importance score of 0.165 in the Random Forest model, followed by catcher percentage (g_c_pct) at 0.147 and center field percentage (g_cf_pct) at 0.137. These findings suggest that defensive specialization, particularly in key defensive positions, correlates strongly with postseason success. The SHAP summary plot (see Figure 1) demonstrates that higher values of g_p_pct consistently push model predictions toward higher probabilities of postseason qualification, while g_c_pct shows a more complex nonlinear relationship with postseason outcomes.

Positional versatility, as measured by the position_count metric, shows a counterintuitive negative relationship with postseason success. 


---

## How to Run

### Local Execution
```bash
# Install dependencies
pip install pandas openpyxl

# Run each step sequentially
cd case_5516_13580
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
