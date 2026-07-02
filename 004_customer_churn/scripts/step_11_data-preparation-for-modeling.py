#!/usr/bin/env python3
"""Step 11: Data Preparation for Modeling — Encode, scale, handle imbalance, split."""
import argparse, os, json, pickle
import pandas as pd, numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--data_dir", default="../data")
    p.add_argument("--output_dir", default=".")
    args = p.parse_args()
    os.makedirs(args.output_dir, exist_ok=True)
    print("=" * 60)
    print("STEP 11: Data Preparation for Modeling")
    print("=" * 60)

    df = pd.read_parquet(os.path.join(args.output_dir, "feature_engineered.parquet"))
    target = "is_churned"

    y = df[target]
    X = df.drop(columns=[target])

    # Drop ID columns and date columns
    drop = [c for c in X.columns if "id" in c.lower() or "date" in c.lower() or c == "signup_date"]
    X = X.drop(columns=[c for c in drop if c in X.columns])

    # Identify column types
    num_cols = X.select_dtypes(include=['float64', 'int64']).columns.tolist()
    cat_cols = X.select_dtypes(include=['object', 'category']).columns.tolist()

    # For categorical columns that are ordinal-like strings, encode as numbers
    for col in cat_cols[:]:
        if X[col].nunique() > 20:
            cat_cols.remove(col)  # too many categories for one-hot

    print(f"\n📊 Features: {len(num_cols)} numerical, {len(cat_cols)} categorical")

    # Build pipeline
    preprocessor = ColumnTransformer([
        ("num", StandardScaler(), num_cols),
        ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False, max_categories=15), cat_cols),
    ], remainder="drop")

    X_processed = preprocessor.fit_transform(X)

    # Get feature names
    try:
        cat_names = preprocessor.named_transformers_["cat"].get_feature_names_out(cat_cols).tolist()
    except Exception:
        cat_names = []
    all_features = num_cols + cat_names

    # Stratified split 70/15/15
    X_train, X_temp, y_train, y_temp = train_test_split(X_processed, y, test_size=0.30, stratify=y, random_state=42)
    X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.50, stratify=y_temp, random_state=42)

    print(f"\n📦 Splits: Train={len(X_train)} | Val={len(X_val)} | Test={len(X_test)}")
    for name, yset in [("Train", y_train), ("Val", y_val), ("Test", y_test)]:
        print(f"   {name} churn rate: {yset.mean()*100:.1f}%")

    np.savez(os.path.join(args.output_dir, "train_data.npz"),
             X_train=X_train, y_train=y_train.values,
             X_val=X_val, y_val=y_val.values, X_test=X_test, y_test=y_test.values)
    with open(os.path.join(args.output_dir, "preprocessor.pkl"), "wb") as f:
        pickle.dump(preprocessor, f)

    with open(os.path.join(args.output_dir, "modeling_metadata.json"), "w") as f:
        json.dump({"n_features": X_processed.shape[1], "feature_names": all_features,
                    "train_size": len(X_train), "test_size": len(X_test)}, f, default=str, indent=2)

    print(f"\n✅ Step 11 complete — {X_processed.shape[1]} features ready for modeling")

if __name__ == "__main__":
    main()
