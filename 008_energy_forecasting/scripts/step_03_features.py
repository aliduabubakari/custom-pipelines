#!/usr/bin/env python3
import argparse, os
import pandas as pd, numpy as np
def main():
    p=argparse.ArgumentParser();p.add_argument("--data_dir",default="../data");p.add_argument("--output_dir",default=".")
    a=p.parse_args();os.makedirs(a.output_dir,exist_ok=True)
    print("STEP 3: Feature Engineering")
    df=pd.read_parquet(os.path.join(a.output_dir,"cleaned.parquet"))
    if 'date' in df.columns:
        df['date']=pd.to_datetime(df['date'],errors='coerce')
        df['month']=df['date'].dt.month;df['quarter']=df['date'].dt.quarter
        df['day_of_week']=df['date'].dt.dayofweek;df['is_weekend']=(df['day_of_week']>=5).astype(int)
        print("   Created: month, quarter, day_of_week, is_weekend")
    df.to_parquet(os.path.join(a.output_dir,"features.parquet"),index=False)
    print(f"   {len(df.columns)} cols");print("OK")
if __name__=="__main__":main()
