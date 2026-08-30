#!/usr/bin/env python3
from __future__ import annotations
import argparse, csv, json
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import yaml


def read_csv(path):
    with path.open(newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))


def main(root: Path):
    out = root/'figures'; out.mkdir(exist_ok=True)
    seams=read_csv(root/'seam_ledger.csv')
    axes=['mathematical_inconsistency','ultraviolet_incompleteness','empirical_anomaly','unexplained_parameter','naturalness_fine_tuning','missing_initial_boundary_condition','inaccessible_regime']
    labels=['math inconsistency','UV incomplete','empirical anomaly','unexplained parameter','naturalness','missing initial/boundary','inaccessible regime']
    m=np.array([[int(r[a]) for a in axes] for r in seams])
    fig,ax=plt.subplots(figsize=(11,8.5))
    im=ax.imshow(m,aspect='auto',interpolation='nearest')
    ax.set_xticks(range(len(labels)),labels,rotation=35,ha='right')
    ax.set_yticks(range(len(seams)),[r['seam_id']+' '+r['seam'] for r in seams],fontsize=7)
    ax.set_title('TP-00 seam taxonomy: logically distinct problem classes')
    for i in range(m.shape[0]):
        for j in range(m.shape[1]):
            ax.text(j,i,str(m[i,j]),ha='center',va='center',fontsize=7)
    fig.colorbar(im,ax=ax,label='ledger flag')
    fig.tight_layout(); fig.savefig(out/'seam_taxonomy_matrix.png',dpi=220); fig.savefig(out/'seam_taxonomy_matrix.pdf'); plt.close(fig)

    scale_rows=[
        ('Hubble scale today',1.5e-42),('CMB temperature',2.35e-13),('neutrino mass scale',5e-11),
        ('electron mass',5.11e-4),('QCD scale',2e-1),('electroweak vev',2.4622e2),('LHC partonic scale',1e4),('reduced Planck scale',2.435e18)
    ]
    names=[x[0] for x in scale_rows]; vals=np.log10([x[1] for x in scale_rows])
    fig,ax=plt.subplots(figsize=(10,5.5)); y=np.arange(len(names)); ax.scatter(vals,y,s=60)
    for x,yy,(name,val) in zip(vals,y,scale_rows): ax.text(x+0.35,yy,f'{name}: {val:.3g} GeV',va='center',fontsize=8)
    ax.set_yticks([]); ax.set_xlabel('log10(energy / GeV)'); ax.set_title('Representative scales spanned by the frontier baseline')
    ax.grid(True,axis='x',alpha=.3); fig.tight_layout(); fig.savefig(out/'verified_scale_map.png',dpi=220); fig.savefig(out/'verified_scale_map.pdf'); plt.close(fig)

    with (root/'successor_acceptance_tests.yaml').open() as f: cfg=yaml.safe_load(f)
    tiers=[]
    for g in cfg['gates']:
        if g['tier'] not in tiers: tiers.append(g['tier'])
    counts=[sum(g['tier']==t for g in cfg['gates']) for t in tiers]
    fatal=[sum(g['tier']==t and g['fatal_if_applicable'] for g in cfg['gates']) for t in tiers]
    fig,ax=plt.subplots(figsize=(10,5.5)); x=np.arange(len(tiers)); w=.38
    ax.bar(x-w/2,counts,w,label='all gates'); ax.bar(x+w/2,fatal,w,label='fatal if applicable')
    ax.set_xticks(x,tiers,rotation=35,ha='right'); ax.set_ylabel('gate count'); ax.set_title('Successor acceptance architecture'); ax.legend(); fig.tight_layout()
    fig.savefig(out/'acceptance_architecture.png',dpi=220); fig.savefig(out/'acceptance_architecture.pdf'); plt.close(fig)

    domains=read_csv(root/'verified_domains.csv')
    classes={}
    for r in domains: classes[r['status']]=classes.get(r['status'],0)+1
    fig,ax=plt.subplots(figsize=(9,5)); ax.bar(range(len(classes)),list(classes.values())); ax.set_xticks(range(len(classes)),list(classes),rotation=30,ha='right')
    ax.set_ylabel('representative domain count'); ax.set_title('Evidence status is not binary: verification, parametrization and open microphysics')
    fig.tight_layout(); fig.savefig(out/'evidence_status_chart.png',dpi=220); fig.savefig(out/'evidence_status_chart.pdf'); plt.close(fig)

    results = root/'results'; results.mkdir(exist_ok=True)
    np.savez_compressed(
        results/'benchmark_arrays.npz',
        seam_taxonomy=m,
        seam_ids=np.array([row['seam_id'] for row in seams]),
        scale_log10_GeV=vals,
        scale_names=np.array(names),
        gate_tiers=np.array(tiers),
        gate_counts=np.array(counts,dtype=int),
        fatal_gate_counts=np.array(fatal,dtype=int),
    )
    metadata={
        'schema_version':'1.0.0',
        'deterministic':True,
        'random_seed':None,
        'source_files':['seam_ledger.csv','verified_domains.csv','successor_acceptance_tests.yaml'],
        'figure_files':sorted(path.name for path in out.glob('*')),
        'array_file':'results/benchmark_arrays.npz',
    }
    (results/'figure_metadata.json').write_text(json.dumps(metadata,indent=2)+'\n',encoding='utf-8')

    print('generated',len(list(out.glob('*'))),'figure files and benchmark_arrays.npz')
if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('--root',default='.'); main(Path(p.parse_args().root).resolve())
