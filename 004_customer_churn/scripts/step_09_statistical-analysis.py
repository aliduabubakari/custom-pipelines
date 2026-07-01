#!/usr/bin/env python3
"""Step 9: Statistical Analysis — Chi-square, ANOVA, survival analysis."""
import argparse, os, json
import pandas as pd, numpy as np
from scipy import stats
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--data_dir", default="../data")
    p.add_argument("--output_dir", default=".")
    args = p.parse_args()
    os.makedirs(args.output_dir, exist_ok=True)
    print("=" * 60)
    print("STEP 9: Statistical Analysis")
    print("=" * 60)

    df = pd.read_parquet(os.path.join(args.output_dir, "feature_engineered.parquet"))
    churned = df[df["is_churned"] == 1]
    retained = df[df["is_churned"] == 0]
    results = []

    # Chi-square for categorical features
    for cat in ["segment", "acquisition_channel", "plan_type"]:
        if cat in df.columns:
            contingency = pd.crosstab(df[cat], df["is_churned"])
            if contingency.shape[0] >= 2 and contingency.shape[1] >= 2:
                chi2, p_val, dof, _ = stats.chi2_contingency(contingency)
                results.append({"test": f"Chi-square: {cat} vs churn", "statistic": round(chi2, 3),
                                "p_value": round(p_val, 6), "significant": p_val < 0.05})
                print(f"📊 {cat} vs churn: χ²={chi2:.2f}, p={p_val:.4f} {'*' if p_val < 0.05 else ''}")

    # T-tests for numerical features
    for col in ["tenure_days", "total_spend", "monthly_fee", "support_contacts", "return_rate",
                "purchase_frequency", "days_since_last_purchase"]:
        if col in df.columns:
            t_stat, p_val = stats.ttest_ind(churned[col].dropna(), retained[col].dropna())
            d = (churned[col].mean() - retained[col].mean()) / \
                np.sqrt((churned[col].std()**2 + retained[col].std()**2) / 2)
            results.append({"test": f"T-test: {col} — churned vs retained",
                            "statistic": round(t_stat, 3), "p_value": round(p_val, 6),
                            "significant": p_val < 0.05, "cohens_d": round(d, 3),
                            "churned_mean": round(churned[col].mean(), 2),
                            "retained_mean": round(retained[col].mean(), 2)})
            print(f"📊 {col}: t={t_stat:.2f}, p={p_val:.4f} {'*' if p_val < 0.05 else ''}"
                  f" (churned={churned[col].mean():.1f} vs retained={retained[col].mean():.1f})")

    # Kaplan-Meier survival curves (simplified)
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # Survival by segment
    if "segment" in df.columns and "tenure_days" in df.columns:
        for seg in df["segment"].unique():
            seg_data = df[df["segment"] == seg]["tenure_days"].sort_values()
            survival = [(len(seg_data) - i) / len(seg_data) for i in range(len(seg_data))]
            axes[0].step(seg_data.values, survival, where="post", label=seg, lw=1.5)
        axes[0].set_title("Survival Curve by Segment")
        axes[0].set_xlabel("Tenure (Days)")
        axes[0].set_ylabel("Survival Probability")
        axes[0].legend(fontsize=8)
        axes[0].set_xlim(0, 1000)

    # Survival by plan type
    if "plan_type" in df.columns and "tenure_days" in df.columns:
        for plan in df["plan_type"].unique():
            plan_data = df[df["plan_type"] == plan]["tenure_days"].sort_values()
            survival = [(len(plan_data) - i) / len(plan_data) for i in range(len(plan_data))]
            axes[1].step(plan_data.values, survival, where="post", label=plan, lw=1.5)
        axes[1].set_title("Survival Curve by Plan Type")
        axes[1].set_xlabel("Tenure (Days)")
        axes[1].set_ylabel("Survival Probability")
        axes[1].legend(fontsize=8)
        axes[1].set_xlim(0, 1000)

    plt.tight_layout()
    fig.savefig(os.path.join(args.output_dir, "step09_statistical.png"), dpi=120)
    plt.close()

    sig = sum(1 for r in results if r.get("significant"))
    print(f"\n📋 {sig}/{len(results)} tests significant at α=0.05")

    with open(os.path.join(args.output_dir, "statistical_tests.json"), "w") as f:
        json.dump({"tests": results, "significant": sig, "total": len(results)}, f, indent=2, default=str)
    print("✅ Step 9 complete")

if __name__ == "__main__":
    main()
