#!/usr/bin/env python3
import argparse, os, json
from datetime import datetime
def main():
    p=argparse.ArgumentParser();p.add_argument("--data_dir",default="../data");p.add_argument("--output_dir",default=".")
    a=p.parse_args();os.makedirs(a.output_dir,exist_ok=True)
    print("STEP 6: Final Report")
    rpt="="*60+"\n    EMPLOYEE ATTRITION PREDICTION — FINAL REPORT\n    "+datetime.now().strftime('%Y-%m-%d %H:%M:%S')+"\n"+"="*60+"\n\nDomain: HR Analytics\nPredicting employee attrition using demographics, engagement surveys, and performance reviews.\n\nThis pipeline executed: Load → Clean → Feature Engineering → EDA → Modeling → Report\nKey outputs are in the output/ directory.\n"+"="*60
    with open(os.path.join(a.output_dir,"final_report.txt"),"w") as f:f.write(rpt)
    print(rpt);print("OK")
if __name__=="__main__":main()
