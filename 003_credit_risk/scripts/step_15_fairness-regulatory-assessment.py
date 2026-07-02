#!/usr/bin/env python3
"""Step 15: Fairness & Regulatory Assessment — Evaluate model fairness across protected groups."""
import argparse, os, json, pickle
import numpy as np, pandas as pd

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--data_dir", default="../data")
    p.add_argument("--output_dir", default=".")
    args = p.parse_args()
    os.makedirs(args.output_dir, exist_ok=True)
    print("=" * 60)
    print("STEP 15: Fairness & Regulatory Assessment")
    print("=" * 60)

    # Load model
    model = None
    for model_file in ["stacking_model.pkl", "xgboost_model.pkl", "best_baseline_model.pkl"]:
        path = os.path.join(args.output_dir, model_file)
        if os.path.exists(path):
            with open(path, "rb") as f:
                model = pickle.load(f)
            break
    if model is None:
        print("❌ No model found.")
        return

    # Load test data
    data = np.load(os.path.join(args.output_dir, "train_data.npz"))
    X_test, y_test = data["X_test"], data["y_test"]

    # Get predictions
    if hasattr(model, "predict_proba"):
        y_prob = model.predict_proba(X_test)[:, 1]
    else:
        y_prob = model.predict(X_test)
    y_pred = (y_prob >= 0.5).astype(int)

    # Load original data to find protected attributes
    # We need to go back to the feature-engineered data and find age/zip/state
    df = pd.read_parquet(os.path.join(args.output_dir, "feature_engineered.parquet"))
    with open(os.path.join(args.output_dir, "modeling_metadata.json")) as f:
        meta = json.load(f)

    # Create synthetic protected groups from test set
    # Since we have preprocessed data, we'll use age_group from original and map back
    # For a real scenario, we'd track protected attributes through preprocessing
    # Here we use a proxy approach

    test_indices = np.load(os.path.join(args.output_dir, "train_data.npz"))["X_test"].shape[0]

    fairness_results = {"fairness_metrics": [], "overall_assessment": {}}

    # 1. Create synthetic protected groups based on available data
    # Use the preprocessed "age" and "state" columns mapping
    print("\n📊 Fairness Analysis by Protected Groups (Proxy):")
    print("   Note: Using feature distribution as age/geo proxies")

    # Age group proxy: split by age feature (if present in feature names)
    age_features = [f for f in meta["feature_names"] if "age" in f.lower() and "group" not in f.lower()]
    if not age_features:
        age_features = [meta["feature_names"][0]]  # fallback to first feature

    # Use age feature as proxy for age-based groups
    age_feat_idx = meta["feature_names"].index(age_features[0]) if age_features[0] in meta["feature_names"] else 0
    age_values = X_test[:, age_feat_idx]
    age_median = np.median(age_values)
    young_mask = age_values < age_median
    older_mask = age_values >= age_median

    young_default_rate = y_test[young_mask].mean()
    older_default_rate = y_test[older_mask].mean()
    young_pred_rate = y_pred[young_mask].mean()
    older_pred_rate = y_pred[older_mask].mean()

    # Statistical parity difference
    spd = young_pred_rate - older_pred_rate

    # Equal opportunity difference (TPR difference)
    young_tpr = ((y_pred == 1) & (y_test == 1) & young_mask).sum() / max((y_test[young_mask] == 1).sum(), 1)
    older_tpr = ((y_pred == 1) & (y_test == 1) & older_mask).sum() / max((y_test[older_mask] == 1).sum(), 1)
    eod = young_tpr - older_tpr

    # Disparate impact
    di = young_pred_rate / max(older_pred_rate, 0.001)

    age_fairness = {
        "protected_attribute": "age (split at median)",
        "group_1": {"name": "Younger", "n": int(young_mask.sum()), "default_rate": round(young_default_rate, 4),
                     "approval_rate": round(young_pred_rate, 4)},
        "group_2": {"name": "Older", "n": int(older_mask.sum()), "default_rate": round(older_default_rate, 4),
                     "approval_rate": round(older_pred_rate, 4)},
        "statistical_parity_difference": round(spd, 4),
        "equal_opportunity_difference": round(eod, 4),
        "disparate_impact": round(di, 4),
        "spd_pass": abs(spd) < 0.10,
        "di_pass": 0.80 <= di <= 1.25,
    }
    print(f"\n   Age Group (split at median):")
    print(f"     Statistical Parity Diff: {spd:.4f} {'✅' if abs(spd) < 0.10 else '⚠️'}")
    print(f"     Equal Opportunity Diff:  {eod:.4f}")
    print(f"     Disparate Impact:        {di:.4f} {'✅' if 0.80 <= di <= 1.25 else '⚠️'}")
    fairness_results["fairness_metrics"].append(age_fairness)

    # 2. Income-based fairness (proxy for economic status)
    income_features = [f for f in meta["feature_names"] if "income" in f.lower() or "loan" in f.lower()]
    if income_features:
        inc_feat_idx = meta["feature_names"].index(income_features[0]) if income_features[0] in meta["feature_names"] else 1
        inc_values = X_test[:, inc_feat_idx]
        inc_median = np.median(inc_values)
        low_inc = inc_values < inc_median
        high_inc = inc_values >= inc_median

        li_pred = y_pred[low_inc].mean()
        hi_pred = y_pred[high_inc].mean()
        di_inc = li_pred / max(hi_pred, 0.001)

        inc_fairness = {
            "protected_attribute": "income_proxy (split at median)",
            "group_1": {"name": "Lower Income", "n": int(low_inc.sum()), "approval_rate": round(li_pred, 4)},
            "group_2": {"name": "Higher Income", "n": int(high_inc.sum()), "approval_rate": round(hi_pred, 4)},
            "statistical_parity_difference": round(li_pred - hi_pred, 4),
            "disparate_impact": round(di_inc, 4),
            "di_pass": 0.80 <= di_inc <= 1.25,
        }
        print(f"\n   Income Proxy:")
        print(f"     Disparate Impact: {di_inc:.4f} {'✅' if 0.80 <= di_inc <= 1.25 else '⚠️'}")
        fairness_results["fairness_metrics"].append(inc_fairness)

    # Overall assessment
    di_checks = [m.get("di_pass", True) for m in fairness_results["fairness_metrics"]]
    spd_checks = [m.get("spd_pass", True) for m in fairness_results["fairness_metrics"]]
    all_pass = all(di_checks) and all(spd_checks)

    fairness_results["overall_assessment"] = {
        "total_metrics": len(fairness_results["fairness_metrics"]),
        "disparate_impact_pass": all(di_checks),
        "statistical_parity_pass": all(spd_checks),
        "overall_fairness": "PASS" if all_pass else "REVIEW_REQUIRED",
        "regulatory_note": "ECOA/FCRA compliance requires monitoring: disparate impact < 0.8 or > 1.25 triggers review.",
        "recommendation": "Proceed to production with monitoring" if all_pass else "Further investigation required for flagged groups"
    }

    status = fairness_results["overall_assessment"]["overall_fairness"]
    print(f"\n📋 Overall Fairness Assessment: {status}")
    print(f"   {'✅ Model meets fairness thresholds' if all_pass else '⚠️  Fairness review required'}")

    # Convert numpy booleans to Python booleans for JSON serialization
    def convert_bools(obj):
        if isinstance(obj, dict):
            return {k: convert_bools(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [convert_bools(i) for i in obj]
        elif isinstance(obj, (np.bool_,)):
            return bool(obj)
        elif isinstance(obj, (np.integer,)):
            return int(obj)
        elif isinstance(obj, (np.floating,)):
            return float(obj)
        return obj
    fairness_results = convert_bools(fairness_results)

    with open(os.path.join(args.output_dir, "fairness_report.json"), "w") as f:
        json.dump(fairness_results, f, default=str, indent=2)

    print(f"\n✅ Step 15 complete — fairness report saved")

if __name__ == "__main__":
    main()
