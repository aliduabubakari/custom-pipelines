# Pipeline: Data Cleaning & Validation Workflow

## Metadata
| Field | Value |
|---|---|
| **Case ID** | `5284` |
| **Difficulty** | N/A/5 |
| **Quality** | N/A/5 |
| **Abilities** |  |
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

### Step 1: Data Loading & Profiling

**Inputs:** None (reads raw data)
**Outputs:** Console output only
**Script:** `scripts/step_01_data-loading-profiling.py`

**Purpose:**
To begin this comprehensive analysis of baseball player data from the all_star.csv and fielding.csv files, I will first establish a structured approach to understand and analyze these datasets. The analysis will proceed through multiple phases:

1. Initial Data Inspection:
   - Load both CSV files into pandas DataFrames
   - Examine basic structure (shape, columns, dtypes)
   - Check for missing values and data quality issues
   - Generate summary statistics for numerical columns
   - Analyze ca

---

### Step 2: Data Loading & Profiling (Phase 2)

**Inputs:** None (reads raw data)
**Outputs:** `all_star_clean.csv`, `fielding_clean.csv`
**Script:** `scripts/step_02_data-loading-profiling-phase-2.py`

**Purpose:**
Based on the initial understanding, the following deeper analyses are warranted:

1. Data Cleaning and Preparation:
   - Develop imputation strategy for missing values
   - Handle inconsistent league_id in fielding data
   - Standardize position representations between datasets

2. Temporal Analysis:
   - Examine all-star selection trends over decades
   - Compare fielding metrics across different eras
   - Identify changes in defensive position importance

3. Player Performance Analysis:
   - C

---

### Step 3: Data Validation & Quality Report

**Inputs:** None (reads raw data)
**Outputs:** `all_star_clean.csv`, `fielding_clean.csv`
**Script:** `scripts/step_03_data-validation-quality-report.py`

**Purpose:**
To resolve this issue and improve the code structure:

1. Need to modify the initial inspection function to:
   - Return the loaded DataFrame
   - Store returned DataFrames in global variables
   - Maintain all previous functionality

2. Should implement better error handling:
   - Check if files exist before loading
   - Validate DataFrame creation
   - Provide meaningful error messages

3. Consider adding data validation steps:
   - Check for required columns
   - Verify data types
   - Ensure

---

### Step 4: resolve this issue, we need to

**Inputs:** None (reads raw data)
**Outputs:** `all_star_clean.csv`, `fielding_clean.csv`
**Script:** `scripts/step_04_resolve-this-issue-we-need-to.py`

**Purpose:**
To resolve this issue, we need to:

1. Remove the markdown code block syntax from the executable code
2. Ensure the pure Python code is passed to the execution environment
3. Maintain all functionality while presenting it in executable form
4. Keep the code well-structured and commented for clarity

The solution involves:
- Removing the ```python and ``` markers
- Keeping all Python code intact
- Adding clear section comments to maintain organization
- Ensuring all imports and functions are prop

---

### Step 5: Model Training & Prediction

**Inputs:** None (reads raw data)
**Outputs:** Console output only
**Script:** `scripts/step_05_model-training-prediction.py`

**Purpose:**
To deepen our analysis, we should now:

1. Investigate Position-Specific Trends:
   - Compare fielding metrics by specific positions (SS vs 2B, CF vs RF)
   - Analyze how position specialization affects all-star selection

2. Player Career Analysis:
   - Track individual player trajectories to all-star status
   - Compare pre-all-star vs post-all-star performance
   - Identify common development patterns

3. Advanced Statistical Modeling:
   - Build predictive models for all-star selection
   - 

---

### Step 6: Data Visualization

**Inputs:** None (reads raw data)
**Outputs:** Console output only
**Script:** `scripts/step_06_data-visualization.py`

**Purpose:**
To resolve this issue while maintaining our visualization goals:

1. First check available matplotlib styles
2. Use either:
   - A similar built-in style ('ggplot', 'fivethirtyeight')
   - Direct seaborn styling without relying on matplotlib styles
3. Ensure all visualization code remains functional
4. Maintain the same aesthetic quality in plots

The solution involves:
- Removing the problematic style specification
- Using seaborn's default styling
- Adding style verification if needed
- Keepin

---

### Step 7: Data Visualization (Phase 2)

**Inputs:** `all_star_clean.csv`, `fielding_clean.csv`
**Outputs:** Console output only
**Script:** `scripts/step_07_data-visualization-phase-2.py`

**Purpose:**
To resolve this issue while maintaining analytical integrity:

1. Need to ensure data continuity between analysis steps
2. Two potential approaches:
   - Load cleaned data from saved CSV files
   - Combine all analysis into a single continuous workflow
3. Should add data validation checks before analysis
4. Need to maintain all existing analytical functionality

The solution will:
- Load cleaned data from files at start of analysis
- Verify data loading success
- Proceed with all planned visuali

---

### Step 8: Regression Modeling

**Inputs:** None (reads raw data)
**Outputs:** Console output only
**Script:** `scripts/step_08_regression-modeling.py`

**Purpose:**
To deepen our analysis, we should now:

1. Investigate Advanced Metrics:
   - Calculate defensive efficiency ratios
   - Analyze putout/assist distributions by position
   - Examine error rates relative to opportunities

2. Temporal Performance Shifts:
   - Compare modern vs historical defensive metrics
   - Analyze how position demands have evolved
   - Identify era-specific performance benchmarks

3. Predictive Modeling:
   - Build logistic regression for all-star prediction
   - Identify most

---

### Step 9: Data Cleaning & Standardization

**Inputs:** `fielding_clean.csv`
**Outputs:** Console output only
**Script:** `scripts/step_09_data-cleaning-standardization.py`

**Purpose:**
To resolve this issue while maintaining analytical integrity:

1. Need to ensure data continuity between analysis steps
2. Two potential approaches:
   - Load cleaned data from saved CSV files at the start of each analysis block
   - Combine all analysis into a single continuous workflow
3. Should add data validation checks before analysis
4. Need to maintain all existing analytical functionality

The solution will:
- Load cleaned data from files at start of analysis
- Verify data loading succes

---

### Step 10: Regression Modeling (Phase 2)

**Inputs:** None (reads raw data)
**Outputs:** Console output only
**Script:** `scripts/step_10_regression-modeling-phase-2.py`

**Purpose:**
To further enhance our analysis, we should:

1. Improve Model Interpretation:
   - Address NaN values in regression output
   - Calculate odds ratios for significant predictors
   - Evaluate model performance metrics (AUC, precision/recall)

2. Deepen Position Analysis:
   - Compare elite vs average performers within positions
   - Analyze how defensive specialization has evolved
   - Examine platoon splits (LHP/RHP) where available

3. Additional Visualizations:
   - Plot odds ratios with confi

---

### Step 11: Data Cleaning & Standardization (Phase 2)

**Inputs:** `fielding_clean.csv`
**Outputs:** Console output only
**Script:** `scripts/step_11_data-cleaning-standardization-phase-2.py`

**Purpose:**
To resolve this issue while maintaining analytical integrity:

1. Need to ensure data continuity between analysis steps
2. Two potential approaches:
   - Reconstruct analysis_data from fielding_clean
   - Combine all analysis into a single continuous workflow
3. Should add data validation checks before analysis
4. Need to maintain all existing analytical functionality

The solution will:
- Reload or recreate analysis_data from source
- Verify data quality before proceeding
- Maintain all planned

---

### Step 12: Data Visualization (Phase 3)

**Inputs:** `fielding_clean.csv`
**Outputs:** Console output only
**Script:** `scripts/step_12_data-visualization-phase-3.py`

**Purpose:**
To resolve this issue while maintaining analytical rigor:

1. Need to recalculate all derived metrics during data loading
2. Should implement more robust data persistence:
   - Save all calculated metrics to CSV
   - Include data validation checks
3. Must ensure all analysis steps remain reproducible
4. Should maintain the analytical pipeline's integrity

The solution will:
- Recalculate defensive efficiency and assist ratio
- Add comprehensive data validation
- Preserve all modeling and visuali

---

### Step 13: Data Visualization (Phase 4)

**Inputs:** None (reads raw data)
**Outputs:** `final_analysis_data.csv`
**Script:** `scripts/step_13_data-visualization-phase-4.py`

**Purpose:**
To resolve this visualization issue while maintaining analytical integrity:

1. Need to properly format error bar data for matplotlib
2. Should maintain all statistical calculations
3. Must preserve the visualization's informational value
4. Need to ensure the plot accurately represents confidence intervals

The solution will:
- Reformat error bar data to required shape
- Keep all statistical calculations unchanged
- Maintain visualization quality and accuracy
- Add proper error handling

---

### Step 14: Data Visualization (Phase 5)

**Inputs:** None (reads raw data)
**Outputs:** `final_analysis_data.csv`
**Script:** `scripts/step_14_data-visualization-phase-5.py`

**Purpose:**
To resolve this issue while maintaining all analytical functionality:

1. Need to ensure all required imports are properly included
2. Should maintain the visualization quality and accuracy
3. Must preserve all statistical calculations and outputs
4. Need to verify all dependencies are available

The solution will:
- Add all necessary import statements
- Keep all visualization and analysis code
- Maintain the same output quality
- Include proper error handling

---

### Step 15: Data Visualization (Phase 6)

**Inputs:** `fielding_clean.csv`
**Outputs:** `final_analysis_data.csv`
**Script:** `scripts/step_15_data-visualization-phase-6.py`

**Purpose:**
To resolve this issue while maintaining analytical rigor:

1. Need to ensure all required data is available
2. Two potential approaches:
   - Recalculate odds_ratios from source data
   - Load previously calculated results
3. Should maintain all statistical validity
4. Must preserve visualization quality

The solution will:
- Recreate the odds_ratios calculation
- Include all necessary data preparation
- Maintain all statistical methods
- Keep visualization quality

---


## Final Output & Deliverables

# Comprehensive Analysis of Baseball Player Performance and All-Star Selection Patterns

## Introduction and Research Context

The analysis of baseball player performance data provides valuable insights into the relationship between defensive metrics and All-Star selection. This study examines two primary datasets: all_star.csv containing All-Star game participation records from 1933 to 2015, and fielding.csv with detailed defensive statistics spanning 1871 to 2015. The intersection of these datasets allows us to investigate how defensive performance correlates with All-Star recognition, while controlling for position-specific demands and temporal trends. Baseball analytics has evolved significantly since the sabermetrics revolution, yet the relationship between defensive excellence and All-Star selection remains understudied compared to offensive metrics. Our analysis bridges this gap by systematically examining defensive metrics across positions and eras, while developing predictive models for All-Star selection. The comprehensive nature of this dataset, covering over 18,000 players and 170,000 defensive seasons, provides robust statistical power for our analyses. We employ advanced statistical techniques including logistic regression and era-stratified analysis to uncover nuanced patterns in the data that might not be apparent through traditional scouting methods alone.

The historical context of baseball's evolution is crucial for interpreting these results. The game has undergone significant changes in defensive strategies, equipment quality, and positional specialization over the 144-year span of our data. For example, the introduction of gloves in the late 19th century and their subsequent technological improvements dramatically impacted fielding percentages. Similarly, the dead-ball era (pre-1920) placed different defensive demands on players compared to the modern power-hitting era. Our analysis accounts for these historical developments through era-based segmentation and position-specific metrics. The All-Star game itself, initiated in 1933, has also evolved in its selection processes and cultural significance, which we control for in our temporal analyses. By examining both the fielding statistics and All-Star selections, we can identify which defensive skills have been consistently valued versus those that have fluctuated in importance over time.

Methodologically, this study combines traditional baseball statistics with modern data science techniques. We calculate both conventional metrics like fielding percentage (FPCT) and range factor (RF), along with more sophisticated measures including defensive efficiency (DE) and assist ratio (AR). These metrics are then analyzed through multiple lenses: by position, by era, and through predictive modeling. The logistic regression approach allows us to quantify the relative importance of different defensive skills while controlling for playing time (games played). Our visualizations reveal tr


---

## How to Run

### Local Execution
```bash
# Install dependencies
pip install pandas openpyxl

# Run each step sequentially
cd case_5284_12990
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
