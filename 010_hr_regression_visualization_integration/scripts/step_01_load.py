#!/usr/bin/env python3
import argparse, os, json
import pandas as pd, numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
def main():
    p=argparse.ArgumentParser();p.add_argument("--data_dir",default="../data");p.add_argument("--output_dir",default=".")
    a=p.parse_args();os.makedirs(a.output_dir,exist_ok=True)
    print("STEP 1: Data Loading & Profiling — HR Salary Regression & Workforce Visualization")
    emp=pd.read_csv(os.path.join(a.data_dir,"employees.csv"))
    dept=pd.read_csv(os.path.join(a.data_dir,"departments.csv"))
    merged=emp.merge(dept,on='department',how='left')
    merged.to_parquet(os.path.join(a.output_dir,"raw_merged.parquet"),index=False)
    print(f"   Employees: {len(emp)}, Departments: {len(dept)}")
    print(f"   Salary range: ${emp['salary'].min():,} - ${emp['salary'].max():,}")
    dfs=[("employees",emp),("departments",dept)]
    for name,df in dfs:
        print(f"   [name]: {len(df)} rows x {len(df.columns)} cols")
        df.to_parquet(os.path.join(a.output_dir,f"raw_{name}.parquet"),index=False)
    prof={n:{"rows":len(d),"cols":len(d.columns)} for n,d in dfs}
    with open(os.path.join(a.output_dir,"profiling.json"),"w") as f:json.dump(prof,f,indent=2,default=str)
    print("OK")
if __name__=="__main__":main()
