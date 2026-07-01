#!/usr/bin/env python3
import argparse, os, json
import pandas as pd, numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
import seaborn as sns
def main():
    p=argparse.ArgumentParser();p.add_argument("--data_dir",default="../data");p.add_argument("--output_dir",default=".")
    a=p.parse_args();os.makedirs(a.output_dir,exist_ok=True)
    print("STEP 4: EDA")
    df=pd.read_parquet(os.path.join(a.output_dir,"features.parquet"))
    num=[c for c in df.select_dtypes(include=['float64','int64']).columns if c not in ['customer_id','employee_id','patient_id','sensor_id','machine_id','claim_id'] and df[c].nunique()>1]
    print(f"   {len(num)} numerical features")
    fig,axes=plt.subplots(2,2,figsize=(14,12));fig.suptitle("HEALTHCARE READMISSION PREDICTION — EDA",fontweight="bold")
    for i in range(min(4,len(num))):
        r,c=i//2,i%2
        axes[r,c].hist(df[num[i]].dropna().clip(df[num[i]].quantile(0.01),df[num[i]].quantile(0.99)),bins=30,color=["#3498db","#e74c3c","#2ecc71","#f39c12"][i],edgecolor="white")
        axes[r,c].set_title(num[i])
    plt.tight_layout();fig.savefig(os.path.join(a.output_dir,"step04_eda.png"),dpi=120);plt.close()
    print("OK")
if __name__=="__main__":main()
