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
    print("STEP 5: Statistical Analysis & Model Training — HR Workforce Visualization & Data Validation")
    df=pd.read_parquet(os.path.join(a.output_dir,"features.parquet"))
    # Clustering for workforce segmentation
    from sklearn.cluster import KMeans
    drop=['emp_id','department','status','gender']
    X=df.drop(columns=[c for c in drop if c in df.columns])
    num=[c for c in X.select_dtypes(include=['float64','int64']).columns if c in X.columns]
    X_num=X[num].fillna(0);scaler=StandardScaler();Xp=scaler.fit_transform(X_num)
    km=KMeans(n_clusters=3,random_state=42,n_init=10);clusters=km.fit_predict(Xp)
    df['workforce_cluster']=clusters
    print("\n   Workforce Clusters:")
    for c in range(3):
        clust=df[df['workforce_cluster']==c]
        print(f"     Cluster {c} (n={len(clust)}): salary=${clust['salary'].mean():,.0f}, tenure={clust['tenure_years'].mean():.1f}yr, perf={clust['performance_score'].mean():.1f}")
    # Simple classification: predict high performance
    if 'performance_score' in df.columns:
        y=(df['performance_score']>=df['performance_score'].median()).astype(int)
        drop2=['workforce_cluster','performance_score']
        X2=df.drop(columns=[c for c in drop+drop2 if c in df.columns])
        num2=[c for c in X2.select_dtypes(include=['float64','int64']).columns if c in X2.columns]
        cat2=[c for c in X2.select_dtypes(include=['object','category']).columns if c in X2.columns and X2[c].nunique()<=20]
        pp=ColumnTransformer([("num",StandardScaler(),num2),("cat",OneHotEncoder(handle_unknown="ignore",sparse_output=False,max_categories=10),cat2)],remainder="drop")
        Xp2=pp.fit_transform(X2);Xt,Xv,yt,yv=train_test_split(Xp2,y,test_size=0.2,stratify=y,random_state=42)
        rf=RandomForestClassifier(n_estimators=100,max_depth=8,random_state=42,n_jobs=-1)
        rf.fit(Xt,yt);pred=rf.predict_proba(Xv)[:,1]
        print(f"\n   High Performer Prediction: ROC-AUC={roc_auc_score(yv, pred, multi_class="ovr", average="weighted"):.3f}, Acc={accuracy_score(yv,(pred>=0.5).astype(int)):.2%}")
        with open(os.path.join(a.output_dir,"model.pkl"),"wb") as f:pickle.dump(rf,f)
if __name__=="__main__":main()
