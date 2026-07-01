#!/usr/bin/env python3
import argparse, os, json
import pandas as pd, numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
import seaborn as sns
def main():
    p=argparse.ArgumentParser();p.add_argument("--data_dir",default="../data");p.add_argument("--output_dir",default=".")
    a=p.parse_args();os.makedirs(a.output_dir,exist_ok=True)
    print("STEP 4: EDA & Visualization — HR Workforce Visualization & Data Validation")
    df=pd.read_parquet(os.path.join(a.output_dir,"features.parquet"))
    drop_keys=['id','date','name']
    num=[c for c in df.select_dtypes(include=['float64','int64']).columns if not any(k in c.lower() for k in drop_keys) and df[c].nunique()>1]
    print(f"   [len(num)] numerical features found")
    fig,axes=plt.subplots(2,2,figsize=(14,12));fig.suptitle("HR Workforce Visualization & Data Validation — EDA Dashboard",fontweight="bold",fontsize=14)
    colors=["#3498db","#e74c3c","#2ecc71","#f39c12"]
    for i in range(min(4,len(num))):
        r,c=i//2,i%2
        d=df[num[i]].dropna().clip(df[num[i]].quantile(0.01),df[num[i]].quantile(0.99))
        axes[r,c].hist(d,bins=30,color=colors[i],edgecolor="white");axes[r,c].set_title(num[i])
    plt.tight_layout();fig.savefig(os.path.join(a.output_dir,"step04_eda.png"),dpi=120);plt.close()
    if len(num)>=2:
        top10=df[num[:10]].corr()
        fig2,ax2=plt.subplots(figsize=(10,8));sns.heatmap(top10,annot=True,fmt=".2f",cmap="RdBu_r",ax=ax2,center=0)
        ax2.set_title("Correlation Heatmap");plt.tight_layout()
        fig2.savefig(os.path.join(a.output_dir,"step04_correlation.png"),dpi=120);plt.close()
    print("OK")
if __name__=="__main__":main()
