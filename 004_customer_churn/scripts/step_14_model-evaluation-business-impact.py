#!/usr/bin/env python3
"""Step 14: Model Evaluation & Business Impact — ROI analysis at different thresholds."""
import argparse, os, json, pickle
import numpy as np
from sklearn.metrics import (roc_auc_score, average_precision_score, brier_score_loss,
    confusion_matrix, classification_report, roc_curve, precision_recall_curve)
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--data_dir", default="../data")
    p.add_argument("--output_dir", default=".")
    args = p.parse_args()
    os.makedirs(args.output_dir, exist_ok=True)
    print("=" * 60)
    print("STEP 14: Model Evaluation & Business Impact")
    print("=" * 60)

    data = np.load(os.path.join(args.output_dir, "train_data.npz"))
    X_test, y_test = data["X_test"], data["y_test"]

    # Load model
    model_path = os.path.join(args.output_dir, "calibrated_ensemble.pkl")
    if not os.path.exists(model_path):
        model_path = os.path.join(args.output_dir, "best_model.pkl")
    with open(model_path, "rb") as f:
        model = pickle.load(f)

    y_prob = model.predict_proba(X_test)[:, 1]
    y_pred = (y_prob >= 0.5).astype(int)

    # Base metrics
    roc = roc_auc_score(y_test, y_prob)
    pr = average_precision_score(y_test, y_prob)
    brier = brier_score_loss(y_test, y_prob)
    print(f"\n📊 Test Performance: ROC={roc:.4f}, PR={pr:.4f}, Brier={brier:.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=["Retained", "Churned"]))

    # Business simulation: ROI at different thresholds
    # Assume: retention campaign costs $50/customer, saves $500/customer (monthly_fee * avg_months)
    campaign_cost = 50
    retention_value = 500
    thresholds = np.linspace(0.05, 0.95, 19)
    roi_results = []

    for thresh in thresholds:
        y_pred_t = (y_prob >= thresh).astype(int)
        tn, fp, fn, tp = confusion_matrix(y_test, y_pred_t).ravel()
        # Revenue: correctly identified churners × retention value
        # Cost: false positives × campaign cost + all targeted × campaign cost
        n_targeted = tp + fp
        revenue = tp * retention_value
        cost = n_targeted * campaign_cost
        roi = revenue - cost
        roi_results.append({"threshold": round(thresh, 2), "n_targeted": int(n_targeted),
                            "tp": int(tp), "fp": int(fp), "fn": int(fn),
                            "revenue": int(revenue), "cost": int(cost), "roi": int(roi)})

    best_roi = max(roi_results, key=lambda x: x["roi"])
    print(f"\n💰 Business Impact Analysis:")
    print(f"   Campaign cost: ${campaign_cost}/customer | Retention value: ${retention_value}/customer")
    print(f"   Best threshold: {best_roi['threshold']} (ROI: ${best_roi['roi']:,})")
    print(f"   Target {best_roi['n_targeted']} customers → save {best_roi['tp']}/{best_roi['tp']+best_roi['fn']} churners")

    # Visualizations
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))

    # ROC curve
    fpr, tpr, _ = roc_curve(y_test, y_prob)
    axes[0, 0].plot(fpr, tpr, color="#3498db", lw=2, label=f"ROC (AUC={roc:.3f})")
    axes[0, 0].plot([0, 1], [0, 1], "k--", alpha=0.3)
    axes[0, 0].set_title("ROC Curve")
    axes[0, 0].legend()

    # Lift curve
    sorted_idx = np.argsort(y_prob)[::-1]
    cum_gains = np.cumsum(y_test[sorted_idx]) / y_test.sum()
    axes[0, 1].plot(np.linspace(0, 1, len(cum_gains)), cum_gains, color="#e74c3c", lw=2)
    axes[0, 1].plot([0, 1], [0, 1], "k--", alpha=0.3)
    axes[0, 1].set_title("Cumulative Gains / Lift Curve")
    axes[0, 1].set_xlabel("Fraction of Population")
    axes[0, 1].set_ylabel("Fraction of Churners Captured")

    # ROI by threshold
    t_vals = [r["threshold"] for r in roi_results]
    roi_vals = [r["roi"] for r in roi_results]
    axes[1, 0].bar(t_vals, roi_vals, width=0.04, color="#27ae60", edgecolor="white")
    axes[1, 0].axvline(x=best_roi["threshold"], color="red", linestyle="--", label=f"Best: {best_roi['threshold']}")
    axes[1, 0].set_title("ROI by Intervention Threshold")
    axes[1, 0].set_xlabel("Threshold")
    axes[1, 0].set_ylabel("ROI ($)")
    axes[1, 0].legend()

    # Precision-Recall
    precision_c, recall_c, _ = precision_recall_curve(y_test, y_prob)
    axes[1, 1].plot(recall_c, precision_c, color="#8e44ad", lw=2)
    axes[1, 1].set_title(f"Precision-Recall (AUC={pr:.3f})")
    axes[1, 1].set_xlabel("Recall")
    axes[1, 1].set_ylabel("Precision")
    axes[1, 1].axhline(y=y_test.mean(), color="gray", linestyle="--", alpha=0.5)

    plt.tight_layout()
    fig.savefig(os.path.join(args.output_dir, "step14_evaluation.png"), dpi=120, bbox_inches="tight")
    plt.close()

    with open(os.path.join(args.output_dir, "evaluation_results.json"), "w") as f:
        json.dump({"test_roc_auc": round(roc, 4), "test_pr_auc": round(pr, 4),
                    "best_threshold": best_roi["threshold"], "best_roi": best_roi["roi"],
                    "roi_by_threshold": roi_results}, f, indent=2)
    print("\n✅ Step 14 complete")

if __name__ == "__main__":
    main()
