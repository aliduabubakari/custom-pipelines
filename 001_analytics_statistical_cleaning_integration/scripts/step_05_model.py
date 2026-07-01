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
    print("STEP 5: Statistical Analysis & Model Training — Stock Market Statistical Cleaning & Integration")
    df=pd.read_parquet(os.path.join(a.output_dir,"features.parquet"))
    drop=[c for c in df.columns if 'id' in c.lower() or 'date' in c.lower() or 'ticker' in c.lower()]
    X=df.drop(columns=[c for c in drop if c in df.columns])
    if 'direction' not in X.columns:
        if 'daily_return' in X.columns:X['direction']=(X['daily_return']>0).astype(int)
        else:X['direction']=(np.random.random(len(X))>0.5).astype(int)
    y=X['direction'];X=X.drop(columns=['direction'])
    num=[c for c in X.select_dtypes(include=['float64','int64']).columns if c in X.columns]
    cat=[c for c in X.select_dtypes(include=['object','category']).columns if c in X.columns and X[c].nunique()<=20]
    pp=ColumnTransformer([("num",StandardScaler(),num),("cat",OneHotEncoder(handle_unknown="ignore",sparse_output=False,max_categories=10),cat)],remainder="drop")
    Xp=pp.fit_transform(X);Xt,Xv,yt,yv=train_test_split(Xp,y,test_size=0.2,stratify=y,random_state=42)
    rf=RandomForestClassifier(n_estimators=150,max_depth=10,random_state=42,class_weight="balanced",n_jobs=-1)
    rf.fit(Xt,yt);pred=rf.predict_proba(Xv)[:,1]
    print(f"   ROC-AUC: {roc_auc_score(yv, pred, multi_class="ovr", average="weighted"):.3f}, Acc: {accuracy_score(yv,(pred>=0.5).astype(int)):.2%}")
    with open(os.path.join(a.output_dir,"model.pkl"),"wb") as f:pickle.dump(rf,f)
    # Feature importance
    imp=pd.Series(rf.feature_importances_,index=pp.get_feature_names_out()).sort_values(ascending=False).head(5)
    print(f"   Top features: {list(imp.index[:3])}")
if __name__=="__main__":main()
