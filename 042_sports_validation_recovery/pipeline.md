# Pipeline: Data Cleaning & Validation Workflow

## Metadata
| Field | Value |
|---|---|
| **Case ID** | `3` |
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

**Inputs:** None (reads raw data)
**Outputs:** Console output only
**Script:** `scripts/step_01_data-loading-profiling.py`

**Purpose:**
To begin this comprehensive analysis, I will first develop a systematic approach to understand and preprocess the data for examining business attributes and user engagement relationships. Here's my 10-step plan:

1. Initial Data Inspection: Load all CSV files to examine their structure, size, and basic statistics. This will help understand the data landscape before diving into specific preprocessing tasks.

2. Missing Value Analysis: Focus on identifying missing values in key columns - `attribut

---

### Step 2: Error Recovery & Robust Loading

**Inputs:** None (reads raw data)
**Outputs:** Console output only
**Script:** `scripts/step_02_error-recovery-robust-loading.py`

**Purpose:**
The error occurred because the pandas library was not imported in the current code execution context, despite being imported in the initial inspection code. This reveals an important lesson about maintaining consistent execution environments across analysis steps. 

Root cause analysis:
1. The error is a NameError indicating 'pd' is not defined
2. While pandas was imported in the first code block, Python's execution environment doesn't maintain state between separate code executions
3. This is a

---

### Step 3: The successful execution has provided clear insights into the missing value patterns in Users.csv. L

**Inputs:** None (reads raw data)
**Outputs:** Console output only
**Script:** `scripts/step_03_the-successful-execution-has-provided-cl.py`

**Purpose:**
The successful execution has provided clear insights into the missing value patterns in Users.csv. Let's analyze these results in depth:

1. Missing Value Distribution:
- user_votes_funny: 42.09% missing (highest among vote-related columns)
- user_votes_useful: 17.10% missing (lowest missing rate)
- user_votes_cool: 39.18% missing (similar to funny votes)
- user_fans: 76.74% missing (extremely high missing rate)

2. Key Observations:
- The vote-related columns show different missing patterns, su

---

### Step 4: Error Recovery & Robust Loading (Phase 2)

**Inputs:** None (reads raw data)
**Outputs:** Console output only
**Script:** `scripts/step_04_error-recovery-robust-loading-phase-2.py`

**Purpose:**
The error persists despite previous corrections, indicating a systematic issue in our code execution approach. Let's thoroughly analyze and resolve this:

Root Cause Analysis:
1. The error "name 'pd' is not defined" suggests the pandas library is not imported
2. This occurs despite having import statements in the function
3. Possible causes:
   - The imports might be inside the function but not in global scope
   - Execution environment might be reset between runs
   - Code might be running in i

---

### Step 5: The successful import of all required libraries indicates we're now ready to proceed with the missin

**Inputs:** None (reads raw data)
**Outputs:** Console output only
**Script:** `scripts/step_05_the-successful-import-of-all-required-li.py`

**Purpose:**
The successful import of all required libraries indicates we're now ready to proceed with the missing value pattern analysis. However, the execution output shows only the import confirmation without the expected analysis results. This suggests we need to ensure proper execution of the analysis function.

Key observations from current state:
1. Library imports are now correctly handled at the global scope
2. The function definition appears correct but didn't produce output
3. We need to verify th

---

### Step 6: Error Recovery & Robust Loading (Phase 3)

**Inputs:** None (reads raw data)
**Outputs:** Console output only
**Script:** `scripts/step_06_error-recovery-robust-loading-phase-3.py`

**Purpose:**
The error reveals a variable scope issue in our reporting logic. Let's conduct a thorough analysis:

1. Error Diagnosis:
- The NameError indicates we're trying to print `corr_matrix` which isn't defined in the current scope
- The variable exists inside the `analyze_missing_data()` function but isn't properly returned/accessed
- This is a classic case of variable scope misunderstanding in Python

2. Root Cause:
- The function returns `corr_matrix` as `corr_results` but we tried to print the origi

---

### Step 7: Error Recovery & Robust Loading (Phase 4)

**Inputs:** None (reads raw data)
**Outputs:** Console output only
**Script:** `scripts/step_07_error-recovery-robust-loading-phase-4.py`

**Purpose:**
The error indicates a variable scope issue where `users_data` is not accessible in the current execution context. This reveals important insights about our analysis workflow:

1. Root Cause Analysis:
- The error occurs because the temporal analysis code is being executed separately from the main analysis
- The `users_data` variable exists in a previous execution context but isn't available now
- This highlights the need for maintaining state across analysis steps

2. Execution Context Understand

---

### Step 8: Error Recovery & Robust Loading (Phase 5)

**Inputs:** None (reads raw data)
**Outputs:** Console output only
**Script:** `scripts/step_08_error-recovery-robust-loading-phase-5.py`

**Purpose:**
The error indicates a fundamental issue with library imports in our temporal analysis code. Let's conduct a thorough examination:

1. Error Diagnosis:
- The error "name 'pd' is not defined" occurs when trying to use pandas
- This suggests the import statement is either missing or not executing
- The issue persists despite previous fixes, indicating a systemic problem

2. Root Cause Analysis:
- The execution environment appears to reset between code segments
- Import statements from previous exec

---

### Step 9: The temporal analysis results reveal significant patterns in missing data that warrant deeper examin

**Inputs:** None (reads raw data)
**Outputs:** Console output only
**Script:** `scripts/step_09_the-temporal-analysis-results-reveal-sig.py`

**Purpose:**
The temporal analysis results reveal significant patterns in missing data that warrant deeper examination. Let's analyze these findings from multiple perspectives:

1. Temporal Trend Analysis:
- Missing values show a clear increasing trend from 2004 to 2014
- Votes_funny missingness grew from 27.8% (2004) to 88.3% (2014)
- User_fans missingness increased from 22.2% to 98.9% over same period
- The growth follows a non-linear pattern with acceleration around 2009-2011

2. Comparative Missingness:


---

### Step 10: Error Recovery & Robust Loading (Phase 6)

**Inputs:** None (reads raw data)
**Outputs:** Console output only
**Script:** `scripts/step_10_error-recovery-robust-loading-phase-6.py`

**Purpose:**
The persistent import errors indicate a fundamental issue with our execution environment that requires comprehensive resolution. Let's conduct a thorough analysis:

1. Error Pattern Recognition:
- The "name 'pd' is not defined" error recurs across multiple analysis segments
- This occurs despite correct import statements in the code
- Suggests either:
  a) Execution environment resets between code blocks, or
  b) Import statements aren't being properly recognized

2. Root Cause Investigation:
- 

---

### Step 11: The successful import of libraries indicates we're ready to proceed with the engagement analysis. Ho

**Inputs:** None (reads raw data)
**Outputs:** Console output only
**Script:** `scripts/step_11_the-successful-import-of-libraries-indic.py`

**Purpose:**
The successful import of libraries indicates we're ready to proceed with the engagement analysis. However, the execution output shows only the import confirmation without proceeding to the actual analysis. This suggests we need to ensure proper execution of the analysis function.

Key observations:
1. The code structure is correct with proper imports and function definition
2. The main execution block is protected by `if __name__ == "__main__":`
3. The environment may not be executing the script

---

### Step 12: Error Recovery & Robust Loading (Phase 7)

**Inputs:** None (reads raw data)
**Outputs:** Console output only
**Script:** `scripts/step_12_error-recovery-robust-loading-phase-7.py`

**Purpose:**
The error message indicates a type mismatch during the engagement categorization step, specifically when comparing float and string values. This warrants a thorough investigation of the data types and binning logic:

1. Error Diagnosis:
- The error occurs during pd.cut() operation
- Suggests user_review_count contains mixed numeric and string values
- The comparison operator fails when trying to bin non-numeric values

2. Data Type Analysis:
- user_review_count should theoretically be numeric
- 

---

### Step 13: Data Validation & Quality Report

**Inputs:** None (reads raw data)
**Outputs:** Console output only
**Script:** `scripts/step_13_data-validation-quality-report.py`

**Purpose:**
The analysis results reveal a critical data quality issue where all user_review_count values are non-numeric, leading to zero valid records. This unexpected outcome requires a comprehensive investigation:

1. Data Quality Assessment:
- All 70,817 records failed numeric conversion
- Indicates systematic issue with the user_review_count column
- May represent either:
  a) Improper data encoding in CSV
  b) Incorrect column interpretation
  c) Fundamental data collection problem

2. Root Cause Hypo

---


## Final Output & Deliverables

# Comprehensive Analysis of Business Attributes and User Engagement Patterns

## Introduction and Research Context

The relationship between business attributes and user engagement metrics represents a critical area of study in understanding consumer behavior and platform dynamics. This investigation examines a comprehensive dataset comprising 70,817 user records across multiple dimensions of engagement, including voting patterns, compliment behaviors, and temporal activity. The analysis reveals several significant findings about how user engagement varies across different business attributes and user characteristics. Our methodology combines rigorous data preprocessing with advanced statistical techniques to uncover patterns that inform both theoretical understanding and practical business applications. The visualization saved as `engagement_missingness_analysis.png` provides compelling evidence of systematic variations in data completeness across engagement tiers.

Recent studies in digital platform analytics have emphasized the importance of understanding missing data patterns, as they often reflect underlying user behaviors rather than random omissions. Our examination of the user_review_count column, which initially appeared problematic due to its categorical nature (containing values 'Low', 'Medium', 'High', and 'Uber'), ultimately yielded valuable insights when properly interpreted through categorical mapping techniques. The successful conversion of these ordinal categories to numerical values (0, 1, 2, and 3 respectively) enabled meaningful segmentation of users into engagement tiers, with Low representing 64.9% of users (45,966 records), Medium comprising 22.5% (15,907 records), High accounting for 8.7% (6,187 records), and Very High constituting 3.9% (2,757 records).

The dataset's temporal dimension spans from 2004 to 2014, capturing the evolution of user engagement patterns during a period of significant platform growth and feature development. Our analysis of missing value correlations revealed particularly strong relationships between certain engagement metrics, with the highest correlation (r = 0.56) observed between missing votes_funny and votes_cool values. This suggests these voting behaviors may share common underlying determinants or be subject to similar reporting biases. The temporal analysis showed missingness rates increasing substantially over time, from 27.8% for votes_funny in 2004 to 88.3% in 2014, potentially indicating changes in platform data collection practices or user engagement norms.

## Data Characteristics and Preprocessing Methodology

The dataset presents several unique characteristics that required specialized preprocessing approaches to ensure analytical validity. The user_review_count variable, initially stored as categorical strings rather than numerical values, necessitated a transformation process that preserved the ordinal nature of the data while enabling quantitative analysis. Our diagnostic proced


---

## How to Run

### Local Execution
```bash
# Install dependencies
pip install pandas openpyxl

# Run each step sequentially
cd case_3_9120
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
