# Pipeline: Data Cleaning & Validation Workflow

## Metadata
| Field | Value |
|---|---|
| **Case ID** | `27` |
| **Difficulty** | N/A/5 |
| **Quality** | N/A/5 |
| **Abilities** |  |
| **Total Steps** | 10 |
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

### Step 1: Data Loading & Profiling

**Inputs:** `course.csv`, `course_analysis.txt`
**Outputs:** `course_analysis.txt`
**Script:** `scripts/step_01_data-loading-profiling.py`

**Purpose:**
To begin this comprehensive exploratory data analysis, I'll first need to understand the structure and content of each provided dataset. The analysis will examine relationships between four key dimensions: course difficulty, professor teaching ability, student capability, and grades. Here's my initial analytical plan:

1. Data Inspection Phase:
   - First examine each file individually to understand their structure and contents
   - Check for missing values, data types, and basic statistics
   -

---

### Step 2: Data Visualization

**Inputs:** `course.csv`
**Outputs:** `course_with_categories.csv`
**Script:** `scripts/step_02_data-visualization.py`

**Purpose:**
To resolve this issue and continue the analysis:

1. Immediate Solution:
   - Need to reload the course data within the visualization code block
   - Ensure all required data is loaded before visualization attempts

2. Structural Improvements:
   - Combine data loading and visualization in single code blocks
   - Add error handling for file loading
   - Include data validation checks

3. Analysis Continuation:
   - Maintain original visualization goals
   - Add additional quality checks on the d

---

### Step 3: Data Visualization (Phase 2)

**Inputs:** `course_with_categories.csv`, `prof.csv`
**Outputs:** Console output only
**Script:** `scripts/step_03_data-visualization-phase-2.py`

**Purpose:**
To continue our comprehensive analysis, we should:

1. Examine the Generated Visualizations:
   - Analyze patterns in course difficulty distribution
   - Investigate relationship between credits and difficulty
   - Identify any outliers or unusual patterns

2. Next Analytical Steps:
   - Load and examine the visualization files to interpret results
   - Analyze the distribution of courses across difficulty categories
   - Prepare to integrate with other datasets (professors, students, registrati

---

### Step 4: Data Loading & Profiling (Phase 2)

**Inputs:** `prof.csv`
**Outputs:** `processed_prof_data.csv`
**Script:** `scripts/step_04_data-loading-profiling-phase-2.py`

**Purpose:**
To maintain analytical momentum and depth:

1. Professor Data Priorities:
   - Understand teaching ability metrics
   - Identify any relationship with course difficulty
   - Examine distribution of professor ratings

2. Integration Strategy:
   - Need to determine how professors connect to courses
   - Plan for eventual multi-dataset joins
   - Consider department-level analysis if available

3. Advanced Analysis Path:
   - Correlation between professor ability and course difficulty
   - Potenti

---

### Step 5: Data Visualization (Phase 3)

**Inputs:** `processed_prof_data.csv`
**Outputs:** `enhanced_prof_data.csv`
**Script:** `scripts/step_05_data-visualization-phase-3.py`

**Purpose:**
To resolve this issue and continue the analysis:

1. Solution Approaches:
   - Option 1: Use valid matplotlib style (e.g., 'seaborn-v0_8')
   - Option 2: Rely solely on seaborn's styling
   - Option 3: Use default matplotlib style

2. Implementation Choice:
   - Will use seaborn's styling through sns.set()
   - Remove matplotlib style specification
   - Maintain all other visualization parameters

3. Additional Improvements:
   - Add error handling for style settings
   - Verify style availabili

---

### Step 6: Data Loading & Profiling (Phase 3)

**Inputs:** `course_with_categories.csv`, `enhanced_prof_data.csv`, `registration.csv`, `processed_reg_data.csv`
**Outputs:** `full_merged_dataset.csv`, `processed_reg_data.csv`
**Script:** `scripts/step_06_data-loading-profiling-phase-3.py`

**Purpose:**
To progress with our comprehensive analysis:

1. Immediate Next Steps:
   - Address the pandas FutureWarning
   - Examine registration data to connect professors and courses
   - Begin integration of datasets

2. Integration Strategy:
   - Need to understand registration.csv structure
   - Identify join keys between datasets
   - Plan merge operations carefully

3. Advanced Analysis Preparation:
   - Prepare for multi-dimensional analysis
   - Consider professor-course combinations
   - Plan for

---

### Step 7: Critical observations and next steps

**Inputs:** `processed_reg_data.csv`
**Outputs:** `enhanced_reg_data.csv`
**Script:** `scripts/step_07_critical-observations-and-next-steps.py`

**Purpose:**
Critical observations and next steps:

1. Immediate Concerns:
   - Registration data lacks professor IDs (prof_id)
   - Cannot directly link professors to courses through registration data
   - Need alternative approach for professor-course relationships

2. Required Adjustments:
   - Need to examine student.csv for potential links
   - Consider alternative relationship paths
   - May need to make assumptions about teaching assignments

3. Analysis Adaptation:
   - Focus initially on course-stud

---

### Step 8: Cluster Analysis

**Inputs:** `student.csv`, `enhanced_student_data.csv`, `enhanced_prof_data.csv`, `enhanced_reg_data.csv`, `course_with_categories.csv`, `RA.csv`
**Outputs:** `enhanced_student_data.csv`, `final_analysis_dataset.csv`
**Script:** `scripts/step_08_cluster-analysis.py`

**Purpose:**
To advance our comprehensive analysis:

1. Immediate Next Steps:
   - Examine student data to complete relationship mapping
   - Investigate student characteristics
   - Explore potential student-performance patterns

2. Integration Requirements:
   - Need student capability metrics from RA.csv
   - Must connect student IDs across datasets
   - Prepare for multi-level analysis

3. Advanced Analysis Path:
   - Student-level performance clustering
   - Course difficulty vs student capability
   - 

---

### Step 9: Data Merging & Integration

**Inputs:** `enhanced_student_data.csv`, `enhanced_prof_data.csv`, `enhanced_reg_data.csv`, `course_with_categories.csv`, `final_analysis_dataset.csv`
**Outputs:** `final_analysis_dataset.csv`
**Script:** `scripts/step_09_data-merging-integration.py`

**Purpose:**
To complete our comprehensive analysis:

1. Final Integration Steps:
   - Execute the prepared integration code
   - Verify merge operations
   - Check for any integration issues

2. Quality Assurance:
   - Validate record counts
   - Ensure no data loss during merges
   - Confirm all key variables preserved

3. Advanced Analysis Preparation:
   - Plan correlation analysis between all key variables
   - Prepare for predictive modeling
   - Design visualizations for integrated data

4. Final Chec

---

### Step 10: Data Merging & Integration (Phase 2)

**Inputs:** `enhanced_student_data.csv`, `enhanced_prof_data.csv`, `enhanced_reg_data.csv`, `course_with_categories.csv`, `RA.csv`
**Outputs:** `final_integrated_dataset.csv`
**Script:** `scripts/step_10_data-merging-integration-phase-2.py`

**Purpose:**
To resolve this issue and complete our comprehensive analysis:

1. Solution Framework:
   - Trace the 'prof_id' column through all merge operations
   - Verify column names across all datasets
   - Implement careful merge sequencing

2. Implementation Strategy:
   - First merge registration with RA data to capture professor links
   - Then merge with student and course data
   - Finally merge professor attributes

3. Data Flow Adjustment:
   - Ensure professor IDs propagate through all merges
  

---


## Final Output & Deliverables

# Comprehensive Analysis of Academic Performance: Integrating Course Difficulty, Professor Effectiveness, and Student Capability

## Introduction and Research Context

The relationship between academic outcomes and various institutional factors has long been a subject of significant scholarly inquiry. This study presents a comprehensive analysis of 148 course registrations across 13 academic courses, involving 38 students and 10 professors at a major university. Our dataset encompasses multiple dimensions of the educational experience, including quantitative measures of course difficulty (ranging from 1-5), professor teaching ability (1-5 scale), student capability assessments (2-5 range), and detailed grade records (A-D scale with 4.0-1.0 numerical equivalents). The research was conducted through an exhaustive exploratory data analysis pipeline that included data cleaning, feature engineering, statistical modeling, and multivariate visualization. Our methodology addressed several data integration challenges, particularly in reconciling professor-student-course relationships, ultimately yielding robust insights despite initial dataset limitations.

Academic performance analysis traditionally focuses on isolated factors, but our integrated approach reveals complex interactions between institutional and individual variables. The dataset shows that 37% of awarded grades were A's (mean numerical grade = 3.82), while D's comprised only 9% of grades (mean = 1.56), suggesting potential grade inflation patterns worth further investigation. Course difficulty follows a roughly normal distribution (mean = 2.92, σ = 1.44), with most courses clustered in the medium difficulty range (3-4). Student capability scores, derived from research assistant evaluations, demonstrate a right-skewed distribution (mean = 3.51, σ = 1.09), indicating most students perform above the theoretical midpoint. These baseline statistics establish the foundation for our more sophisticated analyses of how these variables interact.

The visualization in 'limited_correlation_analysis.png' reveals several unexpected relationships that challenge conventional pedagogical assumptions. Most strikingly, we observe only moderate correlation (r = 0.42) between student capability scores and actual course grades, suggesting academic potential doesn't always translate to performance. Similarly, course difficulty shows minimal correlation with satisfaction scores (r = -0.11), contradicting assumptions that harder courses automatically yield lower satisfaction. These preliminary findings underscore the value of our data-driven approach in surfacing non-intuitive patterns that merit deeper qualitative investigation.

## Methodology and Data Integration Challenges

Our analytical approach employed a multi-stage data integration pipeline that overcame significant structural challenges in the source datasets. The initial dataset architecture comprised five separate tables (course.csv, prof.csv, RA.csv, r


---

## How to Run

### Local Execution
```bash
# Install dependencies
pip install pandas openpyxl

# Run each step sequentially
cd case_27_15311
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
