#!/usr/bin/env python3
import argparse, os, json, pickle
import pandas as pd, numpy as np
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.metrics import accuracy_score, roc_auc_score, mean_absolute_error, r2_score, classification_report
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
def main():
    p=argparse.ArgumentParser();p.add_argument("--data_dir",default="../data");p.add_argument("--output_dir",default=".")
    a=p.parse_args();os.makedirs(a.output_dir,exist_ok=True)
    print("STEP 5: Statistical Analysis & Model Training — HR Salary Regression & Workforce Visualization")
    df=pd.read_parquet(os.path.join(a.output_dir,"features.parquet"))
    y=df['salary']
    drop=['emp_id','salary','department','role','education','gender','location']
    X=df.drop(columns=[c for c in drop if c in df.columns])
    num=[c for c in X.select_dtypes(include=['float64','int64']).columns if c in X.columns]
    cat=[c for c in X.select_dtypes(include=['object','category']).columns if c in X.columns and X[c].nunique()<=20]
    pp=ColumnTransformer([("num",StandardScaler(),num),("cat",OneHotEncoder(handle_unknown="ignore",sparse_output=False,max_categories=10),cat)],remainder="drop")
    Xp=pp.fit_transform(X);Xt,Xv,yt,yv=train_test_split(Xp,y,test_size=0.2,random_state=42)
    lr=LinearRegression();lr.fit(Xt,yt)
    rf=RandomForestRegressor(n_estimators=150,max_depth=10,random_state=42,n_jobs=-1);rf.fit(Xt,yt)
    lr_pred=lr.predict(Xv);rf_pred=rf.predict(Xv)
    print(f"   LinearRegression: MAE=${mean_absolute_error(yv,lr_pred):.0f}, R2={r2_score(yv,lr_pred):.3f}")
    print(f"   RandomForest:     MAE=${mean_absolute_error(yv,rf_pred):.0f}, R2={r2_score(yv,rf_pred):.3f}")
    best_m=rf if r2_score(yv,rf_pred)>r2_score(yv,lr_pred) else lr
    with open(os.path.join(a.output_dir,"model.pkl"),"wb") as f:pickle.dump(best_m,f)
    # Salary by department
    print("\n   Avg Salary by Department:")
    for d in df['department'].unique()[:5]:print(f"     {d}: ${df[df['department']==d]['salary'].mean():,.0f}")
if __name__=="__main__":main()
