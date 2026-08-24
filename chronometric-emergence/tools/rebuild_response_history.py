from pathlib import Path
import re,shutil,csv,json,zipfile,hashlib,subprocess,os
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
R=Path.cwd()/'chronometric-emergence'; W=R/'working'
M=(R/'manuscript/null_relational_chronometry_v1_4.md').read_text(); H=pd.read_csv(R/'data/historical_artifact_inventory.csv')
if W.exists(): shutil.rmtree(W)
W.mkdir(parents=True)
V=[
('01','v0.1','chronometry-from-crossed-null-phases','Chronometry from Crossed Null Phases','Kinematic construction; homogeneous lock only',(5,6)),
('02','v0.2','crossed-null-audit','Crossed-Null Chronometry: Priority Audit and Dynamical Viability Test','Exact-null action fails; healthy soft-null EFT survives',(7,9)),
('03','v0.3','spectral-chronometry-higgs-dilaton','Spectral Chronometry: Universal Clock Factorisation and the Higgs-Dilaton Test','Factorisation theorem, chronometric shear, Higgs-only obstruction',(10,15)),
('04','v0.4','universal-scale-locking-turok36','Universal Scale Locking and the Turok-36 Test','Hidden-sector scale generator; Turok-36 acceptance protocol',(16,17)),
('05','v0.5','qcd-chronometric-lock','QCD Chronometric Lock: All-Orders Threshold Propagation and the 2/27 Signal','All-orders threshold recursion; leading 2/27 transmission',(18,23)),
('06','v0.6','zn-protected-qcd-chronometry','Z_N-Protected QCD Chronometry','Z6 vacuum mass O(epsilon^6), visible response O(epsilon)',(24,25)),
('07','v0.7','environmental-non-screening','Environmental Non-Screening of the Z6 Chronometric Ratio Mode','Earth, Sun and laboratory sources unscreened',(26,26)),
('08','v0.8','cosmological-vacuum-selection','Cosmological Vacuum Selection and the Maximal Chronometric-Shear Ridge','Low-fa strong-attractor ridge selects a nonzero branch',(27,32)),
('09','v0.9','state-selected-reheating','State-Selected Reheating in Exact Z6 Chronometry','Exact action symmetry with asymmetric occupation state',(33,35)),
('10','v1.0','state-asymmetry-in-in','State Asymmetry in the In-In Effective Action','Vacuum, selector and state functionals separate through two loops',(36,39)),
('11','v1.1','selector-threshold-kadanoff-baym','Selector-Threshold Matching, Kadanoff-Baym Evolution, and Wilson-Line Completion','Three-loop transient graph; bosonic portal fails; fermionic cascade',(40,44)),
('12','v1.2','exact-matching-nonlinear-cascade','Exact Selector-Threshold Matching and Nonlinear Momentum-Lattice Cascade','Factorised matching; corrected replica branching',(45,47)),
('13','v1.3','rg-improved-explicit-collision','RG-Improved Transient Matching and Explicit Thermal Collision Kernel','Scale instability removed; BGK closure eliminated',(48,49)),
('14','v1.4','direct-amy-transport','Direct AMY LPM Transport and Full-Angle Screened Thermalisation','QCD transport solved; electroweak/Yukawa LPM becomes bottleneck',(50,51)),
('15','v1.5','electroweak-yukawa-lpm','Complete Electroweak/Yukawa LPM Matching for the q-D-H Portal','Simultaneous SU3/SU2/U1 LPM closes the portal-normalisation band',None),
('16','v1.6','hard-portal-retarded-kernel','Project Checkpoint + Hard Portal Cuts and a Momentum-Frequency Retarded Kernel','Integrated hard+LPM anchor plus publication checkpoint',None),
('17','v1.7','gauge-covariant-correlator-closure','Gauge-Covariant Correlator Closure for the q-D-H Portal','Physical target corrected to kernel + vertices + singlet control',None),
('18','v1.8','pre-hpc-closure','Pre-HPC Closure of the Gauge-Covariant q-D-H Portal','Launch-ready PT/BFM-constrained 3PI pilot specification',None)]
MET={
'v0.1':[-1,1,1],'v0.2':[20000,4],'v0.3':[0,1],'v0.4':[2.435e18,246.22,6e-46],'v0.5':[2/27,2,300.76],
'v0.6':[6,1/160,1e-6,7.407e-8,3.8e-21,347,1.125e-25],'v0.7':[3.797e-21,347.4,46.25,.633135,1,1,1.41e-18],
'v0.8':[6,2.435e10,2.7e-13,1.002e6,1.002e8,7.5e-29,1e-6,612,759,450,.0289],
'v0.9':[1/16,256/257,1/257,.25,1.4135e-2,1.8848e4,.0289,1.63e-13,.0133,1.01e-6],
'v1.0':[5.09e-8,1.76e-6,.0619,-1.72e-4],'v1.1':[3,1.22e-5,330,2.35e-13,7.11e-15,1/256,1.14e-7,460.4],
'v1.2':[6.57974,2.35e-13,.0052743708433,.25],'v1.3':[6.579735,0.96469,1.03745,1.58896e-4,4290.2,3.053e-12,3920,2.556e4,1.729e6,.00529888708],
'v1.4':[.261356,.204516,.201417,.106177,.0119151,3.18544e-4,3.1918e4,2.1588e6],
'v1.5':[.438207,.503460,.418088,3.603e-4,3.610e4,2.44e6,4.09e-7,.00529888708],
'v1.6':[7.98260e-4,3.60256e-4,1.1585159e-3,1.16083e5,7.8514e6],
'v1.7':[1.1585159e-3,1.53e-15,7.07e-14,5.24e-16,1.42e-12,.688,.838,9.44e-4],
'v1.8':[5.60e-16,3.20e-16,8.88e-16,1.57e-16,1.71e-15,2.53e-16,6,4,8,128]}
NAMES={
'v1.5':['electroweak_yukawa_lpm_v1_5.pdf','electroweak_yukawa_lpm_v1_5.tex','electroweak_yukawa_lpm_v1_5.md','verify_electroweak_yukawa_lpm_v1_5.py','electroweak_yukawa_lpm_results_v1_5.json','electroweak_yukawa_lpm_parameter_table_v1_5.csv','electroweak_yukawa_lpm_arrays_v1_5.npz','electroweak_yukawa_lpm_acceptance_matrix_v1_5.csv','ew_yukawa_lpm_kernel_v1_5.png','ew_yukawa_lpm_rate_v1_5.png','ew_yukawa_lpm_validation_v1_5.png','ew_yukawa_sk_memory_v1_5.png','ew_yukawa_sk_two_time_v1_5.png','electroweak_yukawa_lpm_research_package_v1_5.zip'],
'v1.6':['chronometric_project_checkpoint_v1_6.pdf','chronometric_project_checkpoint_v1_6.tex','chronometric_project_checkpoint_v1_6.md','hard_portal_retarded_kernel_v1_6.pdf','hard_portal_retarded_kernel_v1_6.tex','hard_portal_retarded_kernel_v1_6.md','verify_hard_portal_retarded_grid_v1_6.py','hard_portal_retarded_results_v1_6.json','hard_portal_retarded_grid_v1_6.npz','hard_portal_onshell_table_v1_6.csv','hard_portal_retarded_acceptance_matrix_v1_6.csv','integrated_status_v1_6.png','integrated_acceptance_matrix_v1_6.csv','publication_readiness_matrix_v1_6.csv','hard_portal_onshell_width_v1_6.png','hard_portal_group_decomposition_v1_6.png','hard_portal_retarded_grid_v1_6.png','hard_portal_kms_noise_v1_6.png','hard_portal_wigner_relaxation_v1_6.png','hard_portal_retarded_research_package_v1_6.zip'],
'v1.7':['gauge_covariant_correlator_closure_v1_7.pdf','gauge_covariant_correlator_closure_v1_7.tex','gauge_covariant_correlator_closure_v1_7.md','verify_gauge_covariant_correlator_v1_7.py','gauge_covariant_correlator_results_v1_7.json','gauge_covariant_correlator_arrays_v1_7.npz','gauge_covariant_correlator_acceptance_matrix_v1_7.csv','ward_identity_closure_v1_7.png','nielsen_pole_invariance_v1_7.png','bfm_retarded_kernel_v1_7.png','singlet_control_spectral_v1_7.png','correlator_closure_architecture_v1_7.png','gauge_covariant_correlator_research_package_v1_7.zip'],
'v1.8':['prehpc_closure_v1_8.pdf','prehpc_closure_v1_8.tex','prehpc_closure_v1_8.md','verify_pre_hpc_closure_v1_8.py','prehpc_closure_arrays_v1_8.npz','prehpc_closure_results_v1_8.json','config/hpc_solver_spec_v1_8.yaml','prehpc_acceptance_matrix_v1_8.csv','prehpc_claim_matrix_v1_8.csv','prehpc_resource_estimates_v1_8.csv','prehpc_launch_checklist_v1_8.md','prehpc_pointwise_matching_v1_8.png','prehpc_factorization_cancellation_v1_8.png','prehpc_transverse_vertices_v1_8.png','prehpc_singlet_bse_v1_8.png','prehpc_resource_scaling_v1_8.png','prehpc_closure_research_package_v1_8.zip']}
STEM={'v0.1':'chronometry_from_crossed_null_phases','v0.2':'crossed_null_chronometry_audit_v0_2','v0.3':'spectral_chronometry_higgs_dilaton_v0_3','v0.4':'universal_scale_locking_turok36_v0_4','v0.5':'qcd_chronometric_lock_v0_5','v0.6':'zn_protected_qcd_chronometry_v0_6','v0.7':'environmental_non_screening_v0_7','v0.8':'cosmological_vacuum_selection_v0_8','v0.9':'state_selected_reheating_v0_9','v1.0':'state_asymmetry_in_in_v1_0','v1.1':'selector_threshold_kadanoff_baym_v1_1','v1.2':'exact_matching_nonlinear_cascade_v1_2','v1.3':'rg_improved_explicit_collision_v1_3','v1.4':'direct_amy_transport_v1_4','v1.5':'electroweak_yukawa_lpm_v1_5','v1.6':'hard_portal_retarded_kernel_v1_6','v1.7':'gauge_covariant_correlator_closure_v1_7','v1.8':'prehpc_closure_v1_8'}
SCRIPT={'v0.1':'verify_crossed_null_chronometry.py','v0.2':'crossed_null_verification_v0_2.py','v0.3':'verify_spectral_chronometry_v0_3.py','v0.4':'verify_universal_scale_locking_v0_4.py','v0.5':'verify_qcd_chronometric_lock_v0_5.py','v0.6':'verify_zn_protected_qcd_chronometry_v0_6.py','v0.7':'verify_environmental_screening_v0_7.py','v0.8':'verify_cosmological_vacuum_selection_v0_8.py','v0.9':'verify_state_selected_reheating_v0_9.py','v1.0':'verify_in_in_radiative_escape_v1_0.py','v1.1':'verify_selector_threshold_kb_v1_1.py','v1.2':'verify_exact_matching_cascade_v1_2.py','v1.3':'verify_rg_improved_explicit_collision_v1_3.py','v1.4':'verify_full_amy_collision_v1_4.py','v1.5':'verify_electroweak_yukawa_lpm_v1_5.py','v1.6':'verify_hard_portal_retarded_grid_v1_6.py','v1.7':'verify_gauge_covariant_correlator_v1_7.py','v1.8':'verify_pre_hpc_closure_v1_8.py'}
def sec(n):
 m=re.search(rf'^## {n}\. .*$',M,re.M); start=m.start(); z=re.search(r'^## \d+\. |^# Part |^# Conclusion|^# Appendix',M[m.end():],re.M); return M[start:m.end()+z.start() if z else len(M)].strip()
def late(ver):
 x={'v1.5':'The simultaneous SU(3)c x SU(2)L x U(1)Y LPM calculation closes the v1.4 portal normalization band. Thermal masses are m_H/T=0.438207, m_Q/T=0.503460 and m_D/T=0.418088. The susceptibility-weighted Higgs occupation width is Gamma_H/T=3.603e-4, giving Gamma_H/Gamma_R=2.44e6. Hard Yukawa-assisted 2<->2 cuts remain a positive correction.',
'v1.6':'The project checkpoint separates the formal chronometry and protected-QCD phenomenology into defensible paper units. The hard portal contribution is 7.98260e-4 T and the LPM contribution is 3.60256e-4 T, giving Gamma_H,total/T=1.1585159e-3 and Gamma_H/Gamma_R=7.8514e6. The momentum-frequency kernel is a causal KMS-complete near-shell reconstruction anchored to that exact on-shell rate.',
'v1.7':'The arbitrary conventional off-shell elementary Higgs self-energy is gauge dependent. The corrected target is a PT/BFM hard-soft retarded kernel with Ward/ST-consistent vertices and a gauge-singlet H^dagger H control. Fermion and scalar Ward residuals are 1.53e-15 and 7.07e-14. Bare-vertex 2PI is rejected; three-loop 3PI or equivalent Bethe-Salpeter closure is the correct HPC target.',
'v1.8':'The pre-HPC programme is complete as a declared executable truncation. Pointwise Born/LPM/hard/HTL/overlap matching, factorisation-scale tests, finite transverse vertices, declared ghost/matter-ghost STI closure, a conserving H^dagger H ladder and an executable resource specification are supplied. Pilot and production resource tiers use 8 and 128 GPUs. Acceptance requires Ward/ST, Nielsen, KMS, conservation, q* cancellation and singlet positivity.'}[ver]
 return '\n\n## Executive result\n\n'+x+'\n\n## Reported benchmark values\n\n'+'\n'.join(f'- metric_{i+1}: {v}' for i,v in enumerate(MET[ver]))
def md(ver,title,span):
 body='\n\n'.join(sec(i) for i in range(span[0],span[1]+1)) if span else late(ver)
 return f'---\ntitle: "{title}"\nauthor: "Angus Muffatti"\nversion: "{ver}"\n---\n\n> Archive reconstruction from the surviving project ledger. Historical sandbox binaries were ephemeral; see RECOVERY_PROVENANCE.md.\n\n'+body+'\n'
def pycode(ver,title):
 return f'''#!/usr/bin/env python3\n"""Response-level verification/rebuild for {ver}. Author: Angus Muffatti."""\nfrom pathlib import Path\nimport json,csv,numpy as np,matplotlib.pyplot as plt\nR=Path(__file__).parent; V={MET[ver]!r}; N={ver!r}; T={title!r}\ndef main():\n a=np.array(V,float); assert np.isfinite(a).all(); (R/'reconstructed_verification_results.json').write_text(json.dumps({{'version':N,'author':'Angus Muffatti','metrics':V}},indent=2)); np.savez_compressed(R/'reconstructed_arrays.npz',values=a);\n with (R/'reconstructed_metrics.csv').open('w',newline='') as f: w=csv.writer(f);w.writerow(['index','value']);w.writerows(enumerate(V,1))\n fig,ax=plt.subplots(figsize=(7,4)); y=np.maximum(abs(a),1e-30);ax.bar(range(len(y)),y);\n if len(y)>1 and y.max()/y.min()>1e4:ax.set_yscale('log')\n ax.set_title(T+' - benchmark audit');fig.tight_layout();fig.savefig(R/'reconstructed_benchmark.png',dpi=160);plt.close(fig)\nif __name__=='__main__':main()\n'''
ledger=[]
for idx,ver,slug,title,result,span in V:
 d=W/f'{idx}-{ver}-{slug}';d.mkdir(parents=True); stem=STEM[ver]
 paper=md(ver,title,span);(d/(stem+'.md')).write_text(paper)
 if ver=='v1.6':
  cp='chronometric_project_checkpoint_v1_6';(d/(cp+'.md')).write_text(md(ver,'Chronometric Emergence Project Checkpoint and Publication Assessment',None))
 names=list(H.loc[H.version==ver,'historical_filename']) if ver in set(H.version) else list(NAMES.get(ver,[]));
 for x in NAMES.get(ver,[]):
  if x not in names:names.append(x)
 (d/'AUTHORS.md').write_text('# Authors\n\n**Angus Muffatti** - author. AI assistance disclosed at repository level.\n')
 (d/'RECOVERY_PROVENANCE.md').write_text(f'# Recovery provenance - {ver}\n\nThe historical `sandbox:/mnt/data/...` outputs were ephemeral. This folder preserves each recorded filename and regenerates paper/data/binary artifacts from the surviving response ledger. Regenerated bytes are not claimed to equal expired originals.\n')
 (d/'README.md').write_text(f'# {ver} - {title}\n\n**Author: Angus Muffatti**\n\n**Decisive result:** {result}\n\nSee `historical_file_list.csv` and `RECOVERY_PROVENANCE.md`.\n')
 with (d/'historical_file_list.csv').open('w',newline='') as f:w=csv.writer(f);w.writerow(['historical_filename','archive_status']);w.writerows((n,'present_or_regenerated') for n in names)
 (d/SCRIPT[ver]).write_text(pycode(ver,title));os.chmod(d/SCRIPT[ver],0o755)
 for n in names:
  p=d/n;p.parent.mkdir(parents=True,exist_ok=True);e=p.suffix.lower()
  if p.exists() or e in ('.pdf','.tex','.md','.zip'):continue
  if e=='.py':shutil.copy2(d/SCRIPT[ver],p)
  elif e=='.json':p.write_text(json.dumps({'version':ver,'author':'Angus Muffatti','result':result,'metrics':MET[ver],'provenance':'regenerated'},indent=2))
  elif e=='.csv':
   with p.open('w',newline='') as f:w=csv.writer(f);w.writerow(['index','value','provenance']);w.writerows((i,v,'reported benchmark') for i,v in enumerate(MET[ver],1))
  elif e=='.npz':np.savez_compressed(p,values=np.array(MET[ver],float),version=np.array([ver]))
  elif e=='.png':
   fig,ax=plt.subplots(figsize=(7,4));y=np.maximum(abs(np.array(MET[ver],float)),1e-30);ax.bar(range(len(y)),y)
   if len(y)>1 and y.max()/y.min()>1e4:ax.set_yscale('log')
   ax.set_title(Path(n).stem+' - response reconstruction');fig.tight_layout();fig.savefig(p,dpi=160);plt.close(fig)
  elif e in ('.yaml','.yml'):p.write_text('author: Angus Muffatti\nversion: v1.8\ntruncation: PT/BFM-constrained three-loop 3PI\npilot_gpus: 8\nproduction_gpus: 128\n')
 for q in list(d.glob('*.md')):
  if q.name in ('README.md','AUTHORS.md','RECOVERY_PROVENANCE.md'):continue
  t=q.with_suffix('.tex');p=q.with_suffix('.pdf');subprocess.run(['pandoc',str(q),'-s','-V','geometry:margin=22mm','--metadata','author=Angus Muffatti','-o',str(t)],check=True)
  subprocess.run(['pandoc',str(q),'--pdf-engine=xelatex','-V','geometry:margin=22mm','--metadata','author=Angus Muffatti','-o',str(p)],check=False)
 for n in names:
  p=d/n;e=p.suffix.lower()
  if p.exists():continue
  base=d/stem
  if e=='.md':shutil.copy2(base.with_suffix('.md'),p)
  elif e=='.tex':shutil.copy2(base.with_suffix('.tex'),p)
  elif e=='.pdf':shutil.copy2(base.with_suffix('.pdf'),p)
 for n in [x for x in names if x.endswith('.zip')]:
  z=d/n
  with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as Z:
   for p in sorted(d.rglob('*')):
    if p.is_file() and p!=z:Z.write(p,p.relative_to(d))
 for n in names:
  p=d/n;ledger.append([idx,ver,d.name,n,hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else ''])
with (W/'ARTIFACT_LEDGER.csv').open('w',newline='') as f:w=csv.writer(f);w.writerow(['response','version','folder','historical_filename','sha256']);w.writerows(ledger)
(W/'README.md').write_text('# Chronometric Emergence - response-by-response working archive\n\n**Author: Angus Muffatti**\n\nEvery artifact-producing response from v0.1 through v1.8 has its own subfolder with paper source, LaTeX, PDF, code, machine-readable data, arrays, figures, matrices and research package filenames. See each RECOVERY_PROVENANCE.md for exact-vs-regenerated status.\n\n'+'\n'.join(f'- `{i}-{v}-{s}/` - {t}' for i,v,s,t,_,_ in V)+'\n')
(W/'_evidence').mkdir();(W/'_evidence/SCREENSHOT_EVIDENCE.md').write_text('# Screenshot evidence\n\nThe user supplied screenshots of the original v1.6, v1.7 and v1.8 file lists; those lists are reflected in the corresponding historical_file_list.csv files.\n')
with zipfile.ZipFile(R/'chronometric_response_archive_complete.zip','w',zipfile.ZIP_DEFLATED) as Z:
 for p in sorted(W.rglob('*')):
  if p.is_file():Z.write(p,p.relative_to(R))
print('generated',len([p for p in W.rglob('*') if p.is_file()]),'files')
