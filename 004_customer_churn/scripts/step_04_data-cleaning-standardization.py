#!/usr/bin/env python3
"""Step 4: Data Cleaning & Standardization."""
import argparse, os, json
import pandas as pd, numpy as np

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--data_dir", default="../data")
    p.add_argument("--output_dir", default=".")
    args = p.parse_args()
    os.makedirs(args.output_dir, exist_ok=True)
    print("=" * 60)
    print("STEP 4: Data Cleaning & Standardization")
    print("=" * 60)

    df = pd.read_parquet(os.path.join(args.output_dir, "merged_data.parquet"))
    print(f"\n📊 Loaded: {len(df)} rows × {len(df.columns)} cols")

    cleaning_log = {"before_nulls": int(df.isnull().sum().sum()), "actions": []}

    # 1. Fill missing values
    for col in df.columns:
        if df[col].isnull().sum() == 0:
            continue
        if df[col].dtype in ['float64', 'int64']:
            df[col] = df[col].fillna(df[col].median())
            cleaning_log["actions"].append(f"Imputed {col} with median")
        else:
            df[col] = df[col].fillna("Unknown")
            cleaning_log["actions"].append(f"Filled {col} with 'Unknown'")

    # 2. Standardize categoricals
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].astype(str).str.strip().str.title()

    # 3. Cap numerical outliers
    for col in df.select_dtypes(include=['float64', 'int64']).columns:
        if col in ['customer_id', 'is_churned'] or df[col].nunique() < 10:
            continue
        p99 = df[col].quantile(0.99)
        capped = (df[col] > p99).sum()
        if capped > 0:
            df[col] = df[col].clip(upper=p99)
            cleaning_log["actions"].append(f"Capped {col} at 99th pctl ({p99:.1f}), {capped} values")

    cleaning_log["after_nulls"] = int(df.isnull().sum().sum())
    df.to_parquet(os.path.join(args.output_dir, "cleaned_data.parquet"), index=False)

    with open(os.path.join(args.output_dir, "cleaning_log.json"), "w") as f:
        json.dump(cleaning_log, f, indent=2)
    print(f"   Nulls: {cleaning_log['before_nulls']} → {cleaning_log['after_nulls']}")
    print("\n✅ Step 4 complete")

if __name__ == "__main__":
    main()
