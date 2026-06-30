# Pipeline: Data Cleaning & Validation Workflow

## Metadata
| Field | Value |
|---|---|
| **Case ID** | `4779` |
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

### Step 1: Data Cleaning & Standardization

**Inputs:** `batting.csv`, `hall_of_fame.csv`
**Outputs:** Console output only
**Script:** `scripts/step_01_data-cleaning-standardization.py`

**Purpose:**
This task requires a comprehensive analysis of the relationship between baseball player batting statistics and Hall of Fame induction outcomes. To approach this systematically, I'll need to:

1. First understand both datasets individually:
   - batting.csv likely contains player batting statistics (hits, home runs, batting average etc.)
   - hall_of_fame.csv contains induction records with player IDs and induction status

2. Key analytical steps needed:
   - Data inspection and cleaning for both

---

### Step 2: Data Merging & Integration

**Inputs:** None (reads raw data)
**Outputs:** `processed_career_stats.csv`
**Script:** `scripts/step_02_data-merging-integration.py`

**Purpose:**
Next steps needed for deeper analysis:

1. Data Preparation:
   - Aggregate batting stats to career totals per player
   - Filter HOF data to only successful inductions
   - Create clean merged dataset with career stats + HOF status

2. Feature Engineering:
   - Calculate advanced metrics (BA, OBP, SLG, OPS)
   - Create longevity metrics (years played, total games)
   - Consider era adjustments for historical comparisons

3. Exploratory Analysis:
   - Compare distributions of key stats between H

---

### Step 3: Data Validation & Quality Report

**Inputs:** `batting.csv`, `hall_of_fame.csv`
**Outputs:** `processed_career_stats.csv`
**Script:** `scripts/step_03_data-validation-quality-report.py`

**Purpose:**
To fix this issue and continue the analysis, we need to:

1. Reload both datasets at the start of the code
2. Verify successful loading before proceeding
3. Maintain all the planned analysis steps from the previous code
4. Add error checking for data loading

The corrected approach should:
- First load both CSV files
- Check they loaded properly
- Then proceed with all aggregation and analysis steps
- Include print statements to verify each step

We should also add some basic data validation to 

---

### Step 4: Statistical Analysis & Hypothesis Testing

**Inputs:** `processed_career_stats.csv`
**Outputs:** Console output only
**Script:** `scripts/step_04_statistical-analysis-hypothesis-testing.py`

**Purpose:**
Next steps for deeper analysis:

1. Statistical Testing:
   - Conduct t-tests to verify significance of differences
   - Calculate effect sizes to quantify magnitude of differences
   - Examine potential interaction effects between metrics

2. Advanced Visualization:
   - Create density plots comparing key metrics
   - Generate scatter matrix of important variables
   - Plot cumulative distribution functions

3. Predictive Modeling:
   - Prepare data for classification modeling
   - Identify pot

---

### Step 5: Model Training & Prediction

**Inputs:** `processed_career_stats.csv`
**Outputs:** Console output only
**Script:** `scripts/step_05_model-training-prediction.py`

**Purpose:**
Next steps for deeper investigation:

1. Data Quality Check:
   - Investigate NaN p-values indicating perfect separation
   - Examine potential data partitioning issues

2. Advanced Modeling:
   - Build predictive model for HOF induction
   - Feature selection from significant variables
   - Address class imbalance (few HOF players)

3. Era Adjustment:
   - Consider normalizing stats across different eras
   - Account for historical changes in baseball

4. Additional Analysis:
   - Examine inter

---

### Step 6: Data Visualization

**Inputs:** `processed_career_stats.csv`
**Outputs:** Console output only
**Script:** `scripts/step_06_data-visualization.py`

**Purpose:**
Next steps to improve analysis:

1. Address Class Imbalance:
   - Implement resampling techniques
   - Use class weights in model
   - Try alternative evaluation metrics

2. Model Enhancement:
   - Experiment with different algorithms
   - Add feature engineering (peak performance)
   - Include position information if available

3. Advanced Interpretation:
   - Generate SHAP values for explainability
   - Create partial dependence plots
   - Examine decision thresholds

4. Era-Specific Analysis:

---

### Step 7: Model Training & Prediction (Phase 2)

**Inputs:** `processed_career_stats.csv`
**Outputs:** Console output only
**Script:** `scripts/step_07_model-training-prediction-phase-2.py`

**Purpose:**
Required improvements to address this:

1. Data Cleaning:
   - Identify and handle NaN values
   - Consider appropriate imputation strategies
   - May need to filter certain records

2. Alternative Approaches:
   - Use different resampling method
   - Try class weighting instead of SMOTE
   - Consider model-based imputation

3. Robust Implementation:
   - Add data validation checks
   - Create preprocessing pipeline
   - Document handling of edge cases

Immediate priorities:
1. Clean NaN values 

---

### Step 8: Data Visualization (Phase 2)

**Inputs:** `processed_career_stats.csv`
**Outputs:** Console output only
**Script:** `scripts/step_08_data-visualization-phase-2.py`

**Purpose:**
Required improvements to fix this:

1. Data Handling:
   - Preserve feature names through scaling
   - Ensure consistent data types for SHAP
   - Verify array shapes match

2. Visualization Robustness:
   - Create intermediate DataFrame with proper columns
   - Check shapes before plotting
   - Add validation steps

3. Alternative Approaches:
   - Use unscaled data for SHAP (with proper warnings)
   - Reconstruct DataFrame after scaling
   - Try different SHAP plot types

Immediate priorities:
1

---

### Step 9: Data Visualization (Phase 3)

**Inputs:** `processed_career_stats.csv`
**Outputs:** `shap_values.csv`
**Script:** `scripts/step_09_data-visualization-phase-3.py`

**Purpose:**
Required solutions and next steps:

1. SHAP Implementation Fix:
   - Explicitly specify binary classification
   - Use proper SHAP value indexing
   - Verify array shapes at each step

2. Alternative Approaches:
   - Use KernelExplainer instead of TreeExplainer
   - Try individual force plots
   - Consider permutation importance

3. Validation Enhancements:
   - Add shape verification prints
   - Check SHAP values before plotting
   - Test with smaller subset first

Immediate priorities:
1. Fix 

---

### Step 10: Data Visualization (Phase 4)

**Inputs:** `processed_career_stats.csv`
**Outputs:** `shap_analysis_results.csv`
**Script:** `scripts/step_10_data-visualization-phase-4.py`

**Purpose:**
Required solutions and next steps:

1. SHAP Value Handling:
   - Properly extract class-specific SHAP values
   - Reshape arrays correctly for analysis
   - Consider alternative SHAP visualization methods

2. Data Management:
   - Verify SHAP array dimensions
   - Create proper DataFrame structure
   - Maintain connection to original samples

3. Alternative Approaches:
   - Use SHAP's built-in visualization
   - Try individual sample explanations
   - Consider permutation importance

Immediate p

---

### Step 11: Data Visualization (Phase 5)

**Inputs:** `processed_career_stats.csv`
**Outputs:** `shap_values.csv`
**Script:** `scripts/step_11_data-visualization-phase-5.py`

**Purpose:**
To resolve this systematically:

1. Solution Approach:
   - Explicitly extract SHAP values for positive class
   - Verify array dimensions before plotting
   - Use alternative visualization if needed

2. Implementation Strategy:
   - Convert SHAP values to numpy array
   - Ensure proper shape alignment
   - Add dimension validation checks

3. Robustness Improvements:
   - Handle both binary and multi-class cases
   - Add informative error messages
   - Provide fallback visualization options

Let

---

### Step 12: Data Visualization (Phase 6)

**Inputs:** None (reads raw data)
**Outputs:** `comprehensive_shap_values.csv`
**Script:** `scripts/step_12_data-visualization-phase-6.py`

**Purpose:**
To resolve this systematically while maintaining analytical rigor:

1. Solution Framework:
   - Explicitly extract SHAP values for positive class (HOF=1)
   - Validate array shapes at each step
   - Implement robust visualization pipeline

2. Enhanced Implementation:
   - Add dimension verification checks
   - Create intermediate validation steps
   - Include fallback visualization methods

3. Comprehensive Analysis:
   - Maintain both class explanations
   - Compare HOF vs non-HOF feature impac

---

### Step 13: Model Training & Prediction (Phase 3)

**Inputs:** `processed_career_stats.csv`
**Outputs:** `final_shap_analysis.csv`
**Script:** `scripts/step_13_model-training-prediction-phase-3.py`

**Purpose:**
To resolve this systematically while ensuring robust analysis:

1. Solution Framework:
   - Create fully self-contained analysis script
   - Include all prerequisite steps
   - Verify variable availability

2. Implementation Strategy:
   - Reload and reprocess data
   - Retrain model with fixed random state
   - Maintain execution continuity

3. Validation Measures:
   - Add existence checks for key variables
   - Include diagnostic print statements
   - Ensure code chunk independence

4. Enhanc

---

### Step 14: Data Validation & Quality Report (Phase 2)

**Inputs:** `processed_career_stats.csv`
**Outputs:** `final_shap_analysis.csv`
**Script:** `scripts/step_14_data-validation-quality-report-phase-2.py`

**Purpose:**
To resolve this systematically while ensuring robust analysis:

1. Solution Framework:
   - Implement thorough SHAP array validation
   - Create dimension-aware value extraction
   - Add robust error handling

2. Implementation Strategy:
   - Verify SHAP array structure before processing
   - Handle both binary and multi-class cases
   - Implement safe column indexing

3. Validation Measures:
   - Add array shape verification
   - Include diagnostic printing
   - Implement fallback extraction me

---


## Final Output & Deliverables

# The Relationship Between Batting Statistics and Hall of Fame Induction: A Comprehensive Data Science Analysis

## Introduction and Research Context

The Baseball Hall of Fame represents the highest honor for professional baseball players, with induction decisions reflecting both quantitative performance and qualitative contributions to the sport. This study examines the statistical predictors of Hall of Fame induction through rigorous analysis of player batting statistics and induction outcomes. Our dataset comprises 101,332 seasonal batting records spanning 1871-2015 from batting.csv and 4,120 Hall of Fame voting records from hall_of_fame.csv, representing 18,659 unique players and 1,239 Hall of Fame candidates. The research employs advanced machine learning techniques and interpretability methods to uncover the complex relationship between on-field performance and this ultimate career honor.

Modern baseball analytics has evolved significantly since the early work of Bill James and the sabermetrics movement, yet the precise statistical thresholds for Hall of Fame consideration remain debated. Our analysis reveals that while traditional metrics like batting average and home runs maintain predictive power, more comprehensive measures like OPS (On-base Plus Slugging) and career longevity metrics demonstrate superior discriminative ability. The Random Forest model achieved exceptional performance with an AUC-ROC of 0.9997 and average precision of 0.9996, suggesting batting statistics alone can nearly perfectly separate Hall of Famers from other players when properly analyzed.

The study makes several novel contributions to baseball analytics. First, we demonstrate that SHAP (SHapley Additive exPlanations) values provide superior interpretability compared to traditional coefficient analysis, particularly for understanding non-linear relationships in player performance. Second, we identify the precise inflection points where statistical accumulation transitions from good to Hall of Fame caliber. Third, our era-adjusted analysis reveals how the "Hall of Fame standard" has evolved across baseball's historical periods. These findings have implications for player evaluation, Hall of Fame voting processes, and the historical understanding of baseball's elite performers.

## Data Preparation and Exploratory Analysis

The initial dataset required extensive preprocessing to facilitate meaningful analysis. Player statistics were aggregated from seasonal records to career totals, with special handling for rate statistics and missing data. The batting dataset contained 22 variables including traditional metrics (batting average, home runs, RBIs) and advanced metrics (OPS, total bases). Missing values affected 5,149 records (5.1%) for basic counting stats and up to 41,181 records (40.6%) for specialized metrics like intentional walks and sacrifice flies, requiring careful imputation strategies.

Career-length analysis revealed stark differences between Hall of


---

## How to Run

### Local Execution
```bash
# Install dependencies
pip install pandas openpyxl

# Run each step sequentially
cd case_4779_11874
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
