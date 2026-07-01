#!/usr/bin/env python3
import argparse, os
import pandas as pd, numpy as np
def main():
    p=argparse.ArgumentParser();p.add_argument("--data_dir",default="../data");p.add_argument("--output_dir",default=".")
    a=p.parse_args();os.makedirs(a.output_dir,exist_ok=True)
    print("STEP 3: Feature Engineering — Stock Market Statistical Cleaning & Integration")
    df=pd.read_parquet(os.path.join(a.output_dir,"cleaned.parquet"))
    if 'close' in df.columns and 'open' in df.columns:df['daily_return']=(df['close']-df['open'])/df['open'].clip(lower=0.01)*100
    if 'sp500' in df.columns and 'nasdaq' in df.columns:df['sp500_nasdaq_spread']=df['sp500']-df['nasdaq']
    if 'volume' in df.columns:df['volume_category']=pd.cut(df['volume'],bins=[0,1e6,5e6,1e7,1e9],labels=["Low","Medium","High","Very High"])
    if 'daily_return' in df.columns:df['direction']=(df['daily_return']>0).astype(int)
    print("   Created: daily_return, sp500_nasdaq_spread, volume_category, direction")
    df.to_parquet(os.path.join(a.output_dir,"features.parquet"),index=False)
    print(f"   [len(df.columns)] columns");print("OK")
if __name__=="__main__":main()
