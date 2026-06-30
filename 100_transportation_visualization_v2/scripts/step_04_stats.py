#!/usr/bin/env python3
"""Statistical Analysis"""
import argparse,os,json
import pandas as pd,numpy as np
import matplotlib;matplotlib.use('Agg');import matplotlib.pyplot as plt
from scipy import stats
def main():
    p=argparse.ArgumentParser();p.add_argument("--data_dir",default="../data");p.add_argument("--output_dir",default=".")
    args=p.parse_args();os.makedirs(args.output_dir,exist_ok=True)
    print("STEP 4: Statistical Analysis")
    df=pd.read_csv(os.path.join(args.data_dir,"data.csv"))
    for c in df.select_dtypes(include=[np.number]).columns:df[c]=df[c].fillna(df[c].median())
    df.to_parquet(os.path.join(args.output_dir,"data.parquet"),index=False)
    print(f"  Records: {len(df)}")
    fig,axes=plt.subplots(1,2,figsize=(10,4))
    df["feature_a"].hist(bins=25,ax=axes[0],color="#3498db");axes[0].set_title("Feature A")
    df["feature_b"].hist(bins=25,ax=axes[1],color="#e74c3c");axes[1].set_title("Feature B")
    plt.tight_layout();fig.savefig(os.path.join(args.output_dir,f"step04.png"),dpi=100);plt.close()
    print("Done")
if __name__=="__main__":main()
