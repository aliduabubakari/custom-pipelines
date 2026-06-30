# Pipeline: Data Cleaning & Validation Workflow

## Metadata
| Field | Value |
|---|---|
| **Case ID** | `4503` |
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

**Inputs:** `all_star.csv`, `appearances.csv`
**Outputs:** Console output only
**Script:** `scripts/step_01_data-loading-profiling.py`

**Purpose:**
This task requires a comprehensive analysis of positional consistency between All-Star Game starters and their regular-season defensive roles. The analysis involves several key components that need to be systematically addressed:

1. Data Understanding and Preparation:
   - First, we need to examine both datasets (all_star.csv and appearances.csv) to understand their structure, columns, and relationships
   - The all_star.csv contains information about All-Star players including their starting p

---

### Step 2: Data Cleaning & Standardization

**Inputs:** `all_star.csv`, `appearances.csv`
**Outputs:** `merged_all_star_appearances.csv`
**Script:** `scripts/step_02_data-cleaning-standardization.py`

**Purpose:**
Next steps for comprehensive analysis:

1. Data Cleaning and Preparation:
   - Filter all_star data to exclude records with missing starting_pos
   - Create mapping between numeric position codes and standard position abbreviations
   - Filter appearances data to 1933-2015 range
   - Handle missing values in appearances data (particularly g_defense)

2. Primary Position Determination:
   - For each player-year in All-Star data, find corresponding appearances record
   - Calculate primary positio

---

### Step 3: Next phase of analysis should focus on

**Inputs:** None (reads raw data)
**Outputs:** `position_switch_counts.csv`, `position_group_alignment_results.csv`, `decade_alignment_results.csv`, `annual_alignment_results.csv`, `top_mismatch_players.csv`
**Script:** `scripts/step_03_next-phase-of-analysis-should-focus-on.py`

**Purpose:**
Next phase of analysis should focus on:

1. Temporal Analysis:
   - Calculate annual alignment percentages (1933-2015)
   - Identify trends and anomalies in positional consistency
   - Compare pre/post DH era (1973) and expansion eras

2. Position-Specific Analysis:
   - Breakdown alignment percentage by position group (IF, OF, C, P)
   - Identify positions most frequently played out of primary
   - Analyze common position switches (e.g., LF↔RF, 3B↔SS)

3. Player-Level Analysis:
   - Identify to

---

### Step 4: Data Merging & Integration

**Inputs:** `all_star.csv`, `appearances.csv`
**Outputs:** `position_switch_counts.csv`, `merged_all_star_appearances.csv`, `position_group_alignment_results.csv`, `decade_alignment_results.csv`, `annual_alignment_results.csv`, `top_mismatch_players.csv`
**Script:** `scripts/step_04_data-merging-integration.py`

**Purpose:**
To resolve this issue and continue the analysis, we need to:

1. Restructure the code to maintain continuity:
   - Combine all necessary operations into a single executable block
   - Ensure all variables are properly defined and accessible throughout
   - Maintain the DataFrame through all analysis steps

2. Data flow considerations:
   - Preserve the merged DataFrame from initial creation through all transformations
   - Ensure all dependent operations have access to required variables
   - Av

---

### Step 5: deepen our analysis, we should

**Inputs:** None (reads raw data)
**Outputs:** `detailed_switch_matrix.csv`, `league_alignment_results.csv`, `player_career_analysis.csv`
**Script:** `scripts/step_05_deepen-our-analysis-we-should.py`

**Purpose:**
To deepen our analysis, we should:

1. Investigate Historical Trends:
   - Examine specific rule changes impacting alignment (DH, expansion eras)
   - Analyze periods of significant deviation from the trend
   - Compare AL vs NL differences (particularly regarding DH)

2. Enhance Position Switching Analysis:
   - Create detailed transition matrix for position switches
   - Calculate switch probabilities between specific positions
   - Identify most common multi-position players

3. Player-Level 

---

### Step 6: Error Recovery & Robust Loading

**Inputs:** `all_star.csv`, `merged_all_star_appearances.csv`, `appearances.csv`
**Outputs:** `detailed_switch_matrix.csv`, `league_alignment_results.csv`, `player_career_analysis.csv`
**Script:** `scripts/step_06_error-recovery-robust-loading.py`

**Purpose:**
To resolve this issue and ensure robust execution:

1. Code Structure Improvements:
   - Include all necessary imports at the start of each executable block
   - Make each code block self-contained with required dependencies
   - Maintain consistent import aliases throughout

2. Execution Environment Considerations:
   - Assume each code block runs in isolation
   - Re-establish all required environment settings
   - Verify library availability before operations

3. Implementation Strategy:
   -

---

### Step 7: Data Merging & Integration (Phase 2)

**Inputs:** `all_star.csv`, `merged_all_star_appearances.csv`, `appearances.csv`
**Outputs:** `detailed_switch_matrix.csv`, `league_alignment_results.csv`, `player_career_analysis.csv`
**Script:** `scripts/step_07_data-merging-integration-phase-2.py`

**Purpose:**
To resolve this and ensure robust analysis:

1. Data Verification:
   - First confirm existence of league_id in all_star data
   - Check merge operation results
   - Validate column names and data types

2. Alternative Approaches:
   - If league_id unavailable in all_star, find alternative source
   - Consider using team_id to infer league (AL/NL)
   - Implement fallback options for league identification

3. Implementation Strategy:
   - Add data validation steps
   - Create defensive programmin

---

### Step 8: Data Loading & Profiling (Phase 2)

**Inputs:** `all_star.csv`, `merged_all_star_appearances.csv`, `appearances.csv`
**Outputs:** `detailed_switch_matrix.csv`, `player_career_analysis.csv`, `decade_alignment_results.csv`
**Script:** `scripts/step_08_data-loading-profiling-phase-2.py`

**Purpose:**
To resolve this systematically:

1. Data Investigation:
   - Examine team_id values to understand format
   - Check if league can be inferred from other columns
   - Verify if league information exists elsewhere in the data

2. Alternative Solutions:
   - Use external league-team mapping if available
   - Focus analysis on non-league dependent aspects
   - Implement more robust team-league inference

3. Implementation Strategy:
   - Add detailed data validation steps
   - Create defensive progra

---

### Step 9: Data Visualization

**Inputs:** `merged_all_star_appearances.csv`
**Outputs:** `league_comparison_results.csv`, `versatile_players.csv`
**Script:** `scripts/step_09_data-visualization.py`

**Purpose:**
To deepen the analysis, we should now:

1. Leverage Available League Data:
   - Re-examine league_id usage now that we've confirmed its presence
   - Compare AL vs NL positional consistency
   - Analyze DH impact by league

2. Enhanced Player Analysis:
   - Investigate specific case studies (Gwynn, Ortiz, Aaron)
   - Examine position evolution throughout careers
   - Calculate positional versatility metrics

3. Advanced Visualizations:
   - Create small multiples of position switch patterns by d

---

### Step 10: further enhance the analysis, we should

**Inputs:** `merged_all_star_appearances.csv`
**Outputs:** `dh_era_analysis.csv`, `player_versatility_analysis.csv`
**Script:** `scripts/step_10_further-enhance-the-analysis-we-should.py`

**Purpose:**
To further enhance the analysis, we should:

1. Investigate League-Specific Patterns:
   - Analyze DH impact by comparing AL/NL pre- and post-1973
   - Examine expansion era effects on positional flexibility
   - Compare position-specific trends between leagues

2. Deepen Player Analysis:
   - Calculate career position trajectories
   - Identify players with most primary position changes
   - Analyze relationship between versatility and All-Star frequency

3. Advanced Statistical Analysis:
   - 

---

### Step 11: complete our comprehensive analysis, we should

**Inputs:** `merged_all_star_appearances.csv`
**Outputs:** `position_transition_probabilities.csv`, `career_stage_analysis.csv`
**Script:** `scripts/step_11_complete-our-comprehensive-analysis-we-s.py`

**Purpose:**
To complete our comprehensive analysis, we should:

1. Finalize Position Transition Analysis:
   - Create definitive position transition matrix
   - Calculate transition probabilities between positions
   - Identify most common multi-position pathways

2. Career Stage Analysis:
   - Examine position changes by career stage (early/mid/late)
   - Compare peak vs decline years
   - Analyze age-related position flexibility

3. Historical Context:
   - Correlate alignment trends with MLB rule changes

---

### Step 12: Statistical Analysis & Hypothesis Testing

**Inputs:** `merged_all_star_appearances.csv`
**Outputs:** `position_transition_probabilities.csv`, `career_stage_analysis.csv`
**Script:** `scripts/step_12_statistical-analysis-hypothesis-testing.py`

**Purpose:**
To resolve this and complete the comprehensive analysis:

1. Data Cleaning Steps:
   - Convert all position values to strings
   - Handle NaN/None values appropriately
   - Standardize position abbreviations

2. Analysis Validation:
   - Verify all previous results with cleaned data
   - Ensure visualizations remain accurate
   - Confirm statistical tests are unaffected

3. Final Report Preparation:
   - Organize findings into logical sections
   - Prepare publication-quality visualizations
   -

---

### Step 13: Data Validation & Quality Report

**Inputs:** `merged_all_star_appearances.csv`
**Outputs:** `position_transition_probabilities.csv`, `career_stage_analysis.csv`
**Script:** `scripts/step_13_data-validation-quality-report.py`

**Purpose:**
To resolve this while maintaining analytical rigor:

1. Solution Approaches:
   - Use duplicates='drop' parameter in qcut
   - Alternative binning methods (equal spacing, manual cuts)
   - Verify player-year distribution characteristics

2. Impact Assessment:
   - Need to ensure career stage definitions remain meaningful
   - Must maintain consistent bin sizes across players
   - Should validate that changes don't distort analysis

3. Implementation Strategy:
   - Implement duplicates parameter


---

### Step 14: Data Validation & Quality Report (Phase 2)

**Inputs:** `merged_all_star_appearances.csv`
**Outputs:** `position_transition_probabilities.csv`, `career_stage_analysis.csv`
**Script:** `scripts/step_14_data-validation-quality-report-phase-2.py`

**Purpose:**
To resolve this while maintaining analytical validity:

1. Solution Approaches:
   - Use explicit bin edges instead of quantiles
   - Adjust label count to match actual bin edges
   - Implement manual career stage classification

2. Impact Assessment:
   - Need consistent career stage definitions
   - Must preserve temporal progression logic
   - Should maintain comparability across players

3. Implementation Strategy:
   - Switch to fixed bin definitions
   - Add validation checks
   - Document

---


## Final Output & Deliverables

# Positional Consistency in Major League Baseball: A Comprehensive Analysis of All-Star Game Starters and Their Regular Season Defensive Roles

## Introduction and Research Context

The relationship between All-Star Game selections and regular season performance has long been a subject of interest in baseball analytics, yet few studies have systematically examined the positional alignment between these two contexts. This investigation analyzes 1,526 unique player-year All-Star appearances from 1933 to 2015, revealing an overall positional alignment rate of 88.47% between All-Star starting positions and primary regular season defensive roles. The dataset demonstrates significant variations across eras, position groups, and individual player careers, with outfielders showing markedly lower alignment rates (74.85%) compared to catchers (98.79%) and infielders (97.58%). These findings challenge conventional assumptions about position specialization in baseball while providing new insights into how managers utilize player versatility during the midsummer classic.

The historical context of these results becomes particularly compelling when examining decade-by-decade trends. The golden era of positional consistency occurred during the 1950s, when 96.30% of All-Stars played their primary positions, compared to just 75.83% in the 2010s. This 20.47 percentage point decline coincides with several structural changes in Major League Baseball, including expansion, the introduction of the designated hitter, and evolving defensive strategies. The transition matrix analysis reveals 887 total position transitions across the study period, with the most common being catchers remaining at catcher (C→C), followed by right fielders moving between right and left field positions (RF→LF, LF→RF).

Methodologically, this study combines traditional baseball statistics with network analysis techniques to visualize the complex web of position transitions. The resulting network graph (Figure 1) contains 10 nodes representing defensive positions and 35 edges weighted by transition probability, demonstrating an average node degree of 7.0 and network density of 0.389. These metrics indicate a moderately connected system where certain positions serve as hubs for defensive flexibility, particularly in the outfield and corner infield spots. The career stage analysis further reveals that players average 1.03 primary positions during early career appearances, increasing slightly to 1.09 during mid-career before declining to 1.05 in late career phases.

## Historical Trends and Positional Evolution

The longitudinal analysis of positional alignment reveals several distinct eras in All-Star selection patterns. During the 1930s and 1940s, alignment percentages fluctuated between 85.71% and 90.74%, reflecting the early development of All-Star Game traditions and position specialization norms. The post-war era (1950-1969) saw remarkable consistency, with alignment rates exceeding 90% for t


---

## How to Run

### Local Execution
```bash
# Install dependencies
pip install pandas openpyxl

# Run each step sequentially
cd case_4503_11254
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
