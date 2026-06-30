#!/usr/bin/env python3
import argparse,os,numpy as np,pandas as pd
np.random.seed(42)
def g(n=400):
    return pd.DataFrame({"id":[f"X{i+1:04d}" for i in range(n)],"a":np.random.normal(100,25,n),"b":np.random.normal(50,15,n),"cat":np.random.choice(["A","B","C"],n),"y":np.random.choice([0,1],n,p=[.7,.3])})
def main():
    p=argparse.ArgumentParser();p.add_argument("--output_dir",default="data");p.add_argument("--n",type=int,default=400)
    a=p.parse_args();os.makedirs(a.output_dir,exist_ok=True)
    g(a.n).to_csv(os.path.join(a.output_dir,"data.csv"),index=False)
    print(f"OK {a.n}")
if __name__=="__main__":main()
