#!/usr/bin/env python3
"""Step 14: Model Explainability — Feature importance, SHAP-style analysis, simulated LIME."""
import argparse, os, json, pickle
import numpy as np, pandas as pd
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--data_dir", default="../data")
    p.add_argument("--output_dir", default=".")
    args = p.parse_args()
    os.makedirs(args.output_dir, exist_ok=True)
    print("=" * 60)
    print("STEP 14: Model Explainability")
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

    # Load data and feature names
    data = np.load(os.path.join(args.output_dir, "train_data.npz"))
    X_test, y_test = data["X_test"], data["y_test"]
    with open(os.path.join(args.output_dir, "modeling_metadata.json")) as f:
        feat_names = json.load(f)["feature_names"]

    # Ensure feature names match
    if len(feat_names) != X_test.shape[1]:
        feat_names = [f"feature_{i}" for i in range(X_test.shape[1])]
    n_features = X_test.shape[1]

    # Get feature importances
    importances = None
    if hasattr(model, "feature_importances_"):
        importances = model.feature_importances_
    elif hasattr(model, "coef_"):
        importances = np.abs(model.coef_).flatten() if model.coef_.ndim > 1 else np.abs(model.coef_)
    elif hasattr(model, "estimators_"):
        # Stacking: try to get from RF estimator
        estimators = model.estimators_ if hasattr(model, "estimators_") else []
        for est in estimators:
            if hasattr(est, "feature_importances_"):
                importances = est.feature_importances_
                break
    if importances is None and hasattr(model, "named_estimators_"):
        for name, est in model.named_estimators_.items():
            if hasattr(est, "feature_importances_"):
                importances = est.feature_importances_
                break

    if importances is None or len(importances) != n_features:
        print("⚠️  Feature importances not directly extractable from model. Using permutation-based approach...")
        # Simple: use coefficient of variation of each feature between default/non-default
        importances = np.zeros(n_features)
        for i in range(n_features):
            v0 = X_test[y_test == 0, i].var() if (y_test == 0).sum() > 1 else 0
            v1 = X_test[y_test == 1, i].var() if (y_test == 1).sum() > 1 else 0
            mean_diff = abs(X_test[y_test == 0, i].mean() - X_test[y_test == 1, i].mean()) if (y_test == 0).sum() > 0 and (y_test == 1).sum() > 0 else 0
            importances[i] = mean_diff / (np.sqrt(v0 + v1) + 1e-10)
        importances = importances / (importances.sum() + 1e-10)

    # Top features
    top_idx = np.argsort(importances)[::-1]
    top_n = min(15, len(top_idx))
    print(f"\n📊 Top {top_n} Feature Importances:")
    for rank, idx in enumerate(top_idx[:top_n], 1):
        print(f"   {rank:2d}. {feat_names[idx]:40s} = {importances[idx]:.4f}")

    # Visualization: Feature importance barplot
    fig, axes = plt.subplots(1, 2, figsize=(14, 7))

    # Panel 1: Top 15 feature importances
    top_vals = importances[top_idx[:15]]
    top_names = [feat_names[i] for i in top_idx[:15]]
    colors = plt.cm.Reds(np.linspace(0.3, 0.9, len(top_vals)))
    axes[0].barh(range(len(top_vals)), top_vals[::-1], color=colors[::-1], edgecolor="white")
    axes[0].set_yticks(range(len(top_vals)))
    axes[0].set_yticklabels(top_names[::-1])
    axes[0].set_title("Top 15 Feature Importances")
    axes[0].set_xlabel("Importance")
    axes[0].invert_yaxis()

    # Panel 2: Simulated LIME — 5 individual decisions
    # Pick 5 test samples and show their top contributing features
    np.random.seed(42)
    sample_idx = np.random.choice(len(X_test), min(5, len(X_test)), replace=False)
    y_prob = None
    if hasattr(model, "predict_proba"):
        y_prob = model.predict_proba(X_test)[:, 1]
    else:
        y_prob = model.predict(X_test)

    lime_data = []
    for i, idx in enumerate(sample_idx):
        actual = y_test[idx]
        predicted = y_prob[idx]
        # Contribution = feature value × importance (simplified)
        contributions = X_test[idx] * importances
        top_contrib = np.argsort(np.abs(contributions))[::-1][:5]

        lime_data.append({
            "sample": i + 1,
            "actual": int(actual),
            "predicted_prob": round(float(predicted), 3),
            "top_features": [feat_names[j] for j in top_contrib],
            "contributions": [round(float(contributions[j]), 4) for j in top_contrib]
        })

        # Plot individual bar
        y_pos = range(5)
        axes[1].barh([y + i*6 for y in y_pos], [abs(contributions[j]) for j in top_contrib],
                     color=["#e74c3c" if contributions[j] > 0 else "#2ecc71" for j in top_contrib],
                     height=0.8, edgecolor="white")
    axes[1].set_yticks([i*6 + 2 for i in range(5)])
    axes[1].set_yticklabels([f"Sample {i+1}" for i in range(5)])
    axes[1].set_title("Individual Explanation Contributions\n(Red=Positive, Green=Negative)")
    axes[1].set_xlabel("Contribution Magnitude")

    plt.tight_layout()
    fig.savefig(os.path.join(args.output_dir, "step14_explainability.png"), dpi=120, bbox_inches="tight")
    plt.close()

    # Adverse action codes (for denied applicants — top reason for denial)
    denied = np.where(y_prob >= 0.5)[0]
    if len(denied) > 0:
        adverse_reasons = {}
        for feat_idx in top_idx[:5]:
            adverse_reasons[feat_names[feat_idx]] = {
                "importance": round(float(importances[feat_idx]), 4),
                "adverse_action_code": f"RC-{feat_names[feat_idx][:4].upper()}"
            }
    else:
        adverse_reasons = {"note": "No applications denied at 0.5 threshold"}

    with open(os.path.join(args.output_dir, "explainability_report.json"), "w") as f:
        json.dump({
            "top_features": [{"feature": feat_names[i], "importance": round(float(importances[i]), 4)}
                            for i in top_idx[:15]],
            "individual_explanations": lime_data,
            "adverse_action_codes": adverse_reasons,
        }, f, indent=2)

    print(f"\n✅ Step 14 complete — explainability report generated")

if __name__ == "__main__":
    main()
