#!/usr/bin/env python3
"""Step 10: Cohort Analysis — Monthly retention cohorts by signup month."""
import argparse, os, json
import pandas as pd, numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--data_dir", default="../data")
    p.add_argument("--output_dir", default=".")
    args = p.parse_args()
    os.makedirs(args.output_dir, exist_ok=True)
    print("=" * 60)
    print("STEP 10: Cohort Analysis")
    print("=" * 60)

    df = pd.read_parquet(os.path.join(args.output_dir, "feature_engineered.parquet"))

    # Parse signup date and create cohort month
    if "signup_date" not in df.columns:
        print("⚠️  signup_date not found, using tenure_days to infer")
        df["signup_date"] = pd.Timestamp("2023-01-01")

    df["signup_date"] = pd.to_datetime(df["signup_date"], errors="coerce")
    df["cohort_month"] = df["signup_date"].dt.to_period("M").astype(str)
    df["cohort_index"] = ((df["tenure_days"] / 30).astype(int)).clip(0, 12)

    # Build cohort retention matrix
    cohorts = df["cohort_month"].dropna().unique()
    cohorts = sorted(cohorts)[-8:]  # last 8 cohorts

    retention_matrix = {}
    for cohort in cohorts:
        cohort_data = df[df["cohort_month"] == cohort]
        total = len(cohort_data)
        retention = {}
        for month in range(0, 13):
            retained = (cohort_data["tenure_days"] > month * 30).sum()
            retention[str(month)] = round(retained / total * 100, 1) if total > 0 else 0
        retention_matrix[cohort] = retention

    print(f"\n📊 Retention Matrix ({len(cohorts)} cohorts):")
    print(f"{'Cohort':<10}", end="")
    for m in range(0, 13, 2):
        print(f" M{m:>5}", end="")
    print()
    for cohort in cohorts:
        print(f"{cohort:<10}", end="")
        for m in range(0, 13, 2):
            print(f" {retention_matrix[cohort][str(m)]:>5.0f}%", end="")
        print()

    # Heatmap
    mat_df = pd.DataFrame(retention_matrix).T
    fig, ax = plt.subplots(figsize=(14, 6))
    sns.heatmap(mat_df, annot=True, fmt=".0f", cmap="RdYlGn", vmin=0, vmax=100, ax=ax,
                cbar_kws={"label": "Retention (%)"})
    ax.set_title("Monthly Cohort Retention Matrix")
    ax.set_xlabel("Months Since Signup")
    ax.set_ylabel("Cohort (Signup Month)")
    plt.tight_layout()
    fig.savefig(os.path.join(args.output_dir, "step10_cohort.png"), dpi=120, bbox_inches="tight")
    plt.close()

    with open(os.path.join(args.output_dir, "cohort_analysis.json"), "w") as f:
        json.dump({"retention_matrix": retention_matrix, "n_cohorts": len(cohorts)}, f, indent=2)
    print("\n✅ Step 10 complete")

if __name__ == "__main__":
    main()
