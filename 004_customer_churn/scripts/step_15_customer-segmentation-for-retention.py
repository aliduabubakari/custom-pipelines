#!/usr/bin/env python3
"""Step 15: Customer Segmentation for Retention — Cluster at-risk customers."""
import argparse, os, json, pickle
import pandas as pd, numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--data_dir", default="../data")
    p.add_argument("--output_dir", default=".")
    args = p.parse_args()
    os.makedirs(args.output_dir, exist_ok=True)
    print("=" * 60)
    print("STEP 15: Customer Segmentation for Retention")
    print("=" * 60)

    # Load preprocessor and model
    with open(os.path.join(args.output_dir, "preprocessor.pkl"), "rb") as f:
        preprocessor = pickle.load(f)

    model_path = os.path.join(args.output_dir, "calibrated_ensemble.pkl")
    if not os.path.exists(model_path):
        model_path = os.path.join(args.output_dir, "best_model.pkl")
    with open(model_path, "rb") as f:
        model = pickle.load(f)

    # Load original data
    df = pd.read_parquet(os.path.join(args.output_dir, "feature_engineered.parquet"))

    # Process and predict
    target = "is_churned"
    y = df[target]
    X = df.drop(columns=[target])
    drop = [c for c in X.columns if "id" in c.lower() or "date" in c.lower() or c in ["signup_date", "first_purchase", "last_purchase"]]
    X = X.drop(columns=[c for c in drop if c in X.columns])

    # Use the same ColumnTransformer approach
    num_cols = X.select_dtypes(include=['float64', 'int64']).columns.tolist()
    cat_cols = X.select_dtypes(include=['object', 'category']).columns.tolist()
    cat_cols = [c for c in cat_cols if X[c].nunique() <= 20]

    # Simple manual preprocessing for clustering
    X_num = X[num_cols].fillna(0)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_num)

    # Predict churn probabilities
    # Use the preprocessed features if possible, else use scaled numerical
    try:
        X_proc = preprocessor.transform(X)
    except Exception:
        X_proc = X_scaled
    y_prob = model.predict_proba(X_proc)[:, 1]
    df["churn_probability"] = y_prob

    # Filter at-risk customers
    best_thresh = 0.35  # default threshold
    eval_path = os.path.join(args.output_dir, "evaluation_results.json")
    if os.path.exists(eval_path):
        with open(eval_path) as f:
            best_thresh = json.load(f).get("best_threshold", 0.35)

    at_risk = df[df["churn_probability"] >= best_thresh].copy()
    print(f"\n👥 At-risk customers (prob ≥ {best_thresh:.2f}): {len(at_risk)} / {len(df)} ({len(at_risk)/len(df)*100:.1f}%)")

    if len(at_risk) < 5:
        print("   Too few at-risk customers for clustering — using all customers")
        at_risk = df.copy()

    # Cluster on behavioral features
    cluster_features = ["tenure_days", "total_spend", "monthly_fee", "support_contacts",
                        "return_rate", "purchase_frequency", "days_since_last_purchase", "discount_usage_rate"]
    cluster_features = [c for c in cluster_features if c in at_risk.columns]
    X_cluster = at_risk[cluster_features].fillna(0)
    X_cluster_scaled = StandardScaler().fit_transform(X_cluster)

    # Find optimal k
    inertias = []
    K_range = range(1, min(8, len(at_risk)))
    for k in K_range:
        km = KMeans(n_clusters=k, random_state=42, n_init=10)
        km.fit(X_cluster_scaled)
        inertias.append(km.inertia_)

    # Use k=3 or elbow
    k_optimal = 3 if len(at_risk) >= 10 else 2
    kmeans = KMeans(n_clusters=k_optimal, random_state=42, n_init=10)
    at_risk["retention_cluster"] = kmeans.fit_predict(X_cluster_scaled)

    # Profile clusters
    print(f"\n📊 Retention Clusters (k={k_optimal}):")
    strategies = {
        0: "Discount Offer — Price-sensitive at-risk customers",
        1: "Feature Education — Low-engagement customers",
        2: "Account Review — High-support, frustrated customers"
    }
    for c in range(k_optimal):
        cluster = at_risk[at_risk["retention_cluster"] == c]
        profile = {feat: round(cluster[feat].mean(), 2) for feat in cluster_features}
        print(f"\n   Cluster {c} (n={len(cluster)}): {strategies.get(c, 'Custom intervention')}")
        print(f"   Avg tenure: {profile.get('tenure_days', 0):.0f}d | Spend: ${profile.get('total_spend', 0):.0f}")
        print(f"   Support contacts: {profile.get('support_contacts', 0):.1f} | Return rate: {profile.get('return_rate', 0)*100:.1f}%")

    # Visualization
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Elbow plot
    axes[0].plot(K_range, inertias, "o-", color="#3498db", lw=2, markersize=6)
    axes[0].axvline(x=k_optimal, color="red", linestyle="--", label=f"k={k_optimal}")
    axes[0].set_title("Elbow Method for Optimal k")
    axes[0].set_xlabel("Number of Clusters")
    axes[0].legend()

    # Cluster scatter
    scatter_x = cluster_features[0] if len(cluster_features) > 0 else "tenure_days"
    scatter_y = cluster_features[1] if len(cluster_features) > 1 else "total_spend"
    for c in range(k_optimal):
        subset = at_risk[at_risk["retention_cluster"] == c]
        axes[1].scatter(subset[scatter_x], subset[scatter_y], label=f"Cluster {c}", alpha=0.6, s=20)
    axes[1].set_title(f"At-Risk Customer Clusters")
    axes[1].set_xlabel(scatter_x)
    axes[1].set_ylabel(scatter_y)
    axes[1].legend()

    plt.tight_layout()
    fig.savefig(os.path.join(args.output_dir, "step15_retention_segments.png"), dpi=120, bbox_inches="tight")
    plt.close()

    at_risk[["customer_id", "churn_probability", "retention_cluster"] + cluster_features].to_csv(
        os.path.join(args.output_dir, "at_risk_customers.csv"), index=False)

    with open(os.path.join(args.output_dir, "retention_segmentation.json"), "w") as f:
        json.dump({"n_at_risk": len(at_risk), "n_clusters": k_optimal,
                    "recommended_strategies": strategies}, f, indent=2)
    print("\n✅ Step 15 complete")

if __name__ == "__main__":
    main()
