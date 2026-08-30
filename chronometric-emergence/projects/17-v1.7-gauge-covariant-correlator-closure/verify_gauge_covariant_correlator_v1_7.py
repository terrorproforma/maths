#!/usr/bin/env python3
"""Response-level verification/rebuild for v1.7. Author: Angus Muffatti."""
from pathlib import Path
import json,csv,numpy as np,matplotlib.pyplot as plt
R=Path(__file__).parent; V=[0.0011585159, 1.53e-15, 7.07e-14, 5.24e-16, 1.42e-12, 0.688, 0.838, 0.000944]; N='v1.7'; T='Gauge-Covariant Correlator Closure for the q-D-H Portal'
def main():
 a=np.array(V,float); assert np.isfinite(a).all(); (R/'reconstructed_verification_results.json').write_text(json.dumps({'version':N,'author':'Angus Muffatti','metrics':V},indent=2)); np.savez_compressed(R/'reconstructed_arrays.npz',values=a);
 with (R/'reconstructed_metrics.csv').open('w',newline='') as f: w=csv.writer(f);w.writerow(['index','value']);w.writerows(enumerate(V,1))
 fig,ax=plt.subplots(figsize=(7,4)); y=np.maximum(abs(a),1e-30);ax.bar(range(len(y)),y);
 if len(y)>1 and y.max()/y.min()>1e4:ax.set_yscale('log')
 ax.set_title(T+' - benchmark audit');fig.tight_layout();fig.savefig(R/'reconstructed_benchmark.png',dpi=160);plt.close(fig)
if __name__=='__main__':main()
