#!/usr/bin/env python3
import argparse, os
import pandas as pd, numpy as np
def main():
    p=argparse.ArgumentParser();p.add_argument("--data_dir",default="../data");p.add_argument("--output_dir",default=".")
    a=p.parse_args();os.makedirs(a.output_dir,exist_ok=True)
    print("STEP 3: Feature Engineering")
    df=pd.read_parquet(os.path.join(a.output_dir,"cleaned.parquet"))
    if 'age' in df.columns:df['age_group']=pd.cut(df['age'],bins=[0,30,50,65,80,120],labels=["<30","30-50","50-65","65-80","80+"])
    print("   Created: age_group")
    df.to_parquet(os.path.join(a.output_dir,"features.parquet"),index=False)
    print(f"   {len(df.columns)} cols");print("OK")
if __name__=="__main__":main()
