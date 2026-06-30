#!/usr/bin/env python3
import argparse,os,json
import pandas as pd,numpy as np
import matplotlib;matplotlib.use('Agg');import matplotlib.pyplot as plt
def main():
    p=argparse.ArgumentParser();p.add_argument("--data_dir",default="../data");p.add_argument("--output_dir",default=".")
    a=p.parse_args();os.makedirs(a.output_dir,exist_ok=True)
    print("STEP 1: Load")
    df=pd.read_csv(os.path.join(a.data_dir,"data.csv"))
    for c in df.select_dtypes(include=[np.number]).columns:df[c]=df[c].fillna(df[c].median())
    df.to_parquet(os.path.join(a.output_dir,"data.parquet"),index=False)
    print(f"OK {len(df)} rows")
    fig,ax=plt.subplots(1,2,figsize=(10,4))
    df["a"].hist(bins=25,ax=ax[0],color="#3498db");ax[0].set_title("A")
    df["b"].hist(bins=25,ax=ax[1],color="#e74c3c");ax[1].set_title("B")
    plt.tight_layout();fig.savefig(os.path.join(a.output_dir,f"s1.png"),dpi=100);plt.close()
    print("Done")
if __name__=="__main__":main()
