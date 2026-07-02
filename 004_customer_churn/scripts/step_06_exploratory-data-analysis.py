#!/usr/bin/env python3
"""Step 6: Exploratory Data Analysis — Analyze churn patterns."""
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
    eda = {}

    # Churn by segments
    for cat in ["segment", "acquisition_channel", "plan_type", "tenure_group"]:
        if cat in df.columns:
            rates = df.groupby(cat, observed=False)["is_churned"].agg(["mean", "count"])
            eda[f"churn_by_{cat}"] = rates.to_dict()
            print(f"\n📊 Churn by {cat}:")
            for idx, row in rates.iterrows():
                print(f"   {idx}: {row['mean']*100:.1f}% (n={int(row['count'])})")

    # Correlation with churn
    num_cols = df.select_dtypes(include=['float64', 'int64']).columns
    num_cols = [c for c in num_cols if c not in ['customer_id'] and df[c].nunique() > 1]
    corr = df[num_cols].corr()["is_churned"].drop("is_churned").sort_values(key=abs, ascending=False)
    eda["top_correlations"] = corr.head(10).to_dict()
    print(f"\n🔗 Top churn correlations:")
    for feat, val in corr.head(8).items():
        print(f"   {feat}: {val:+.3f}")

    # Visualizations
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))

    # A: Churn by segment
    seg_rates = df.groupby("segment")["is_churned"].mean() * 100
    seg_rates.sort_values().plot(kind="barh", ax=axes[0, 0], color="#e74c3c", edgecolor="white")
    axes[0, 0].set_title("Churn Rate by Segment")
    axes[0, 0].axvline(x=df["is_churned"].mean()*100, color="black", linestyle="--")

    # B: Tenure vs churn
    tenure_bins = [0, 30, 90, 180, 365, 730, 5000]
    tenure_labels = ["<1m", "1-3m", "3-6m", "6-12m", "1-2yr", "2yr+"]
    df["tenure_bin_viz"] = pd.cut(df["tenure_days"], bins=tenure_bins, labels=tenure_labels)
    t_rates = df.groupby("tenure_bin_viz", observed=False)["is_churned"].mean() * 100
    axes[0, 1].plot(range(len(t_rates)), t_rates.values, "o-", color="#3498db", lw=2, markersize=8)
    axes[0, 1].set_xticks(range(len(t_rates)))
    axes[0, 1].set_xticklabels(t_rates.index)
    axes[0, 1].set_title("Churn Rate by Tenure")
    axes[0, 1].set_ylabel("Churn Rate (%)")

    # C: Spend distribution by churn
    for flag, label, color in [(0, "Retained", "#2ecc71"), (1, "Churned", "#e74c3c")]:
        subset = df[df["is_churned"] == flag]["total_spend"].clip(0, 5000)
        axes[1, 0].hist(subset, bins=30, alpha=0.6, label=label, color=color, edgecolor="white")
    axes[1, 0].set_title("Total Spend Distribution by Churn Status")
    axes[1, 0].legend()

    # D: Support contacts vs churn
    supp_rates = df.groupby("support_contacts")["is_churned"].mean() * 100
    axes[1, 1].bar(supp_rates.index.astype(str), supp_rates.values, color="#8e44ad", edgecolor="white")
    axes[1, 1].set_title("Churn Rate by Support Contacts")
    axes[1, 1].set_ylabel("Churn Rate (%)")
    axes[1, 1].set_xlabel("Number of Support Contacts")

    plt.tight_layout()
    fig.savefig(os.path.join(args.output_dir, "step06_eda.png"), dpi=120)
    plt.close()

    with open(os.path.join(args.output_dir, "eda_results.json"), "w") as f:
        json.dump(eda, f, default=str, indent=2)
    print("\n✅ Step 6 complete")

if __name__ == "__main__":
    main()
