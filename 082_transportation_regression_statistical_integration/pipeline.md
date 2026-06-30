# Pipeline: Data Cleaning & Validation Workflow

## Metadata
| Field | Value |
|---|---|
| **Case ID** | `14` |
| **Difficulty** | N/A/5 |
| **Quality** | N/A/5 |
| **Abilities** |  |
| **Total Steps** | 9 |
| **Input Files** | 2 |
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

**Inputs:** `player_allstar.csv`, `awards_players.csv`
**Outputs:** Console output only
**Script:** `scripts/step_01_data-loading-profiling.py`

**Purpose:**
This task requires combining data from two tables (awards_players and player_allstar) to create a comprehensive player performance analysis. The key steps needed are:

1. Data Understanding Phase:
- First need to examine the structure of both tables to understand their columns and data types
- Verify the common key (playerID) that will be used for joining
- Check for missing values and data quality issues in both datasets

2. Data Processing Steps:
- For awards_players: Count total awards per pl

---

### Step 2: Data Merging & Integration

**Inputs:** `player_allstar.csv`, `awards_players.csv`
**Outputs:** `player_awards_ppg.csv`
**Script:** `scripts/step_02_data-merging-integration.py`

**Purpose:**
Based on the data understanding, here's the refined analysis plan:

1. Data Processing Priorities:
- For awards: Simple count aggregation by playerID
- For all-star: Need to calculate points per game (points/games_played)
- Must handle cases where games_played=0 to avoid division errors
- Should consider imputing missing points data or excluding those records

2. Join Strategy:
- Inner join will only keep players with both awards and all-star appearances
- Outer join would preserve all players b

---

### Step 3: Statistical Analysis & Hypothesis Testing

**Inputs:** `player_awards_ppg.csv`
**Outputs:** `player_awards_ppg_cleaned.csv`
**Script:** `scripts/step_03_statistical-analysis-hypothesis-testing.py`

**Purpose:**
Key areas requiring further investigation and refinement:

1. Data Cleaning Priorities:
- Need to resolve playerID collision for 'onealsh01'
- Should investigate PPG=0 cases for potential data errors
- Consider filtering extreme outliers in PPG

2. Enhanced Analysis Opportunities:
- Calculate award density (awards per season)
- Add position information from awards data
- Analyze correlation between awards and PPG
- Examine temporal trends in award/performance relationship

3. Visualization Needs

---

### Step 4: Data Loading & Profiling (Phase 2)

**Inputs:** `player_allstar.csv`, `awards_players.csv`, `player_awards_ppg_cleaned.csv`
**Outputs:** `player_awards_ppg_enhanced.csv`
**Script:** `scripts/step_04_data-loading-profiling-phase-2.py`

**Purpose:**
For deeper understanding, we should:

1. Position-Based Analysis:
- Merge position data from awards table
- Compare guard/forward/center performance patterns
- Examine if certain positions accumulate more awards

2. Temporal Analysis:
- Incorporate decade-based grouping
- Analyze if award-PPG relationship has changed over time
- Compare different NBA eras

3. Advanced Statistical Modeling:
- Consider non-linear regression models
- Account for games played as weighting factor
- Cluster analysis t

---

### Step 5: Regression Modeling

**Inputs:** `player_awards_ppg_enhanced.csv`
**Outputs:** `nba_player_analysis_final.csv`
**Script:** `scripts/step_05_regression-modeling.py`

**Purpose:**
For final comprehensive analysis, we should:

1. Statistical Modeling:
- Implement regression analysis controlling for position and decade
- Test significance of position and era effects
- Consider interaction terms between position and era

2. Advanced Visualization:
- Create small multiples showing position trends by decade
- Add confidence intervals to show statistical significance
- Highlight standout players in each category

3. Final Data Enrichment:
- Add career length as a control variab

---

### Step 6: Regression Modeling (Phase 2)

**Inputs:** `nba_player_analysis_final.csv`
**Outputs:** `nba_career_analysis_final.csv`
**Script:** `scripts/step_06_regression-modeling-phase-2.py`

**Purpose:**
Final refinements needed before report generation:

1. Data Aggregation:
- Create true career averages by properly aggregating multi-season players
- Ensure each player appears only once in final dataset
- Calculate career length as additional variable

2. Model Enhancement:
- Add interaction terms between position and era
- Include total awards as predictor in regression
- Consider non-linear terms for awards-performance relationship

3. Visualization Refinement:
- Create faceted plots by posit

---

### Step 7: Final Synthesis & Reporting

**Inputs:** `nba_analysis_summary.txt`, `nba_career_analysis_final.csv`
**Outputs:** `nba_analysis_summary.txt`
**Script:** `scripts/step_07_final-synthesis-reporting.py`

**Purpose:**
Final steps needed for comprehensive report:

1. Model Simplification:
- Remove non-significant interaction terms
- Focus on core relationship between awards and performance
- Consider polynomial terms for awards

2. Visualization Enhancement:
- Create final scatterplot with regression line
- Highlight top performers with annotations
- Add distribution plots for key variables

3. Report Preparation:
- Organize findings into logical sections
- Create summary tables of key results
- Prepare visual

---

### Step 8: Revised Analysis & Refinement

**Inputs:** `nba_career_analysis_final.csv`
**Outputs:** Console output only
**Script:** `scripts/step_08_revised-analysis-refinement.py`

**Purpose:**
Revised approach to resolve the conflict:

1. Alternative Implementation Paths:
- Use seaborn's lmplot instead of regplot
- Separate scatter and regression plotting
- Reduce styling complexity temporarily

2. Priority Preservation:
- Maintain core analytical visualization
- Keep all data elements visible
- Ensure readability of annotations

3. Quality Assurance:
- Test minimal working example first
- Gradually add back styling elements
- Verify output at each step

Implementation priorities:
1. 

---

### Step 9: Data Visualization

**Inputs:** `nba_career_analysis_final.csv`
**Outputs:** Console output only
**Script:** `scripts/step_09_data-visualization.py`

**Purpose:**
To improve code quality and future-proof the implementation:

1. Immediate Improvements:
- Update boxplot syntax to comply with new seaborn standards
- Maintain all existing visualization features
- Ensure backward compatibility

2. Enhanced Robustness:
- Add explicit parameter handling
- Document visualization choices
- Include version compatibility notes

3. Final Quality Checks:
- Verify visual output matches requirements
- Confirm file saving works correctly
- Check warning resolution

Imple

---


## Final Output & Deliverables

# Comprehensive Analysis of NBA Player Performance: The Relationship Between Career Awards and All-Star Game Performance

## Introduction and Research Context

The analysis of professional athlete performance has long been a subject of intense interest in sports analytics, with basketball presenting particularly rich opportunities for quantitative examination. This study investigates the relationship between career achievement (as measured by awards) and on-court performance (as measured by All-Star game points per game) among NBA players across multiple decades. Our dataset comprises 314 unique player careers spanning from the 1950s through the 2000s, representing a comprehensive cross-section of basketball talent at the highest level of competition. The research methodology combines statistical modeling with visual analytics to uncover patterns that may inform our understanding of how recognition correlates with measurable performance outcomes.

Several foundational questions guided this investigation. First, to what extent does the quantity of career awards predict a player's scoring performance in All-Star games? Second, how do positional differences affect this relationship? Third, have these patterns remained consistent across different eras of professional basketball? The analysis reveals that while a statistically significant relationship exists between awards and performance (r = 0.307, p < 0.001), this association explains only a modest portion of the variance in All-Star performance (R² = 0.096 in our final model). Centers demonstrated the highest average performance metrics (12.11 PPG) and award counts (12.08), followed by forwards (11.71 PPG, 7.10 awards) and guards (10.99 PPG, 6.55 awards).

The temporal analysis uncovered intriguing patterns in the evolution of player performance. While the 1990s saw the highest average awards per player (11.26), the 2000s featured the strongest scoring performance (12.02 PPG). This suggests potential shifts in how awards were allocated or how All-Star games were played across different eras. The visualization in [final_awards_ppg_analysis.png] illustrates these relationships, highlighting exceptional performers like LeBron James (23.67 PPG) and Kareem Abdul-Jabbar (35 career awards). These findings contribute to ongoing discussions about the objectivity of performance metrics versus subjective award allocations in professional sports.

Methodologically, this study employed a multi-phase analytical approach. After initial data cleaning that resolved issues like playerID collisions (notably for 'onealsh01'), we implemented a series of regression models progressing from simple bivariate analyses to more complex multivariate formulations. The final model incorporated position groups and award counts as predictors while controlling for era effects. Our visual analytics approach produced several key outputs, including the position comparison chart in [position_ppg_comparison.png], which demonstrates the


---

## How to Run

### Local Execution
```bash
# Install dependencies
pip install pandas openpyxl

# Run each step sequentially
cd case_14_17178
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
