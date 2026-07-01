#!/usr/bin/env python3
import argparse, os
import pandas as pd, numpy as np
def main():
    p=argparse.ArgumentParser();p.add_argument("--data_dir",default="../data");p.add_argument("--output_dir",default=".")
    a=p.parse_args();os.makedirs(a.output_dir,exist_ok=True)
    print("STEP 3: Feature Engineering — HR Workforce Visualization & Data Validation")
    df=pd.read_parquet(os.path.join(a.output_dir,"cleaned.parquet"))
    if 'tenure_years' in df.columns:df['tenure_group']=pd.cut(df['tenure_years'],bins=[-1,1,3,7,15,50],labels=["<1yr","1-3yr","3-7yr","7-15yr","15yr+"])
    if 'age' in df.columns:df['age_group']=pd.cut(df['age'],bins=[0,30,45,60,100],labels=["<30","30-45","45-60","60+"])
    if 'salary' in df.columns and 'bonus' in df.columns:df['bonus_pct']=(df['bonus']/df['salary'].clip(lower=1)*100).clip(0,100)
    print("   Created: tenure_group, age_group, bonus_pct")
    df.to_parquet(os.path.join(a.output_dir,"features.parquet"),index=False)
    print(f"   [len(df.columns)] columns");print("OK")
if __name__=="__main__":main()
