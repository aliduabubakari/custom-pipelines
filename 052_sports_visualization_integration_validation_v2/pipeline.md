# Pipeline: Data Cleaning & Validation Workflow

## Metadata
| Field | Value |
|---|---|
| **Case ID** | `5328` |
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
This task requires calculating the average max disk loading of aircraft associated with airports with Airport_ID 1 or 2. To accomplish this, we need to:

1. First understand the structure and content of both datasets:
   - aircraft.csv: Likely contains aircraft specifications including max disk loading
   - airport_aircraft.csv: Likely contains mapping between airports and aircraft

2. The analytical steps required are:
   - Load and inspect both datasets to understand their structure
   - Ident

---

### Step 2: Data Merging & Integration

**Inputs:** `airport_aircraft.csv`, `aircraft.csv`
**Outputs:** Console output only
**Script:** `scripts/step_02_data-merging-integration.py`

**Purpose:**
Based on our understanding, we need to implement the following processing steps:

1. Data Extraction:
   - Create a function to parse the Max_disk_Loading strings
   - Extract the numerical value before "lb/ft²"
   - Convert these values to float type for calculations

2. Data Filtering:
   - Filter airport_aircraft_df for Airport_ID 1 or 2
   - This should yield exactly 2 records based on the distribution

3. Data Joining:
   - Perform an inner join between filtered airport data and aircraft da

---

### Step 3: Data Visualization

**Inputs:** `airport_aircraft.csv`, `aircraft.csv`
**Outputs:** `processed_aircraft_data.csv`
**Script:** `scripts/step_03_data-visualization.py`

**Purpose:**
To provide a more comprehensive analysis, we should implement these additional steps:

1. Comparative Analysis:
   - Calculate average disk loading for all aircraft
   - Compare our subset average to the fleet-wide average
   - Analyze the percentage difference between them

2. Visualization:
   - Create a bar chart showing disk loading by aircraft type
   - Generate a scatter plot of weight vs. disk loading
   - Visualize the airport-aircraft distribution

3. Statistical Summary:
   - Compute d

---

### Step 4: Data Validation & Quality Report

**Inputs:** `airport_aircraft.csv`, `aircraft.csv`
**Outputs:** `processed_aircraft_data.csv`
**Script:** `scripts/step_04_data-validation-quality-report.py`

**Purpose:**
To implement a robust solution, we should:

1. Immediate Fixes:
   - Add the missing re import
   - Maintain all existing functionality
   - Preserve the analytical workflow

2. Enhanced Reliability:
   - Add try-except blocks for string parsing
   - Validate string formats before processing
   - Implement fallback values for parsing failures

3. Code Organization:
   - Group all imports at the beginning
   - Add clear section comments
   - Maintain consistent style

4. Verification Steps:
   - 

---

### Step 5: Data Visualization (Phase 2)

**Inputs:** `processed_aircraft_data.csv`
**Outputs:** `enhanced_aircraft_analysis.csv`
**Script:** `scripts/step_05_data-visualization-phase-2.py`

**Purpose:**
To deepen our analysis, we should implement:

1. Advanced Statistical Analysis:
   - Shapiro-Wilk test for normality
   - Calculation of skewness and kurtosis
   - Confidence intervals for the means

2. Enhanced Visualizations:
   - Kernel density plots for disk loading distribution
   - Categorical coloring in scatter plots
   - Annotated extreme values in charts

3. Engineering Analysis:
   - Classification by disk loading ranges (light/medium/heavy)
   - Calculation of disk area to weight rat

---

### Step 6: Data Visualization (Phase 3)

**Inputs:** `enhanced_aircraft_analysis.csv`
**Outputs:** `final_aircraft_analysis.csv`
**Script:** `scripts/step_06_data-visualization-phase-3.py`

**Purpose:**
To produce a comprehensive final analysis, we should implement:

1. Multivariate Visualization:
   - Parallel coordinates plot linking all numerical features
   - Radar chart for normalized performance comparison
   - 3D scatter plot of weight, loading, and disk area

2. Statistical Enhancement:
   - Effect size calculation for category differences
   - Non-parametric tests given small sample size
   - Bootstrapped confidence intervals

3. Engineering Contextualization:
   - Add manufacturer per

---

### Step 7: Data Visualization (Phase 4)

**Inputs:** `enhanced_aircraft_analysis.csv`
**Outputs:** `final_aircraft_analysis.csv`
**Script:** `scripts/step_07_data-visualization-phase-4.py`

**Purpose:**
To implement a robust solution, we should:

1. Immediate Fixes:
   - Convert Loading_Class to explicit string type
   - Verify all column types before visualization
   - Maintain original numerical precision

2. Enhanced Data Validation:
   - Add pre-visualization type checking
   - Implement safe type conversion utilities
   - Preserve data integrity during transformations

3. Error Handling:
   - Add try-catch blocks for visualization steps
   - Implement fallback visualization options
   - Pr

---

### Step 8: Data Visualization (Phase 5)

**Inputs:** `enhanced_aircraft_analysis.csv`
**Outputs:** `final_aircraft_analysis.csv`
**Script:** `scripts/step_08_data-visualization-phase-5.py`

**Purpose:**
To resolve these issues, we should implement:

1. Comprehensive Data Preparation:
   - Create visualization-specific data frames
   - Explicitly select and type numeric features
   - Isolate categorical variables

2. Robust Visualization Pipeline:
   - Separate plotting code into functions
   - Add data validation checks
   - Implement graceful fallbacks

3. Statistical Validation:
   - Manual verification of effect size
   - Add confidence intervals
   - Consider alternative effect size measure

---

### Step 9: Data Visualization (Phase 6)

**Inputs:** `enhanced_aircraft_analysis.csv`
**Outputs:** `final_aircraft_analysis.csv`
**Script:** `scripts/step_09_data-visualization-phase-6.py`

**Purpose:**
To produce a polished final analysis, we should implement:

1. Warning Resolution:
   - Handle NaN values explicitly in radar chart
   - Implement safe normalization
   - Add validation checks

2. Enhanced Statistics:
   - Calculate Hedges' g for small sample bias correction
   - Add 95% confidence intervals
   - Include non-parametric alternatives

3. Visualization Improvements:
   - Add direct labels to data points
   - Implement logarithmic scaling where appropriate
   - Improve color contras

---

### Step 10: Data Visualization (Phase 7)

**Inputs:** `final_aircraft_analysis.csv`
**Outputs:** `performance_summary_stats.csv`
**Script:** `scripts/step_10_data-visualization-phase-7.py`

**Purpose:**
To finalize this analysis appropriately, we should:

1. Contextualize Statistical Results:
   - Replace quantitative effect sizes with qualitative descriptions
   - Focus on engineering meaning rather than statistical measures
   - Acknowledge small sample limitations

2. Visualization Finalization:
   - Keep current visualizations as they effectively show patterns
   - Add explanatory captions about the logarithmic scaling
   - Document the benign nature of the normalization warning

3. Reporti

---

### Step 11: Final Synthesis & Reporting

**Inputs:** `README.md`, `requirements.txt`
**Outputs:** `README.md`, `requirements.txt`
**Script:** `scripts/step_11_final-synthesis-reporting.py`

**Purpose:**
To properly conclude this analysis, we should implement these final steps:

1. Documentation:
   - Create comprehensive README documentation
   - Add code comments explaining key decisions
   - Document file dependencies and requirements

2. Reproducibility:
   - Generate requirements.txt for Python dependencies
   - Add session information (Python version, package versions)
   - Include sample execution instructions

3. Final Validation:
   - Verify all files can be opened and parsed
   - Check

---

### Step 12: Error Recovery & Robust Loading

**Inputs:** `README.md`, `requirements.txt`
**Outputs:** `README.md`, `requirements.txt`
**Script:** `scripts/step_12_error-recovery-robust-loading.py`

**Purpose:**
The error encountered reveals a final oversight in our comprehensive analysis workflow:

1. Root Cause Analysis:
   - The NameError indicates numpy was referenced but not imported
   - Occurred during requirements.txt generation
   - Despite extensive previous analysis, this basic dependency was missed

2. Impact Assessment:
   - Prevents complete documentation generation
   - Does not affect core analytical results
   - Highlights need for final import verification

3. Solution Requirements:
  

---

### Step 13: Data Visualization (Phase 8)

**Inputs:** `README.md`, `requirements.txt`
**Outputs:** `README.md`, `requirements.txt`
**Script:** `scripts/step_13_data-visualization-phase-8.py`

**Purpose:**
The error reveals another critical oversight in our finalization process:

1. Root Cause Analysis:
   - The AttributeError indicates matplotlib.pyplot lacks __version__ attribute
   - This is a known characteristic of pyplot's structure
   - Version information needs to be accessed through matplotlib.__version__ instead

2. Impact Assessment:
   - Prevents complete requirements file generation
   - Does not affect core analysis or visualizations
   - Highlights need for precise package version h

---


## Final Output & Deliverables

# Comprehensive Analysis of Aircraft Disk Loading Characteristics

## Introduction and Research Background

The study of aircraft disk loading characteristics represents a critical intersection of aerospace engineering and performance optimization. Disk loading, defined as the ratio of an aircraft's weight to the total area of its rotor disk, serves as a fundamental parameter influencing numerous aspects of helicopter performance including lift capacity, power requirements, and operational efficiency. This comprehensive analysis examines disk loading patterns across five distinct helicopter models, revealing significant variations that correlate strongly with aircraft classification and intended operational use. The dataset under investigation comprises detailed specifications for aircraft ranging from light utility helicopters to heavy-lift transport models, providing a unique opportunity to examine performance characteristics across multiple weight classes. 

Modern rotorcraft design increasingly relies on precise disk loading optimization to balance competing requirements of payload capacity, fuel efficiency, and maneuverability. The numerical results obtained in this study demonstrate clear stratification of disk loading values corresponding to three operational categories: light utility (2.6-3.7 lb/ft²), medium (8.8 lb/ft²), and heavy-lift (14.5-15.0 lb/ft²) helicopters. These findings align with established aerospace engineering principles while providing specific quantitative benchmarks for contemporary aircraft models. The statistical analysis reveals remarkably consistent within-class disk loading values, with standard deviations of just 0.78 lb/ft² for light helicopters and 0.35 lb/ft² for heavy-lift models, suggesting manufacturers adhere closely to optimal loading ranges for each operational category.

Methodologically, this investigation employed a multi-phase analytical approach beginning with data acquisition and validation, progressing through statistical characterization, and culminating in comprehensive visualization and interpretation. The analytical workflow incorporated rigorous quality control measures, including unit consistency verification, missing data checks, and outlier detection protocols. Particular attention was devoted to the accurate extraction of numerical values from composite measurement strings (e.g., "2.6 lb/ft² (14 kg/m²)"), ensuring the reliability of subsequent calculations. The research methodology produced several key artifacts including the performance summary statistics table (performance_summary_stats.csv) and the comparative visualization (final_performance_comparison.png), which together provide both granular numerical data and intuitive graphical representation of the findings.

From an engineering perspective, the disk loading values observed in this study carry significant implications for aircraft design and operation. The light utility helicopters (Robinson R-22 and Bell 206B3 JetRanger) exhibi


---

## How to Run

### Local Execution
```bash
# Install dependencies
pip install pandas openpyxl

# Run each step sequentially
cd case_5328_13047
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
