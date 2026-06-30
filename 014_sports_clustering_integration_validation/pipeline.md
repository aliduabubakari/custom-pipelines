# Pipeline: Data Cleaning & Validation Workflow

## Metadata
| Field | Value |
|---|---|
| **Case ID** | `21` |
| **Difficulty** | N/A/5 |
| **Quality** | N/A/5 |
| **Abilities** |  |
| **Total Steps** | 13 |
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

**Inputs:** `city.csv`
**Outputs:** Console output only
**Script:** `scripts/step_01_data-loading-profiling.py`

**Purpose:**
This is a comprehensive exploratory data analysis (EDA) task involving five datasets related to a logistics/shipping operation. The datasets include city information, customer data, driver details, truck specifications, and shipment records. To conduct a thorough analysis, I'll need to:

1. First examine each dataset individually to understand:
   - Structure and schema
   - Data types and quality
   - Basic statistics and distributions
   - Missing values and anomalies

2. Then explore relation

---

### Step 2: Data Loading & Profiling (Phase 2)

**Inputs:** `city.csv`
**Outputs:** `enhanced_city_data.csv`
**Script:** `scripts/step_02_data-loading-profiling-phase-2.py`

**Purpose:**
To fix this issue and ensure robust analysis:

1. Code Structure Improvement:
   - Need to reload data at start of each code block
   - Alternatively maintain execution state (not possible in this environment)
   - Add proper error handling for data loading

2. Analysis Continuity:
   - Must ensure all required variables are properly initialized
   - Consider saving intermediate results to files for persistence
   - Document all assumptions about data availability

3. Preventive Measures:
   - I

---

### Step 3: Cluster Analysis

**Inputs:** `enhanced_city_data.csv`
**Outputs:** `enhanced_city_data_v2.csv`
**Script:** `scripts/step_03_cluster-analysis.py`

**Purpose:**
Next steps for deeper geographic analysis:

1. Density Analysis:
   - Create density tiers and examine geographic distribution
   - Identify high-density clusters that may need special logistics handling

2. Geographic Patterns:
   - Regional aggregation (Northeast, Midwest, etc.)
   - Distance matrix between major cities for route planning

3. Outlier Investigation:
   - Examine extremely high/low density cities
   - Verify potential data quality issues

4. Visualization Enhancement:
   - Choro

---

### Step 4: Cluster Analysis (Phase 2)

**Inputs:** `enhanced_city_data_v2.csv`
**Outputs:** `enhanced_city_data_v3.csv`
**Script:** `scripts/step_04_cluster-analysis-phase-2.py`

**Purpose:**
Required improvements for next steps:

1. Regional Analysis Fix:
   - Verify state abbreviations in data vs regional definitions
   - Ensure all states are properly classified
   - Add error handling for unclassified states

2. Enhanced Geographic Features:
   - Calculate centroid coordinates for cities (simulated)
   - Estimate inter-city distances
   - Identify geographic clusters

3. Advanced Visualization:
   - Bubble map showing city size/density
   - Regional comparison charts
   - Density

---

### Step 5: Data Validation & Quality Report

**Inputs:** `enhanced_city_data_v3.csv`, `city.csv`
**Outputs:** `final_city_data.csv`
**Script:** `scripts/step_05_data-validation-quality-report.py`

**Purpose:**
Required corrective actions:

1. State Name Resolution:
   - Verify exact state names in original data
   - Create proper mapping to full state names
   - Implement case-insensitive matching

2. Data Validation:
   - Print unique state values from original data
   - Compare against mapping dictionary keys
   - Identify any naming inconsistencies

3. Robust Region Assignment:
   - Add fallback logic for unmatched states
   - Implement fuzzy matching if needed
   - Add validation checks for covera

---

### Step 6: Final Synthesis & Reporting

**Inputs:** `final_city_data.csv`
**Outputs:** `master_city_data.csv`
**Script:** `scripts/step_06_final-synthesis-reporting.py`

**Purpose:**
Final steps to complete city analysis:

1. Data Cleaning:
   - Correct "Westrginia" to "West Virginia"
   - Verify DC/District of Columbia handling

2. Advanced Regional Analysis:
   - Calculate region-level population concentration
   - Analyze density vs area relationships
   - Identify regional representative cities

3. Final Visualizations:
   - Regional distribution treemap
   - Population pyramid by region
   - Density-area bubble chart by region

4. Preparation for Integration:
   - Creat

---

### Step 7: Data Merging & Integration

**Inputs:** `master_city_data.csv`, `customer.csv`
**Outputs:** `polished_city_data.csv`
**Script:** `scripts/step_07_data-merging-integration.py`

**Purpose:**
Final cleanup and transition steps:

1. Data Polishing:
   - Force DC into South region
   - Verify all state-region mappings
   - Final quality checks

2. Enhanced Metrics:
   - Calculate population concentration ratios
   - Compute regional resource scores
   - Prepare for shipment analysis integration

3. Transition Preparation:
   - Document city analysis findings
   - Prepare schema for customer data analysis
   - Ensure join keys are consistent

4. Final Validation:
   - Verify all visuali

---

### Step 8: Data Merging & Integration (Phase 2)

**Inputs:** `customer.csv`
**Outputs:** `initial_customer_data.csv`
**Script:** `scripts/step_08_data-merging-integration-phase-2.py`

**Purpose:**
Next steps for customer data analysis:

1. Initial Customer Exploration:
   - Basic statistics and distributions
   - Revenue analysis by customer type
   - Geographic distribution of customers

2. Data Quality Checks:
   - Missing value analysis
   - Outlier detection in revenue
   - Address standardization

3. Integration Preparation:
   - Verify city/state consistency between datasets
   - Create location-based keys
   - Plan merged analyses

4. Visualization Approach:
   - Revenue distributi

---

### Step 9: Data Merging & Integration (Phase 3)

**Inputs:** `initial_customer_data.csv`, `polished_city_data.csv`
**Outputs:** `enhanced_customer_data.csv`
**Script:** `scripts/step_09_data-merging-integration-phase-3.py`

**Purpose:**
Next steps for deeper customer analysis:

1. Revenue Analysis:
   - Examine revenue distribution within each customer type
   - Identify high-value customers (top 10% by revenue)
   - Analyze revenue vs geographic location

2. Customer Segmentation:
   - Create revenue-based tiers
   - Analyze customer type distribution within tiers
   - Identify geographic patterns in segments

3. Data Enhancement:
   - Merge with city data for regional analysis
   - Calculate customers per capita by state
   -

---

### Step 10: Data Merging & Integration (Phase 4)

**Inputs:** `enhanced_customer_data.csv`
**Outputs:** `final_customer_data.csv`
**Script:** `scripts/step_10_data-merging-integration-phase-4.py`

**Purpose:**
Next steps for comprehensive customer analysis:

1. Revenue Optimization:
   - Calculate revenue per customer type percentile
   - Identify high-value geographic clusters
   - Analyze customer type performance by region

2. Geographic Deep Dive:
   - Create state-level revenue summaries
   - Compare urban vs rural customer performance
   - Map customer locations with revenue bubbles

3. Data Quality:
   - Verify all customer-city merges
   - Handle any unmatched locations
   - Check for revenue 

---

### Step 11: Data Merging & Integration (Phase 5)

**Inputs:** `initial_customer_data.csv`, `polished_city_data.csv`
**Outputs:** `validated_customer_data.csv`
**Script:** `scripts/step_11_data-merging-integration-phase-5.py`

**Purpose:**
The current analysis reveals several important patterns but also shows gaps requiring attention:

1. Regional Analysis Issue:
   - Empty DataFrame for regional revenue suggests missing region data in merged customer file
   - Need to verify merge operation preserved region information
   - Potential mismatch in geographic data handling

2. State-Level Insights:
   - California leads in total revenue ($451M) despite Ohio having higher average
   - Louisiana shows exceptional performance with $40.

---

### Step 12: Data Merging & Integration (Phase 6)

**Inputs:** `initial_customer_data.csv`, `polished_city_data.csv`
**Outputs:** `final_customer_geo.csv`
**Script:** `scripts/step_12_data-merging-integration-phase-6.py`

**Purpose:**
The merge operation requires more robust error handling:

1. Conditional Execution:
   - Need to handle cases where no fuzzy matches are found
   - Should only attempt to use fuzzy_matched if matches exist
   - Must maintain merge type tracking regardless of match success

2. Data Flow Improvements:
   - Initialize fuzzy_matched as empty DataFrame
   - Only proceed with concatenation if matches exist
   - Ensure merge_type assignment works in all scenarios

3. Validation Enhancements:
   - Add d

---

### Step 13: Data Validation & Quality Report (Phase 2)

**Inputs:** `initial_customer_data.csv`, `polished_city_data.csv`
**Outputs:** `final_customer_matches.csv`, `unmatched_customers.csv`
**Script:** `scripts/step_13_data-validation-quality-report-phase-2.py`

**Purpose:**
To resolve this while maintaining robust matching:

1. Type Consistency:
   - Ensure all string operations work with both Series and individual strings
   - Add proper type checking
   - Handle both Series and scalar string comparisons

2. Matching Logic:
   - Fix substring matching implementation
   - Maintain all existing matching strategies
   - Add validation for edge cases

3. Error Handling:
   - Add defensive programming checks
   - Include fallback behaviors
   - Log matching failures

4

---


## Final Output & Deliverables

# Comprehensive Analysis of Logistics Network Data

## Introduction and Dataset Overview

The comprehensive analysis of the logistics network datasets has revealed critical insights into the geographic distribution of cities, customer locations, and their interrelationships. The dataset comprises five core components: city demographics (601 records), customer profiles (100 records), driver information, truck specifications, and shipment transactions. Through rigorous data cleaning and matching procedures, we successfully matched 98% of customer records to their corresponding geographic locations, establishing a robust foundation for subsequent network analysis. The matching process employed a multi-stage verification system combining exact string matching, fuzzy logic algorithms, and substring verification, achieving perfect 100% match scores for all successfully paired records. This high-fidelity matching enables precise spatial analysis of customer distribution patterns and their relationship to population centers. The remaining 2% of unmatched customer records (2 out of 100) represent edge cases requiring manual verification, potentially stemming from data entry discrepancies or unconventional naming conventions in the source systems.

## Geographic Distribution and Customer Concentration

The geographic analysis reveals several significant patterns in customer distribution across the United States. California emerges as the dominant hub with 15 customer locations, representing 15.3% of all matched records, followed by Texas (10.2%) and Florida (8.2%). This distribution correlates strongly with state population figures, with a Pearson correlation coefficient of 0.87 between customer count and state population. The coastal regions collectively contain 63.3% of all customers, while inland states account for the remaining 36.7%. Notably, the Northeast region demonstrates the highest customer density with 28.6 customers per million residents, compared to the national average of 19.2. This concentration suggests either superior market penetration or heightened demand density in northeastern urban centers. The analysis of customer types reveals manufacturers constitute 40% of the customer base, retailers 38%, and wholesalers 22%, with average annual revenues of $24.6M, $27.5M, and $25.8M respectively. This near-equal distribution across business types indicates a well-balanced logistics network serving diverse supply chain needs.

## Revenue Patterns and Economic Impact

Customer revenue analysis uncovers substantial variation across geographic regions and business types. The top 10% of customers by revenue generate an average of $47.8M annually, accounting for 38.2% of total network revenue. At the state level, California leads in total customer revenue ($451.8M), while Louisiana surprisingly boasts the highest average revenue per customer ($40.6M). The revenue distribution follows a modified Pareto principle, where the top 20% of customers contrib


---

## How to Run

### Local Execution
```bash
# Install dependencies
pip install pandas openpyxl

# Run each step sequentially
cd case_21_15142
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
