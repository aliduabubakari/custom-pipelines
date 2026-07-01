#!/usr/bin/env python3
import argparse, os, json
import pandas as pd, numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
def main():
    p=argparse.ArgumentParser();p.add_argument("--data_dir",default="../data");p.add_argument("--output_dir",default=".")
    a=p.parse_args();os.makedirs(a.output_dir,exist_ok=True)
    print("STEP 1: Data Loading & Profiling — Stock Market Statistical Cleaning & Integration")
    stocks=pd.read_csv(os.path.join(a.data_dir,"stocks.csv"))
    indices=pd.read_csv(os.path.join(a.data_dir,"market_indices.csv"))
    stocks['date']=pd.to_datetime(stocks['date']);indices['date']=pd.to_datetime(indices['date'])
    print(f"   Stocks: {len(stocks)} rows, {stocks['ticker'].nunique()} tickers, {stocks['sector'].nunique()} sectors")
    print(f"   Indices: {len(indices)} days, S&P range: {indices['sp500'].min():.1f}-{indices['sp500'].max():.1f}")
    merged=stocks.merge(indices,on='date',how='left')
    merged.to_parquet(os.path.join(a.output_dir,"raw_merged.parquet"),index=False)
    dfs=[("stocks",stocks),("indices",indices)]
    for name,df in dfs:
        print(f"   [name]: {len(df)} rows x {len(df.columns)} cols")
        df.to_parquet(os.path.join(a.output_dir,f"raw_{name}.parquet"),index=False)
    prof={n:{"rows":len(d),"cols":len(d.columns)} for n,d in dfs}
    with open(os.path.join(a.output_dir,"profiling.json"),"w") as f:json.dump(prof,f,indent=2,default=str)
    print("OK")
if __name__=="__main__":main()
