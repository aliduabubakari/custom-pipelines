#!/usr/bin/env python3
"""Step 5: Model Training — Cleaning, Integration, Regression"""
import argparse, os, json, pickle
import pandas as pd, numpy as np
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.metrics import accuracy_score, roc_auc_score, mean_absolute_error, r2_score
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
def main():
    p=argparse.ArgumentParser();p.add_argument("--data_dir",default="../data");p.add_argument("--output_dir",default=".")
    a=p.parse_args();os.makedirs(a.output_dir,exist_ok=True)
    print("STEP 5: Model Training — cleaning, integration, regression")
    df=pd.read_parquet(os.path.join(a.output_dir,"features.parquet"))
    target='operational_cost'
    if target not in df.columns:target=df.select_dtypes(include=['int64','float64']).columns[-1]
    y=df[target]
    drop=[c for c in df.columns if 'id' in c.lower() or c==target]
    X=df.drop(columns=[c for c in drop if c in df.columns])
    num=[c for c in X.select_dtypes(include=['float64','int64']).columns if c in X.columns]
    cat=[c for c in X.select_dtypes(include=['object','category']).columns if c in X.columns and X[c].nunique()<=20]
    pp=ColumnTransformer([('num',StandardScaler(),num),('cat',OneHotEncoder(handle_unknown='ignore',sparse_output=False,max_categories=10),cat)],remainder='drop')
    Xp=pp.fit_transform(X)
    # Regression
    Xt,Xv,yt,yv=train_test_split(Xp,y,test_size=0.2,random_state=42)
    rf=RandomForestRegressor(n_estimators=100,max_depth=8,random_state=42,n_jobs=-1)
    rf.fit(Xt,yt);pred=rf.predict(Xv)
    print(f'   MAE: {mean_absolute_error(yv,pred):.2f}, R2: {r2_score(yv,pred):.3f}')
    with open(os.path.join(a.output_dir,'model.pkl'),'wb') as f:pickle.dump(rf,f)
    print('   Model saved')
if __name__=="__main__":main()
