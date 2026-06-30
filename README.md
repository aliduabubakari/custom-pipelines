# 🚀 Custom Pipelines — _100 Production-Ready ML Data Pipelines_

<p align="center">
  <img src="https://img.shields.io/badge/Pipelines-100-blue?style=for-the-badge" alt="100 Pipelines"/>
  <img src="https://img.shields.io/badge/Scripts-800+-orange?style=for-the-badge" alt="800+ Scripts"/>
  <img src="https://img.shields.io/badge/Domains-12-purple?style=for-the-badge" alt="12 Domains"/>
  <img src="https://img.shields.io/badge/Visualizations-592-9cf?style=for-the-badge" alt="592 Visualizations"/>
  <img src="https://img.shields.io/badge/Argo_Ready-✓-green?style=for-the-badge" alt="Argo Ready"/>
</p>

<p align="center">
  <em>A comprehensive collection of end-to-end ML data pipelines spanning finance, healthcare, sports analytics, transportation, HR, energy, e-commerce, and more. Each pipeline is self-contained, reproducible, and ready to deploy on <strong>Argo Workflows</strong>.</em>
</p>

---

## 📊 By the Numbers

| Metric | Count |
|---|---|
| **Total Pipelines** | 100 |
| **Total Python Scripts** | 800+ |
| **Pipeline Documentation (`.md`)** | 100 |
| **Argo Workflow Definitions (`.yaml`)** | 100 |
| **Data Generation Scripts** | 100 |
| **Generated Visualizations** | 592 |
| **Sample Datasets (CSV)** | 140 |
| **Processed Output Files** | 126 `.parquet` |
| **Pipeline Steps per Pipeline** | 8–16 |

---

## 🗺️ Domain Landscape

The 100 pipelines span **12 business domains**, offering a rich tapestry of real-world data challenges:

| Domain | # Pipelines | Highlights |
|---|---|---|
| 🏦 **Finance** | 3 | Credit risk scoring, fraud detection, loan default prediction |
| 👔 **HR & People Analytics** | 3 | Employee attrition, regression visualization, validation workflows |
| 🏥 **Healthcare** | 2 | Hospital readmission prediction, insurance claims analysis |
| ⚡ **Energy & Utilities** | 1 | Energy consumption forecasting |
| 🛒 **E-commerce** | 1 | Product recommendation engine |
| 📦 **Manufacturing** | 1 | Predictive maintenance scheduling |
| 📞 **Telecom** | 1 | Customer churn prediction |
| 📈 **Demand Planning** | 1 | Demand forecasting models |
| 🎓 **Education** | 1 | Student performance analytics |
| ⚽ **Sports Analytics** | 40 | Clustering, prediction, regression, statistical & visualization pipelines |
| 🚌 **Transportation** | 45 | Transit analytics, geospatial, cleaning, prediction, regression |
| 📊 **General Analytics** | 2 | Statistical cleaning & integration patterns |

---

## 🔬 Anatomy of a Pipeline

Every pipeline follows a standardized 8–16 step architecture:

```
  ┌─────────────────┐
  │  generate_data  │ ── Synthetic data generation (ships with each pipeline)
  └────────┬────────┘
           ▼
  ┌─────────────────┐
  │ Step 1: LOAD    │ ── Data ingestion from CSV/JSON/Excel + initial profiling
  └────────┬────────┘
           ▼
  ┌─────────────────┐
  │ Step 2: CLEAN   │ ── Missing value handling, outlier capping, standardization
  └────────┬────────┘
           ▼
  ┌─────────────────┐
  │ Step 3: EDA     │ ── Correlation matrices, distribution analysis, VIF detection
  └────────┬────────┘
           ▼
  ┌─────────────────┐
  │ Step 4: STATS   │ ── Hypothesis tests (t-test, chi-square, ANOVA), effect sizes
  └────────┬────────┘
           ▼
  ┌─────────────────┐
  │ Step 5: VIZ     │ ── Multi-panel dashboards, heatmaps, geospatial choropleths
  └────────┬────────┘
           ▼
  ┌─────────────────┐
  │ Step 6: MODEL   │ ── LogisticRegression, RandomForest, XGBoost, LightGBM, Optuna tuning
  └────────┬────────┘
           ▼
  ┌─────────────────┐
  │ Step 7: EVAL    │ ── ROC-AUC, Precision-Recall, confusion matrix, threshold optimization
  └────────┬────────┘
           ▼
  ┌─────────────────┐
  │ Step 8: REPORT  │ ── Final synthesis, business recommendations, model cards
  └─────────────────┘
```

**Complex pipelines** (16 steps) additionally include: data merging & integration, advanced feature engineering, model explainability (SHAP/LIME), fairness audits, and compliance validation.

---

## 📂 Complete Pipeline Catalog

### Finance & Risk (#001–#012)

| # | Pipeline | Description |
|---|---|---|
| 001 | `analytics_statistical_cleaning_integration` | Statistical cleaning with multi-source integration |
| 002 | `analytics_statistical_integration` | Statistical analysis on integrated datasets |
| 003 | `credit_risk` | 🔥 Full credit risk scoring: FICO analysis, ensemble models, SHAP explainability, fairness audit |
| 004 | `customer_churn` | Telecom churn prediction with survival analysis |
| 005 | `demand_forecasting` | Time-series demand forecasting with seasonal decomposition |
| 006 | `ecommerce_recommendation` | Collaborative filtering & content-based product recommendations |
| 007 | `employee_attrition` | HR attrition prediction with engagement survey integration |
| 008 | `energy_forecasting` | Energy consumption forecasting with weather covariates |
| 009 | `healthcare_readmission` | Patient readmission risk with clinical feature engineering |
| 010 | `hr_regression_visualization_integration` | HR regression modeling with visualization dashboards |
| 011 | `hr_visualization_integration_validation` | HR analytics with integrated validation workflows |
| 012 | `insurance_claims` | Claims severity prediction & fraud indicator detection |
| 013 | `predictive_maintenance` | Equipment failure prediction with sensor data |

---

### ⚽ Sports Analytics (#014–#053)

_A deep exploration of sports data through 40 distinct pipelines, systematically varying analytical techniques._

| # | Pipeline | Techniques |
|---|---|---|
| 014 | `sports_clustering_integration_validation` | Clustering + Integration + Validation |
| 015 | `sports_clustering_prediction_statistical` | Clustering → Prediction → Statistical tests |
| 016 | `sports_clustering_prediction_visualization` | Clustering → Prediction → Visualization |
| 017 | `sports_clustering_statistical_visualization` | Clustering + Statistical + Visualization |
| 018 | `sports_clustering_visualization_integration` | Clustering + Visualization + Integration |
| 019 | `sports_prediction_cleaning_integration` | Prediction-focused pipeline with cleaning & integration |
| 020 | `sports_prediction_statistical_visualization` | Prediction → Stats → Viz |
| 021 | `sports_prediction_statistical_visualization_v2` | v2 — refined model selection |
| 022 | `sports_prediction_visualization_cleaning` | Prediction + Visualization + Cleaning |
| 023 | `sports_regression_clustering_visualization` | Regression + Clustering + Visualization trifecta |
| 024 | `sports_regression_prediction_statistical` | Regression → Prediction → Statistical inference |
| 025 | `sports_regression_prediction_statistical_v2` | v2 — with interaction features |
| 026 | `sports_regression_prediction_statistical_v3` | v3 — advanced regularization |
| 027 | `sports_regression_prediction_visualization` | Regression → Prediction → Viz |
| 028 | `sports_regression_prediction_visualization_v2` | v2 — interactive dashboard outputs |
| 029 | `sports_regression_statistical_visualization` | Regression + Stats + Viz |
| 030 | `sports_statistical_cleaning` | Pure statistical analysis with cleaning |
| 031 | `sports_statistical_cleaning_integration` | Stats + Cleaning + Integration |
| 032–035 | `sports_statistical_cleaning_integration_v2`–`v5` | Iterative refinements across 4 versions |
| 036 | `sports_statistical_cleaning_validation` | Statistical analysis with cleaning & validation |
| 037 | `sports_statistical_integration` | Statistical integration pipeline |
| 038 | `sports_statistical_integration_v2` | v2 — improved schema inference |
| 039 | `sports_statistical_visualization_cleaning` | Stats + Viz + Cleaning |
| 040 | `sports_statistical_visualization_cleaning_v2` | v2 — enhanced chart styling |
| 041 | `sports_statistical_visualization_integration` | Stats + Viz + Integration |
| 042 | `sports_validation_recovery` | Validation & error recovery patterns |
| 043 | `sports_visualization` | Pure visualization pipeline |
| 044 | `sports_visualization_cleaning_integration` | Viz + Cleaning + Integration |
| 045 | `sports_visualization_cleaning_recovery` | Viz + Cleaning + Recovery |
| 046 | `sports_visualization_cleaning_recovery_v2` | v2 — improved error handling |
| 047 | `sports_visualization_integration_features` | Feature-rich visualization integration |
| 048 | `sports_visualization_integration_geospatial` | Geospatial visualization integration |
| 049 | `sports_visualization_integration_recovery` | Integration + Recovery workflows |
| 050 | `sports_visualization_integration_recovery_v2` | v2 — with checkpointing |
| 051 | `sports_visualization_integration_validation` | Viz + Integration + Validation |
| 052 | `sports_visualization_integration_validation_v2` | v2 — strict schema validation |
| 053 | `sports_visualization_validation_recovery` | Viz + Validation + Recovery |

---

### 🚌 Transportation (#054–#100)

_Comprehensive transit & logistics pipelines with geospatial enrichment._

| # | Pipeline | Key Capabilities |
|---|---|---|
| 054 | `student_performance` | Academic performance prediction |
| 055 | `transportation_analysis` | Core transportation analytics |
| 056 | `transportation_cleaning` | Data cleaning pipeline |
| 057 | `transportation_cleaning_integration` | Cleaning + Integration |
| 058 | `transportation_cleaning_integration_geospatial` | Cleaning + Integration + Geospatial |
| 059 | `transportation_cleaning_integration_recovery` | Cleaning + Integration + Recovery |
| 060 | `transportation_cleaning_integration_validation` | Cleaning + Integration + Validation |
| 061 | `transportation_cleaning_v2` | v2 — enhanced cleaning rules |
| 062 | `transportation_cleaning_validation_features` | Cleaning + Validation + Features |
| 063 | `transportation_clustering_validation` | Clustering with validation |
| 064 | `transportation_integration` | Multi-table integration |
| 065 | `transportation_integration_extra` | Extended integration with profiling |
| 066 | `transportation_integration_geospatial` | Geospatial integration |
| 067 | `transportation_integration_validation` | Integration + Validation |
| 068 | `transportation_prediction_cleaning` | Prediction + Cleaning |
| 069 | `transportation_prediction_cleaning_integration` | Prediction + Cleaning + Integration |
| 070 | `transportation_prediction_cleaning_validation` | Prediction + Cleaning + Validation |
| 071 | `transportation_prediction_statistical_cleaning` | Prediction + Stats + Cleaning |
| 072 | `transportation_prediction_statistical_integration` | Prediction + Stats + Integration |
| 073 | `transportation_prediction_validation` | Prediction + Validation |
| 074 | `transportation_prediction_validation_recovery` | Prediction + Validation + Recovery |
| 075 | `transportation_prediction_validation_v2` | v2 — with calibration |
| 076 | `transportation_prediction_visualization_geospatial` | Prediction + Viz + Geospatial |
| 077 | `transportation_prediction_visualization_integration` | Prediction + Viz + Integration |
| 078 | `transportation_prediction_visualization_integration_v2` | v2 — map overlays |
| 079 | `transportation_regression` | Pure regression pipeline |
| 080 | `transportation_regression_cleaning_integration` | Regression + Cleaning + Integration |
| 081 | `transportation_regression_statistical_cleaning` | Regression + Stats + Cleaning |
| 082 | `transportation_regression_statistical_integration` | Regression + Stats + Integration |
| 083 | `transportation_regression_visualization_integration` | Regression + Viz + Integration |
| 084 | `transportation_statistical_cleaning_integration` | Stats + Cleaning + Integration |
| 085 | `transportation_statistical_geospatial` | Statistical analysis with geospatial |
| 086 | `transportation_statistical_geospatial_validation` | Stats + Geospatial + Validation |
| 087 | `transportation_statistical_integration` | Statistical integration |
| 088 | `transportation_statistical_integration_v2` | v2 — with bootstrapping |
| 089 | `transportation_statistical_visualization_integration` | Stats + Viz + Integration |
| 090 | `transportation_statistical_visualization_integration_v2` | v2 — enhanced visualizations |
| 091 | `transportation_visualization` | Pure visualization |
| 092 | `transportation_visualization_cleaning_integration` | Viz + Cleaning + Integration |
| 093 | `transportation_visualization_cleaning_validation` | Viz + Cleaning + Validation |
| 094 | `transportation_visualization_cleaning_validation_v2` | v2 — with anomaly detection |
| 095 | `transportation_visualization_geospatial` | Geospatial visualization |
| 096 | `transportation_visualization_integration` | Viz + Integration |
| 097 | `transportation_visualization_integration_v2` | v2 — interactive outputs |
| 098 | `transportation_visualization_integration_validation` | Viz + Integration + Validation |
| 099 | `transportation_visualization_recovery_reporting` | Recovery & reporting |
| 100 | `transportation_visualization_v2` | v2 — final visualization pipeline |

---

## 🧪 What Makes This Dataset Unique?

### 1. **Combinatorial Pipeline Design** 🧩
The sports and transportation sections systematically explore every meaningful combination of analytical techniques: clustering × prediction × regression × statistical testing × visualization × integration × cleaning × validation × geospatial enrichment. This creates a **combinatorially diverse training set** ideal for ML models that learn pipeline composition.

### 2. **Self-Contained & Reproducible** ♻️
Every pipeline includes its own `generate_data.py` script — a synthetic data generator that creates realistic datasets on-the-fly. No external data dependencies. Just run and go.

### 3. **Argo-Workflows Ready** ☸️
All 100 pipelines come with `pipeline.yaml` — production-grade Argo Workflow definitions. Deploy directly to any Kubernetes cluster running Argo.

### 4. **Multi-Format Input Handling** 📥
Pipelines read from CSV, JSON, Excel (`.xlsx`), and plain text — simulating real-world data heterogeneity.

### 5. **Versioned Iterations** 🔢
Many pipelines have `_v2`, `_v3`, `_v4`, `_v5` variants — revealing the **evolution of pipeline design decisions** over time. This temporal dimension is invaluable for understanding pipeline optimization patterns.

---

## 🏗️ Directory Structure

```
custom-pipelines/
├── 001_analytics_statistical_cleaning_integration/
│   ├── data/                    # Input datasets (CSV/JSON/XLSX)
│   ├── scripts/                 # Step-by-step Python scripts (8-16 files)
│   │   ├── step_01_load.py
│   │   ├── step_02_clean.py
│   │   ├── step_03_eda.py
│   │   ├── step_04_stats.py
│   │   ├── step_05_viz.py
│   │   ├── step_06_model.py
│   │   ├── step_07_eval.py
│   │   └── step_08_report.py
│   ├── output/                  # Generated artifacts (parquet, png, json, joblib)
│   ├── pipeline.md              # Full documentation with business context
│   ├── pipeline.yaml            # Argo Workflow definition
│   └── generate_data.py         # Synthetic data generator
├── 002_analytics_statistical_integration/
├── ...
└── 100_transportation_visualization_v2/
```

---

## 🚀 Quick Start

### Prerequisites

```bash
pip install pandas numpy matplotlib seaborn scikit-learn openpyxl pyarrow
# For advanced pipelines:
pip install xgboost lightgbm optuna shap
```

### Run Any Pipeline Locally

```bash
cd 003_credit_risk

# Generate sample data
python generate_data.py

# Execute all 16 steps sequentially
python scripts/step_01_data-loading-profiling.py --data_dir data/ --output_dir output/
python scripts/step_02_data-merging-integration.py --data_dir data/ --output_dir output/
# ... continue through step_16

# Or run all steps at once:
for script in scripts/step_*.py; do
  python "$script" --data_dir data/ --output_dir output/
done
```

### Deploy on Argo Workflows

```bash
cd 003_credit_risk
argo submit pipeline.yaml
argo watch @latest
argo logs @latest
```

### Explore Outputs

Each pipeline's `output/` directory contains:
- 📊 **Visualizations** — PNG charts, heatmaps, dashboards
- 📄 **Reports** — JSON summaries, model results, profiling reports
- 🤖 **Models** — Trained `.joblib` files (for complex pipelines)
- 📦 **Processed Data** — Cleaned `.parquet` files ready for downstream use

---

## 🎯 Use Cases

This collection is designed for:

| Audience | Use Case |
|---|---|
| **ML Researchers** | Benchmark pipeline generation, study pipeline composition patterns |
| **Data Engineers** | Reference implementations of ETL/ELT patterns across domains |
| **MLOps Engineers** | Production-ready Argo Workflow templates with best practices |
| **Data Scientists** | Domain-specific feature engineering and modeling strategies |
| **Educators** | Teaching data pipeline design with real-world complexity |
| **Prompt Engineers** | Training data for automated pipeline generation from natural language |

---

## 🏷️ Pipeline Abilities Matrix

Each pipeline exercises a subset of these core **data engineering & ML abilities**:

| Ability | Description | Present In |
|---|---|---|
| `cleaning` | Missing value imputation, outlier handling, standardization | 70+ pipelines |
| `statistical` | Hypothesis testing, effect sizes, distribution analysis | 60+ pipelines |
| `visualization` | Chart generation, dashboards, geospatial maps | 65+ pipelines |
| `prediction` | ML model training (classification/regression) | 50+ pipelines |
| `integration` | Multi-source data merging & schema reconciliation | 55+ pipelines |
| `clustering` | K-means, hierarchical, DBSCAN segmentation | 10+ pipelines |
| `regression` | Linear/logistic regression with diagnostics | 20+ pipelines |
| `validation` | Schema validation, data quality checks, compliance | 25+ pipelines |
| `recovery` | Error handling, checkpointing, graceful degradation | 12+ pipelines |
| `geospatial` | Geo-enrichment, choropleth maps, spatial joins | 12+ pipelines |
| `features` | Feature engineering, encoding, selection | 15+ pipelines |
| `reporting` | Final synthesis, executive summaries, model cards | 15+ pipelines |

---

## 📈 Dataset Statistics

```
Total Python Scripts .............. 800
Lines of Python Code .............. ~45,000+
Pipeline Documentation (MD) ....... 100 files (~500K words)
Argo Workflow Definitions ......... 100 YAML files
Generated Visualizations .......... 592 PNG images
Sample Datasets (CSV/JSON/XLSX) ... 140 files
Pipeline Steps (avg) .............. 10.2 per pipeline
Max Steps (complex pipelines) ..... 16
Domain Coverage ................... 12 industries
```

---

## 🤝 Contributing

This is a curated research dataset. To suggest additions or improvements:

1. Fork the repository
2. Add your pipeline following the standard directory structure
3. Ensure `generate_data.py` produces reproducible synthetic data
4. Submit a PR with a `pipeline.md` describing business context

---

## 📄 License

This dataset is released for research and educational purposes. See individual pipeline `pipeline.md` files for specific attribution.

---

## 👤 Author

**Alidu Abubakari**  
GitHub: [@aliduabubakari](https://github.com/aliduabubakari)

---

<p align="center">
  <em>100 pipelines. 12 domains. 800 scripts. Infinite possibilities.</em> 🔬
</p>
