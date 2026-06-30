# Pipeline: Data Cleaning & Validation Workflow

## Metadata
| Field | Value |
|---|---|
| **Case ID** | `4550` |
| **Difficulty** | N/A/5 |
| **Quality** | N/A/5 |
| **Abilities** |  |
| **Total Steps** | 13 |
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

**Inputs:** `pitching_postseason.csv`, `team.csv`
**Outputs:** Console output only
**Script:** `scripts/step_01_data-loading-profiling.py`

**Purpose:**
To begin this analysis, I'll first need to understand the structure and content of both datasets. The task requires joining pitching postseason data with team data for 2015, calculating average ERA by team, and including team metadata. Here's my comprehensive plan:

1. Data Inspection Phase:
   - First examine the pitching_postseason.csv structure (columns, data types, missing values)
   - Then examine team.csv structure with same thoroughness
   - Verify both datasets contain 2015 data and have

---

### Step 2: Error Recovery & Robust Loading

**Inputs:** `pitching_postseason.csv`, `team.csv`
**Outputs:** Console output only
**Script:** `scripts/step_02_error-recovery-robust-loading.py`

**Purpose:**
The error indicates that the 'yearID' column doesn't exist in the pitching_post DataFrame, which suggests either:
1. The column has a different name in the dataset
2. The dataset uses a different structure than anticipated

Key observations from the error:
- The error occurs when trying to access yearID.min()
- The RuntimeWarning about invalid values suggests potential NaN values in numerical operations
- We need to first verify the actual column names in both datasets

Next steps:
1. First exam

---

### Step 3: Data Merging & Integration

**Inputs:** `pitching_postseason.csv`, `team.csv`
**Outputs:** Console output only
**Script:** `scripts/step_03_data-merging-integration.py`

**Purpose:**
The execution results provide valuable insights into the dataset structures. Here's my comprehensive analysis:

1. Dataset Structure Understanding:
- Both datasets contain 'year' and 'team_id' columns, which will serve as our primary join keys
- The pitching data contains detailed postseason performance metrics including ERA (era)
- The team data contains organizational information including attendance

2. Key Observations:
- Common columns include many statistical measures, but we'll focus on t

---

### Step 4: Error Recovery & Robust Loading (Phase 2)

**Inputs:** `pitching_postseason.csv`, `team.csv`
**Outputs:** Console output only
**Script:** `scripts/step_04_error-recovery-robust-loading-phase-2.py`

**Purpose:**
The error reveals important insights about our data quality and analysis approach:

1. Error Analysis:
- The ValueError indicates non-finite ERA values in our dataset
- The RuntimeWarning suggests numerical instability in calculations
- This likely stems from either:
  * Infinite ERA values (mathematically possible if pitcher allows runs with 0 innings)
  * Extremely large ERA values
  * Corrupted/missing data representations

2. Data Quality Findings:
- The ERA column appears to contain problem

---

### Step 5: Error Recovery & Robust Loading (Phase 3)

**Inputs:** `pitching_postseason.csv`, `team.csv`
**Outputs:** Console output only
**Script:** `scripts/step_05_error-recovery-robust-loading-phase-3.py`

**Purpose:**
The latest error reveals another structural issue in our dataset that requires careful handling:

1. Error Analysis:
- The KeyError indicates the 'division' column doesn't exist in the team data
- This contradicts our initial assumption about the dataset structure
- We need to verify the actual available columns in the team dataset

2. Data Structure Investigation:
- Previous inspection showed team data has 'div_id' but not 'division'
- Need to determine the correct column for division informati

---

### Step 6: The execution results provide valuable insights into the division structure and data quality

**Inputs:** None (reads raw data)
**Outputs:** `team_era_analysis_2015.csv`
**Script:** `scripts/step_06_the-execution-results-provide-valuable-i.py`

**Purpose:**
The execution results provide valuable insights into the division structure and data quality:

1. Division Structure Understanding:
- The div_id column contains 'C', 'E', 'W' representing Central, East, West divisions
- Each division has exactly 10 teams in 2015 (5 AL and 5 NL teams per division)
- The mapping shows logical geographic alignment (e.g., NY teams in East, California teams in West)

2. Data Quality Observations:
- Attendance data appears complete for the sample teams shown
- ERA val

---

### Step 7: Error Recovery & Robust Loading (Phase 4)

**Inputs:** `pitching_postseason.csv`, `team.csv`
**Outputs:** `team_era_analysis_2015.csv`
**Script:** `scripts/step_07_error-recovery-robust-loading-phase-4.py`

**Purpose:**
The error reveals a critical oversight in our code execution flow:

1. Root Cause Analysis:
- The NameError indicates we're trying to use 'pitching_subset' before it's defined
- This occurred because we didn't properly maintain variable continuity between code blocks
- The pitching_subset was defined in previous code blocks but not preserved

2. Execution Flow Problem:
- Each code block executes in a separate environment
- Variables don't persist between executions
- We need to ensure all requir

---

### Step 8: The successful execution provides a foundation for deeper analysis. Here's my comprehensive assessme

**Inputs:** `pitching_postseason.csv`, `team.csv`, `team_era_analysis_2015.csv`
**Outputs:** `enhanced_team_era_analysis_2015.csv`
**Script:** `scripts/step_08_the-successful-execution-provides-a-foun.py`

**Purpose:**
The successful execution provides a foundation for deeper analysis. Here's my comprehensive assessment of the results and next steps:

1. Key Findings from Current Output:
- Significant ERA variation exists among postseason teams (1.44 to 11.17)
- Pittsburgh Pirates had the best postseason ERA (1.44) despite middle-tier attendance
- Dodgers had the worst ERA (11.17) despite highest attendance
- Central division shows most consistent performance (lower std deviation)

2. Data Quality Observations

---

### Step 9: Statistical Analysis & Hypothesis Testing

**Inputs:** `pitching_postseason.csv`, `team.csv`
**Outputs:** `final_team_era_analysis_2015.csv`
**Script:** `scripts/step_09_statistical-analysis-hypothesis-testing.py`

**Purpose:**
The execution results reveal several important insights and areas for improvement:

1. Statistical Findings:
- The ANOVA test (p=0.4075) shows no significant ERA differences between divisions
- Moderate correlation (0.60) between simple and weighted ERA metrics
- Weak correlation between attendance and ERA (0.37)

2. Warning Analysis:
- RuntimeWarning suggests some invalid values in weighted calculations
- FutureWarning indicates deprecated pandas groupby behavior
- Need to handle these properly

---

### Step 10: Statistical Analysis & Hypothesis Testing (Phase 2)

**Inputs:** `pitching_postseason.csv`, `final_team_era_analysis_2015.csv`, `team.csv`
**Outputs:** `comprehensive_team_profiles_2015.csv`
**Script:** `scripts/step_10_statistical-analysis-hypothesis-testing-.py`

**Purpose:**
The latest results provide compelling insights that warrant deeper investigation:

1. Key Statistical Findings:
- Spearman correlation (rho=0.212) confirms weak monotonic relationship between attendance and ERA
- High p-value (0.5563) indicates no statistical significance in the correlation
- Results suggest team pitching performance in postseason is largely independent of regular season attendance

2. Data Interpretation:
- The weak positive correlation contradicts conventional wisdom about hom

---

### Step 11: Data Merging & Integration (Phase 2)

**Inputs:** `pitching_postseason.csv`, `final_team_era_analysis_2015.csv`, `team.csv`
**Outputs:** `validated_team_profiles_2015.csv`
**Script:** `scripts/step_11_data-merging-integration-phase-2.py`

**Purpose:**
The error reveals a critical data integration issue that requires careful resolution:

1. Root Cause Analysis:
- The KeyError indicates 'attendance' column is missing during standardization
- This occurred because the column naming changed during merging
- The team_era dataframe had 'attendance' but it wasn't properly preserved

2. Data Flow Examination:
- Multiple merges created column naming inconsistencies
- The final team_profiles dataframe lost the original attendance column
- Need to verif

---

### Step 12: Data Cleaning & Standardization

**Inputs:** `validated_team_profiles_2015.csv`
**Outputs:** `fully_processed_team_profiles_2015.csv`
**Script:** `scripts/step_12_data-cleaning-standardization.py`

**Purpose:**
The ValueError indicates our data contains infinite or extremely large values that cannot be processed by the StandardScaler. This requires a systematic approach to resolve:

1. Data Quality Investigation:
- Need to identify which metrics contain problematic values
- Must examine distributions of each standardization candidate
- Should verify calculation methods for derived metrics

2. Root Cause Analysis:
- The error likely stems from:
  * Division by zero in SO9/BB9 calculations
  * Infinite v

---

### Step 13: Data Validation & Quality Report

**Inputs:** `pitching_postseason.csv`, `team.csv`
**Outputs:** `final_team_analysis_2015.csv`
**Script:** `scripts/step_13_data-validation-quality-report.py`

**Purpose:**
The FileNotFoundError reveals a critical path dependency in our analysis workflow that requires systematic resolution:

1. Root Cause Examination:
- The error occurs when attempting to load a previously saved intermediate file
- This indicates our code assumes file persistence between executions
- The workflow lacks proper file existence validation

2. Workflow Analysis:
- Previous code blocks created 'validated_team_profiles_2015.csv'
- Current environment doesn't maintain file persistence
- Ne

---


## Final Output & Deliverables

# Comprehensive Analysis of 2015 MLB Postseason Pitching Performance

## Introduction and Research Context

The 2015 Major League Baseball postseason represented a fascinating case study in pitching performance dynamics, particularly when examined through the lens of team-level statistics and their relationship to regular season achievements. This exhaustive analysis examines the complex interplay between postseason earned run averages (ERA), regular season performance metrics, and team attendance figures across all participating franchises. The dataset encompasses detailed pitching statistics from every 2015 postseason game combined with comprehensive team metadata, creating a robust foundation for multivariate examination. Our methodological approach combines traditional statistical techniques with advanced machine learning preprocessing to uncover non-obvious relationships in the data.

Several compelling patterns emerge from the correlation matrix, most notably the extremely strong positive relationship (r = 0.991) between raw postseason ERA and the ERA difference metric (postseason ERA minus regular season ERA). This near-perfect correlation indicates that teams' postseason ERA values primarily drove the differential scores rather than their regular season performance. The Shapiro-Wilk normality tests (p-values 0.7575, 0.4375, 0.5485) confirm that all key pitching metrics follow approximately normal distributions, validating our use of parametric statistical methods throughout the analysis.

Attendance figures demonstrate moderate positive correlations with both postseason ERA (r = 0.367) and ERA difference (r = 0.409), suggesting that higher-attendance teams tended to see greater ERA inflation during postseason play. This counterintuitive finding contradicts conventional wisdom about home field advantage and merits deeper investigation into potential confounding variables. The strongest negative correlation emerges between regular season ERA and postseason strikeouts per nine innings (SO9) at r = -0.649, indicating that teams with better regular season pitching tended to maintain higher strikeout rates in postseason play.

## Methodology and Data Processing

Our analytical pipeline incorporated multiple stages of rigorous data transformation and validation to ensure robust results. The initial dataset contained 30,423 pitching records across all postseason games from 2015, which we filtered to 247 relevant observations through systematic quality controls. We implemented a weighted ERA calculation using innings pitched as weights, with special handling for edge cases including zero-inning appearances and missing values. The RobustScaler preprocessing technique was selected over standard normalization due to its resilience to outliers in the relatively small postseason sample (n=10 teams).

The data merging process combined three primary sources: postseason pitching statistics, regular season team performance metrics, and franchise demographi


---

## How to Run

### Local Execution
```bash
# Install dependencies
pip install pandas openpyxl

# Run each step sequentially
cd case_4550_11372
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
