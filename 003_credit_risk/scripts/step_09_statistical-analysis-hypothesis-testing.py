#!/usr/bin/env python3
"""Step 9: Statistical Analysis & Hypothesis Testing."""
import argparse, os, json
import pandas as pd, numpy as np
from scipy import stats

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--data_dir", default="../data")
    p.add_argument("--output_dir", default=".")
    args = p.parse_args()
    os.makedirs(args.output_dir, exist_ok=True)
    print("=" * 60)
    print("STEP 9: Statistical Analysis & Hypothesis Testing")
    print("=" * 60)

    df = pd.read_parquet(os.path.join(args.output_dir, "feature_engineered.parquet"))
    default = df[df["default_flag"] == 1]
    non_default = df[df["default_flag"] == 0]
    results = []

    # H1: FICO score significantly differs between defaulted and non-defaulted (t-test)
    if "fico_score" in df.columns:
        t_stat, p_val = stats.ttest_ind(default["fico_score"].dropna(), non_default["fico_score"].dropna())
        cohens_d = (default["fico_score"].mean() - non_default["fico_score"].mean()) / \
                   np.sqrt((default["fico_score"].std()**2 + non_default["fico_score"].std()**2) / 2)
        results.append({
            "hypothesis": "H1: FICO score differs between defaulted/non-defaulted",
            "test": "Independent t-test",
            "statistic": round(t_stat, 4),
            "p_value": round(p_val, 6),
            "significant": p_val < 0.05,
            "effect_size_cohens_d": round(cohens_d, 3),
            "default_mean": round(default["fico_score"].mean(), 1),
            "non_default_mean": round(non_default["fico_score"].mean(), 1)
        })
        print(f"\n📊 H1: FICO score — t={t_stat:.2f}, p={p_val:.6f}, d={cohens_d:.3f}")
        print(f"   Default mean: {default['fico_score'].mean():.0f} | Non-default: {non_default['fico_score'].mean():.0f}")

    # H2: DTI > 43 increases default odds (chi-square)
    if "dti_ratio" in df.columns:
        df["high_dti"] = (df["dti_ratio"] > 43).astype(int)
        contingency = pd.crosstab(df["high_dti"], df["default_flag"])
        if contingency.shape == (2, 2):
            chi2, p_val, dof, expected = stats.chi2_contingency(contingency)
            odds_ratio = (contingency.iloc[1, 1] * contingency.iloc[0, 0]) / \
                        (contingency.iloc[1, 0] * contingency.iloc[0, 1]) if contingency.iloc[1, 0] * contingency.iloc[0, 1] > 0 else float('inf')
            results.append({
                "hypothesis": "H2: DTI > 43 increases default odds",
                "test": "Chi-square test",
                "statistic": round(chi2, 4),
                "p_value": round(p_val, 6),
                "significant": p_val < 0.05,
                "odds_ratio": round(odds_ratio, 3),
                "contingency": contingency.to_dict()
            })
            print(f"\n📊 H2: DTI > 43 — χ²={chi2:.2f}, p={p_val:.6f}, OR={odds_ratio:.2f}")

    # H3: Employment length < 2 years increases risk (proportions z-test)
    if "employment_length" in df.columns:
        short_emp = df[df["employment_length"].isin(["<1 year", "1-3 years", "Unknown"])]
        long_emp = df[~df["employment_length"].isin(["<1 year", "1-3 years", "Unknown"])]
        p1, p2 = short_emp["default_flag"].mean(), long_emp["default_flag"].mean()
        n1, n2 = len(short_emp), len(long_emp)
        p_pool = (short_emp["default_flag"].sum() + long_emp["default_flag"].sum()) / (n1 + n2)
        se = np.sqrt(p_pool * (1 - p_pool) * (1/n1 + 1/n2))
        z_stat = (p1 - p2) / se if se > 0 else 0
        p_val = 2 * (1 - stats.norm.cdf(abs(z_stat)))
        results.append({
            "hypothesis": "H3: Short employment (< 3 years) increases default risk",
            "test": "Two-proportion z-test",
            "statistic": round(z_stat, 4),
            "p_value": round(p_val, 6),
            "significant": p_val < 0.05,
            "short_emp_default_rate": round(p1 * 100, 2),
            "long_emp_default_rate": round(p2 * 100, 2),
            "rate_difference_pct": round((p1 - p2) * 100, 2)
        })
        print(f"\n📊 H3: Employment — z={z_stat:.2f}, p={p_val:.6f}")
        print(f"   Short emp default: {p1*100:.1f}% | Long emp: {p2*100:.1f}%")

    # Summary
    sig_count = sum(1 for r in results if r["significant"])
    print(f"\n{'─' * 40}")
    print(f"📋 Results: {sig_count}/{len(results)} hypotheses significant at α=0.05")

    with open(os.path.join(args.output_dir, "statistical_tests.json"), "w") as f:
        json.dump({"hypotheses": results, "significant_count": sig_count, "total_tests": len(results)}, f, indent=2, default=str)

    print(f"\n✅ Step 9 complete — statistical test results saved")

if __name__ == "__main__":
    main()
