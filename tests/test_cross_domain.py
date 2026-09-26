import unittest
import json
from pathlib import Path
import sys

base_dir = Path(__file__).parent.parent
sys.path.insert(0, str(base_dir))

from src.corpus_loader import load_standards_corpus
from src.verifier import verify_standards_scenario

class TestCrossDomain(unittest.TestCase):
    def setUp(self):
        self.data_dir = base_dir / "src" / "data"
        self.demo_dir = base_dir / "examples" / "cross_domain_demo"
        self.corpus = load_standards_corpus(self.data_dir)
        scenarios_path = self.demo_dir / "cross_domain_scenarios.json"
        self.scenarios = json.loads(scenarios_path.read_text(encoding="utf-8"))

    def test_load_standards_corpus(self):
        self.assertGreaterEqual(len(self.corpus), 10)
        coga_found = any("COGA" in k for k in self.corpus.keys())
        wcag_found = any("WCAG" in k for k in self.corpus.keys())
        eu_found = any("EU-AI" in k for k in self.corpus.keys())
        self.assertTrue(coga_found, "W3C COGA standards missing from corpus")
        self.assertTrue(wcag_found, "W3C WCAG 2.2 standards missing from corpus")
        self.assertTrue(eu_found, "EU AI Act articles missing from corpus")

    def test_cross_domain_scenarios_count(self):
        self.assertEqual(len(self.scenarios), 14, "Expected exactly 14 cross-domain compliance scenarios")

    def test_verify_all_14_scenarios_pass(self):
        passed = 0
        for scen in self.scenarios:
            res = verify_standards_scenario(scen, self.corpus)
            self.assertTrue(res["all_pass"], f"Scenario {scen.get('id')} failed deterministic verification: {res}")
            passed += 1
        self.assertEqual(passed, 14, "All 14 cross-domain scenarios must pass Stage 4 checks")

    def test_banned_words_rejection(self):
        dirty_scenario = self.scenarios[0].copy()
        dirty_scenario["summary"] = "The developer was waiting for an additional senior engineer review."
        res = verify_standards_scenario(dirty_scenario, self.corpus)
        self.assertFalse(res["all_pass"], "Banned seniority word should fail deterministic check")
        self.assertIn("senior", res["banned_words"]["found"])

if __name__ == "__main__":
    unittest.main()
