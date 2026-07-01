#!/usr/bin/env python3
"""Step 13: Model Evaluation & Threshold Optimization."""
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
    print("STEP 13: Model Evaluation & Threshold Optimization")
    print("=" * 60)

    # Load test data
    data = np.load(os.path.join(args.output_dir, "train_data.npz"))
    X_test, y_test = data["X_test"], data["y_test"]

    # Load best model (try stacking first, then baseline)
    model = None
    model_name = "unknown"
    for model_file, name in [("stacking_model.pkl", "StackingClassifier"),
                              ("xgboost_model.pkl", "XGBoost"),
                              ("best_baseline_model.pkl", "BestBaseline")]:
        path = os.path.join(args.output_dir, model_file)
        if os.path.exists(path):
            with open(path, "rb") as f:
                model = pickle.load(f)
            model_name = name
            break

    if model is None:
        print("❌ No trained model found. Run steps 11-12 first.")
        return

    # Predict
    if hasattr(model, "predict_proba"):
        y_prob = model.predict_proba(X_test)[:, 1]
    else:
        y_prob = model.predict(X_test)

    y_pred_default = (y_prob >= 0.5).astype(int)

    # Metrics
    roc = roc_auc_score(y_test, y_prob)
    pr = average_precision_score(y_test, y_prob)
    brier = brier_score_loss(y_test, y_prob)

    print(f"\n📊 Test Set Performance ({model_name}):")
    print(f"   ROC-AUC: {roc:.4f}")
    print(f"   PR-AUC:  {pr:.4f}")
    print(f"   Brier:   {brier:.4f}")
    print(f"\n   Classification Report (threshold=0.5):")
    print(classification_report(y_test, y_pred_default, target_names=["Non-Default", "Default"]))

    # Threshold optimization — maximize F2-score (prioritize recall)
    thresholds = np.linspace(0.05, 0.95, 91)
    best_f2, best_thresh = 0, 0.5
    threshold_results = []
    for thresh in thresholds:
        y_pred_t = (y_prob >= thresh).astype(int)
        tn, fp, fn, tp = confusion_matrix(y_test, y_pred_t).ravel()
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        f2 = (5 * precision * recall) / (4 * precision + recall) if (precision + recall) > 0 else 0
        f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        threshold_results.append({"threshold": round(thresh, 2), "precision": round(precision, 3),
            "recall": round(recall, 3), "f1": round(f1, 3), "f2": round(f2, 3),
            "tp": int(tp), "fp": int(fp), "tn": int(tn), "fn": int(fn)})
        if f2 > best_f2:
            best_f2, best_thresh = f2, thresh

    # Apply optimal threshold
    y_pred_opt = (y_prob >= best_thresh).astype(int)
    print(f"\n🎯 Optimal Threshold (max F2-score): {best_thresh:.2f}")
    print(f"   At threshold {best_thresh:.2f}:")
    tn, fp, fn, tp = confusion_matrix(y_test, y_pred_opt).ravel()
    print(f"   TP={tp}, FP={fp}, TN={tn}, FN={fn}")
    print(f"   Precision: {tp/(tp+fp):.3f}, Recall: {tp/(tp+fn):.3f}")

    # Expected financial impact (simplified)
    avg_loan = 25000  # assumed
    interest_revenue = avg_loan * 0.08  # 8% interest
    default_loss = avg_loan * 0.60  # 60% loss given default
    profit_default_strategy = tp * interest_revenue - fp * default_loss
    print(f"\n💰 Simplified Financial Impact at optimal threshold:")
    print(f"   Assuming avg loan = ${avg_loan:,}, 8% interest, 60% LGD:")
    print(f"   Profit from approved: ${profit_default_strategy:,.0f}")
    print(f"   Defaults prevented (recall): {tp}/{tp+fn} = {tp/(tp+fn)*100:.1f}%")

    # Visualizations
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))
    fig.suptitle(f"Model Evaluation — {model_name}", fontsize=16, fontweight="bold")

    # ROC curve
    fpr, tpr, _ = roc_curve(y_test, y_prob)
    axes[0, 0].plot(fpr, tpr, color="#3498db", lw=2, label=f"ROC (AUC={roc:.3f})")
    axes[0, 0].plot([0, 1], [0, 1], "k--", alpha=0.3)
    axes[0, 0].fill_between(fpr, tpr, alpha=0.2, color="#3498db")
    axes[0, 0].set_xlabel("False Positive Rate")
    axes[0, 0].set_ylabel("True Positive Rate")
    axes[0, 0].set_title("ROC Curve")
    axes[0, 0].legend()

    # Precision-Recall curve
    precision_curve, recall_curve, _ = precision_recall_curve(y_test, y_prob)
    axes[0, 1].plot(recall_curve, precision_curve, color="#e74c3c", lw=2, label=f"PR (AUC={pr:.3f})")
    axes[0, 1].axhline(y=y_test.mean(), color="gray", linestyle="--", alpha=0.5, label=f"Baseline ({y_test.mean():.2f})")
    axes[0, 1].set_xlabel("Recall")
    axes[0, 1].set_ylabel("Precision")
    axes[0, 1].set_title("Precision-Recall Curve")
    axes[0, 1].legend()

    # F2-score vs threshold
    thresh_vals = [r["threshold"] for r in threshold_results]
    f2_vals = [r["f2"] for r in threshold_results]
    f1_vals = [r["f1"] for r in threshold_results]
    axes[1, 0].plot(thresh_vals, f2_vals, color="#8e44ad", lw=2, label="F2-score")
    axes[1, 0].plot(thresh_vals, f1_vals, color="#3498db", lw=2, label="F1-score")
    axes[1, 0].axvline(x=best_thresh, color="red", linestyle="--", label=f"Optimal: {best_thresh:.2f}")
    axes[1, 0].set_xlabel("Threshold")
    axes[1, 0].set_ylabel("Score")
    axes[1, 0].set_title("F2 & F1 Score vs Threshold")
    axes[1, 0].legend()

    # Confusion Matrix at optimal threshold
    cm = confusion_matrix(y_test, y_pred_opt)
    axes[1, 1].imshow(cm, cmap="Blues")
    for i in range(2):
        for j in range(2):
            axes[1, 1].text(j, i, cm[i, j], ha="center", va="center", fontsize=16, fontweight="bold")
    axes[1, 1].set_xticks([0, 1])
    axes[1, 1].set_xticklabels(["Non-Default", "Default"])
    axes[1, 1].set_yticks([0, 1])
    axes[1, 1].set_yticklabels(["Non-Default", "Default"])
    axes[1, 1].set_title(f"Confusion Matrix (threshold={best_thresh:.2f})")

    plt.tight_layout()
    fig.savefig(os.path.join(args.output_dir, "step13_evaluation.png"), dpi=120, bbox_inches="tight")
    plt.close()

    # Save results
    with open(os.path.join(args.output_dir, "evaluation_results.json"), "w") as f:
        json.dump({
            "model": model_name,
            "test_roc_auc": round(roc, 4),
            "test_pr_auc": round(pr, 4),
            "test_brier": round(brier, 4),
            "optimal_threshold": round(best_thresh, 4),
            "optimal_f2": round(best_f2, 4),
            "threshold_analysis": threshold_results,
        }, f, indent=2)

    print(f"\n✅ Step 13 complete — model evaluation complete")

if __name__ == "__main__":
    main()
