# Pipeline: Data Cleaning & Validation Workflow

## Metadata
| Field | Value |
|---|---|
| **Case ID** | `4967` |
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

### Step 1: This task requires a comprehensive analysis comparing team game participation and player all-star ap

**Inputs:** `all_star.csv`, `team.csv`
**Outputs:** `allstar_2015_sample.csv`, `team_2015_sample.csv`
**Script:** `scripts/step_01_this-task-requires-a-comprehensive-analy.py`

**Purpose:**
This task requires a comprehensive analysis comparing team game participation and player all-star appearances in 2015. The approach should be methodical:

1. Data Exploration Phase:
- First need to understand both datasets' structure (columns, data types, completeness)
- Verify year 2015 data exists in both datasets
- Check for missing values and data quality issues

2. Data Preparation:
- Filter both datasets for year 2015 only
- For team data: extract team identifiers and games played ('g')
- 

---

### Step 2: properly handle this situation, we should

**Inputs:** `all_star.csv`, `team_columns.txt`, `allstar_columns.txt`, `team.csv`
**Outputs:** `team_columns.txt`, `allstar_columns.txt`
**Script:** `scripts/step_02_properly-handle-this-situation-we-should.py`

**Purpose:**
To properly handle this situation, we should:
1. First inspect all column names in both datasets
2. Identify potential year-related columns (could be 'year', 'season', 'YearID', etc.)
3. Verify which columns contain team identifiers
4. Check for case sensitivity issues in column names
5. Ensure the 'g' column exists for games played in team data
6. Confirm player-team association columns in all-star data

The next code will:
- Print all column names for both datasets
- Check for alternative year

---

### Step 3: Data Merging & Integration

**Inputs:** `all_star.csv`, `team.csv`
**Outputs:** `team_allstar_merged_2015.csv`
**Script:** `scripts/step_03_data-merging-integration.py`

**Purpose:**
Next steps for comprehensive analysis:

1. Data Filtering:
- Filter both datasets for year 2015 specifically
- Verify sufficient data exists for 2015 season

2. Data Transformation:
- For team data: extract team_id and games played (g)
- For all-star data: count appearances per team
- Handle potential multiple game_num entries per player

3. Data Integration:
- Merge team games with all-star counts
- Handle possible missing teams (no all-star participants)

4. Analysis Preparation:
- Calculate b

---

### Step 4: Revised Analysis & Refinement

**Inputs:** `all_star.csv`, `team.csv`
**Outputs:** `enhanced_team_allstar_2015.csv`
**Script:** `scripts/step_04_revised-analysis-refinement.py`

**Purpose:**
Revised analytical approach needed:

1. Data Characteristics:
- Games played is effectively a constant (162 for most teams)
- Cannot calculate meaningful quartiles or correlations with constant/near-constant variables
- All-star appearances show actual variation worth analyzing

2. Alternative Approaches:
- Focus analysis solely on all-star appearances distribution
- Compare team performance metrics (wins, rank) with all-star appearances
- Consider league-level differences (AL vs NL)
- Analyze p

---

### Step 5: Statistical Analysis & Hypothesis Testing

**Inputs:** `all_star.csv`, `enhanced_team_allstar_2015.csv`
**Outputs:** `final_team_allstar_analysis_2015.csv`
**Script:** `scripts/step_05_statistical-analysis-hypothesis-testing.py`

**Purpose:**
Next steps for deeper analysis:

1. Statistical Testing:
- Perform t-test between AL/NL all-star appearances
- Calculate correlation between win percentage and appearances
- Test significance of rank vs appearances relationship

2. Advanced Visualization:
- Create ranked bar chart of all-star appearances
- Plot appearances vs final standings position
- Show league comparison with statistical annotations

3. Position Analysis:
- Examine distribution of starting positions
- Compare pitchers vs pos

---

### Step 6: Statistical Analysis & Hypothesis Testing (Phase 2)

**Inputs:** `final_analysis_summary.txt`, `final_team_allstar_analysis_2015.csv`
**Outputs:** `final_analysis_summary.txt`
**Script:** `scripts/step_06_statistical-analysis-hypothesis-testing-.py`

**Purpose:**
Final analytical enhancements needed:

1. Correlation Interpretation:
- Quantify strength of win percentage relationship
- Consider non-linear regression approaches
- Calculate R-squared value for predictive power

2. Team Analysis:
- Investigate why specific teams deviate from expectations
- Examine roster composition of outlier teams
- Compare with fan voting patterns if available

3. Historical Context:
- Compare 2015 patterns with adjacent years
- Identify if 2015 was typical or exceptional


---

### Step 7: Regression Modeling

**Inputs:** `mlb_allstar_2015_final_report.md`, `team.csv`, `final_team_allstar_analysis_2015.csv`
**Outputs:** `mlb_allstar_2015_final_report.md`
**Script:** `scripts/step_07_regression-modeling.py`

**Purpose:**
Final considerations for completing the analysis:

1. Model Enhancement:
- Consider multiple regression with additional predictors (runs scored, ERA)
- Test polynomial regression for non-linear relationships
- Evaluate need for league-specific models

2. Contextual Factors:
- Examine impact of All-Star game location (host team advantage)
- Consider fan voting patterns and player popularity
- Account for roster construction differences

3. Final Reporting:
- Prepare comprehensive discussion of li

---

### Step 8: Statistical Analysis & Hypothesis Testing (Phase 3)

**Inputs:** `mlb_allstar_2015_final_report.md`, `team.csv`, `final_team_allstar_analysis_2015.csv`
**Outputs:** `mlb_allstar_2015_final_report.md`
**Script:** `scripts/step_08_statistical-analysis-hypothesis-testing-.py`

**Purpose:**
To ensure robust final analysis:

1. Code Corrections:
- Add missing import for r2_score
- Verify all required imports are present
- Maintain consistent model evaluation metrics

2. Analysis Integrity:
- Ensure all statistical tests are properly executed
- Validate visualization outputs
- Confirm report generation completeness

3. Final Quality Check:
- Review all numerical outputs for consistency
- Verify file saving operations
- Check markdown report formatting

The corrected code will:
1. Add

---

### Step 9: Model Training & Prediction

**Inputs:** `mlb_allstar_2015_final_report.md`, `team.csv`, `final_team_allstar_analysis_2015.csv`
**Outputs:** `mlb_allstar_2015_final_report.md`
**Script:** `scripts/step_09_model-training-prediction.py`

**Purpose:**
Final analytical refinements needed:

1. Multicollinearity Investigation:
- Calculate Variance Inflation Factors (VIFs)
- Consider removing correlated predictors
- Evaluate model stability

2. Model Simplification:
- Test reduced models with only significant predictors
- Compare AIC/BIC values
- Validate with holdout samples if possible

3. Final Interpretation:
- Prepare clear explanation of coefficients
- Discuss practical significance beyond statistical significance
- Highlight limitations of

---

### Step 10: Final Synthesis & Reporting

**Inputs:** `mlb_allstar_2015_final_report.md`, `team.csv`, `final_team_allstar_analysis_2015.csv`
**Outputs:** `mlb_allstar_2015_final_report.md`
**Script:** `scripts/step_10_final-synthesis-reporting.py`

**Purpose:**
Final refinements needed to complete the analysis:

1. Data Preparation:
- Address multicollinearity through centering/scaling
- Implement proper dataframe operations to avoid warnings
- Ensure numerical stability

2. Model Validation:
- Cross-validate results to ensure reliability
- Check for influential outliers
- Verify assumptions of linear models

3. Reporting:
- Finalize all visualizations
- Complete interpretation of results
- Document limitations and caveats

The code will:
1. Properly h

---

### Step 11: Regression Modeling (Phase 2)

**Inputs:** `mlb_allstar_2015_final_report.md`, `team.csv`, `final_team_allstar_analysis_2015.csv`
**Outputs:** `mlb_allstar_2015_final_report.md`
**Script:** `scripts/step_11_regression-modeling-phase-2.py`

**Purpose:**
Required corrections and improvements:

1. Code Alignment:
- Ensure consistent feature matrix construction
- Match prediction and plotting dimensions
- Maintain proper intercept handling

2. Visualization Enhancement:
- Implement proper residual plotting
- Add regression line to residual plot
- Improve diagnostic visuals

3. Robustness:
- Add error handling
- Validate matrix shapes
- Include dimension checks

The corrected code will:
1. Properly align prediction dimensions
2. Implement robust re

---

### Step 12: Model Training & Prediction (Phase 2)

**Inputs:** `final_team_allstar_analysis_2015.csv`
**Outputs:** `final_model_coefficients.csv`, `validation_results.csv`
**Script:** `scripts/step_12_model-training-prediction-phase-2.py`

**Purpose:**
Root cause analysis and solution pathways:

1. Data Characteristics:
- Small sample size (n=30 teams) makes cross-validation unstable
- Potential outliers disproportionately affecting different folds
- Limited feature space may not capture selection complexity

2. Modeling Approaches:
- Need simpler models for small dataset
- Consider leave-one-out cross-validation
- Implement regularization to prevent overfitting
- Test non-parametric alternatives

3. Validation Strategy:
- Switch to repeated k

---

### Step 13: Data Merging & Integration (Phase 2)

**Inputs:** `team.csv`, `final_team_allstar_analysis_2015.csv`
**Outputs:** `complete_analysis_dataset.csv`, `final_model_interpretation.csv`, `comprehensive_validation_results.csv`
**Script:** `scripts/step_13_data-merging-integration-phase-2.py`

**Purpose:**
Comprehensive solution approach:

1. Data Reconstruction:
- Reload raw data sources
- Reperform merges with proper validation
- Verify all required columns exist

2. Robust Engineering:
- Implement data validation checks
- Add column existence verification
- Include fallback procedures

3. Pipeline Improvement:
- Create complete processing workflow
- Save intermediate checkpoints
- Document data lineage

4. Final Validation:
- Comprehensive feature checking
- Cross-verify all data sources
- Ensu

---

### Step 14: Data Visualization

**Inputs:** `team.csv`, `final_team_allstar_analysis_2015.csv`
**Outputs:** `validation_metrics.csv`, `coefficient_stability.csv`
**Script:** `scripts/step_14_data-visualization.py`

**Purpose:**
Comprehensive solution approach:

1. Import Verification:
- Audit all required sklearn imports
- Include all necessary model evaluation tools
- Add visualization dependencies

2. Code Structure:
- Organize imports logically
- Group related functionality
- Add import verification checks

3. Analysis Continuity:
- Maintain previous analysis steps
- Ensure reproducible results
- Validate all intermediate outputs

4. Final Validation:
- Test complete execution
- Verify output generation
- Check file

---


## Final Output & Deliverables

# Comprehensive Analysis of MLB All-Star Selection Patterns in the 2015 Season

## Introduction and Research Context

The Major League Baseball All-Star Game represents one of the most prestigious honors in professional sports, where player selection patterns reveal important insights about team performance, player recognition, and potential selection biases. This study examines the relationship between team performance metrics and All-Star selections during the 2015 MLB season, employing advanced statistical modeling techniques to quantify these relationships while controlling for various confounding factors. The analysis utilizes two primary datasets: team-level performance statistics capturing win percentages, runs scored, and earned run averages, along with detailed All-Star selection records for all participating players. Through this investigation, we aim to establish empirical evidence regarding the degree to which objective team performance measures predict All-Star selections, while also identifying potential anomalies in the selection process that may indicate subjective influences such as fan popularity or media narratives.

Previous research in sports analytics has demonstrated varying degrees of correlation between individual performance metrics and All-Star selections across different professional sports leagues. However, few studies have systematically examined the team-level factors that influence selection outcomes while accounting for the complex interdependencies between different performance indicators. Our methodological approach combines multiple validation techniques including repeated k-fold cross-validation, leave-one-out analysis, and holdout validation to ensure robust model performance assessment. The analysis reveals that while team winning percentage serves as the most reliable predictor of All-Star selections, explaining approximately 23.5% of the observed variance, significant unexplained variation persists, suggesting the operation of additional non-performance factors in the selection process.

The practical implications of this research extend beyond academic interest, offering valuable insights for team managers, players, and league officials seeking to understand the determinants of All-Star recognition. From a player development perspective, understanding these selection patterns can inform career decisions and training focus areas. For league administrators, the findings may prompt reconsideration of selection criteria to ensure balanced representation across teams and positions. Furthermore, the methodological framework developed in this study establishes a replicable approach for analyzing selection processes in other professional sports leagues where similar honor systems exist.

## Data Preparation and Descriptive Statistics

The foundation of this analysis rests upon careful data preparation and thorough exploratory analysis of the 2015 MLB season statistics. Our dataset incorporates information from al


---

## How to Run

### Local Execution
```bash
# Install dependencies
pip install pandas openpyxl

# Run each step sequentially
cd case_4967_12301
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
