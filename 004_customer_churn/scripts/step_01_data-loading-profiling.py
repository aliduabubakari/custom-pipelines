#!/usr/bin/env python3
"""Step 1: Data Loading & Profiling — Load customer profiles and transaction history."""
import argparse, os, json
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
    print("STEP 1: Data Loading & Profiling")
    print("=" * 60)

    # Load data
    cust = pd.read_csv(os.path.join(args.data_dir, "customers.csv"))
    with open(os.path.join(args.data_dir, "transactions.json")) as f:
        trans = pd.DataFrame(json.load(f))

    # Profile customers
    print(f"\n📊 CUSTOMERS: {len(cust)} profiles, {len(cust.columns)} columns")
    print(f"   Columns: {', '.join(cust.columns.tolist())}")
    print(f"   Churn rate: {cust['is_churned'].mean()*100:.1f}%")
    print(f"   Segments: {cust['segment'].value_counts().to_dict()}")
    print(f"   Nulls: {cust.isnull().sum().sum()} total")

    # Profile transactions
    print(f"\n📊 TRANSACTIONS: {len(trans)} records across {trans['customer_id'].nunique()} customers")
    print(f"   Date range: {trans['transaction_date'].min()} to {trans['transaction_date'].max()}")
    print(f"   Avg order value: ${trans['amount'].mean():.2f}")
    print(f"   Return rate: {trans['is_return'].mean()*100:.1f}%")
    print(f"   Categories: {trans['category'].nunique()}")

    # Save profiling summary
    profiling = {
        "customers": {"rows": len(cust), "churn_rate": round(cust["is_churned"].mean(), 4),
                       "segments": cust["segment"].value_counts().to_dict()},
        "transactions": {"rows": len(trans), "unique_customers": trans["customer_id"].nunique(),
                          "avg_amount": round(trans["amount"].mean(), 2),
                          "return_rate": round(trans["is_return"].mean(), 4)},
        "target": "is_churned"
    }
    with open(os.path.join(args.output_dir, "profiling_summary.json"), "w") as f:
        json.dump(profiling, f, indent=2, default=str)

    # Save raw parquet
    cust.to_parquet(os.path.join(args.output_dir, "raw_customers.parquet"), index=False)
    trans.to_parquet(os.path.join(args.output_dir, "raw_transactions.parquet"), index=False)

    # Viz: churn by segment and plan
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    cust.groupby("segment")["is_churned"].mean().sort_values().plot(kind="barh", ax=axes[0], color="#e74c3c", edgecolor="white")
    axes[0].set_title("Churn Rate by Segment")
    axes[0].set_xlabel("Churn Rate")
    cust.groupby("plan_type")["is_churned"].mean().sort_values().plot(kind="barh", ax=axes[1], color="#3498db", edgecolor="white")
    axes[1].set_title("Churn Rate by Plan Type")
    axes[1].set_xlabel("Churn Rate")
    plt.tight_layout()
    fig.savefig(os.path.join(args.output_dir, "step01_profiling.png"), dpi=100)
    plt.close()
    print("\n✅ Step 1 complete")

if __name__ == "__main__":
    main()
