#!/usr/bin/env python3
import argparse, os, numpy as np, pandas as pd
np.random.seed(42)

def generate(n=400):
    # This is a simplified generator - data structure based on pipeline context
    return pd.DataFrame({"id": [f"X{i+1:04d}" for i in range(n)],
                         "value_a": np.random.normal(100, 20, n),
                         "value_b": np.random.normal(50, 10, n),
                         "category": np.random.choice(["A","B","C","D"], n),
                         "target": np.random.choice([0,1], n, p=[0.7,0.3])})

def main():
    p = argparse.ArgumentParser(); p.add_argument("--output_dir", default="data"); p.add_argument("--n", type=int, default=400)
    args = p.parse_args(); os.makedirs(args.output_dir, exist_ok=True)
    df = generate(args.n)
    df.to_csv(os.path.join(args.output_dir,"data.csv"),index=False)
    print(f"Generated {len(df)} records for sports_regression_clustering_visualization")
if __name__ == "__main__": main()
