#!/usr/bin/env python3
"""Step 12: Model Training — Multi-model comparison."""
import argparse, os, json, pickle
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.metrics import roc_auc_score, average_precision_score, fbeta_score, brier_score_loss
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--data_dir", default="../data")
    p.add_argument("--output_dir", default=".")
    args = p.parse_args()
    os.makedirs(args.output_dir, exist_ok=True)
    print("=" * 60)
    print("STEP 12: Model Training — Multi-Model Comparison")
    print("=" * 60)

    data = np.load(os.path.join(args.output_dir, "train_data.npz"))
    X_train, y_train = data["X_train"], data["y_train"]
    X_val, y_val = data["X_val"], data["y_val"]

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    models_registry = []

    # 1. Logistic Regression
    print("\n🔷 Logistic Regression")
    lr = LogisticRegression(max_iter=5000, random_state=42, class_weight="balanced")
    lr_cv = cross_val_score(lr, X_train, y_train, cv=cv, scoring="roc_auc")
    lr.fit(X_train, y_train)
    lr_pred = lr.predict_proba(X_val)[:, 1]
    models_registry.append(model_eval("LogisticRegression", lr_cv, lr_pred, y_val))
    print(f"   ROC-AUC: {models_registry[-1]['val_roc_auc']:.4f}")

    # 2. Random Forest
    print("\n🔷 Random Forest")
    rf = RandomForestClassifier(n_estimators=200, max_depth=12, random_state=42, class_weight="balanced", n_jobs=-1)
    rf_cv = cross_val_score(rf, X_train, y_train, cv=cv, scoring="roc_auc")
    rf.fit(X_train, y_train)
    rf_pred = rf.predict_proba(X_val)[:, 1]
    models_registry.append(model_eval("RandomForest", rf_cv, rf_pred, y_val))
    print(f"   ROC-AUC: {models_registry[-1]['val_roc_auc']:.4f}")

    # 3. XGBoost
    try:
        import xgboost as xgb
        print("\n🔷 XGBoost")
        xgb_model = xgb.XGBClassifier(n_estimators=200, max_depth=6, learning_rate=0.1, random_state=42,
            scale_pos_weight=(y_train==0).sum()/(y_train==1).sum(),
            use_label_encoder=False, eval_metric="logloss", verbosity=0)
        xgb_cv = cross_val_score(xgb_model, X_train, y_train, cv=cv, scoring="roc_auc")
        xgb_model.fit(X_train, y_train)
        xgb_pred = xgb_model.predict_proba(X_val)[:, 1]
        models_registry.append(model_eval("XGBoost", xgb_cv, xgb_pred, y_val))
        print(f"   ROC-AUC: {models_registry[-1]['val_roc_auc']:.4f}")
        with open(os.path.join(args.output_dir, "xgboost_model.pkl"), "wb") as f:
            pickle.dump(xgb_model, f)
    except ImportError:
        print("\n🔷 XGBoost — not installed")

    # 4. LightGBM
    try:
        import lightgbm as lgb
        print("\n🔷 LightGBM")
        lgbm = lgb.LGBMClassifier(n_estimators=200, max_depth=8, random_state=42, class_weight="balanced", verbose=-1)
        lgb_cv = cross_val_score(lgbm, X_train, y_train, cv=cv, scoring="roc_auc")
        lgbm.fit(X_train, y_train)
        lgb_pred = lgbm.predict_proba(X_val)[:, 1]
        models_registry.append(model_eval("LightGBM", lgb_cv, lgb_pred, y_val))
        print(f"   ROC-AUC: {models_registry[-1]['val_roc_auc']:.4f}")
    except ImportError:
        print("\n🔷 LightGBM — not installed")

    # Save best model
    best = max(models_registry, key=lambda x: x["val_roc_auc"])
    print(f"\n🏆 Best: {best['model']} (ROC={best['val_roc_auc']:.4f})")

    for m_name, m_obj in [("LogisticRegression", lr), ("RandomForest", rf)]:
        if m_name == best["model"]:
            with open(os.path.join(args.output_dir, "best_model.pkl"), "wb") as f:
                pickle.dump(m_obj, f)

    # Comparison chart
    fig, ax = plt.subplots(figsize=(10, 5))
    models_list = [m["model"] for m in models_registry]
    roc_values = [m["val_roc_auc"] for m in models_registry]
    pr_values = [m["val_pr_auc"] for m in models_registry]
    x = range(len(models_list))
    w = 0.35
    ax.bar([i - w/2 for i in x], roc_values, w, label="ROC-AUC", color="#3498db", edgecolor="white")
    ax.bar([i + w/2 for i in x], pr_values, w, label="PR-AUC", color="#e74c3c", edgecolor="white")
    ax.set_xticks(x)
    ax.set_xticklabels(models_list)
    ax.set_title("Model Comparison — Validation Set")
    ax.set_ylabel("Score")
    ax.legend()
    ax.set_ylim(0, 1)
    plt.tight_layout()
    fig.savefig(os.path.join(args.output_dir, "step12_model_comparison.png"), dpi=100)
    plt.close()

    with open(os.path.join(args.output_dir, "model_registry.json"), "w") as f:
        json.dump({"models": models_registry, "best": best["model"], "best_roc_auc": best["val_roc_auc"]}, f, default=str, indent=2)
    print(f"\n✅ Step 12 complete")

def model_eval(name, cv_scores, val_pred, y_val):
    return {
        "model": name,
        "cv_roc_auc_mean": round(cv_scores.mean(), 4),
        "cv_roc_auc_std": round(cv_scores.std(), 4),
        "val_roc_auc": round(roc_auc_score(y_val, val_pred), 4),
        "val_pr_auc": round(average_precision_score(y_val, val_pred), 4),
        "val_brier": round(brier_score_loss(y_val, val_pred), 4),
    }

if __name__ == "__main__":
    main()
