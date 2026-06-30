# Pipeline: Data Cleaning & Validation Workflow

## Metadata
| Field | Value |
|---|---|
| **Case ID** | `5558` |
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

**Inputs:** `team_inspection.txt`, `all_star.csv`, `team.csv`, `all_star_inspection.txt`
**Outputs:** `team_inspection.txt`, `all_star_inspection.txt`
**Script:** `scripts/step_01_data-loading-profiling.py`

**Purpose:**
To begin this comprehensive analysis, I will first develop a structured approach to examine the correlation between player starting positions in all-star games and team statistics. Here's my multi-phase analytical plan:

1. Data Exploration Phase:
- First need to understand both datasets' structure and contents
- Examine all_star.csv for player positions and game details
- Explore team.csv for team performance statistics
- Identify common keys between datasets (likely team IDs or names)

2. Data

---

### Step 2: Data Cleaning & Standardization

**Inputs:** `all_star.csv`, `team.csv`
**Outputs:** Console output only
**Script:** `scripts/step_02_data-cleaning-standardization.py`

**Purpose:**
To properly capture DataFrame information for our analysis, we should:

1. Replace the info() method calls with alternative approaches:
   - Use dtypes property for column types
   - Use isnull().sum() for missing value counts
   - Use shape for dimensions
   - Use columns attribute for column names

2. Improve the inspection code to:
   - Handle the info() limitation
   - Include more comprehensive data summaries
   - Add memory usage information
   - Include value counts for categorical column

---

### Step 3: Data Loading & Profiling (Phase 2)

**Inputs:** `all_star.csv`, `team.csv`
**Outputs:** `cleaned_team.csv`, `cleaned_all_star.csv`
**Script:** `scripts/step_03_data-loading-profiling-phase-2.py`

**Purpose:**
Next steps in our analysis should focus on:

1. Data Quality Assessment:
- Examine missing value patterns in both datasets
- Identify any data inconsistencies
- Check for duplicate records

2. Feature Understanding:
- Identify position-related columns in all_star.csv
- Categorize team statistics in team.csv (offensive, defensive, etc.)
- Determine temporal aspects (season/year columns)

3. Join Strategy Development:
- Identify common identifiers between datasets
- Determine appropriate merge con

---

### Step 4: Data Loading & Profiling (Phase 3)

**Inputs:** `column_analysis.txt`, `all_star.csv`, `team.csv`
**Outputs:** `column_analysis.txt`
**Script:** `scripts/step_04_data-loading-profiling-phase-3.py`

**Purpose:**
To properly address this, we should:

1. First verify all column names in both datasets
2. Identify which columns contain position information
3. Check for alternative naming conventions (e.g., 'position', 'player_position')
4. Examine the data dictionary if available in the files
5. Adjust our visualization plan based on actual columns

The corrected approach should:
- Print all column names first
- Identify position-related columns through pattern matching
- Handle cases where position data mi

---

### Step 5: Data Cleaning & Standardization (Phase 2)

**Inputs:** `column_analysis.txt`, `all_star.csv`, `team.csv`
**Outputs:** `column_analysis.txt`
**Script:** `scripts/step_05_data-cleaning-standardization-phase-2.py`

**Purpose:**
To resolve this and continue our analysis:

1. We need to ensure clean Python code without markdown formatting
2. The previous code logic was sound and should be maintained
3. We should add additional error handling for robustness
4. Include verification steps to confirm successful execution

The corrected approach will:
- Remove all markdown formatting artifacts
- Maintain the same analytical logic
- Add verification prints
- Include try-except blocks for critical operations

Here's the clean, 

---

### Step 6: Data Merging & Integration

**Inputs:** `all_star.csv`, `team.csv`
**Outputs:** `position_team_merge.csv`
**Script:** `scripts/step_06_data-merging-integration.py`

**Purpose:**
Next steps for comprehensive analysis:

1. Data Alignment:
- Verify team_id consistency between datasets
- Check year ranges for overlap
- Examine league_id correspondence

2. Position Analysis:
- Analyze distribution of starting positions
- Examine position trends over time
- Identify most common positions

3. Team Stat Adjustment:
- Identify relevant baseball metrics to analyze
- Select stats that might correlate with positions
- Create normalized metrics for comparison

4. Merge Preparation:


---

### Step 7: Statistical Analysis & Hypothesis Testing

**Inputs:** `position_team_merge.csv`
**Outputs:** `feature_importance.csv`, `significant_correlations.csv`
**Script:** `scripts/step_07_statistical-analysis-hypothesis-testing.py`

**Purpose:**
To deepen our analysis, we should:

1. Decode Position Numbers:
- Map numeric positions to baseball positions
- Verify if 0.0 and 10.0 represent special cases

2. Advanced Correlation Analysis:
- Calculate correlation coefficients between positions and stats
- Identify statistically significant relationships
- Control for year/era effects

3. Temporal Analysis:
- Examine how position-performance relationships change over time
- Identify distinct historical periods
- Account for rule changes

4. 

---

### Step 8: Statistical Analysis & Hypothesis Testing (Phase 2)

**Inputs:** `classification_report.txt`, `position_team_merge.csv`
**Outputs:** `classification_report.txt`, `feature_importance.csv`, `significant_correlations.csv`
**Script:** `scripts/step_08_statistical-analysis-hypothesis-testing-.py`

**Purpose:**
To resolve this and continue our advanced analysis:

1. Data Cleaning Steps Needed:
- Identify columns with inf/NaN values
- Decide on imputation or removal strategy
- Verify data distribution after cleaning

2. Analysis Adjustments:
- Add data validation before correlation calculations
- Implement robust error handling
- Consider alternative correlation methods

3. Enhanced Workflow:
- Add preprocessing pipeline
- Include data quality checks
- Document cleaning decisions

Here's the corrected c

---

### Step 9: Model Training & Prediction

**Inputs:** `position_team_merge.csv`
**Outputs:** `feature_importance.csv`, `classification_report.csv`
**Script:** `scripts/step_09_model-training-prediction.py`

**Purpose:**
To resolve this and complete our analysis:

1. Feature Engineering:
- Explicitly select numerical features for modeling
- Exclude any categorical or datetime features
- Verify dtypes before modeling

2. Data Pipeline:
- Create clear separation between features and metadata
- Implement feature validation step
- Document feature selection criteria

3. Enhanced Modeling:
- Add feature type verification
- Include feature importance analysis
- Store modeling metadata

Here's the corrected code that:


---

### Step 10: Data Cleaning & Standardization (Phase 3)

**Inputs:** `position_team_merge.csv`
**Outputs:** `cleaned_all_star_team_data.csv`, `feature_importance.csv`, `classification_report.csv`
**Script:** `scripts/step_10_data-cleaning-standardization-phase-3.py`

**Purpose:**
To resolve this and complete our analysis:

1. Data Cleaning:
- Explicitly check for and handle missing target values
- Document removal/imputation decisions
- Verify data completeness after cleaning

2. Enhanced Pipeline:
- Add target variable validation
- Implement comprehensive missing data handling
- Include data quality reporting

3. Analysis Integrity:
- Assess impact of removed records
- Maintain transparency in methodology
- Document all preprocessing steps

Here's the corrected code tha

---

### Step 11: Statistical Analysis & Hypothesis Testing (Phase 3)

**Inputs:** `position_team_merge.csv`, `model_metrics.txt`
**Outputs:** `permutation_importance.csv`, `feature_importance.csv`, `enhanced_classification_report.csv`, `model_metrics.txt`
**Script:** `scripts/step_11_statistical-analysis-hypothesis-testing-.py`

**Purpose:**
To improve our analysis, we should:

1. Address Data Quality:
- Investigate why 69% of positions are missing
- Consider alternative data sources or imputation
- Document limitations of current dataset

2. Enhance Modeling:
- Handle class imbalance through sampling
- Add evaluation metrics for imbalanced data
- Consider alternative algorithms

3. Expand Analysis:
- Include feature correlation analysis
- Add model interpretation techniques
- Perform sensitivity analysis

Here's the enhanced code t

---

### Step 12: Data Visualization

**Inputs:** `position_team_merge.csv`
**Outputs:** `final_classification_report.csv`, `permutation_importance.csv`, `feature_importance.csv`
**Script:** `scripts/step_12_data-visualization.py`

**Purpose:**
To resolve this and complete our comprehensive analysis:

1. Visualization Fix:
- Properly align error bars with plotted features
- Ensure dimensional consistency
- Maintain visualization integrity

2. Enhanced Reporting:
- Include both standard and permutation importance
- Add model interpretation metrics
- Document methodological choices

3. Final Analysis Components:
- Data quality assessment
- Feature importance comparison
- Model performance evaluation
- Strategic recommendations

Here's th

---

### Step 13: Data Visualization (Phase 2)

**Inputs:** `position_team_merge.csv`
**Outputs:** `final_classification_report.csv`, `permutation_importance.csv`, `feature_importance.csv`
**Script:** `scripts/step_13_data-visualization-phase-2.py`

**Purpose:**
To resolve this visualization challenge and complete our analysis:

1. Visualization Solution:
- Use proper error bar formatting for seaborn
- Ensure dimensional consistency
- Maintain statistical validity

2. Comprehensive Reporting:
- Include both standard and permutation importance
- Add model interpretation metrics
- Document visualization methodology

3. Final Analysis Components:
- Data quality assessment
- Feature importance comparison
- Model performance evaluation
- Strategic recommenda

---


## Final Output & Deliverables

# Comprehensive Analysis of All-Star Player Positions and Team Performance Metrics in Major League Baseball

## Introduction and Research Background

The relationship between player positions in All-Star games and team performance metrics represents a compelling intersection of individual athletic excellence and collective team success in Major League Baseball. This study examines a dataset spanning from 1933 to 2015, comprising 5,069 initial records of All-Star appearances merged with comprehensive team statistics to uncover patterns, correlations, and predictive relationships between positional representation in All-Star games and various team performance indicators. The analysis reveals several critical insights about how different positions contribute to team success, how their representation in All-Star games correlates with team metrics, and what statistical patterns emerge across different eras of baseball history. Our methodology incorporated advanced machine learning techniques including Random Forest classification with SMOTE oversampling to handle class imbalance, permutation importance analysis for feature interpretation, and comprehensive visualization approaches to elucidate complex relationships within the data.

The dataset presented several analytical challenges that required sophisticated handling, including significant missing data (with 3,489 of 5,069 initial records missing position information), class imbalance in position representation, and the need to reconcile categorical position data with continuous team performance metrics. Through systematic data cleaning, feature engineering, and multiple modeling approaches, we established robust methods for analyzing these relationships while accounting for potential confounding factors such as era-specific trends and varying team strategies. The final cleaned dataset contained 1,580 complete records with position information, representing 31.2% of the original data but providing a sufficiently large sample for meaningful analysis across all standard baseball positions. Our analytical framework focused on eight key team performance metrics (wins, losses, runs, hits, home runs, ERA, strikeouts, and attendance) that showed the strongest predictive relationships with All-Star positions.

The historical context of this analysis spans significant changes in baseball strategy and player evaluation, from the dead-ball era through the modern statistical revolution. This temporal dimension adds complexity to our analysis but also provides valuable insights into how the relationship between All-Star positions and team performance has evolved. The position mapping used in our analysis follows standard baseball conventions: 1.0 for Pitcher, 2.0 for Catcher, 3.0 for First Base, 4.0 for Second Base, 5.0 for Third Base, 6.0 for Shortstop, 7.0 for Left Field, 8.0 for Center Field, 9.0 for Right Field, and 10.0 for Designated Hitter, with 0.0 representing unknown positions that were excluded from 


---

## How to Run

### Local Execution
```bash
# Install dependencies
pip install pandas openpyxl

# Run each step sequentially
cd case_5558_13593
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
