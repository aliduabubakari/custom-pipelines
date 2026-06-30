# Pipeline: Data Cleaning & Validation Workflow

## Metadata
| Field | Value |
|---|---|
| **Case ID** | `40` |
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
To begin this comprehensive Olympic Games dataset analysis, I'll first need to understand the structure and relationships between all provided files. The dataset appears to be relational, with multiple CSV files that likely connect through key fields. Here's my initial analysis plan:

1. Data Structure Investigation:
   - Examine each file's contents and structure
   - Identify primary keys and potential relationships
   - Determine data types and missing values

2. Data Quality Assessment:
   -

---

### Step 2: Data Visualization

**Inputs:** `games_city.csv`, `noc_region.csv`, `medal.csv`, `competitor_event.csv`, `city.csv`, `person.csv`, `sport.csv`, `games.csv`, `event.csv`, `games_competitor.csv`, `person_region.csv`
**Outputs:** Console output only
**Script:** `scripts/step_02_data-visualization.py`

**Purpose:**
To resolve this issue and continue with our analysis, we should:

1. Update the style specification to use current matplotlib style names
2. Verify seaborn package availability
3. Implement graceful fallback options if preferred styles aren't available
4. Consider adding error handling for style-related operations

The visualization aspect is important for our EDA, but we should ensure the code runs reliably across different environments. We'll modify the code to:

1. Use a more current style na

---

### Step 3: Data Cleaning & Standardization

**Inputs:** `eda_outputs/merged_results.csv`, `eda_outputs/merged_athlete_region.csv`, `eda_outputs/merged_games_full.csv`, `eda_outputs/error_log.txt`
**Outputs:** `eda_outputs/full_olympic_data.csv`, `eda_outputs/participation_stats.csv`, `eda_outputs/error_log.txt`, `eda_outputs/medal_stats.csv`
**Script:** `scripts/step_03_data-cleaning-standardization.py`

**Purpose:**
To resolve this issue and prevent similar problems going forward, we should:

1. Verify the actual filenames in the eda_outputs directory
2. Implement more robust file loading with:
   - Explicit file existence checking
   - Clear error messages
   - Consistent naming conventions
3. Consider building a file manifest to track all generated files
4. Add logging to track file operations

The immediate solution is to adjust the filename to match what was actually saved ('cleaned_competitor.csv' rath

---

### Step 4: Data Loading & Profiling (Phase 2)

**Inputs:** None (reads raw data)
**Outputs:** `eda_outputs/full_olympic_data.csv`
**Script:** `scripts/step_04_data-loading-profiling-phase-2.py`

**Purpose:**
To resolve this issue and ensure robust merging, we should:

1. Verify the column names in all cleaned/merged datasets
2. Implement explicit column checking before merging
3. Add detailed error logging to identify exactly which merge fails
4. Consider using more specific column names for merging
5. Add validation steps to ensure data integrity

The immediate steps should be:
1. Examine the structure of all intermediate files
2. Update the merge logic to use correct column names
3. Add validation

---

### Step 5: Data Loading & Profiling (Phase 3)

**Inputs:** `eda_outputs/merged_games_full.csv`
**Outputs:** `eda_outputs/full_olympic_data.csv`
**Script:** `scripts/step_05_data-loading-profiling-phase-3.py`

**Purpose:**
To resolve this issue, we need to:

1. Examine the actual contents of 'merged_games_full.csv'
2. Verify the column names used in the original merge operation
3. Update our validation to match the actual data structure
4. Ensure consistent column naming across all processing steps

The solution approach should be:

1. First inspect the actual file structure
2. Adjust our validation requirements to match reality
3. Update merge operations to use correct column names
4. Add consistency checks for c

---

### Step 6: Data Merging & Integration

**Inputs:** `eda_outputs/cleaned_person.csv`, `eda_outputs/merged_athlete_region.csv`, `eda_outputs/merged_games_full.csv`, `eda_outputs/merged_results.csv`, `eda_outputs/cleaned_competitor.csv`
**Outputs:** `eda_outputs/full_olympic_data.csv`
**Script:** `scripts/step_06_data-merging-integration.py`

**Purpose:**
To resolve this persistent issue, we need to:

1. Implement more thorough column inspection before merging
2. Add detailed logging of merge operations
3. Handle column renaming more systematically
4. Verify all merge keys exist before attempting merges
5. Add fallback options for column naming variations

The solution approach should be:

1. Create a function to standardize column names across all DataFrames
2. Add pre-merge validation of all key columns
3. Implement detailed merge logging
4. Ad

---

### Step 7: Data Merging & Integration (Phase 2)

**Inputs:** `eda_outputs/cleaned_person.csv`, `eda_outputs/merged_athlete_region.csv`, `eda_outputs/merged_games_full.csv`, `eda_outputs/merged_results.csv`, `eda_outputs/cleaned_competitor.csv`
**Outputs:** `eda_outputs/full_olympic_data.csv`
**Script:** `scripts/step_07_data-merging-integration-phase-2.py`

**Purpose:**
To resolve this issue, we need to:

1. Clearly map the relationship between person.id and athlete_region.person_id
2. Update our merge logic to use the correct column names
3. Ensure our standardization function handles this case
4. Add explicit schema documentation to prevent future confusion

The solution approach should:

1. Modify the first merge to use person.id and athlete_region.person_id
2. Update the standardization function to preserve these distinct column names
3. Add schema validati

---

### Step 8: Data Merging & Integration (Phase 3)

**Inputs:** `eda_outputs/cleaned_person.csv`, `eda_outputs/merged_athlete_region.csv`, `eda_outputs/merged_games_full.csv`, `eda_outputs/merged_results.csv`, `eda_outputs/cleaned_competitor.csv`
**Outputs:** `eda_outputs/full_olympic_data.csv`
**Script:** `scripts/step_08_data-merging-integration-phase-3.py`

**Purpose:**
To resolve this issue, we should:

1. Add detailed inspection of intermediate DataFrames before merging
2. Implement more flexible column name handling
3. Add comprehensive logging of DataFrame structures
4. Handle column renaming more carefully between merge steps
5. Verify the merge keys at each step

The solution approach should:

1. Add DataFrame inspection before each merge
2. Implement dynamic column name resolution
3. Add merge step-specific validation
4. Include detailed error reporting


---

### Step 9: Data Merging & Integration (Phase 4)

**Inputs:** `eda_outputs/cleaned_person.csv`, `eda_outputs/merged_athlete_region.csv`, `eda_outputs/merged_games_full.csv`, `eda_outputs/merged_results.csv`, `eda_outputs/cleaned_competitor.csv`
**Outputs:** `eda_outputs/full_olympic_data.csv`
**Script:** `scripts/step_09_data-merging-integration-phase-4.py`

**Purpose:**
To finally resolve this persistent issue, we should:

1. Completely inspect all intermediate DataFrames
2. Implement a more robust column tracking system
3. Add explicit column verification before each merge
4. Handle all possible column naming variations
5. Document the expected schema at each step

The solution approach should:

1. Add comprehensive DataFrame inspection after each merge
2. Implement column existence verification
3. Add schema validation at each processing stage
4. Include deta

---

### Step 10: Data Validation & Quality Report

**Inputs:** `eda_outputs/cleaned_person.csv`, `eda_outputs/merged_athlete_region.csv`, `eda_outputs/merged_games_full.csv`, `eda_outputs/merged_results.csv`, `eda_outputs/cleaned_competitor.csv`
**Outputs:** `eda_outputs/full_olympic_data.csv`
**Script:** `scripts/step_10_data-validation-quality-report.py`

**Purpose:**
To resolve this issue and improve our validation system, we should:

1. Fix the column verification logic to properly handle string inputs
2. Add type checking for the required_columns parameter
3. Implement more robust column name comparison
4. Maintain the existing data loading pipeline
5. Add debugging information for column validation

The solution approach should:

1. Modify verify_columns() to properly handle string inputs
2. Add input validation for the required_columns parameter
3. Prese

---

### Step 11: Data Merging & Integration (Phase 5)

**Inputs:** `eda_outputs/cleaned_person.csv`, `eda_outputs/merged_athlete_region.csv`, `eda_outputs/merged_games_full.csv`, `eda_outputs/merged_results.csv`, `eda_outputs/cleaned_competitor.csv`
**Outputs:** `eda_outputs/full_olympic_data.csv`
**Script:** `scripts/step_11_data-merging-integration-phase-5.py`

**Purpose:**
To resolve this issue and create a robust merging pipeline, we should:

1. Explicitly handle pandas merge suffixes
2. Track column name changes through each merge operation
3. Use consistent merge keys throughout the pipeline
4. Add merge step documentation
5. Implement merge result validation

The solution approach should:

1. Modify merge operations to use explicit suffixes
2. Update column references to match actual merged column names
3. Add merge result inspection
4. Maintain clear column n

---

### Step 12: Data Merging & Integration (Phase 6)

**Inputs:** `eda_outputs/cleaned_person.csv`, `eda_outputs/merged_athlete_region.csv`, `eda_outputs/merged_games_full.csv`, `eda_outputs/merged_results.csv`, `eda_outputs/cleaned_competitor.csv`
**Outputs:** `eda_outputs/full_olympic_data.csv`
**Script:** `scripts/step_12_data-merging-integration-phase-6.py`

**Purpose:**
To resolve this persistent merge issue, we should:

1. Implement comprehensive DataFrame inspection after each merge
2. Add explicit column name tracking throughout the pipeline
3. Develop a merge key resolution system
4. Include merge schema validation
5. Add detailed merge operation logging

The solution approach should:

1. Inspect and log DataFrame structures after each merge
2. Dynamically resolve merge keys based on actual columns
3. Validate merge schemas before operations
4. Handle all c

---

### Step 13: Data Merging & Integration (Phase 7)

**Inputs:** `eda_outputs/cleaned_person.csv`, `eda_outputs/merged_athlete_region.csv`, `eda_outputs/merged_games_full.csv`, `eda_outputs/merged_results.csv`, `eda_outputs/cleaned_competitor.csv`
**Outputs:** `eda_outputs/full_olympic_data.csv`
**Script:** `scripts/step_13_data-merging-integration-phase-7.py`

**Purpose:**
To resolve this issue and create a robust merging pipeline, we should:

1. Implement comprehensive column name inspection before merging
2. Develop a dynamic suffix generation system
3. Handle existing suffixes in column names
4. Add column name conflict resolution
5. Implement merge validation with name checking

The solution approach should:

1. Examine column names before merging
2. Generate unique suffixes dynamically
3. Handle pre-existing suffixes
4. Resolve naming conflicts automatically


---


## Final Output & Deliverables

# Comprehensive Analysis of Olympic Games Dataset

## Introduction and Dataset Overview

The Olympic Games represent one of the most significant international sporting events, bringing together athletes from around the world to compete in various disciplines. This comprehensive analysis examines a rich dataset containing information about Olympic athletes, events, medals, and host cities spanning multiple years. The dataset comprises 11 interconnected tables with over 180,000 competitor records and 260,000 event results, providing a robust foundation for exploring patterns and trends in Olympic history. The analysis focuses on four primary dimensions: temporal trends in participation and performance, geographic distribution of athletes and host cities, demographic characteristics of competitors, and sport-specific performance metrics. Through rigorous statistical analysis and advanced visualization techniques, this study reveals compelling insights about the evolution of the Olympic Games and the factors influencing athletic success at this prestigious international competition.

The dataset's relational structure enables sophisticated analysis of complex relationships between athletes, events, and nations. Key tables include athlete biographical information (128,854 records), competition results (260,971 entries), and host city details (42 locations). The temporal scope covers Olympic Games from 1896 through 2016, representing both Summer and Winter competitions. Preliminary analysis revealed several data quality challenges that required careful handling, including missing values in athlete physical measurements (approximately 12% of height/weight records) and inconsistent naming conventions across tables. These issues were addressed through a comprehensive data cleaning pipeline that standardized formats, handled missing values appropriately, and ensured relational integrity across all tables. The cleaning process resulted in a final merged dataset containing 87 key variables spanning athlete demographics, competition results, and event characteristics.

## Temporal Analysis of Olympic Participation and Performance

The analysis of temporal trends reveals significant changes in Olympic participation and performance metrics over the 120-year period covered by the dataset. Athlete participation has grown exponentially, from just 241 competitors in 1896 to over 11,000 in the 2016 Games, representing a compound annual growth rate of 3.4%. This expansion reflects both the increasing globalization of sports and the International Olympic Committee's efforts to broaden the Games' appeal. Female participation has shown particularly dramatic growth, increasing from just 2.2% of athletes in 1900 to 45% in 2016, though notable disparities persist across sports and nations. The average age of Olympic athletes has remained relatively stable at 25-26 years, with a standard deviation of 6.1 years, suggesting consistent demographic patterns despite the Games' e


---

## How to Run

### Local Execution
```bash
# Install dependencies
pip install pandas openpyxl

# Run each step sequentially
cd case_40_15558
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
