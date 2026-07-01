#!/usr/bin/env python3
"""Step 7: Data Visualization — Churn Patterns dashboard."""
import argparse, os
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
    print("STEP 7: Data Visualization — Churn Patterns")
    print("=" * 60)

    df = pd.read_parquet(os.path.join(args.output_dir, "feature_engineered.parquet"))

    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    fig.suptitle("Customer Churn Pattern Dashboard", fontsize=16, fontweight="bold")

    # Panel 1: Churn by Segment
    seg = df.groupby("segment")["is_churned"].mean() * 100
    seg.sort_values().plot(kind="barh", ax=axes[0, 0], color="#e74c3c", edgecolor="white")
    axes[0, 0].set_title("Churn Rate by Segment")
    axes[0, 0].axvline(x=df["is_churned"].mean()*100, color="gray", linestyle="--")

    # Panel 2: Tenure vs Churn
    if "tenure_days" in df.columns:
        for flag, label, color in [(0, "Retained", "#2ecc71"), (1, "Churned", "#e74c3c")]:
            subset = df[df["is_churned"] == flag]["tenure_days"].clip(0, 1000)
            axes[0, 1].hist(subset, bins=40, alpha=0.6, label=label, color=color, edgecolor="white")
        axes[0, 1].set_title("Tenure Distribution by Churn")
        axes[0, 1].legend()

    # Panel 3: Acquisition channel churn heatmap
    if "acquisition_channel" in df.columns and "segment" in df.columns:
        heatmap = df.pivot_table(values="is_churned", index="segment", columns="acquisition_channel",
                                 aggfunc="mean", observed=False) * 100
        sns.heatmap(heatmap, annot=True, fmt=".1f", cmap="YlOrRd", ax=axes[0, 2])
        axes[0, 2].set_title("Churn Rate: Segment × Channel")

    # Panel 4: Monthly spend trend (simulated: spend by tenure group)
    if "monthly_spend" in df.columns and "tenure_group" in df.columns:
        for flag, label, color in [(0, "Retained", "#2ecc71"), (1, "Churned", "#e74c3c")]:
            means = df[df["is_churned"] == flag].groupby("tenure_group", observed=False)["monthly_spend"].mean()
            axes[1, 0].plot(means.index, means.values, "o-", color=color, label=label, lw=2)
        axes[1, 0].set_title("Avg Monthly Spend by Tenure Group")
        axes[1, 0].legend()
        axes[1, 0].tick_params(axis='x', rotation=30)

    # Panel 5: LTV distribution
    if "total_spend" in df.columns:
        for flag, label, color in [(0, "Retained", "#2ecc71"), (1, "Churned", "#e74c3c")]:
            subset = df[df["is_churned"] == flag]["total_spend"].clip(0, 5000)
            axes[1, 1].hist(subset, bins=30, alpha=0.5, label=label, color=color, edgecolor="white")
        axes[1, 1].set_title("LTV (Total Spend) by Churn Status")
        axes[1, 1].legend()

    # Panel 6: Return rate vs churn
    if "return_rate" in df.columns:
        df["return_bin"] = pd.cut(df["return_rate"], bins=[-0.01, 0, 0.1, 0.3, 1.01],
                                   labels=["0%", "1-10%", "10-30%", "30%+"])
        ret = df.groupby("return_bin", observed=False)["is_churned"].mean() * 100
        axes[1, 2].bar(ret.index, ret.values, color="#e67e22", edgecolor="white")
        axes[1, 2].set_title("Churn Rate by Return Rate")
        axes[1, 2].set_ylabel("Churn Rate (%)")

    plt.tight_layout()
    fig.savefig(os.path.join(args.output_dir, "step07_churn_patterns.png"), dpi=120, bbox_inches="tight")
    plt.close()
    print("📊 Dashboard generated with 6 panels")
    print("✅ Step 7 complete")

if __name__ == "__main__":
    main()
