#!/usr/bin/env python3
"""Step 1: Data Loading & Profiling — Load and profile all three data sources."""
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
    print("=" * 60)
    print("STEP 1: Data Loading & Profiling")
    print("=" * 60)

    # Load
    apps = pd.read_csv(os.path.join(args.data_dir, "applications.csv"))
    with open(os.path.join(args.data_dir, "credit_history.json")) as f:
        history = pd.DataFrame(json.load(f))
    bureau = pd.read_excel(os.path.join(args.data_dir, "bureau_data.xlsx"))

    # Profile each dataset
    profiling = {}
    for name, df in [("applications", apps), ("credit_history", history), ("bureau_data", bureau)]:
        profile = {
            "rows": len(df),
            "columns": len(df.columns),
            "column_names": df.columns.tolist(),
            "dtypes": {c: str(t) for c, t in df.dtypes.items()},
            "null_counts": df.isnull().sum().to_dict(),
            "null_pct": (df.isnull().sum() / len(df) * 100).round(2).to_dict()
        }
        if "default_flag" in df.columns:
            profile["default_rate"] = round(df["default_flag"].mean() * 100, 2)
        if "fico_score" in df.columns:
            profile["fico_stats"] = {
                "mean": round(df["fico_score"].mean(), 1),
                "median": round(df["fico_score"].median(), 1),
                "min": int(df["fico_score"].min()),
                "max": int(df["fico_score"].max()),
                "std": round(df["fico_score"].std(), 1)
            }
        profiling[name] = profile
        print(f"\n{'─' * 40}")
        print(f"📊 {name.upper()}: {profile['rows']} rows × {profile['columns']} cols")
        print(f"   Columns: {', '.join(df.columns[:5])}...")
        print(f"   Nulls: {sum(v > 0 for v in profile['null_counts'].values())} columns have nulls")

    # Identify target
    target_col = "default_flag"
    print(f"\n🎯 Target variable: '{target_col}' (default rate: {profiling['applications']['default_rate']}%)")

    # Save profiling summary
    with open(os.path.join(args.output_dir, "profiling_summary.json"), "w") as f:
        json.dump(profiling, f, indent=2, default=str)

    # Save raw parquet for downstream
    apps.to_parquet(os.path.join(args.output_dir, "raw_applications.parquet"), index=False)
    history.to_parquet(os.path.join(args.output_dir, "raw_credit_history.parquet"), index=False)
    bureau.to_parquet(os.path.join(args.output_dir, "raw_bureau.parquet"), index=False)

    # Viz: default rate by loan purpose
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    apps.groupby("loan_purpose")["default_flag"].mean().sort_values().plot(
        kind="barh", ax=axes[0], color="#e74c3c", edgecolor="white")
    axes[0].set_title("Default Rate by Loan Purpose")
    axes[0].set_xlabel("Default Rate")

    apps.groupby("home_ownership")["default_flag"].mean().sort_values().plot(
        kind="barh", ax=axes[1], color="#3498db", edgecolor="white")
    axes[1].set_title("Default Rate by Home Ownership")
    axes[1].set_xlabel("Default Rate")

    plt.tight_layout()
    fig.savefig(os.path.join(args.output_dir, "step01_profiling.png"), dpi=100)
    plt.close()
    print("\n✅ Step 1 complete — profiling saved + initial visualizations generated")

if __name__ == "__main__":
    main()
