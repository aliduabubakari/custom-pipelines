#!/usr/bin/env python3
import argparse, os
import pandas as pd, numpy as np
def main():
    p=argparse.ArgumentParser();p.add_argument("--data_dir",default="../data");p.add_argument("--output_dir",default=".")
    a=p.parse_args();os.makedirs(a.output_dir,exist_ok=True)
    print("STEP 3: Feature Engineering — Statistical Integration & Analysis Benchmark")
    df=pd.read_parquet(os.path.join(a.output_dir,"cleaned.parquet"))
    if 'baseline_score' in df.columns and 'post_score' in df.columns:df['improvement']=df['post_score']-df['baseline_score']
    if 'age' in df.columns:df['age_group']=pd.cut(df['age'],bins=[0,30,50,65,90],labels=["Young","Middle","Senior","Elderly"])
    if 'sessions_attended' in df.columns:df['attendance_rate']=df['sessions_attended']/df['sessions_attended'].max()
    print("   Created: improvement, age_group, attendance_rate")
    df.to_parquet(os.path.join(a.output_dir,"features.parquet"),index=False)
    print(f"   [len(df.columns)] columns");print("OK")
if __name__=="__main__":main()
