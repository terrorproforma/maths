#!/usr/bin/env python3
from __future__ import annotations
import argparse, csv, json, math
from fractions import Fraction
from pathlib import Path
import yaml


def anomaly_coefficients():
    # One generation, all fermions represented as left-handed Weyl fields.
    Y = {
        'Q': Fraction(1,6), 'uc': Fraction(-2,3), 'dc': Fraction(1,3),
        'L': Fraction(-1,2), 'ec': Fraction(1,1)
    }
    out = {}
    out['SU3^2-U1'] = 2*Fraction(1,2)*Y['Q'] + Fraction(1,2)*Y['uc'] + Fraction(1,2)*Y['dc']
    out['SU2^2-U1'] = 3*Fraction(1,2)*Y['Q'] + Fraction(1,2)*Y['L']
    out['U1^3'] = 6*Y['Q']**3 + 3*Y['uc']**3 + 3*Y['dc']**3 + 2*Y['L']**3 + Y['ec']**3
    out['grav^2-U1'] = 6*Y['Q'] + 3*Y['uc'] + 3*Y['dc'] + 2*Y['L'] + Y['ec']
    out['SU3^3_relative'] = Fraction(2-1-1,1)
    out['Witten_SU2_doublets_mod2'] = Fraction((3+1) % 2,1)
    return out


def read_csv(path):
    with path.open(newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))


def run(root: Path):
    checks = []
    coeffs = anomaly_coefficients()
    checks.append({'id':'anomalies_exact','pass':all(v == 0 for v in coeffs.values()),'details':{k:str(v) for k,v in coeffs.items()}})

    constants = json.loads((root/'results'/'baseline_constants.json').read_text(encoding='utf-8'))
    inputs = constants['representative_inputs']
    h0_planck = inputs['Planck_H0_km_s_Mpc']
    h0_shoes = inputs['SH0ES_H0_km_s_Mpc']
    w_atlas = inputs['m_W_MeV_ATLAS']
    w_cdf = inputs['m_W_MeV_CDFII']
    eta = inputs['eta_Ti_Pt_MICROSCOPE']
    h0_naive_pull = (h0_shoes['value']-h0_planck['value'])/math.hypot(h0_shoes['uncertainty'],h0_planck['uncertainty'])
    w_naive_pull = (w_cdf['value']-w_atlas['value'])/math.hypot(w_cdf['uncertainty'],w_atlas['uncertainty'])
    eta_sigma = math.hypot(eta['stat'],eta['syst'])
    scale_span = math.log10(inputs['Mbar_P_GeV']/inputs['Hubble_energy_GeV_representative']['value'])
    diagnostics = {
        'schema_version':'1.0.0',
        'warning':'Naive independent-Gaussian pulls are regression diagnostics only; they are not substitute likelihood analyses or universal successor gates.',
        'naive_independent_gaussian_pulls':{
            'SH0ES_minus_Planck_base_LCDM':h0_naive_pull,
            'CDFII_minus_ATLAS_W_mass':w_naive_pull,
        },
        'MICROSCOPE_combined_uncertainty':eta_sigma,
        'MICROSCOPE_central_over_combined_sigma':eta['central']/eta_sigma,
        'representative_scale_span_decades_H0_to_MbarP':scale_span,
        'electroweak_to_reduced_Planck_ratio':inputs['v_GeV']/inputs['Mbar_P_GeV'],
    }
    (root/'results'/'numerical_diagnostics.json').write_text(json.dumps(diagnostics,indent=2)+'\n',encoding='utf-8')
    finite = all(math.isfinite(v) for v in [h0_naive_pull,w_naive_pull,eta_sigma,scale_span])
    checks.append({'id':'numerical_diagnostics_reproducible','pass':finite and scale_span>60,'details':diagnostics})

    seams = read_csv(root/'seam_ledger.csv')
    required_seams = ['quantum gravity','vacuum energy','singular','dark matter','dark energy','neutrino','baryogenesis','inflation','hierarchy','strong cp','flavour','three generations']
    blob = ' '.join(r['seam'].lower() for r in seams)
    checks.append({'id':'required_seams_present','pass':all(x in blob for x in required_seams),'details':{'count':len(seams)}})
    complete = all(r['structural_equation'].strip() and r['established_status'].strip() and r['resolution_evidence'].strip() and r['sources'].strip() for r in seams)
    checks.append({'id':'seam_rows_traceable','pass':complete,'details':{'rows':len(seams)}})
    category_cols = ['mathematical_inconsistency','ultraviolet_incompleteness','empirical_anomaly','unexplained_parameter','naturalness_fine_tuning','missing_initial_boundary_condition','inaccessible_regime']
    binary = all(r[c] in {'0','1'} for r in seams for c in category_cols)
    checks.append({'id':'seam_taxonomy_binary','pass':binary,'details':{'axes':category_cols}})

    with (root/'successor_acceptance_tests.yaml').open(encoding='utf-8') as f:
        cfg = yaml.safe_load(f)
    gates = cfg['gates']
    ids = [g['id'] for g in gates]
    checks.append({'id':'gate_ids_unique','pass':len(ids)==len(set(ids)),'details':{'count':len(ids)}})
    tiers = set(g['tier'] for g in gates)
    expected_tiers = {'algebraic','perturbative','recovery','nonperturbative','laboratory','astrophysical','cosmological','reproducibility'}
    checks.append({'id':'test_hierarchy_complete','pass':expected_tiers.issubset(tiers),'details':{'tiers':sorted(tiers)}})
    no_total = 'NO SINGLE TOTAL SCORE' in cfg.get('aggregation_rule','')
    checks.append({'id':'no_invalid_aggregate_score','pass':no_total,'details':{'rule':cfg.get('aggregation_rule')}})
    fatal_count = sum(bool(g['fatal_if_applicable']) for g in gates)
    checks.append({'id':'fatal_gates_declared','pass':fatal_count>0,'details':{'fatal_count':fatal_count}})

    sources = read_csv(root/'source_ledger.csv')
    source_ids = {s['source_id'] for s in sources}
    cited = set()
    for table in [seams, read_csv(root/'verified_domains.csv'), read_csv(root/'recovery_requirements.csv'), read_csv(root/'anomaly_watchlist.csv')]:
        for r in table:
            for s in r.get('sources','').split(';'):
                if s: cited.add(s)
    missing = sorted(cited-source_ids)
    checks.append({'id':'source_keys_resolve','pass':not missing,'details':{'missing':missing,'source_count':len(source_ids)}})

    deps = read_csv(root/'dependency_map.csv')
    project_ids = {d['project_id'] for d in deps}
    expected_projects = {f'TP-{i:02d}' for i in range(1,17)}
    checks.append({'id':'dependency_map_TP01_TP16','pass':project_ids==expected_projects,'details':{'projects':sorted(project_ids)}})

    required_files = [
        'README.md','frontier_model_action.tex','seam_ledger.csv','successor_acceptance_tests.yaml','known_limits.md',
        'minimum_viable_successor_checklist.md','minimum_viable_successor_checklist.pdf','dependency_map.md',
        'source_and_notation_ledger.md','claim_novelty_acceptance_matrix.csv','references.bib',
        'paper/frontier_model_constraint_ledger.tex','paper/frontier_model_constraint_ledger.pdf',
        'code/generate_latex_tables.py','code/generate_figures.py','code/verify_frontier_model.py',
        'results/numerical_diagnostics.json','results/benchmark_arrays.npz',
        'tables/verified_domains_table.tex','tables/seam_summary_table.tex','tables/successor_gates_table.tex',
        'figures/seam_taxonomy_matrix.pdf','figures/verified_scale_map.pdf'
    ]
    missing_files = [f for f in required_files if not (root/f).exists()]
    checks.append({'id':'required_deliverables_present','pass':not missing_files,'details':{'missing':missing_files}})

    result = {
        'schema_version':'1.0.0', 'all_pass':all(c['pass'] for c in checks), 'checks':checks,
        'summary': {'seam_count':len(seams),'gate_count':len(gates),'fatal_gate_count':fatal_count,'source_count':len(sources),'dependency_count':len(deps)}
    }
    out = root/'results'/'verification_results.json'
    out.write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(json.dumps(result, indent=2))
    return 0 if result['all_pass'] else 1

if __name__ == '__main__':
    p=argparse.ArgumentParser(); p.add_argument('--root',default='.')
    raise SystemExit(run(Path(p.parse_args().root).resolve()))
