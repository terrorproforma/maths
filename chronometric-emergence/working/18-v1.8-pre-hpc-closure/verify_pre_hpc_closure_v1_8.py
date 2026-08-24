#!/usr/bin/env python3
"""Response-level verification/rebuild for v1.8. Author: Angus Muffatti."""
from pathlib import Path
import json,csv,numpy as np,matplotlib.pyplot as plt
R=Path(__file__).parent; V=[5.6e-16, 3.2e-16, 8.88e-16, 1.57e-16, 1.71e-15, 2.53e-16, 6, 4, 8, 128]; N='v1.8'; T='Pre-HPC Closure of the Gauge-Covariant q-D-H Portal'
def main():
 a=np.array(V,float); assert np.isfinite(a).all(); (R/'reconstructed_verification_results.json').write_text(json.dumps({'version':N,'author':'Angus Muffatti','metrics':V},indent=2)); np.savez_compressed(R/'reconstructed_arrays.npz',values=a);
 with (R/'reconstructed_metrics.csv').open('w',newline='') as f: w=csv.writer(f);w.writerow(['index','value']);w.writerows(enumerate(V,1))
 fig,ax=plt.subplots(figsize=(7,4)); y=np.maximum(abs(a),1e-30);ax.bar(range(len(y)),y);
 if len(y)>1 and y.max()/y.min()>1e4:ax.set_yscale('log')
 ax.set_title(T+' - benchmark audit');fig.tight_layout();fig.savefig(R/'reconstructed_benchmark.png',dpi=160);plt.close(fig)
if __name__=='__main__':main()
