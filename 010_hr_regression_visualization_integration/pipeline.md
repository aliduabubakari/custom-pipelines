# Pipeline: Data Cleaning & Validation Workflow

## Metadata
| Field | Value |
|---|---|
| **Case ID** | `44` |
| **Difficulty** | N/A/5 |
| **Quality** | N/A/5 |
| **Abilities** |  |
| **Total Steps** | 13 |
| **Input Files** | 0 |
| **Output Files** | 0 |

---

## Executive Summary

This comprehensive report presents a detailed analysis of employee data spanning multiple dimensions including compensation, career progression, departmental mobility, and demographic patterns. The study leverages advanced statistical techniques and data visualization methods to uncover meaningful insights from organizational data, with particular emphasis on pay equity considerations, career trajectory analysis, and workforce dynamics. Our analysis draws upon multiple interconnected datasets containing detailed employment records, compensation history, department assignments, and demographic information, enabling a holistic view of organizational patterns and potential areas for improvement. The findings reveal several significant patterns in compensation structures, gender disparities in leadership representation, and departmental mobility trends that warrant further examination by human resources professionals and organizational leadership.

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

### Step 1: This dataset appears to be a collection of CSV files representing what looks like a relational datab

**Inputs:** None (reads raw data)
**Outputs:** Console output only
**Script:** `scripts/step_01_this-dataset-appears-to-be-a-collection-.py`

**Purpose:**
This dataset appears to be a collection of CSV files representing what looks like a relational database schema for a business system, possibly for sales, inventory, and human resources management. The files vary significantly in size from 0.1KB to 13005.5KB, suggesting they contain different amounts of data records.

Initial observations:
1. The largest files are Person.csv (13005.5KB), SalesOrderDetail.csv (11988.6KB), and WorkOrderRouting.csv (9182.1KB), indicating these likely contain the mos

---

### Step 2: Data Merging & Integration

**Inputs:** `EmployeeDepartmentHistory.csv`, `Employee.csv`, `Person.csv`, `Department.csv`
**Outputs:** Console output only
**Script:** `scripts/step_02_data-merging-integration.py`

**Purpose:**
Root cause analysis:
1. In the initial code block, we properly imported pandas as pd and used it successfully
2. The error occurred in subsequent analysis when trying to merge DataFrames
3. This suggests either:
   - The execution environment doesn't maintain state between code blocks
   - We need to re-import required modules in each code block

Solution approach:
1. Always include necessary imports at the start of each code block
2. Verify all required modules are properly imported
3. Consider

---

### Step 3: Next steps for deeper analysis

**Inputs:** `EmployeePayHistory.csv`
**Outputs:** Console output only
**Script:** `scripts/step_03_next-steps-for-deeper-analysis.py`

**Purpose:**
Next steps for deeper analysis:

1. Enhanced Employee Analysis:
   - Examine job title distribution by gender
   - Analyze salary/pay history data if available
   - Investigate department movement patterns

2. Temporal Analysis Expansion:
   - Compare hiring spikes with business events
   - Analyze employee tenure and turnover
   - Examine seasonal hiring patterns

3. Department Analysis:
   - Verify completeness of department history data
   - Analyze department growth over time
   - Cross-refe

---

### Step 4: Error Recovery & Robust Loading

**Inputs:** None (reads raw data)
**Outputs:** Console output only
**Script:** `scripts/step_04_error-recovery-robust-loading.py`

**Purpose:**
Root cause analysis:
1. Environment behavior: The execution context appears to reset between code blocks
2. Import persistence: Previous imports are not being maintained
3. Error propagation: The initial import failure cascades through all dependent operations

Solution approach:
1. Make each code block completely self-contained with all required imports
2. Add explicit error handling for import statements
3. Verify module availability before proceeding with analysis
4. Consider alternative appr

---

### Step 5: Data Validation & Quality Report

**Inputs:** `Employee.csv`, `EmployeePayHistory.csv`, `Person.csv`, `Department.csv`, `EmployeeDepartmentHistory.csv`
**Outputs:** Console output only
**Script:** `scripts/step_05_data-validation-quality-report.py`

**Purpose:**
Root cause analysis:
1. The expression `None in [person_df, employee_df, dept_df]` tries to evaluate DataFrames as booleans
2. Pandas intentionally makes this ambiguous to prevent accidental misuse
3. We need explicit checks for None values rather than containment testing

Solution approach:
1. Replace the ambiguous condition with explicit None checks
2. Add more granular error reporting for dataset loading
3. Implement proper validation of DataFrame contents
4. Consider adding dataset checksum 

---

### Step 6: Data Loading & Profiling

**Inputs:** `EmployeeDepartmentHistory.csv`, `Employee.csv`, `Person.csv`, `Department.csv`
**Outputs:** Console output only
**Script:** `scripts/step_06_data-loading-profiling.py`

**Purpose:**
Root cause analysis:
1. Column name mismatch: The gender data may exist under a different column name
2. Data structure variation: The dataset version may differ from expected schema
3. Embedded data: Gender information might be in the Demographics XML field
4. Validation over-specification: Our requirements may be too strict

Solution approach:
1. First examine actual column names in Person.csv
2. Check if gender data exists in alternative columns or formats
3. Explore the Demographics XML fiel

---

### Step 7: Data Validation & Quality Report (Phase 2)

**Inputs:** `EmployeeDepartmentHistory.csv`, `Employee.csv`, `Person.csv`, `Department.csv`
**Outputs:** Console output only
**Script:** `scripts/step_07_data-validation-quality-report-phase-2.py`

**Purpose:**
Root Cause Analysis:
1. Primary Issue: Over-reliance on XML data when structured data exists
2. Secondary Issue: XML parsing implementation needs improvement
3. Missed Opportunity: Employee.csv gender data was validated but unused

Solution Strategy:
1. Prioritize structured gender data from Employee.csv
2. Keep XML parsing as fallback only
3. Implement more robust XML parsing with:
   - Better error handling
   - XML namespace awareness
   - Alternative parsing approaches

Implementation Improv

---

### Step 8: Data Merging & Integration (Phase 2)

**Inputs:** None (reads raw data)
**Outputs:** Console output only
**Script:** `scripts/step_08_data-merging-integration-phase-2.py`

**Purpose:**
Root Cause Analysis:
1. Primary Oversight:
   - Not utilizing Employee.csv's Gender column due to merge suffix (_y)
   - Failing to align our analysis with available structured data

2. Data Limitations:
   - Department history has limited temporal coverage
   - Many department assignments lack end dates

3. XML Challenges:
   - Complex namespaces in Demographics field
   - Possibly malformed XML in some records

Solution Strategy:
1. Immediate Fixes:
   - Directly use Employee.csv gender data
 

---

### Step 9: Data Validation & Quality Report (Phase 3)

**Inputs:** `EmployeeDepartmentHistory.csv`, `Employee.csv`, `EmployeePayHistory.csv`, `Department.csv`
**Outputs:** Console output only
**Script:** `scripts/step_09_data-validation-quality-report-phase-3.py`

**Purpose:**
Root cause analysis:
1. The expression `None in [employee_df, dept_df, emp_dept_df]` tries to evaluate DataFrames as booleans
2. Pandas intentionally makes this ambiguous to prevent misuse
3. We need to:
   - Use explicit None checks with `is None`
   - Verify dataset integrity more robustly
   - Implement proper DataFrame validation

Solution approach:
1. Replace ambiguous condition with explicit None checks
2. Add dataset quality validation:
   - Check for empty DataFrames
   - Verify required

---

### Step 10: Data Visualization

**Inputs:** `EmployeeDepartmentHistory.csv`, `Employee.csv`, `EmployeePayHistory.csv`, `Department.csv`
**Outputs:** Console output only
**Script:** `scripts/step_10_data-visualization.py`

**Purpose:**
Next Steps for Deeper Analysis:

1. Gender Pay Equity Investigation:
   - Control for job title/level
   - Analyze pay progression over time
   - Examine promotion patterns

2. Department Analysis:
   - Correlate duration with performance metrics
   - Analyze department growth trends
   - Examine cross-department movement

3. Tenure Analysis:
   - Correlate tenure with pay/seniority
   - Analyze turnover patterns
   - Examine hiring waves

4. Visualization Enhancements:
   - Interactive dashboar

---

### Step 11: Data Merging & Integration (Phase 3)

**Inputs:** None (reads raw data)
**Outputs:** Console output only
**Script:** `scripts/step_11_data-merging-integration-phase-3.py`

**Purpose:**
Root Cause Analysis:
1. Data Flow Issue:
   - Tenure calculated on employee_df
   - Pay data merged separately
   - Final visualization uses emp_pay which lacks tenure data

2. Structural Problems:
   - Incomplete data merging pipeline
   - Column name inconsistencies
   - Missing data validation steps

3. Analysis Limitations:
   - Job level extraction too simplistic
   - Department transitions need temporal analysis
   - Pay equity analysis could control for more variables

Solution Strategy:


---

### Step 12: 1. Missing Dependency

**Inputs:** None (reads raw data)
**Outputs:** Console output only
**Script:** `scripts/step_12_1-missing-dependency.py`

**Purpose:**
Root Cause Analysis:
1. Missing Dependency:
   - Regular expression operations used without importing 're'
   - Python cannot resolve the 're' reference

2. Impact Assessment:
   - Job level classification fails completely
   - Pay equity analysis becomes less accurate
   - Subsequent analyses using job levels are affected

3. Solution Requirements:
   - Add 're' to imports
   - Maintain all existing functionality
   - Ensure backward compatibility

Implementation Improvements:
1. Comprehensive 

---

### Step 13: Regression Modeling

**Inputs:** `EmployeeDepartmentHistory.csv`, `Employee.csv`, `EmployeePayHistory.csv`, `Department.csv`
**Outputs:** Console output only
**Script:** `scripts/step_13_regression-modeling.py`

**Purpose:**
Root Cause Analysis:
1. Technical Misimplementation:
   - Incorrect assumption about scipy.stats capabilities
   - Missing statsmodels import for regression
   - Functionality split between libraries

2. Impact Assessment:
   - Pay equity analysis incomplete without regression
   - Cannot control for multiple factors simultaneously
   - Limited statistical inference capabilities

3. Solution Requirements:
   - Add statsmodels import
   - Implement proper OLS regression
   - Maintain existing ana

---


## Final Output & Deliverables

# Comprehensive Analysis of Employee Data: Pay Equity, Career Progression, and Organizational Dynamics

## Executive Summary

This comprehensive report presents a detailed analysis of employee data spanning multiple dimensions including compensation, career progression, departmental mobility, and demographic patterns. The study leverages advanced statistical techniques and data visualization methods to uncover meaningful insights from organizational data, with particular emphasis on pay equity considerations, career trajectory analysis, and workforce dynamics. Our analysis draws upon multiple interconnected datasets containing detailed employment records, compensation history, department assignments, and demographic information, enabling a holistic view of organizational patterns and potential areas for improvement. The findings reveal several significant patterns in compensation structures, gender disparities in leadership representation, and departmental mobility trends that warrant further examination by human resources professionals and organizational leadership.

## Data Description and Methodology

The analysis incorporates four primary datasets containing employee records from a mid-sized organization over an eight-year period from 2006 to 2014. The Employee dataset comprises 290 records with 16 attributes including demographic information, job titles, and hire dates. The EmployeePayHistory dataset contains 316 records documenting compensation changes over time. Departmental assignments are tracked in the EmployeeDepartmentHistory dataset (296 records), while department metadata appears in the Department dataset (16 records). Our methodological approach combines exploratory data analysis with inferential statistics, employing multiple regression techniques to control for confounding variables when examining pay equity. All analyses were conducted using Python's scientific computing stack including pandas for data manipulation, statsmodels for regression analysis, and matplotlib/seaborn for visualization. Data validation procedures ensured the integrity of our findings, with particular attention to handling missing data and verifying temporal consistency across records.

## Pay Equity Analysis

The examination of compensation patterns reveals several noteworthy findings regarding pay equity across gender lines and job levels. Our initial descriptive analysis shows female employees in leadership positions earn a mean hourly rate of $37.16 (SD=$16.37), compared to $40.59 (SD=$18.44) for their male counterparts. This 8.4% raw pay gap narrows considerably when controlling for tenure and job level in our regression models. The most striking disparity emerges in technical roles classified as "Other," where male employees demonstrate both higher maximum compensation ($125.50 vs $60.10) and greater variance in pay distribution. Our regression analysis, which accounts for 72.3% of pay variance (adjusted R²=0.723), indicates that each additional year


---

## How to Run

### Local Execution
```bash
# Install dependencies
pip install pandas openpyxl

# Run each step sequentially
cd case_44_15629
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
