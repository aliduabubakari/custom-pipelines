# Pipeline: Data Cleaning & Validation Workflow

## Metadata
| Field | Value |
|---|---|
| **Case ID** | `11846` |
| **Difficulty** | 4/5 |
| **Quality** | 5/5 |
| **Abilities** | Data Preparation, Data Analysis, Data Modeling, Code Generation, Reasoning, Instruction Following, Structural Understanding |
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

### Step 1: Error Recovery & Robust Loading

**Inputs:** None (reads raw data)
**Outputs:** Console output only
**Script:** `scripts/step_01_error-recovery-robust-loading.py`

**Purpose:**
The JSON decode error suggests there's an issue with the format of the aircraft.json file. The error "Extra data" typically occurs when:
1. The JSON file contains multiple JSON objects concatenated together without proper array formatting
2. There might be malformed JSON syntax
3. The file might actually be JSON Lines format (each line is a separate JSON object)

Given this error, we need to:
1. First verify the actual content of the JSON file
2. Try alternative JSON parsing approaches
3. Handle

---

### Step 2: Data Loading & Profiling

**Inputs:** `airport_aircraft.json`, `aircraft.json`
**Outputs:** `airport_aircraft.json`, `cleaned_aircraft_data.csv`, `aircraft.json`
**Script:** `scripts/step_02_data-loading-profiling.py`

**Purpose:**
The error indicates that `aircraft_df` is not defined when we try to use it, despite having successfully created it in the previous code execution. This suggests we need to:

1. Re-establish our DataFrames from the JSON Lines data
2. Ensure proper variable scope and persistence
3. Verify the data structure before processing

Root cause:
- The previous successful DataFrame creation wasn't preserved in the current execution context
- We need to reload the data before processing

Solution approach:

---

### Step 3: Data Loading & Profiling (Phase 2)

**Inputs:** `airport_aircraft.json`, `aircraft.json`
**Outputs:** `aircraft_classification.csv`, `airport_aircraft.json`, `aircraft.json`
**Script:** `scripts/step_03_data-loading-profiling-phase-2.py`

**Purpose:**
The persistent "not defined" error suggests we're losing our DataFrame between executions. Let's implement a more robust solution:

1. Root Cause Analysis:
   - The execution environment appears to not maintain state between code blocks
   - We need to ensure all required data is loaded within each execution

2. Solution Approach:
   - Create a self-contained function that handles the entire workflow
   - Load data, process it, and generate output in one continuous flow
   - Add comprehensive er

---

### Step 4: Data Visualization

**Inputs:** `classification_report.txt`, `aircraft_classification.csv`, `cleaned_aircraft_data.csv`
**Outputs:** `classification_report.txt`
**Script:** `scripts/step_04_data-visualization.py`

**Purpose:**
The error indicates that pandas ('pd') was not imported in the current execution context. This suggests we need to:

1. Ensure all required imports are included
2. Maintain proper execution state between code blocks
3. Verify data availability before processing

Root Cause:
- The visualization code assumes pandas is already imported
- The execution environment doesn't maintain imports between code blocks

Solution Approach:
1. Create a self-contained visualization script
2. Include all necessary

---

### Step 5: Data Visualization (Phase 2)

**Inputs:** `aircraft_classification.csv`, `cleaned_aircraft_data.csv`
**Outputs:** Console output only
**Script:** `scripts/step_05_data-visualization-phase-2.py`

**Purpose:**
The error indicates a column name mismatch when trying to generate visualizations. This suggests:

1. Data Structure Issue:
   - The code expects an 'Aircraft' column that doesn't exist in the CSV
   - The column names in the saved CSV may differ from the DataFrame we worked with earlier

2. Root Cause:
   - Possible column name changes during CSV saving
   - Inconsistent column references between code blocks

3. Solution Approach:
   - First inspect the actual CSV file structure
   - Verify all

---

### Step 6: Data Visualization (Phase 3)

**Inputs:** `aircraft_classification.csv`, `cleaned_aircraft_data.csv`
**Outputs:** Console output only
**Script:** `scripts/step_06_data-visualization-phase-3.py`

**Purpose:**
The visualization generation has now completed successfully. Here's the analysis of the results:

1. Successful Outputs:
   - Verified all required columns exist in both CSV files
   - Generated three visualization files:
     * weight_class_distribution.png
     * disk_loading_by_weight.png
     * airport_assignments.png
   - Confirmed data integrity through column validation

2. Data Insights:
   - The classification file contains all expected columns
   - The cleaned data file includes both o

---

### Step 7: Final Synthesis & Reporting

**Inputs:** `README.md`
**Outputs:** `README.md`
**Script:** `scripts/step_07_final-synthesis-reporting.py`

**Purpose:**
The error indicates that pandas ('pd') is not imported in the current execution context. This is the final step in our analysis pipeline, so we should:

1. Ensure all required imports are included
2. Make the summary generation self-contained
3. Provide comprehensive output verification

Root Cause:
- Missing pandas import in the final summary function
- Need to maintain complete independence of each code block

Solution Approach:
1. Create a fully self-contained summary function
2. Include all 

---

### Step 8: Error Recovery & Robust Loading (Phase 2)

**Inputs:** `README.md`
**Outputs:** `README.md`
**Script:** `scripts/step_08_error-recovery-robust-loading-phase-2.py`

**Purpose:**
The empty execution output suggests the script ran without producing any console output, which could indicate either:

1. Successful silent execution
2. Execution failure without error messages
3. Missing print statements in critical sections

To properly diagnose and complete the task, we should:

1. Verify file generation
2. Add more detailed progress reporting
3. Ensure proper error handling
4. Generate visible confirmation of completion

The following enhanced code will:
1. Explicitly verify

---

### Step 9: The persistent empty execution output suggests a fundamental issue with the execution environment. G

**Inputs:** `file_verification_report.txt`
**Outputs:** `file_verification_report.txt`
**Script:** `scripts/step_09_the-persistent-empty-execution-output-su.py`

**Purpose:**
The persistent empty execution output suggests a fundamental issue with the execution environment. Given multiple attempts to generate output have failed, we should:

1. Simplify the approach to focus on core verification
2. Implement basic file checking without dependencies
3. Generate minimal but reliable output
4. Document the issue for further troubleshooting

The following streamlined code will:
1. Remove pandas dependency for basic verification
2. Focus on essential file checks
3. Generate

---

### Step 10: The verification results show that all files were successfully generated except for 'classification_

**Inputs:** `classification_report.txt`, `README.md`
**Outputs:** `classification_report.txt`, `README.md`
**Script:** `scripts/step_10_the-verification-results-show-that-all-f.py`

**Purpose:**
The verification results show that all files were successfully generated except for 'classification_report.txt'. Here's the analysis:

1. Successful Outputs:
   - All CSV, PNG, and PDF files were properly created
   - File sizes appear reasonable for their formats
   - Verification report was generated successfully

2. Missing File:
   - 'classification_report.txt' was not found
   - This was likely generated in a previous step that didn't persist

3. Next Steps:
   - Recreate the missing text r

---

### Step 11: Final Synthesis & Reporting (Phase 2)

**Inputs:** `ANALYSIS_COMPLETE.txt`
**Outputs:** `ANALYSIS_COMPLETE.txt`
**Script:** `scripts/step_11_final-synthesis-reporting-phase-2.py`

**Purpose:**
The successful execution confirms all required files have been properly generated and verified. Here's the final assessment:

1. Completion Status:
   - All output files successfully created
   - Missing classification report regenerated
   - Comprehensive README documentation in place
   - Final verification passed

2. Output Files:
   - 3 CSV files with classification data and metrics
   - 3 visualization PNG files
   - 3 report files (PDF, TXT, MD)
   - Verification report

3. Final Steps:
  

---


## Final Output & Deliverables

The aircraft classification and airport assignment analysis has been successfully completed. Here's the comprehensive summary of the entire process:

1. **Data Processing Pipeline**:
   - Successfully processed aircraft data from JSON files
   - Cleaned and standardized all measurements to metric units
   - Implemented K-means clustering for weight classification
   - Applied percentile-based binning for disk loading classification
   - Counted airport assignments for each aircraft

2. **Output Files Generated**:
   - **Data Files**:
     - `aircraft_classification.csv`: Main classification results
     - `cleaned_aircraft_data.csv`: Standardized metric data
   - **Visualizations**:
     - `weight_class_distribution.png`: Weight class chart
     - `disk_loading_by_weight.png`: Disk loading analysis
     - `airport_assignments.png`: Assignment distribution
   - **Reports**:
     - `aircraft_classification_report.pdf`: Comprehensive analysis
     - `classification_report.txt`: Summary findings
     - `file_verification_report.txt`: Output verification
     - `README.md`: Complete documentation
   - **Archive**:
     - `aircraft_analysis_results_[timestamp].zip`: All outputs packaged

3. **Key Findings**:
   - Aircraft were classified into:
     - Weight Classes: 2 Light, 2 Heavy, 1 Medium
     - Disk Loading: 2 Low, 2 High, 1 Medium
   - Airport assignments showed:
     - 4 aircraft assigned to 1 airport each
     - 1 aircraft with no assignments

4. **Quality Assurance**:
   - All output files verified and validated
   - Missing files regenerated when needed
   - Comprehensive documentation created

5. **Final Deliverables**:
   - Zip archive containing all analysis outputs
   - Completion marker file with timestamp
   - Complete documentation in README.md

**Next Steps**:
1. Review the PDF report for complete analysis
2. Examine the CSV files for detailed metrics
3. Share the zip archive with stakeholders
4. Consider manual review of classification thresholds for edge cases

The analysis has been successfully completed and all outputs are ready for use. The final zip archive `aircraft_analysis_results_20250715_082357.zip` contains the complete set of results for further examination and reporting.

```plaintext
ANALYSIS COMPLETE
================
Timestamp: 20250715_082357
Output Files: 9
Archive: aircraft_analysis_results_20250715_082357.zip
Verification: All files validated
Status: Success
```


---

## How to Run

### Local Execution
```bash
# Install dependencies
pip install pandas openpyxl

# Run each step sequentially
cd case_11846_22824
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
