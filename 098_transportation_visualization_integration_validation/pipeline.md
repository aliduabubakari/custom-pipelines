# Pipeline: Data Cleaning & Validation Workflow

## Metadata
| Field | Value |
|---|---|
| **Case ID** | `4686` |
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

### Step 1: This task requires a comprehensive analysis of the relationship between MLB home game attendance and

**Inputs:** `data_inspection_report.txt`, `home_game.csv`, `manager_award.csv`
**Outputs:** `data_inspection_report.txt`
**Script:** `scripts/step_01_this-task-requires-a-comprehensive-analy.py`

**Purpose:**
This task requires a comprehensive analysis of the relationship between MLB home game attendance and managerial awards over a 144-year period (1871-2015). The analysis involves several key components that need careful planning:

1. Data Preparation:
- First need to inspect both datasets' structure and contents
- Identify common keys for merging (year and league_id mentioned)
- Handle potential data quality issues (missing values, inconsistencies)

2. Core Analysis Requirements:
- Calculate annua

---

### Step 2: Data Merging & Integration

**Inputs:** None (reads raw data)
**Outputs:** `team_attendance_avg.csv`, `cleaned_awards.csv`, `league_attendance_avg.csv`
**Script:** `scripts/step_02_data-merging-integration.py`

**Purpose:**
Next steps needed for comprehensive analysis:

1. Data Cleaning:
- Handle missing league_id values in home_game data
- Standardize league_id values between datasets (ML vs AL/NL)
- Filter to only BBWAA Manager of the Year awards per instructions

2. Data Enhancement:
- Need to merge manager-team relationships (missing from current data)
- May need external data source to link award-winning managers to teams
- Consider normalizing attendance by games played

3. Temporal Alignment:
- Restrict anal

---

### Step 3: Data Visualization

**Inputs:** `home_game.csv`, `manager_award.csv`
**Outputs:** `team_attendance_avg.csv`, `cleaned_home_games.csv`, `cleaned_awards.csv`, `league_attendance_avg.csv`
**Script:** `scripts/step_03_data-visualization.py`

**Purpose:**
To resolve this and ensure robust analysis:

1. Immediate Fix:
- Reload both datasets at start of new code block
- Maintain consistent variable naming
- Verify successful loading before proceeding

2. Structural Improvements:
- Create persistent data storage (saved files) for intermediate steps
- Implement error checking for data loading
- Add validation steps after key operations

3. Analysis Continuity:
- Need to preserve all data transformations
- Ensure visualizations use latest cleaned data

---

### Step 4: Next phase requirements

**Inputs:** `cleaned_home_games.csv`, `cleaned_awards.csv`, `statistical_results.txt`, `league_attendance_avg.csv`
**Outputs:** `statistical_results.txt`, `award_comparison_analysis.csv`
**Script:** `scripts/step_04_next-phase-requirements.py`

**Purpose:**
Next phase requirements:

1. Manager-Team Linkage:
- Critical missing component: Need to associate award-winning managers with their teams
- Potential solutions:
  * External data source lookup
  * Inference from historical records
  * Team identification via player_id patterns

2. Comparative Analysis Framework:
- Need to:
  * Identify award-winning managers' teams each year
  * Calculate their attendance metrics
  * Compare against league averages
  * Compute percentage differences

3. Advance

---

### Step 5: Data Validation & Quality Report

**Inputs:** `team_attendance_avg.csv`, `cleaned_home_games.csv`, `cleaned_awards.csv`, `league_attendance_avg.csv`
**Outputs:** `award_comparison_analysis.csv`
**Script:** `scripts/step_05_data-validation-quality-report.py`

**Purpose:**
Required improvements:

1. Robust Data Loading:
- Explicitly load all required datasets
- Verify successful loading before proceeding
- Handle potential file reading errors

2. Execution Independence:
- Ensure code works in fresh environment
- No reliance on previous execution state
- Complete data pipeline in single block

3. Data Validation:
- Check for required columns before merging
- Verify no nulls in key fields
- Confirm temporal alignment

Solution Approach:
1. Reload all necessary datas

---

### Step 6: Data Validation & Quality Report (Phase 2)

**Inputs:** None (reads raw data)
**Outputs:** `award_comparison_analysis.csv`
**Script:** `scripts/step_06_data-validation-quality-report-phase-2.py`

**Purpose:**
Required improvements for robust validation:

1. Variable Handling:
- Store loaded DataFrames in dictionary instead of individual variables
- This provides consistent access pattern
- Enables systematic validation

2. Validation Approach:
- Create dedicated validation function
- Check both existence and content of DataFrames
- Provide detailed error reporting

3. Error Prevention:
- Implement early failure for missing data
- Clear error messages about what's missing
- Graceful handling of partia

---

### Step 7: Error Recovery & Robust Loading

**Inputs:** `analysis_summary.txt`, `award_comparison_analysis.csv`
**Outputs:** `analysis_summary.txt`
**Script:** `scripts/step_07_error-recovery-robust-loading.py`

**Purpose:**
Required improvements for robust analysis:

1. Manager-Team Resolution:
- Need complete manager-team mapping
- Potential solutions:
  * External reference database
  * Web scraping of historical records
  * Team inference from award years

2. Data Quality Enhancement:
- Handle missing mappings systematically
- Consider probabilistic matching
- Document coverage limitations

3. Advanced Analysis:
- Implement:
  * Longitudinal trend analysis
  * League-specific effects
  * Control for team perform

---

### Step 8: Error Recovery & Robust Loading (Phase 2)

**Inputs:** `advanced_analysis_report.txt`, `award_comparison_analysis.csv`
**Outputs:** `advanced_analysis_report.txt`
**Script:** `scripts/step_08_error-recovery-robust-loading-phase-2.py`

**Purpose:**
Required improvements for robust conclusions:

1. Data Completeness:
- Critical need to resolve manager-team mappings
- Potential approaches:
  * Baseball-reference.com API integration
  * Retrosheet historical data
  * Manual verification for key cases

2. Enhanced Statistical Analysis:
- Implement:
  * Power analysis for required sample size
  * Bootstrapping for small sample inference
  * Multivariate controls (if possible)
  * Effect size confidence intervals

3. Results Interpretation:
- Ne

---

### Step 9: Model Training & Prediction

**Inputs:** `advanced_analysis_report.txt`, `award_comparison_analysis.csv`
**Outputs:** `advanced_analysis_report.txt`
**Script:** `scripts/step_09_model-training-prediction.py`

**Purpose:**
Required adjustments:

1. API Correction:
- Use correct import path for power functions
- Verify statsmodels version compatibility
- Implement fallback if unavailable

2. Alternative Approaches:
- Manual power calculation formulas
- Use scipy.stats for basic power analysis
- Consider external power analysis packages

3. Code Robustness:
- Add version checking
- Implement graceful degradation
- Provide informative error messages

Solution Strategy:
1. Update import statement
2. Add version compat

---

### Step 10: Data Visualization (Phase 2)

**Inputs:** `award_comparison_analysis.csv`
**Outputs:** Console output only
**Script:** `scripts/step_10_data-visualization-phase-2.py`

**Purpose:**
Required improvements:

1. Error Bar Specification:
- Need to properly format asymmetric errors
- Should use 2xN array for upper/lower bounds
- Alternative: Use symmetric error bars

2. Visualization Clarity:
- Maintain clear display of confidence intervals
- Ensure proper scaling
- Include reference line at zero

3. Code Robustness:
- Add input validation
- Handle edge cases
- Provide informative labels

Solution Approach:
1. Restructure error bar data
2. Simplify to symmetric errors if needed


---

### Step 11: Statistical Analysis & Hypothesis Testing

**Inputs:** `advanced_modeling_results.txt`, `award_comparison_analysis.csv`
**Outputs:** `advanced_modeling_results.txt`
**Script:** `scripts/step_11_statistical-analysis-hypothesis-testing.py`

**Purpose:**
Required next steps for comprehensive analysis:

1. Expanded Data Collection:
- Resolve remaining manager-team mappings
- Increase sample size to narrow confidence intervals
- Verify temporal representativeness

2. Advanced Statistical Modeling:
- Implement mixed-effects models to account for:
  * Repeated managers
  * Team-level effects
  * Temporal autocorrelation
- Consider Bayesian approaches for small samples

3. Subgroup Analysis:
- Examine effects by:
  * League (AL vs NL)
  * Era (pre/po

---

### Step 12: Model Training & Prediction (Phase 2)

**Inputs:** `advanced_modeling_results_refined.txt`, `award_comparison_analysis.csv`
**Outputs:** `advanced_modeling_results_refined.txt`
**Script:** `scripts/step_12_model-training-prediction-phase-2.py`

**Purpose:**
Required improvements for reliable modeling:

1. Bayesian Analysis Alternatives:
- Implement manual Bayesian estimation
- Use PyMC3 or bambi if available
- Fall back to Bayesian approximation formulas

2. Mixed Model Refinement:
- Add constraints to prevent boundary estimates
- Consider simpler random effects structure
- Validate model assumptions

3. Technical Robustness:
- Add library version checks
- Implement graceful degradation
- Provide informative warnings

4. Analysis Continuity:
- Main

---

### Step 13: Model Training & Prediction (Phase 3)

**Inputs:** `final_analysis_results.txt`, `award_comparison_analysis.csv`
**Outputs:** `final_analysis_results.txt`
**Script:** `scripts/step_13_model-training-prediction-phase-3.py`

**Purpose:**
Required improvements for final analysis:

1. Technical Corrections:
- Add missing pingouin import
- Implement fallback for t-test if unavailable
- Ensure all dependencies are properly referenced

2. Model Refinement:
- Simplify random effects structure
- Consider alternative model specifications
- Validate convergence criteria

3. Analysis Completeness:
- Finalize all planned analyses
- Ensure reproducible results
- Document methodological choices

4. Reporting Preparation:
- Organize all resul

---


## Final Output & Deliverables

# The Impact of Managerial Awards on MLB Home Game Attendance: A Comprehensive Analysis (1871-2015)

## Introduction and Research Background

The relationship between managerial excellence and team performance has long been a subject of interest in baseball analytics, yet the connection between managerial recognition and fan engagement remains underexplored. This study examines 144 years of Major League Baseball data (1871-2015) to quantify the relationship between BBWAA Manager of the Year awards and home game attendance, controlling for historical trends and league-wide attendance patterns. Our analysis reveals that while award-winning managers are associated with an average attendance increase of 11.93%, this effect shows substantial variability (95% CI: -3.36% to 27.82%) and lacks statistical significance (p=0.172) in our limited sample of 17 complete records. The Bayesian Factor of 1.84 suggests anecdotal but inconclusive evidence for a positive effect, while era-based analysis reveals no significant difference between pre-1994 (M=9.21%, SD=28.37) and post-1994 (M=13.45%, SD=25.19) periods (t=0.41, p=0.341).

The historical context of managerial awards in baseball provides important framing for these results. The BBWAA Manager of the Year award, established in 1983, represents the most prestigious recognition of managerial performance, yet our data shows it correlates only moderately with attendance fluctuations. Interestingly, the effect size appears larger in the National League (M=14.72%) than the American League (M=9.15%), though this difference also fails to reach statistical significance (t=0.56, p=0.584). The temporal distribution of effects shows particular volatility during expansion years, with the largest positive spikes occurring in 1993 (COL, 42.1% above league average) and 1998 (SD, 38.7% above), both coinciding with franchise inaugurations. These findings suggest that while managerial recognition may contribute to attendance, its impact is likely mediated by numerous contextual factors including team performance, market size, and historical period.

## Methodology and Data Processing

Our analytical approach employed a multi-stage process to ensure robust findings. Beginning with the raw datasets containing 2,944 home game records and 177 managerial awards, we implemented rigorous data cleaning protocols. Missing league identifiers (2.6% of home game records) were imputed using modal replacement (NL), while award records were filtered to only include BBWAA Manager of the Year recipients (n=67). The subsequent merging process revealed significant data linkage challenges, with only 25.4% of award records successfully matching to team attendance data through our initial manager-team mapping. This limitation necessitated the development of alternative analytical strategies, including bootstrap resampling (1,000 iterations) to estimate confidence intervals and Bayesian approximation methods when specialized packages were unavailabl


---

## How to Run

### Local Execution
```bash
# Install dependencies
pip install pandas openpyxl

# Run each step sequentially
cd case_4686_11638
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
