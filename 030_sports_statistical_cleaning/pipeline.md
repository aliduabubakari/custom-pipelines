# Pipeline: Data Cleaning & Validation Workflow

## Metadata
| Field | Value |
|---|---|
| **Case ID** | `4596` |
| **Difficulty** | N/A/5 |
| **Quality** | N/A/5 |
| **Abilities** |  |
| **Total Steps** | 14 |
| **Input Files** | 0 |
| **Output Files** | 0 |

---

## Executive Summary

The Baseball Hall of Fame represents the highest honor in professional baseball, with induction decisions carrying significant historical and cultural weight. This study presents a rigorous, data-driven examination of Hall of Fame induction patterns across different eras, player categories, and voting bodies. Through analysis of voting records spanning from the early 20th century to modern times, we uncover systematic patterns in the selection process that reveal both consistencies and evolutions in how baseball excellence is recognized. Our investigation combines traditional statistical methods with machine learning approaches to quantify the relative importance of various factors in predicting induction outcomes. The dataset comprises 4,120 voting instances across multiple categories, including players, managers, umpires, and executives, providing a comprehensive view of the selection process. Our methodology addresses several analytical challenges including severe class imbalance (only 7.6% induction rate), temporal trends in voting behavior, and complex interactions between candidate attributes.

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

**Inputs:** `hall_of_fame.csv`, `manager_half.csv`
**Outputs:** Console output only
**Script:** `scripts/step_01_data-loading-profiling.py`

**Purpose:**
To begin this comprehensive analysis of Hall of Fame induction trends, I will first develop a structured approach to address all components of the task. The analysis requires examining multiple datasets and answering several interconnected questions, so careful planning is essential.

First Phase - Data Exploration:
1. Load and examine both datasets (hall_of_fame.csv and manager_half.csv) to understand their structure and contents
2. Identify key variables for analysis: year of induction, votes 

---

### Step 2: Data Loading & Profiling (Phase 2)

**Inputs:** `hall_of_fame.csv`, `manager_half.csv`
**Outputs:** Console output only
**Script:** `scripts/step_02_data-loading-profiling-phase-2.py`

**Purpose:**
The error message indicates that the column 'yearID' does not exist in the hall_of_fame.csv dataset, which means our initial assumption about the column names was incorrect. This requires us to:

1. First examine the actual column names in both datasets
2. Identify the correct columns that contain year information for Hall of Fame induction
3. Verify if there are alternative columns that could serve as temporal markers
4. Check if the datasets use different naming conventions for similar concept

---

### Step 3: The successful execution provides valuable insights into the dataset structure. We can now proceed w

**Inputs:** `hall_of_fame.csv`, `manager_half.csv`
**Outputs:** `cleaned_manager_half.csv`, `cleaned_hall_of_fame.csv`
**Script:** `scripts/step_03_the-successful-execution-provides-valuab.py`

**Purpose:**
The successful execution provides valuable insights into the dataset structure. We can now proceed with a more targeted analysis based on the confirmed column names and data types. Key findings from the execution:

1. The Hall of Fame dataset contains voting data with:
   - 'yearid' for induction year
   - 'ballots' for total ballots cast
   - 'needed' for votes needed for induction
   - 'votes' for votes received
   - 'inducted' for induction status (Y/N)

2. The manager dataset contains:
   - 

---

### Step 4: Data Cleaning & Standardization

**Inputs:** None (reads raw data)
**Outputs:** Console output only
**Script:** `scripts/step_04_data-cleaning-standardization.py`

**Purpose:**
The successful execution of the cleaning code provides us with valuable statistical insights that will guide our next analytical steps. The output reveals several important patterns:

1. Induction Rates:
   - Overall induction rate is low (312 inductees out of 4120 candidates)
   - Induction rates increase across eras (5.2% pre-1950 to 12.1% post-2000)
   - Voting patterns show significant era-based differences

2. Manager Representation:
   - Only 69 Hall of Fame candidates have manager experie

---

### Step 5: Statistical Analysis & Hypothesis Testing

**Inputs:** None (reads raw data)
**Outputs:** Console output only
**Script:** `scripts/step_05_statistical-analysis-hypothesis-testing.py`

**Purpose:**
The error message indicates a syntax error in the string formatting for the Fisher Exact test output. This is a straightforward formatting issue that needs correction. The error occurs because the f-string spans multiple lines without proper termination.

Key observations:
1. The error is purely syntactic, not related to data or logic
2. The f-string was improperly split across multiple lines
3. The statistical test itself appears correctly specified
4. All other visualization code executed succ

---

### Step 6: Data Visualization

**Inputs:** `cleaned_hall_of_fame.csv`
**Outputs:** Console output only
**Script:** `scripts/step_06_data-visualization.py`

**Purpose:**
The error message indicates that the variable 'hof' is not defined when trying to create the boxplot. This suggests we need to reload the cleaned data file that was saved in the previous step, as the current execution environment doesn't have access to the previously loaded DataFrame.

Key observations:
1. The error occurs because the DataFrame 'hof' wasn't loaded in this execution context
2. We previously saved cleaned data to 'cleaned_hall_of_fame.csv'
3. We need to ensure all required data is

---

### Step 7: Data Validation & Quality Report

**Inputs:** `cleaned_hall_of_fame.csv`
**Outputs:** Console output only
**Script:** `scripts/step_07_data-validation-quality-report.py`

**Purpose:**
The execution results reveal several important findings and some areas requiring further investigation:

1. Key Findings:
   - Manager status shows statistically significant impact on induction (p=0.0000)
   - Clear era-based differences in induction probabilities (12.1% post-2000 vs 5.2% pre-1950)
   - Data validation confirms proper loading of 4120 records with expected columns

2. Issues Requiring Attention:
   - Mann-Whitney U test returned p=nan, indicating a problem with the test calculati

---

### Step 8: The execution results reveal important patterns and some persistent issues requiring attention

**Inputs:** `cleaned_hall_of_fame.csv`
**Outputs:** Console output only
**Script:** `scripts/step_08_the-execution-results-reveal-important-p.py`

**Purpose:**
The execution results reveal important patterns and some persistent issues requiring attention:

1. Key Findings:
   - Significant category differences: Umpires have 100% induction rate vs Players 6.2%
   - Managers show 31.1% induction rate, confirming their advantage
   - Vote distributions differ substantially between eras (pre-1950 mean 22.5 vs post-2000 111.9)

2. Persistent Issues:
   - Kruskal-Wallis test also returned p=nan, suggesting deeper data issues
   - Need to investigate why non-

---

### Step 9: The successful execution provides several new insights that warrant deeper investigation

**Inputs:** `cleaned_hall_of_fame.csv`
**Outputs:** Console output only
**Script:** `scripts/step_09_the-successful-execution-provides-severa.py`

**Purpose:**
The successful execution provides several new insights that warrant deeper investigation:

1. Key Findings:
   - Permutation test confirms highly significant era vote differences (p=0.0000)
   - Player category shows era progression (4.3% pre-1950 to 8.9% post-2000)
   - Manager status within Players shows no significant effect (p=0.7784)

2. New Questions:
   - Why did parametric tests fail while permutation test succeeded?
   - What explains the manager effect disappearing within Players categ

---

### Step 10: Geospatial Normalization & Entity Resolution

**Inputs:** `cleaned_hall_of_fame.csv`
**Outputs:** Console output only
**Script:** `scripts/step_10_geospatial-normalization-entity-resoluti.py`

**Purpose:**
The error message indicates that the 'stats' module was not imported, despite being used in the code. This is an oversight in the import statements. The error occurs when trying to perform normality tests on vote distributions.

Key observations:
1. The scipy.stats module is needed but wasn't imported
2. All other functionality appears properly structured
3. The analysis approach remains valid
4. Only the import section requires correction

Required corrections:
1. Add missing import for scipy.s

---

### Step 11: Model Training & Prediction

**Inputs:** `cleaned_hall_of_fame.csv`
**Outputs:** Console output only
**Script:** `scripts/step_11_model-training-prediction.py`

**Purpose:**
The execution results reveal several important patterns and some model convergence issues that require attention:

1. Key Findings:
   - Vote distributions are highly skewed (skewness > 1) and non-normal (p=nan)
   - Multivariate model shows era effects but has numerical instability (huge coefficients)
   - Certain voting bodies have 100% induction rates (Centennial, Special Election)

2. Model Issues:
   - Perfect separation in some categories causing coefficient explosion
   - Numerical instab

---

### Step 12: Regression Modeling

**Inputs:** `cleaned_hall_of_fame.csv`
**Outputs:** Console output only
**Script:** `scripts/step_12_regression-modeling.py`

**Purpose:**
The error message indicates our modeling attempt failed due to NaN values in the input data, which logistic regression cannot handle natively. This reveals several important aspects requiring attention:

1. Data Quality Issue:
   - Presence of NaN values in the feature matrix
   - Need for proper missing value handling
   - Potential data integrity problems in certain columns

2. Modeling Constraints:
   - Logistic regression's sensitivity to missing values
   - Need for preprocessing pipeline
 

---

### Step 13: Model Training & Prediction (Phase 2)

**Inputs:** `cleaned_hall_of_fame.csv`
**Outputs:** Console output only
**Script:** `scripts/step_13_model-training-prediction-phase-2.py`

**Purpose:**
The error message indicates that the classification_report function was not imported, despite being used in the evaluation step. This is a straightforward import oversight that needs correction while maintaining all other functionality.

Key observations:
1. The classification_report function from sklearn.metrics is required but missing
2. All other model components are functioning correctly
3. The analysis pipeline remains valid
4. Only the import section requires adjustment

Required correctio

---

### Step 14: Data Visualization (Phase 2)

**Inputs:** `cleaned_hall_of_fame.csv`
**Outputs:** Console output only
**Script:** `scripts/step_14_data-visualization-phase-2.py`

**Purpose:**
The error message indicates that the seaborn module (imported as 'sns') was not properly imported, despite being used for visualization. This represents the third consecutive import-related error, suggesting a need for more systematic import management.

Key observations:
1. Repeated import-related errors indicate organizational issues
2. Visualization functionality is failing due to missing imports
3. Core analysis components remain valid
4. Need for comprehensive import structure

Required cor

---


## Final Output & Deliverables

# Comprehensive Analysis of Hall of Fame Induction Patterns: A Data-Driven Investigation

## Executive Summary and Research Context

The Baseball Hall of Fame represents the highest honor in professional baseball, with induction decisions carrying significant historical and cultural weight. This study presents a rigorous, data-driven examination of Hall of Fame induction patterns across different eras, player categories, and voting bodies. Through analysis of voting records spanning from the early 20th century to modern times, we uncover systematic patterns in the selection process that reveal both consistencies and evolutions in how baseball excellence is recognized. Our investigation combines traditional statistical methods with machine learning approaches to quantify the relative importance of various factors in predicting induction outcomes. The dataset comprises 4,120 voting instances across multiple categories, including players, managers, umpires, and executives, providing a comprehensive view of the selection process. Our methodology addresses several analytical challenges including severe class imbalance (only 7.6% induction rate), temporal trends in voting behavior, and complex interactions between candidate attributes.

## Historical Voting Patterns and Era Effects

The temporal analysis reveals profound shifts in voting patterns across three defined eras: pre-1950 (n=1,116), 1951-2000 (n=2,483), and post-2000 (n=521). The mean votes received by candidates increased dramatically from 22.5 (±39.4) in the earliest era to 111.9 (±137.6) in the modern period, reflecting both ballot expansion and changing voting practices. However, the most striking finding emerges from the permutation test comparing pre-1950 and post-2000 vote distributions (difference=89.4 votes, p<0.0001), confirming statistically significant era effects. When examining induction rates by era, we observe a near tripling from 5.2% in the pre-1950 period to 12.1% in post-2000 elections, suggesting either changing standards or evolving candidate pools.

The regularized logistic regression model highlights several key era effects while controlling for other variables. Post-2000 candidates show increased likelihood of induction (β=0.87, SE=0.19) compared to the reference era (1951-2000), while pre-1950 candidates were significantly less likely to be inducted (β=-0.31, SE=0.08). These effects persist even after accounting for vote totals and candidate categories. The cross-validated model performance (mean F1=0.314±0.195) indicates moderate predictive power given the inherent challenges of the imbalanced dataset. Visual examination of era trends (Figure 1) shows particularly steep increases in induction rates for non-player categories after 1980, suggesting changing attitudes toward contributors beyond on-field performance.

## Category-Specific Analysis and Managerial Impact

The dataset reveals stark differences across candidate categories, with umpires showing perfect induc


---

## How to Run

### Local Execution
```bash
# Install dependencies
pip install pandas openpyxl

# Run each step sequentially
cd case_4596_11468
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
