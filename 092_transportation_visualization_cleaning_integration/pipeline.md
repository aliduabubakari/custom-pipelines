# Pipeline: Data Cleaning & Validation Workflow

## Metadata
| Field | Value |
|---|---|
| **Case ID** | `5376` |
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

### Step 1: Data Loading & Profiling

**Inputs:** `all_star.csv`, `appearances.csv`
**Outputs:** `appearances_sample.csv`, `all_star_sample.csv`
**Script:** `scripts/step_01_data-loading-profiling.py`

**Purpose:**
To begin this analysis, I need to carefully examine the task requirements and develop a comprehensive plan. The instruction asks us to join two datasets (all_star.csv and appearances.csv) to find the total number of games played by each player who started in an All-Star game, along with their starting position, filtering for players with more than 30 games played.

Key steps in our analysis plan:
1. Data Inspection: First, we need to understand the structure and content of both datasets. This in

---

### Step 2: Data Merging & Integration

**Inputs:** `all_star.csv`, `appearances.csv`
**Outputs:** `all_star_starters_with_games.csv`
**Script:** `scripts/step_02_data-merging-integration.py`

**Purpose:**
Based on the initial data understanding, here's the refined analysis plan:

1. Data Preparation:
- Handle missing values in all_star (starting_pos and gp)
- Verify that g_all in appearances represents total games played
- Ensure year and player_id formats match between datasets

2. Join Strategy:
- Inner join on player_id and year to find players who both appeared in All-Star games and have game participation records
- Need to consider that players may have multiple All-Star appearances in a yea

---

### Step 3: Data Cleaning & Standardization

**Inputs:** `all_star_starters_with_games.csv`
**Outputs:** `enhanced_all_star_analysis.csv`
**Script:** `scripts/step_03_data-cleaning-standardization.py`

**Purpose:**
To deepen our analysis, we should:

1. Enhance Position Interpretation:
- Map numeric positions to standard baseball positions (e.g., 1=Pitcher)
- This will make results more interpretable

2. Temporal Analysis:
- Examine how game participation varies by era
- Compare pre/post expansion era (1961) players

3. Position-Specific Trends:
- Compare average career length by position
- Identify positions with longest/shortest careers

4. Outlier Examination:
- Investigate players with extremely high g

---

### Step 4: Data Visualization

**Inputs:** `enhanced_all_star_analysis.csv`
**Outputs:** `iron_men_players.csv`, `final_all_star_analysis.csv`
**Script:** `scripts/step_04_data-visualization.py`

**Purpose:**
Critical improvements needed for deeper analysis:

1. Temporal Analysis Fix:
- Extract debut years from external source or estimate from player_id numbering
- Implement proper decade bins for meaningful era comparisons

2. Position-Specific Insights:
- Calculate career length percentiles by position
- Identify "iron man" thresholds (e.g., top 10% by position)
- Compare modern vs. historical positional demands

3. Advanced Visualizations:
- Small multiples plot of career distributions by position

---

### Step 5: Data Loading & Profiling (Phase 2)

**Inputs:** `all_star.csv`, `appearances.csv`
**Outputs:** `final_era_adjusted_analysis.csv`, `era_adjusted_iron_men.csv`
**Script:** `scripts/step_05_data-loading-profiling-phase-2.py`

**Purpose:**
To address these issues and deepen the analysis:

1. Data Correction:
- Implement proper decade estimation using available year columns
- Cross-validate with external source if possible
- Consider using all_star year as proxy for active period

2. Enhanced Positional Analysis:
- Calculate career length normalized by era (adjust for season length changes)
- Compare pre- and post-free agency periods
- Examine positional trends in modern vs. dead-ball eras

3. Advanced Statistical Methods:
- Post-h

---

### Step 6: Model Training & Prediction

**Inputs:** `final_era_adjusted_analysis.csv`
**Outputs:** `feature_importance.csv`
**Script:** `scripts/step_06_model-training-prediction.py`

**Purpose:**
To deepen our understanding, we should:

1. Examine Positional Trajectories:
- Analyze how position value correlates with career length
- Compare offensive vs. defensive positions

2. Refine Era Adjustments:
- Incorporate league expansion impacts
- Adjust for strike-shortened seasons
- Consider positional evolution over time

3. Advanced Modeling:
- Implement survival analysis with position as covariate
- Build predictive models for career longevity
- Analyze retirement hazard rates by position


---

### Step 7: Data Visualization (Phase 2)

**Inputs:** `final_era_adjusted_analysis.csv`
**Outputs:** `hazard_ratios.csv`
**Script:** `scripts/step_07_data-visualization-phase-2.py`

**Purpose:**
To resolve this and enhance our survival analysis:

1. Visualization Alternatives:
- Use current lifelines plotting methods
- Create manual hazard ratio plots from model coefficients
- Implement forest plot visualization

2. Additional Survival Analysis:
- Add confidence intervals to KM curves
- Test proportional hazards assumption
- Include Schoenfeld residuals analysis

3. Model Enhancement:
- Add interaction terms (position × era)
- Include additional covariates (e.g., All-Star frequency)
- C

---

### Step 8: Data Visualization (Phase 3)

**Inputs:** `final_era_adjusted_analysis.csv`
**Outputs:** `corrected_hazard_ratios.csv`
**Script:** `scripts/step_08_data-visualization-phase-3.py`

**Purpose:**
To resolve this and improve the analysis:

1. Confidence Interval Access:
- Update column references to match current lifelines format
- Verify confidence interval structure before plotting

2. Enhanced Visualization:
- Add reference lines for hazard ratios
- Improve plot formatting and labels
- Add annotations for significant results

3. Additional Diagnostics:
- Include Schoenfeld residuals plot
- Add log-log survival plots for PH assumption checking
- Incorporate AIC/BIC model comparison

Nex

---

### Step 9: Model Training & Prediction (Phase 2)

**Inputs:** `final_era_adjusted_analysis.csv`
**Outputs:** `cox_model_results.csv`, `variance_inflation_factors.csv`, `model_diagnostics.csv`
**Script:** `scripts/step_09_model-training-prediction-phase-2.py`

**Purpose:**
To resolve this and improve the analysis:

1. Correct Results Extraction:
- Access model parameters directly through params_ attribute
- Use confidence_intervals_ attribute for CI values
- Calculate hazard ratios manually from coefficients

2. Enhanced Output:
- Create comprehensive results dataframe
- Add statistical significance indicators
- Include baseline hazard information

3. Additional Validation:
- Add model fit statistics (AIC, concordance)
- Include variance inflation factors
- Check 

---

### Step 10: Data Validation & Quality Report

**Inputs:** `final_era_adjusted_analysis.csv`
**Outputs:** `cox_model_results_robust.csv`
**Script:** `scripts/step_10_data-validation-quality-report.py`

**Purpose:**
To resolve this robustly:

1. Safer Data Access:
- Inspect confidence intervals structure first
- Use position-based access as fallback
- Add error handling for column access

2. Simplified Approach:
- Use summary DataFrame provided by lifelines
- Extract needed values directly from printed output
- Reduce dependency on internal structures

3. Enhanced Validation:
- Add structure verification before processing
- Include fallback mechanisms
- Add debug information for troubleshooting

Next steps 

---

### Step 11: Data Visualization (Phase 4)

**Inputs:** `final_era_adjusted_analysis.csv`
**Outputs:** `positional_hazard_matrix.csv`, `survival_probabilities.csv`
**Script:** `scripts/step_11_data-visualization-phase-4.py`

**Purpose:**
To maximize insights from these results:

1. Interpretation Enhancement:
- Calculate absolute risk differences
- Convert hazard ratios to more intuitive metrics
- Create risk score visualizations

2. Comparative Analysis:
- Compare against traditional longevity metrics
- Validate with player career duration data
- Benchmark against league averages

3. Advanced Visualization:
- Create risk heatmap by position and decade
- Generate interactive risk calculator
- Plot survival curves by risk strata


---

### Step 12: Final Synthesis & Reporting

**Inputs:** `model_summary.txt`, `final_era_adjusted_analysis.csv`
**Outputs:** `model_summary.txt`, `final_positional_hazard_results.csv`
**Script:** `scripts/step_12_final-synthesis-reporting.py`

**Purpose:**
To complete the analysis robustly:

1. Survival Analysis Correction:
- Use available baseline survival attributes
- Implement proper survival prediction
- Maintain comparative analysis capability

2. Enhanced Visualization:
- Create publication-quality survival curves
- Add confidence intervals
- Include at-risk tables

3. Comprehensive Reporting:
- Prepare all results for final report
- Organize findings by research question
- Structure supporting evidence

Next steps in code:
1. Correct surviv

---

### Step 13: Final Synthesis & Reporting (Phase 2)

**Inputs:** `final_era_adjusted_analysis.csv`
**Outputs:** `cox_model_summary.csv`, `final_hazard_comparison.csv`
**Script:** `scripts/step_13_final-synthesis-reporting-phase-2.py`

**Purpose:**
To resolve this and complete the analysis:

1. Data Structure Alignment:
- Ensure prediction data matches training structure
- Initialize all required columns
- Maintain consistent dummy variable approach

2. Robust Prediction:
- Create proper synthetic observation
- Include all model features
- Handle reference category properly

3. Final Visualization:
- Generate publication-ready survival curves
- Add confidence intervals
- Include proper labeling

Next steps in code:
1. Fix prediction data s

---

### Step 14: Data Visualization (Phase 5)

**Inputs:** `final_report.md`, `final_era_adjusted_analysis.csv`
**Outputs:** `final_report.md`, `final_model_summary.csv`, `final_hazard_ratios.csv`
**Script:** `scripts/step_14_data-visualization-phase-5.py`

**Purpose:**
To resolve this and finalize the analysis:

1. Array Handling:
- Ensure consistent array shapes for plotting
- Properly handle both baseline and predicted survival
- Maintain original time points

2. Visualization Enhancement:
- Add confidence bands
- Improve plot styling
- Add at-risk counts

3. Final Reporting:
- Prepare comprehensive results
- Organize all visualizations
- Structure final outputs

Next steps in code:
1. Fix array dimensions for plotting
2. Enhance survival curve visualization

---


## Final Output & Deliverables

# Comprehensive Analysis of All-Star Baseball Player Career Longevity by Position

## Introduction and Research Background

The analysis of professional athletes' career longevity provides valuable insights into the physical demands and occupational hazards associated with different positions in sports. In Major League Baseball (MLB), where careers can span decades for some players while ending abruptly for others, understanding the factors that influence career duration has significant implications for player development, team management, and medical staff. This study examines 5,069 All-Star game appearances from 1933 to 2015, combining them with detailed game participation records from 100,951 seasonal appearances to quantify positional differences in career longevity. The research employs survival analysis techniques to account for the time-to-event nature of career duration while adjusting for historical era effects. Our findings reveal substantial variations in career longevity across positions, with catchers demonstrating remarkable durability despite their physically demanding role, while pitchers show significantly shorter careers compared to position players. These results challenge some conventional wisdom about baseball positions while confirming other long-held beliefs with rigorous statistical evidence.

The dataset combines two primary sources: the all_star.csv file containing 5,069 records of All-Star game participants from 1933 to 2015, and the appearances.csv file with 100,951 seasonal records detailing game participation by position. After data cleaning and merging, our final analysis dataset includes 734 players who started in All-Star games and had more than 30 games played in their respective seasons. The statistical modeling employs Cox proportional hazards regression, which allows us to estimate hazard ratios while controlling for the decade in which players were active. This approach provides several advantages over traditional methods of comparing career lengths, including the ability to handle right-censored data and incorporate time-dependent covariates. The model achieves a concordance index of 0.77, indicating strong discriminative power in predicting career longevity based on position and era.

Our methodology addresses several challenges inherent in baseball career analysis. First, we account for the increasing number of games per season over time through era-adjustment factors. Second, we handle the positional mobility of many players by focusing on their primary All-Star position. Third, we mitigate survivor bias by including all players who met the selection criteria, not just those with complete careers. The analysis proceeds in three main phases: exploratory data analysis to understand basic patterns, survival analysis to model career duration, and comparative analysis to quantify positional differences. Visualizations including survival curves, hazard ratio forest plots, and era-adjusted positional comparisons


---

## How to Run

### Local Execution
```bash
# Install dependencies
pip install pandas openpyxl

# Run each step sequentially
cd case_5376_13211
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
