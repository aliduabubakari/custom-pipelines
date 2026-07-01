#!/usr/bin/env python3
import argparse, os
import pandas as pd, numpy as np
def main():
    p=argparse.ArgumentParser();p.add_argument("--data_dir",default="../data");p.add_argument("--output_dir",default=".")
    a=p.parse_args();os.makedirs(a.output_dir,exist_ok=True)
    print("STEP 3: Feature Engineering")
    df=pd.read_parquet(os.path.join(a.output_dir,"cleaned.parquet"))
    if 'tenure_days' in df.columns:df['tenure_years']=df['tenure_days']/365
    df['tenure_group']=pd.cut(df.get('tenure_years',0),bins=[-0.01,1,3,5,10,50],labels=["<1yr","1-3yr","3-5yr","5-10yr","10yr+"])
    print("   Created: tenure_years, tenure_group")
    df.to_parquet(os.path.join(a.output_dir,"features.parquet"),index=False)
    print(f"   {len(df.columns)} cols");print("OK")
if __name__=="__main__":main()
