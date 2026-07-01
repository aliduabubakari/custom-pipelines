#!/usr/bin/env python3
"""Step 3: Data Cleaning & Standardization — Handle nulls, standardize, cap outliers."""
import argparse, os, json
import pandas as pd, numpy as np

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--data_dir", default="../data")
    p.add_argument("--output_dir", default=".")
    args = p.parse_args()
    os.makedirs(args.output_dir, exist_ok=True)
    print("=" * 60)
    print("STEP 3: Data Cleaning & Standardization")
    print("=" * 60)

    # Load merged data from step 2 (or data_dir)
    merged_path = os.path.join(args.output_dir, "merged_data.parquet")
    if os.path.exists(merged_path):
        df = pd.read_parquet(merged_path)
    else:
        # Fallback: load from data_dir
        df = pd.read_csv(os.path.join(args.data_dir, "applications.csv"))
    print(f"\n📊 Loaded: {len(df)} rows × {len(df.columns)} cols")

    cleaning_log = {"before_nulls": {}, "after_nulls": {}, "outlier_cols_capped": [], "standardizations": []}

    # Record before state
    cleaning_log["before_nulls"] = {c: int(v) for c, v in df.isnull().sum().items() if v > 0}

    # 1. Handle missing values
    for col in df.columns:
        if df[col].isnull().sum() == 0:
            continue
        if df[col].dtype in ['float64', 'int64']:
            df[col] = df[col].fillna(df[col].median())
            cleaning_log.setdefault("imputed_numerical", []).append(col)
        else:
            df[col] = df[col].fillna("Unknown")
            cleaning_log.setdefault("imputed_categorical", []).append(col)

    # 2. Standardize categoricals
    cat_standardizations = {
        "employment_length": {"< 1 year": "<1 year", "10+ years": "10+ years"},
    }
    for col, mapping in cat_standardizations.items():
        if col in df.columns:
            df[col] = df[col].replace(mapping)
            cleaning_log["standardizations"].append(f"{col}: normalized {len(mapping)} categories")

    # Trim whitespace from all string columns
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].astype(str).str.strip()
    cleaning_log["standardizations"].append("all string columns: whitespace trimmed")

    # 3. Cap outliers at 99th percentile for numerical columns
    numerical_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
    exclude_from_cap = ['default_flag', 'application_id']
    for col in numerical_cols:
        if col in exclude_from_cap or df[col].nunique() < 10:
            continue
        p99 = df[col].quantile(0.99)
        n_capped = (df[col] > p99).sum()
        if n_capped > 0:
            df[col] = df[col].clip(upper=p99)
            cleaning_log["outlier_cols_capped"].append(f"{col}: {n_capped} values capped at {p99:.1f} (99th pctl)")

    # Record after state
    cleaning_log["after_nulls"] = {c: int(v) for c, v in df.isnull().sum().items() if v > 0}

    # Save
    df.to_parquet(os.path.join(args.output_dir, "cleaned_data.parquet"), index=False)

    with open(os.path.join(args.output_dir, "cleaning_log.json"), "w") as f:
        json.dump(cleaning_log, f, indent=2, default=str)

    # Report
    print(f"\n🧹 Nulls resolved: {sum(cleaning_log['before_nulls'].values())} → {sum(cleaning_log['after_nulls'].values())}")
    print(f"   Imputed numerical: {len(cleaning_log.get('imputed_numerical', []))} cols")
    print(f"   Imputed categorical: {len(cleaning_log.get('imputed_categorical', []))} cols")
    print(f"   Outlier-capped: {len(cleaning_log['outlier_cols_capped'])} cols")
    print(f"\n✅ Step 3 complete — cleaned data saved")

if __name__ == "__main__":
    main()
