# E-Commerce: Product Recommendation & Customer Analytics

## Metadata
| Field | Value |
|---|---|
| **Pipeline ID** | `ecommerce_recommendation` |
| **Domain** | E-Commerce / Retail |
| **Total Steps** | 6 |
| **Input Files** | 3 |
| **Pipeline Type** | ML Pipeline (End-to-End) |

---

## Executive Summary

Builds a product recommendation engine using customer segments, order history, and product catalog attributes. Applies K-Means clustering to identify customer segments and uses RandomForest classification to predict purchase patterns.

---

## Business Context & Need

E-commerce platforms lose 35% of potential revenue from poor product discovery. Personalized recommendations drive 20-30% of Amazon's revenue. An ML recommendation system increases average order value by 15-25%, conversion rates by 10%, and customer retention by 20%.

---

## Data Sources

- **`customers.csv`** — Customer profiles (500 customers, 7 columns)
- **`products.csv`** — Product catalog (200 products, 8 columns)
- **`orders.json`** — Order history (11,436 transactions, 7 columns)

---

## Pipeline Architecture

```
  Input Data ──▶ [Step 1: Data Loading & Profiling]
                  │
                  ▼
               [Step 2: Data Cleaning & Standardizatio]
                  │
                  ▼
               [Step 3: Feature Engineering]
                  │
                  ▼
               [Step 4: Exploratory Data Analysis & Vis]
                  │
                  ▼
               [Step 5: Model Training: Clustering]
                  │
                  ▼
               [Step 6: Final Synthesis & Report] ──▶ Final Output
```

---

## Step Details

### Step 1: Data Loading & Profiling
**Description:** Load customers CSV, products CSV, and orders JSON. Profile each dataset for row counts, column types, null percentages, and basic statistics.
**Script:** `scripts/step_01_load.py`

### Step 2: Data Cleaning & Standardization
**Description:** Handle missing values (median for numerical, 'Unknown' for categorical). Cap outliers at 99th percentile. Standardize categorical values.
**Script:** `scripts/step_02_clean.py`

### Step 3: Feature Engineering
**Description:** Create derived features: price tiers (Budget/Standard/Premium/Luxury/Ultra) and rating tiers (Low/Medium/High) for product categorization.
**Script:** `scripts/step_03_features.py`

### Step 4: Exploratory Data Analysis & Visualization
**Description:** Generate multi-panel EDA dashboard with distribution histograms, correlation analysis, and segment patterns.
**Script:** `scripts/step_04_eda.py`

### Step 5: Model Training
**Description:** Apply K-Means clustering to segment customers into 3 groups. Train RandomForest classifier on cluster labels for recommendation patterns.
**Script:** `scripts/step_05_model.py`

### Step 6: Final Report
**Description:** Compile final synthesis with key findings, cluster profiles, and business recommendations for recommendation strategies.
**Script:** `scripts/step_06_report.py`

---


## How to Run

### Local Execution
```bash
cd 006_ecommerce_recommendation
pip install pandas numpy matplotlib seaborn scikit-learn

for script in scripts/step_*.py; do
  python "$script" --data_dir data/ --output_dir output/
done
```

### Argo Workflow
```bash
argo submit 006_ecommerce_recommendation/pipeline.yaml
argo watch @latest
argo logs @latest
```
