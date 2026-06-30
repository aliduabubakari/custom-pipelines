#!/usr/bin/env python3
"""Batch writer for pipeline scripts."""
import os, sys

def write_script(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content)
    print(f"  ✓ {os.path.basename(path)}")

# ============================================================================
# EMPLOYEE ATTRITION — 16 scripts
# ============================================================================
BASE = "employee_attrition/scripts"

write_script(f"{BASE}/step_01_data-loading-profiling.py", '''#!/usr/bin/env python3
import argparse, os, json
import pandas as pd, numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--data_dir", default="../data")
    p.add_argument("--output_dir", default=".")
    args = p.parse_args()
    os.makedirs(args.output_dir, exist_ok=True)
    print("STEP 1: Data Loading & Profiling")

    emp = pd.read_csv(os.path.join(args.data_dir, "employees.csv"))
    with open(os.path.join(args.data_dir, "engagement_surveys.json")) as f:
        surveys = pd.DataFrame(json.load(f))
    reviews = pd.read_excel(os.path.join(args.data_dir, "performance_reviews.xlsx"))

    print(f"Employees: {len(emp)}, Surveys: {len(surveys)}, Reviews: {len(reviews)}")
    print(f"Attrition: {emp['is_attrited'].mean()*100:.1f}%")
    print(f"Dept dist:\\n{emp['department'].value_counts().to_string()}")
    print(f"Nulls:\\n{emp.isnull().sum().to_string()}")

    # Save profiling
    with open(os.path.join(args.output_dir, "profiling_summary.json"), "w") as f:
        json.dump({"n_employees": len(emp), "attrition_rate": round(emp["is_attrited"].mean(), 4)}, f)

    # Viz
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    emp.groupby("department")["is_attrited"].mean().sort_values().plot(kind="barh", ax=axes[0], color="#e74c3c")
    axes[0].set_title("Attrition by Department")
    emp["tenure_days"].hist(bins=30, ax=axes[1], color="#3498db")
    axes[1].set_title("Tenure Distribution")
    plt.tight_layout(); fig.savefig(os.path.join(args.output_dir, "step01_profiling.png"), dpi=100); plt.close()
    print("Done")
if __name__ == "__main__": main()
''')

write_script(f"{BASE}/step_02_data-aggregation--surveys.py", '''#!/usr/bin/env python3
import argparse, os, json
import pandas as pd, numpy as np

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--data_dir", default="../data")
    p.add_argument("--output_dir", default=".")
    args = p.parse_args()
    os.makedirs(args.output_dir, exist_ok=True)
    print("STEP 2: Data Aggregation — Surveys")

    with open(os.path.join(args.data_dir, "engagement_surveys.json")) as f:
        surveys = pd.DataFrame(json.load(f))

    if len(surveys) > 0:
        agg = surveys.groupby("employee_id").agg(
            avg_engagement=("engagement_score", "mean"),
            avg_satisfaction=("satisfaction_score", "mean"),
            avg_manager_score=("manager_score", "mean"),
            avg_career_growth=("career_growth_score", "mean"),
            avg_work_env=("work_env_score", "mean"),
            n_surveys=("survey_date", "count"),
        ).reset_index()
    else:
        agg = pd.DataFrame(columns=["employee_id"])
    agg.to_parquet(os.path.join(args.output_dir, "survey_agg.parquet"), index=False)
    print(f"Aggregated {len(agg)} employees with surveys")
if __name__ == "__main__": main()
''')

write_script(f"{BASE}/step_03_data-aggregation--performance.py", '''#!/usr/bin/env python3
import argparse, os
import pandas as pd, numpy as np

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--data_dir", default="../data")
    p.add_argument("--output_dir", default=".")
    args = p.parse_args()
    os.makedirs(args.output_dir, exist_ok=True)
    print("STEP 3: Data Aggregation — Performance")

    reviews = pd.read_excel(os.path.join(args.data_dir, "performance_reviews.xlsx"))
    if len(reviews) > 0:
        agg = reviews.groupby("employee_id").agg(
            avg_performance=("performance_score", "mean"),
            avg_goal_achievement=("goal_achievement_pct", "mean"),
            avg_peer_feedback=("peer_feedback_score", "mean"),
            avg_manager_rating=("manager_rating", "mean"),
            total_promotions=("promotion_recommended", "sum"),
            n_reviews=("review_year", "count"),
        ).reset_index()
    else:
        agg = pd.DataFrame(columns=["employee_id"])
    agg.to_parquet(os.path.join(args.output_dir, "review_agg.parquet"), index=False)
    print(f"Aggregated {len(agg)} employees with reviews")
if __name__ == "__main__": main()
''')

write_script(f"{BASE}/step_04_data-merging-integration.py", '''#!/usr/bin/env python3
import argparse, os
import pandas as pd, numpy as np

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--data_dir", default="../data")
    p.add_argument("--output_dir", default=".")
    args = p.parse_args()
    os.makedirs(args.output_dir, exist_ok=True)
    print("STEP 4: Merging & Integration")

    emp = pd.read_csv(os.path.join(args.data_dir, "employees.csv"))
    surveys = pd.read_parquet(os.path.join(args.output_dir, "survey_agg.parquet"))
    reviews = pd.read_parquet(os.path.join(args.output_dir, "review_agg.parquet"))

    df = emp.merge(surveys, on="employee_id", how="left").merge(reviews, on="employee_id", how="left")
    print(f"Merged: {len(df)} employees, {len(df.columns)} cols")
    df.to_parquet(os.path.join(args.output_dir, "unified_employees.parquet"), index=False)
    print("Done")
if __name__ == "__main__": main()
''')

write_script(f"{BASE}/step_05_data-cleaning-standardization.py", '''#!/usr/bin/env python3
import argparse, os
import pandas as pd, numpy as np

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--data_dir", default="../data")
    p.add_argument("--output_dir", default=".")
    args = p.parse_args()
    os.makedirs(args.output_dir, exist_ok=True)
    print("STEP 5: Data Cleaning")

    df = pd.read_parquet(os.path.join(args.output_dir, "unified_employees.parquet"))
    # Fill missing survey/review aggregates
    for col in df.columns:
        if col.startswith("avg_") or col.startswith("total_"):
            df[col] = df[col].fillna(df[col].median() if df[col].dtype in ('float64','int64') else 0)
        if col in ("n_surveys", "n_reviews"):
            df[col] = df[col].fillna(0).astype(int)
    df["is_attrited"] = df["is_attrited"].astype(int)
    print(f"Cleaned: {len(df)} rows, nulls: {df.isnull().sum().sum()}")
    df.to_parquet(os.path.join(args.output_dir, "cleaned_employees.parquet"), index=False)
    print("Done")
if __name__ == "__main__": main()
''')

write_script(f"{BASE}/step_06_feature-engineering.py", '''#!/usr/bin/env python3
import argparse, os
import pandas as pd, numpy as np

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--data_dir", default="../data")
    p.add_argument("--output_dir", default=".")
    args = p.parse_args()
    os.makedirs(args.output_dir, exist_ok=True)
    print("STEP 6: Feature Engineering")

    df = pd.read_parquet(os.path.join(args.output_dir, "cleaned_employees.parquet"))
    # Engagement composite
    df["engagement_composite"] = df[["avg_engagement", "avg_satisfaction", "avg_work_env"]].mean(axis=1)
    # Tenure years
    df["tenure_years"] = df["tenure_days"] / 365.25
    # Salary to tenure ratio
    df["salary_per_year"] = df["monthly_salary"] * 12 / (df["tenure_years"] + 1)
    # Commute stress
    df["commute_stress"] = pd.cut(df["commute_miles"], bins=[0,5,15,30,100], labels=[1,2,3,4]).astype(int)
    # Promotion rate
    df["promotion_rate"] = df["total_promotions"] / (df["tenure_years"] + 1)
    # Risk indicators
    df["low_engagement_flag"] = (df["avg_engagement"] < 3).astype(int)
    df["low_satisfaction_flag"] = (df["avg_satisfaction"] < 3).astype(int)
    df["high_commute_flag"] = (df["commute_miles"] > 20).astype(int)
    df["risk_score"] = df["low_engagement_flag"] + df["low_satisfaction_flag"] + df["high_commute_flag"] + df["overtime"]

    print(f"Features: {len(df.columns)} columns")
    df.to_parquet(os.path.join(args.output_dir, "features.parquet"), index=False)
    print("Done")
if __name__ == "__main__": main()
''')

write_script(f"{BASE}/step_07_data-validation-quality-report.py", '''#!/usr/bin/env python3
import argparse, os, json
import pandas as pd, numpy as np

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--data_dir", default="../data")
    p.add_argument("--output_dir", default=".")
    args = p.parse_args()
    os.makedirs(args.output_dir, exist_ok=True)
    print("STEP 7: Data Validation")

    df = pd.read_parquet(os.path.join(args.output_dir, "features.parquet"))
    report = {
        "rows": len(df),
        "nulls": int(df.isnull().sum().sum()),
        "attrition_rate": round(float(df["is_attrited"].mean()), 4),
        "dept_count": int(df["department"].nunique()),
        "duplicate_ids": int(df["employee_id"].duplicated().sum()),
    }
    with open(os.path.join(args.output_dir, "validation_report.json"), "w") as f:
        json.dump(report, f, indent=2)
    print(f"Validation: {json.dumps(report, indent=2)}")
    print("Done")
if __name__ == "__main__": main()
''')

write_script(f"{BASE}/step_08_exploratory-data-analysis.py", '''#!/usr/bin/env python3
import argparse, os, json
import pandas as pd, numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
plt.style.use('seaborn-v0_8-darkgrid')

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--data_dir", default="../data")
    p.add_argument("--output_dir", default=".")
    args = p.parse_args()
    os.makedirs(args.output_dir, exist_ok=True)
    print("STEP 8: EDA")

    df = pd.read_parquet(os.path.join(args.output_dir, "features.parquet"))
    results = {}
    for col in ["department", "job_role", "education", "gender", "location"]:
        if col in df.columns:
            grp = df.groupby(col)["is_attrited"].mean().round(4)
            results[f"attrition_by_{col}"] = grp.to_dict()
            print(f"\\n{col}:\\n{grp.to_string()}")

    nums = df.select_dtypes(include=[np.number])
    corr = nums.corr()["is_attrited"].sort_values(key=abs, ascending=False).drop("is_attrited")
    print(f"\\nTop correlations:\\n{corr.head(8).to_string()}")
    results["top_correlations"] = corr.head(8).to_dict()
    with open(os.path.join(args.output_dir, "eda_insights.json"), "w") as f: json.dump(results, f, indent=2)

    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    df.groupby("department")["is_attrited"].mean().sort_values().plot(kind="barh", ax=axes[0], color="#e74c3c")
    axes[0].set_title("Attrition by Dept")
    df.boxplot(column="monthly_salary", by="is_attrited", ax=axes[1])
    axes[1].set_title("Salary by Attrition")
    df.boxplot(column="tenure_days", by="is_attrited", ax=axes[2])
    axes[2].set_title("Tenure by Attrition")
    plt.tight_layout(); fig.savefig(os.path.join(args.output_dir, "step08_eda.png"), dpi=100); plt.close()
    print("Done")
if __name__ == "__main__": main()
''')

write_script(f"{BASE}/step_09_data-visualization--attrition-patterns.py", '''#!/usr/bin/env python3
import argparse, os
import pandas as pd, numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
plt.style.use('seaborn-v0_8-darkgrid')

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--data_dir", default="../data")
    p.add_argument("--output_dir", default=".")
    args = p.parse_args()
    os.makedirs(args.output_dir, exist_ok=True)
    print("STEP 9: Attrition Patterns Visualization")

    df = pd.read_parquet(os.path.join(args.output_dir, "features.parquet"))
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))

    # 1. Attrition by department
    df.groupby("department")["is_attrited"].mean().sort_values().plot(kind="barh", ax=axes[0,0], color="#e74c3c")
    axes[0,0].set_title("Attrition % by Department")

    # 2. Overtime vs attrition
    ot = df.groupby("overtime")["is_attrited"].mean()*100
    ot.plot(kind="bar", ax=axes[0,1], color=["#2ecc71","#e74c3c"])
    axes[0,1].set_title("Attrition by Overtime")

    # 3. Satisfaction vs attrition scatter
    sample = df.sample(min(300, len(df)))
    axes[0,2].scatter(sample["avg_satisfaction"], sample["avg_engagement"], c=sample["is_attrited"], cmap="coolwarm", alpha=0.6)
    axes[0,2].set_title("Satisfaction vs Engagement")

    # 4. Tenure histogram by attrition
    for label, color in [(0,"#2ecc71"),(1,"#e74c3c")]:
        df[df["is_attrited"]==label]["tenure_days"].hist(bins=25, ax=axes[1,0], alpha=0.5, color=color, label=["Retained","Attrited"][label])
    axes[1,0].set_title("Tenure Distribution"); axes[1,0].legend()

    # 5. Job satisfaction by role
    df.pivot_table(values="is_attrited", index="job_role", aggfunc="mean").sort_values("is_attrited").tail(8).plot(kind="barh", ax=axes[1,1], color="#9b59b6", legend=False)
    axes[1,1].set_title("Top Attrition Roles")

    # 6. Commute vs attrition
    df["commute_bin"] = pd.cut(df["commute_miles"], bins=5)
    df.groupby("commute_bin", observed=False)["is_attrited"].mean().plot(kind="bar", ax=axes[1,2], color="#3498db")
    axes[1,2].set_title("Attrition by Commute")

    plt.tight_layout(); fig.savefig(os.path.join(args.output_dir, "step09_attrition_patterns.png"), dpi=100); plt.close()
    print("Done")
if __name__ == "__main__": main()
''')

write_script(f"{BASE}/step_10_data-visualization--engagement-performance.py", '''#!/usr/bin/env python3
import argparse, os
import pandas as pd, numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.style.use('seaborn-v0_8-darkgrid')

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--data_dir", default="../data")
    p.add_argument("--output_dir", default=".")
    args = p.parse_args()
    os.makedirs(args.output_dir, exist_ok=True)
    print("STEP 10: Engagement & Performance Viz")

    df = pd.read_parquet(os.path.join(args.output_dir, "features.parquet"))
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    # Engagement by department
    df.groupby("department")["engagement_composite"].mean().sort_values().plot(kind="barh", ax=axes[0,0], color="#3498db")
    axes[0,0].set_title("Avg Engagement by Dept")

    # Performance vs attrition
    df.boxplot(column="avg_performance", by="is_attrited", ax=axes[0,1])
    axes[0,1].set_title("Performance by Attrition")

    # Promotions vs attrition
    df.boxplot(column="total_promotions", by="is_attrited", ax=axes[1,0])
    axes[1,0].set_title("Promotions by Attrition")

    # Work-life balance vs attrition
    wlb = df.groupby("work_life_balance")["is_attrited"].mean()*100
    wlb.plot(kind="bar", ax=axes[1,1], color="#2ecc71")
    axes[1,1].set_title("Attrition by WLB Score")

    plt.tight_layout(); fig.savefig(os.path.join(args.output_dir, "step10_engagement.png"), dpi=100); plt.close()
    print("Done")
if __name__ == "__main__": main()
''')

write_script(f"{BASE}/step_11_statistical-analysis.py", '''#!/usr/bin/env python3
import argparse, os, json
import pandas as pd, numpy as np
from scipy import stats

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--data_dir", default="../data")
    p.add_argument("--output_dir", default=".")
    args = p.parse_args()
    os.makedirs(args.output_dir, exist_ok=True)
    print("STEP 11: Statistical Analysis")

    df = pd.read_parquet(os.path.join(args.output_dir, "features.parquet"))
    results = {}
    # Chi-square for categorical
    for col in ["department", "gender", "education", "marital_status", "overtime"]:
        if col in df.columns:
            ct = pd.crosstab(df[col], df["is_attrited"])
            chi2, p_val, _, _ = stats.chi2_contingency(ct)
            results[f"chi2_{col}"] = {"chi2": round(chi2,2), "p": round(p_val,4), "sig": p_val<0.05}
            print(f"  {col}: chi2={chi2:.1f}, p={p_val:.4f} {'*' if p_val<0.05 else ''}")

    # T-tests for numerical
    for col in ["monthly_salary", "tenure_days", "avg_engagement", "avg_performance", "commute_miles"]:
        if col in df.columns:
            g0 = df[df["is_attrited"]==0][col].dropna()
            g1 = df[df["is_attrited"]==1][col].dropna()
            t, p_val = stats.ttest_ind(g0, g1)
            results[f"ttest_{col}"] = {"t": round(t,2), "p": round(p_val,4), "sig": p_val<0.05}
            print(f"  {col}: t={t:.2f}, p={p_val:.4f} {'*' if p_val<0.05 else ''}")

    with open(os.path.join(args.output_dir, "statistical_results.json"), "w") as f: json.dump(results, f, indent=2)
    print("Done")
if __name__ == "__main__": main()
''')

write_script(f"{BASE}/step_12_data-preparation-for-modeling.py", '''#!/usr/bin/env python3
import argparse, os, json
import pandas as pd, numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import RobustScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from imblearn.over_sampling import SMOTE
import joblib

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--data_dir", default="../data")
    p.add_argument("--output_dir", default=".")
    args = p.parse_args()
    os.makedirs(args.output_dir, exist_ok=True)
    print("STEP 12: Data Preparation for Modeling")

    df = pd.read_parquet(os.path.join(args.output_dir, "features.parquet"))
    cat_cols = ["department", "job_role", "education", "marital_status", "location", "gender"]
    num_cols = ["age", "tenure_days", "monthly_salary", "commute_miles", "work_life_balance",
                "job_satisfaction", "num_companies_worked", "promotions", "overtime", "training_hours",
                "avg_engagement", "avg_satisfaction", "avg_manager_score", "avg_performance",
                "avg_goal_achievement", "total_promotions", "engagement_composite",
                "commute_stress", "promotion_rate", "risk_score"]
    cat_cols = [c for c in cat_cols if c in df.columns]
    num_cols = [c for c in num_cols if c in df.columns]

    X = df[cat_cols + num_cols].copy()
    for c in cat_cols: X[c] = X[c].fillna("Unknown")
    for c in num_cols: X[c] = X[c].fillna(0)
    y = df["is_attrited"].values

    X_temp, X_test, y_temp, y_test = train_test_split(X, y, test_size=0.15, random_state=42, stratify=y)
    X_train, X_val, y_train, y_val = train_test_split(X_temp, y_temp, test_size=0.1765, random_state=42, stratify=y_temp)

    preprocessor = ColumnTransformer([
        ("num", RobustScaler(), num_cols),
        ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), cat_cols),
    ])
    X_train_p = preprocessor.fit_transform(X_train)
    X_val_p = preprocessor.transform(X_val)
    X_test_p = preprocessor.transform(X_test)

    smote = SMOTE(random_state=42)
    X_train_r, y_train_r = smote.fit_resample(X_train_p, y_train)

    np.savez_compressed(os.path.join(args.output_dir, "train_data.npz"), X=X_train_r, y=y_train_r)
    np.savez_compressed(os.path.join(args.output_dir, "val_data.npz"), X=X_val_p, y=y_val)
    np.savez_compressed(os.path.join(args.output_dir, "test_data.npz"), X=X_test_p, y=y_test)
    joblib.dump(preprocessor, os.path.join(args.output_dir, "preprocessor.joblib"))

    cat_names = preprocessor.named_transformers_["cat"].get_feature_names_out(cat_cols)
    meta = {"feature_names": num_cols + list(cat_names), "n_features": X_train_p.shape[1],
            "n_cat": len(cat_cols), "n_num": len(num_cols)}
    with open(os.path.join(args.output_dir, "prep_metadata.json"), "w") as f: json.dump(meta, f)
    print(f"Train: {X_train_r.shape}, Val: {X_val_p.shape}, Test: {X_test_p.shape}")
    print("Done")
if __name__ == "__main__": main()
''')

write_script(f"{BASE}/step_13_model-training-comparison.py", '''#!/usr/bin/env python3
import argparse, os, json
import numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold, cross_validate
from sklearn.metrics import make_scorer, roc_auc_score, fbeta_score, average_precision_score
import warnings; warnings.filterwarnings("ignore")

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--data_dir", default="../data")
    p.add_argument("--output_dir", default=".")
    args = p.parse_args()
    os.makedirs(args.output_dir, exist_ok=True)
    print("STEP 13: Model Training Comparison")

    train = np.load(os.path.join(args.output_dir, "train_data.npz"))
    X, y = train["X"], train["y"]
    models = {
        "LogisticRegression": LogisticRegression(max_iter=2000, random_state=42, n_jobs=-1),
        "RandomForest": RandomForestClassifier(n_estimators=150, max_depth=10, random_state=42, n_jobs=-1),
    }
    try:
        from xgboost import XGBClassifier
        models["XGBoost"] = XGBClassifier(n_estimators=100, max_depth=6, random_state=42, n_jobs=-1, verbosity=0)
    except: pass
    try:
        from lightgbm import LGBMClassifier
        models["LightGBM"] = LGBMClassifier(n_estimators=100, max_depth=6, random_state=42, n_jobs=-1, verbose=-1)
    except: pass

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    scoring = {"roc_auc": make_scorer(roc_auc_score), "pr_auc": make_scorer(average_precision_score), "f2": make_scorer(fbeta_score, beta=2)}
    results = {}
    for name, model in models.items():
        print(f"Training {name}...")
        try:
            cv_r = cross_validate(model, X, y, cv=cv, scoring=scoring, n_jobs=-1)
            results[name] = {k: round(v.mean(),4) for k,v in cv_r.items() if k.startswith("test_")}
            print(f"  ROC-AUC: {results[name]['test_roc_auc']:.4f}")
        except Exception as e: print(f"  Failed: {e}")

    ranked = sorted(results.items(), key=lambda x: x[1]["test_roc_auc"], reverse=True)
    top2 = [r[0] for r in ranked[:2]]
    print(f"Top: {top2}")
    with open(os.path.join(args.output_dir, "top_models.json"), "w") as f: json.dump({"top": top2, "all": {k:{kk:vv for kk,vv in v.items()} for k,v in results.items()}}, f, indent=2)

    fig, ax = plt.subplots(figsize=(8,5))
    names = list(results.keys()); x = np.arange(len(names)); w = 0.25
    ax.bar(x-w, [results[n]["test_roc_auc"] for n in names], w, label="ROC-AUC", color="#3498db")
    ax.bar(x, [results[n]["test_pr_auc"] for n in names], w, label="PR-AUC", color="#e74c3c")
    ax.bar(x+w, [results[n]["test_f2"] for n in names], w, label="F2", color="#2ecc71")
    ax.set_xticks(x); ax.set_xticklabels(names, rotation=15); ax.legend(); ax.set_ylim(0,1)
    plt.tight_layout(); fig.savefig(os.path.join(args.output_dir, "step13_model_comparison.png"), dpi=100); plt.close()
    print("Done")
if __name__ == "__main__": main()
''')

write_script(f"{BASE}/step_14_model-optimization.py", '''#!/usr/bin/env python3
import argparse, os, json
import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.calibration import CalibratedClassifierCV
from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import roc_auc_score
import warnings; warnings.filterwarnings("ignore")

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--data_dir", default="../data")
    p.add_argument("--output_dir", default=".")
    args = p.parse_args()
    os.makedirs(args.output_dir, exist_ok=True)
    print("STEP 14: Model Optimization & Ensembling")

    train = np.load(os.path.join(args.output_dir, "train_data.npz"))
    val = np.load(os.path.join(args.output_dir, "val_data.npz"))
    with open(os.path.join(args.output_dir, "top_models.json")) as f: top_info = json.load(f)

    X_tr, y_tr = train["X"], train["y"]
    X_v, y_v = val["X"], val["y"]
    top = top_info["top"]
    print(f"Tuning: {top}")

    param_grids = {
        "LogisticRegression": {"C": [0.01,0.1,1,10], "solver": ["lbfgs","liblinear"]},
        "RandomForest": {"n_estimators": [100,200], "max_depth": [5,10,15,None], "min_samples_split":[2,5]},
        "XGBoost": {"n_estimators":[100,200], "max_depth":[3,5,7], "learning_rate":[0.01,0.1,0.2]},
        "LightGBM": {"n_estimators":[100,200], "max_depth":[3,5,7], "learning_rate":[0.01,0.1,0.2], "num_leaves":[15,31]},
    }

    tuned = {}
    for name in top:
        if name not in param_grids: continue
        print(f"  Tuning {name}...")
        try:
            if name == "LogisticRegression": m = LogisticRegression(max_iter=2000, random_state=42, n_jobs=-1)
            elif name == "RandomForest": m = RandomForestClassifier(random_state=42, n_jobs=-1)
            elif name == "XGBoost":
                from xgboost import XGBClassifier; m = XGBClassifier(random_state=42, n_jobs=-1, verbosity=0)
            elif name == "LightGBM":
                from lightgbm import LGBMClassifier; m = LGBMClassifier(random_state=42, n_jobs=-1, verbose=-1)
            else: continue
            search = RandomizedSearchCV(m, param_grids[name], n_iter=15, cv=3, scoring="roc_auc", n_jobs=-1, random_state=42)
            search.fit(X_tr, y_tr)
            v_score = roc_auc_score(y_v, search.predict_proba(X_v)[:,1])
            tuned[name] = search.best_estimator_
            print(f"    Val ROC-AUC: {v_score:.4f}")
        except Exception as e: print(f"    Failed: {e}")

    if len(tuned) >= 2:
        ens = VotingClassifier([(n,m) for n,m in tuned.items()], voting="soft", n_jobs=-1)
        ens.fit(X_tr, y_tr)
        final = CalibratedClassifierCV(ens, method="isotonic", cv="prefit")
        final.fit(X_v, y_v)
    elif len(tuned) == 1:
        final = CalibratedClassifierCV(list(tuned.values())[0], method="isotonic", cv="prefit")
        final.fit(X_v, y_v)
    else:
        final = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1).fit(X_tr, y_tr)

    joblib.dump(final, os.path.join(args.output_dir, "final_model.joblib"))
    print("Model saved")
if __name__ == "__main__": main()
''')

write_script(f"{BASE}/step_15_model-explainability-retention-insights.py", '''#!/usr/bin/env python3
import argparse, os, json
import numpy as np, pandas as pd
import joblib
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.metrics import roc_auc_score, classification_report, confusion_matrix, roc_curve, precision_recall_curve

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--data_dir", default="../data")
    p.add_argument("--output_dir", default=".")
    args = p.parse_args()
    os.makedirs(args.output_dir, exist_ok=True)
    print("STEP 15: Model Explainability & Retention Insights")

    test = np.load(os.path.join(args.output_dir, "test_data.npz"))
    model = joblib.load(os.path.join(args.output_dir, "final_model.joblib"))
    X_t, y_t = test["X"], test["y"]

    y_prob = model.predict_proba(X_t)[:,1]
    y_pred = model.predict(X_t)
    auc = roc_auc_score(y_t, y_prob)
    f1 = classification_report(y_t, y_pred, output_dict=True)["1"]["f1-score"]

    print(f"ROC-AUC: {auc:.4f}, F1: {f1:.4f}")
    print(f"\\n{classification_report(y_t, y_pred, target_names=['Retained','Attrited'])}")

    # Feature importance via permutation (simple)
    try:
        from sklearn.inspection import permutation_importance
        with open(os.path.join(args.output_dir, "prep_metadata.json")) as f: meta = json.load(f)
        imp = permutation_importance(model, X_t, y_t, n_repeats=5, random_state=42, scoring="roc_auc")
        importance_df = pd.DataFrame({"feature": meta["feature_names"][:len(imp.importances_mean)],
                                       "importance": imp.importances_mean}).sort_values("importance", ascending=False).head(15)

        fig, ax = plt.subplots(figsize=(8,5))
        importance_df.head(10).plot(kind="barh", x="feature", y="importance", ax=ax, color="#3498db", legend=False)
        ax.set_title("Top 10 Feature Importances"); ax.invert_yaxis()
        plt.tight_layout(); fig.savefig(os.path.join(args.output_dir, "step15_feature_importance.png"), dpi=100); plt.close()
    except Exception as e: print(f"Feature importance skipped: {e}")

    # Confusion matrix + curves
    fig, axes = plt.subplots(1, 3, figsize=(16, 4))
    cm = confusion_matrix(y_t, y_pred)
    axes[0].imshow(cm, cmap="Blues"); axes[0].set_title(f"Confusion Matrix\\nAUC={auc:.3f}")
    for i in range(2):
        for j in range(2): axes[0].text(j,i,cm[i,j],ha="center",va="center",fontsize=14)
    axes[0].set_xticks([0,1]); axes[0].set_yticks([0,1]); axes[0].set_xticklabels(["Ret","Attr"]); axes[0].set_yticklabels(["Ret","Attr"])

    fpr,tpr,_ = roc_curve(y_t, y_prob)
    axes[1].plot(fpr, tpr, color="#e74c3c"); axes[1].plot([0,1],[0,1],"k--")
    axes[1].set_title(f"ROC (AUC={auc:.3f})")

    prec, rec, _ = precision_recall_curve(y_t, y_prob)
    axes[2].plot(rec, prec, color="#2ecc71")
    axes[2].set_title("Precision-Recall")

    plt.tight_layout(); fig.savefig(os.path.join(args.output_dir, "step15_evaluation.png"), dpi=100); plt.close()

    metrics = {"roc_auc": round(auc,4), "f1": round(f1,4)}
    with open(os.path.join(args.output_dir, "evaluation_metrics.json"), "w") as f: json.dump(metrics, f)
    print("Done")
if __name__ == "__main__": main()
''')

write_script(f"{BASE}/step_16_final-synthesis-retention-strategy.py", '''#!/usr/bin/env python3
import argparse, os, json
from datetime import datetime

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--data_dir", default="../data")
    p.add_argument("--output_dir", default=".")
    args = p.parse_args()
    os.makedirs(args.output_dir, exist_ok=True)
    print("STEP 16: Final Retention Strategy Report")

    try:
        with open(os.path.join(args.output_dir, "evaluation_metrics.json")) as f: eval_m = json.load(f)
        with open(os.path.join(args.output_dir, "eda_insights.json")) as f: eda = json.load(f)
        with open(os.path.join(args.output_dir, "top_models.json")) as f: top = json.load(f)
    except: eval_m, eda, top = {}, {}, {}

    lines = ["="*60, "EMPLOYEE ATTRITION — RETENTION STRATEGY REPORT", "="*60,
             f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}", "",
             "1. MODEL PERFORMANCE",
             f"  ROC-AUC: {eval_m.get('roc_auc','N/A')}",
             f"  F1 Score: {eval_m.get('f1','N/A')}", ""]

    if top.get("all"):
        lines.append("  Model Comparison (CV ROC-AUC):")
        for name, scores in sorted(top["all"].items(), key=lambda x: x[1].get("test_roc_auc",0), reverse=True):
            lines.append(f"    {name}: {scores.get('test_roc_auc','N/A')}")
    lines.append("")

    lines.append("2. KEY ATTRITION DRIVERS")
    if eda.get("top_correlations"):
        for feat, val in list(eda["top_correlations"].items())[:5]:
            lines.append(f"  {feat}: r={val:.3f}")
    lines.append("")

    lines.extend(["3. RETENTION RECOMMENDATIONS",
                  "  • Target employees with low engagement scores for stay interviews",
                  "  • Review compensation for high-attrition roles",
                  "  • Address overtime concerns in departments with high attrition",
                  "  • Implement flexible work for employees with long commutes",
                  "  • Create career development paths for roles with low promotion rates",
                  "  • Conduct exit interview analysis quarterly",
                  "", "4. MONITORING PLAN",
                  "  • Track monthly attrition rate by department",
                  "  • Monitor model PSI quarterly",
                  "  • Retrain model every 6 months",
                  "", "="*60, "END OF REPORT", "="*60])

    report = "\\n".join(lines)
    print(report)
    with open(os.path.join(args.output_dir, "retention_strategy.txt"), "w") as f: f.write(report)
    print("Done")
if __name__ == "__main__": main()
''')

print("Employee attrition scripts done!")
