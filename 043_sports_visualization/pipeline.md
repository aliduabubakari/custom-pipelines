# Pipeline: Data Cleaning & Validation Workflow

## Metadata
| Field | Value |
|---|---|
| **Case ID** | `5283` |
| **Difficulty** | N/A/5 |
| **Quality** | N/A/5 |
| **Abilities** |  |
| **Total Steps** | 15 |
| **Input Files** | 0 |
| **Output Files** | 0 |

---

## Executive Summary

This study presents a rigorous examination of the relationship between player awards and subsequent managerial performance in professional baseball, analyzing over 3,400 manager-seasons and 6,000 player award records spanning more than a century of competition. The research combines advanced statistical modeling with historical trend analysis to uncover patterns that challenge conventional wisdom about the transition from playing to managing. Our findings reveal that while certain award combinations correlate with managerial success, the relationship is non-linear and heavily moderated by temporal factors and positional background. The negative R-squared value (-0.148) from our predictive model indicates fundamental limitations in using player achievements alone to forecast managerial success, suggesting more complex organizational dynamics at play. These results carry significant implications for front office decision-making and player development programs across Major League Baseball.

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

**Inputs:** `player_award.csv`, `manager.csv`
**Outputs:** Console output only
**Script:** `scripts/step_01_data-loading-profiling.py`

**Purpose:**
This is a comprehensive baseball analytics project requiring multi-faceted analysis of managerial performance and player awards. Let me break down the key components and develop an execution plan:

1. Data Understanding Phase:
- First need to examine both datasets' structure (columns, data types, missing values)
- Understand the temporal scope (what years are covered)
- Identify key variables: plyr_mgr flag, win-loss records, rankings, award types

2. Core Analytical Tasks:
- Statistical compari

---

### Step 2: Data Loading & Profiling (Phase 2)

**Inputs:** None (reads raw data)
**Outputs:** Console output only
**Script:** `scripts/step_02_data-loading-profiling-phase-2.py`

**Purpose:**
The error indicates that the 'awardID' column doesn't exist in the player_award.csv dataset, which suggests our initial assumption about the column names was incorrect. This requires:

1. Error Diagnosis:
- Need to verify actual column names in player_award.csv
- The error occurred during visualization attempt
- The manager.csv portion executed successfully (based on no error message for that part)

2. Required Adjustments:
- First examine actual column names in both files
- Modify visualization

---

### Step 3: Data Visualization

**Inputs:** None (reads raw data)
**Outputs:** Console output only
**Script:** `scripts/step_03_data-visualization.py`

**Purpose:**
The new error reveals a missing matplotlib import, which is needed for visualization. This indicates:

1. Current Issues:
- Missing library import for plotting
- Visualization code attempted without required imports
- Need to ensure all dependencies are properly loaded

2. Root Cause Analysis:
- The inspection function worked correctly
- Error occurred only during visualization step
- Basic data loading and inspection was successful

3. Required Fixes:
- Add proper matplotlib import at beginning

---

### Step 4: The successful execution provides valuable insights into both datasets. Here's my analysis of the re

**Inputs:** `player_award.csv`, `manager.csv`
**Outputs:** Console output only
**Script:** `scripts/step_04_the-successful-execution-provides-valuab.py`

**Purpose:**
The successful execution provides valuable insights into both datasets. Here's my analysis of the results and next steps:

1. Data Understanding:
- Manager data contains 3,405 records with 10 columns
- Key variables: plyr_mgr (Y/N), win/loss records, rankings
- Player award data has 6,078 records with 6 columns
- Award types are in 'award_id' column (27 unique types)

2. Key Observations:
- 645 player-managers vs 2,760 non-player managers
- Award data spans 117 years with 27 award types
- Manage

---

### Step 5: The execution results reveal several important findings that warrant deeper investigation

**Inputs:** `player_award.csv`, `manager.csv`
**Outputs:** Console output only
**Script:** `scripts/step_05_the-execution-results-reveal-several-imp.py`

**Purpose:**
The execution results reveal several important findings that warrant deeper investigation:

1. Key Findings from Current Analysis:
- Significant difference in win percentage between player-managers (46.7%) and non-player managers (49.0%) with p=0.0004
- Award distribution shows dramatic historical shifts, particularly for player-managers
- Data gaps in recent decades for player-managers (NaN values)

2. Required Deepening of Analysis:
- Need to examine if award types (not just counts) affect per

---

### Step 6: The latest results provide deeper insights into the manager performance dynamics. Here's my analysis

**Inputs:** `player_award.csv`, `manager.csv`
**Outputs:** Console output only
**Script:** `scripts/step_06_the-latest-results-provide-deeper-insigh.py`

**Purpose:**
The latest results provide deeper insights into the manager performance dynamics. Here's my analysis of the findings and next steps:

1. Key Findings from Current Analysis:
- Confirmed significant performance difference with Cohen's d effect size of 0.183 (small to medium effect)
- Top award types show minimal performance impact (all within 1% of mean)
- Baseball Magazine All-Star and MVP awards show slight positive impact
- Warning about deprecated ci parameter in seaborn (needs adjustment)

2.

---

### Step 7: Data Merging & Integration

**Inputs:** `player_award.csv`, `manager.csv`
**Outputs:** Console output only
**Script:** `scripts/step_07_data-merging-integration.py`

**Purpose:**
The error reveals a critical data flow issue in our analysis pipeline. Here's my detailed diagnosis and solution approach:

1. Error Analysis:
- KeyError indicates 'win_pct' column is missing during the award combination analysis
- This suggests the column creation step was either skipped or overwritten
- The error occurs after merging but before the groupby operation

2. Root Cause Investigation:
- The 'win_pct' column was originally created in previous code segments
- The current merged DataFr

---

### Step 8: The successful execution reveals several compelling patterns that warrant deeper investigation

**Inputs:** `player_award.csv`, `manager.csv`
**Outputs:** Console output only
**Script:** `scripts/step_08_the-successful-execution-reveals-several.py`

**Purpose:**
The successful execution reveals several compelling patterns that warrant deeper investigation:

1. Key Findings from Current Analysis:
- Player-managers transition much faster (avg 9.4 years) than non-player managers (22.8 years)
- Award combinations show non-linear impact, with 4-award winners performing best (50.8% win rate)
- Single-award managers outperform no-award managers (49.9% vs 48.3%)

2. Emerging Research Questions:
- Why do player-managers transition faster? Is this due to differen

---

### Step 9: Data Merging & Integration (Phase 2)

**Inputs:** `player_award.csv`, `manager.csv`
**Outputs:** Console output only
**Script:** `scripts/step_09_data-merging-integration-phase-2.py`

**Purpose:**
The error indicates a missing 'years_to_manage' column, revealing a discontinuity in our data pipeline. Here's my comprehensive analysis:

1. Error Diagnosis:
- The 'years_to_manage' column is referenced but not found
- This column was created in previous iterations but is missing now
- Suggests either:
  a) The column creation step was skipped
  b) The DataFrame was overwritten without preserving the column
  c) The merge operation didn't include necessary components

2. Data Flow Examination:


---

### Step 10: Cluster Analysis

**Inputs:** `player_award.csv`, `manager.csv`
**Outputs:** Console output only
**Script:** `scripts/step_10_cluster-analysis.py`

**Purpose:**
The successful execution reveals several compelling patterns that warrant deeper investigation:

1. Key Findings from Current Analysis:
- Pitcher managers show distinct patterns (24.8 year transition for non-player vs 13.8 for player-managers)
- Cluster 2 (MVP-dominated) shows highest win percentage (49.4%) despite lower award counts
- Position players transition faster to management (7.2 years) than pitchers (13.8 years)
- Cluster 1 shows high Gold Glove prevalence (94.8%) with moderate perform

---

### Step 11: Cluster Analysis (Phase 2)

**Inputs:** `player_award.csv`, `manager.csv`
**Outputs:** Console output only
**Script:** `scripts/step_11_cluster-analysis-phase-2.py`

**Purpose:**
The error reveals a critical oversight in our data pipeline continuity. Here's my comprehensive analysis:

1. Error Diagnosis:
- Missing 'award_cluster' column which was created in previous iterations
- The warning indicates deprecated pandas behavior in groupby operations
- Suggests we need to:
  a) Recreate the clustering features
  b) Update groupby syntax
  c) Maintain feature consistency throughout pipeline

2. Data Flow Examination:
- Award clustering was performed in earlier steps but not

---

### Step 12: Regression Modeling

**Inputs:** `player_award.csv`, `manager.csv`
**Outputs:** `final_merged_data.csv`
**Script:** `scripts/step_12_regression-modeling.py`

**Purpose:**
The error reveals a critical data quality issue that requires immediate attention. Here's my comprehensive analysis:

1. Error Diagnosis:
- NaN values present in the feature matrix X
- LinearRegression cannot handle missing values natively
- Affects both the modeling and visualization steps
- Primary sources likely:
  a) years_to_manage (from temporal calculation)
  b) is_pitcher (from position classification)
  c) award_score (from weighted calculation)

2. Impact Assessment:
- 3.8% of records 

---

### Step 13: Cluster Analysis (Phase 3)

**Inputs:** `player_award.csv`, `manager.csv`
**Outputs:** `final_processed_data.csv`
**Script:** `scripts/step_13_cluster-analysis-phase-3.py`

**Purpose:**
The error indicates a missing import for the KMeans clustering algorithm. This reveals a gap in our dependency management that needs addressing. Here's my comprehensive analysis:

1. Error Diagnosis:
- KMeans class not found despite being used in code
- Shows missing sklearn.cluster import
- Impacts the award clustering functionality
- Related visualization steps will also fail

2. Impact Assessment:
- Cluster analysis cannot proceed
- Downstream modeling affected
- Visualizations dependent on c

---

### Step 14: Data Loading & Profiling (Phase 3)

**Inputs:** `final_processed_data.csv`
**Outputs:** Console output only
**Script:** `scripts/step_14_data-loading-profiling-phase-3.py`

**Purpose:**
The successful execution with a strong silhouette score of 0.797 indicates well-separated clusters in our award feature space. This presents an opportunity to deepen our analysis in several dimensions:

1. Cluster Interpretation:
- Need to characterize each cluster's award profile
- Examine performance differences between clusters
- Investigate position distribution across clusters
- Analyze temporal trends in cluster membership

2. Modeling Enhancements:
- Incorporate cluster features into pred

---

### Step 15: Data Merging & Integration (Phase 3)

**Inputs:** `final_processed_data.csv`
**Outputs:** `final_processed_data.csv`
**Script:** `scripts/step_15_data-merging-integration-phase-3.py`

**Purpose:**
The error indicates a missing 'award_score' column in our merged dataset, revealing a discontinuity in our feature engineering pipeline. This requires careful examination and correction:

1. Error Diagnosis:
- 'award_score' column referenced but not found
- This feature was created in previous iterations but not preserved
- Suggests either:
  a) Column creation was skipped in current version
  b) Data was saved/loaded without this feature
  c) Merging operation dropped the column

2. Impact Asse

---


## Final Output & Deliverables

# Comprehensive Analysis of Managerial Performance and Player Awards in Professional Baseball

## Executive Summary and Research Context

This study presents a rigorous examination of the relationship between player awards and subsequent managerial performance in professional baseball, analyzing over 3,400 manager-seasons and 6,000 player award records spanning more than a century of competition. The research combines advanced statistical modeling with historical trend analysis to uncover patterns that challenge conventional wisdom about the transition from playing to managing. Our findings reveal that while certain award combinations correlate with managerial success, the relationship is non-linear and heavily moderated by temporal factors and positional background. The negative R-squared value (-0.148) from our predictive model indicates fundamental limitations in using player achievements alone to forecast managerial success, suggesting more complex organizational dynamics at play. These results carry significant implications for front office decision-making and player development programs across Major League Baseball.

## Data Characteristics and Methodological Framework

The analysis integrates two primary datasets: manager performance records containing win-loss statistics, team rankings, and manager type (player-manager vs. non-player manager), and player award records detailing individual accolades. Our cleaned dataset contains 3,405 managerial records with complete feature sets, including derived metrics such as award scores (weighted sum of accolades) and years between playing and managing careers. The clustering analysis revealed three distinct manager profiles based on award patterns, with silhouette scores of 0.797 indicating strong separation. Cluster 0 (n=3,031) represents managers with minimal awards, Cluster 1 (n=232) shows specialized defensive recognition (94% Gold Glove prevalence), and Cluster 2 (n=142) comprises MVP-dominated profiles. Positional distribution analysis showed pitchers transition to management later (median 24.8 years) compared to position players (18.9 years), with particularly stark differences among player-managers (13.8 vs 7.2 years).

## Key Findings and Statistical Relationships

Contrary to expectations, our analysis revealed several counterintuitive patterns. Managers in Cluster 2 (MVP-dominated) showed marginally better performance (49.4% win rate) than those in Cluster 1 (48.8%) or Cluster 0 (48.5%), but with substantial overlap in confidence intervals. The random forest model identified years_to_manage as the most important predictive feature (62.7% importance), significantly outweighing award_score (28.0%) or cluster membership (2.4-4.2%). Temporal analysis uncovered a pronounced decline in player-manager prevalence from 32.1% in the 1920s to 0.7% in the 2010s, coinciding with professionalization trends in baseball operations. Among the 645 player-managers identified, those with pitching background


---

## How to Run

### Local Execution
```bash
# Install dependencies
pip install pandas openpyxl

# Run each step sequentially
cd case_5283_12969
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
