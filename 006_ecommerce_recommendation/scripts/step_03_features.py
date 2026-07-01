#!/usr/bin/env python3
import argparse, os
import pandas as pd, numpy as np
def main():
    p=argparse.ArgumentParser();p.add_argument("--data_dir",default="../data");p.add_argument("--output_dir",default=".")
    a=p.parse_args();os.makedirs(a.output_dir,exist_ok=True)
    print("STEP 3: Feature Engineering")
    df=pd.read_parquet(os.path.join(a.output_dir,"cleaned.parquet"))
    if 'price' in df.columns:df['price_tier']=pd.cut(df['price'],bins=[0,25,50,100,500,10000],labels=["Budget","Standard","Premium","Luxury","Ultra"])
    if 'rating' in df.columns:df['rating_tier']=pd.cut(df['rating'],bins=[0,3,4,5.1],labels=["Low","Medium","High"])
    print("   Created: price_tier, rating_tier")
    df.to_parquet(os.path.join(a.output_dir,"features.parquet"),index=False)
    print(f"   {len(df.columns)} cols");print("OK")
if __name__=="__main__":main()
