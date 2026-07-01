#!/usr/bin/env python3
"""Step 7: Data Visualization — Risk Profiles dashboard."""
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
    print("STEP 7: Data Visualization — Risk Profiles")
    print("=" * 60)

    df = pd.read_parquet(os.path.join(args.output_dir, "feature_engineered.parquet"))

    fig, axes = plt.subplots(2, 2, figsize=(14, 12))
    fig.suptitle("Credit Risk Profile Dashboard", fontsize=16, fontweight="bold", y=1.01)

    # 1. Loan Amount by Purpose with default overlay
    if "loan_purpose" in df.columns and "loan_amount" in df.columns:
        purpose_order = df.groupby("loan_purpose")["loan_amount"].median().sort_values().index
        for purpose in purpose_order:
            subset = df[df["loan_purpose"] == purpose]
            default_rate = subset["default_flag"].mean()
            axes[0, 0].scatter(subset["loan_amount"], [purpose]*len(subset),
                              c=["#e74c3c" if d else "#2ecc71" for d in subset["default_flag"]],
                              alpha=0.4, s=15)
        axes[0, 0].set_title("Loan Amount by Purpose (Red=Default, Green=Non-Default)")
        axes[0, 0].set_xlabel("Loan Amount ($)")
        axes[0, 0].set_xscale("log")

    # 2. Employment length vs default rate
    if "employment_length" in df.columns:
        emp_order = ["<1 year", "1-3 years", "3-5 years", "5-10 years", "10+ years", "Unknown"]
        emp_present = [e for e in emp_order if e in df["employment_length"].values]
        emp_rates = df[df["employment_length"].isin(emp_present)].groupby("employment_length")["default_flag"].mean() * 100
        emp_counts = df[df["employment_length"].isin(emp_present)].groupby("employment_length").size()

        x = range(len(emp_rates))
        axes[0, 1].bar(x, emp_rates.values, color="#3498db", edgecolor="white")
        for i, (rate, cnt) in enumerate(zip(emp_rates.values, emp_counts.values)):
            axes[0, 1].text(i, rate + 0.5, f"n={cnt}", ha="center", fontsize=8)
        axes[0, 1].set_xticks(x)
        axes[0, 1].set_xticklabels(emp_rates.index, rotation=30, ha="right")
        axes[0, 1].set_title("Default Rate by Employment Length")
        axes[0, 1].set_ylabel("Default Rate (%)")
        axes[0, 1].axhline(y=df["default_flag"].mean()*100, color="red", linestyle="--", alpha=0.5)

    # 3. Geographic default rate (by state)
    if "state" in df.columns:
        state_rates = df.groupby("state")["default_flag"].agg(["mean", "count"])
        state_rates = state_rates[state_rates["count"] >= 3].sort_values("mean", ascending=False).head(15)
        axes[1, 0].barh(range(len(state_rates)), state_rates["mean"].values * 100, color="#e67e22", edgecolor="white")
        axes[1, 0].set_yticks(range(len(state_rates)))
        axes[1, 0].set_yticklabels(state_rates.index)
        axes[1, 0].set_title("Default Rate by State (Top 15)")
        axes[1, 0].set_xlabel("Default Rate (%)")
        axes[1, 0].invert_yaxis()

    # 4. Age vs Income scatter with default coloring
    if "age" in df.columns and "annual_income" in df.columns:
        colors = ["#e74c3c" if d else "#3498db" for d in df["default_flag"]]
        axes[1, 1].scatter(df["age"], df["annual_income"], c=colors, alpha=0.4, s=20, edgecolors="none")
        axes[1, 1].set_title("Age vs Annual Income (Blue=Safe, Red=Default)")
        axes[1, 1].set_xlabel("Age")
        axes[1, 1].set_ylabel("Annual Income ($)")

    plt.tight_layout()
    fig.savefig(os.path.join(args.output_dir, "step07_risk_profiles.png"), dpi=120, bbox_inches="tight")
    plt.close()

    print(f"📊 Risk profile dashboard generated with 4 panels")
    print(f"✅ Step 7 complete")

if __name__ == "__main__":
    main()
