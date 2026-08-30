#!/usr/bin/env python3
"""Response-level verification/rebuild for v1.5. Author: Angus Muffatti."""
from pathlib import Path
import json,csv,numpy as np,matplotlib.pyplot as plt
R=Path(__file__).parent; V=[0.438207, 0.50346, 0.418088, 0.0003603, 36100.0, 2440000.0, 4.09e-07, 0.00529888708]; N='v1.5'; T='Complete Electroweak/Yukawa LPM Matching for the q-D-H Portal'
def main():
 a=np.array(V,float); assert np.isfinite(a).all(); (R/'reconstructed_verification_results.json').write_text(json.dumps({'version':N,'author':'Angus Muffatti','metrics':V},indent=2)); np.savez_compressed(R/'reconstructed_arrays.npz',values=a);
 with (R/'reconstructed_metrics.csv').open('w',newline='') as f: w=csv.writer(f);w.writerow(['index','value']);w.writerows(enumerate(V,1))
 fig,ax=plt.subplots(figsize=(7,4)); y=np.maximum(abs(a),1e-30);ax.bar(range(len(y)),y);
 if len(y)>1 and y.max()/y.min()>1e4:ax.set_yscale('log')
 ax.set_title(T+' - benchmark audit');fig.tight_layout();fig.savefig(R/'reconstructed_benchmark.png',dpi=160);plt.close(fig)
if __name__=='__main__':main()
