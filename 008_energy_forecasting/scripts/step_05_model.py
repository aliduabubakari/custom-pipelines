#!/usr/bin/env python3
import argparse, os, json, pickle
import pandas as pd, numpy as np
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.metrics import accuracy_score, roc_auc_score, mean_absolute_error, r2_score
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
def main():
    p=argparse.ArgumentParser();p.add_argument("--data_dir",default="../data");p.add_argument("--output_dir",default=".")
    a=p.parse_args();os.makedirs(a.output_dir,exist_ok=True)
    print("STEP 5: Model Training")
    df=pd.read_parquet(os.path.join(a.output_dir,"features.parquet"))
    drop=[c for c in df.columns if 'id' in c.lower() or 'date' in c.lower()]
    X=df.drop(columns=[c for c in drop if c in df.columns])
    target=None
    for tc in ['consumption','energy_kwh','kwh','demand']:
        if tc in X.columns:target=tc;break
    if target is None:target=X.select_dtypes(include=['float64']).columns[0]
    print(f"   Target: {target}")
    y=X[target];X=X.drop(columns=[target])
    num=[c for c in X.select_dtypes(include=['float64','int64']).columns if c in X.columns]
    X=X[num].fillna(X[num].median());scaler=StandardScaler();Xp=scaler.fit_transform(X)
    Xt,Xv,yt,yv=train_test_split(Xp,y,test_size=0.2,random_state=42)
    rf=RandomForestRegressor(n_estimators=100,max_depth=8,random_state=42,n_jobs=-1)
    rf.fit(Xt,yt);pred=rf.predict(Xv)
    print(f"   MAE: {mean_absolute_error(yv,pred):.1f}, R2: {r2_score(yv,pred):.3f}")
    with open(os.path.join(a.output_dir,"model.pkl"),"wb") as f:pickle.dump(rf,f)
if __name__=="__main__":main()
