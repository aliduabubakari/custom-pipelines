# Pipeline: Data Cleaning & Validation Workflow

## Metadata
| Field | Value |
|---|---|
| **Case ID** | `4687` |
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

**Inputs:** `team.csv`, `fielding_postseason.csv`
**Outputs:** Console output only
**Script:** `scripts/step_01_data-loading-profiling.py`

**Purpose:**
This is a comprehensive data science task requiring analysis of MLB team performance across regular season and postseason from 1903-2015. The analysis requires multiple interconnected components:

1. Data Understanding Phase:
- First need to examine both datasets' structure (fielding_postseason.csv and team.csv)
- Understand what defensive metrics are available in postseason data (putouts, assists, errors, double plays)
- Identify regular season performance metrics in team data (win-loss, runs s

---

### Step 2: Error Recovery & Robust Loading

**Inputs:** `team.csv`, `fielding_postseason.csv`
**Outputs:** Console output only
**Script:** `scripts/step_02_error-recovery-robust-loading.py`

**Purpose:**
The error indicates that the column 'PO' (putouts) does not exist in the fielding_postseason.csv dataset. This suggests:

1. Data Structure Issue:
- The fielding postseason data may use different column naming conventions than expected
- Need to verify actual column names containing defensive metrics
- May need to explore alternative column names for putouts (e.g., 'Putouts', 'putouts', 'PO_post')

2. Required Adjustments:
- First need to print all column names to identify defensive metrics
- Ma

---

### Step 3: The execution results reveal several important insights about the data structure

**Inputs:** `team.csv`, `fielding_postseason.csv`
**Outputs:** Console output only
**Script:** `scripts/step_03_the-execution-results-reveal-several-imp.py`

**Purpose:**
The execution results reveal several important insights about the data structure:

1. Column Identification:
- Fielding postseason data contains defensive metrics but with abbreviated names ('po', 'a', 'e', 'dp')
- Team data contains win/loss metrics ('w', 'l') and run metrics ('r', 'ra') but defensive metrics are limited ('e', 'dp', 'fp')
- The initial defensive metrics search failed because it looked for full words rather than abbreviations

2. Data Quality Observations:
- Fielding data has co

---

### Step 4: The execution results provide valuable insights that shape our next steps

**Inputs:** None (reads raw data)
**Outputs:** Console output only
**Script:** `scripts/step_04_the-execution-results-provide-valuable-i.py`

**Purpose:**
The execution results provide valuable insights that shape our next steps:

1. Data Availability Insights:
- All expected defensive metrics are present in both datasets
- Fielding percentage (fp) in team data can serve as defensive efficiency proxy
- Postseason data covers exactly our target timeframe (1903-2015)
- Regular season data extends further back (1871) which may need filtering

2. Data Characteristics:
- Average 3.7 teams/year in postseason suggests we're capturing all playoff teams
- 

---

### Step 5: Data Loading & Profiling (Phase 2)

**Inputs:** `team.csv`, `fielding_postseason.csv`
**Outputs:** Console output only
**Script:** `scripts/step_05_data-loading-profiling-phase-2.py`

**Purpose:**
The error reveals a fundamental issue with variable scope and data loading:

1. Root Cause Analysis:
- The 'team' variable is not defined because the code execution environment doesn't maintain state between executions
- Previous data loading was in a separate code block that wasn't preserved
- Need to reload all data within the same execution block

2. Impact Assessment:
- All subsequent operations fail because they depend on the team data
- Fielding_post data also needs to be reloaded
- Any vi

---

### Step 6: Error Recovery & Robust Loading (Phase 2)

**Inputs:** `team.csv`, `fielding_postseason.csv`
**Outputs:** Console output only
**Script:** `scripts/step_06_error-recovery-robust-loading-phase-2.py`

**Purpose:**
The error message indicates a column access issue in our aggregation step. Let's analyze this deeply:

1. Error Diagnosis:
- The error "'e', 'dp' not in index" occurs during the groupby aggregation
- This suggests these columns don't exist in fielding_post when we try to aggregate them
- However, our earlier inspection showed these columns exist in the raw data

2. Potential Causes:
- The columns might be missing in some years/teams
- There could be case sensitivity issues (uppercase vs lowercas

---

### Step 7: Statistical Analysis & Hypothesis Testing

**Inputs:** `team.csv`, `fielding_postseason.csv`
**Outputs:** `mlb_processed_data.csv`
**Script:** `scripts/step_07_statistical-analysis-hypothesis-testing.py`

**Purpose:**
The successful execution reveals several important insights about our data relationships:

1. Correlation Matrix Interpretation:
- Strong positive correlation (0.83) between win percentage and run differential confirms expected relationship
- Negative correlation between fielding percentage (fp) and win percentage (-0.45) is counterintuitive and requires investigation
- Very high correlation (0.95) between putouts (po) and assists (a) suggests potential multicollinearity

2. Data Quality Observa

---

### Step 8: Data Merging & Integration

**Inputs:** `team.csv`, `fielding_postseason.csv`
**Outputs:** `final_processed_data.csv`
**Script:** `scripts/step_08_data-merging-integration.py`

**Purpose:**
The persistent KeyError for defensive metrics reveals deeper data structure issues that require systematic troubleshooting:

1. Error Root Cause Investigation:
- The error suggests defensive columns (e, dp) are missing in the merged dataframe despite aggregation
- Need to verify if these columns exist in the source data and survive the merge operation
- Potential causes: column renaming during merge, data type mismatches, or merge key issues

2. Data Flow Verification Points:
- Confirm presence 

---

### Step 9: Data Merging & Integration (Phase 2)

**Inputs:** `team.csv`, `fielding_postseason.csv`
**Outputs:** `mlb_final_processed.csv`
**Script:** `scripts/step_09_data-merging-integration-phase-2.py`

**Purpose:**
The execution results reveal a critical column naming issue during the merge operation that requires careful resolution:

1. Merge Conflict Analysis:
- The merge created duplicate columns with suffixes (_x, _y) for 'e' and 'dp'
- Original team data already contained 'e' and 'dp' columns (regular season stats)
- Fielding post data added postseason 'e' and 'dp' causing automatic suffixing
- This explains why our correlation analysis failed - we were looking for base column names

2. Data Structure

---

### Step 10: Statistical Analysis & Hypothesis Testing (Phase 2)

**Inputs:** `mlb_final_processed.csv`
**Outputs:** `mlb_modeling_data.csv`
**Script:** `scripts/step_10_statistical-analysis-hypothesis-testing-.py`

**Purpose:**
The successful execution provides a robust foundation for deeper analysis, revealing several important patterns and opportunities for further investigation:

1. Correlation Matrix Insights:
- The strong negative correlation (-0.92) between regular season fielding percentage (fp_reg) and errors (e_reg) validates our data quality
- Postseason defensive metrics show expected high correlations (0.95 between po_post and a_post) indicating internal consistency
- The moderate correlation (0.30) between

---

### Step 11: Statistical Analysis & Hypothesis Testing (Phase 3)

**Inputs:** `mlb_modeling_data.csv`, `mlb_final_processed.csv`
**Outputs:** `run_diff_interaction.csv`, `era_feature_importance.csv`
**Script:** `scripts/step_11_statistical-analysis-hypothesis-testing-.py`

**Purpose:**
The era-stratified results reveal fascinating historical patterns that warrant deeper investigation:

1. Era-Specific Insights:
- The Expansion era (1960-1976) shows the strongest positive fp_reg/win_pct correlation (0.34), contrasting with other periods
- Modern era (1994-2015) postseason errors (e_post) correlate positively with wins (0.20), suggesting possible survivor bias
- Free Agency era (1976-1994) shows defensive metrics having minimal correlation with wins

2. Feature Correlation Findi

---

### Step 12: Model Training & Prediction

**Inputs:** `mlb_final_processed.csv`
**Outputs:** `feature_importance_analysis.csv`, `era_specific_results.csv`
**Script:** `scripts/step_12_model-training-prediction.py`

**Purpose:**
The error encountered during ROC AUC calculation reveals a fundamental issue with our classification task that requires careful examination:

1. Error Diagnosis:
- The IndexError suggests predict_proba() returns only one column instead of two
- This occurs when the RandomForestClassifier only predicts one class
- Indicates potential class imbalance or insufficient data in certain eras

2. Root Cause Analysis:
- Some historical eras may have very few World Series winners
- The train/test split mi

---

### Step 13: Data Merging & Integration (Phase 3)

**Inputs:** `mlb_final_processed.csv`
**Outputs:** `robust_era_results.csv`, `feature_importance_full_analysis.csv`
**Script:** `scripts/step_13_data-merging-integration-phase-3.py`

**Purpose:**
The error reveals a critical limitation in our dataset that requires methodological refinement:

1. Error Context:
- The ValueError indicates insufficient samples in some World Series winner classes
- Occurs during stratified sampling when a class has <2 members
- Particularly problematic for rare events like World Series wins in certain eras

2. Root Cause Examination:
- Some historical eras have very few championship teams
- The 410-team merged dataset contains only 112 World Series winners (2

---

### Step 14: Data Visualization

**Inputs:** `mlb_final_processed.csv`
**Outputs:** `robust_era_results.csv`, `feature_importance_full_analysis.csv`
**Script:** `scripts/step_14_data-visualization.py`

**Purpose:**
The error reveals a simple but critical oversight in our code implementation that requires correction:

1. Error Diagnosis:
- The NameError indicates missing matplotlib.pyplot import
- Visualization code was added but without proper library import
- Basic Python import oversight despite correct analysis logic

2. Impact Assessment:
- Prevents generation of feature importance visualizations
- Does not affect core analytical computations
- Easily remedied with proper imports

3. Solution Approach:

---


## Final Output & Deliverables

# The Relationship Between Postseason Defensive Performance and Regular Season Success in Major League Baseball: A Comprehensive Analysis (1903-2015)

## Introduction and Research Context

The analysis of baseball performance metrics has long fascinated statisticians and sports analysts alike, with particular interest in understanding how regular season performance translates to postseason success. This study examines 112 years of Major League Baseball data (1903-2015) to investigate the relationship between postseason defensive performance and regular season team success. Our analysis incorporates multiple defensive metrics including putouts (PO), assists (A), errors (E), double plays (DP), and fielding percentage (FP), while considering regular season performance through win-loss records, runs scored/allowed, and various efficiency measures.

The fundamental hypothesis guiding this research suggests that teams demonstrating consistent defensive performance between regular season and postseason play achieve greater postseason success. However, our preliminary findings reveal several counterintuitive relationships that challenge conventional baseball wisdom. For instance, the negative correlation (-0.45) between regular season fielding percentage and win percentage directly contradicts traditional baseball analytics, suggesting that superior fielding teams might sacrifice offensive production or that error-prone teams might compensate through other performance dimensions.

Methodologically, this study employs a multi-phase analytical approach. The initial data preparation phase involved merging two comprehensive datasets: the fielding_postseason.csv (604.1KB) containing detailed defensive metrics for postseason games, and the team.csv (534.4KB) with regular season performance statistics. After extensive data cleaning and validation, we analyzed 410 team-seasons that included both regular season and postseason play. The analytical framework incorporates correlation analysis, era-stratified modeling, and machine learning techniques to uncover nuanced relationships between defensive performance and team success.

Several surprising findings emerged from our initial exploration. Postseason double plays (dp_post) showed a higher correlation with World Series wins (0.20) than either regular season (0.13) or postseason (0.02) defensive efficiency metrics. This suggests that the ability to execute double plays in high-leverage postseason situations may be more valuable than overall defensive consistency. Furthermore, the era-specific analysis revealed dramatic fluctuations in the importance of various defensive metrics, with the Expansion Era (1960-1976) showing the strongest positive correlation between fielding percentage and win percentage (0.34), while the Modern Era (1994-2015) demonstrated virtually no relationship (0.007).

The comprehensive nature of this study addresses several gaps in existing baseball analytics literature. First, it provides t


---

## How to Run

### Local Execution
```bash
# Install dependencies
pip install pandas openpyxl

# Run each step sequentially
cd case_4687_11664
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
