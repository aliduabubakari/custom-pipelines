#!/usr/bin/env python3
"""Step 11: Model Training — Baseline models (LogisticRegression, RandomForest, LightGBM)."""
import argparse, os, json
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.metrics import roc_auc_score, average_precision_score, brier_score_loss

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--data_dir", default="../data")
    p.add_argument("--output_dir", default=".")
    args = p.parse_args()
    os.makedirs(args.output_dir, exist_ok=True)
    print("=" * 60)
    print("STEP 11: Model Training — Baseline Models")
    print("=" * 60)

    # Load data
    data = np.load(os.path.join(args.output_dir, "train_data.npz"))
    X_train, y_train = data["X_train"], data["y_train"]
    X_val, y_val = data["X_val"], data["y_val"]

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    model_registry = []

    # ===== Logistic Regression =====
    print("\n🔷 Logistic Regression")
    lr = LogisticRegression(max_iter=5000, random_state=42, class_weight="balanced")
    lr_cv_scores = cross_val_score(lr, X_train, y_train, cv=cv, scoring="roc_auc")
    lr.fit(X_train, y_train)
    lr_val_pred = lr.predict_proba(X_val)[:, 1]
    lr_results = {
        "model": "LogisticRegression",
        "cv_roc_auc_mean": round(lr_cv_scores.mean(), 4),
        "cv_roc_auc_std": round(lr_cv_scores.std(), 4),
        "val_roc_auc": round(roc_auc_score(y_val, lr_val_pred), 4),
        "val_pr_auc": round(average_precision_score(y_val, lr_val_pred), 4),
        "val_brier": round(brier_score_loss(y_val, lr_val_pred), 4),
    }
    print(f"   CV ROC-AUC: {lr_results['cv_roc_auc_mean']:.4f} ± {lr_results['cv_roc_auc_std']:.4f}")
    print(f"   Val ROC-AUC: {lr_results['val_roc_auc']:.4f}, PR-AUC: {lr_results['val_pr_auc']:.4f}")
    model_registry.append(lr_results)

    # ===== Random Forest =====
    print("\n🔷 Random Forest")
    rf = RandomForestClassifier(n_estimators=200, max_depth=12, random_state=42, class_weight="balanced", n_jobs=-1)
    rf_cv_scores = cross_val_score(rf, X_train, y_train, cv=cv, scoring="roc_auc")
    rf.fit(X_train, y_train)
    rf_val_pred = rf.predict_proba(X_val)[:, 1]
    rf_results = {
        "model": "RandomForest",
        "cv_roc_auc_mean": round(rf_cv_scores.mean(), 4),
        "cv_roc_auc_std": round(rf_cv_scores.std(), 4),
        "val_roc_auc": round(roc_auc_score(y_val, rf_val_pred), 4),
        "val_pr_auc": round(average_precision_score(y_val, rf_val_pred), 4),
        "val_brier": round(brier_score_loss(y_val, rf_val_pred), 4),
        "feature_importances_top5": []
    }
    # Top 5 features
    with open(os.path.join(args.output_dir, "modeling_metadata.json")) as f:
        meta = json.load(f)
    feat_names = meta["feature_names"]
    if len(feat_names) == X_train.shape[1]:
        top_idx = np.argsort(rf.feature_importances_)[::-1][:5]
        rf_results["feature_importances_top5"] = [
            {"feature": feat_names[i], "importance": round(float(rf.feature_importances_[i]), 4)}
            for i in top_idx
        ]
        print(f"   Top features: {', '.join(feat_names[i] for i in top_idx[:3])}")
    print(f"   CV ROC-AUC: {rf_results['cv_roc_auc_mean']:.4f} ± {rf_results['cv_roc_auc_std']:.4f}")
    print(f"   Val ROC-AUC: {rf_results['val_roc_auc']:.4f}, PR-AUC: {rf_results['val_pr_auc']:.4f}")
    model_registry.append(rf_results)

    # ===== LightGBM (optional) =====
    try:
        import lightgbm as lgb
        print("\n🔷 LightGBM")
        lgbm = lgb.LGBMClassifier(n_estimators=200, max_depth=8, random_state=42, class_weight="balanced", verbose=-1)
        lgb_cv_scores = cross_val_score(lgbm, X_train, y_train, cv=cv, scoring="roc_auc")
        lgbm.fit(X_train, y_train)
        lgb_val_pred = lgbm.predict_proba(X_val)[:, 1]
        lgb_results = {
            "model": "LightGBM",
            "cv_roc_auc_mean": round(lgb_cv_scores.mean(), 4),
            "cv_roc_auc_std": round(lgb_cv_scores.std(), 4),
            "val_roc_auc": round(roc_auc_score(y_val, lgb_val_pred), 4),
            "val_pr_auc": round(average_precision_score(y_val, lgb_val_pred), 4),
            "val_brier": round(brier_score_loss(y_val, lgb_val_pred), 4),
            "feature_importances_top5": []
        }
        top_idx = np.argsort(lgbm.feature_importances_)[::-1][:5]
        lgb_results["feature_importances_top5"] = [
            {"feature": feat_names[i], "importance": round(float(lgbm.feature_importances_[i]), 4)}
            for i in top_idx
        ]
        print(f"   CV ROC-AUC: {lgb_results['cv_roc_auc_mean']:.4f} ± {lgb_results['cv_roc_auc_std']:.4f}")
        model_registry.append(lgb_results)
    except ImportError:
        print("\n🔷 LightGBM — not installed, skipping")

    # ===== Select best =====
    best = max(model_registry, key=lambda x: x["val_roc_auc"])
    print(f"\n{'─' * 40}")
    print(f"🏆 Best baseline model: {best['model']} (ROC-AUC: {best['val_roc_auc']:.4f})")

    # Save model registry
    with open(os.path.join(args.output_dir, "model_registry.json"), "w") as f:
        json.dump({"models": model_registry, "best": best["model"],
                    "best_roc_auc": best["val_roc_auc"]}, f, indent=2)

    # Save best baseline model for next step
    import pickle
    if best["model"] == "LogisticRegression":
        with open(os.path.join(args.output_dir, "best_baseline_model.pkl"), "wb") as f:
            pickle.dump(lr, f)
    elif best["model"] == "RandomForest":
        with open(os.path.join(args.output_dir, "best_baseline_model.pkl"), "wb") as f:
            pickle.dump(rf, f)
    elif best["model"] == "LightGBM":
        with open(os.path.join(args.output_dir, "best_baseline_model.pkl"), "wb") as f:
            pickle.dump(lgbm, f)

    print(f"\n✅ Step 11 complete — {len(model_registry)} models evaluated")

if __name__ == "__main__":
    main()
