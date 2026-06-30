# Pipeline: Data Cleaning & Validation Workflow

## Metadata
| Field | Value |
|---|---|
| **Case ID** | `5515` |
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

**Inputs:** `airport_aircraft.csv`, `aircraft.csv`
**Outputs:** Console output only
**Script:** `scripts/step_01_data-loading-profiling.py`

**Purpose:**
To begin this comprehensive data science report on aircraft specifications and their distribution across airports, I will first need to understand the structure and content of both provided CSV files. The analysis will proceed through several logical phases:

1. Initial Data Exploration:
   - First inspect the aircraft.csv file to understand what specifications are available
   - Then examine airport_aircraft.csv to understand the relationship between airports and aircraft
   - Determine if ther

---

### Step 2: Data Loading & Profiling (Phase 2)

**Inputs:** `airport_aircraft.csv`, `aircraft.csv`
**Outputs:** `merged_airport_aircraft.csv`, `processed_aircraft.csv`
**Script:** `scripts/step_02_data-loading-profiling-phase-2.py`

**Purpose:**
Based on the initial understanding, the following analytical steps should be performed:

1. Data Preprocessing:
- Extract numerical values from mixed-unit strings in aircraft data
- Convert all measurements to consistent units (metric preferred)
- Create cleaned numerical columns for analysis

2. Enhanced Data Exploration:
- Analyze distribution of aircraft specifications
- Examine correlations between technical parameters
- Investigate airport-aircraft relationship patterns

3. Advanced Visuali

---

### Step 3: Regression Modeling

**Inputs:** `merged_airport_aircraft.csv`, `processed_aircraft.csv`
**Outputs:** `enhanced_aircraft.csv`
**Script:** `scripts/step_03_regression-modeling.py`

**Purpose:**
The current analysis has established fundamental relationships between aircraft specifications. To deepen our understanding, we should:

1. Expand Statistical Analysis:
- Calculate descriptive statistics for the new numerical columns
- Perform regression analysis to quantify specification relationships
- Analyze variance between aircraft categories

2. Enhance Visualization:
- Create 3D scatter plot incorporating all three numerical parameters
- Generate parallel coordinates plot for multivariat

---

### Step 4: Data Loading & Profiling (Phase 3)

**Inputs:** `enhanced_aircraft.csv`, `merged_airport_aircraft.csv`
**Outputs:** `airport_capacity_stats.csv`, `final_aircraft_analysis.csv`
**Script:** `scripts/step_04_data-loading-profiling-phase-3.py`

**Purpose:**
To deepen our analysis, we should:

1. Segmentation Analysis:
- Create weight-based categories (light/medium/heavy)
- Compare specifications across segments
- Analyze loading efficiency by category

2. Outlier Examination:
- Investigate extreme values in weight and disk area
- Assess whether outliers represent special cases or errors

3. Operational Analysis:
- Calculate power-to-weight ratios if engine data available
- Estimate lift efficiency metrics
- Compare military vs civilian applications

---

### Step 5: Regression Modeling (Phase 2)

**Inputs:** `merged_airport_aircraft.csv`, `airport_capacity_stats.csv`, `final_aircraft_analysis.csv`
**Outputs:** `airport_capacity_profiles.csv`, `final_aircraft_analysis_v2.csv`
**Script:** `scripts/step_05_regression-modeling-phase-2.py`

**Purpose:**
To improve and expand our analysis:

1. Code Quality Improvements:
- Address Seaborn deprecation warning
- Enhance visualization labeling and styling
- Add interactive plot elements where beneficial

2. Advanced Analytics:
- Implement cross-validation for predictive models
- Add feature importance analysis
- Explore non-linear regression approaches

3. Operational Insights:
- Calculate airport capacity utilization
- Analyze aircraft type distribution patterns
- Develop compatibility scoring betw

---

### Step 6: Model Training & Prediction

**Inputs:** `merged_airport_aircraft.csv`, `aircraft.csv`, `final_aircraft_analysis.csv`
**Outputs:** `validated_aircraft_data.csv`
**Script:** `scripts/step_06_model-training-prediction.py`

**Purpose:**
To address these issues and enhance the analysis:

1. Data Integrity Fixes:
- Verify column names throughout processing pipeline
- Implement consistent naming conventions
- Add data validation checks

2. Small Sample Adjustments:
- Replace cross-validation with holdout validation
- Simplify models to avoid overfitting
- Focus on descriptive rather than predictive analytics

3. Enhanced Error Handling:
- Add defensive programming checks
- Implement data validation before operations
- Create fallb

---

### Step 7: Model Training & Prediction (Phase 2)

**Inputs:** `merged_airport_aircraft.csv`, `aircraft.csv`, `final_aircraft_analysis.csv`
**Outputs:** Console output only
**Script:** `scripts/step_07_model-training-prediction-phase-2.py`

**Purpose:**
To resolve this issue and improve the analysis:

1. Immediate Fixes:
- Add missing import statement
- Verify all required imports are present
- Ensure consistent code structure

2. Enhanced Robustness:
- Implement import verification
- Add try-except blocks for critical operations
- Create function-based organization

3. Analysis Improvements:
- Expand model evaluation metrics
- Include model interpretation
- Add residual analysis

4. Documentation:
- Add inline comments
- Include docstrings for

---

### Step 8: Data Visualization

**Inputs:** `merged_airport_aircraft.csv`, `aircraft.csv`, `final_aircraft_analysis.csv`
**Outputs:** Console output only
**Script:** `scripts/step_08_data-visualization.py`

**Purpose:**
To resolve this systematically:

1. Data Verification:
- Add detailed column existence checks
- Implement fallback column creation
- Verify data persistence in CSV files

2. Error Handling:
- Create robust fallback procedures
- Add detailed error logging
- Implement graceful degradation

3. Analysis Adaptation:
- Develop alternative airport metrics
- Focus on available data relationships
- Prioritize visualization over aggregation

4. Code Structure:
- Modularize airport analysis
- Separate data

---

### Step 9: Data Merging & Integration

**Inputs:** `aircraft.csv`, `merged_airport_aircraft.csv`
**Outputs:** Console output only
**Script:** `scripts/step_09_data-merging-integration.py`

**Purpose:**
To resolve these issues and enhance the analysis:

1. Data Flow Investigation:
- Add detailed DataFrame inspection points
- Track column states through pipeline
- Verify merge operations

2. Analysis Adaptation:
- Implement alternative airport metrics
- Focus on categorical relationships
- Expand visualization capabilities

3. Model Enhancement:
- Add coefficient interpretation
- Include prediction intervals
- Calculate effect sizes

4. Code Improvement:
- Add comprehensive logging
- Implement d

---

### Step 10: Data Visualization (Phase 2)

**Inputs:** `aircraft.csv`
**Outputs:** `model_diagnostics.csv`
**Script:** `scripts/step_10_data-visualization-phase-2.py`

**Purpose:**
To enhance the analysis, we should:

1. Model Enhancement:
- Add variance inflation factor (VIF) analysis
- Include coefficient significance tests
- Calculate confidence intervals

2. Diagnostic Analysis:
- Generate Q-Q plot of residuals
- Plot residual vs fitted values
- Perform Shapiro-Wilk normality test

3. Data Exploration:
- Conduct outlier detection
- Analyze leverage points
- Examine influence metrics

4. Visualization Expansion:
- Create coefficient plot with CIs
- Generate partial depe

---

### Step 11: Statistical Analysis & Hypothesis Testing

**Inputs:** `aircraft.csv`
**Outputs:** `collinearity_diagnostics.csv`
**Script:** `scripts/step_11_statistical-analysis-hypothesis-testing.py`

**Purpose:**
To address these findings, we should:

1. Multicollinearity Mitigation:
- Consider ridge regression or PCA
- Evaluate dropping one correlated feature
- Analyze correlation structure

2. Model Robustness:
- Implement regularized regression
- Compare with simple linear models
- Calculate variance decomposition

3. Diagnostic Enhancement:
- Plot correlation heatmap
- Calculate condition indices
- Perform variance proportion analysis

4. Alternative Approaches:
- Non-parametric methods
- Bayesian re

---

### Step 12: Regression Modeling (Phase 3)

**Inputs:** `aircraft.csv`
**Outputs:** `regularization_results.csv`
**Script:** `scripts/step_12_regression-modeling-phase-3.py`

**Purpose:**
To address this issue and enhance our analysis:

1. Immediate Fixes:
- Remove deprecated `normalize` parameter
- Implement explicit feature scaling
- Maintain backward compatibility

2. Enhanced Methodology:
- Add StandardScaler before Ridge regression
- Compare standardized vs non-standardized results
- Document version-specific requirements

3. Analysis Expansion:
- Include ElasticNet for comparison
- Add cross-validated hyperparameter tuning
- Implement model persistence

4. Robustness Improv

---

### Step 13: Data Validation & Quality Report

**Inputs:** `aircraft.csv`
**Outputs:** `regularization_results.csv`, `coefficient_analysis.csv`
**Script:** `scripts/step_13_data-validation-quality-report.py`

**Purpose:**
To resolve this and enhance robustness:

1. Parameter Validation:
- Add explicit alpha validation
- Implement fallback alpha values
- Ensure proper parameter passing

2. Error Prevention:
- Add pipeline configuration checks
- Validate cross-validation results
- Implement defensive programming

3. Analysis Improvements:
- Expand hyperparameter tuning
- Add early stopping criteria
- Include convergence monitoring

4. Code Structure:
- Modularize parameter tuning
- Separate validation from executio

---

### Step 14: Regression Modeling (Phase 4)

**Inputs:** `aircraft.csv`
**Outputs:** `descriptive_statistics.csv`, `aircraft_profiles.csv`
**Script:** `scripts/step_14_regression-modeling-phase-4.py`

**Purpose:**
Given these findings, we should:

1. Methodological Shift:
- Abandon traditional regression approaches
- Focus on descriptive statistics
- Implement non-parametric methods

2. Data-Centric Analysis:
- Expand feature engineering
- Create composite indicators
- Analyze pairwise relationships

3. Visualization Focus:
- Develop comprehensive visual profiles
- Create radar charts for comparisons
- Generate small-sample friendly plots

4. Alternative Techniques:
- Implement similarity analysis
- Calcu

---


## Final Output & Deliverables

# Comprehensive Analysis of Aircraft Specifications and Distribution Patterns

## Introduction and Dataset Overview

The analysis of aircraft specifications and their distribution across airports represents a critical examination of aviation engineering characteristics and operational deployment patterns. This study focuses on five distinct helicopter models ranging from light utility aircraft to heavy-lift helicopters, with specifications including maximum gross weight, total disk area, and maximum disk loading. The dataset, though limited in sample size (n=5), presents an intriguing case study in aerospace engineering statistics and operational logistics. The Robinson R-22 serves as our baseline light utility helicopter with a maximum gross weight of 1,370 kg, while the Mil Mi-26 represents the heaviest aircraft at 123,500 kg, demonstrating a 90-fold difference in weight capacity across the fleet. Such extreme ranges in technical specifications necessitate careful analytical approaches that account for non-linear relationships and scale effects in the data.

Descriptive statistics reveal substantial variation across all measured parameters. The maximum gross weight shows a mean of 50,314 kg (SD=51,257 kg), while total disk area averages 4,084 m² (SD=3,383 m²). The maximum disk loading displays slightly less relative variability with a mean of 8.92 kg/m² (SD=5.82 kg/m²). These metrics underscore the technical diversity present in our sample, with coefficient of variation values exceeding 100% for weight-related measures. The size index, calculated as the natural logarithm of the product of weight and disk area, provides a composite metric ranging from 13.43 to 20.77 across aircraft types. This logarithmic transformation helps normalize the extreme differences in scale while preserving the ordinal relationships between aircraft classes.

The efficiency index, defined as the ratio of maximum gross weight to disk loading, offers insights into lift performance characteristics. Values range from 526.92 for the Robinson R-22 to 8,517.24 for the CH-53E Super Stallion, indicating nearly a 16-fold difference in this operational efficiency metric. These findings suggest that heavier helicopters achieve significantly better efficiency ratios, though this relationship requires careful interpretation given the small sample size. The similarity matrix analysis, calculated using Euclidean distances between standardized specifications, reveals that the Mil Mi-26 and CH-53E Super Stallion show the greatest dissimilarity (distance=50,129.07), while the Bell 206B3 JetRanger and Robinson R-22 demonstrate the closest technical profile (distance=1,868.03).

## Technical Specification Analysis

The examination of aircraft technical specifications through multiple analytical lenses yields several significant insights. Radar chart visualizations (see Figure 1 in supplementary materials) demonstrate that no single helicopter dominates all performance categories, with eac


---

## How to Run

### Local Execution
```bash
# Install dependencies
pip install pandas openpyxl

# Run each step sequentially
cd case_5515_13564
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
