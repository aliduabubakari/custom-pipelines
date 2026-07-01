#!/usr/bin/env python3
"""Step 3: Feature Engineering — Cleaning, Statistical, Validation features"""
import argparse, os
import pandas as pd, numpy as np
def main():
    p=argparse.ArgumentParser();p.add_argument("--data_dir",default="../data");p.add_argument("--output_dir",default=".")
    a=p.parse_args();os.makedirs(a.output_dir,exist_ok=True)
    print("STEP 3: Feature Engineering")
    df=pd.read_parquet(os.path.join(a.output_dir,"cleaned.parquet"))
    features_created=[]
    if 'points_per_game' in df.columns and 'games_played' in df.columns:
        df['total_points']=df['points_per_game']*df['games_played'];features_created.append('total_points')
    if 'age' in df.columns and 'experience_years' in df.columns:
        df['age_started']=df['age']-df['experience_years'];features_created.append('age_started')
    if 'salary_millions' in df.columns:df['salary_tier']=pd.cut(df['salary_millions'],bins=[0,3,10,20,50],labels=['Low','Mid','High','Star']);features_created.append('salary_tier')
    print(f'   Created: {len(features_created)} features')
    df.to_parquet(os.path.join(a.output_dir,"features.parquet"),index=False)
    print(f"   {len(df.columns)} columns");print("OK")
if __name__=="__main__":main()
