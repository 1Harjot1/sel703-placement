import unittest
from pathlib import Path
import sys

base_dir = Path(__file__).parent.parent
sys.path.insert(0, str(base_dir))

from src.corpus_loader import load_taxonomies, load_quote_corpus, get_candidate_sentences
from src.generator import build_prompt_payload, generate_scenario_offline

class TestGenerator(unittest.TestCase):
    def setUp(self):
        self.data_dir = base_dir / "src" / "data"
        self.tax = load_taxonomies(self.data_dir)
        self.corpus = load_quote_corpus(self.data_dir)

    def test_build_prompt_payload(self):
        combo = {
            "dysfunction": self.tax["dysfunctions"][0],
            "behavior": self.tax["behaviors"][0],
            "sdlc": self.tax["sdlc"].get("tasks", self.tax["sdlc"])[0] if isinstance(self.tax["sdlc"], dict) else self.tax["sdlc"][0],
            "value": self.tax["values"][0]
        }
        doi = "10.1017/s0140525x01003922"
        candidates = get_candidate_sentences(doi, self.corpus, limit=3)
        payload = build_prompt_payload(combo, self.corpus, candidates, doi)
        self.assertIn("system", payload)
        self.assertIn("user", payload)
        self.assertIn(combo["dysfunction"]["name"], payload["user"])
        self.assertIn(combo["behavior"]["name"], payload["user"])
        self.assertIn(doi, payload["user"])

    def test_offline_generation(self):
        combo = {
            "dysfunction": self.tax["dysfunctions"][0],
            "behavior": self.tax["behaviors"][0],
            "sdlc": self.tax["sdlc"].get("tasks", self.tax["sdlc"])[0] if isinstance(self.tax["sdlc"], dict) else self.tax["sdlc"][0],
            "value": self.tax["values"][0]
        }
        scen = generate_scenario_offline(combo, self.data_dir)
        self.assertIn("summary", scen)
        self.assertIn("full_scenario", scen)
        self.assertIn("citation_doi", scen)
        self.assertIn("quote_id", scen)
        self.assertIn("relevance", scen)

if __name__ == "__main__":
    unittest.main()
