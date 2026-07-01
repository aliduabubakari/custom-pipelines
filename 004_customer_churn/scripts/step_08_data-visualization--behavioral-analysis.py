#!/usr/bin/env python3
"""Step 8: Data Visualization — Behavioral Analysis (RFM patterns)."""
import argparse, os
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
    print("STEP 8: Data Visualization — Behavioral Analysis")
    print("=" * 60)

    df = pd.read_parquet(os.path.join(args.output_dir, "feature_engineered.parquet"))

    fig, axes = plt.subplots(2, 2, figsize=(14, 12))
    fig.suptitle("Customer Behavior Analysis", fontsize=16, fontweight="bold")

    # 1. RFM scatter: Recency vs Frequency colored by churn
    if "days_since_last_purchase" in df.columns and "purchase_frequency" in df.columns:
        for flag, label, color, marker in [(0, "Retained", "#2ecc71", "o"), (1, "Churned", "#e74c3c", "x")]:
            subset = df[df["is_churned"] == flag].sample(min(200, (df["is_churned"] == flag).sum()), random_state=42)
            axes[0, 0].scatter(subset["days_since_last_purchase"].clip(0, 365),
                              subset["purchase_frequency"].clip(0, 10),
                              c=color, marker=marker, alpha=0.6, s=30, label=label, edgecolors="none")
        axes[0, 0].set_title("Recency vs Frequency (Color=Churn)")
        axes[0, 0].set_xlabel("Days Since Last Purchase")
        axes[0, 0].set_ylabel("Purchases/Month")
        axes[0, 0].legend()

    # 2. Return rate vs churn scatter
    if "return_rate" in df.columns and "total_spend" in df.columns:
        for flag, label, color in [(0, "Retained", "#2ecc71"), (1, "Churned", "#e74c3c")]:
            subset = df[df["is_churned"] == flag].sample(min(150, (df["is_churned"] == flag).sum()), random_state=42)
            axes[0, 1].scatter(subset["return_rate"] * 100, subset["total_spend"].clip(0, 5000),
                              c=color, alpha=0.5, s=25, label=label, edgecolors="none")
        axes[0, 1].set_title("Return Rate vs Total Spend")
        axes[0, 1].set_xlabel("Return Rate (%)")
        axes[0, 1].set_ylabel("Total Spend ($)")
        axes[0, 1].legend()

    # 3. Discount dependency vs churn
    if "discount_usage_rate" in df.columns:
        disc_bins = pd.cut(df["discount_usage_rate"], bins=[-0.01, 0, 0.25, 0.5, 0.75, 1.01],
                           labels=["0%", "1-25%", "25-50%", "50-75%", "75%+"])
        disc = df.groupby(disc_bins, observed=False)["is_churned"].mean() * 100
        axes[1, 0].bar(disc.index, disc.values, color="#9b59b6", edgecolor="white")
        axes[1, 0].set_title("Churn Rate by Discount Usage")
        axes[1, 0].set_ylabel("Churn Rate (%)")
        axes[1, 0].axhline(y=df["is_churned"].mean()*100, color="gray", linestyle="--")

    # 4. Category diversity bar chart
    if "category_diversity" in df.columns:
        for flag, label, color in [(0, "Retained", "#2ecc71"), (1, "Churned", "#e74c3c")]:
            counts = df[df["is_churned"] == flag]["category_diversity"].value_counts().sort_index()
            axes[1, 1].bar(counts.index + (0.15 if flag == 1 else -0.15), counts.values,
                           width=0.3, color=color, alpha=0.7, label=label, edgecolor="white")
        axes[1, 1].set_title("Category Diversity by Churn")
        axes[1, 1].set_xlabel("Unique Categories Purchased")
        axes[1, 1].legend()

    plt.tight_layout()
    fig.savefig(os.path.join(args.output_dir, "step08_behavioral.png"), dpi=120, bbox_inches="tight")
    plt.close()
    print("📊 Behavioral dashboard generated")
    print("✅ Step 8 complete")

if __name__ == "__main__":
    main()
