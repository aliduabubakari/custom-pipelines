#!/usr/bin/env python3
"""Step 1: Data Loading & Profiling — Sports Cleaning, Statistical"""
import argparse, os, json
import pandas as pd, numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
def main():
    p=argparse.ArgumentParser();p.add_argument("--data_dir",default="../data");p.add_argument("--output_dir",default=".")
    a=p.parse_args();os.makedirs(a.output_dir,exist_ok=True)
    print("STEP 1: Load & Profile — Sports | Techniques: cleaning, statistical")
    df=pd.read_csv(os.path.join(a.data_dir,"data.csv"))
    print(f"   Data: {len(df)} rows x {len(df.columns)} cols")
    print(f"   Columns: {list(df.columns[:8])}...")
    for c in df.select_dtypes(include=['float64','int64']).columns[:4]:
        print(f"   {c}: mean={df[c].mean():.2f}, std={df[c].std():.2f}")
    df.to_parquet(os.path.join(a.output_dir,"raw_data.parquet"),index=False)
    prof={"rows":len(df),"cols":len(df.columns),"nulls":int(df.isnull().sum().sum())}
    with open(os.path.join(a.output_dir,"profiling.json"),"w") as f:json.dump(prof,f,indent=2,default=str)
    print("OK")
if __name__=="__main__":main()
