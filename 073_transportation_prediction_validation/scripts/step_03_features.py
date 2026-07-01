#!/usr/bin/env python3
"""Step 3: Feature Engineering — Prediction, Validation features"""
import argparse, os
import pandas as pd, numpy as np
def main():
    p=argparse.ArgumentParser();p.add_argument("--data_dir",default="../data");p.add_argument("--output_dir",default=".")
    a=p.parse_args();os.makedirs(a.output_dir,exist_ok=True)
    print("STEP 3: Feature Engineering")
    df=pd.read_parquet(os.path.join(a.output_dir,"cleaned.parquet"))
    features_created=[]
    if 'delay_minutes' in df.columns:df['delay_category']=pd.cut(df['delay_minutes'],bins=[-1,5,15,30,100],labels=['OnTime','Slight','Moderate','Severe']);features_created.append('delay_category')
    if 'distance_km' in df.columns and 'passengers' in df.columns:df['passenger_km']=df['distance_km']*df['passengers'];features_created.append('passenger_km')
    if 'departure_hour' in df.columns:df['is_rush_hour']=df['departure_hour'].isin([7,8,9,17,18,19]).astype(int);features_created.append('is_rush_hour')
    print(f'   Created: {len(features_created)} features')
    df.to_parquet(os.path.join(a.output_dir,"features.parquet"),index=False)
    print(f"   {len(df.columns)} columns");print("OK")
if __name__=="__main__":main()
