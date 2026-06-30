# Pipeline: Data Cleaning & Validation Workflow

## Metadata
| Field | Value |
|---|---|
| **Case ID** | `5054` |
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

**Inputs:** `all_star.csv`, `fielding_postseason.csv`
**Outputs:** `2015_position_stats.csv`
**Script:** `scripts/step_01_data-loading-profiling.py`

**Purpose:**
This analysis presents an interesting challenge of examining potential relationships between historical all-star player positions (1933) and postseason defensive statistics from a much later period (2015). The temporal gap of 82 years suggests we're likely dealing with entirely different generations of players, making any direct comparisons problematic. However, we can approach this systematically:

1. Data Understanding Phase:
   - First examine both datasets' structures, columns, and basic sta

---

### Step 2: Data Visualization

**Inputs:** `all_star.csv`, `fielding_postseason.csv`
**Outputs:** `all_star_sample.csv`, `fielding_post_sample.csv`
**Script:** `scripts/step_02_data-visualization.py`

**Purpose:**
The error reveals a critical data structure issue - the all_star.csv dataset doesn't contain a 'position' column as expected. This requires immediate investigation and adjustment to our analysis approach:

1. Error Diagnosis:
   - The KeyError indicates our assumption about column names was incorrect
   - We need to first verify the actual column names in all_star.csv
   - The error occurred during visualization attempt, suggesting our initial data exploration was incomplete

2. Required Adjustm

---

### Step 3: Data Cleaning & Standardization

**Inputs:** `all_star.csv`, `fielding_postseason.csv`
**Outputs:** `2015_defensive_metrics.csv`
**Script:** `scripts/step_03_data-cleaning-standardization.py`

**Purpose:**
The execution results reveal important structural information about both datasets that requires careful consideration:

1. Data Structure Findings:
   - All-star data contains 'starting_pos' (float) rather than expected 'position' column
   - Postseason data has categorical 'pos' column (object type)
   - No matching position columns found in our predefined list

2. Key Observations:
   - The 'starting_pos' in all_star.csv likely represents numerical position codes
   - Need to map these numeric

---

### Step 4: Error Recovery & Robust Loading

**Inputs:** `fielding_postseason.csv`
**Outputs:** `available_defensive_stats.csv`
**Script:** `scripts/step_04_error-recovery-robust-loading.py`

**Purpose:**
The latest error reveals another critical data structure mismatch - the expected defensive metric columns (A, DP, E, PO) are not present in the fielding_postseason.csv dataset as we assumed. This requires careful re-examination of the actual available columns and adjustment of our analytical approach:

1. Error Diagnosis:
   - The KeyError indicates our assumption about defensive metric columns was incorrect
   - We need to verify the actual defensive statistics available in the dataset
   - The

---

### Step 5: Data Cleaning & Standardization (Phase 2)

**Inputs:** `all_star.csv`, `fielding_postseason.csv`
**Outputs:** `position_distribution_comparison.csv`, `enhanced_defensive_metrics.csv`
**Script:** `scripts/step_05_data-cleaning-standardization-phase-2.py`

**Purpose:**
The execution results provide a comprehensive view of the available defensive metrics and position data, enabling us to proceed with a more informed analysis. Here's our refined approach:

1. Data Validation Findings:
   - Confirmed availability of standard defensive metrics (PO, A, E, DP)
   - Identified 11 distinct position categories in 2015 data
   - Verified numerical position mapping works for 1933 all-star data

2. Key Insights from Current Output:
   - Catchers (C) show highest putout (P

---

### Step 6: Error Recovery & Robust Loading (Phase 2)

**Inputs:** `all_star.csv`, `fielding_postseason.csv`
**Outputs:** `position_distribution_comparison.csv`, `enhanced_defensive_metrics.csv`
**Script:** `scripts/step_06_error-recovery-robust-loading-phase-2.py`

**Purpose:**
The error reveals a structural issue with our defensive metrics DataFrame that requires attention:

1. Error Diagnosis:
   - The error occurs when trying to sort a multi-index DataFrame
   - The 'sort_values()' method requires explicit column specification
   - Our defensive stats DataFrame has hierarchical columns after aggregation

2. Data Structure Understanding:
   - The groupby operation created a MultiIndex columns structure
   - Need to properly reference the 'fielding_pct' column
   - Mu

---

### Step 7: The successful execution provides valuable insights that warrant deeper exploration. Here's our comp

**Inputs:** `position_distribution_comparison.csv`, `enhanced_defensive_metrics.csv`
**Outputs:** `final_defensive_metrics.csv`, `final_position_distribution.csv`
**Script:** `scripts/step_07_the-successful-execution-provides-valuab.py`

**Purpose:**
The successful execution provides valuable insights that warrant deeper exploration. Here's our comprehensive analysis plan moving forward:

1. Key Findings from Current Output:
   - Outfielders (OF) show perfect fielding percentage (1.000) but with minimal data points
   - Catchers (C) and first basemen (1B) demonstrate exceptional fielding percentages (>0.99)
   - Shortstops (SS) dominate assist metrics (10.41 mean assists)
   - Pitchers (P) comprise 41% of 2015 postseason players vs 11% in 19

---

### Step 8: Data Loading & Profiling (Phase 2)

**Inputs:** `position_distribution_comparison.csv`, `enhanced_defensive_metrics.csv`
**Outputs:** `validated_position_distribution.csv`, `validated_defensive_metrics.csv`
**Script:** `scripts/step_08_data-loading-profiling-phase-2.py`

**Purpose:**
The error indicates a mismatch in our data loading assumptions, requiring careful examination of the saved file structure:

1. Error Diagnosis:
   - The ValueError suggests the 'pos' index column doesn't exist in the CSV
   - Likely caused by how we previously saved the position_distribution_comparison.csv
   - Need to verify the actual structure of saved files

2. Data Structure Investigation:
   - Check if index was properly saved in the CSV
   - Verify column names in saved files
   - Determi

---

### Step 9: Data Loading & Profiling (Phase 3)

**Inputs:** `validated_position_distribution.csv`, `validated_defensive_metrics.csv`, `fielding_postseason.csv`
**Outputs:** `era_comparison_matrix.csv`, `position_defensive_profiles.csv`, `normalized_defensive_stats.csv`
**Script:** `scripts/step_09_data-loading-profiling-phase-3.py`

**Purpose:**
The successful execution with proper data loading reveals several important insights that warrant deeper investigation:

1. Key Findings from Current Output:
   - The chi-square test (p=0.0000) confirms statistically significant differences in position distributions between 1933 and 2015
   - Outfielders (OF) maintain perfect fielding percentage (1.000) but with limited sample size
   - Catchers (C) and first basemen (1B) show remarkably consistent high fielding percentages (>0.99)

2. Data Qual

---

### Step 10: Data Visualization (Phase 2)

**Inputs:** `fielding_postseason.csv`
**Outputs:** `era_comparison_matrix.csv`, `normalized_defensive_stats.csv`
**Script:** `scripts/step_10_data-visualization-phase-2.py`

**Purpose:**
The execution errors reveal several technical issues that require careful resolution while maintaining our analytical objectives:

1. Error Diagnosis:
   - Radar chart error: Dimension mismatch between angles (6) and values (5)
   - Runtime warnings: Division by zero in normalized stats calculation
   - FutureWarning: Pandas groupby behavior change

2. Root Cause Analysis:
   - Radar chart values incorrectly sliced (missing final element for loop closure)
   - Some positions may have zero inning

---

### Step 11: Data Visualization (Phase 3)

**Inputs:** `fielding_postseason.csv`
**Outputs:** `era_comparison_matrix.csv`, `normalized_defensive_stats.csv`
**Script:** `scripts/step_11_data-visualization-phase-3.py`

**Purpose:**
The latest errors reveal persistent issues with data indexing and pandas operations that require systematic resolution:

1. Error Diagnosis:
   - KeyError 'C' indicates missing position data in the defensive stats
   - FutureWarning persists regarding groupby operations
   - Data alignment issues between visualization and source data

2. Root Cause Analysis:
   - Position labels may not be properly indexed in defensive stats
   - Groupby operation still includes grouping columns
   - Data valida

---

### Step 12: Data Visualization (Phase 4)

**Inputs:** `fielding_postseason.csv`
**Outputs:** `final_radar_data.csv`, `final_era_comparison.csv`, `final_normalized_stats.csv`
**Script:** `scripts/step_12_data-visualization-phase-4.py`

**Purpose:**
The persistent radar chart error and groupby warning indicate fundamental issues requiring systematic resolution before proceeding to final reporting:

1. Error Diagnosis:
   - Dimension mismatch (7 vs 6) suggests incorrect value aggregation
   - FutureWarning confirms deprecated pandas behavior
   - Data structure inconsistencies remain unresolved

2. Root Cause Analysis:
   - Radar chart values not properly aligned with angles
   - Groupby operation still includes grouping columns
   - Data va

---


## Final Output & Deliverables

# Comparative Analysis of Defensive Performance Metrics Across Baseball Eras: 1933 All-Stars vs. 2015 Postseason Players

## Introduction and Research Context

The evolution of defensive play in Major League Baseball represents one of the most significant yet understudied aspects of the game's development. This comprehensive analysis examines the defensive performance metrics across two distinct eras in baseball history: the 1933 All-Star players and the 2015 postseason participants. The temporal gap of 82 years between these datasets provides a unique opportunity to study how defensive expectations, positional requirements, and performance standards have transformed throughout baseball's modern era. Our investigation focuses on three primary dimensions: positional distribution patterns, normalized defensive metrics, and the evolution of fielding efficiency across different defensive roles.

The 1933 season represents a pivotal year in baseball history, marking the inaugural All-Star game and occurring during the live-ball era's peak. Contrastingly, the 2015 postseason data reflects contemporary baseball's sophisticated defensive analytics and specialized positional play. Our analysis reveals that first basemen in 2015 maintained an exceptional fielding percentage of 0.991, while their 1933 counterparts represented 10.96% of all All-Star selections compared to just 6.92% of 2015 postseason players. This inverse relationship between representation and performance suggests fundamental changes in defensive expectations for the position.

Methodologically, this study employs several innovative approaches to cross-era comparison. We have normalized defensive statistics to account for differences in playing time, with putouts per 1000 innings ranging from 786.17 for catchers to 237.44 for second basemen in the 2015 data. The radar chart visualization in position_profiles_radar.png demonstrates the multidimensional nature of defensive performance, particularly highlighting how shortstops (SS) dominate assist metrics while catchers (C) excel in putouts. These positional specializations have become increasingly pronounced over time, as evidenced by the chi-square test (p < 0.0001) confirming statistically significant differences in position distribution between eras.

## Positional Distribution and Defensive Specialization

The transformation of defensive positioning between 1933 and 2015 reveals profound changes in baseball strategy and player deployment. Our analysis of the position_distribution_comparison.csv dataset shows that pitchers comprised 41.09% of 2015 postseason players compared to just 10.96% of 1933 All-Stars, reflecting the modern emphasis on specialized bullpen roles. Conversely, outfield positions (LF, CF, RF) collectively represented 32.83% of 1933 All-Stars versus 24.25% in 2015, indicating a relative de-emphasis on outfield defense in contemporary baseball. These distribution patterns suggest that modern baseball prioritizes defensive


---

## How to Run

### Local Execution
```bash
# Install dependencies
pip install pandas openpyxl

# Run each step sequentially
cd case_5054_12453
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
