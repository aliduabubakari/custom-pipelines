#!/usr/bin/env python3
import argparse, os
import pandas as pd, numpy as np
def main():
    p=argparse.ArgumentParser();p.add_argument("--data_dir",default="../data");p.add_argument("--output_dir",default=".")
    a=p.parse_args();os.makedirs(a.output_dir,exist_ok=True)
    print("STEP 3: Feature Engineering")
    df=pd.read_parquet(os.path.join(a.output_dir,"cleaned.parquet"))
    if 'temperature' in df.columns and 'vibration' in df.columns:df['temp_vib_ratio']=df['temperature']/df['vibration'].clip(lower=0.01)
    if 'runtime_hours' in df.columns:df['runtime_days']=df['runtime_hours']/24
    print("   Created features")
    df.to_parquet(os.path.join(a.output_dir,"features.parquet"),index=False)
    print(f"   {len(df.columns)} cols");print("OK")
if __name__=="__main__":main()
