#!/usr/bin/env python3
"""Step 8: Data Visualization — Credit Behavior patterns."""
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
    print("STEP 8: Data Visualization — Credit Behavior")
    print("=" * 60)

    df = pd.read_parquet(os.path.join(args.output_dir, "feature_engineered.parquet"))

    fig, axes = plt.subplots(2, 2, figsize=(14, 12))
    fig.suptitle("Credit Behavior Analysis", fontsize=16, fontweight="bold")

    # 1. Utilization ratio histogram by default status
    # Use revolving_utilization or avg_utilization
    util_col = "revolving_utilization" if "revolving_utilization" in df.columns else "avg_utilization"
    if util_col in df.columns:
        for flag, label, color in [(0, "Non-Default", "#2ecc71"), (1, "Default", "#e74c3c")]:
            subset = df[df["default_flag"] == flag][util_col].dropna().clip(0, 150)
            axes[0, 0].hist(subset, bins=40, alpha=0.6, label=label, color=color, edgecolor="white")
        axes[0, 0].set_title(f"{util_col} Distribution by Default Status")
        axes[0, 0].set_xlabel("Utilization (%)")
        axes[0, 0].legend()

    # 2. Account type / number of accounts by default
    if "total_accounts" in df.columns:
        for flag, label, color in [(0, "Non-Default", "#2ecc71"), (1, "Default", "#e74c3c")]:
            subset = df[df["default_flag"] == flag]["total_accounts"].dropna()
            axes[0, 1].hist(subset, bins=25, alpha=0.6, label=label, color=color, edgecolor="white")
        axes[0, 1].set_title("Total Accounts Distribution by Default Status")
        axes[0, 1].set_xlabel("Number of Accounts")
        axes[0, 1].legend()

    # 3. Inquiry count vs default rate with confidence intervals
    if "inquiries_6mo" in df.columns:
        df["inquiry_bin"] = pd.cut(df["inquiries_6mo"], bins=[-1, 0, 1, 2, 4, 10, 100],
                                    labels=["0", "1", "2", "3-4", "5-10", "10+"])
        inquiry_rates = df.groupby("inquiry_bin", observed=False)["default_flag"].agg(["mean", "count", "std"])
        inquiry_rates["ci"] = 1.96 * inquiry_rates["std"] / np.sqrt(inquiry_rates["count"])

        x = range(len(inquiry_rates))
        axes[1, 0].bar(x, inquiry_rates["mean"] * 100, yerr=inquiry_rates["ci"] * 100,
                       color="#8e44ad", edgecolor="white", capsize=4)
        for i, (_, row) in enumerate(inquiry_rates.iterrows()):
            axes[1, 0].text(i, row["mean"] * 100 + 1, f"n={int(row['count'])}", ha="center", fontsize=8)
        axes[1, 0].set_xticks(x)
        axes[1, 0].set_xticklabels(inquiry_rates.index)
        axes[1, 0].set_title("Default Rate by Inquiries (6mo) — with 95% CI")
        axes[1, 0].set_ylabel("Default Rate (%)")
        axes[1, 0].set_xlabel("Inquiries in Last 6 Months")

    # 4. Credit age vs default
    if "credit_age_months" in df.columns:
        credit_bins = [0, 24, 60, 120, 240, 480]
        credit_labels = ["<2yr", "2-5yr", "5-10yr", "10-20yr", "20+yr"]
        df["credit_age_bin"] = pd.cut(df["credit_age_months"], bins=credit_bins, labels=credit_labels)
        credit_rates = df.groupby("credit_age_bin", observed=False)["default_flag"].agg(["mean", "count"])
        axes[1, 1].bar(range(len(credit_rates)), credit_rates["mean"] * 100, color="#16a085", edgecolor="white")
        axes[1, 1].set_xticks(range(len(credit_rates)))
        axes[1, 1].set_xticklabels(credit_rates.index)
        axes[1, 1].set_title("Default Rate by Credit History Length")
        axes[1, 1].set_ylabel("Default Rate (%)")
        for i, (_, row) in enumerate(credit_rates.iterrows()):
            axes[1, 1].text(i, row["mean"] * 100 + 0.5, f"n={int(row['count'])}", ha="center", fontsize=8)

    plt.tight_layout()
    fig.savefig(os.path.join(args.output_dir, "step08_credit_behavior.png"), dpi=120, bbox_inches="tight")
    plt.close()

    print("📊 Credit behavior dashboard generated")
    print("✅ Step 8 complete")

if __name__ == "__main__":
    main()
