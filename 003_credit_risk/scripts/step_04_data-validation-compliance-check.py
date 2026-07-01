#!/usr/bin/env python3
"""Step 4: Data Validation & Compliance Check — Validate fields for regulatory readiness."""
import argparse, os, json
import pandas as pd, numpy as np

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--data_dir", default="../data")
    p.add_argument("--output_dir", default=".")
    args = p.parse_args()
    os.makedirs(args.output_dir, exist_ok=True)
    print("=" * 60)
    print("STEP 4: Data Validation & Compliance Check")
    print("=" * 60)

    # Load cleaned data
    df = pd.read_parquet(os.path.join(args.output_dir, "cleaned_data.parquet"))
    compliance = {"checks": [], "flags": [], "summary": {}}

    # Check 1: Required fields completeness
    required_fields = ["application_id", "annual_income", "loan_amount", "fico_score", "dti_ratio", "age"]
    for field in required_fields:
        present = field in df.columns
        null_count = int(df[field].isnull().sum()) if present else len(df)
        check = {
            "check": f"Required field: {field}",
            "present": present,
            "null_count": null_count,
            "pass": present and null_count == 0
        }
        compliance["checks"].append(check)
        if not check["pass"]:
            compliance["flags"].append(f"MISSING: {field} has {null_count} nulls")

    # Check 2: Value range validations
    range_checks = {
        "annual_income": (0, 5_000_000),  # Reasonable income range
        "loan_amount": (0, 2_000_000),
        "fico_score": (300, 850),
        "dti_ratio": (0, 100),
        "age": (18, 120),
        "revolving_utilization": (0, 150),
    }
    for col, (lo, hi) in range_checks.items():
        if col not in df.columns:
            continue
        outliers = ((df[col] < lo) | (df[col] > hi)).sum()
        check = {
            "check": f"Range validation: {col} in [{lo}, {hi}]",
            "outliers": int(outliers),
            "outlier_pct": round(outliers / len(df) * 100, 2),
            "pass": outliers == 0
        }
        compliance["checks"].append(check)
        if not check["pass"]:
            compliance["flags"].append(f"RANGE: {col} has {outliers} values outside [{lo}, {hi}]")

    # Check 3: Default rate reasonableness
    default_rate = df["default_flag"].mean()
    compliance["checks"].append({
        "check": "Default rate reasonableness (2%–40%)",
        "actual_rate": round(default_rate * 100, 2),
        "pass": 0.02 <= default_rate <= 0.40
    })

    # Check 4: No duplicate application IDs
    dupes = df["application_id"].duplicated().sum()
    compliance["checks"].append({
        "check": "No duplicate application IDs",
        "duplicates": int(dupes),
        "pass": dupes == 0
    })

    # Summary
    passed = sum(c["pass"] for c in compliance["checks"])
    failed = len(compliance["checks"]) - passed
    compliance["summary"] = {
        "total_checks": len(compliance["checks"]),
        "passed": passed,
        "failed": failed,
        "overall_status": "PASS" if failed == 0 else "FAIL",
        "records_reviewed": len(df),
        "flags_raised": len(compliance["flags"])
    }

    with open(os.path.join(args.output_dir, "compliance_report.json"), "w") as f:
        json.dump(compliance, f, indent=2, default=str)

    status = compliance["summary"]["overall_status"]
    print(f"\n📋 {len(compliance['checks'])} checks run: {passed} ✅ passed, {failed} ❌ failed")
    print(f"   Overall Status: {status}")
    if compliance["flags"]:
        print("   Flags:")
        for flag in compliance["flags"]:
            print(f"     ⚠️  {flag}")

    print(f"\n✅ Step 4 complete — compliance report saved")

if __name__ == "__main__":
    main()
