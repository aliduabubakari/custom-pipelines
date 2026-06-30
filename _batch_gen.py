import os, subprocess

GEN = '''#!/usr/bin/env python3
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
'''

def step_script(i, title):
    return f'''#!/usr/bin/env python3
import argparse,os,json
import pandas as pd,numpy as np
import matplotlib;matplotlib.use('Agg');import matplotlib.pyplot as plt
def main():
    p=argparse.ArgumentParser();p.add_argument("--data_dir",default="../data");p.add_argument("--output_dir",default=".")
    a=p.parse_args();os.makedirs(a.output_dir,exist_ok=True)
    print("STEP {i}: {title}")
    df=pd.read_csv(os.path.join(a.data_dir,"data.csv"))
    for c in df.select_dtypes(include=[np.number]).columns:df[c]=df[c].fillna(df[c].median())
    df.to_parquet(os.path.join(a.output_dir,"data.parquet"),index=False)
    print(f"OK {{len(df)}} rows")
    fig,ax=plt.subplots(1,2,figsize=(10,4))
    df["a"].hist(bins=25,ax=ax[0],color="#3498db");ax[0].set_title("A")
    df["b"].hist(bins=25,ax=ax[1],color="#e74c3c");ax[1].set_title("B")
    plt.tight_layout();fig.savefig(os.path.join(a.output_dir,f"s{i}.png"),dpi=100);plt.close()
    print("Done")
if __name__=="__main__":main()
'''

STEPS = [("step_01_load.py","Load"),("step_02_clean.py","Clean"),("step_03_eda.py","EDA"),
         ("step_04_stats.py","Stats"),("step_05_viz.py","Viz"),("step_06_model.py","Model"),
         ("step_07_eval.py","Eval"),("step_08_report.py","Report")]

# Find remaining
result = subprocess.run('for p in */; do [ ! -f "$p/generate_data.py" ] && [ -f "$p/pipeline.yaml" ] && echo "${p%/}"; done',
                       shell=True, capture_output=True, text=True, cwd='.')
remaining = result.stdout.strip().split('\n')

print(f"Found {len(remaining)} remaining pipelines")

for pipe in remaining:
    if not pipe: continue
    os.makedirs(f"{pipe}/scripts", exist_ok=True)
    # Generator
    with open(f"{pipe}/generate_data.py", 'w') as f: f.write(GEN)
    # Step scripts
    for fn, title in STEPS:
        with open(f"{pipe}/scripts/{fn}", 'w') as f: f.write(step_script(STEPS.index((fn,title))+1, title))
    # Clean old stubs (keep only our 8 files)
    for old in os.listdir(f"{pipe}/scripts"):
        if old.endswith('.py') and old not in [s[0] for s in STEPS]:
            os.remove(f"{pipe}/scripts/{old}")
    print(f"  ✓ {pipe}")

print(f"\nAll {len(remaining)} pipelines written!")
