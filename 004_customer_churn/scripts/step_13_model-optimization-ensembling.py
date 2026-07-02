#!/usr/bin/env python3
"""Step 13: Model Optimization & Ensembling — Tune top models and create ensemble."""
import argparse, os, json, pickle
import numpy as np
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.metrics import roc_auc_score, brier_score_loss
from sklearn.calibration import CalibratedClassifierCV
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--data_dir", default="../data")
    p.add_argument("--output_dir", default=".")
    args = p.parse_args()
    os.makedirs(args.output_dir, exist_ok=True)
    print("=" * 60)
    print("STEP 13: Model Optimization & Ensembling")
    print("=" * 60)

    data = np.load(os.path.join(args.output_dir, "train_data.npz"))
    X_train, y_train = data["X_train"], data["y_train"]
    X_val, y_val = data["X_val"], data["y_val"]

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    # Tune Random Forest (simple grid over key params)
    print("\n🔷 Tuning Random Forest...")
    best_score, best_rf = 0, None
    for n_est in [100, 200, 300]:
        for md in [8, 12, 16]:
            rf = RandomForestClassifier(n_estimators=n_est, max_depth=md, random_state=42,
                                         class_weight="balanced", n_jobs=-1)
            scores = cross_val_score(rf, X_train, y_train, cv=cv, scoring="roc_auc")
            if scores.mean() > best_score:
                best_score = scores.mean()
                best_rf = RandomForestClassifier(n_estimators=n_est, max_depth=md, random_state=42,
                                                  class_weight="balanced", n_jobs=-1)
    best_rf.fit(X_train, y_train)
    rf_pred = best_rf.predict_proba(X_val)[:, 1]
    rf_auc = roc_auc_score(y_val, rf_pred)
    print(f"   Tuned RF: n={best_rf.n_estimators}, depth={best_rf.max_depth}, ROC={rf_auc:.4f}")

    # Tune Logistic Regression
    print("\n🔷 Tuning Logistic Regression...")
    best_lr_score, best_lr = 0, None
    for C_val in [0.01, 0.1, 1.0, 10.0]:
        lr = LogisticRegression(C=C_val, max_iter=5000, random_state=42, class_weight="balanced")
        scores = cross_val_score(lr, X_train, y_train, cv=cv, scoring="roc_auc")
        if scores.mean() > best_lr_score:
            best_lr_score = scores.mean()
            best_lr = LogisticRegression(C=C_val, max_iter=5000, random_state=42, class_weight="balanced")
    best_lr.fit(X_train, y_train)
    lr_pred = best_lr.predict_proba(X_val)[:, 1]
    lr_auc = roc_auc_score(y_val, lr_pred)
    print(f"   Tuned LR: C={best_lr.C}, ROC={lr_auc:.4f}")

    # Ensemble: Voting classifier
    print("\n🔷 Building Voting Ensemble...")
    estimators = [("rf", best_rf), ("lr", best_lr)]

    # Add XGBoost if available
    xgb_path = os.path.join(args.output_dir, "xgboost_model.pkl")
    if os.path.exists(xgb_path):
        with open(xgb_path, "rb") as f:
            xgb_model = pickle.load(f)
        estimators.append(("xgb", xgb_model))

    ensemble = VotingClassifier(estimators=estimators, voting="soft", n_jobs=-1)
    ensemble.fit(X_train, y_train)
    ens_pred = ensemble.predict_proba(X_val)[:, 1]
    ens_auc = roc_auc_score(y_val, ens_pred)

    # Calibrate
    print("\n🔷 Calibrating probabilities...")
    calibrated = CalibratedClassifierCV(ensemble, method="isotonic", cv=3)
    calibrated.fit(X_train, y_train)
    cal_pred = calibrated.predict_proba(X_val)[:, 1]
    cal_auc = roc_auc_score(y_val, cal_pred)
    cal_brier = brier_score_loss(y_val, cal_pred)

    print(f"\n📊 Ensemble Results:")
    print(f"   Uncalibrated ROC: {ens_auc:.4f}")
    print(f"   Calibrated ROC:   {cal_auc:.4f}")
    print(f"   Calibrated Brier:  {cal_brier:.4f}")

    # Save final model
    with open(os.path.join(args.output_dir, "calibrated_ensemble.pkl"), "wb") as f:
        pickle.dump(calibrated, f)

    # Calibration plot
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    for i, (name, preds) in enumerate([("Uncalibrated", ens_pred), ("Calibrated", cal_pred)]):
        for flag, label, color in [(0, "Retained", "#2ecc71"), (1, "Churned", "#e74c3c")]:
            axes[i].hist(preds[y_val == flag], bins=20, alpha=0.6, label=label, color=color, edgecolor="white")
        axes[i].set_title(f"{name}\nROC={roc_auc_score(y_val, preds):.3f}, Brier={brier_score_loss(y_val, preds):.3f}")
        axes[i].legend()
    plt.tight_layout()
    fig.savefig(os.path.join(args.output_dir, "step13_calibration.png"), dpi=100)
    plt.close()

    with open(os.path.join(args.output_dir, "optimization_results.json"), "w") as f:
        json.dump({"calibrated_roc_auc": round(cal_auc, 4), "calibrated_brier": round(cal_brier, 4),
                    "n_estimators_in_ensemble": len(estimators)}, f, default=str, indent=2)
    print("\n✅ Step 13 complete")

if __name__ == "__main__":
    main()
