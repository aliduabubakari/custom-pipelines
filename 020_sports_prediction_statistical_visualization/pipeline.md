# Pipeline: Data Cleaning & Validation Workflow

## Metadata
| Field | Value |
|---|---|
| **Case ID** | `4870` |
| **Difficulty** | N/A/5 |
| **Quality** | N/A/5 |
| **Abilities** |  |
| **Total Steps** | 16 |
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

**Inputs:** `all_star.csv`, `team.csv`
**Outputs:** Console output only
**Script:** `scripts/step_01_data-loading-profiling.py`

**Purpose:**
To begin this comprehensive analysis of All-Star players and their teams' performance trends, I will first establish a structured approach to understand and analyze the provided datasets. The task requires examining performance trends over time, which suggests we'll need to:

1. First understand the structure and content of both datasets:
   - all_star.csv (198.4KB) - Likely contains player-level All-Star selections
   - team.csv (534.4KB) - Likely contains team performance metrics

2. Key analy

---

### Step 2: Data Merging & Integration

**Inputs:** None (reads raw data)
**Outputs:** `merged_all_star_team_data.csv`
**Script:** `scripts/step_02_data-merging-integration.py`

**Purpose:**
Based on the initial data understanding, the following analytical directions emerge:

1. Data Cleaning Priorities:
   - Handle missing values strategically (impute/drop based on analysis impact)
   - Standardize team identifiers across datasets
   - Verify temporal alignment between datasets

2. Enhanced Data Exploration Needed:
   - Distribution of All-Stars per team/year
   - Positional trends in All-Star selections
   - Team performance metrics correlation with All-Star count
   - League-leve

---

### Step 3: Data Loading & Profiling (Phase 2)

**Inputs:** `all_star.csv`, `team.csv`
**Outputs:** `merged_all_star_team_data.csv`
**Script:** `scripts/step_03_data-loading-profiling-phase-2.py`

**Purpose:**
To resolve this issue and ensure continuity in our analysis, we need to:

1. Restructure the code to either:
   - Combine all operations into a single executable block that maintains variable continuity
   - Explicitly reload the data at the beginning of each analysis phase

2. Consider the trade-offs:
   - Combined code blocks may become unwieldy for large analyses
   - Reloading data ensures independence but requires additional I/O operations

3. Implementation decision:
   - For this analysis

---

### Step 4: Statistical Analysis & Hypothesis Testing

**Inputs:** `merged_all_star_team_data.csv`, `all_star.csv`
**Outputs:** `enhanced_all_star_analysis.csv`
**Script:** `scripts/step_04_statistical-analysis-hypothesis-testing.py`

**Purpose:**
To deepen our analysis, we should now:

1. Perform quantitative analysis to supplement visualizations:
   - Calculate correlation coefficients between All-Star counts and performance metrics
   - Conduct significance testing on observed differences
   - Compute temporal trends with regression analysis

2. Enhance visual analysis:
   - Add trend lines to scatter plots
   - Create faceted visualizations by era/decade
   - Generate interactive visualizations for deeper exploration

3. Explore advan

---

### Step 5: Model Training & Prediction

**Inputs:** `enhanced_all_star_analysis.csv`, `all_star.csv`
**Outputs:** `final_all_star_analysis.csv`
**Script:** `scripts/step_05_model-training-prediction.py`

**Purpose:**
To further enhance our analysis, we should:

1. Address multicollinearity concerns:
   - Perform variance inflation factor (VIF) analysis
   - Consider principal component analysis
   - Evaluate alternative model specifications

2. Deepen temporal analysis:
   - Examine structural breaks in trends
   - Compare pre/post expansion eras
   - Analyze labor dispute impacts (strike years)

3. Enhance position analysis:
   - Map position numbers to actual positions (e.g., 1=P, 2=C)
   - Analyze defensi

---

### Step 6: resolve this issue and improve our era analysis, we should

**Inputs:** `enhanced_all_star_analysis.csv`, `all_star.csv`
**Outputs:** `final_all_star_analysis.csv`
**Script:** `scripts/step_06_resolve-this-issue-and-improve-our-era-a.py`

**Purpose:**
To resolve this issue and improve our era analysis, we should:

1. Correct the bin-label mismatch by:
   - Either adding one more bin edge to match the labels
   - Or adjusting the labels to match the existing bin edges

2. Consider the most appropriate era breakdown:
   - Current breaks: 1933, 1946, 1961, 1994, 2015
   - Historical context suggests these are meaningful breakpoints
   - Should maintain all breakpoints for complete coverage

3. Solution approach:
   - Keep all 5 breakpoints (4 bi

---

### Step 7: Data Visualization

**Inputs:** `enhanced_all_star_analysis.csv`, `all_star.csv`
**Outputs:** `final_all_star_analysis.csv`
**Script:** `scripts/step_07_data-visualization.py`

**Purpose:**
To resolve these issues and improve robustness:

1. Immediate fixes needed:
   - Correct the column reference from 'era_stat' to 'era' (ERA metric)
   - Address the pandas deprecation warning explicitly

2. Data validation improvements:
   - Verify all referenced columns exist before operations
   - Add defensive programming checks
   - Include more descriptive error messages

3. Analysis enhancements:
   - Add era-specific visualizations
   - Include confidence intervals in era comparisons
   -

---

### Step 8: Statistical Analysis & Hypothesis Testing (Phase 2)

**Inputs:** `enhanced_all_star_analysis.csv`, `all_star.csv`
**Outputs:** `final_enhanced_analysis.csv`
**Script:** `scripts/step_08_statistical-analysis-hypothesis-testing-.py`

**Purpose:**
To complete our analysis and address remaining issues:

1. Required fixes:
   - Remove categorical 'era' from aggregation
   - Focus on numerical metrics for era comparison
   - Maintain era as grouping variable only

2. Additional analytical opportunities:
   - Era-specific VIF analysis
   - Positional trends by era
   - Network metrics calculation
   - Multicollinearity mitigation strategies

3. Enhanced visualizations:
   - Era-specific correlation heatmaps
   - Position distribution by era
 

---

### Step 9: Final Synthesis & Reporting

**Inputs:** `enhanced_all_star_analysis.csv`, `all_star.csv`
**Outputs:** `final_all_star_analysis.csv`
**Script:** `scripts/step_09_final-synthesis-reporting.py`

**Purpose:**
To resolve this issue and complete the analysis:

1. Immediate fixes needed:
   - Replace 'era_stat' with correct column name ('era')
   - Verify all column references in analysis
   - Add column existence validation

2. Analysis improvements:
   - Clarify metric naming (ERA vs era categories)
   - Add defensive programming checks
   - Maintain consistent variable naming

3. Additional enhancements:
   - Era-specific performance decompositions
   - Positional value trends by era
   - Network evo

---

### Step 10: Data Visualization (Phase 2)

**Inputs:** `enhanced_all_star_analysis.csv`
**Outputs:** `final_filtered_analysis.csv`
**Script:** `scripts/step_10_data-visualization-phase-2.py`

**Purpose:**
To improve the analysis and address the issues:

1. Required Fixes:
   - Handle infinite values in VIF calculations
   - Remove duplicate era column operation
   - Filter eras with insufficient data

2. Analytical Enhancements:
   - Implement PCA for multicollinearity mitigation
   - Add era-weighted network metrics
   - Include confidence intervals for era comparisons

3. Visualization Improvements:
   - Create era-specific network visualizations
   - Add error bars to era comparison charts
   

---

### Step 11: Data Merging & Integration (Phase 2)

**Inputs:** `all_star.csv`, `team.csv`
**Outputs:** `era_network_metrics.csv`, `player_centrality.csv`
**Script:** `scripts/step_11_data-merging-integration-phase-2.py`

**Purpose:**
To resolve this and complete the analysis:

1. Required Fixes:
   - Reload original all_star data to get player-team relationships
   - Properly merge with team performance data
   - Preserve key identifiers through processing steps

2. Analysis Improvements:
   - Create comprehensive player-team-year dataset
   - Add player position information to networks
   - Calculate player centrality measures

3. Data Flow Changes:
   - Separate network data preparation from statistical analysis
   - Maint

---

### Step 12: Data Merging & Integration (Phase 3)

**Inputs:** `all_star.csv`, `team.csv`
**Outputs:** `era_network_metrics.csv`, `full_network_metrics.csv`
**Script:** `scripts/step_12_data-merging-integration-phase-3.py`

**Purpose:**
To resolve this issue and enhance the analysis:

1. Required Fixes:
   - Verify era column creation and preservation
   - Add data validation checks after each transformation
   - Implement proper merge operations that preserve all needed columns

2. Enhanced Analysis Plan:
   - Temporal network evolution analysis
   - Player mobility patterns across eras
   - Team composition changes over time
   - Positional network centrality trends

3. Data Quality Improvements:
   - Comprehensive data valid

---

### Step 13: Data Visualization (Phase 3)

**Inputs:** `all_star.csv`, `team.csv`
**Outputs:** `era_network_metrics.csv`, `full_network_metrics.csv`
**Script:** `scripts/step_13_data-visualization-phase-3.py`

**Purpose:**
To resolve this and proceed with the analysis:

1. Immediate Fixes Needed:
   - Verify clean code block formatting
   - Ensure proper Python syntax
   - Check for hidden characters

2. Process Improvements:
   - Implement more robust error handling
   - Add validation for code execution
   - Include environment checks

3. Analysis Continuation Plan:
   - Maintain all planned analytical components
   - Preserve data validation steps
   - Keep visualization pipeline

4. Verification Steps:
   - Te

---

### Step 14: Data Merging & Integration (Phase 4)

**Inputs:** `all_star.csv`, `team.csv`
**Outputs:** `era_network_metrics.csv`, `full_network_metrics.csv`
**Script:** `scripts/step_14_data-merging-integration-phase-4.py`

**Purpose:**
To resolve this issue and complete the analysis:

1. Root Cause Analysis:
   - Verify era column creation in load_data()
   - Check merge operation preserves era column
   - Validate categorical bin assignment

2. Required Fixes:
   - Explicitly verify era column after creation
   - Ensure merge operation keeps era column
   - Add data validation checks

3. Enhanced Analysis Plan:
   - Era distribution validation
   - Network metric robustness checks
   - Positional network analysis

4. Implemen

---

### Step 15: Data Merging & Integration (Phase 5)

**Inputs:** `all_star.csv`, `team.csv`
**Outputs:** `era_network_metrics.csv`, `full_network_metrics.csv`
**Script:** `scripts/step_15_data-merging-integration-phase-5.py`

**Purpose:**
To resolve this persistent merge issue:

1. Root Cause Analysis:
   - Possible column name conflicts during merge
   - Merge operation may be dropping categorical columns
   - Potential data type mismatches in merge keys

2. Solution Strategy:
   - Explicit column selection during merge
   - Alternative merge approaches
   - Enhanced merge validation

3. Implementation Plan:
   - Preserve era column through merge
   - Verify merge keys consistency
   - Add merge conflict resolution

4. Verificat

---

### Step 16: Data Merging & Integration (Phase 6)

**Inputs:** `all_star.csv`, `team.csv`
**Outputs:** `era_network_metrics.csv`, `full_network_metrics.csv`
**Script:** `scripts/step_16_data-merging-integration-phase-6.py`

**Purpose:**
To resolve this and complete the analysis:

1. Root Cause Analysis:
   - Verify column inclusion in initial data load
   - Check merge operation impact on position data
   - Validate column preservation through pipeline

2. Solution Strategy:
   - Explicitly include 'starting_pos' in merge
   - Add column existence validation
   - Implement fallback for missing position data

3. Implementation Plan:
   - Modify data loading to preserve positions
   - Enhance error handling for missing columns
  

---


## Final Output & Deliverables

# Comprehensive Analysis of Major League Baseball All-Star Networks (1933-2015)

## Introduction and Background

The analysis of professional sports networks provides valuable insights into the structural dynamics of team compositions and player interactions over time. This study examines the complete historical record of Major League Baseball All-Star selections from 1933 through 2015, comprising 5,069 player appearances across 82 years of All-Star games. The dataset includes detailed information about player positions, team affiliations, and seasonal performance metrics, allowing for a multifaceted network analysis. Baseball's unique position as a sport with discrete defensive roles and a long, well-documented history makes it particularly suitable for network-based examination of player-team relationships. The preservation of position data (starting_pos) in our final dataset shows a balanced distribution across defensive positions (172 appearances each for positions 1-9), with designated hitters (position 10) appearing 22 times and reserve players (position 0) appearing 10 times. This distribution immediately suggests several analytical opportunities regarding positional representation in All-Star selections.

The temporal segmentation of the data into four distinct eras—Pre-WWII (1933-1945), Post-War (1946-1960), Expansion (1961-1993), and Modern (1994-2015)—enables comparative analysis across different phases of baseball's evolution. These periods correspond to significant structural changes in the league, including integration, expansion teams, and the introduction of divisional play. Our network metrics capture these transitions through changes in connectivity patterns between players and teams. The successful preservation of both era and position data in our final merged dataset (as evidenced by the output showing 1933 data points with complete position information) provides the foundation for robust temporal and positional analysis. The network approach allows us to quantify relationships that traditional statistical analysis might overlook, particularly in terms of how player mobility and team composition strategies have evolved alongside changes in league structure and playing styles.

## Methodology and Data Preparation

The analytical framework employed in this study combines social network analysis with traditional statistical methods to examine the interconnected nature of All-Star selections. Network graphs were constructed with players and teams as nodes, connected by edges representing All-Star selections. This bipartite network structure captures both direct relationships (player-team) and indirect relationships (players connected through shared teams, teams connected through shared players). The pandas and networkx libraries in Python facilitated this network construction and analysis, with scikit-learn used for supplementary dimensionality reduction when examining multivariate relationships. Data preparation involved meticulo


---

## How to Run

### Local Execution
```bash
# Install dependencies
pip install pandas openpyxl

# Run each step sequentially
cd case_4870_12053
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
