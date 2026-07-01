#!/usr/bin/env python3
"""Step 12: Model Training — Advanced Ensemble (XGBoost + Stacking)."""
import argparse, os, json, pickle
import numpy as np
from sklearn.ensemble import RandomForestClassifier, StackingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.metrics import roc_auc_score, average_precision_score, brier_score_loss
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--data_dir", default="../data")
    p.add_argument("--output_dir", default=".")
    args = p.parse_args()
    os.makedirs(args.output_dir, exist_ok=True)
    print("=" * 60)
    print("STEP 12: Model Training — Advanced Ensemble")
    print("=" * 60)

    data = np.load(os.path.join(args.output_dir, "train_data.npz"))
    X_train, y_train = data["X_train"], data["y_train"]
    X_val, y_val = data["X_val"], data["y_val"]

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    ensemble_models = []

    # ===== XGBoost with basic tuning =====
    try:
        import xgboost as xgb
        print("\n🔷 XGBoost (with hyperparameter tuning)")

        # Simple grid search over key params
        best_score, best_params = 0, {}
        for n_est in [100, 200]:
            for lr in [0.05, 0.1]:
                for md in [4, 6, 8]:
                    xgb_model = xgb.XGBClassifier(
                        n_estimators=n_est, max_depth=md, learning_rate=lr,
                        random_state=42, scale_pos_weight=(y_train == 0).sum() / (y_train == 1).sum(),
                        use_label_encoder=False, eval_metric="logloss", verbosity=0
                    )
                    scores = cross_val_score(xgb_model, X_train, y_train, cv=cv, scoring="roc_auc")
                    mean_score = scores.mean()
                    if mean_score > best_score:
                        best_score = mean_score
                        best_params = {"n_estimators": n_est, "max_depth": md, "learning_rate": lr}

        print(f"   Best params: {best_params} (CV ROC-AUC: {best_score:.4f})")

        xgb_best = xgb.XGBClassifier(**best_params, random_state=42,
            scale_pos_weight=(y_train == 0).sum() / (y_train == 1).sum(),
            use_label_encoder=False, eval_metric="logloss", verbosity=0)
        xgb_best.fit(X_train, y_train)
        xgb_val_pred = xgb_best.predict_proba(X_val)[:, 1]

        xgb_results = {
            "model": "XGBoost",
            "params": best_params,
            "cv_roc_auc": round(best_score, 4),
            "val_roc_auc": round(roc_auc_score(y_val, xgb_val_pred), 4),
            "val_pr_auc": round(average_precision_score(y_val, xgb_val_pred), 4),
            "val_brier": round(brier_score_loss(y_val, xgb_val_pred), 4),
        }
        print(f"   Val ROC-AUC: {xgb_results['val_roc_auc']:.4f}")
        ensemble_models.append(xgb_results)
        with open(os.path.join(args.output_dir, "xgboost_model.pkl"), "wb") as f:
            pickle.dump(xgb_best, f)
    except ImportError:
        print("\n🔷 XGBoost — not installed, skipping")

    # ===== Stacking Classifier =====
    print("\n🔷 Stacking Classifier (RF + LR + XGBoost)")
    base_estimators = [
        ("rf", RandomForestClassifier(n_estimators=200, max_depth=12, random_state=42, class_weight="balanced", n_jobs=-1)),
        ("lr", LogisticRegression(max_iter=5000, random_state=42, class_weight="balanced")),
    ]
    # Add XGBoost if available
    xgb_available = False
    try:
        import xgboost as xgb
        base_estimators.append(("xgb", xgb.XGBClassifier(n_estimators=100, max_depth=6,
            random_state=42, use_label_encoder=False, eval_metric="logloss", verbosity=0)))
        xgb_available = True
    except ImportError:
        pass

    meta_learner = LogisticRegression(max_iter=5000, random_state=42, class_weight="balanced")
    stack = StackingClassifier(estimators=base_estimators, final_estimator=meta_learner,
                                cv=3, n_jobs=-1)
    stack_cv = cross_val_score(stack, X_train, y_train, cv=cv, scoring="roc_auc")
    stack.fit(X_train, y_train)
    stack_val_pred = stack.predict_proba(X_val)[:, 1]

    stack_results = {
        "model": "StackingClassifier",
        "base_models": [name for name, _ in base_estimators],
        "meta_learner": "LogisticRegression",
        "cv_roc_auc_mean": round(stack_cv.mean(), 4),
        "cv_roc_auc_std": round(stack_cv.std(), 4),
        "val_roc_auc": round(roc_auc_score(y_val, stack_val_pred), 4),
        "val_pr_auc": round(average_precision_score(y_val, stack_val_pred), 4),
        "val_brier": round(brier_score_loss(y_val, stack_val_pred), 4),
    }
    print(f"   CV ROC-AUC: {stack_results['cv_roc_auc_mean']:.4f} ± {stack_results['cv_roc_auc_std']:.4f}")
    print(f"   Val ROC-AUC: {stack_results['val_roc_auc']:.4f}")
    ensemble_models.append(stack_results)

    # Save stacking model
    with open(os.path.join(args.output_dir, "stacking_model.pkl"), "wb") as f:
        pickle.dump(stack, f)

    # ===== Compare all advanced models =====
    best_advanced = max(ensemble_models, key=lambda x: x["val_roc_auc"])
    print(f"\n🏆 Best advanced model: {best_advanced['model']} (ROC-AUC: {best_advanced['val_roc_auc']:.4f})")

    # Save ensemble results
    with open(os.path.join(args.output_dir, "ensemble_results.json"), "w") as f:
        json.dump({"models": ensemble_models, "best": best_advanced["model"],
                    "best_roc_auc": best_advanced["val_roc_auc"]}, f, indent=2)

    # Calibration comparison plot
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    models_labeled = [("Stacking", stack_val_pred, stack_results["val_roc_auc"])]
    if xgb_available:
        models_labeled.append(("XGBoost", xgb_val_pred, xgb_results["val_roc_auc"]))

    for i, (name, preds, auc) in enumerate(models_labeled):
        axes[i].hist(preds[y_val == 0], bins=20, alpha=0.6, label="Non-Default", color="#2ecc71", edgecolor="white")
        axes[i].hist(preds[y_val == 1], bins=20, alpha=0.6, label="Default", color="#e74c3c", edgecolor="white")
        axes[i].set_title(f"{name}\nROC-AUC: {auc:.3f}")
        axes[i].set_xlabel("Predicted Probability")
        axes[i].legend()

    plt.tight_layout()
    fig.savefig(os.path.join(args.output_dir, "step12_calibration.png"), dpi=100)
    plt.close()

    print(f"\n✅ Step 12 complete — advanced models evaluated")

if __name__ == "__main__":
    main()
