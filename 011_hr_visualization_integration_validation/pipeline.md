# Pipeline: Data Cleaning & Validation Workflow

## Metadata
| Field | Value |
|---|---|
| **Case ID** | `5058` |
| **Difficulty** | N/A/5 |
| **Quality** | N/A/5 |
| **Abilities** |  |
| **Total Steps** | 16 |
| **Input Files** | 0 |
| **Output Files** | 0 |

---

## Executive Summary

This comprehensive study examines the intricate relationships between employee tenure, employment status, and bonus allocation patterns within organizational compensation systems. Through rigorous statistical analysis of 5 complete employee records (after data validation), we uncover significant insights about reward distribution mechanisms. The analysis reveals a moderate positive relationship between tenure and bonus amounts (Cohen's d=0.35), though not statistically significant at conventional levels (p=0.285). Full-time employees demonstrated an average tenure of 7.2 years when receiving bonuses, with average bonus amounts of $3,100. The study identifies important patterns in compensation practices while acknowledging limitations stemming from the small sample size and restricted bonus range ($2,900-$3,200).

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

**Inputs:** `hiring.csv`, `evaluation.csv`
**Outputs:** Console output only
**Script:** `scripts/step_01_data-loading-profiling.py`

**Purpose:**
This task requires a comprehensive analysis of employee bonus data across two datasets (evaluation.csv and hiring.csv) with several specific analytical requirements. Let me break down the key components and develop a systematic approach:

1. Data Understanding Phase:
- First need to examine both datasets' structure, columns, and data quality
- Must identify common keys (likely Employee_ID) to merge datasets
- Need to verify presence of required fields: Year_awarded, Start_from, Is_full_time, Bon

---

### Step 2: Data Merging & Integration

**Inputs:** `hiring.csv`, `evaluation.csv`
**Outputs:** `merged_bonus_data.csv`
**Script:** `scripts/step_02_data-merging-integration.py`

**Purpose:**
For the merge operation, we need to consider:
1. Merge Strategy:
- Left join on evaluation data to preserve all bonus records
- This may create NaN values for employees without hiring records
- Need to handle these cases per requirements

2. Data Processing Pipeline:
1. Merge datasets
2. Calculate tenure
3. Filter valid records
4. Split by employment type
5. Perform required analyses

3. Validation Requirements:
- Verify no Employee_IDs are lost during merge
- Check tenure calculations are reaso

---

### Step 3: Data Merging & Integration (Phase 2)

**Inputs:** `hiring.csv`, `evaluation.csv`
**Outputs:** Console output only
**Script:** `scripts/step_03_data-merging-integration-phase-2.py`

**Purpose:**
For our next steps, we should:

1. Diagnostic Checks:
- Compare pre-merge and post-merge record counts
- Examine part-time employee records specifically
- Verify data types and values at each step

2. Remaining Analyses:
- Shop performance analysis (Requirement 2)
- Tenure distribution comparison (Requirement 3)
- Additional visualization for better insights

3. Implementation Strategy:
1. First perform detailed diagnostics
2. Then proceed with shop analysis
3. Finally conduct tenure distributio

---

### Step 4: Data Merging & Integration (Phase 3)

**Inputs:** `hiring.csv`, `evaluation.csv`
**Outputs:** Console output only
**Script:** `scripts/step_04_data-merging-integration-phase-3.py`

**Purpose:**
Revised implementation plan:

1. Processing Pipeline:
1. Load and merge data
2. Calculate tenure immediately after merge
3. Verify column creation
4. Perform filtering
5. Conduct analyses

2. Verification Steps:
- Check columns after merge
- Verify tenure calculation
- Confirm column persistence
- Validate final dataframe structure

3. Error Prevention:
- Use explicit column handling
- Add verification prints
- Include data integrity checks
- Structure operations carefully

4. Code Structure:
- 

---

### Step 5: Data Visualization

**Inputs:** `hiring.csv`, `evaluation.csv`
**Outputs:** `enhanced_shop_analysis.csv`, `statistical_results.csv`
**Script:** `scripts/step_05_data-visualization.py`

**Purpose:**
For comprehensive reporting, we should:

1. Visualization Plan:
- Histograms of tenure by bonus group
- Boxplots for distribution comparison
- Scatterplot of tenure vs bonus amount
- Bar chart of shop performance

2. Statistical Analysis:
- t-test for tenure differences
- Effect size calculation
- Confidence intervals

3. Enhanced Reporting:
- Tabular summary of all findings
- Interpretation of statistical results
- Business implications
- Limitations discussion

4. Implementation Approach:
1. G

---

### Step 6: Data Validation & Quality Report

**Inputs:** `analysis_documentation.txt`, `enhanced_shop_analysis.csv`, `statistical_results.csv`
**Outputs:** `analysis_documentation.txt`
**Script:** `scripts/step_06_data-validation-quality-report.py`

**Purpose:**
For our final verification and reporting preparation:

1. Verification Steps:
- Check file creation
- Validate content structure
- Verify image quality
- Confirm statistical validity

2. Reporting Enhancements:
- Create analysis metadata
- Generate data dictionary
- Document processing steps
- Record key decisions

3. Implementation Approach:
1. File verification checks
2. Summary statistics generation
3. Documentation creation
4. Final quality checks

Here's the code to implement these final st

---

### Step 7: Final Synthesis & Reporting

**Inputs:** `enhanced_shop_analysis.csv`, `final_results_summary.txt`, `evaluation.csv`, `statistical_results.csv`, `hiring.csv`
**Outputs:** `final_results_summary.txt`
**Script:** `scripts/step_07_final-synthesis-reporting.py`

**Purpose:**
For our final reporting preparation:

1. Content Enhancement:
- Statistical interpretation narrative
- Effect size contextualization
- Visual refinement
- Professional formatting

2. Quality Assurance:
- Final data validation
- Output verification
- Consistency checks
- Professional standards review

3. Implementation Plan:
1. Generate final summary
2. Create interpretation narrative
3. Refine visualizations
4. Prepare publication-ready outputs

Here's the code to complete these final steps:

---

### Step 8: Revised Analysis & Refinement

**Inputs:** `enhanced_shop_analysis.csv`, `final_results_summary.txt`, `evaluation.csv`, `statistical_results.csv`, `hiring.csv`
**Outputs:** `final_results_summary.txt`
**Script:** `scripts/step_08_revised-analysis-refinement.py`

**Purpose:**
Revised approach for final reporting:

1. Data Preparation:
- Clean column names first
- Ensure consistent formatting
- Verify data integrity

2. Output Generation:
- Use robust string formatting
- Handle special characters
- Maintain professional standards

3. Quality Assurance:
- Verify file generation
- Check content accuracy
- Validate formatting

4. Implementation Steps:
1. Clean column names
2. Generate summary statistics
3. Create final visualization
4. Produce comprehensive report

Here'

---

### Step 9: Data Visualization (Phase 2)

**Inputs:** `enhanced_shop_analysis.csv`, `statistical_results.csv`, `report_structure.json`
**Outputs:** `report_structure.json`
**Script:** `scripts/step_09_data-visualization-phase-2.py`

**Purpose:**
For our final polishing:

1. Code Refinement:
- Update seaborn parameters
- Maintain visualization quality
- Ensure reproducibility

2. Output Verification:
- Check file integrity
- Validate content
- Confirm visual quality

3. Reporting Preparation:
- Structure academic report
- Prepare methodology section
- Document limitations

Here's the final refinement code:

---

### Step 10: Data Visualization (Phase 3)

**Inputs:** `hiring.csv`, `report_structure.json`, `evaluation.csv`
**Outputs:** `report_structure.json`
**Script:** `scripts/step_10_data-visualization-phase-3.py`

**Purpose:**
For robust final implementation:

1. Code Structure:
- Complete data loading
- Explicit processing steps
- Clear variable definitions
- Self-contained operations

2. Error Prevention:
- Check variable existence
- Verify data completeness
- Include validation steps

3. Final Implementation:
1. Load all required data
2. Perform complete processing
3. Generate visualization
4. Create report structure

Here's the corrected and complete code:

---

### Step 11: Data Visualization (Phase 4)

**Inputs:** `enhanced_shop_analysis.csv`, `evaluation.csv`, `statistical_results.csv`, `hiring.csv`, `employee_bonus_analysis_report.md`
**Outputs:** `employee_bonus_analysis_report.md`
**Script:** `scripts/step_11_data-visualization-phase-4.py`

**Purpose:**
For the final report generation:

1. Content Organization:
- Introduction and background
- Methods and materials
- Results with visualizations
- Discussion and limitations

2. Technical Implementation:
- Markdown report generation
- Image embedding
- Table formatting
- Professional styling

3. Quality Assurance:
- Content completeness
- Technical accuracy
- Visual clarity
- Readability check

Here's the code to compile the final report:

---

### Step 12: Data Validation & Quality Report (Phase 2)

**Inputs:** `enhanced_shop_analysis.csv`, `evaluation.csv`, `statistical_results.csv`, `hiring.csv`, `employee_bonus_analysis_report.md`
**Outputs:** `employee_bonus_analysis_report.md`
**Script:** `scripts/step_12_data-validation-quality-report-phase-2.py`

**Purpose:**
For final robust reporting:

1. Data Verification:
- Load and inspect all source files
- Verify column names
- Check data completeness

2. Report Generation:
- Align with real data structure
- Add validation checks
- Handle missing data

3. Final Output:
- Professional formatting
- Complete content
- Accurate references

Here's the corrected final report code:

---

### Step 13: Data Validation & Quality Report (Phase 3)

**Inputs:** `enhanced_shop_analysis.csv`, `evaluation.csv`, `statistical_results.csv`, `hiring.csv`, `employee_bonus_analysis_report.md`
**Outputs:** `employee_bonus_analysis_report.md`
**Script:** `scripts/step_13_data-validation-quality-report-phase-3.py`

**Purpose:**
For final robust reporting:

1. Data Verification:
- Check file existence
- Validate column presence
- Verify data types
- Ensure completeness

2. Report Generation:
- Flexible column mapping
- Graceful error handling
- Comprehensive validation
- Clear user feedback

3. Final Output:
- Professional formatting
- Complete content
- Accurate references

Here's the corrected final report code with enhanced validation:

---

### Step 14: Data Loading & Profiling (Phase 2)

**Inputs:** `statistical_results.csv`
**Outputs:** Console output only
**Script:** `scripts/step_14_data-loading-profiling-phase-2.py`

**Purpose:**
For final resolution:

1. Diagnostic Approach:
- Examine statistical_results.csv
- Verify analysis pipeline
- Generate missing metrics
- Ensure complete reporting

2. Implementation Strategy:
1. First inspect current data
2. Then regenerate or adapt
3. Finally produce report

3. Quality Controls:
- Complete metric validation
- Robust error handling
- Clear documentation
- Professional outputs

Here's the diagnostic code:

---

### Step 15: Data Visualization (Phase 5)

**Inputs:** `enhanced_shop_analysis.csv`, `evaluation.csv`, `statistical_results.csv`, `hiring.csv`, `employee_bonus_analysis_report.md`
**Outputs:** `employee_bonus_analysis_report.md`
**Script:** `scripts/step_15_data-visualization-phase-5.py`

**Purpose:**
For final report generation:

1. Column Handling:
- Flexible name matching
- Apostrophe handling
- Case insensitivity
- Comprehensive validation

2. Report Content:
- Complete statistical results
- Detailed methodology
- Visualizations
- Comprehensive discussion

3. Quality Assurance:
- Verify all data references
- Check numerical accuracy
- Validate visualizations
- Ensure professional formatting

Here's the corrected final report code:

---

### Step 16: Data Merging & Integration (Phase 4)

**Inputs:** `enhanced_shop_analysis.csv`, `evaluation.csv`, `statistical_results.csv`, `hiring.csv`, `employee_bonus_analysis_report.md`
**Outputs:** `employee_bonus_analysis_report.md`
**Script:** `scripts/step_16_data-merging-integration-phase-4.py`

**Purpose:**
For final robust implementation:

1. Data Processing:
- Complete reload of source data
- Verified merge operation
- Explicit tenure calculation
- Validated output

2. Report Generation:
- Column existence checks
- Robust error handling
- Complete validation
- Professional formatting

3. Quality Controls:
- Step-by-step verification
- Intermediate checks
- Final validation
- Comprehensive testing

Here's the corrected code:

---


## Final Output & Deliverables

# Comprehensive Analysis of Employee Tenure, Employment Status, and Bonus Allocation Patterns

## Executive Summary
This comprehensive study examines the intricate relationships between employee tenure, employment status, and bonus allocation patterns within organizational compensation systems. Through rigorous statistical analysis of 5 complete employee records (after data validation), we uncover significant insights about reward distribution mechanisms. The analysis reveals a moderate positive relationship between tenure and bonus amounts (Cohen's d=0.35), though not statistically significant at conventional levels (p=0.285). Full-time employees demonstrated an average tenure of 7.2 years when receiving bonuses, with average bonus amounts of $3,100. The study identifies important patterns in compensation practices while acknowledging limitations stemming from the small sample size and restricted bonus range ($2,900-$3,200).

## 1. Introduction and Background

The examination of compensation structures represents a critical area of organizational research, particularly in understanding how tenure and employment status influence reward allocation. This study builds upon existing literature in human resource management by analyzing a unique dataset that links employee tenure records with bonus allocation patterns. Our dataset comprises 6 evaluation records and 7 hiring records, which after rigorous quality control procedures yielded 5 complete cases for final analysis. The research focuses specifically on employees who received bonuses, examining how their length of service correlates with reward amounts while controlling for employment type and organizational unit.

Contemporary compensation theory suggests that tenure should demonstrate a positive relationship with reward amounts, reflecting both human capital accumulation and organizational commitment. Our analysis tests this hypothesis within a specific organizational context, where bonus allocations ranged from $2,900 to $3,200 across the observed period. The study period covers employees hired between 2003 and 2013, with bonus awards occurring between 2011 and 2018. This temporal span allows for examination of tenure effects while controlling for potential cohort differences in compensation practices.

Methodologically, this research combines traditional statistical techniques with modern data visualization approaches to provide both quantitative precision and intuitive understanding of compensation patterns. We employ independent samples t-tests for group comparisons, Cohen's d for effect size measurement, and comprehensive visualization techniques to explore the data from multiple perspectives. The analytical framework incorporates robust data validation procedures to ensure the reliability of our findings while maintaining transparency about the study's limitations.

The organizational context for this research represents a particularly interesting case study, as the bonus allocation patt


---

## How to Run

### Local Execution
```bash
# Install dependencies
pip install pandas openpyxl

# Run each step sequentially
cd case_5058_12524
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
