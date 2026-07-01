#!/usr/bin/env python3
"""Step 10: Data Preparation for Modeling — Encode, scale, split."""
import argparse, os, json, pickle
import pandas as pd, numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder, OrdinalEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--data_dir", default="../data")
    p.add_argument("--output_dir", default=".")
    args = p.parse_args()
    os.makedirs(args.output_dir, exist_ok=True)
    print("=" * 60)
    print("STEP 10: Data Preparation for Modeling")
    print("=" * 60)

    df = pd.read_parquet(os.path.join(args.output_dir, "feature_engineered.parquet"))

    # Separate target
    target = "default_flag"
    y = df[target]
    X = df.drop(columns=[target])

    # Identify column types
    id_cols = [c for c in X.columns if "id" in c.lower() and X[c].nunique() == len(X)]
    num_cols = X.select_dtypes(include=['float64', 'int64']).columns.tolist()
    num_cols = [c for c in num_cols if c not in id_cols]
    cat_cols = X.select_dtypes(include=['object', 'category']).columns.tolist()

    # Remove ID columns from features (keep for tracking)
    if id_cols:
        print(f"\n🔑 Dropping ID columns: {id_cols}")
        X = X.drop(columns=id_cols)
        num_cols = [c for c in num_cols if c not in id_cols]
        cat_cols = [c for c in cat_cols if c not in id_cols]

    # Convert date-like columns to ordinal (days since epoch) and move to numerical
    date_cols = [c for c in cat_cols if 'date' in c.lower() or 'report' in c.lower()]
    for dc in date_cols:
        try:
            X[dc] = pd.to_datetime(X[dc], errors='coerce')
            X[dc] = (X[dc] - pd.Timestamp('1970-01-01')).dt.days
            num_cols.append(dc)
            cat_cols.remove(dc)
        except Exception:
            pass

    print(f"\n📊 Features: {len(num_cols)} numerical, {len(cat_cols)} categorical")
    print(f"   Numerical: {num_cols}")
    print(f"   Categorical: {cat_cols}")

    # Build preprocessing pipeline
    numerical_pipe = Pipeline([("scaler", StandardScaler())])

    categorical_pipe = Pipeline([
        ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False))
    ])

    preprocessor = ColumnTransformer([
        ("num", numerical_pipe, num_cols),
        ("cat", categorical_pipe, cat_cols),
    ], remainder="drop")

    # Fit and transform
    X_processed = preprocessor.fit_transform(X)

    # Get feature names
    cat_feature_names = []
    if cat_cols:
        cat_feature_names = preprocessor.named_transformers_["cat"]["onehot"].get_feature_names_out(cat_cols).tolist()
    all_feature_names = num_cols + cat_feature_names

    print(f"\n🔧 After encoding: {X_processed.shape[1]} features (from {len(num_cols) + len(cat_cols)} raw)")

    # Stratified split (70/15/15)
    X_train, X_temp, y_train, y_temp = train_test_split(
        X_processed, y, test_size=0.30, stratify=y, random_state=42
    )
    X_val, X_test, y_val, y_test = train_test_split(
        X_temp, y_temp, test_size=0.50, stratify=y_temp, random_state=42
    )

    print(f"\n📦 Data splits: Train={len(X_train)} | Val={len(X_val)} | Test={len(X_test)}")
    for name, yset in [("Train", y_train), ("Val", y_val), ("Test", y_test)]:
        print(f"   {name} default rate: {yset.mean()*100:.1f}%")

    # Save everything
    np.savez(os.path.join(args.output_dir, "train_data.npz"),
             X_train=X_train, y_train=y_train.values,
             X_val=X_val, y_val=y_val.values,
             X_test=X_test, y_test=y_test.values)
    with open(os.path.join(args.output_dir, "preprocessor.pkl"), "wb") as f:
        pickle.dump(preprocessor, f)

    # Save metadata
    with open(os.path.join(args.output_dir, "modeling_metadata.json"), "w") as f:
        json.dump({
            "n_features": X_processed.shape[1],
            "feature_names": all_feature_names,
            "train_size": len(X_train),
            "val_size": len(X_val),
            "test_size": len(X_test),
            "train_default_rate": round(y_train.mean(), 4),
            "val_default_rate": round(y_val.mean(), 4),
            "test_default_rate": round(y_test.mean(), 4),
        }, f, indent=2)

    print(f"\n✅ Step 10 complete — processed data & preprocessor saved")

if __name__ == "__main__":
    main()
