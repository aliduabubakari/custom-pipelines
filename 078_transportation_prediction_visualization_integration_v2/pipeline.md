# Pipeline: Data Cleaning & Validation Workflow

## Metadata
| Field | Value |
|---|---|
| **Case ID** | `9822` |
| **Difficulty** | 4/5 |
| **Quality** | 5/5 |
| **Abilities** | Data Preparation, Data Analysis, Data Visualization, Data Modeling, Data Insight, Code Generation, Reasoning, Numerical Calculation, Instruction Following, Structural Understanding |
| **Total Steps** | 9 |
| **Input Files** | 1 |
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

### Step 1: Geospatial Normalization & Entity Resolution

**Inputs:** `all_star.json`
**Outputs:** `all_star_parsed.csv`, `all_star.json`
**Script:** `scripts/step_01_geospatial-normalization-entity-resoluti.py`

**Purpose:**
The error indicates that the all_star.json file contains malformed JSON data that cannot be parsed normally. This suggests:

1. The JSON file might be:
   - A JSON Lines file (each line is a separate JSON object)
   - Contains multiple JSON objects concatenated without proper array structure
   - Has formatting issues or corrupted data

2. Next steps needed:
   - First try reading the file as JSON Lines format
   - If that fails, inspect the raw file content to understand its structure
   - Impl

---

### Step 2: Error Recovery & Robust Loading

**Inputs:** `pitching_postseason.csv`, `pitching_post_info.txt`
**Outputs:** `pitching_post_info.txt`
**Script:** `scripts/step_02_error-recovery-robust-loading.py`

**Purpose:**
The error occurred because the pandas import statement was not included in this code segment. This is a simple oversight that can be easily fixed. Here's what we need to do:

1. Error Analysis:
- The NameError indicates we tried to use pandas (pd) without importing it
- This happened because we're working in a new code block that doesn't inherit imports from previous blocks

2. Solution:
- Add the required pandas import at the beginning
- Re-run the same inspection code
- Ensure all future code 

---

### Step 3: Data Loading & Profiling

**Inputs:** `pitching_postseason.csv`, `all_star_parsed.csv`
**Outputs:** `merged_data.csv`
**Script:** `scripts/step_03_data-loading-profiling.py`

**Purpose:**
The pitching postseason data has been successfully loaded and inspected. Here's the comprehensive understanding:

1. Data Structure:
- 5,109 records of postseason pitching performances
- 30 columns covering player identification, year, round, team info, and detailed pitching stats
- Key metrics: W/L records, ERA, strikeouts (so), innings pitched (ipouts), etc.

2. Key Observations:
- Both player_id and year fields are complete (no missing values)
- Year range spans 1884-2015, matching well with 

---

### Step 4: Data Merging & Integration

**Inputs:** `merged_data.csv`, `feature_description.txt`
**Outputs:** `enhanced_data.csv`, `feature_description.txt`
**Script:** `scripts/step_04_data-merging-integration.py`

**Purpose:**
The merge operation was successful, yielding a dataset of 704 postseason appearances by 289 All-Star pitchers. Here's the detailed analysis:

1. Merge Results:
- Successfully joined 1,741 unique All-Star pitchers with postseason data
- Resulted in 704 records of All-Star pitchers' postseason performances
- Coverage from 1933-2015 matches historical All-Star game timeline

2. Data Characteristics:
- Each record represents a pitcher's performance in a specific postseason round
- Some pitchers appe

---

### Step 5: Geospatial Normalization & Entity Resolution (Phase 2)

**Inputs:** `enhanced_data.csv`, `pitching_postseason.csv`, `performance_analysis.txt`
**Outputs:** `performance_analysis.txt`
**Script:** `scripts/step_05_geospatial-normalization-entity-resoluti.py`

**Purpose:**
The feature engineering was successful, creating a rich dataset for analysis. Here's the current state:

1. Enhanced Data Features:
- Created 13 round flags (WS, ALCS, etc.)
- Added performance metrics normalized by outs (SO/out, BB/out)
- Established All-Star to postseason ratio (though limited by data scope)
- Handled missing values in key stats

2. Current Limitations:
- Postseason performance delta couldn't be fully implemented without regular season data
- Some ratios may need refinement (e

---

### Step 6: Data Visualization

**Inputs:** `enhanced_data.csv`, `pitching_postseason.csv`, `performance_analysis.txt`
**Outputs:** `performance_analysis.txt`
**Script:** `scripts/step_06_data-visualization.py`

**Purpose:**
The analysis revealed several important findings and issues that need addressing:

1. Key Results:
- All-Star pitchers show better performance (lower ERA, more strikeouts, more wins)
- Significant differences in SO (p<0.0001) and W (p<0.0001) between groups
- Visualization successfully created showing ERA distributions

2. Identified Issues:
- ERA comparison produced NaN values due to infinite values in non-All-Star group
- Runtime warnings during statistical calculations
- Need to clean data be

---

### Step 7: Data Validation & Quality Report

**Inputs:** `pitching_postseason.csv`, `model_preparation.pkl`, `all_star_parsed.csv`, `model_features.txt`
**Outputs:** `model_preparation.pkl`, `model_features.txt`
**Script:** `scripts/step_07_data-validation-quality-report.py`

**Purpose:**
The error occurred due to a missing numpy import, which is needed for handling infinite values. This is a straightforward fix. Here's the analysis:

1. Error Analysis:
- The code uses numpy's infinity constants (np.inf) without importing numpy
- This is a simple oversight in the imports section

2. Required Fixes:
- Add numpy import at the beginning
- The rest of the code logic remains valid
- All other functionality should work as intended

3. Impact Assessment:
- This won't affect the overall 

---

### Step 8: Model Training & Prediction

**Inputs:** `model_preparation.pkl`, `model_evaluation.txt`, `all_star_predictor.pkl`
**Outputs:** `model_preparation.pkl`, `model_evaluation.txt`, `all_star_predictor.pkl`
**Script:** `scripts/step_08_model-training-prediction.py`

**Purpose:**
The model preparation was successful, creating a balanced dataset ready for classification. Here's the detailed analysis:

1. Data Preparation Results:
- Final dataset contains 2,063 pitcher records (1,736 training after SMOTE, 327 test)
- 4 key features: ERA, SO/game, win percentage, postseason appearances
- Original class imbalance (33.6% All-Stars) was addressed with SMOTE oversampling

2. Key Characteristics:
- Training set now perfectly balanced (50/50)
- Test set maintains original distrib

---

### Step 9: Data Merging & Integration (Phase 2)

**Inputs:** `model_preparation.pkl`, `final_report.txt`, `all_star_predictor.pkl`
**Outputs:** `model_preparation.pkl`, `final_report.txt`, `all_star_predictor.pkl`
**Script:** `scripts/step_09_data-merging-integration-phase-2.py`

**Purpose:**
The model training and evaluation are complete, yielding important insights:

1. Model Performance Summary:
- Logistic Regression emerged as the best model (All-Star recall: 0.69)
- All models showed moderate performance, with LR achieving the best balance
- Confusion matrices reveal reasonable classification for both classes

2. Key Observations:
- Models perform better at identifying Non-All-Stars (higher precision/recall)
- All-Star identification remains challenging (best F1-score: 0.63)
- F

---


## Final Output & Deliverables

# Comprehensive Analysis of All-Star Pitchers' Postseason Performance

## Project Overview
This analysis examined the postseason performance of MLB All-Star pitchers by combining All-Star selection data with postseason pitching statistics. The project successfully:

1. Merged datasets from 1,741 unique pitchers across 1933-2015
2. Engineered key features like All-Star appearance ratios
3. Compared performance metrics between All-Star and non-All-Star pitchers
4. Developed a predictive model for All-Star selection

## Key Findings

### Performance Comparison
- **All-Star pitchers** showed better postseason performance:
  - Lower ERA (3.83 vs 4.10)
  - More strikeouts per game (5.54 vs 3.25)
  - Higher win percentage (0.43 vs 0.26)
- Differences were statistically significant for SO and W (p<0.0001)

### Predictive Modeling
- **Logistic Regression** performed best among tested models:
  - 69% recall for identifying All-Stars
  - 72% overall accuracy
  - Balanced precision-recall (AP=0.65)
- Most important features:
  1. Postseason appearances
  2. Strikeouts per game
  3. Win percentage
  4. ERA

## Deliverables Produced

### Data Files
1. `merged_data.csv` - Combined All-Star and postseason data
2. `enhanced_data.csv` - Dataset with engineered features
3. `model_preparation.pkl` - Processed modeling dataset

### Analysis Outputs
1. `performance_analysis.txt` - Statistical comparisons
2. `era_comparison.png` - Visual performance comparison
3. `final_report.txt` - Comprehensive model documentation

### Models
1. `all_star_predictor.pkl` - Trained classifier with preprocessing
2. `pr_curve.png` - Model performance visualization
3. `shap_summary.png` - Feature importance analysis

## Conclusion
This analysis provides valuable insights into how All-Star pitchers perform in postseason play and demonstrates the feasibility of predicting All-Star selections based on postseason performance. The deliverables offer a foundation for further exploration of pitcher performance analytics.

Future work could incorporate regular season statistics, expand to position players, or analyze temporal trends in performance characteristics.


---

## How to Run

### Local Execution
```bash
# Install dependencies
pip install pandas openpyxl

# Run each step sequentially
cd case_9822_21888
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
