# Pipeline: Data Cleaning & Validation Workflow

## Metadata
| Field | Value |
|---|---|
| **Case ID** | `4027` |
| **Difficulty** | 4/5 |
| **Quality** | 4/5 |
| **Abilities** | Data Preparation, Data Analysis, Data Modeling, Code Generation, Reasoning, Instruction Following, Structural Understanding |
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

### Step 1: Geospatial Normalization & Entity Resolution

**Inputs:** `team_half.csv`, `all_star.csv`
**Outputs:** Console output only
**Script:** `scripts/step_01_geospatial-normalization-entity-resoluti.py`

**Purpose:**
Let me break down this comprehensive data transformation task systematically:

1. **Task Understanding**:
- We have two CSV files: all_star (player-level data) and team_half (team performance data)
- Need to perform multi-step transformations on both tables before integration
- Final output requires feature engineering and normalization

2. **Approach Planning**:
Phase 1: Data Inspection
- First need to understand both datasets' structure and quality
- Check for missing values, data types, and d

---

### Step 2: Data Cleaning & Standardization: all_star Processing Priorities

**Inputs:** `all_star.csv`
**Outputs:** `processed_all_star.csv`
**Script:** `scripts/step_02_data-cleaning-standardization-allstar-pr.py`

**Purpose:**
Given this understanding, here's my refined transformation plan:

1. **all_star Processing Priorities**:
- Handle the massive starting_pos missingness by:
  * Creating an explicit 'NA' category
  * Making it ordered categorical (1 < 2 < ... < NA)
- Implement careful game_id parsing with validation
- Use median imputation for gp within team/year/league groups

2. **team_half Processing Strategy**:
- Simple aggregation since data is clean
- Need to handle division encoding carefully (div_id has W/

---

### Step 3: Revised Analysis & Refinement

**Inputs:** `team_half.csv`, `all_star.csv`
**Outputs:** `processed_all_star_fixed.csv`, `processed_team_half.csv`
**Script:** `scripts/step_03_revised-analysis-refinement.py`

**Purpose:**
To resolve this, we should:

1. **Fix the NaN Handling**:
- First identify remaining NaN values
- Then properly convert them to 'NA' category
- Ensure no duplicate category addition

2. **Revised Approach**:
- Check for NaN values in starting_pos
- Use proper categorical conversion without redundant adds
- Maintain all other transformations

3. **Implementation Plan**:
1. Fix the starting_pos NaN handling
2. Verify the fix
3. Continue with team_half processing

Let me modify the code to handle t

---

### Step 4: Data Cleaning & Standardization: Revise the Starting Position Handling

**Inputs:** `all_star.csv`
**Outputs:** `processed_all_star_corrected.csv`
**Script:** `scripts/step_04_data-cleaning-standardization-revise-the.py`

**Purpose:**
To resolve these issues, we need to:

1. **Revise the Starting Position Handling**:
- First preserve existing numeric values
- Then convert only true missing values to 'NA'
- Finally apply categorical ordering

2. **Implementation Strategy**:
- Use pd.NA for missing values instead of numpy.nan
- Ensure proper type conversion before categorical
- Add validation checks at each step

3. **Quality Assurance**:
- Verify value counts after each transformation
- Check for data preservation
- Ensure joi

---

### Step 5: Data Cleaning & Standardization: Revise Validation Approach

**Inputs:** `all_star.csv`
**Outputs:** `processed_all_star_final.csv`
**Script:** `scripts/step_05_data-cleaning-standardization-revise-val.py`

**Purpose:**
To resolve this, we'll:

1. **Revise Validation Approach**:
- Compare original and converted data before categorical conversion
- Use non-categorical methods for verification
- Preserve dtype integrity

2. **Implementation Plan**:
1. Perform validation before final categorical conversion
2. Use value counts comparison instead of crosstab
3. Add safety checks at each stage

3. **Safety Measures**:
- Store intermediate results for verification
- Add explicit dtype checks
- Document all validation 

---

### Step 6: Data Cleaning & Standardization: Core Problem

**Inputs:** `all_star.csv`
**Outputs:** `all_star_final_processed.csv`
**Script:** `scripts/step_06_data-cleaning-standardization-core-probl.py`

**Purpose:**
The execution results show we're still facing a critical issue with the starting_pos conversion - all values are being converted to NaN despite our careful approach. This suggests we need a fundamentally different strategy. Here's my analysis:

1. **Core Problem**:
- The numeric-to-string conversion isn't preserving the original values
- All values are being converted to NaN in the final output
- The categorical conversion is working, but receiving empty data

2. **Root Cause**:
- The string con

---

### Step 7: Data Merging & Integration

**Inputs:** `all_star_final_processed.csv`, `team_half.csv`
**Outputs:** `final_integrated_dataset.csv`
**Script:** `scripts/step_07_data-merging-integration.py`

**Purpose:**
With the all_star data successfully processed, we'll now:

1. **Complete Team Processing**:
- Finalize team_half aggregations
- Implement categorical encoding
- Calculate derived metrics

2. **Integration Plan**:
- Perform left join on (year, league_id, team_id)
- Handle any missing team data gracefully
- Preserve all validation flags from all_star

3. **Feature Engineering**:
- Implement the planned advanced features
- Ensure proper normalization
- Document all transformations

Here's the code 

---

### Step 8: Revised Analysis & Refinement (Phase 2)

**Inputs:** `all_star_final_processed.csv`, `team_half.csv`
**Outputs:** `final_integrated_dataset_robust.csv`
**Script:** `scripts/step_08_revised-analysis-refinement-phase-2.py`

**Purpose:**
To resolve this, we need to:

1. **Adjust Integration Strategy**:
- Keep all player records regardless of team data availability
- Modify feature engineering to handle missing team data
- Add indicators for data availability

2. **Implementation Plan**:
1. Add missing data indicators
2. Adjust feature calculations to handle NaN
3. Preserve core player information
4. Document limitations

3. **Revised Feature Engineering**:
- Create availability flags
- Set default values for missing team metrics

---

### Step 9: Data Merging & Integration (Phase 2)

**Inputs:** `all_star_final_processed.csv`, `team_half.csv`
**Outputs:** `enhanced_all_star_dataset_final.csv`
**Script:** `scripts/step_09_data-merging-integration-phase-2.py`

**Purpose:**
To resolve this, we'll:

1. **Revise Position Frequency Calculation**:
- Create dummy columns for each position first
- Then calculate frequencies
- Ensure NA values are handled properly

2. **Implementation Steps**:
1. Convert starting_pos to indicator variables
2. Calculate league-year position frequencies
3. Merge back with player data
4. Add validation checks

3. **Safety Measures**:
- Preserve original data
- Add intermediate validation
- Document each transformation

Here's the corrected i

---

### Step 10: Error Recovery & Robust Loading

**Inputs:** `all_star_final_processed.csv`, `team_half.csv`
**Outputs:** `robust_all_star_dataset.csv`
**Script:** `scripts/step_10_error-recovery-robust-loading.py`

**Purpose:**
The results show partial success but reveal new issues to address:

1. **Current Status**:
- Team data coverage remains at 1.2% (expected)
- Position frequency features are mostly NaN
- Starting_pos statistics only reflect non-NA values (1,570 records)

2. **Key Problems**:
- Position frequency calculations didn't propagate properly
- NA values in starting_pos are causing calculation issues
- Feature distributions aren't meaningful yet

3. **Required Fixes**:
1. Properly handle NA values in posi

---

### Step 11: Data Merging & Integration (Phase 3)

**Inputs:** `all_star_final_processed.csv`, `team_half.csv`
**Outputs:** `position_enhanced_dataset.csv`
**Script:** `scripts/step_11_data-merging-integration-phase-3.py`

**Purpose:**
To create meaningful features, we'll:

1. **Implement New Feature Strategy**:
- Create binary position indicators
- Calculate league-year position probabilities
- Use joint probability features
- Preserve existing team metrics

2. **Implementation Steps**:
1. Generate position dummy variables
2. Compute league position distributions
3. Create player-position interaction features
4. Normalize appropriately

3. **Feature Engineering**:
- Player position vs league expectation
- Position popularity 

---

### Step 12: Problem Diagnosis

**Inputs:** `all_star_final_processed.csv`, `team_half.csv`
**Outputs:** `era_adjusted_dataset.csv`
**Script:** `scripts/step_12_problem-diagnosis.py`

**Purpose:**
The results show our position features still lack meaningful variation. Here's a comprehensive solution:

1. **Problem Diagnosis**:
- All position scores show zero variation (single value)
- The multiplicative approach isn't capturing differences
- Need fundamentally different feature engineering

2. **New Strategy**:
1. Use position indicators directly
2. Calculate position popularity by era
3. Create player-position interaction features
4. Incorporate temporal trends

3. **Implementation Plan*

---


## Final Output & Deliverables

After multiple iterations of refinement, we've developed a comprehensive solution for the data transformation and integration task. Here's the final summary:

1. **Key Outcomes**:
- Successfully processed 5,069 All-Star records spanning 1933-2015
- Created meaningful player-centric features despite limited team data (1.2% coverage)
- Developed era-adjusted position features and player consistency metrics
- Preserved all original records while adding valuable contextual information

2. **Final Dataset Features**:
- **Player Identification**: player_id, year, league_id, team_id
- **Temporal Context**: decade, years_active, total_appearances
- **Position Analysis**: starting_pos, era-adjusted position features
- **Team Performance**: win_pct (where available), has_team_data flag
- **Specialization Metrics**: position-specific consistency measures

3. **Technical Implementation**:
- Robust handling of missing position data (3,489 NA values)
- Era-based normalization for fair historical comparisons
- Min-max scaling for all numeric features
- Comprehensive validation at each processing stage

4. **Data Quality Insights**:
- Team data is only available for 1981 (61 records)
- Position distribution shows expected patterns (1-9 + 10 for DH)
- Player appearances range from single-year to multi-decade participants

5. **Usage Recommendations**:
- For analyses requiring team performance, filter on has_team_data=1
- Era-adjusted features enable fair cross-decade comparisons
- Position specialization metrics identify versatile vs specialized players

The final dataset ('era_adjusted_dataset.csv') provides a robust foundation for analyzing All-Star player characteristics across baseball history, with features that account for the temporal and positional context of each appearance.

```python
# Example code to load and analyze the final dataset
import pandas as pd
import matplotlib.pyplot as plt

final_data = pd.read_csv('era_adjusted_dataset.csv')

# Plot position distribution by decade
positions = ['1','2','3','4','5','6','7','8','9','10','NA']
pos_counts = final_data.groupby('decade')[['starting_pos']].value_counts().unstack()
pos_counts.plot(kind='bar', stacked=True, figsize=(12,6))
plt.title('All-Star Position Distribution by Decade')
plt.ylabel('Count')
plt.show()

# Analyze player specialization
top_players = final_data.groupby('player_id')[['total_appearances']].max().nlargest(10, 'total_appearances')
print("Players with Most All-Star Appearances:")
print(top_players)
```

This solution provides a comprehensive, analytically-ready dataset that preserves the richness of the original All-Star data while adding valuable contextual features for deeper analysis.


---

## How to Run

### Local Execution
```bash
# Install dependencies
pip install pandas openpyxl

# Run each step sequentially
cd case_4027_23912
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
