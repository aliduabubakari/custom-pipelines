# Pipeline: Data Cleaning & Validation Workflow

## Metadata
| Field | Value |
|---|---|
| **Case ID** | `4829` |
| **Difficulty** | N/A/5 |
| **Quality** | N/A/5 |
| **Abilities** |  |
| **Total Steps** | 15 |
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

### Step 1: Data Loading & Profiling: Initial Data Exploration

**Inputs:** `all_star.csv`, `team.csv`
**Outputs:** Console output only
**Script:** `scripts/step_01_data-loading-profiling-initial-data-expl.py`

**Purpose:**
This is a comprehensive data science task requiring multiple analytical approaches to examine the relationship between MLB All-Star participation and team performance. The analysis will require careful data integration, statistical modeling, and temporal analysis. Here's my detailed plan:

1. **Initial Data Exploration**
   - First need to examine both datasets' structure, columns, and completeness
   - Verify key join fields (team_id and year) exist in both datasets
   - Check for missing value

---

### Step 2: Data Cleaning & Standardization: Data Cleaning Priorities

**Inputs:** `all_star.csv`, `team.csv`
**Outputs:** Console output only
**Script:** `scripts/step_02_data-cleaning-standardization-data-clean.py`

**Purpose:**
Based on the initial exploration, we should proceed with:

1. **Data Cleaning Priorities**
   - Handle missing league_id in team data (likely pre-AL/NL era)
   - Decide how to treat missing starting_pos in All-Star data
   - Verify team_id consistency across datasets

2. **Feature Engineering Needs**
   - Calculate All-Star player counts per team per year
   - Create win percentage metric from w/g
   - Normalize offensive stats by games played
   - Create playoff eligibility flag combining div_w

---

### Step 3: Statistical Analysis & Hypothesis Testing

**Inputs:** None (reads raw data)
**Outputs:** `modeling_data.csv`
**Script:** `scripts/step_03_statistical-analysis-hypothesis-testing.py`

**Purpose:**
The analysis suggests several important next steps:

1. **Temporal Analysis Needs**
   - Investigate how correlations have changed over different eras
   - Examine league-specific trends (AL vs NL)
   - Consider impact of expansion teams on relationships

2. **Modeling Considerations**
   - Playoff prediction model should account for:
     - Changing playoff formats over time
     - League-specific differences
     - Non-linear relationships apparent in scatterplots

3. **Additional Visualizatio

---

### Step 4: Data Merging & Integration

**Inputs:** `all_star.csv`, `team.csv`
**Outputs:** `modeling_data_clean.csv`
**Script:** `scripts/step_04_data-merging-integration.py`

**Purpose:**
To resolve this issue and continue the analysis, we need to:

1. **Re-establish the Data Pipeline**
   - Reload and re-merge the datasets to recreate 'merged'
   - Ensure all cleaning steps are reapplied
   - Maintain consistency with previous transformations

2. **Improve Code Structure**
   - Include all necessary preprocessing in this code block
   - Add verification steps to confirm data integrity
   - Consider saving/loading intermediate results if needed

3. **Prevent Future Scope Issues**

---

### Step 5: Data Validation & Quality Report

**Inputs:** `all_star.csv`, `team.csv`
**Outputs:** `model_ready_data.csv`
**Script:** `scripts/step_05_data-validation-quality-report.py`

**Purpose:**
To resolve this and improve the analysis:

1. **Column Reference Corrections**
   - Replace 'era_stat' with 'era' (the pitching metric)
   - Rename era period column to avoid confusion
   - Verify all column names before calculations

2. **Data Quality Checks**
   - Add explicit column existence verification
   - Include dtype validation for numeric columns
   - Add bounds checking for metric values

3. **Enhanced Error Handling**
   - Implement try-catch blocks for statistical operations
   - A

---

### Step 6: Data Validation & Quality Report (Phase 2)

**Inputs:** `all_star.csv`, `team.csv`
**Outputs:** `final_model_data.csv`
**Script:** `scripts/step_06_data-validation-quality-report-phase-2.py`

**Purpose:**
To resolve this issue and improve the robustness of our analysis:

1. **Immediate Fixes Needed**
   - Update validation function to match current column names
   - Ensure all references to 'era' are consistent throughout the code
   - Verify all required columns exist before validation

2. **Longer-Term Improvements**
   - Create a centralized column name reference system
   - Implement schema validation before processing
   - Add data version checks

3. **Analysis Continuity**
   - Maintain all

---

### Step 7: Statistical Analysis & Hypothesis Testing (Phase 2)

**Inputs:** `final_model_data.csv`
**Outputs:** `enhanced_model_data.csv`
**Script:** `scripts/step_07_statistical-analysis-hypothesis-testing-.py`

**Purpose:**
To enhance the analysis and address the warning:

1. **Immediate Improvements Needed**
   - Fix DataFrameGroupBy warning by updating correlation calculation
   - Improve correlation matrix presentation
   - Add statistical significance testing

2. **Additional Analysis Opportunities**
   - Include confidence intervals for correlations
   - Add era-specific regression models
   - Perform ANOVA across periods

3. **Visualization Enhancements**
   - Add correlation coefficient annotations to plots


---

### Step 8: Data Visualization: Immediate Fixes Needed

**Inputs:** None (reads raw data)
**Outputs:** Console output only
**Script:** `scripts/step_08_data-visualization-immediate-fixes-neede.py`

**Purpose:**
To resolve this and improve the visualization:

1. **Immediate Fixes Needed**
   - Replace 'order' parameter with proper categorical sorting
   - Ensure period sequence is maintained
   - Verify all plotting parameters are valid

2. **Visualization Enhancements**
   - Add confidence intervals to line plots
   - Improve axis labeling for clarity
   - Add annotations for key findings

3. **Code Robustness**
   - Add parameter validation for plotting functions
   - Include error handling for visual

---

### Step 9: Regression Modeling

**Inputs:** `enhanced_model_data.csv`
**Outputs:** `final_analysis_results.csv`, `feature_importance.csv`, `performance_anomalies.csv`
**Script:** `scripts/step_09_regression-modeling.py`

**Purpose:**
To complete the comprehensive analysis, we should now:

1. **Finalize Modeling Preparation**
   - Create train/test splits preserving temporal order
   - Standardize features within eras
   - Encode categorical variables

2. **Implement Predictive Models**
   - Logistic regression for playoff prediction
   - Era-specific model variants
   - Feature importance analysis

3. **Conduct Anomaly Detection**
   - Identify over/under-performing teams
   - Analyze characteristics of anomalies
   - Visual

---

### Step 10: Data Validation & Quality Report (Phase 3)

**Inputs:** `all_star.csv`, `team.csv`
**Outputs:** `model_feature_importance.csv`, `final_analysis_dataset.csv`
**Script:** `scripts/step_10_data-validation-quality-report-phase-3.py`

**Purpose:**
To resolve this and ensure robust analysis completion:

1. **Immediate Solutions**
   - Recreate the required data from scratch
   - Verify file paths and existence
   - Add file existence checks

2. **Pipeline Improvements**
   - Implement complete data regeneration
   - Add validation checks for dependencies
   - Include fallback data generation

3. **Execution Robustness**
   - Make each step self-contained
   - Handle missing data gracefully
   - Provide informative error messages

4. **Anal

---

### Step 11: Data Visualization: Immediate Improvements

**Inputs:** `model_feature_importance.csv`, `final_analysis_dataset.csv`
**Outputs:** Console output only
**Script:** `scripts/step_11_data-visualization-immediate-improvement.py`

**Purpose:**
To complete the comprehensive analysis:

1. **Immediate Improvements**
   - Address seaborn warning
   - Add model interpretation visuals
   - Include prediction examples

2. **Enhanced Analysis**
   - Add SHAP values for feature interpretation
   - Include partial dependence plots
   - Calculate confidence intervals

3. **Final Outputs**
   - Compile all visualizations
   - Generate model cards
   - Create analysis summary

4. **Presentation Quality**
   - Improve plot aesthetics
   - Add expla

---

### Step 12: Regression Modeling (Phase 2)

**Inputs:** `final_analysis_dataset.csv`
**Outputs:** Console output only
**Script:** `scripts/step_12_regression-modeling-phase-2.py`

**Purpose:**
The error indicates that the LogisticRegression class from scikit-learn was not imported, despite being used in the code. This reveals several important considerations:

1. **Code Structure Issue**
   - The class was referenced without proper import
   - This breaks the execution flow despite correct logic
   - Highlights need for complete import verification

2. **Execution Context**
   - Previous successful runs may have had different imports
   - Environment state cannot be assumed between ex

---

### Step 13: Final Synthesis & Reporting

**Inputs:** None (reads raw data)
**Outputs:** `final_feature_importance.csv`, `analysis_summary.csv`, `final_dataset.csv`
**Script:** `scripts/step_13_final-synthesis-reporting.py`

**Purpose:**
To resolve this and complete the analysis:

1. **Immediate Fixes**
   - Update partial dependence code for current sklearn version
   - Add return structure inspection
   - Implement version-agnostic access

2. **Robustness Improvements**
   - Add error handling for visualization
   - Include fallback plotting methods
   - Verify sklearn version compatibility

3. **Analysis Completion**
   - Ensure all core outputs are generated
   - Maintain model interpretability
   - Preserve statistical vali

---

### Step 14: Data Visualization: Immediate Solution

**Inputs:** `analysis_summary.txt`, `final_dataset.csv`
**Outputs:** `analysis_summary.txt`
**Script:** `scripts/step_14_data-visualization-immediate-solution.py`

**Purpose:**
To resolve this and finalize the analysis:

1. **Immediate Solution**
   - Reimport matplotlib.pyplot
   - Verify all visualization dependencies
   - Ensure consistent execution context

2. **Robustness Improvements**
   - Consolidate all imports at start
   - Add import verification checks
   - Include defensive programming

3. **Finalization Steps**
   - Generate remaining visualizations
   - Compile comprehensive results
   - Prepare for final report

4. **Quality Assurance**
   - Verify all 

---

### Step 15: Data Visualization: Immediate Solution (Phase 2)

**Inputs:** `all_star.csv`, `analysis_summary.txt`, `team.csv`
**Outputs:** `analysis_summary.txt`, `final_dataset.csv`
**Script:** `scripts/step_15_data-visualization-immediate-solution-ph.py`

**Purpose:**
To resolve this and complete the comprehensive analysis:

1. **Immediate Solution**
   - Rebuild the dataset from original sources
   - Implement self-contained data preparation
   - Add file existence checks

2. **Robustness Improvements**
   - Make analysis steps independent
   - Include fallback data generation
   - Add validation checks

3. **Finalization Strategy**
   - Consolidate all data processing
   - Generate required visualizations
   - Compile final results

4. **Quality Assurance**

---


## Final Output & Deliverables

# The Relationship Between All-Star Player Participation and Team Performance in Major League Baseball: A Comprehensive Longitudinal Analysis

## Introduction and Research Context

The relationship between individual player excellence and team success in professional sports has long been a subject of both academic inquiry and practical team management strategy. In Major League Baseball (MLB), the annual All-Star game serves as a unique showcase where the league's most talented players are selected to represent their respective teams and leagues. This study examines the quantitative relationship between All-Star player participation and team performance metrics across eight decades of MLB history (1933-2015), providing one of the most comprehensive longitudinal analyses of this relationship to date. The analysis incorporates multiple performance dimensions including win percentage, earned run average (ERA), runs scored, and playoff qualification outcomes, while controlling for historical era effects and league-specific factors.

Our dataset comprises 1,894 team-season observations from the Lahman Baseball Database, incorporating both traditional box score statistics and advanced metrics. The statistical modeling reveals several significant relationships, most notably that teams with more All-Star selections demonstrate a 0.918 prediction accuracy for playoff qualification (AUC-ROC = 0.965), with win percentage emerging as the strongest predictor (coefficient = 3.538). However, the analysis also uncovers nuanced patterns that challenge conventional wisdom, particularly regarding the relative importance of All-Star participation compared to other performance factors. The visualization in [final_shap_analysis.png] demonstrates the differential impact of various features on playoff probability, while [enhanced_partial_dependence.png] reveals non-linear relationships between key predictors and outcomes.

The historical segmentation of the data into five distinct eras (Pre-Integration 1933-1946, Post-War 1947-1960, Expansion 1961-1976, Free Agency 1977-1993, and Modern 1994-2015) allows for examination of how these relationships have evolved alongside structural changes in the game. Notably, the Modern era shows the strongest correlation between All-Star participation and playoff success (r = 0.492), compared to just 0.380 in the Post-War era. This suggests that the value of star players has increased in contemporary baseball, possibly due to changes in playoff structure, player specialization, or competitive balance dynamics.

## Data Preparation and Methodological Framework

The foundation of this analysis rests on a rigorous data preparation process that merged individual All-Star selections from the all_star.csv dataset with team performance metrics from team.csv. The merging process utilized team_id and year as primary keys, resulting in a comprehensive dataset covering 82 seasons of MLB competition. During data cleaning, we addressed several chall


---

## How to Run

### Local Execution
```bash
# Install dependencies
pip install pandas openpyxl

# Run each step sequentially
cd case_4829_12001
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
