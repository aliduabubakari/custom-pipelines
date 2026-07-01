#!/usr/bin/env python3
"""Step 5: Feature Engineering — Create behavioral churn risk features."""
import argparse, os, json
import pandas as pd, numpy as np

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--data_dir", default="../data")
    p.add_argument("--output_dir", default=".")
    args = p.parse_args()
    os.makedirs(args.output_dir, exist_ok=True)
    print("=" * 60)
    print("STEP 5: Feature Engineering")
    print("=" * 60)

    df = pd.read_parquet(os.path.join(args.output_dir, "cleaned_data.parquet"))
    initial_cols = len(df.columns)
    features = []

    # 1. Recency score (days since last purchase, binned)
    df["recency_score"] = pd.cut(df["days_since_last_purchase"].clip(0, 365),
        bins=[-1, 7, 30, 90, 180, 366], labels=[5, 4, 3, 2, 1])
    features.append("recency_score (5 bins)")

    # 2. Frequency score (purchases per month)
    df["frequency_score"] = pd.cut(df["purchase_frequency"].clip(0, 20),
        bins=[-0.01, 0.5, 1, 2, 5, 21], labels=[1, 2, 3, 4, 5])
    features.append("frequency_score (5 bins)")

    # 3. Monetary score (avg spend per month)
    df["monthly_spend"] = np.where(df["tenure_days"] > 0,
        df["total_spend"] / (df["tenure_days"] / 30), 0)
    df["monetary_score"] = pd.cut(df["monthly_spend"].clip(0, 5000),
        bins=[-0.01, 50, 100, 200, 500, 5001], labels=[1, 2, 3, 4, 5])
    features.append("monetary_score (5 bins)")

    # 4. Engagement score (frequency × category diversity)
    df["engagement_score"] = (df["purchase_frequency"] * df["category_diversity"]).clip(0, 50)
    features.append("engagement_score")

    # 5. Tenure group
    df["tenure_group"] = pd.cut(df["tenure_days"],
        bins=[-1, 30, 90, 180, 365, 730, 10000],
        labels=["<1mo", "1-3mo", "3-6mo", "6-12mo", "1-2yr", "2yr+"])
    features.append("tenure_group")

    # 6. Support contact intensity
    df["support_intensity"] = pd.cut(df["support_contacts"],
        bins=[-1, 0, 2, 5, 100], labels=["None", "Low", "Medium", "High"])
    features.append("support_intensity")

    # 7. Spend-to-fee ratio
    df["spend_fee_ratio"] = np.where(df["monthly_fee"] > 0,
        df["monthly_spend"] / df["monthly_fee"], 0)
    features.append("spend_fee_ratio")

    # 8. Recent customer flag
    df["is_recent_customer"] = (df["tenure_days"] < 90).astype(int)
    features.append("is_recent_customer")

    df.to_parquet(os.path.join(args.output_dir, "feature_engineered.parquet"), index=False)

    with open(os.path.join(args.output_dir, "feature_engineering_log.json"), "w") as f:
        json.dump({"features_created": len(features), "feature_list": features,
                    "initial_cols": initial_cols, "final_cols": len(df.columns)}, f, indent=2)

    print(f"\n🔧 Created {len(features)} new features: " + ", ".join(features[:4]) + f" +{len(features)-4} more")
    print(f"   Final: {len(df.columns)} columns")
    print("✅ Step 5 complete")

if __name__ == "__main__":
    main()
