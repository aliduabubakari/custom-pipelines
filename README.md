# 🚀 Custom Pipelines — _100 Production-Ready ML Data Pipelines_

<p align="center">
  <img src="https://img.shields.io/badge/Pipelines-100-blue?style=for-the-badge" alt="100 Pipelines"/>
  <img src="https://img.shields.io/badge/Scripts-600+-orange?style=for-the-badge" alt="600+ Scripts"/>
  <img src="https://img.shields.io/badge/Domains-10-purple?style=for-the-badge" alt="10 Domains"/>
  <img src="https://img.shields.io/badge/Techniques-12-9cf?style=for-the-badge" alt="12 Techniques"/>
  <img src="https://img.shields.io/badge/Runnable-✓-green?style=for-the-badge" alt="100% Runnable"/>
</p>

<p align="center">
  <em>A curated collection of 100 end-to-end ML data pipelines — every single one is <strong>self-contained, runnable, and domain-aware</strong>. From credit risk scoring to sports analytics, from energy forecasting to fraud detection — each pipeline ships with its own synthetic data, working Python scripts, and comprehensive documentation.</em>
</p>

---

## 📊 By the Numbers

| Metric | Count |
|---|---|
| **Total Pipelines** | 100 |
| **Total Python Scripts** | 624 |
| **Pipeline Documentation (`.md`)** | 100 |
| **Argo Workflow Definitions (`.yaml`)** | 100 |
| **Input Data Files** | 115 (CSV, JSON, XLSX) |
| **Domains Covered** | 10 |
| **ML Techniques** | 12 |
| **Lines of Python** | ~19,000+ |
| **Pipeline Steps per Pipeline** | 6–16 |

---

## 🏗️ Architecture

Every pipeline follows a standardized architecture. The number of steps varies by complexity:

### Standard Pipeline (6 steps)

```
  ┌─────────────────────────┐
  │  Step 1: LOAD & PROFILE │ ── Data ingestion, column profiling, null detection
  └────────────┬────────────┘
               ▼
  ┌─────────────────────────┐
  │  Step 2: CLEAN          │ ── Missing value imputation, outlier capping, standardization
  └────────────┬────────────┘
               ▼
  ┌─────────────────────────┐
  │  Step 3: FEATURES       │ ── Derived features, categorical encoding, ratio creation
  └────────────┬────────────┘
               ▼
  ┌─────────────────────────┐
  │  Step 4: EDA & VIZ      │ ── Distribution histograms, correlation heatmaps, dashboards
  └────────────┬────────────┘
               ▼
  ┌─────────────────────────┐
  │  Step 5: MODEL          │ ── ML training: classification, regression, clustering
  └────────────┬────────────┘
               ▼
  ┌─────────────────────────┐
  │  Step 6: REPORT          │ ── Final synthesis, business recommendations
  └─────────────────────────┘
```

### Advanced Pipeline (10–16 steps)

Complex Category A pipelines additionally include:

| Extra Step | Example Pipeline |
|---|---|
| **Data Merging & Integration** | Multi-source joins (credit_risk: 3 sources) |
| **Data Validation & Compliance** | Regulatory checks, SOC 2 metrics |
| **Time Series Decomposition** | Seasonal patterns, trend analysis (demand_forecasting) |
| **Cohort Analysis** | Retention cohorts, survival curves (customer_churn) |
| **Statistical Hypothesis Testing** | T-tests, chi-square, ANOVA, effect sizes |
| **Advanced Feature Engineering** | RFM scores, temporal lags, interaction terms |
| **Multi-Model Comparison** | LR vs RF vs XGBoost vs LightGBM with CV |
| **Hyperparameter Tuning** | Grid search, Optuna Bayesian optimization |
| **Model Explainability** | SHAP values, LIME explanations, adverse action codes |
| **Fairness & Bias Audit** | Statistical parity, disparate impact, ECOA compliance |
| **Customer Segmentation** | K-Means clustering for retention targeting |
| **Inventory Optimization** | Safety stock, reorder point, holding cost simulation |
| **ROI / Business Impact Analysis** | Campaign cost vs retention value at optimal thresholds |

---

## 🗺️ Domain Landscape

The 100 pipelines span **10 business domains**, with two distinct design philosophies:

### Category A — Rich Domain Pipelines (#001–#013)

_Deep, domain-specific pipelines with multi-source real-world data schemas. Each tells a complete business story from data to decision._

| # | Pipeline | Steps | Domain | Data Sources | Key Techniques |
|---|---|---|---|---|---|
| 001 | `analytics_statistical_cleaning_integration` | 6 | Finance | `stocks.csv`, `market_indices.csv` | Stock returns, sector analysis, market direction prediction |
| 002 | `analytics_statistical_integration` | 6 | Analytics | `data.csv` (experimental) | Treatment effects, hypothesis testing, ANOVA |
| 003 | `credit_risk` | 16 | Finance | `applications.csv`, `bureau_data.xlsx`, `credit_history.json` | FICO scoring, ensemble models, SHAP explainability, fairness audit |
| 004 | `customer_churn` | 16 | SaaS | `customers.csv`, `transactions.json` | RFM analysis, cohort retention, survival curves, ROI optimization |
| 005 | `demand_forecasting` | 10 | Supply Chain | `inventory.csv`, `sales_orders.json`, `suppliers.xlsx` | Time series decomposition, seasonal indices, inventory optimization |
| 006 | `ecommerce_recommendation` | 6 | E-Commerce | `customers.csv`, `products.csv`, `orders.json` | K-Means clustering, product segmentation |
| 007 | `employee_attrition` | 6 | HR Analytics | `employees.csv`, `engagement_surveys.json`, `performance_reviews.xlsx` | Attrition prediction, engagement scoring |
| 008 | `energy_forecasting` | 6 | Energy | `energy_consumption.csv`, `weather.csv` | Consumption regression, weather covariates |
| 009 | `healthcare_readmission` | 6 | Healthcare | `patients.csv`, `admissions.json`, `lab_results.json`, `medications.xlsx` | Clinical risk prediction, 4-source integration |
| 010 | `hr_regression_visualization_integration` | 6 | HR Analytics | `employees.csv`, `departments.csv` | Salary regression, budget analysis, pay equity |
| 011 | `hr_visualization_integration_validation` | 6 | HR Analytics | `hr_data.csv` | Workforce clustering, validation checks, performance prediction |
| 012 | `insurance_claims` | 6 | Insurance | `claims.csv` | Fraud detection, claim pattern analysis |
| 013 | `predictive_maintenance` | 6 | Manufacturing | `sensor_readings.csv` | Failure prediction from IoT sensor data |

### Category B — Technique-Varied Pipelines (#014–#100)

_Systematic exploration of ML technique combinations across sports and transportation domains. Each pipeline name encodes its analytical abilities._

#### ⚽ Sports Analytics — 40 Pipelines (#014–#053)

Uses synthetic player data (500 records, 15+ features): `player_id`, `team`, `position`, `games_played`, `points_per_game`, `assists_per_game`, `rebounds_per_game`, `minutes_per_game`, `age`, `experience_years`, `salary_millions`, and technique-specific columns.

| Technique | # Pipelines | What It Does |
|---|---|---|
| **Clustering** | 5 | K-Means player segmentation, cluster profiling, play-style grouping |
| **Prediction** | 9 | Binary classification (All-Star, injury risk), RandomForest, ROC-AUC |
| **Regression** | 10 | Market value prediction, win shares modeling, MAE/R² evaluation |
| **Statistical** | 8 | Pearson correlation, ANOVA by team/position, hypothesis testing |
| **Visualization** | 8 | Multi-panel dashboards, correlation heatmaps, distribution plots |

Full sports pipeline listing:

| # | Pipeline | Techniques |
|---|---|---|
| 014 | `sports_clustering_integration_validation` | Clustering + Integration + Validation |
| 015 | `sports_clustering_prediction_statistical` | Clustering + Prediction + Statistical |
| 016 | `sports_clustering_prediction_visualization` | Clustering + Prediction + Visualization |
| 017 | `sports_clustering_statistical_visualization` | Clustering + Statistical + Visualization |
| 018 | `sports_clustering_visualization_integration` | Clustering + Visualization + Integration |
| 019 | `sports_prediction_cleaning_integration` | Prediction + Cleaning + Integration |
| 020 | `sports_prediction_statistical_visualization` | Prediction + Statistical + Visualization |
| 021 | `sports_prediction_statistical_visualization_v2` | Prediction + Statistical + Visualization (v2) |
| 022 | `sports_prediction_visualization_cleaning` | Prediction + Visualization + Cleaning |
| 023 | `sports_regression_clustering_visualization` | Regression + Clustering + Visualization |
| 024 | `sports_regression_prediction_statistical` | Regression + Prediction + Statistical |
| 025 | `sports_regression_prediction_statistical_v2` | Regression + Prediction + Statistical (v2) |
| 026 | `sports_regression_prediction_statistical_v3` | Regression + Prediction + Statistical (v3) |
| 027 | `sports_regression_prediction_visualization` | Regression + Prediction + Visualization |
| 028 | `sports_regression_prediction_visualization_v2` | Regression + Prediction + Visualization (v2) |
| 029 | `sports_regression_statistical_visualization` | Regression + Statistical + Visualization |
| 030 | `sports_statistical_cleaning` | Statistical + Cleaning |
| 031 | `sports_statistical_cleaning_integration` | Statistical + Cleaning + Integration |
| 032 | `sports_statistical_cleaning_integration_v2` | Statistical + Cleaning + Integration (v2) |
| 033 | `sports_statistical_cleaning_integration_v3` | Statistical + Cleaning + Integration (v3) |
| 034 | `sports_statistical_cleaning_integration_v4` | Statistical + Cleaning + Integration (v4) |
| 035 | `sports_statistical_cleaning_integration_v5` | Statistical + Cleaning + Integration (v5) |
| 036 | `sports_statistical_cleaning_validation` | Statistical + Cleaning + Validation |
| 037 | `sports_statistical_integration` | Statistical + Integration |
| 038 | `sports_statistical_integration_v2` | Statistical + Integration (v2) |
| 039 | `sports_statistical_visualization_cleaning` | Statistical + Visualization + Cleaning |
| 040 | `sports_statistical_visualization_cleaning_v2` | Statistical + Visualization + Cleaning (v2) |
| 041 | `sports_statistical_visualization_integration` | Statistical + Visualization + Integration |
| 042 | `sports_validation_recovery` | Validation + Recovery |
| 043 | `sports_visualization` | Visualization |
| 044 | `sports_visualization_cleaning_integration` | Visualization + Cleaning + Integration |
| 045 | `sports_visualization_cleaning_recovery` | Visualization + Cleaning + Recovery |
| 046 | `sports_visualization_cleaning_recovery_v2` | Visualization + Cleaning + Recovery (v2) |
| 047 | `sports_visualization_integration_features` | Visualization + Integration + Features |
| 048 | `sports_visualization_integration_geospatial` | Visualization + Integration + Geospatial |
| 049 | `sports_visualization_integration_recovery` | Visualization + Integration + Recovery |
| 050 | `sports_visualization_integration_recovery_v2` | Visualization + Integration + Recovery (v2) |
| 051 | `sports_visualization_integration_validation` | Visualization + Integration + Validation |
| 052 | `sports_visualization_integration_validation_v2` | Visualization + Integration + Validation (v2) |
| 053 | `sports_visualization_validation_recovery` | Visualization + Validation + Recovery |

#### 📚 Education — 1 Pipeline (#054)

| # | Pipeline | Techniques |
|---|---|---|
| 054 | `student_performance` | Student GPA analysis, at-risk prediction, study habit modeling |

#### 🚌 Transportation — 46 Pipelines (#055–#100)

Uses synthetic transit data (500–800 records, 12+ features): `trip_id`, `route`, `vehicle_type`, `departure_hour`, `distance_km`, `passengers`, `fare_amount`, `delay_minutes`, `day_of_week`, `is_holiday`, `weather_condition`, and technique-specific columns (geospatial coordinates, revenue/cost, satisfaction scores).

| Technique | # Pipelines | What It Does |
|---|---|---|
| **Cleaning** | 7 | Outlier detection, null handling, standardization patterns |
| **Prediction** | 9 | Delay prediction, cancellation risk, RandomForest classifier |
| **Regression** | 5 | Revenue forecasting, operational cost modeling |
| **Statistical** | 7 | Correlation analysis, ANOVA by route/vehicle type |
| **Visualization** | 12 | Transit dashboards, geospatial maps, rush-hour analysis |
| **Integration** | 4 | Multi-source merge patterns, schema reconciliation |
| **Clustering** | 1 | Route segmentation, peak-hour grouping |
| **Geospatial** | 6 | Origin-destination mapping, regional analysis |

Full transportation pipeline listing:

| # | Pipeline | Key Capabilities |
|---|---|---|
| 055 | `transportation_analysis` | Core analytics |
| 056 | `transportation_cleaning` | Data cleaning |
| 057 | `transportation_cleaning_integration` | Cleaning + Integration |
| 058 | `transportation_cleaning_integration_geospatial` | Cleaning + Integration + Geospatial |
| 059 | `transportation_cleaning_integration_recovery` | Cleaning + Integration + Recovery |
| 060 | `transportation_cleaning_integration_validation` | Cleaning + Integration + Validation |
| 061 | `transportation_cleaning_v2` | Cleaning (v2) |
| 062 | `transportation_cleaning_validation_features` | Cleaning + Validation + Features |
| 063 | `transportation_clustering_validation` | Clustering + Validation |
| 064 | `transportation_integration` | Integration |
| 065 | `transportation_integration_extra` | Extended integration |
| 066 | `transportation_integration_geospatial` | Geospatial integration |
| 067 | `transportation_integration_validation` | Integration + Validation |
| 068 | `transportation_prediction_cleaning` | Prediction + Cleaning |
| 069 | `transportation_prediction_cleaning_integration` | Prediction + Cleaning + Integration |
| 070 | `transportation_prediction_cleaning_validation` | Prediction + Cleaning + Validation |
| 071 | `transportation_prediction_statistical_cleaning` | Prediction + Statistical + Cleaning |
| 072 | `transportation_prediction_statistical_integration` | Prediction + Statistical + Integration |
| 073 | `transportation_prediction_validation` | Prediction + Validation |
| 074 | `transportation_prediction_validation_recovery` | Prediction + Validation + Recovery |
| 075 | `transportation_prediction_validation_v2` | Prediction + Validation (v2) |
| 076 | `transportation_prediction_visualization_geospatial` | Prediction + Visualization + Geospatial |
| 077 | `transportation_prediction_visualization_integration` | Prediction + Visualization + Integration |
| 078 | `transportation_prediction_visualization_integration_v2` | Prediction + Visualization + Integration (v2) |
| 079 | `transportation_regression` | Regression |
| 080 | `transportation_regression_cleaning_integration` | Regression + Cleaning + Integration |
| 081 | `transportation_regression_statistical_cleaning` | Regression + Statistical + Cleaning |
| 082 | `transportation_regression_statistical_integration` | Regression + Statistical + Integration |
| 083 | `transportation_regression_visualization_integration` | Regression + Visualization + Integration |
| 084 | `transportation_statistical_cleaning_integration` | Statistical + Cleaning + Integration |
| 085 | `transportation_statistical_geospatial` | Statistical + Geospatial |
| 086 | `transportation_statistical_geospatial_validation` | Statistical + Geospatial + Validation |
| 087 | `transportation_statistical_integration` | Statistical + Integration |
| 088 | `transportation_statistical_integration_v2` | Statistical + Integration (v2) |
| 089 | `transportation_statistical_visualization_integration` | Statistical + Visualization + Integration |
| 090 | `transportation_statistical_visualization_integration_v2` | Statistical + Visualization + Integration (v2) |
| 091 | `transportation_visualization` | Visualization |
| 092 | `transportation_visualization_cleaning_integration` | Visualization + Cleaning + Integration |
| 093 | `transportation_visualization_cleaning_validation` | Visualization + Cleaning + Validation |
| 094 | `transportation_visualization_cleaning_validation_v2` | Visualization + Cleaning + Validation (v2) |
| 095 | `transportation_visualization_geospatial` | Visualization + Geospatial |
| 096 | `transportation_visualization_integration` | Visualization + Integration |
| 097 | `transportation_visualization_integration_v2` | Visualization + Integration (v2) |
| 098 | `transportation_visualization_integration_validation` | Visualization + Integration + Validation |
| 099 | `transportation_visualization_recovery_reporting` | Recovery + Reporting |
| 100 | `transportation_visualization_v2` | Visualization (v2) |

---

## 🧪 What Makes This Dataset Unique?

### 1. **100% Runnable** ✅
Every single pipeline runs end-to-end with zero errors. Each ships with its own synthetic dataset — no external dependencies, no broken references, no missing files. Clone, install, and run.

### 2. **Combinatorial Technique Design** 🧩
The Category B pipelines (087 total) systematically explore every meaningful combination of 12 ML techniques: `clustering × prediction × regression × statistical × visualization × integration × cleaning × validation × geospatial × recovery × features × reporting`. This creates a combinatorially diverse training set ideal for ML models that learn pipeline composition.

### 3. **Two-Tier Architecture** 🏛️
- **Tier 1 (Category A):** 13 deep pipelines with real-world data schemas (FICO scores, medical records, HR databases, stock market data). 6–16 steps with advanced techniques like SHAP explainability, fairness audits, and cohort analysis.
- **Tier 2 (Category B):** 87 technique-varied pipelines across sports and transportation. Each pipeline name is a "menu" of techniques applied. Systematic coverage of the ML technique space.

### 4. **Self-Contained Data** 📦
Every pipeline includes its own `data/data.csv` — generated with deterministic seeds for reproducibility. Category A pipelines use realistic multi-source schemas (CSV + JSON + Excel). Category B pipelines use domain-appropriate synthetic data (player stats, transit records, student grades).

### 5. **Argo Workflows Ready** ☸️
All 100 pipelines come with `pipeline.yaml` — deploy directly to any Kubernetes cluster running Argo Workflows.

### 6. **Versioned Iterations** 🔢
Many pipelines have `_v2` through `_v5` variants — capturing the evolution of pipeline design decisions. This temporal dimension is invaluable for understanding how pipelines are refined over time.

### 7. **Documentation-First** 📝
Every pipeline has a comprehensive `pipeline.md` with: business context, data sources, architecture diagram, step-by-step descriptions, and run instructions. Total documentation: ~200,000 words across 100 files.

---

## 🏗️ Directory Structure

```
custom-pipelines/
├── 001_analytics_statistical_cleaning_integration/
│   ├── data/                       # Input dataset(s)
│   │   ├── stocks.csv              # Stock price data
│   │   └── market_indices.csv      # S&P 500, NASDAQ indices
│   ├── scripts/                    # Python scripts (6-16 per pipeline)
│   │   ├── step_01_load.py         # Data loading & profiling
│   │   ├── step_02_clean.py        # Data cleaning & standardization
│   │   ├── step_03_features.py     # Feature engineering
│   │   ├── step_04_eda.py          # EDA & visualization
│   │   ├── step_05_model.py        # Model training
│   │   └── step_06_report.py       # Final report
│   ├── pipeline.md                 # Full documentation
│   └── pipeline.yaml               # Argo Workflow definition
├── 003_credit_risk/
│   ├── data/
│   │   ├── applications.csv        # 500 loan applications
│   │   ├── credit_history.json     # 5,564 payment records
│   │   └── bureau_data.xlsx        # Credit bureau (FICO, utilization)
│   └── scripts/                    # 16 steps
│       ├── step_01_data-loading-profiling.py
│       ├── step_02_data-merging-integration.py
│       ├── ...
│       └── step_16_final-synthesis-business-recommendations.py
├── ...
├── 054_student_performance/
│   ├── data/data.csv               # 300 student records
│   └── scripts/                    # 6 steps
├── 076_transportation_prediction_visualization_geospatial/
│   ├── data/data.csv               # Transit data with geo-coordinates
│   └── scripts/                    # 6 steps
├── ...
├── 100_transportation_visualization_v2/
├── README.md
└── .gitignore
```

---

## 🚀 Quick Start

### Prerequisites

```bash
pip install pandas numpy matplotlib seaborn scikit-learn
# For advanced pipelines (003, 004, 005):
pip install xgboost lightgbm scipy
```

### Run Any Pipeline

```bash
# Pick a pipeline
cd 003_credit_risk

# Run all steps sequentially
for script in scripts/step_*.py; do
  python "$script" --data_dir data/ --output_dir output/
done

# Check outputs
ls output/
# profiling.json  cleaned.parquet  features.parquet  model.pkl
# step04_eda.png  step06_report.txt  ...
```

### Run All 100 Pipelines

```bash
# From the repo root
for pipe in */; do
  echo "Running $pipe..."
  for script in "$pipe/scripts/"*.py; do
    python "$script" --data_dir "$pipe/data/" --output_dir "$pipe/output/"
  done
done
```

### Deploy on Argo Workflows

```bash
cd 003_credit_risk
argo submit pipeline.yaml
argo watch @latest
argo logs @latest
```

---

## 🏷️ Technique Abilities Matrix

Each pipeline exercises a subset of these core **data engineering & ML abilities**:

| Ability | Description | # Pipelines |
|---|---|---|
| `cleaning` | Missing value imputation, outlier capping, standardization | 80 |
| `statistical` | Pearson correlation, t-tests, chi-square, ANOVA, effect sizes | 64 |
| `visualization` | Multi-panel dashboards, heatmaps, distribution plots | 67 |
| `prediction` | Binary/multi-class classification with RandomForest, ROC-AUC | 53 |
| `integration` | Multi-source data merging, schema reconciliation | 56 |
| `clustering` | K-Means segmentation, cluster profiling | 7 |
| `regression` | RandomForest/Linear regression, MAE, R² evaluation | 21 |
| `validation` | Schema validation, data quality checks, compliance reports | 24 |
| `recovery` | Error handling patterns, graceful degradation | 12 |
| `geospatial` | Latitude/longitude features, regional analysis | 12 |
| `features` | Domain-specific feature engineering, categorical encoding | 12 |
| `reporting` | Final synthesis, executive summaries, business recommendations | 100 |

---

## 🎯 Use Cases

| Audience | Use Case |
|---|---|
| **ML Researchers** | Study pipeline composition patterns across 87 technique variations |
| **Data Engineers** | Reference implementations of ETL patterns with multi-format data |
| **MLOps Engineers** | 100 Argo Workflow templates with best practices |
| **Data Scientists** | Domain-specific feature engineering across 10 industries |
| **Educators** | Teaching pipeline design with real-world complexity and documented examples |
| **Prompt Engineers** | Training data for automated pipeline generation from natural language |
| **Benchmark Developers** | Standardized dataset for evaluating pipeline generation systems |

---

## 📈 Dataset Statistics

```
Total Python Scripts .............. 624
Lines of Python Code .............. ~19,000+
Pipeline Documentation (MD) ....... 100 files (~200K words)
Argo Workflow Definitions ......... 100 YAML files
Input Data Files .................. 115 (CSV + JSON + XLSX)
Pipeline Steps (avg) .............. 6.4 per pipeline
Max Steps (credit_risk) ........... 16
Domain Coverage ................... 10 industries
ML Techniques Exercised ........... 12
Unique Data Schemas ............... 6 (stocks, credit, churn, supply chain, sports, transit)
```

---

## 🔍 Category A Pipeline Deep Dives

### 🔥 `003_credit_risk` — The Flagship (16 steps)
The most complex pipeline in the collection. Loads 3 data sources → merges credit history + bureau data → cleans & validates → engineers 10 risk features → runs EDA with FICO/DTI heatmaps → creates risk profile dashboards → performs 3 hypothesis tests → preprocesses for ML → trains baseline models (LR, RF, LightGBM) → trains advanced ensemble (XGBoost + Stacking) → evaluates with threshold optimization → generates SHAP explanations → audits fairness (disparate impact, statistical parity) → produces final business report with risk tiers and monitoring plan.

**Outputs:** 7 PNG visualizations, 9 JSON reports, 3 trained models (.pkl), 1 final report (.txt)

### 📊 `004_customer_churn` — Retention Analytics (16 steps)
Analyzes 500 customers with 15,843 transactions. Aggregates purchase behavior → engineers RFM scores → visualizes churn patterns by segment → performs survival analysis → creates monthly retention cohorts → trains multi-model ensemble → calculates ROI at different thresholds → clusters at-risk customers for personalized retention strategies.

### 📦 `005_demand_forecasting` — Supply Chain (10 steps)
Forecasts demand for 50 SKUs across 4 regions. Decomposes time series for seasonal patterns → engineers temporal features (lags, rolling windows) → trains RandomForest regressor → optimizes safety stock with 95% service level → simulates 4 what-if scenarios (demand surge, supply disruption, economic downturn).

---

## 🤝 Contributing

This is a curated research dataset. To suggest additions or improvements:

1. Fork the repository
2. Add your pipeline following the standard directory structure:
   - `data/data.csv` or domain-specific files
   - `scripts/step_01_load.py` through `step_06_report.py`
   - `pipeline.md` with business context
   - `pipeline.yaml` for Argo
3. Ensure all scripts run end-to-end: `for f in scripts/*.py; do python "$f" --data_dir data/ --output_dir output/; done`
4. Submit a PR

---

## 📄 License

This dataset is released for research and educational purposes. See individual pipeline `pipeline.md` files for specific details.

---

## 👤 Author

**Alidu Abubakari**  
GitHub: [@aliduabubakari](https://github.com/aliduabubakari)  
Repository: [custom-pipelines](https://github.com/aliduabubakari/custom-pipelines)

---

<p align="center">
  <strong>100 pipelines. 10 domains. 12 techniques. 624 scripts.</strong><br>
  <em>Every single one runs. Every single one tells a story. 🔬</em>
</p>
