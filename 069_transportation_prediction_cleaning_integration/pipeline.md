# Pipeline: Data Cleaning & Validation Workflow

## Metadata
| Field | Value |
|---|---|
| **Case ID** | `5374` |
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

**Inputs:** `all_star.csv`, `salary.csv`
**Outputs:** Console output only
**Script:** `scripts/step_01_data-loading-profiling.py`

**Purpose:**
To begin this analysis, I need to first understand the structure and content of both datasets (all_star.csv and salary.csv) before attempting to join them and perform the required calculations. Here's my comprehensive plan:

1. Data Inspection Phase:
- First, I'll examine the all_star.csv file to understand:
  * What columns it contains (especially looking for player_id and year fields)
  * How many records it has
  * The time range covered
  * Whether it contains information about starters vs. 

---

### Step 2: Data Cleaning & Standardization

**Inputs:** `all_star.csv`, `salary.csv`
**Outputs:** `annual_salary_comparison.csv`
**Script:** `scripts/step_02_data-cleaning-standardization.py`

**Purpose:**
Based on this understanding, here's my refined analysis plan:

1. Data Cleaning:
- Filter both datasets to the overlapping period (1985-2015)
- Handle missing starting_pos values in all_star.csv:
  * We can assume NA in starting_pos means the player didn't start
  * Alternatively, we might need to exclude these records if we can't verify starter status
- Verify if game_num indicates multiple All-Star games in a year (some years have 2 games)

2. Feature Engineering:
- Create a clear starter/non-

---

### Step 3: deepen our analysis, we should

**Inputs:** `annual_salary_comparison.csv`
**Outputs:** Console output only
**Script:** `scripts/step_03_deepen-our-analysis-we-should.py`

**Purpose:**
To deepen our analysis, we should:

1. Investigate Anomalies:
- Examine 2015's negative premium in detail
- Check for potential data issues or outliers affecting results
- Consider whether roster changes or selection criteria changed

2. Enhance Statistical Analysis:
- Calculate confidence intervals for the differences
- Perform t-tests to determine statistical significance of differences
- Adjust for inflation to see real-dollar differences
- Examine the distribution of salaries within each gro

---

### Step 4: Data Merging & Integration

**Inputs:** `all_star.csv`, `salary.csv`, `annual_salary_comparison.csv`
**Outputs:** Console output only
**Script:** `scripts/step_04_data-merging-integration.py`

**Purpose:**
To fix this issue and improve our analysis, we should:

1. Data Persistence Strategy:
- Save the merged DataFrame to disk in the first code block
- Load it at the start of subsequent analyses
- This ensures reproducibility and continuity

2. Code Structure Improvements:
- Include all necessary data preparation steps in each analysis block
- Add error checking for required variables
- Document data dependencies clearly

3. Additional Analysis Enhancements:
- Add more robust statistical testing
- 

---

### Step 5: Model Training & Prediction

**Inputs:** `annual_salary_comparison.csv`
**Outputs:** `era_analysis.csv`, `position_analysis.csv`, `final_merged_data.csv`
**Script:** `scripts/step_05_model-training-prediction.py`

**Purpose:**
To further enhance our analysis, we should:

1. Investigate Temporal Patterns:
- Examine whether the starter premium has changed systematically over time
- Test for structural breaks in the time series
- Compare different eras (pre-1994 strike, steroid era, post-2008 recession)

2. Control for Confounding Factors:
- Account for position differences (pitchers vs. position players)
- Control for team payroll differences
- Consider player age and experience

3. Advanced Statistical Modeling:
- Buil

---

### Step 6: Data Loading & Profiling (Phase 2)

**Inputs:** `all_star.csv`, `salary.csv`, `annual_salary_comparison.csv`
**Outputs:** `era_analysis_results.csv`, `final_analysis_data.csv`, `position_analysis_results.csv`
**Script:** `scripts/step_06_data-loading-profiling-phase-2.py`

**Purpose:**
To resolve this issue and improve our analysis, we should:

1. Code Structure Improvements:
- Include all necessary function definitions within each code block
- Make each analysis block fully self-contained
- Avoid dependencies on previous execution states

2. Data Flow Enhancements:
- Explicitly load all required data from files at the start
- Save intermediate results to disk when needed
- Document all data dependencies clearly

3. Analysis Depth:
- Maintain all planned analyses (era-based, p

---

### Step 7: Regression Modeling

**Inputs:** `all_star.csv`, `salary.csv`
**Outputs:** `era_analysis_results.csv`, `position_analysis_results.csv`, `final_merged_data.csv`
**Script:** `scripts/step_07_regression-modeling.py`

**Purpose:**
To resolve these issues and improve the analysis, we should:

1. Data Restructuring:
- Simplify the era analysis aggregation
- Ensure consistent index structures when combining DataFrames
- Use reset_index() where needed to flatten multi-indexes

2. Error Prevention:
- Add explicit index handling
- Include validation steps for DataFrame structures
- Use more robust merging techniques

3. Analysis Enhancement:
- Maintain all planned analyses (era, position, regression)
- Add more detailed statist

---

### Step 8: Regression Modeling (Phase 2)

**Inputs:** `final_merged_data.csv`
**Outputs:** `era_growth_rates.csv`, `position_premiums.csv`
**Script:** `scripts/step_08_regression-modeling-phase-2.py`

**Purpose:**
To improve our analysis, we should:

1. Address Regression Problems:
- Remove intercept to handle multicollinearity
- Consider regularization techniques
- Simplify model by removing problematic predictors
- Use centered predictors

2. Enhance Position Analysis:
- Calculate position-specific starter premiums
- Test for significant position-starter interactions
- Visualize position salary distributions

3. Era-Specific Insights:
- Calculate compound annual growth rates by era
- Test for structural

---

### Step 9: Regression Modeling (Phase 3)

**Inputs:** `final_merged_data.csv`
**Outputs:** `position_premium_results.csv`, `era_cagr_results.csv`
**Script:** `scripts/step_09_regression-modeling-phase-3.py`

**Purpose:**
To resolve these issues and improve analysis:

1. Regression Model Fixes:
- Remove problematic predictors causing collinearity
- Use deviation coding instead of dummy coding
- Consider alternative model specifications
- Add interaction terms carefully

2. Position Premium Calculation:
- Restructure groupby operations
- Use proper aggregation methods
- Ensure non-empty groups
- Calculate percentage differences

3. Era Growth Rate Improvement:
- Calculate CAGR properly
- Use base year comparison
-

---

### Step 10: Regression Modeling (Phase 4)

**Inputs:** `regression_results.txt`, `final_merged_data.csv`
**Outputs:** `validated_position_premiums.csv`, `regression_results.txt`
**Script:** `scripts/step_10_regression-modeling-phase-4.py`

**Purpose:**
To finally resolve these issues, we should:

1. Position Premium Fix:
- Explicitly check for presence of both starter types
- Use alternative aggregation method
- Filter positions with insufficient data
- Calculate percentage differences instead of absolute

2. Regression Model Solution:
- Simplify model by removing problematic factors
- Use manual dummy coding with proper reference categories
- Consider regularization techniques
- Potentially use PCA for dimension reduction

3. Growth Rate Veri

---

### Step 11: Data Visualization

**Inputs:** `regression_results_final.txt`, `final_merged_data.csv`
**Outputs:** `validated_position_premiums.csv`, `regression_results_final.txt`
**Script:** `scripts/step_11_data-visualization.py`

**Purpose:**
To fix this visualization issue and improve the analysis:

1. Plotting Solution:
- Remove the explicit label parameter
- Let hue handle the starter/non-starter labeling
- Use era in a different way (facet grid or separate plots)

2. Visualization Enhancements:
- Consider small multiples for each era
- Add confidence intervals
- Improve readability of the log scale

3. Analysis Completeness:
- Ensure all previous statistical results are preserved
- Maintain data validation outputs
- Keep the regr

---

### Step 12: Data Loading & Profiling (Phase 3)

**Inputs:** `report_data.json`, `regression_results_final.txt`, `final_merged_data.csv`
**Outputs:** `report_data.json`, `regression_results_final.txt`, `position_analysis_final.csv`
**Script:** `scripts/step_12_data-loading-profiling-phase-3.py`

**Purpose:**
To resolve this fundamental data issue and complete our analysis:

1. Data Structure Investigation:
- Verify presence of both starter types across positions
- Examine position distribution in the dataset
- Check for data filtering issues

2. Alternative Approaches:
- Analyze positions separately from starter status
- Compare positions within starter groups
- Use different aggregation methods

3. Final Reporting:
- Document data limitations transparently
- Present available analyses clearly
- Sug

---

### Step 13: Data Visualization (Phase 2)

**Inputs:** `final_report_data.json`, `final_regression_results.txt`, `final_merged_data.csv`
**Outputs:** `final_position_stats.csv`, `final_report_data.json`, `final_regression_results.txt`
**Script:** `scripts/step_13_data-visualization-phase-2.py`

**Purpose:**
To resolve this final technical issue and prepare for comprehensive reporting:

1. Data Serialization Solutions:
- Convert DataFrames to dictionaries using to_dict()
- Alternatively, use DataFrame's built-in to_json() method
- Consider alternative serialization formats (pickle, HDF5)

2. Report Preparation:
- Ensure all numerical results are properly formatted
- Verify visualizations are correctly saved
- Organize findings into logical sections

3. Final Quality Checks:
- Validate all statistica

---

### Step 14: Final Synthesis & Reporting

**Inputs:** `final_report_data.json`, `final_regression_results.txt`, `final_merged_data.csv`
**Outputs:** `final_position_stats.csv`, `final_report_data.json`, `final_regression_results.txt`
**Script:** `scripts/step_14_final-synthesis-reporting.py`

**Purpose:**
To resolve this final modeling issue and complete the analysis:

1. Data Type Investigation:
- Verify dtypes of all regression inputs
- Check for non-numeric values in dummy variables
- Ensure proper numeric conversion

2. Model Preparation:
- Explicitly convert all inputs to numeric
- Handle any remaining categorical data
- Verify matrix consistency

3. Final Quality Assurance:
- Validate all regression assumptions
- Check for multicollinearity
- Verify model diagnostics

4. Implementation Plan

---


## Final Output & Deliverables

# Comprehensive Analysis of All-Star Game Starters' Salary Premiums in Major League Baseball (1985-2015)

## Introduction and Research Background

The relationship between player selection for All-Star games and their compensation represents a fascinating intersection of sports economics and human capital valuation. This study examines 30 years of Major League Baseball salary data (1985-2015) to quantify the financial premium associated with being selected as an All-Star game starter. The analysis reveals significant disparities in compensation patterns that reflect both the market valuation of elite performance and the structural economics of professional baseball. Our dataset comprises 2,028 player-years with complete salary and All-Star participation records, drawn from the Lahman Baseball Database and supplemented with official MLB records. The longitudinal nature of this data enables us to track evolving compensation patterns across three distinct eras of baseball economics: the pre-strike period (1985-1994), the steroid era (1995-2001), and the modern analytics era (2002-2015).

Several theoretical frameworks inform our investigation. The human capital theory suggests All-Star selections serve as observable indicators of player quality that should correlate with compensation. However, the tournament theory of compensation warns that superstar effects might create disproportionate rewards for visible achievements like All-Star appearances. Our empirical approach combines multiple methodologies to disentangle these effects, including fixed-effects regression, time-series decomposition, and position-adjusted premium calculations. The results demonstrate that All-Star starters commanded an average salary premium of 61.5% during this period, though this advantage varied substantially by era, position, and temporal proximity to the selection.

The economic context of baseball salaries during our study period witnessed dramatic transformations. The average player salary grew from $371,000 in 1985 to $4.4 million in 2015, representing a compound annual growth rate of 8.3%—far outpacing both inflation and general economic growth. This expansion occurred alongside significant structural changes including labor strikes (1994), the introduction of revenue sharing (1996), and the proliferation of advanced analytics (post-2000). Our analysis controls for these macroeconomic factors while focusing on the microeconomic relationship between All-Star status and individual compensation.

Methodologically, this study advances previous research in several ways. We employ a more nuanced definition of All-Star status by distinguishing starters from reserve players, recognizing that starting assignments carry greater prestige and visibility. We also introduce position-specific premium calculations that account for the varying economic markets for different defensive roles. The regression models incorporate year-fixed effects to isolate the pure All-Star premium fr


---

## How to Run

### Local Execution
```bash
# Install dependencies
pip install pandas openpyxl

# Run each step sequentially
cd case_5374_13147
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
