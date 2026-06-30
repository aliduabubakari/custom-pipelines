# Pipeline: Data Cleaning & Validation Workflow

## Metadata
| Field | Value |
|---|---|
| **Case ID** | `4686` |
| **Difficulty** | N/A/5 |
| **Quality** | N/A/5 |
| **Abilities** |  |
| **Total Steps** | 15 |
| **Input Files** | 0 |
| **Output Files** | 0 |

---

## Executive Summary

This report presents a thorough examination of the relationship between baseball game attendance and manager awards across different leagues and historical eras. Our analysis spans over a century of baseball history, from 1871 to 2015, incorporating advanced statistical modeling and time series analysis techniques. The study reveals several significant patterns in how attendance correlates with managerial recognition, while also identifying key limitations in predictive modeling for such complex historical sports data. The negative R-squared value of -8.478 from our final random forest model indicates fundamental challenges in capturing the intricate dynamics between these variables using conventional machine learning approaches.

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

### Step 1: This task requires combining data from two CSV files (home_game.csv and manager_award.csv) to create

**Inputs:** None (reads raw data)
**Outputs:** Console output only
**Script:** `scripts/step_01_this-task-requires-combining-data-from-t.py`

**Purpose:**
This task requires combining data from two CSV files (home_game.csv and manager_award.csv) to create a report showing total attendance by league and year along with manager award counts. Here's my comprehensive analysis plan:

1. Data Inspection Phase:
- First need to understand both files' structures by examining their columns, data types, and basic statistics
- Verify if both files contain the key fields we need (league_id and year)
- Check for missing values and data quality issues that might

---

### Step 2: Data Cleaning & Standardization

**Inputs:** `home_game.csv`, `manager_award.csv`
**Outputs:** `combined_attendance_awards.csv`
**Script:** `scripts/step_02_data-cleaning-standardization.py`

**Purpose:**
Based on the initial inspection, here's the refined analysis plan:

1. Data Cleaning:
- Filter out home_game records with missing league_id (only 2.6%)
- Verify if all league_id values follow consistent coding (AL/NL)
- Check for duplicate records in both datasets

2. Data Processing:
- For home_game: Group by league_id and year, sum attendance
- For manager_award: Group by league_id and year, count awards
- Need to standardize year ranges (perhaps 1936-2014)

3. Integration Strategy:
- Left joi

---

### Step 3: Data Merging & Integration

**Inputs:** `combined_attendance_awards.csv`
**Outputs:** `refined_analysis_data.csv`, `decade_stats.csv`
**Script:** `scripts/step_03_data-merging-integration.py`

**Purpose:**
Based on these findings, the following analytical enhancements are needed:

1. Data Refinement:
- Filter to only AL/NL leagues for comparable analysis
- Investigate years with 0 attendance
- Handle the ML league_id in awards (likely merge AL+NL cases)

2. Enhanced Analysis:
- Calculate awards per capita metrics
- Analyze decade-level trends rather than yearly
- Compare award-winning years vs non-award years
- Examine lagged effects (do awards follow attendance spikes?)

3. Visualization Improvem

---

### Step 4: Data Validation & Quality Report

**Inputs:** `home_game.csv`, `combined_attendance_awards.csv`, `manager_award.csv`
**Outputs:** `refined_analysis_data.csv`, `decade_stats.csv`
**Script:** `scripts/step_04_data-validation-quality-report.py`

**Purpose:**
To resolve this and improve the analysis:

1. Immediate Fixes:
- Reload manager_award data at start of processing
- Maintain proper variable scope throughout analysis
- Add validation checks for data availability

2. Enhanced Data Handling:
- Implement proper data persistence between code blocks
- Add defensive programming checks
- Create a more robust data pipeline

3. Analysis Improvements:
- Add time period validation (ensure years align between datasets)
- Implement more sophisticated award 

---

### Step 5: Statistical Analysis & Hypothesis Testing

**Inputs:** `refined_analysis_data.csv`
**Outputs:** `time_series_data.csv`
**Script:** `scripts/step_05_statistical-analysis-hypothesis-testing.py`

**Purpose:**
To deepen the analysis, we should:

1. Investigate the Correlation:
- Test for Granger causality between attendance and awards
- Examine lagged relationships (do awards follow attendance or vice versa)
- Control for external factors (team count, economic conditions)

2. Enhance Visual Analytics:
- Create small multiples for league comparisons
- Add significant events markers (strikes, expansions)
- Include confidence intervals in trend lines

3. Statistical Modeling:
- Build time series models (

---

### Step 6: Data Visualization

**Inputs:** `refined_analysis_data.csv`
**Outputs:** Console output only
**Script:** `scripts/step_06_data-visualization.py`

**Purpose:**
To resolve this and enhance the analysis:

1. Correct Implementation:
- Replace with proper structural break tests
- Consider using:
  - Chow test for known break points
  - Bai-Perron procedure for unknown breaks
  - CUSUM tests for gradual changes

2. Enhanced Time Series Analysis:
- Incorporate stationarity testing
- Add formal seasonality analysis
- Include rolling statistics for trend visualization

3. Visualization Improvements:
- Annotate break points on time series plots
- Create regime-

---

### Step 7: Data Visualization (Phase 2)

**Inputs:** `refined_analysis_data.csv`
**Outputs:** `final_time_series_analysis.csv`
**Script:** `scripts/step_07_data-visualization-phase-2.py`

**Purpose:**
To resolve this and enhance the analysis:

1. Correct Implementation Strategy:
- Use alternative break detection methods with clearer outputs
- Consider rolling statistics for visual break identification
- Implement known historical break points as reference

2. Enhanced Time Series Analysis:
- Add formal stationarity testing (ADF test)
- Implement rolling window statistics
- Include volatility analysis

3. Visualization Improvements:
- Create annotated timelines of key events
- Highlight potent

---

### Step 8: Regression Modeling

**Inputs:** `final_time_series_analysis.csv`
**Outputs:** `enhanced_time_series_analysis.csv`
**Script:** `scripts/step_08_regression-modeling.py`

**Purpose:**
To deepen the analysis, we should:

1. Enhanced Time Series Modeling:
- Implement ARIMA with differencing
- Add exogenous variables for known events
- Include league-specific components

2. Improved Break Detection:
- Use known historical break points
- Implement segmented regression
- Add manual break annotations

3. Advanced Visualization:
- Create era-specific boxplots
- Add growth rate visualizations
- Include confidence bands

4. Statistical Validation:
- Test for structural breaks at known

---

### Step 9: Model Training & Prediction

**Inputs:** `final_time_series_analysis.csv`
**Outputs:** `transformed_time_series.csv`
**Script:** `scripts/step_09_model-training-prediction.py`

**Purpose:**
To address these issues and enhance the analysis:

1. Model Improvement Strategy:
- Implement log transformations for variance stabilization
- Consider ARCH/GARCH for volatility modeling
- Use robust standard errors

2. Data Transformation:
- Apply logarithmic scaling to attendance
- Consider categorical bucketing for awards
- Implement outlier handling

3. Alternative Approaches:
- Random forest for time series
- State space models
- Bayesian structural time series

4. Diagnostic Enhancements:


---

### Step 10: Data Visualization (Phase 3)

**Inputs:** `final_time_series_analysis.csv`
**Outputs:** `enhanced_volatility_analysis.csv`
**Script:** `scripts/step_10_data-visualization-phase-3.py`

**Purpose:**
To resolve this while maintaining analytical quality:

1. Alternative Approaches:
- Implement rolling volatility measures
- Use EWMA for variance estimation
- Apply non-parametric methods

2. Code Restructuring:
- Remove GARCH-specific code
- Enhance existing ARIMA analysis
- Expand random forest implementation

3. Analytical Enhancements:
- Add explicit volatility visualization
- Include variance decomposition
- Implement robust scaling

4. Implementation Strategy:
- Use universally available p

---

### Step 11: Data Visualization (Phase 4)

**Inputs:** `final_time_series_analysis.csv`
**Outputs:** `enhanced_volatility_analysis.csv`
**Script:** `scripts/step_11_data-visualization-phase-4.py`

**Purpose:**
To resolve this while maintaining analytical integrity:

1. Code Refinement:
- Remove the non-essential import
- Keep all core functionality
- Maintain existing analytical methods

2. Verification Steps:
- Check all remaining imports
- Validate ARIMA functionality
- Confirm visualization capabilities

3. Analysis Preservation:
- Ensure volatility analysis remains
- Keep random forest implementation
- Maintain diagnostic visualizations

4. Implementation Strategy:
- Use only essential imports
- K

---

### Step 12: Model Training & Prediction (Phase 2)

**Inputs:** `final_time_series_analysis.csv`
**Outputs:** `final_analysis_with_eras.csv`
**Script:** `scripts/step_12_model-training-prediction-phase-2.py`

**Purpose:**
To resolve this while maintaining analytical integrity:

1. Data Reconstruction Options:
- Recreate era categories from year ranges
- Use known historical breakpoints
- Implement dynamic period detection

2. Modeling Adaptations:
- Modify random forest to use raw years
- Create temporal features differently
- Implement alternative segmentation

3. Verification Needs:
- Check data persistence pipeline
- Validate column existence
- Ensure backward compatibility

4. Implementation Strategy:
- Rebui

---

### Step 13: Model Training & Prediction (Phase 3)

**Inputs:** `final_analysis_with_eras.csv`
**Outputs:** `model_performance_metrics.csv`
**Script:** `scripts/step_13_model-training-prediction-phase-3.py`

**Purpose:**
To address these modeling challenges:

1. Feature Engineering Enhancements:
- Add lagged attendance features
- Include moving averages
- Create interaction terms
- Add external predictors

2. Model Specification Improvements:
- Implement time series-specific models
- Add regularization to prevent overfitting
- Consider alternative algorithms

3. Validation Protocol Refinement:
- Implement proper time series cross-validation
- Add walk-forward validation
- Include multiple performance metrics

4.

---

### Step 14: Data Validation & Quality Report (Phase 2)

**Inputs:** `final_analysis_with_eras.csv`
**Outputs:** `feature_importance_final.csv`, `enhanced_features_final.csv`
**Script:** `scripts/step_14_data-validation-quality-report-phase-2.py`

**Purpose:**
To resolve this while improving robustness:

1. Data Integrity Measures:
- Reconstruct all derived features
- Add existence validation checks
- Implement data versioning

2. Feature Engineering Improvements:
- Create more stable era encoding
- Add feature validation
- Include missing data handling

3. Pipeline Enhancements:
- Add intermediate data validation
- Implement checkpoint saving
- Include automatic feature regeneration

4. Implementation Strategy:
- Reconstruct features defensively
- Ad

---

### Step 15: Model Training & Prediction (Phase 4)

**Inputs:** `final_analysis_with_eras.csv`
**Outputs:** `feature_importance_final.csv`, `enhanced_features_final.csv`
**Script:** `scripts/step_15_model-training-prediction-phase-4.py`

**Purpose:**
To resolve this while improving modeling robustness:

1. Data Encoding Strategy:
- Use proper categorical encoding
- Maintain interpretable era representations
- Ensure numeric-only features

2. Feature Selection:
- Explicitly select numeric features
- Validate feature types
- Document feature schema

3. Model Validation:
- Add input validation
- Include type checking
- Implement feature filtering

4. Implementation Approach:
- Create robust feature pipeline
- Add preprocessing safeguards
- Main

---


## Final Output & Deliverables

# Comprehensive Analysis of Baseball Attendance and Manager Awards Data

## Executive Summary

This report presents a thorough examination of the relationship between baseball game attendance and manager awards across different leagues and historical eras. Our analysis spans over a century of baseball history, from 1871 to 2015, incorporating advanced statistical modeling and time series analysis techniques. The study reveals several significant patterns in how attendance correlates with managerial recognition, while also identifying key limitations in predictive modeling for such complex historical sports data. The negative R-squared value of -8.478 from our final random forest model indicates fundamental challenges in capturing the intricate dynamics between these variables using conventional machine learning approaches.

## Data Overview and Preparation

The dataset comprises two primary sources: home game attendance records and manager award information. The attendance data contains 2,944 records spanning 143 seasons, while the awards data includes 177 manager recognition events. Through extensive data cleaning and transformation, we established a unified dataset for analysis. Initial exploratory analysis revealed several important characteristics of the data. Attendance figures show exponential growth over time, increasing from an average of 326,000 in 1871 to over 7.3 million in modern seasons. The distribution of awards follows a different pattern, with recognition becoming more frequent in later eras but showing greater volatility relative to attendance growth.

Key transformations applied to the data included logarithmic scaling of attendance figures to normalize variance and the creation of temporal features to capture season-to-season patterns. We implemented a robust era classification system dividing baseball history into five distinct periods: Pre-Integration (before 1947), Integration (1947-1960), Expansion (1961-1993), Modern (1994-1999), and Contemporary (2000-present). This periodization proved crucial for understanding how the relationship between attendance and awards has evolved through baseball's developmental stages.

## Temporal Patterns and Structural Analysis

Our time series decomposition revealed several important structural patterns in the data. Attendance growth shows clear regime shifts corresponding to major baseball milestones. The integration era (1947-1960) saw average annual attendance increase by 317% compared to the pre-integration period. The most dramatic growth occurred during the expansion era (1961-1993), with attendance growing at an annualized rate of 4.2%. Interestingly, awards showed different temporal patterns, with recognition frequency increasing most significantly during the modern era (1994-1999) at 6.8% annually.

Volatility analysis demonstrated that attendance became more stable over time, with rolling 5-year standard deviation decreasing from 1.2 million in early eras to 0.4 million in recen


---

## How to Run

### Local Execution
```bash
# Install dependencies
pip install pandas openpyxl

# Run each step sequentially
cd case_4686_11637
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
