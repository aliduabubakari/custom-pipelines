# Pipeline: Data Cleaning & Validation Workflow

## Metadata
| Field | Value |
|---|---|
| **Case ID** | `4822` |
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

**Inputs:** `airport_aircraft.csv`, `aircraft.csv`
**Outputs:** Console output only
**Script:** `scripts/step_01_data-loading-profiling.py`

**Purpose:**
This task requires joining two datasets (aircraft.csv and airport_aircraft.csv) to combine aircraft specifications with their airport assignments, specifically focusing on max disk loading values. The analysis will involve several key steps:

1. Data Inspection:
   - First need to examine both files' structure and contents
   - Check for missing values, data types, and potential join keys
   - Verify if 'max disk loading' exists in aircraft.csv

2. Data Preparation:
   - Identify common fields f

---

### Step 2: Data Merging & Integration

**Inputs:** `airport_aircraft.csv`, `aircraft.csv`
**Outputs:** Console output only
**Script:** `scripts/step_02_data-merging-integration.py`

**Purpose:**
Given the error, we should modify our approach:

1. First, we need to inspect the actual column names in both files without making assumptions
2. Then identify potential join candidates by:
   - Looking for columns with similar names/concepts
   - Checking for unique identifiers that might link aircraft to airports
   - Verifying data types are compatible for joining

3. We should also:
   - Handle the case where column names might have different cases or spaces
   - Check for composite keys if 

---

### Step 3: Data Merging & Integration (Phase 2)

**Inputs:** `airport_aircraft.csv`, `aircraft.csv`
**Outputs:** `aircraft_airport_loading.csv`
**Script:** `scripts/step_03_data-merging-integration-phase-2.py`

**Purpose:**
Next steps for comprehensive analysis:

1. Data Join:
   - Perform inner join on 'Aircraft_ID' to combine specifications with assignments
   - Verify join completeness (ensure no records are lost)
   - Check for potential many-to-many relationships

2. Data Transformation:
   - Extract numerical values from 'Max_disk_Loading' (handle unit conversions)
   - Consider standardizing all disk loading values to a single unit
   - Clean any special characters from numerical fields

3. Result Enhancemen

---

### Step 4: Data Loading & Profiling (Phase 2)

**Inputs:** `aircraft_airport_loading.csv`
**Outputs:** `enhanced_aircraft_loading.csv`
**Script:** `scripts/step_04_data-loading-profiling-phase-2.py`

**Purpose:**
To enhance the analysis, we should:

1. Perform deeper statistical analysis:
   - Calculate loading by aircraft type
   - Examine airport distributions
   - Identify potential outliers

2. Create visualizations to better understand:
   - Distribution of disk loading values
   - Relationship between aircraft size and loading
   - Airport assignment patterns

3. Conduct additional data quality checks:
   - Verify physical plausibility of loading values
   - Cross-check with known aircraft specific

---

### Step 5: Data Visualization

**Inputs:** `enhanced_aircraft_loading.csv`, `aircraft.csv`
**Outputs:** `final_aircraft_analysis.csv`
**Script:** `scripts/step_05_data-visualization.py`

**Purpose:**
To deepen the analysis, we should:

1. Expand the context:
   - Research industry standards for disk loading ranges
   - Compare our values against typical helicopter specifications
   - Examine the relationship between disk loading and aircraft weight

2. Enhance visual analysis:
   - Create a scatter plot of disk loading vs. aircraft weight
   - Generate a radar chart comparing all aircraft specifications
   - Plot airport locations with their assigned aircraft loading

3. Perform advanced cal

---

### Step 6: Data Visualization (Phase 2)

**Inputs:** `aircraft.csv`, `enhanced_aircraft_loading.csv`
**Outputs:** `validated_aircraft_analysis.csv`
**Script:** `scripts/step_06_data-visualization-phase-2.py`

**Purpose:**
To resolve this and improve the analysis:

1. Data Extraction Fixes:
   - Implement more robust number extraction from disk area strings
   - Handle potential comma separators in large numbers
   - Verify all extracted columns exist before plotting

2. Error Prevention:
   - Add intermediate validation checks
   - Implement fallback patterns for data extraction
   - Verify dataframe structures before operations

3. Analysis Enhancement:
   - Maintain original string values for reference
   - Add

---

### Step 7: Cluster Analysis

**Inputs:** `validated_aircraft_analysis.csv`
**Outputs:** `aircraft_performance_summary.csv`, `final_aircraft_metrics.csv`, `loading_correlation_matrix.csv`
**Script:** `scripts/step_07_cluster-analysis.py`

**Purpose:**
To produce a comprehensive final report, we should:

1. Finalize Visualizations:
   - Generate publication-quality comparative charts
   - Add reference lines for industry benchmarks
   - Include detailed axis labels and annotations

2. Advanced Statistical Analysis:
   - Calculate loading-to-weight ratios
   - Perform cluster analysis on aircraft characteristics
   - Compute efficiency metrics per aircraft type

3. Operational Impact Assessment:
   - Estimate runway/pad requirements
   - Analyz

---

### Step 8: Data Visualization (Phase 3)

**Inputs:** `aircraft_performance_summary.csv`, `final_aircraft_metrics.csv`
**Outputs:** `analysis_metadata.csv`
**Script:** `scripts/step_08_data-visualization-phase-3.py`

**Purpose:**
To finalize the analysis, we should:

1. Create Executive Summary Visualizations:
   - Radar chart comparing all aircraft metrics
   - Side-by-side performance benchmark charts
   - Loading efficiency scatter plots

2. Generate Technical Appendices:
   - Detailed statistical tables
   - Calculation methodologies
   - Data source documentation

3. Prepare Final Outputs:
   - Professional report-quality figures
   - Comprehensive CSV exports
   - Analysis metadata

4. Validation Checks:
   - Cross

---

### Step 9: Data Visualization (Phase 4)

**Inputs:** `aircraft_performance_summary.csv`, `final_aircraft_metrics.csv`
**Outputs:** Console output only
**Script:** `scripts/step_09_data-visualization-phase-4.py`

**Purpose:**
To resolve this while maintaining analysis quality:

1. Style Adjustment:
   - Use valid matplotlib built-in styles
   - Verify style availability before application
   - Maintain visual clarity goals

2. Code Robustness:
   - Add style verification step
   - Implement fallback options
   - Preserve all existing functionality

3. Visualization Quality:
   - Ensure grid visibility
   - Maintain professional appearance
   - Keep color consistency

4. Implementation Plan:
   - List available styles

---

### Step 10: Data Visualization (Phase 5)

**Inputs:** `aircraft_performance_summary.csv`, `README.md`, `analysis_methodology.json`, `final_aircraft_metrics.csv`
**Outputs:** `README.md`, `analysis_methodology.json`
**Script:** `scripts/step_10_data-visualization-phase-5.py`

**Purpose:**
To finalize the comprehensive report, we should:

1. Enhance Visual Consistency:
   - Standardize on seaborn-v0_8-whitegrid
   - Ensure all plots use same style
   - Maintain color palette consistency

2. Add Final Report Components:
   - Create executive summary visualization
   - Generate methodology documentation
   - Prepare analysis metadata

3. Quality Assurance:
   - Verify all numerical outputs
   - Cross-check visualization accuracy
   - Validate file outputs

4. Final Output Preparatio

---

### Step 11: Data Validation & Quality Report

**Inputs:** `analysis_environment.json`
**Outputs:** `analysis_environment.json`, `file_checksums.csv`
**Script:** `scripts/step_11_data-validation-quality-report.py`

**Purpose:**
To ensure the analysis is fully complete and ready for delivery:

1. Final Quality Checks:
   - Verify all file permissions
   - Check file sizes for completeness
   - Validate image resolutions

2. Delivery Preparation:
   - Create zip archive of all outputs
   - Generate SHA checksums for verification
   - Document software versions

3. Process Documentation:
   - Record execution environment
   - Note any limitations
   - Suggest future enhancements

4. Validation Script:
   - Create final ve

---

### Step 12: Error Recovery & Robust Loading

**Inputs:** `analysis_environment.json`
**Outputs:** `analysis_environment.json`, `file_checksums.csv`
**Script:** `scripts/step_12_error-recovery-robust-loading.py`

**Purpose:**
To resolve this while maintaining comprehensive environment reporting:

1. System Info Collection:
   - Use platform module for cross-platform compatibility
   - Implement graceful fallbacks
   - Capture essential system characteristics

2. Code Robustness:
   - Handle various OS environments
   - Maintain informative output
   - Preserve existing functionality

3. Implementation Plan:
   - Import platform module
   - Create OS-agnostic info collection
   - Format output consistently

4. Verific

---

### Step 13: Data Validation & Quality Report (Phase 2)

**Inputs:** `analysis_environment.json`
**Outputs:** `analysis_environment.json`, `file_checksums.csv`
**Script:** `scripts/step_13_data-validation-quality-report-phase-2.py`

**Purpose:**
To resolve this while maintaining comprehensive environment reporting:

1. Import Management:
   - Add explicit numpy import
   - Include all required module imports
   - Maintain consistent naming conventions

2. Code Structure:
   - Organize imports at module level
   - Group related imports logically
   - Ensure all dependencies declared

3. Verification:
   - Test import statements
   - Check namespace availability
   - Validate version reporting

4. Implementation:
   - Add missing import
 

---


## Final Output & Deliverables

# Comprehensive Analysis of Aircraft Disk Loading Patterns and Airport Assignment Dynamics

## Introduction and Research Context

The analysis of aircraft disk loading patterns and their relationship to airport assignments represents a critical intersection of aerospace engineering and operational logistics. This study examines the fundamental physical characteristics of rotary-wing aircraft through the lens of disk loading - a crucial performance metric defined as the ratio of an aircraft's weight to its rotor disk area. The dataset under investigation comprises detailed specifications for five distinct helicopter models, including the Robinson R-22 light utility helicopter with a disk loading of 2.6 lb/ft² (14 kg/m²), the Bell 206B3 JetRanger at 3.7 lb/ft² (18 kg/m²), the CH-47D Chinook tandem rotor helicopter at 8.8 lb/ft² (43 kg/m²), and the CH-53E Super Stallion heavy-lift helicopter exhibiting the highest disk loading at 15 lb/ft² (72 kg/m²). These values were extracted from the aircraft.csv dataset through rigorous data processing techniques that involved numerical value extraction from mixed-unit strings and comprehensive data validation procedures.

The operational context of these aircraft becomes particularly significant when examining their airport assignments, as documented in the airport_aircraft.csv dataset. Our analysis reveals that each aircraft type is assigned to a distinct airport, creating a unique operational profile at each location. Airport 2 handles the lightest loading aircraft (Robinson R-22), while Airport 6 manages the most demanding operational scenario with the CH-53E Super Stallion. The intermediate loading aircraft, the Bell 206B3 JetRanger and CH-47D Chinook, are assigned to Airports 1 and 9 respectively, demonstrating a thoughtful distribution of operational requirements across the airport network. This distribution pattern suggests potential operational strategies that may consider factors such as runway/pad strength requirements, noise profiles, or maintenance capabilities at each facility.

Methodologically, this research employed a multi-stage analytical approach beginning with data validation and cleaning, followed by feature engineering to extract numerical values from textual data fields containing mixed units. The core analytical phase involved joining aircraft specifications with airport assignment records through a carefully validated merge operation using Aircraft_ID as the primary key. Subsequent stages included comprehensive statistical analysis, visualization generation, and operational metric development. The technical implementation utilized Python's scientific computing stack, including pandas for data manipulation (version 1.5.3), numpy for numerical computations (version 1.23.5), and matplotlib/seaborn for visualization (versions 3.6.2 and 0.12.1 respectively), as documented in the analysis_environment.json file.

From a physics perspective, disk loading serves as a fundamental determinant of 


---

## How to Run

### Local Execution
```bash
# Install dependencies
pip install pandas openpyxl

# Run each step sequentially
cd case_4822_11900
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
