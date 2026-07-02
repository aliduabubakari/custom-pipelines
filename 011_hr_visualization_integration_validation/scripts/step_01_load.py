#!/usr/bin/env python3
import argparse, os, json
import pandas as pd, numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
def main():
    p=argparse.ArgumentParser();p.add_argument("--data_dir",default="../data");p.add_argument("--output_dir",default=".")
    a=p.parse_args();os.makedirs(a.output_dir,exist_ok=True)
    print("STEP 1: Data Loading & Profiling — HR Workforce Visualization & Data Validation")
    hr=pd.read_csv(os.path.join(a.data_dir,"hr_data.csv"))
    print(f"   HR data: {len(hr)} employees, {len(hr.columns)} columns")
    print(f"   Departments: {hr['department'].nunique()}, Status: {hr['status'].value_counts().to_dict()}")
    print(f"   Avg salary: ${hr['salary'].mean():,.0f}, Avg tenure: {hr['tenure_years'].mean():.1f} yrs")
    # Validation checks
    checks=[]
    if hr['emp_id'].duplicated().sum()>0:checks.append(f"DUPLICATE: {hr['emp_id'].duplicated().sum()} duplicate employee IDs")
    if hr['salary'].isnull().sum()>0:checks.append(f"NULL: {hr['salary'].isnull().sum()} missing salaries")
    if (hr['salary']<=0).sum()>0:checks.append(f"INVALID: {(hr['salary']<=0).sum()} zero/negative salaries")
    if (hr['age']<18).sum()>0:checks.append(f"INVALID: {(hr['age']<18).sum()} employees under 18")
    print(f"\n   Validation: {len(checks)} issues found")
    for c in checks:print(f"     ⚠️ {c}")
    with open(os.path.join(a.output_dir,"validation_report.json"),"w") as f:json.dump({"checks":checks,"total_issues":len(checks)},f,default=str,indent=2)
    dfs=[("hr_data",hr)]
    for name,df in dfs:
        print(f"   {name}: {len(df)} rows x {len(df.columns)} cols")
        df.to_parquet(os.path.join(a.output_dir,f"raw_{name}.parquet"),index=False)
    prof={n:{"rows":len(d),"cols":len(d.columns)} for n,d in dfs}
    with open(os.path.join(a.output_dir,"profiling.json"),"w") as f:json.dump(prof,f,indent=2,default=str)
    print("OK")
if __name__=="__main__":main()
