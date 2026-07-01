#!/usr/bin/env python3
"""Step 5: Feature Engineering — Create risk features for credit modeling."""
import argparse, os, json
import pandas as pd, numpy as np

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--data_dir", default="../data")
    p.add_argument("--output_dir", default=".")
    args = p.parse_args()
    os.makedirs(args.output_dir, exist_ok=True)
    print("=" * 60)
    print("STEP 5: Feature Engineering")
    print("=" * 60)

    df = pd.read_parquet(os.path.join(args.output_dir, "cleaned_data.parquet"))
    initial_cols = len(df.columns)
    features_created = []

    # 1. DTI Category (Debt-to-Income risk bands)
    if "dti_ratio" in df.columns:
        df["DTI_category"] = pd.cut(df["dti_ratio"],
            bins=[-0.01, 20, 35, 43, 100],
            labels=["Low", "Medium", "High", "Very High"])
        features_created.append("DTI_category (4 bands)")

    # 2. FICO Score Band
    if "fico_score" in df.columns:
        df["FICO_band"] = pd.cut(df["fico_score"],
            bins=[299, 579, 669, 739, 799, 851],
            labels=["Poor", "Fair", "Good", "Very Good", "Exceptional"])
        features_created.append("FICO_band (5 tiers)")

    # 3. Employment Stability (tenure / age ratio proxy)
    if "months_at_address" in df.columns and "age" in df.columns:
        df["address_stability"] = (df["months_at_address"] / 12 / df["age"].clip(lower=18)).clip(0, 3)
        features_created.append("address_stability (months_at_address / age)")

    # 4. Credit Utilization (already present, just normalize)
    if "revolving_utilization" in df.columns:
        df["utilization_normalized"] = df["revolving_utilization"].clip(0, 150) / 100
        features_created.append("utilization_normalized (0–1.5 scale)")

    # 5. Inquiry Velocity (inquiries per month proxy)
    if "inquiries_6mo" in df.columns:
        df["inquiry_velocity"] = df["inquiries_6mo"] / 6
        features_created.append("inquiry_velocity (inquiries/month)")

    # 6. Account age diversity
    if "oldest_account_months" in df.columns and "credit_age_months" in df.columns:
        df["account_age_ratio"] = np.where(df["credit_age_months"] > 0,
            df["oldest_account_months"] / df["credit_age_months"], 0)
        features_created.append("account_age_ratio")

    # 7. Payment consistency score (from credit history aggregation)
    if "pct_accounts_delinquent" in df.columns:
        df["payment_consistency"] = 100 - df["pct_accounts_delinquent"].fillna(0)
        features_created.append("payment_consistency (100 - delinquency%)")

    # 8. Income-to-loan ratio
    if "annual_income" in df.columns and "loan_amount" in df.columns:
        df["income_loan_ratio"] = (df["annual_income"] / df["loan_amount"].clip(lower=100)).clip(0, 50)
        features_created.append("income_loan_ratio")

    # 9. Loan amount category
    if "loan_amount" in df.columns:
        df["loan_size"] = pd.cut(df["loan_amount"],
            bins=[0, 10_000, 25_000, 50_000, 1_000_000],
            labels=["Micro", "Small", "Medium", "Large"])
        features_created.append("loan_size (4 tiers)")

    # 10. Age group
    if "age" in df.columns:
        df["age_group"] = pd.cut(df["age"],
            bins=[17, 25, 35, 50, 65, 120],
            labels=["18-25", "26-35", "36-50", "51-65", "65+"])
        features_created.append("age_group (5 tiers)")

    new_cols = len(df.columns) - initial_cols
    print(f"\n🔧 Created {new_cols} new features:")
    for f in features_created:
        print(f"   ✓ {f}")

    # Save feature-engineered dataset
    df.to_parquet(os.path.join(args.output_dir, "feature_engineered.parquet"), index=False)

    # Feature engineering log
    with open(os.path.join(args.output_dir, "feature_engineering_log.json"), "w") as f:
        json.dump({
            "initial_columns": initial_cols,
            "new_features": new_cols,
            "features_created": features_created,
            "final_columns": len(df.columns)
        }, f, indent=2)

    print(f"\n✅ Step 5 complete — {len(df.columns)} total columns ({len(df)} rows)")

if __name__ == "__main__":
    main()
