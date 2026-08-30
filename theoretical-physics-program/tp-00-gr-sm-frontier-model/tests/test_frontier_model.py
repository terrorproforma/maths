import csv, json, subprocess, sys, unittest
from pathlib import Path
import yaml
ROOT=Path(__file__).resolve().parents[1]
class TestFrontierModel(unittest.TestCase):
    def test_verifier(self):
        p=subprocess.run([sys.executable,str(ROOT/'code'/'verify_frontier_model.py'),'--root',str(ROOT)],capture_output=True,text=True)
        self.assertEqual(p.returncode,0,p.stdout+p.stderr)
    def test_yaml_no_total_score(self):
        cfg=yaml.safe_load((ROOT/'successor_acceptance_tests.yaml').read_text())
        self.assertIn('NO SINGLE TOTAL SCORE',cfg['aggregation_rule'])
    def test_every_seam_has_equation_and_resolution(self):
        with (ROOT/'seam_ledger.csv').open(encoding='utf-8', newline='') as fh:
            rows=list(csv.DictReader(fh))
        self.assertGreaterEqual(len(rows),18)
        for r in rows:
            self.assertTrue(r['structural_equation'].strip())
            self.assertTrue(r['resolution_evidence'].strip())
            self.assertTrue(r['sources'].strip())
    def test_generated_tables_and_arrays(self):
        self.assertTrue((ROOT/'tables'/'seam_equation_index.tex').exists())
        self.assertTrue((ROOT/'results'/'benchmark_arrays.npz').exists())
    def test_numerical_diagnostics(self):
        subprocess.run([sys.executable,str(ROOT/'code'/'verify_frontier_model.py'),'--root',str(ROOT)],check=True,capture_output=True)
        obj=json.loads((ROOT/'results'/'numerical_diagnostics.json').read_text())
        self.assertGreater(obj['representative_scale_span_decades_H0_to_MbarP'],60.0)
        self.assertIn('warning',obj)
    def test_results_json(self):
        subprocess.run([sys.executable,str(ROOT/'code'/'verify_frontier_model.py'),'--root',str(ROOT)],check=True,capture_output=True)
        obj=json.loads((ROOT/'results'/'verification_results.json').read_text())
        self.assertTrue(obj['all_pass'])
if __name__=='__main__': unittest.main()
