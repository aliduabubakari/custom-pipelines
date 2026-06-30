# Pipeline: Data Cleaning & Validation Workflow

## Metadata
| Field | Value |
|---|---|
| **Case ID** | `11742` |
| **Difficulty** | 4/5 |
| **Quality** | 5/5 |
| **Abilities** | Data Preparation, Data Analysis, Data Visualization, Data Modeling, Data Insight, Code Generation, Reasoning, Numerical Calculation, Instruction Following, Structural Understanding |
| **Total Steps** | 15 |
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

### Step 1: Data Loading & Profiling: Initial Data Inspection

**Inputs:** `Documents.xlsx`, `Documents_Mailed.csv`
**Outputs:** Console output only
**Script:** `scripts/step_01_data-loading-profiling-initial-data-insp.py`

**Purpose:**
Let me break down this comprehensive data analysis task into manageable steps and plan the approach:

1. **Initial Data Inspection**: First need to examine both input files to understand their structure, data types, and potential issues.

2. **Task Breakdown**:
   - Tasks 1-2: Data preparation (indexing and joining)
   - Tasks 3-12: Various analytical operations including filtering, time calculations, aggregations, and error detection

3. **Execution Strategy**:
   - Start with reading both file

---

### Step 2: Data Merging & Integration

**Inputs:** `Documents.xlsx`, `Documents_Mailed.csv`
**Outputs:** `output_mailed_indexed.csv`, `output_documents_indexed.csv`, `output_combined_docs.csv`
**Script:** `scripts/step_02_data-merging-integration.py`

**Purpose:**
For Task 1 (setting document_id as index) and Task 2 (inner join), we need to:
1. Convert date columns to proper datetime format
2. Set index on both DataFrames
3. Save indexed versions
4. Perform inner join
5. Verify join results

The join will help us understand how many documents have mailing records. Since we have 15 documents and 14 mailing records (with duplicates), the inner join will show us documents that have at least one mailing record.

Potential issues to handle:
- Duplicate documen

---

### Step 3: Data Loading & Profiling

**Inputs:** None (reads raw data)
**Outputs:** `output_overdue_hd_al.csv`
**Script:** `scripts/step_03_data-loading-profiling.py`

**Purpose:**
For robust execution, we should:
1. Restart with proper imports
2. Reload the data with consistent parameters
3. Reattempt Task 3 filtering
4. Include verification steps to confirm proper loading

Additional considerations:
- Ensure datetime parsing is consistent
- Verify the index is properly set
- Include defensive checks for file existence

---

### Step 4: Data Loading & Profiling: Requirements

**Inputs:** None (reads raw data)
**Outputs:** `output_receipt_ym_added.csv`
**Script:** `scripts/step_04_data-loading-profiling-requirements.py`

**Purpose:**
For Task 4 (extract year-month from receipt_date):

1. **Requirements**:
   - Input: output_combined_docs.csv from Task 2
   - Output: New column 'receipt_ym' in YYYY-MM format
   - Must maintain all existing data

2. **Technical Considerations**:
   - receipt_date is already parsed as datetime in combined data
   - Can use dt.strftime('%Y-%m') for conversion
   - Need to handle potential timezone-naive datetimes

3. **Implementation Plan**:
   - Load combined dataset
   - Add new column using d

---

### Step 5: Requirements

**Inputs:** None (reads raw data)
**Outputs:** `output_multiple_mailed_docs.csv`
**Script:** `scripts/step_05_requirements.py`

**Purpose:**
For Task 5 (multiple mailings identification):

1. **Requirements**:
   - Input: Documents_Mailed.csv
   - Output: document_ids with >1 mailing, with all mailing dates and addresses
   - Must preserve all mailing records for duplicates

2. **Technical Approach**:
   - Use value_counts() to find duplicates
   - Filter original dataset for document_ids with counts >1
   - Sort by document_id and mailing_date for readability

3. **Data Considerations**:
   - Already know from Task 1 that 4 records 

---

### Step 6: Requirements (Phase 2)

**Inputs:** None (reads raw data)
**Outputs:** `output_days_to_mail_added.csv`
**Script:** `scripts/step_06_requirements-phase-2.py`

**Purpose:**
For Task 6 (days to first mail calculation):

1. **Requirements**:
   - Calculate time difference between receipt_date and earliest mailing_date
   - Round to 2 decimal places
   - Add new column 'days_to_first_mail'
   - Handle documents with multiple mailings

2. **Technical Considerations**:
   - Need to group by document_id and find min(mailing_date)
   - Calculate timedelta in days
   - Must maintain datetime precision
   - Should verify negative time differences (mailing before receipt)

3

---

### Step 7: Error Recovery & Robust Loading

**Inputs:** None (reads raw data)
**Outputs:** `output_mailing_before_receipt_errors.csv`
**Script:** `scripts/step_07_error-recovery-robust-loading.py`

**Purpose:**
For Task 8 (mailing before receipt errors):

1. **Requirements**:
   - Identify all records where mailing_date < receipt_date
   - Output document_id, receipt_date, and mailing_date
   - Should use the most recent combined dataset

2. **Technical Approach**:
   - Filter records where days_to_first_mail < 0
   - Extract requested columns
   - Sort by severity of time difference
   - Include verification metrics

3. **Data Considerations**:
   - Already calculated days_to_first_mail in Task 6
   -

---

### Step 8: Data Cleaning & Standardization: Requirements

**Inputs:** `Documents.xlsx`
**Outputs:** `output_type_agent_status_counts.csv`
**Script:** `scripts/step_08_data-cleaning-standardization-requiremen.py`

**Purpose:**
For Task 7 (document counts by type, agent, status):

1. **Requirements**:
   - Count documents for all combinations of:
     - document_type_code
     - shipping_agent_code
     - document_status_code
   - Include combinations with zero counts
   - Output as CSV

2. **Technical Approach**:
   - Use pd.crosstab() or groupby with size()
   - Create all possible combinations with pd.MultiIndex
   - Fill missing combinations with zeros
   - Format as clean output table

3. **Data Considerations**:


---

### Step 9: Error Recovery & Robust Loading (Phase 2)

**Inputs:** None (reads raw data)
**Outputs:** `output_mailing_timeliness_added.csv`
**Script:** `scripts/step_09_error-recovery-robust-loading-phase-2.py`

**Purpose:**
For Task 9 (mailing timeliness categorization):

1. **Requirements**:
   - Create new column 'mailing_timeliness' with categories:
     - "on_time" if days_to_first_mail ≤ 15
     - "delayed" if 15 < days_to_first_mail ≤ 30
     - "severely_delayed" if days_to_first_mail > 30
     - "not_mailed" if no mailing record exists

2. **Technical Considerations**:
   - Need to handle NaN values for "not_mailed"
   - Should verify negative days_to_first_mail (from earlier errors)
   - Must maintain origi

---

### Step 10: Data Merging & Integration (Phase 2)

**Inputs:** `Documents.xlsx`
**Outputs:** `output_avg_days_by_status.csv`
**Script:** `scripts/step_10_data-merging-integration-phase-2.py`

**Purpose:**
For Task 10 (average days by status):

1. **Requirements**:
   - Calculate average days_to_first_mail by document_status_code
   - Exclude "not_mailed" records
   - Sort by average days (descending)
   - Handle negative values (either exclude or flag)

2. **Technical Approach**:
   - Filter out negative days_to_first_mail
   - Group by document_status_code
   - Calculate mean and round
   - Sort results

3. **Data Considerations**:
   - Need to merge status codes from original documents
   - Sho

---

### Step 11: Data Merging & Integration (Phase 3)

**Inputs:** `Documents.xlsx`
**Outputs:** `output_avg_days_by_status.csv`
**Script:** `scripts/step_11_data-merging-integration-phase-3.py`

**Purpose:**
Revised plan for Task 10:

1. **Column Handling**:
   - Drop 'document_status_code' from timeliness_df before merge
   - Keep original status codes from documents_df

2. **Merge Strategy**:
   - Use left join on document_id
   - Ensure only one status code column remains

3. **Error Prevention**:
   - Add column existence checks
   - Include merge verification steps
   - Handle potential missing values

4. **Execution Flow**:
   - Load both datasets
   - Clean column names
   - Perform merge
   

---

### Step 12: Data Merging & Integration (Phase 4)

**Inputs:** `Documents.xlsx`, `Documents_Mailed.csv`
**Outputs:** `output_agent_address_ratio.csv`
**Script:** `scripts/step_12_data-merging-integration-phase-4.py`

**Purpose:**
For Task 11 (agent address ratio):

1. **Requirements**:
   - For each shipping_agent_code:
     - Count unique mailed_to_address_id
     - Count total mailings
     - Calculate ratio (unique/total)
   - Round ratio to 3 decimal places

2. **Data Sources**:
   - Documents_Mailed.csv (address info)
   - Documents.xlsx (agent info)

3. **Technical Approach**:
   - Merge mailing records with agent codes
   - Group by shipping_agent_code
   - Calculate both metrics
   - Compute and round ratio
   - 

---

### Step 13: Data Merging & Integration (Phase 5)

**Inputs:** `Documents.xlsx`
**Outputs:** Console output only
**Script:** `scripts/step_13_data-merging-integration-phase-5.py`

**Purpose:**
For Task 12 (correlation calculation):

1. **Requirements**:
   - Filter for "done" status documents
   - Calculate Pearson correlation between:
     - receipt_number (numeric)
     - days_to_first_mail
   - Round result to 4 decimal places
   - Handle potential missing values

2. **Data Source**:
   - output_days_to_mail_added.csv (from Task 6)
   - Need to merge with status codes

3. **Technical Approach**:
   - Load days_to_mail data
   - Merge with original documents for status codes
   - Fi

---

### Step 14: Data Merging & Integration (Phase 6)

**Inputs:** `Documents.xlsx`
**Outputs:** Console output only
**Script:** `scripts/step_14_data-merging-integration-phase-6.py`

**Purpose:**
Revised approach for Task 12:

1. **Column Handling**:
   - Explicitly drop 'document_status_code' from days_df if exists
   - Keep original status codes from documents_df

2. **Merge Strategy**:
   - Use left join on document_id
   - Ensure only one status code column remains

3. **Error Prevention**:
   - Add defensive checks for column existence
   - Include merge verification steps
   - Handle potential edge cases

4. **Execution Flow**:
   - Load both datasets
   - Clean column names
   - P

---

### Step 15: Data Merging & Integration (Phase 7)

**Inputs:** `Documents.xlsx`
**Outputs:** Console output only
**Script:** `scripts/step_15_data-merging-integration-phase-7.py`

**Purpose:**
Revised approach for Task 12:

1. **Alternative Solutions**:
   - Report the data limitation explicitly
   - Show available "done" status records regardless of days_to_first_mail
   - Consider expanding to "working" status if analysis scope allows

2. **Implementation Plan**:
   - Load and merge datasets
   - Filter for "done" status
   - Show all available records
   - Provide descriptive statistics
   - Clearly state correlation limitations

3. **Output Format**:
   - Structured result acknowl

---


## Final Output & Deliverables

After completing all 12 analysis tasks, here is the comprehensive summary of findings and recommendations:

1. **Data Quality Issues**:
   - Found 6 documents with mailing dates before receipt dates (Task 8)
   - Extreme time discrepancies (up to 31 years difference)
   - Recommendation: Implement data validation rules for date sequencing

2. **Document Processing Patterns**:
   - Average mailing delays vary by status (Task 10):
     - Working: 2,676 days
     - Overdue: 2,339 days 
     - Done: 1,060 days
   - Hard Drive documents primarily shipped via FE agent (Task 7)

3. **Shipping Agent Performance**:
   - US agent shows address reuse (ratio 0.833) (Task 11)
   - Other agents maintain perfect 1.0 address ratios
   - Recommendation: Review US agent's delivery practices

4. **Correlation Analysis Limitation**:
   - Only 3 "done" status documents available (Task 12)
   - Calculated correlation of -1.0 suggests inverse relationship but sample size is too small
   - Recommendation: Collect more data for reliable correlation analysis

5. **Key Data Files Generated**:
   - Combined dataset: output_combined_docs.csv
   - Overdue documents: output_overdue_hd_al.csv
   - Agent statistics: output_agent_address_ratio.csv
   - Date anomalies: output_mailing_before_receipt_errors.csv

6. **Actionable Insights**:
   - Prioritize investigation of documents with negative processing times
   - Consider standardizing shipping agent assignments by document type
   - Implement data quality checks for date validity

7. **Technical Implementation Notes**:
   - Handled duplicate document_ids in mailing records
   - Managed datetime conversions and time delta calculations
   - Addressed merge conflicts between datasets
   - Implemented defensive programming for edge cases

The analysis reveals significant opportunities for improving data quality and operational processes. The most critical finding is the systemic issue with mailing dates preceding receipt dates, which requires immediate attention to ensure data reliability for future analyses.

Final recommendation: Conduct a comprehensive data audit to validate all temporal relationships in the document processing system before performing further analytics.


---

## How to Run

### Local Execution
```bash
# Install dependencies
pip install pandas openpyxl

# Run each step sequentially
cd case_11742_22756
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
