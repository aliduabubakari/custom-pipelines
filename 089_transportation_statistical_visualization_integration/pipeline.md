# Pipeline: Data Cleaning & Validation Workflow

## Metadata
| Field | Value |
|---|---|
| **Case ID** | `4780` |
| **Difficulty** | N/A/5 |
| **Quality** | N/A/5 |
| **Abilities** |  |
| **Total Steps** | 14 |
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

### Step 1: Data Loading & Profiling: Data Inspection & Joining Strategy

**Inputs:** `data_inspection_report.txt`, `all_star.csv`, `batting_postseason.csv`
**Outputs:** `data_inspection_report.txt`
**Script:** `scripts/step_01_data-loading-profiling-data-inspection-j.py`

**Purpose:**
To begin this comprehensive analysis of MLB postseason batting performance comparing All-Stars vs. non-All-Stars, I'll develop a multi-phase analytical approach:

1. **Data Inspection & Joining Strategy**
   - First need to examine both datasets' structure (columns, data types, completeness)
   - Must verify join keys (player_id and year) exist in both datasets
   - Need to confirm temporal alignment between All-Star selections and postseason appearances

2. **Data Preparation Pipeline**
   - Cr

---

### Step 2: Data Merging & Integration

**Inputs:** None (reads raw data)
**Outputs:** `summary_statistics.csv`, `processed_postseason_data.csv`, `statistical_tests.csv`
**Script:** `scripts/step_02_data-merging-integration.py`

**Purpose:**
Based on the initial understanding, the next steps should focus on:

1. **Data Filtering and Preparation**:
   - Restrict analysis to 2000-2015 as specified in requirements
   - Create clean merged dataset with proper All-Star flagging
   - Calculate per-game metrics while handling zero-game appearances

2. **Data Quality Enhancement**:
   - Handle missing league_id values
   - Verify consistency of team_id across datasets
   - Address potential duplicate records (game_num in All-Star data)

3. 

---

### Step 3: Data Loading & Profiling: Data Loading Reliability

**Inputs:** `all_star.csv`, `batting_postseason.csv`
**Outputs:** `summary_statistics.csv`, `processed_postseason_data.csv`
**Script:** `scripts/step_03_data-loading-profiling-data-loading-reli.py`

**Purpose:**
To resolve this issue and ensure robust execution:

1. **Data Loading Reliability**:
   - Need to reload both datasets at start of new execution
   - Should verify successful loading before proceeding
   - Must maintain consistent variable naming

2. **Error Prevention**:
   - Add existence checks for input files
   - Include verbose logging of loading process
   - Implement defensive programming practices

3. **Code Structure Improvements**:
   - Create self-contained executable block
   - Ensu

---

### Step 4: Statistical Analysis & Hypothesis Testing

**Inputs:** `processed_postseason_data.csv`
**Outputs:** `statistical_results.csv`, `yearly_trends.csv`
**Script:** `scripts/step_04_statistical-analysis-hypothesis-testing.py`

**Purpose:**
The results warrant deeper investigation in these areas:

1. **Statistical Significance Testing**:
   - Need formal hypothesis tests for observed differences
   - Should calculate effect sizes (Cohen's d) for practical significance
   - Requires league-specific comparisons

2. **Temporal Trend Analysis**:
   - Year-by-year performance patterns
   - Potential changes in All-Star selection impact
   - League performance trajectories

3. **Advanced Visualization**:
   - Small multiples for league c

---

### Step 5: Data Visualization: Address Technical Warnings

**Inputs:** `processed_postseason_data.csv`
**Outputs:** `nl_enhanced_results.csv`, `al_enhanced_results.csv`
**Script:** `scripts/step_05_data-visualization-address-technical-war.py`

**Purpose:**
To further enhance the analysis, we should:

1. **Address Technical Warnings**:
   - Update seaborn plotting syntax
   - Ensure future compatibility

2. **Deepen Statistical Analysis**:
   - Add non-parametric tests (Mann-Whitney U)
   - Calculate confidence intervals for effect sizes
   - Perform power analysis

3. **Enrich Visualizations**:
   - Add significance annotations to plots
   - Include effect size benchmarks
   - Improve table formatting

4. **Advanced Modeling**:
   - Consider mixed

---

### Step 6: Data Visualization: Finalize Statistical Reporting

**Inputs:** `nl_enhanced_results.csv`, `al_enhanced_results.csv`, `mixed_model_results.txt`, `processed_postseason_data.csv`
**Outputs:** `mixed_model_results.txt`, `al_publication_table.csv`, `nl_publication_table.csv`
**Script:** `scripts/step_06_data-visualization-finalize-statistical-.py`

**Purpose:**
To complete the comprehensive analysis, we should:

1. **Finalize Statistical Reporting**:
   - Generate publication-quality tables
   - Calculate NNT (Number Needed to Treat) equivalents
   - Prepare results for multiple comparison adjustment

2. **Advanced Visualization**:
   - Small multiples for all metrics
   - Cumulative distribution plots
   - Raincloud plots for distribution comparison

3. **Contextual Analysis**:
   - Compare to regular season performance gaps
   - Examine round-specifi

---

### Step 7: Data Visualization: Visualization Adaptation

**Inputs:** `nl_enhanced_results.csv`, `al_enhanced_results.csv`, `mixed_model_results.txt`, `processed_postseason_data.csv`
**Outputs:** `mixed_model_results.txt`, `al_publication_table.csv`, `nl_publication_table.csv`
**Script:** `scripts/step_07_data-visualization-visualization-adaptat.py`

**Purpose:**
To maintain analysis continuity while addressing the dependency issue:

1. **Visualization Adaptation**:
   - Replace raincloud plot with combined violin/box/swarm plot
   - Use seaborn's native capabilities
   - Preserve the distribution comparison functionality

2. **Code Robustness**:
   - Implement graceful fallback for missing packages
   - Maintain all core analytical components
   - Ensure backward compatibility

3. **Output Preservation**:
   - Keep all statistical tables and model resul

---

### Step 8: Data Visualization: Data Structure Correction

**Inputs:** `nl_enhanced_results.csv`, `al_enhanced_results.csv`, `mixed_model_results.txt`, `processed_postseason_data.csv`
**Outputs:** `mixed_model_results.txt`, `al_publication_table.csv`, `nl_publication_table.csv`
**Script:** `scripts/step_08_data-visualization-data-structure-correc.py`

**Purpose:**
To resolve these issues while maintaining analytical integrity:

1. **Data Structure Correction**:
   - Need to reshape data for small multiples visualization
   - Create proper 'metric' column through melting
   - Ensure consistent variable naming

2. **Visualization Optimization**:
   - Replace swarmplot with jittered strip plot for dense data
   - Adjust marker size and transparency
   - Consider sampling for extremely dense distributions

3. **Error Prevention**:
   - Add data validation che

---

### Step 9: Model Training & Prediction

**Inputs:** `nl_enhanced_results.csv`, `al_enhanced_results.csv`, `mixed_model_results.txt`, `processed_postseason_data.csv`
**Outputs:** `mixed_model_results.txt`, `al_publication_table.csv`, `nl_publication_table.csv`
**Script:** `scripts/step_09_model-training-prediction.py`

**Purpose:**
To resolve this while maintaining analytical rigor:

1. **Data Type Correction**:
   - Convert player_id to categorical codes
   - Ensure numeric type for grouping variable
   - Verify all formula variables have proper dtypes

2. **Model Specification**:
   - Alternative random effects specification
   - Explicit type conversion before modeling
   - Additional data validation

3. **Implementation Strategy**:
   - Create numeric player codes
   - Maintain original player_id for reference
   - Add

---

### Step 10: Data Visualization: Model Improvement

**Inputs:** `final_report.txt`, `al_publication_table.csv`, `processed_postseason_data.csv`, `nl_publication_table.csv`
**Outputs:** `final_report.txt`
**Script:** `scripts/step_10_data-visualization-model-improvement.py`

**Purpose:**
To finalize the analysis, we should:

1. **Model Improvement**:
   - Address multicollinearity concerns
   - Consider robust standard errors
   - Explore interaction effects

2. **Diagnostic Visualization**:
   - Residual plots
   - QQ plots for normality
   - Influence metrics

3. **Final Reporting**:
   - Consolidate all results
   - Prepare interpretation narrative
   - Generate comprehensive visual summary

The final code will implement these refinements while preserving all key findings.

---

### Step 11: Final Synthesis & Reporting

**Inputs:** `final_report.txt`, `processed_postseason_data.csv`
**Outputs:** `final_report.txt`
**Script:** `scripts/step_11_final-synthesis-reporting.py`

**Purpose:**
To complete the analysis, we should:

1. **Final Interpretation**:
   - Synthesize statistical and practical significance
   - Contextualize within baseball research
   - Discuss limitations and future work

2. **Visual Storytelling**:
   - Create executive summary visualization
   - Highlight key comparisons
   - Show effect size benchmarks

3. **Robustness Checks**:
   - Quantile regression for non-normal outcomes
   - Bootstrapped confidence intervals
   - Sensitivity analyses

Final code wil

---

### Step 12: Data Preparation & Feature Engineering: Data Persistence Solution

**Inputs:** `final_report.txt`, `processed_postseason_data.csv`
**Outputs:** `final_report.txt`
**Script:** `scripts/step_12_data-preparation-feature-engineering-dat.py`

**Purpose:**
To resolve this while maintaining analytical integrity:

1. **Data Persistence Solution**:
   - Recreate the postseason_round mapping during data loading
   - Verify all required columns exist before analysis
   - Implement defensive column checking

2. **Process Improvement**:
   - Add data validation steps
   - Create persistent intermediate files with all features
   - Document data transformation pipeline

3. **Analysis Continuity**:
   - Maintain all previous findings
   - Ensure backward c

---

### Step 13: Revised Analysis & Refinement

**Inputs:** `final_report.txt`, `processed_postseason_data.csv`
**Outputs:** `final_report.txt`
**Script:** `scripts/step_13_revised-analysis-refinement.py`

**Purpose:**
To resolve this while maintaining report quality:

1. **String Formatting Solution**:
   - Separate table generation from f-string
   - Use consistent string formatting approach
   - Ensure proper brace closure

2. **Report Structure Enhancement**:
   - Maintain all statistical content
   - Improve table presentation
   - Ensure proper Markdown formatting

3. **Output Validation**:
   - Verify all numerical results
   - Check table alignment
   - Test file writing operation

The revised code wil

---

### Step 14: Regression Modeling

**Inputs:** `final_report.txt`, `processed_postseason_data.csv`
**Outputs:** `final_report.txt`
**Script:** `scripts/step_14_regression-modeling.py`

**Purpose:**
To resolve this while maintaining analytical integrity:

1. **Data Validation**:
   - Verify numeric types in quantile regression results
   - Handle failed regressions gracefully
   - Ensure proper DataFrame structure

2. **Visualization Robustness**:
   - Add numeric type checking before plotting
   - Implement fallback visualization options
   - Maintain all statistical results

3. **Process Improvement**:
   - Add intermediate data validation checks
   - Document data structure expectations


---


## Final Output & Deliverables

# Comprehensive Analysis of Postseason Batting Performance: All-Stars vs. Non-All-Stars (2000-2015)

## Introduction and Research Context

Major League Baseball's postseason represents the pinnacle of competitive play, where the game's elite performers face heightened scrutiny under pressure conditions. This study examines 15 seasons of postseason performance data (2000-2015) to quantify the differences between players selected as All-Stars in the same year versus their non-All-Star counterparts. The analysis focuses on three key batting metrics: hits per game (H/G), home runs per game (HR/G), and runs batted in per game (RBI/G), while controlling for league affiliation (American vs. National) and postseason round progression. The dataset comprises 4,708 postseason appearances from 1,153 unique players, creating a robust sample for evaluating performance differentials under postseason conditions.

Previous research has established that All-Star selections generally identify superior regular season performers, but few studies have systematically examined whether this advantage persists in postseason play. The postseason environment presents unique challenges including heightened competition, strategic pitching adjustments, and increased media scrutiny. Our analysis reveals that All-Stars maintain statistically significant performance advantages across all measured metrics, though the magnitude varies by league and specific offensive category. The American League shows particularly pronounced effects, with All-Stars demonstrating 57.4% greater hits per game compared to 67.7% in the National League, suggesting interesting league-specific dynamics.

Methodologically, this study employs multiple analytical approaches to ensure robust findings. We combine traditional descriptive statistics with advanced modeling techniques, including quantile regression (though limited by data constraints) and mixed effects modeling. The visualization strategy incorporates both distributional analysis and temporal trends, providing multiple perspectives on the performance gaps. All analyses were conducted using Python's scientific computing stack (pandas, statsmodels, seaborn) with rigorous data validation checks at each processing stage.

The practical implications of these findings extend beyond academic interest. Teams making postseason roster decisions must weigh regular season performance against potential postseason contributions. Our results suggest All-Star status provides meaningful predictive value for postseason batting performance, though the relationship varies by league and metric. These insights could inform managerial decisions regarding lineup construction and pinch-hitting strategies during critical postseason games.

## Data Preparation and Methodological Framework

The analytical pipeline began with comprehensive data preparation to ensure clean, analysis-ready datasets. The source data came from two primary tables: all_star.csv (1,153 records) and 


---

## How to Run

### Local Execution
```bash
# Install dependencies
pip install pandas openpyxl

# Run each step sequentially
cd case_4780_11892
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
