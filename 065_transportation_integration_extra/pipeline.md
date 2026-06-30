# Pipeline: Data Cleaning & Validation Workflow

## Metadata
| Field | Value |
|---|---|
| **Case ID** | `4547` |
| **Difficulty** | N/A/5 |
| **Quality** | N/A/5 |
| **Abilities** |  |
| **Total Steps** | 11 |
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

**Inputs:** `school_bus.csv`, `driver.csv`
**Outputs:** Console output only
**Script:** `scripts/step_01_data-loading-profiling.py`

**Purpose:**
This task requires a comprehensive analysis of two datasets related to school bus drivers, focusing on demographic and employment characteristics. The analysis will involve multiple steps:

1. Data Inspection and Understanding:
   - First need to examine both CSV files to understand their structure and contents
   - Determine how the datasets relate to each other (common keys/join conditions)
   - Identify data types, missing values, and basic statistics

2. Data Preparation:
   - Merge the data

---

### Step 2: Data Loading & Profiling (Phase 2)

**Inputs:** `school_bus.csv`, `driver.csv`
**Outputs:** Console output only
**Script:** `scripts/step_02_data-loading-profiling-phase-2.py`

**Purpose:**
The error indicates that the 'driver_id' column does not exist in the driver.csv dataset, which means my initial assumption about the join key was incorrect. This requires a revised approach:

1. First Need to Understand Actual Data Structure:
   - The error suggests we need to examine the actual column names in both datasets
   - Need to determine what columns exist that could serve as join keys
   - Should print the actual column names to identify potential relationships

2. Data Inspection Ad

---

### Step 3: The execution results provide valuable insights into the dataset structure

**Inputs:** `school_bus.csv`, `driver.csv`
**Outputs:** `merged_driver_bus.csv`
**Script:** `scripts/step_03_the-execution-results-provide-valuable-i.py`

**Purpose:**
The execution results provide valuable insights into the dataset structure:

1. Data Structure Confirmation:
   - Both datasets contain 'Driver_ID' as a common column
   - Driver dataset includes demographic information (Name, Party, Home_city, Age)
   - School bus dataset contains employment details (Years_Working, If_full_time)

2. Data Quality Observations:
   - The sample rows show consistent data formats
   - No immediate missing values in the displayed samples
   - Need to verify if all Dr

---

### Step 4: Data Merging & Integration

**Inputs:** `merged_driver_bus.csv`
**Outputs:** `complete_cases_driver_bus.csv`
**Script:** `scripts/step_04_data-merging-integration.py`

**Purpose:**
The merge results reveal several important insights about our dataset:

1. Data Completeness Issues:
   - Only 5 out of 12 records (41.7%) have complete matching information
   - 7 drivers lack bus assignment information (School_ID, Years_Working, If_full_time are NaN)
   - No bus records lack driver information, indicating all bus assignments reference existing drivers

2. Data Distribution Characteristics:
   - Strong political party imbalance: 10 Democrats vs 2 Republicans
   - 5 unique home 

---

### Step 5: The complete cases analysis reveals several important patterns that require deeper investigation

**Inputs:** `complete_cases_driver_bus.csv`, `merged_driver_bus.csv`
**Outputs:** `statistical_test_results.csv`
**Script:** `scripts/step_05_the-complete-cases-analysis-reveals-seve.py`

**Purpose:**
The complete cases analysis reveals several important patterns that require deeper investigation:

1. Key Findings from Current Analysis:
   - Significant political party disparity in matched cases (100% Democrats)
   - Age distribution shows matched drivers are slightly younger (mean 39.8 vs 41.4)
   - Strong full-time employment bias (80% full-time among complete cases)
   - Years working shows wide variation (2-10 years) with mean 5.8 years

2. Required Deep Dives:
   - Need to examine why on

---

### Step 6: Data Loading & Profiling (Phase 3)

**Inputs:** `merged_driver_bus.csv`
**Outputs:** `prepared_driver_data.csv`
**Script:** `scripts/step_06_data-loading-profiling-phase-3.py`

**Purpose:**
The error reveals a critical oversight in our analysis workflow:

1. Root Cause Analysis:
   - The 'has_employment_data' column was created in a previous code block but not saved to the CSV
   - When reloading data from CSV, this derived column is lost
   - Need to either recreate this column or persist it with the saved data

2. Data Flow Problems:
   - Previous analysis created temporary columns that weren't preserved
   - Need to maintain consistency between in-memory and saved data
   - Shou

---

### Step 7: Statistical Analysis & Hypothesis Testing

**Inputs:** `prepared_driver_data.csv`
**Outputs:** `logistic_regression_coefficients.csv`
**Script:** `scripts/step_07_statistical-analysis-hypothesis-testing.py`

**Purpose:**
The statistical results reveal several important insights that warrant deeper investigation:

1. Key Findings from Statistical Tests:
   - No significant age difference between matched/unmatched drivers (p=0.705)
   - Party affiliation difference approaches but doesn't reach significance (p=0.600)
   - Full-time workers show lower average years of service (4.75) vs part-time (10.0)

2. Emerging Patterns Requiring Further Analysis:
   - Potential non-linear relationship between tenure and full-ti

---

### Step 8: Regression Modeling

**Inputs:** `prepared_driver_data.csv`
**Outputs:** `bootstrap_coefficients.csv`
**Script:** `scripts/step_08_regression-modeling.py`

**Purpose:**
The latest results reveal several critical insights that require deeper examination:

1. Key Findings from Current Analysis:
   - Logistic regression shows Years_Working has strong negative coefficient (-0.827) for full-time status
   - Perfect classification accuracy likely indicates overfitting (100% precision/recall)
   - Low statistical power (41.57%) suggests limited ability to detect effects
   - Geographic analysis shows Hartford has 100% full-time rate vs East Hartford's 50%

2. Emerging

---

### Step 9: Regression Modeling (Phase 2)

**Inputs:** `prepared_driver_data.csv`
**Outputs:** `robust_analysis_results.csv`
**Script:** `scripts/step_09_regression-modeling-phase-2.py`

**Purpose:**
The error reveals a fundamental limitation in our dataset that requires careful consideration:

1. Root Cause Analysis:
   - The error occurs when bootstrap samples contain only one class (all full-time or all part-time)
   - With only 1 part-time observation in our complete cases (n=5), many bootstrap samples will be single-class
   - This makes traditional logistic regression and cross-validation unreliable

2. Data Limitations:
   - Extreme class imbalance (4:1 ratio) in complete cases
   - S

---

### Step 10: Model Training & Prediction

**Inputs:** `prepared_driver_data.csv`
**Outputs:** `bootstrap_estimates.csv`
**Script:** `scripts/step_10_model-training-prediction.py`

**Purpose:**
The error reveals another limitation in our dataset structure that requires careful handling:

1. Root Cause Analysis:
   - Fisher's exact test requires a 2x2 contingency table
   - Our data has only Democratic party entries in complete cases (no Republicans)
   - This creates a degenerate table structure (1x2 instead of 2x2)

2. Data Constraints:
   - Complete cases lack political diversity (all Democrats)
   - Sample size too small for meaningful party comparisons
   - Need alternative approac

---

### Step 11: The bootstrap results provide stable estimates despite the small sample size, revealing several impo

**Inputs:** `prepared_driver_data.csv`
**Outputs:** `enhanced_analysis_results.csv`
**Script:** `scripts/step_11_the-bootstrap-results-provide-stable-est.py`

**Purpose:**
The bootstrap results provide stable estimates despite the small sample size, revealing several important patterns:

1. Key Findings from Current Analysis:
   - Stable age estimates (mean 39.8, CI 36.8-43.4) despite small sample
   - Years working shows wider variation (mean 5.84, CI 3.2-8.4)
   - Strong geographic disparity in employment types (100% FT in Hartford vs 50% in East Hartford)
   - Consistent 4:1 full-time to part-time ratio in complete cases

2. Remaining Analytical Gaps:
   - Need

---


## Final Output & Deliverables

# Comprehensive Analysis of School Bus Driver Demographics and Employment Patterns

## Introduction and Research Context

The relationship between workforce demographics and employment characteristics represents a critical area of study in organizational psychology and labor economics. This investigation examines school bus drivers, a vital yet understudied segment of the transportation workforce, through the lens of their demographic profiles and employment patterns. Our analysis merges two datasets containing driver demographics (age, home city, party affiliation) and employment details (years working, full-time status), creating a rich foundation for exploring workforce dynamics. The study population consists of 12 drivers, with complete employment data available for 5 individuals (41.7% of the sample), presenting both opportunities and challenges for statistical analysis. The demographic composition reveals a politically skewed distribution (10 Democrats to 2 Republicans) and age range from 30 to 46 years (mean = 39.8, 95% CI [36.8, 43.4]), while employment tenure shows substantial variation (mean = 5.84 years, 95% CI [3.2, 8.4]). These baseline characteristics establish the context for our multidimensional examination of workforce patterns.

Geographic distribution analysis identifies Hartford and East Hartford as the primary service areas, with 3 and 2 drivers respectively in the complete cases dataset. The employment type distribution shows a pronounced full-time dominance (80% full-time vs 20% part-time), though this ratio varies significantly by location (100% full-time in Hartford vs 50% in East Hartford). These preliminary observations raise important questions about potential systemic factors influencing employment conditions across different municipalities. Our bootstrap analyses indicate stable estimates for age (SD = 4.15) despite the small sample size, while years working demonstrates greater variability (SD = 3.35), suggesting tenure may be more sensitive to external factors than demographic characteristics. The permutation test for city differences in tenure yields a non-significant p-value (1.000) with negligible effect size (Cohen's d = -0.08), indicating observed geographic variations may represent random fluctuations rather than systematic differences.

Methodologically, we confronted several analytical challenges stemming from the dataset's limitations. The small sample size (n=5 complete cases) necessitated alternative statistical approaches, including bootstrap resampling (1000 iterations) and permutation testing, to generate robust estimates. Our correlation analysis between age and tenure produced a weak negative relationship (r = -0.18) that failed to reach statistical significance, with bootstrapped confidence intervals that could not be reliably estimated due to constant input warnings. This suggests the observed age-tenure relationship may be substantially influenced by the outlier part-time worker with 10 years of 


---

## How to Run

### Local Execution
```bash
# Install dependencies
pip install pandas openpyxl

# Run each step sequentially
cd case_4547_11319
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
