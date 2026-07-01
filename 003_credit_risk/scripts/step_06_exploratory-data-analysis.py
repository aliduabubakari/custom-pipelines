#!/usr/bin/env python3
"""Step 6: Exploratory Data Analysis — Analyze default patterns and correlations."""
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
    print("STEP 6: Exploratory Data Analysis")
    print("=" * 60)

    df = pd.read_parquet(os.path.join(args.output_dir, "feature_engineered.parquet"))
    eda_results = {}

    # 1. Default rate by categorical segments
    for cat_col in ["FICO_band", "DTI_category", "loan_purpose", "home_ownership", "loan_size", "age_group"]:
        if cat_col in df.columns:
            rates = df.groupby(cat_col, observed=False)["default_flag"].agg(["mean", "count"]).round(4)
            rates.columns = ["default_rate", "count"]
            eda_results[f"default_rate_by_{cat_col}"] = rates.to_dict()
            print(f"\n📊 Default rate by {cat_col}:")
            for idx, row in rates.iterrows():
                print(f"   {idx}: {row['default_rate']*100:.1f}% (n={int(row['count'])})")

    # 2. Correlation matrix (numerical only)
    num_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
    # Remove ID-like columns and target
    num_cols = [c for c in num_cols if c not in ['application_id'] and df[c].nunique() > 1]
    corr = df[num_cols].corr()
    eda_results["top_correlations_with_default"] = {}
    if "default_flag" in corr.columns:
        corr_default = corr["default_flag"].drop("default_flag").sort_values(key=abs, ascending=False)
        eda_results["top_correlations_with_default"] = corr_default.to_dict()
        print(f"\n🔗 Top correlations with default_flag:")
        for feat, val in corr_default.head(8).items():
            print(f"   {feat}: {val:+.3f}")

    # 3. VIF-like check for multicollinearity
    # Simplified: flag any pair with |r| > 0.8
    high_corr_pairs = []
    for i in range(len(num_cols)):
        for j in range(i+1, len(num_cols)):
            if abs(corr.iloc[i, j]) > 0.8:
                high_corr_pairs.append((num_cols[i], num_cols[j], round(corr.iloc[i, j], 3)))
    if high_corr_pairs:
        print(f"\n⚠️  High multicollinearity pairs (|r| > 0.8):")
        for c1, c2, val in high_corr_pairs:
            print(f"   {c1} ↔ {c2}: {val}")
    eda_results["high_correlation_pairs"] = high_corr_pairs

    # 4. Visualizations
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))

    # A: Default rate by FICO band
    if "FICO_band" in df.columns:
        rates = df.groupby("FICO_band", observed=False)["default_flag"].mean() * 100
        rates.plot(kind="bar", ax=axes[0, 0], color=["#c0392b", "#e67e22", "#f1c40f", "#2ecc71", "#27ae60"], edgecolor="white")
        axes[0, 0].set_title("Default Rate by FICO Band")
        axes[0, 0].set_ylabel("Default Rate (%)")
        axes[0, 0].axhline(y=df["default_flag"].mean()*100, color="black", linestyle="--", alpha=0.5)

    # B: Loan amount distribution by default status
    if "loan_amount" in df.columns:
        for flag, label, color in [(0, "Non-Default", "#2ecc71"), (1, "Default", "#e74c3c")]:
            subset = df[df["default_flag"] == flag]["loan_amount"]
            axes[0, 1].hist(subset, bins=30, alpha=0.6, label=label, color=color, edgecolor="white")
        axes[0, 1].set_title("Loan Amount Distribution by Default Status")
        axes[0, 1].set_xlabel("Loan Amount ($)")
        axes[0, 1].legend()

    # C: Heatmap of default rate by FICO × DTI
    if "FICO_band" in df.columns and "DTI_category" in df.columns:
        heatmap = df.pivot_table(values="default_flag", index="DTI_category", columns="FICO_band", aggfunc="mean", observed=False) * 100
        sns.heatmap(heatmap, annot=True, fmt=".1f", cmap="YlOrRd", ax=axes[1, 0], cbar_kws={'label': 'Default Rate (%)'})
        axes[1, 0].set_title("Default Rate Heatmap: FICO × DTI")

    # D: DTI ratio distribution by default
    if "dti_ratio" in df.columns:
        for flag, label, color in [(0, "Non-Default", "#2ecc71"), (1, "Default", "#e74c3c")]:
            subset = df[df["default_flag"] == flag]["dti_ratio"]
            axes[1, 1].hist(subset, bins=30, alpha=0.6, label=label, color=color, edgecolor="white")
        axes[1, 1].set_title("DTI Ratio Distribution by Default Status")
        axes[1, 1].set_xlabel("DTI Ratio (%)")
        axes[1, 1].legend()

    plt.tight_layout()
    fig.savefig(os.path.join(args.output_dir, "step06_eda.png"), dpi=120)
    plt.close()

    # Save EDA results
    with open(os.path.join(args.output_dir, "eda_results.json"), "w") as f:
        json.dump(eda_results, f, indent=2, default=str)

    print(f"\n✅ Step 6 complete — EDA results saved")

if __name__ == "__main__":
    main()
