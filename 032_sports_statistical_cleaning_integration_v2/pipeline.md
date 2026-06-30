# Pipeline: Data Cleaning & Validation Workflow

## Metadata
| Field | Value |
|---|---|
| **Case ID** | `5240` |
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

**Inputs:** `all_star.csv`, `all_star_initial_exploration.txt`
**Outputs:** `all_star_initial_exploration.txt`
**Script:** `scripts/step_01_data-loading-profiling.py`

**Purpose:**
To begin this comprehensive analysis of player and team performance trends across years and leagues, I'll first need to understand the structure and content of the provided datasets. The two files are:

1. all_star.csv - Likely contains data about All-Star players, potentially including performance metrics, years, and league affiliations
2. team.csv (534.4KB) - Likely contains team-level statistics across seasons, possibly including win-loss records, offensive/defensive metrics, and league infor

---

### Step 2: Revised Analysis & Refinement

**Inputs:** `all_star.csv`, `all_star_initial_exploration.txt`
**Outputs:** `all_star_initial_exploration.txt`
**Script:** `scripts/step_02_revised-analysis-refinement.py`

**Purpose:**
Given the execution context, I'll revise the code with these improvements:
1. Remove the unsupported datetime_is_numeric parameter
2. Split the describe() into separate calls for numeric and non-numeric columns
3. Add explicit checks for datetime columns
4. Include more robust error handling
5. Maintain all visualization capabilities
6. Ensure complete output capture

The analysis will proceed through these stages in the revised code:
1. Basic dataset inspection
2. Data quality assessment (missi

---

### Step 3: Building on the initial exploration, we should conduct deeper analysis in these areas

**Inputs:** `all_star.csv`, `all_star_advanced_analysis.txt`
**Outputs:** `all_star_advanced_analysis.txt`
**Script:** `scripts/step_03_building-on-the-initial-exploration-we-s.py`

**Purpose:**
Building on the initial exploration, we should conduct deeper analysis in these areas:

1. Temporal Analysis:
   - Yearly trends in All-Star selections
   - League-specific temporal patterns
   - Changes in team representation over time

2. Player Analysis:
   - Distribution of appearances by player
   - Positional analysis (where data exists)
   - Relationship between appearances and other metrics

3. Team/League Analysis:
   - Team representation patterns
   - League comparison across metrics


---

### Step 4: deepen our analysis, we should now

**Inputs:** `all_star.csv`, `all_star_deep_analysis.txt`
**Outputs:** `all_star_deep_analysis.txt`
**Script:** `scripts/step_04_deepen-our-analysis-we-should-now.py`

**Purpose:**
To deepen our analysis, we should now:

1. Positional Analysis:
   - Examine distribution of positions among All-Stars
   - Analyze positional trends over time
   - Compare positions between leagues

2. Game-Level Analysis:
   - Investigate years with multiple All-Star games
   - Compare player participation across games
   - Analyze selection patterns for multiple games

3. Advanced Team Analysis:
   - Calculate All-Star representation rate per team
   - Identify teams with consistently high re

---

### Step 5: Data Merging & Integration

**Inputs:** `summary_statistics.json`, `team.csv`, `final_integrated_analysis.txt`
**Outputs:** `summary_statistics.json`, `final_integrated_analysis.txt`
**Script:** `scripts/step_05_data-merging-integration.py`

**Purpose:**
To complete our comprehensive analysis, we should now:

1. Integrate Team Data:
   - Load and explore team.csv
   - Identify merge keys with all_star data
   - Create unified analysis dataset

2. Performance Correlation Analysis:
   - Examine relationship between All-Star selections and team performance
   - Compare league-level performance patterns
   - Analyze team success vs All-Star representation

3. Advanced Temporal Modeling:
   - Model selection trends over time
   - Identify significant

---

### Step 6: Data Merging & Integration (Phase 2)

**Inputs:** `all_star.csv`, `team.csv`, `final_analysis_summary.json`
**Outputs:** `top_central_players.csv`, `final_analysis_summary.json`
**Script:** `scripts/step_06_data-merging-integration-phase-2.py`

**Purpose:**
To fix this issue and ensure robust analysis, we need to:

1. Restructure Code Execution:
   - Make each code block self-contained
   - Reload all required data at start
   - Verify successful loading before proceeding

2. Add Defensive Programming:
   - Include existence checks for DataFrames
   - Add error handling for file operations
   - Validate merge keys before merging

3. Maintain Analysis Continuity:
   - Preserve all planned analysis steps
   - Ensure visualizations and outputs remain 

---

### Step 7: Data Loading & Profiling (Phase 2)

**Inputs:** `all_star.csv`, `team_column_mapping.json`, `team.csv`
**Outputs:** `merged_data_sample.csv`, `team_column_mapping.json`
**Script:** `scripts/step_07_data-loading-profiling-phase-2.py`

**Purpose:**
To resolve this issue and proceed with analysis:

1. Immediate Next Steps:
   - Examine actual team.csv column structure
   - Identify equivalent columns for required fields
   - Map expected fields to actual columns

2. Required Adjustments:
   - Modify column validation logic
   - Update merge key definitions
   - Adapt analysis to actual data structure

3. Robustness Improvements:
   - Add exploratory data examination
   - Implement flexible column mapping
   - Include fallback options for mi

---

### Step 8: Error Recovery & Robust Loading

**Inputs:** `all_star.csv`, `analysis_summary.json`, `team.csv`
**Outputs:** `merged_data_sample.csv`, `analysis_summary.json`
**Script:** `scripts/step_08_error-recovery-robust-loading.py`

**Purpose:**
To resolve this issue and enable analysis:

1. Required Adjustments:
   - Make column renaming more robust
   - Handle missing columns gracefully
   - Align column selection with actual availability

2. Improved Approach:
   - Dynamically determine available columns
   - Create flexible renaming logic
   - Proceed with available data only

3. Implementation Strategy:
   - Verify column existence before renaming
   - Match new names to available columns
   - Maintain analysis with partial data

4

---

### Step 9: Statistical Analysis & Hypothesis Testing

**Inputs:** `merged_data_sample.csv`, `advanced_analysis_results.json`
**Outputs:** `league_comparison_stats.csv`, `advanced_analysis_results.json`, `team_performance_analysis.csv`
**Script:** `scripts/step_09_statistical-analysis-hypothesis-testing.py`

**Purpose:**
To deepen our analysis with the available data, we should:

1. Enhance Team Performance Analysis:
   - Investigate relationship between wins and All-Star selections
   - Compare league-level performance patterns
   - Analyze team success vs All-Star representation

2. Expand Statistical Analysis:
   - Incorporate additional team metrics (ERA, batting stats)
   - Examine correlations between team stats and All-Star counts
   - Identify statistically significant relationships

3. Advanced Visualiz

---

### Step 10: Final Synthesis & Reporting

**Inputs:** `advanced_analysis_results.json`
**Outputs:** `league_comparison_stats.csv`, `advanced_analysis_results.json`, `team_performance_analysis.csv`
**Script:** `scripts/step_10_final-synthesis-reporting.py`

**Purpose:**
To resolve this issue and complete the analysis:

1. Required Fixes:
   - Add os module import
   - Maintain all existing analysis logic
   - Keep file checking functionality

2. Implementation Approach:
   - Import os at beginning of code
   - Preserve all analysis steps
   - Ensure backward compatibility

3. Additional Improvements:
   - Add error handling for file operations
   - Verify file paths before operations
   - Maintain clean code structure

4. Analysis Continuity:
   - All planned a

---

### Step 11: Data Merging & Integration (Phase 3)

**Inputs:** `final_analysis_report.json`, `merged_data_sample.csv`, `team_performance_analysis.csv`
**Outputs:** `final_analysis_report.json`, `statistical_test_results.csv`
**Script:** `scripts/step_11_data-merging-integration-phase-3.py`

**Purpose:**
To finalize our comprehensive analysis, we should:

1. Expand Data Coverage:
   - Load full merged dataset (not just sample)
   - Verify consistency with sample results
   - Ensure robust conclusions

2. Enhance Visualizations:
   - Add interactive elements for exploration
   - Create small multiples for detailed comparisons
   - Improve visualization aesthetics

3. Deepen Statistical Analysis:
   - Add confidence intervals to correlations
   - Perform ANOVA for multi-group comparisons
   - Chec

---

### Step 12: Data Merging & Integration (Phase 4)

**Inputs:** `final_analysis_results.json`, `all_star.csv`, `team.csv`
**Outputs:** `final_analysis_results.json`
**Script:** `scripts/step_12_data-merging-integration-phase-4.py`

**Purpose:**
The execution results indicate an empty DataFrame was loaded (shape: (0, 6)), suggesting our data loading pipeline has failed at the final stage despite previous successful executions. This requires systematic troubleshooting:

1. Data Pipeline Examination:
   - The team_performance_analysis.csv file exists but contains no data
   - Previous merged_data_sample.csv had 100 records
   - The saving/loading process may have corrupted data

2. Root Cause Hypotheses:
   - File writing may have failed 

---

### Step 13: Data Cleaning & Standardization

**Inputs:** `all_star.csv`, `cleaned_analysis_results.json`, `team.csv`
**Outputs:** `cleaned_team_performance.csv`, `cleaned_analysis_results.json`
**Script:** `scripts/step_13_data-cleaning-standardization.py`

**Purpose:**
To resolve this issue and complete our analysis:

1. Required Fixes:
   - Standardize column names in team.csv
   - Remove duplicate league identifiers
   - Ensure unique column labels

2. Solution Approach:
   - Pre-process team data before merging
   - Select preferred league identifier
   - Drop redundant columns
   - Validate uniqueness

3. Implementation Strategy:
   - Add data cleaning step
   - Implement column selection
   - Verify uniqueness
   - Proceed with analysis

4. Quality Assura

---


## Final Output & Deliverables

# Comprehensive Analysis of All-Star Player and Team Performance Trends

## Introduction and Dataset Overview

The analysis of All-Star player selections and team performance metrics provides valuable insights into the evolving landscape of professional baseball over multiple decades. This study examines two primary datasets: the all_star.csv file containing detailed records of All-Star player selections from 1933 to 2015, and the team.csv file featuring comprehensive team statistics across seasons. The merged dataset encompasses 5,069 All-Star selections across 83 seasons, representing 1,741 unique players and 49 distinct teams. The temporal coverage offers a rare longitudinal perspective on how player recognition and team success metrics have evolved through different eras of baseball history, including significant rule changes, expansion periods, and the steroid era.

Initial exploratory analysis revealed several important structural characteristics of the data. The all_star.csv dataset contains eight key variables: player_id, year, game_num, game_id, team_id, league_id, gp (game participation), and starting_pos (position). The team.csv dataset proved more expansive with 47 columns covering traditional metrics like wins (w) and losses (l), along with advanced statistics including earned run average (era), batting averages, and fielding percentages. A critical finding during data preparation was the presence of duplicate column labels in the team data, particularly around league identifiers (both league_id and lgID), which required careful preprocessing to ensure analytical integrity.

The data cleaning process involved several meticulous steps to create a robust analytical dataset. Column standardization ensured consistent naming conventions across both datasets, with particular attention to team and league identifiers. Missing value analysis showed that while most player selection records were complete (0.96% missing values in game_id), position data (starting_pos) was only available for 31.2% of records (1,580 of 5,069). This partial completeness of positional data necessitated careful interpretation of position-specific analyses. The merging process successfully combined the datasets using team_id and year as composite keys, preserving all All-Star selections while matching them with their respective team performance metrics.

Key descriptive statistics highlight the scope of our analysis. The average number of All-Star selections per season was 61.1 players (σ = 14.3), with a minimum of 36 selections in 1933 and a maximum of 84 in 2011. League representation was remarkably balanced, with the American League (AL) accounting for 50.2% of selections (2,544) and the National League (NL) 49.8% (2,525). Player-level analysis showed a right-skewed distribution of appearances, with most players (73.4%) appearing only once as All-Stars, while a select group of 27 players achieved 10 or more selections, led by Hank Aaron (25 appearances).

## Tempor


---

## How to Run

### Local Execution
```bash
# Install dependencies
pip install pandas openpyxl

# Run each step sequentially
cd case_5240_12921
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
