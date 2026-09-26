import unittest
from pathlib import Path
import sys

base_dir = Path(__file__).parent.parent
sys.path.insert(0, str(base_dir))

from src.corpus_loader import load_quote_corpus
from src.verifier import (
    check_schema, check_banned_words, check_no_language_names,
    check_no_label_leakage, check_quote_verified, verify_scenario
)

class TestVerifier(unittest.TestCase):
    def setUp(self):
        self.data_dir = base_dir / "src" / "data"
        self.corpus = load_quote_corpus(self.data_dir)
        self.cache_file = self.data_dir / "doi_cache.json"

    def test_schema_completeness(self):
        valid = {f: "val" for f in ["summary", "full_scenario", "impact", "reasoning", "intervention", "value_violated", "behaviour", "citation_doi", "quote_id"]}
        self.assertTrue(check_schema(valid)["pass"])
        invalid = valid.copy()
        del invalid["quote_id"]
        self.assertFalse(check_schema(invalid)["pass"])

    def test_banned_words(self):
        clean = {"summary": "A developer had difficulties planning the module contracts."}
        self.assertTrue(check_banned_words(clean)["pass"])
        buzzword = {"summary": "This seamlessly leverages a transformative paradigm."}
        self.assertFalse(check_banned_words(buzzword)["pass"])

    def test_no_language_names(self):
        clean = {"summary": "The assistant changed the method signature."}
        self.assertTrue(check_no_language_names(clean)["pass"])
        with_python = {"summary": "The developer was writing a python script."}
        self.assertFalse(check_no_language_names(with_python)["pass"])

    def test_no_label_leakage_word_boundaries(self):
        # Crucial test: 'interface' must NOT trigger 'face'
        scenario_with_interface = {
            "summary": "The developer was reviewing interface promises and contracts.",
            "full_scenario": "I asked the assistant to specify the interface methods."
        }
        res = check_no_label_leakage(scenario_with_interface)
        self.assertTrue(res["pass"], f"False positive label leakage detected: {res.get('found')}")

        # Explicit leakage of value label 'face' or dysfunction name should fail
        scenario_with_leakage = {
            "summary": "The developer experienced working memory overload when reading the text.",
            "full_scenario": "This threatened the developer's face in front of colleagues."
        }
        res_leak = check_no_label_leakage(scenario_with_leakage)
        self.assertFalse(res_leak["pass"])

    def test_quote_verification_quote_id(self):
        doi = "10.1017/s0140525x01003922"
        scenario = {
            "citation_doi": doi,
            "quote_id": "s68",
            "citation_quote": ""
        }
        res = check_quote_verified(scenario, self.corpus)
        self.assertTrue(res["pass"])
        self.assertTrue("results in markedly less accurate" in res["resolved_quote"])

    def test_full_scenario_verification(self):
        sample = {
            "summary": "A developer sorting requirement statements asked for classification help.",
            "full_scenario": "I was converting requirements into interface specifications.",
            "impact": "The review packet is delayed.",
            "reasoning": "Working memory limits are exceeded.",
            "intervention": "Pin category rubrics.",
            "value_violated": "Self-direction-thought",
            "behaviour": "Non-deterministic Output",
            "citation_doi": "10.1017/s0140525x01003922",
            "quote_id": "s68"
        }
        res = verify_scenario(sample, self.corpus, self.cache_file)
        self.assertTrue(res["all_pass"])

if __name__ == "__main__":
    unittest.main()
