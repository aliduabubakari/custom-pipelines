#!/usr/bin/env python3
"""Step 2: Data Merging & Integration — Aggregate credit history and merge all sources."""
import argparse, os, json
import pandas as pd, numpy as np

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--data_dir", default="../data")
    p.add_argument("--output_dir", default=".")
    args = p.parse_args()
    os.makedirs(args.output_dir, exist_ok=True)
    print("=" * 60)
    print("STEP 2: Data Merging & Integration")
    print("=" * 60)

    # Load
    apps = pd.read_csv(os.path.join(args.data_dir, "applications.csv"))
    with open(os.path.join(args.data_dir, "credit_history.json")) as f:
        history = pd.DataFrame(json.load(f))
    bureau = pd.read_excel(os.path.join(args.data_dir, "bureau_data.xlsx"))

    # Aggregate credit history per application
    print(f"\n📋 Aggregating {len(history)} credit history records across {history['application_id'].nunique()} applications...")
    hist_agg = history.groupby("application_id").agg(
        n_accounts=("account_status", "count"),
        avg_balance=("balance", "mean"),
        max_balance=("balance", "max"),
        avg_utilization=("utilization_pct", "mean"),
        max_utilization=("utilization_pct", "max"),
        pct_accounts_delinquent=("account_status", lambda x: (x.isin(["Late (30 days)", "Late (60 days)", "Late (90+ days)", "Charge-off"])).mean() * 100),
        has_charge_off=("account_status", lambda x: int(any(s == "Charge-off" for s in x))),
        has_90plus_delinquency=("account_status", lambda x: int(any(s == "Late (90+ days)" for s in x))),
        latest_report_date=("report_date", "max"),
        earliest_report_date=("report_date", "min"),
    ).reset_index()

    # Merge: applications ← aggregated history
    merged = apps.merge(hist_agg, on="application_id", how="left")
    print(f"   After history merge: {len(merged)} rows")

    # Merge: ← bureau data
    merged = merged.merge(bureau, on="application_id", how="left", suffixes=("", "_bureau_drop"))
    # Drop duplicate columns from bureau merge
    drop_cols = [c for c in merged.columns if c.endswith("_bureau_drop")]
    if drop_cols:
        merged = merged.drop(columns=drop_cols)
    print(f"   After bureau merge: {len(merged)} rows × {len(merged.columns)} cols")

    # Fill nulls in merged columns (applications without history/bureau records)
    null_counts = merged.isnull().sum()
    null_cols = null_counts[null_counts > 0]
    if len(null_cols) > 0:
        print(f"\n⚠️  {len(null_cols)} columns have nulls after merge:")
        for col, cnt in null_cols.items():
            print(f"   - {col}: {cnt} nulls ({cnt/len(merged)*100:.1f}%)")

    # Save merged dataset
    merged.to_parquet(os.path.join(args.output_dir, "merged_data.parquet"), index=False)
    merged.to_csv(os.path.join(args.output_dir, "merged_data.csv"), index=False)

    # Merge summary
    summary = {
        "applications": len(apps),
        "credit_history_records": len(history),
        "unique_apps_in_history": history["application_id"].nunique(),
        "bureau_records": len(bureau),
        "final_rows": len(merged),
        "final_columns": len(merged.columns),
        "merged_successfully": len(apps) == len(merged),
        "columns_with_nulls": {c: int(cnt) for c, cnt in merged.isnull().sum().items() if cnt > 0}
    }
    with open(os.path.join(args.output_dir, "merge_summary.json"), "w") as f:
        json.dump(summary, f, indent=2, default=str)

    print(f"\n✅ Step 2 complete — merged dataset: {len(merged)} rows × {len(merged.columns)} cols")

if __name__ == "__main__":
    main()
