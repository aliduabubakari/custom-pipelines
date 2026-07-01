#!/usr/bin/env python3
"""Step 3: Feature Engineering — Analysis features"""
import argparse, os
import pandas as pd, numpy as np
def main():
    p=argparse.ArgumentParser();p.add_argument("--data_dir",default="../data");p.add_argument("--output_dir",default=".")
    a=p.parse_args();os.makedirs(a.output_dir,exist_ok=True)
    print("STEP 3: Feature Engineering")
    df=pd.read_parquet(os.path.join(a.output_dir,"cleaned.parquet"))
    features_created=[]
    if 'age' in df.columns and 'experience_years' in df.columns:
        df['age_started']=df['age']-df['experience_years'];features_created.append('age_started')
    if 'study_hours_per_week' in df.columns:df['study_group']=pd.cut(df['study_hours_per_week'],bins=[0,5,15,25,50],labels=['Low','Medium','High','Very High']);features_created.append('study_group')
    if 'previous_gpa' in df.columns and 'current_gpa' in df.columns:df['gpa_change']=df['current_gpa']-df['previous_gpa'];features_created.append('gpa_change')
    print(f'   Created: {len(features_created)} features')
    df.to_parquet(os.path.join(a.output_dir,"features.parquet"),index=False)
    print(f"   {len(df.columns)} columns");print("OK")
if __name__=="__main__":main()
