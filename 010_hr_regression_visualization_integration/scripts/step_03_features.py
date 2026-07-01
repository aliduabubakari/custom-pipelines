#!/usr/bin/env python3
import argparse, os
import pandas as pd, numpy as np
def main():
    p=argparse.ArgumentParser();p.add_argument("--data_dir",default="../data");p.add_argument("--output_dir",default=".")
    a=p.parse_args();os.makedirs(a.output_dir,exist_ok=True)
    print("STEP 3: Feature Engineering — HR Salary Regression & Workforce Visualization")
    df=pd.read_parquet(os.path.join(a.output_dir,"cleaned.parquet"))
    if 'experience_years' in df.columns:df['exp_level']=pd.cut(df['experience_years'],bins=[-1,3,7,15,50],labels=["Junior","Mid","Senior","Executive"])
    if 'salary' in df.columns and 'budget_millions' in df.columns:df['salary_budget_ratio']=df['salary']/(df['budget_millions']*1e6).clip(lower=1)
    if 'age' in df.columns:df['age_group']=pd.cut(df['age'],bins=[0,30,45,60,100],labels=["<30","30-45","45-60","60+"])
    print("   Created: exp_level, salary_budget_ratio, age_group")
    df.to_parquet(os.path.join(a.output_dir,"features.parquet"),index=False)
    print(f"   [len(df.columns)] columns");print("OK")
if __name__=="__main__":main()
