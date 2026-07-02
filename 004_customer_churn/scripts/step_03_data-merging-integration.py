#!/usr/bin/env python3
"""Step 3: Data Merging & Integration — Merge aggregated transactions with customer profiles."""
import argparse, os, json
import pandas as pd, numpy as np

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--data_dir", default="../data")
    p.add_argument("--output_dir", default=".")
    args = p.parse_args()
    os.makedirs(args.output_dir, exist_ok=True)
    print("=" * 60)
    print("STEP 3: Data Merging & Integration")
    print("=" * 60)

    cust = pd.read_csv(os.path.join(args.data_dir, "customers.csv"))
    metrics = pd.read_parquet(os.path.join(args.output_dir, "customer_metrics.parquet"))

    # Merge
    merged = cust.merge(metrics, on="customer_id", how="left")
    print(f"\n📊 Merged: {len(merged)} rows (customers: {len(cust)}, metrics: {len(metrics)})")

    # Flags for customers with no transactions
    no_txn = merged["purchase_count"].isna().sum()
    if no_txn > 0:
        print(f"   ⚠️  {no_txn} customers have no transactions — filling with zeros")
        fill_zero = ["total_spend", "avg_order_value", "purchase_count", "items_per_order_avg",
                      "return_rate", "discount_usage_rate", "category_diversity", "purchase_frequency"]
        for col in fill_zero:
            if col in merged.columns:
                merged[col] = merged[col].fillna(0)
        merged["days_since_last_purchase"] = merged["days_since_last_purchase"].fillna(999)

    # Verify merge completeness
    print(f"   All customers matched: {merged['customer_id'].nunique() == len(cust)}")
    print(f"   Churn rate preserved: {merged['is_churned'].mean()*100:.1f}%")

    merged.to_parquet(os.path.join(args.output_dir, "merged_data.parquet"), index=False)

    with open(os.path.join(args.output_dir, "merge_summary.json"), "w") as f:
        json.dump({"total_rows": len(merged), "customers_without_transactions": int(no_txn)}, f, default=str)
    print("\n✅ Step 3 complete")

if __name__ == "__main__":
    main()
