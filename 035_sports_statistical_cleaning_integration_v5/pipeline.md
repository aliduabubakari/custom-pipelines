# Pipeline: Data Cleaning & Validation Workflow

## Metadata
| Field | Value |
|---|---|
| **Case ID** | `5052` |
| **Difficulty** | N/A/5 |
| **Quality** | N/A/5 |
| **Abilities** |  |
| **Total Steps** | 12 |
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

**Inputs:** `team_half.csv`, `pitching.csv`
**Outputs:** Console output only
**Script:** `scripts/step_01_data-loading-profiling.py`

**Purpose:**
To begin this comprehensive analysis of the 1981 MLB season, I will first outline the key steps required to complete the task:

1. Data Understanding Phase:
- First need to examine the structure and contents of both CSV files (team_half.csv and pitching.csv)
- Verify column names, data types, and completeness of records for 1981 season
- Check for missing values or data quality issues that might affect analysis

2. Division-Winning Team Identification:
- Filter team_half.csv for 1981 season wher

---

### Step 2: Based on the execution results, I can now proceed with the next steps of analysis after understandin

**Inputs:** `team_half.csv`, `pitching.csv`
**Outputs:** `team_pitching_stats.csv`, `top_pitchers_details.csv`, `era_distribution.csv`
**Script:** `scripts/step_02_based-on-the-execution-results-i-can-now.py`

**Purpose:**
Based on the execution results, I can now proceed with the next steps of analysis after understanding the data structure and quality:

1. Data Quality Observations:
- Team_half.csv is complete with no missing values across all 52 records
- Pitching.csv has some missing values in key metrics:
  * era missing in 90 records (critical for our analysis)
  * ipouts missing in 1 record (needed for WHIP calculation)
  * Other missing values in less critical columns

2. Key Findings from Initial Explorat

---

### Step 3: Data Loading & Profiling (Phase 2)

**Inputs:** `team_half.csv`, `pitching.csv`
**Outputs:** `era_distribution_verified.csv`, `top_pitchers_details_verified.csv`, `team_pitching_stats_verified.csv`
**Script:** `scripts/step_03_data-loading-profiling-phase-2.py`

**Purpose:**
The error reveals a critical issue in our data merging and column handling approach. Let's examine this systematically:

1. Error Diagnosis:
- The KeyError for column 'w' indicates we're trying to sort by a column that doesn't exist in the merged DataFrame
- This occurs because both team_half.csv and pitching.csv have a 'w' column (wins)
- During merging, pandas automatically disambiguates by adding suffixes (_x for left, _y for right)

2. Data Structure Investigation:
- team_half.csv 'w' repres

---

### Step 4: Data Cleaning & Standardization

**Inputs:** `team_half.csv`, `pitching.csv`
**Outputs:** `final_era_distribution.csv`, `final_top_pitchers.csv`, `final_team_stats.csv`
**Script:** `scripts/step_04_data-cleaning-standardization.py`

**Purpose:**
The latest error reveals an issue with our categorical data handling in the ERA distribution analysis. Let's conduct a thorough examination:

1. Error Diagnosis:
- The KeyError for '<=3.50' indicates the expected category label doesn't exist in our grouped data
- This suggests none of our top pitchers had ERAs ≤3.50 in some team halves
- The FutureWarning about observed=False suggests we should be explicit about handling categorical groupings

2. Data Quality Investigation:
- The ERA distributio

---

### Step 5: Data Loading & Profiling (Phase 3)

**Inputs:** `team_half.csv`, `pitching.csv`
**Outputs:** `final_team_stats_v2.csv`, `final_top_pitchers_v2.csv`, `final_era_distribution_v2.csv`
**Script:** `scripts/step_05_data-loading-profiling-phase-3.py`

**Purpose:**
The persistent KeyError indicates we need to fundamentally re-examine our approach to ERA categorization and distribution analysis. Let's conduct a comprehensive review:

1. Deep Error Analysis:
- The error occurs when trying to access 'low_era' column which doesn't exist
- This suggests our categorical grouping isn't producing expected output
- The issue likely stems from how pd.cut() interacts with groupby()

2. Data Distribution Insights:
- The ERA values may be clustered in a way that preven

---

### Step 6: Error Recovery & Robust Loading

**Inputs:** `team_half.csv`, `pitching.csv`
**Outputs:** `final_top_pitchers_v3.csv`, `final_team_stats_v3.csv`, `final_era_distribution_v3.csv`
**Script:** `scripts/step_06_error-recovery-robust-loading.py`

**Purpose:**
The latest error reveals a fundamental issue with our data structure construction. Let's conduct a thorough investigation:

1. Error Root Cause:
- The KeyError indicates our era_labels ('low_era', 'high_era') aren't becoming columns in era_dist
- This suggests the counting logic isn't properly creating the expected columns
- The manual counting approach isn't translating labels into dataframe columns

2. Data Flow Analysis:
- The era_counts list of dictionaries should create columns from keys
- 

---

### Step 7: Data Cleaning & Standardization (Phase 2)

**Inputs:** `team_half.csv`, `pitching.csv`
**Outputs:** `validated_era_distribution.csv`, `validated_top_pitchers.csv`, `validated_team_stats.csv`
**Script:** `scripts/step_07_data-cleaning-standardization-phase-2.py`

**Purpose:**
The persistent assertion error indicates our fundamental approach to counting ERA categories needs revision. Let's conduct a comprehensive root cause analysis:

1. Deep Problem Examination:
- The assertion failure confirms our counting mechanism isn't creating expected columns
- This suggests the era_category assignments aren't propagating correctly
- The issue likely stems from how we're handling categorical data in the groupby operation

2. Data Flow Investigation:
- The pd.cut() operation app

---

### Step 8: Data Merging & Integration

**Inputs:** `team_half.csv`, `pitching.csv`
**Outputs:** Console output only
**Script:** `scripts/step_08_data-merging-integration.py`

**Purpose:**
The empty DataFrame outputs reveal a critical data flow issue that requires systematic investigation:

1. Problem Diagnosis:
- The validation output shows empty DataFrames despite successful execution
- ERA categories exist in definition but not in actual data
- This suggests our filtering/merging process is eliminating all records

2. Data Flow Examination:
- Initial filters on division winners and pitching data appear too restrictive
- The merge operation may be producing an empty result set
-

---

### Step 9: The debug output reveals a fundamental issue with our initial assumptions about the 1981 season data

**Inputs:** `team_half.csv`, `pitching.csv`
**Outputs:** `validated_division_winners.csv`, `validated_top_pitchers.csv`
**Script:** `scripts/step_09_the-debug-output-reveals-a-fundamental-i.py`

**Purpose:**
The debug output reveals a fundamental issue with our initial assumptions about the 1981 season data. Let's conduct a thorough investigation:

1. Critical Finding:
- The team_half.csv shows no division winners (div_win='Y') for 1981
- This contradicts historical knowledge of the 1981 MLB season
- The issue likely stems from how division winners are recorded in this dataset

2. Historical Context:
- The 1981 season had a unique split-season format due to a player strike
- Division winners were de

---

### Step 10: Data Merging & Integration (Phase 2)

**Inputs:** `validated_division_winners.csv`, `validated_top_pitchers.csv`
**Outputs:** `correlation_matrix.csv`, `final_team_stats.csv`, `era_distribution.csv`
**Script:** `scripts/step_10_data-merging-integration-phase-2.py`

**Purpose:**
The successful merge and identification of top pitchers allows us to proceed with the comprehensive analysis. Let's examine the current state and plan next steps:

1. Current Progress:
- Successfully identified 1981 division winners using historical records
- Merged with pitching data to get 194 records
- Extracted top pitchers with valid ERA and WHIP data

2. Data Validation:
- The sample shows plausible pitcher stats (e.g., Nolan Ryan with 11 wins and 1.69 ERA)
- Team distribution matches know

---

### Step 11: Statistical Analysis & Hypothesis Testing

**Inputs:** `validated_division_winners.csv`, `validated_top_pitchers.csv`, `final_team_stats.csv`, `era_distribution.csv`
**Outputs:** `top_5_performers.csv`, `league_comparison.csv`, `half_season_comparison.csv`
**Script:** `scripts/step_11_statistical-analysis-hypothesis-testing.py`

**Purpose:**
The successful execution provides valuable statistical insights that warrant deeper examination. Let's analyze the results and plan additional investigations:

1. Key Findings from Summary Statistics:
- Average ERA of top pitchers: 2.98 ± 0.67 (mean ± std)
- Strong negative correlation (-0.84) between team rank and wins
- 80.95% of top pitchers had ERAs ≤3.50
- Teams averaged 29.71 wins per half-season

2. Interesting Patterns:
- The weak negative correlation (-0.25) between ERA and wins suggest

---

### Step 12: Data Merging & Integration (Phase 3)

**Inputs:** `validated_division_winners.csv`, `validated_top_pitchers.csv`, `final_team_stats.csv`, `era_distribution.csv`
**Outputs:** `enhanced_team_stats.csv`, `enhanced_top_pitchers.csv`
**Script:** `scripts/step_12_data-merging-integration-phase-3.py`

**Purpose:**
The error reveals a data integration issue that requires systematic investigation:

1. Error Diagnosis:
- The boxplot visualization failed because 'league_id' wasn't found in top_pitchers
- This indicates our merge operation didn't properly propagate league information
- The hue parameter requires categorical data that exists in the dataframe

2. Data Flow Examination:
- League information exists in division_winners but wasn't merged with top_pitchers
- Our earlier merge operations focused on te

---


## Final Output & Deliverables

# Comprehensive Analysis of 1981 MLB Season Pitching Performance

## Introduction and Historical Context

The 1981 Major League Baseball season represents a unique case study in baseball history due to its unusual structure resulting from a mid-season players' strike. This analysis examines the pitching performance of division-winning teams during this remarkable season, focusing on the relationship between elite pitcher performance and team success. The season was divided into two halves, with the first half running from April through June and the second half from August through October, creating an unprecedented competitive environment that affected team strategies and player performance metrics. Our dataset includes detailed pitching statistics for all teams that qualified for the postseason through either half of the split season, providing a rich source for understanding how pitching excellence contributed to team success under these special circumstances.

The statistical analysis reveals several surprising patterns in pitching performance during this transitional period in baseball history. The average ERA of top pitchers across all division-winning teams stood at 2.98 with a standard deviation of 0.67, indicating substantial consistency in elite performance despite the season's disruption. Interestingly, 80.95% of these top pitchers maintained ERAs at or below 3.50, demonstrating the exceptional quality of postseason-bound staffs. The data shows a particularly strong negative correlation (-0.84) between team rank and wins, suggesting that pitching success was more closely tied to team standing than to absolute win totals, which showed a weaker correlation (-0.25) with ERA.

Methodologically, this study employed a multi-phase analytical approach. We first identified all division-winning team halves from the 1981 season, then extracted their top three pitchers by win total, and finally conducted comprehensive statistical analyses on these pitchers' performance metrics. The validation process included cross-referencing with known historical records of the 1981 season winners, ensuring data accuracy. Our analytical framework incorporated both traditional pitching metrics (ERA, WHIP, strikeouts) and advanced statistical techniques including correlation analysis and significance testing to uncover meaningful patterns in the data.

## Methodology and Data Preparation

The research methodology employed in this study involved several rigorous stages of data collection, validation, and analysis. We began by extracting team performance data from the team_half.csv dataset, focusing specifically on teams that finished in first place during either half of the 1981 season. This initial filter identified 14 team-half combinations that qualified for postseason play under the unique rules of the strike-shortened season. The pitching.csv dataset provided detailed individual performance metrics, which we carefully merged with team information while maintaini


---

## How to Run

### Local Execution
```bash
# Install dependencies
pip install pandas openpyxl

# Run each step sequentially
cd case_5052_12415
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
