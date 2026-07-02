#!/usr/bin/env python3
"""Step 2: Data Aggregation — Aggregate transaction metrics per customer."""
import argparse, os, json
import pandas as pd, numpy as np

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--data_dir", default="../data")
    p.add_argument("--output_dir", default=".")
    args = p.parse_args()
    os.makedirs(args.output_dir, exist_ok=True)
    print("=" * 60)
    print("STEP 2: Data Aggregation — Customer Metrics")
    print("=" * 60)

    with open(os.path.join(args.data_dir, "transactions.json")) as f:
        trans = pd.DataFrame(json.load(f))

    print(f"\n📊 Aggregating {len(trans)} transactions...")

    trans["transaction_date"] = pd.to_datetime(trans["transaction_date"])
    max_date = trans["transaction_date"].max()

    # Aggregate per customer
    agg = trans.groupby("customer_id").agg(
        total_spend=("amount", "sum"),
        avg_order_value=("amount", "mean"),
        purchase_count=("transaction_id", "count"),
        days_since_last_purchase=("transaction_date", lambda x: (max_date - x.max()).days),
        items_per_order_avg=("items_count", "mean"),
        return_rate=("is_return", "mean"),
        discount_usage_rate=("discount_applied", lambda x: (x > 0).mean()),
        category_diversity=("category", "nunique"),
        first_purchase=("transaction_date", "min"),
        last_purchase=("transaction_date", "max"),
    ).reset_index()

    agg["purchase_frequency"] = agg["purchase_count"] / \
        np.maximum((agg["last_purchase"] - agg["first_purchase"]).dt.days / 30, 1)
    agg["total_spend"] = agg["total_spend"].round(2)
    agg["avg_order_value"] = agg["avg_order_value"].round(2)

    print(f"   Aggregated: {len(agg)} customers with metrics")
    print(f"   Avg spend: ${agg['total_spend'].mean():.0f} | Avg orders: {agg['purchase_count'].mean():.1f}")
    print(f"   Avg return rate: {agg['return_rate'].mean()*100:.1f}% | Avg categories: {agg['category_diversity'].mean():.1f}")

    agg.to_parquet(os.path.join(args.output_dir, "customer_metrics.parquet"), index=False)
    with open(os.path.join(args.output_dir, "aggregation_summary.json"), "w") as f:
        json.dump({"n_customers_aggregated": len(agg), "metrics_columns": len(agg.columns)}, f, default=str)
    print("\n✅ Step 2 complete")

if __name__ == "__main__":
    main()
