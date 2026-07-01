#!/usr/bin/env python3
import argparse, os, json
import pandas as pd, numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
def main():
    p=argparse.ArgumentParser();p.add_argument("--data_dir",default="../data");p.add_argument("--output_dir",default=".")
    a=p.parse_args();os.makedirs(a.output_dir,exist_ok=True)
    print("STEP 1: Load & Profile")
    pat=pd.read_csv(os.path.join(a.data_dir,"patients.csv"))
    with open(os.path.join(a.data_dir,"admissions.json")) as f:adm=pd.DataFrame(json.load(f))
    with open(os.path.join(a.data_dir,"lab_results.json")) as f:lab=pd.DataFrame(json.load(f))
    med=pd.read_excel(os.path.join(a.data_dir,"medications.xlsx"))
    dfs=[("patients",pat),("admissions",adm),("lab_results",lab),("medications",med)]
    for name,df in dfs:
        print(f"   {name}: {len(df)} rows x {len(df.columns)} cols")
        df.to_parquet(os.path.join(a.output_dir,f"raw_{name}.parquet"),index=False)
    prof={n:{"rows":len(d),"cols":len(d.columns)} for n,d in dfs}
    with open(os.path.join(a.output_dir,"profiling.json"),"w") as f:json.dump(prof,f,indent=2,default=str)
    print("OK")
if __name__=="__main__":main()
