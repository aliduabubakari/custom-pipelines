# Pipeline: Data Cleaning & Validation Workflow

## Metadata
| Field | Value |
|---|---|
| **Case ID** | `5236` |
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

**Inputs:** None (reads raw data)
**Outputs:** Console output only
**Script:** `scripts/step_01_data-loading-profiling.py`

**Purpose:**
This task requires a comprehensive analysis of the relationship between aircraft specifications and their distribution across airports. Since we don't have access to the actual data files yet, our first step must be to examine and understand the structure and content of both provided CSV files.

The analysis will proceed through several logical phases:

1. Data Inspection Phase:
   - First, we need to examine both files to understand their structure and contents
   - We should check for basic fi

---

### Step 2: Data Merging & Integration

**Inputs:** `airport_aircraft.csv`, `aircraft.csv`
**Outputs:** `cleaned_aircraft.csv`, `merged_aircraft_data.csv`
**Script:** `scripts/step_02_data-merging-integration.py`

**Purpose:**
Based on the data understanding, our next steps should focus on:

1. Data Cleaning and Transformation:
   - Extract numerical values from formatted text fields (weight, area, loading)
   - Standardize units (convert all to metric or imperial consistently)
   - Consider creating derived features (e.g., weight-to-area ratio)

2. Data Integration:
   - Perform inner join on Aircraft_ID to combine datasets
   - Verify join operation preserves all relevant records
   - Explore potential many-to-many 

---

### Step 3: Data Merging & Integration (Phase 2)

**Inputs:** None (reads raw data)
**Outputs:** `aircraft_correlations.csv`
**Script:** `scripts/step_03_data-merging-integration-phase-2.py`

**Purpose:**
With clean, merged data available, we can now proceed to deeper analysis. The following analytical directions appear promising:

1. Descriptive Statistics:
   - Calculate comprehensive statistics for numerical aircraft features
   - Examine distributions across different airport assignments
   - Compare means/medians between aircraft at different airports

2. Visualization:
   - Create scatter plots of weight vs. disk area
   - Generate bar charts of aircraft features by airport
   - Plot weight

---

### Step 4: Data Visualization

**Inputs:** `airport_aircraft.csv`, `aircraft.csv`
**Outputs:** `analysis_output/correlation_matrix.csv`
**Script:** `scripts/step_04_data-visualization.py`

**Purpose:**
To resolve this issue and enable comprehensive analysis, we should:

1. Implementation Approach:
   - Combine all data loading, cleaning, and visualization into a single code block
   - Ensure all DataFrames are available throughout the entire analysis
   - Maintain the same cleaning and transformation logic
   - Keep all visualization components

2. Additional Improvements:
   - Add more descriptive plot titles and labels
   - Include proper figure sizing for better readability
   - Save visual

---

### Step 5: Statistical Analysis & Hypothesis Testing

**Inputs:** `analysis_output/cleaned_aircraft.csv`, `analysis_output/merged_aircraft_data.csv`
**Outputs:** `analysis_output/enhanced_correlation_matrix.csv`, `analysis_output/advanced_statistics.csv`, `analysis_output/correlation_pvalues.csv`
**Script:** `scripts/step_05_statistical-analysis-hypothesis-testing.py`

**Purpose:**
To deepen our analysis, we should:

1. Address Technical Warnings:
   - Update visualization code to use recommended seaborn parameters
   - Ensure future compatibility of visualization code

2. Expand Statistical Analysis:
   - Calculate pairwise correlations between all numerical features
   - Perform significance testing on observed relationships
   - Compute effect sizes for key comparisons

3. Enhance Visualizations:
   - Add regression lines to scatter plots
   - Include confidence interva

---

### Step 6: Data Cleaning & Standardization

**Inputs:** `airport_aircraft.csv`, `aircraft.csv`
**Outputs:** `analysis_output/enhanced_correlation_matrix.csv`, `analysis_output/cleaned_aircraft.csv`, `analysis_output/advanced_statistics.csv`, `analysis_output/merged_aircraft_data.csv`, `analysis_output/correlation_pvalues.csv`
**Script:** `scripts/step_06_data-cleaning-standardization.py`

**Purpose:**
To resolve this issue and enable robust analysis, we should:

1. Implementation Strategy:
   - Make the enhanced analysis self-contained by including all data cleaning steps
   - Remove dependency on intermediate files
   - Maintain all the enhanced analytical capabilities

2. Code Structure Improvements:
   - Create a complete analysis pipeline in one function
   - Include data loading, cleaning, and analysis in sequence
   - Add error handling for file operations
   - Verify directory creation

---

### Step 7: Regression Modeling

**Inputs:** `analysis_output/enhanced_correlation_matrix.csv`, `analysis_output/cleaned_aircraft.csv`, `analysis_output/merged_aircraft_data.csv`, `analysis_output/regression_results.txt`
**Outputs:** `analysis_output/regression_results.txt`
**Script:** `scripts/step_07_regression-modeling.py`

**Purpose:**
To further enhance the analysis, we should:

1. Advanced Statistical Modeling:
   - Fit regression models to quantify relationships
   - Calculate confidence intervals for key parameters
   - Perform residual analysis for model diagnostics

2. Expanded Visualization:
   - Create 3D plots of key aircraft specifications
   - Generate radar charts for multivariate comparison
   - Add interactive visualizations for exploration

3. Domain-Specific Analysis:
   - Calculate payload efficiency metrics
 

---

### Step 8: Statistical Analysis & Hypothesis Testing (Phase 2)

**Inputs:** `analysis_output/cleaned_aircraft.csv`
**Outputs:** `analysis_output/vif_results.csv`, `analysis_output/spearman_correlations.csv`, `analysis_output/enhanced_aircraft_data.csv`, `analysis_output/bootstrap_cis.csv`
**Script:** `scripts/step_08_statistical-analysis-hypothesis-testing-.py`

**Purpose:**
To strengthen the analysis and address limitations, we should:

1. Address Small Sample Issues:
   - Implement exact permutation tests instead of parametric tests
   - Calculate non-parametric correlation measures
   - Add bootstrapped confidence intervals

2. Enhance Model Diagnostics:
   - Perform variance inflation factor analysis
   - Check model specification with link tests
   - Examine partial regression plots

3. Expand Visualization:
   - Add prediction surfaces to 3D plot
   - Include 

---

### Step 9: Statistical Analysis & Hypothesis Testing (Phase 3)

**Inputs:** `analysis_output/cleaned_aircraft.csv`
**Outputs:** `analysis_output/vif_results.csv`, `analysis_output/spearman_correlations.csv`, `analysis_output/enhanced_aircraft_data.csv`, `analysis_output/bootstrap_cis.csv`
**Script:** `scripts/step_09_statistical-analysis-hypothesis-testing-.py`

**Purpose:**
To resolve this issue and ensure robust analysis, we should:

1. Implementation Strategy:
   - Add all required import statements at function start
   - Make the analysis completely self-contained
   - Maintain all planned robust statistical methods

2. Code Structure Improvements:
   - Verify all library imports are present
   - Add error handling for missing dependencies
   - Include defensive programming checks

3. Analysis Enhancements:
   - Keep all non-parametric correlation measures
   - 

---

### Step 10: Statistical Analysis & Hypothesis Testing (Phase 4)

**Inputs:** `analysis_output/enhanced_aircraft_data.csv`
**Outputs:** Console output only
**Script:** `scripts/step_10_statistical-analysis-hypothesis-testing-.py`

**Purpose:**
To finalize the analysis and prepare for reporting, we should:

1. Final Statistical Tests:
   - Calculate effect sizes for key relationships
   - Perform pairwise comparison tests between aircraft
   - Compute power analysis for future studies

2. Reporting Preparation:
   - Generate comprehensive summary tables
   - Format all results for academic publication
   - Create executive summary of key findings

3. Visualization Refinement:
   - Polish all visualizations for publication quality
   - 

---

### Step 11: Model Training & Prediction

**Inputs:** `analysis_output/final_report.md`, `analysis_output/descriptive_stats.csv`, `analysis_output/spearman_correlations.csv`, `analysis_output/effect_sizes.csv`, `analysis_output/enhanced_aircraft_data.csv`
**Outputs:** `analysis_output/final_report.md`
**Script:** `scripts/step_11_model-training-prediction.py`

**Purpose:**
To complete the analytical process, we should now:

1. Final Reporting:
   - Compile all results into a cohesive structure
   - Add interpretative narrative connecting findings
   - Format for academic publication standards

2. Limitations Documentation:
   - Explicitly address small sample considerations
   - Note non-significance vs. effect size distinctions
   - Discuss generalizability constraints

3. Future Research:
   - Outline recommended sample sizes
   - Suggest additional variables to

---

### Step 12: Error Recovery & Robust Loading

**Inputs:** `analysis_output/final_report.md`, `analysis_output/descriptive_stats.csv`, `analysis_output/spearman_correlations.csv`, `analysis_output/effect_sizes.csv`, `analysis_output/enhanced_aircraft_data.csv`
**Outputs:** `analysis_output/final_report.md`
**Script:** `scripts/step_12_error-recovery-robust-loading.py`

**Purpose:**
To resolve this issue and complete the comprehensive report, we should:

1. Implementation Strategy:
   - Add all required import statements
   - Make the reporting completely self-contained
   - Maintain all planned reporting components

2. Code Structure Improvements:
   - Verify all library imports are present
   - Add error handling for missing data files
   - Include defensive programming checks

3. Reporting Enhancements:
   - Keep all planned sections and analyses
   - Maintain academic w

---

### Step 13: Error Recovery & Robust Loading (Phase 2)

**Inputs:** `airport_aircraft.csv`, `aircraft.csv`, `analysis_output/comprehensive_aircraft_report.md`
**Outputs:** `analysis_output/spearman_correlations.csv`, `analysis_output/effect_sizes.csv`, `analysis_output/descriptive_statistics.csv`, `analysis_output/comprehensive_aircraft_report.md`
**Script:** `scripts/step_13_error-recovery-robust-loading-phase-2.py`

**Purpose:**
To resolve this issue and complete the comprehensive report, we need to:

1. Implementation Strategy:
   - Make the report generation self-contained
   - Include all necessary analysis steps within the function
   - Remove external file dependencies

2. Code Structure Improvements:
   - Perform all calculations internally
   - Generate required metrics on-demand
   - Maintain robust error handling

3. Analysis Enhancements:
   - Keep all planned statistical methods
   - Include effect size calcu

---

### Step 14: Error Recovery & Robust Loading (Phase 3)

**Inputs:** `airport_aircraft.csv`, `aircraft.csv`, `analysis_output/comprehensive_aircraft_report.md`
**Outputs:** `analysis_output/spearman_correlations.csv`, `analysis_output/effect_sizes.csv`, `analysis_output/descriptive_statistics.csv`, `analysis_output/comprehensive_aircraft_report.md`
**Script:** `scripts/step_14_error-recovery-robust-loading-phase-3.py`

**Purpose:**
To resolve this issue and complete the comprehensive report, we should:

1. Implementation Strategy:
   - Add all required import statements
   - Make the reporting completely self-contained
   - Maintain all planned reporting components

2. Code Structure Improvements:
   - Verify all library imports are present
   - Add error handling for missing dependencies
   - Include defensive programming checks

3. Reporting Enhancements:
   - Keep all planned sections and analyses
   - Maintain academic

---


## Final Output & Deliverables

# Comprehensive Analysis of Aircraft Specifications and Their Distribution Across Airports

## Introduction and Research Background

The relationship between aircraft specifications and their operational deployment patterns represents a critical area of study in aviation logistics and infrastructure planning. This comprehensive analysis examines five distinct helicopter models and their distribution across four airports, revealing fundamental principles governing aircraft assignment based on technical capabilities. The dataset encompasses detailed specifications including maximum gross weight (ranging from 1,370 to 123,500 lbs), total disk area (497 to 8,495 ft²), and maximum disk loading (2.6 to 15.0 lb/ft²), providing a robust foundation for investigating the interplay between engineering design and operational deployment. Through rigorous statistical analysis and multidimensional visualization techniques, this study establishes quantitative relationships that inform strategic decision-making in aviation management.

The methodology employed in this research incorporates both parametric and non-parametric statistical approaches to account for the small sample size while maintaining analytical rigor. Spearman rank correlation coefficients (ranging from 0.7 to 1.0) demonstrate strong monotonic relationships between key aircraft parameters, while Cohen's d effect size metrics (up to 1.70) reveal substantial practical differences in operational capabilities. The analysis particularly highlights how disk loading efficiency varies significantly across aircraft types, with weight-to-area ratios spanning from 2.76 to 15.0 lb/ft². These findings carry important implications for airport capacity planning, fleet optimization, and aviation safety protocols.

## Methodology and Analytical Framework

The research methodology was designed to address several key challenges inherent in aviation performance analysis, particularly the small sample size (n=5 aircraft) and the need to extract numerical data from formatted text fields. The data processing pipeline began with systematic extraction of numerical values from specification strings using regular expressions, converting measurements like "1,370 lb (635 kg)" into analyzable numeric format. This preprocessing step enabled precise quantitative comparisons across aircraft models with varying specification formats. The cleaned dataset was then subjected to multiple validation checks to ensure numerical accuracy and consistency across all parameters.

Statistical analysis proceeded through three complementary approaches: descriptive statistics to characterize central tendencies and dispersion patterns, correlation analysis to quantify inter-relationships between specifications, and effect size calculations to determine practical significance. The Spearman rank correlation method was selected as the primary measure of association due to its robustness against non-normal distributions, supplemented by Pearson corr


---

## How to Run

### Local Execution
```bash
# Install dependencies
pip install pandas openpyxl

# Run each step sequentially
cd case_5236_12853
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
