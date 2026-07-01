#!/usr/bin/env python3
import argparse, os
import pandas as pd, numpy as np
def main():
    p=argparse.ArgumentParser();p.add_argument("--data_dir",default="../data");p.add_argument("--output_dir",default=".")
    a=p.parse_args();os.makedirs(a.output_dir,exist_ok=True)
    print("STEP 2: Clean & Standardize")
    df=pd.read_parquet(os.path.join(a.output_dir,"raw_energy.parquet"))
    for c in df.columns:
        if df[c].dtype in ['float64','int64']:df[c]=df[c].fillna(df[c].median())
        elif df[c].dtype=='object':df[c]=df[c].fillna("Unknown")
    for c in df.select_dtypes(include=['object']).columns:df[c]=df[c].astype(str).str.strip()
    for c in df.select_dtypes(include=['float64','int64']).columns:
        if df[c].nunique()>5:p99=df[c].quantile(0.99);df[c]=df[c].clip(upper=p99)
    df.to_parquet(os.path.join(a.output_dir,"cleaned.parquet"),index=False)
    print(f"   {len(df)} rows saved");print("OK")
if __name__=="__main__":main()
