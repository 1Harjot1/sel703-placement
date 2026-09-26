import unittest
from pathlib import Path
import sys

base_dir = Path(__file__).parent.parent
sys.path.insert(0, str(base_dir))

from src.corpus_loader import load_taxonomies, load_quote_corpus, get_candidate_sentences

class TestCorpusLoader(unittest.TestCase):
    def setUp(self):
        self.data_dir = base_dir / "src" / "data"

    def test_load_taxonomies(self):
        tax = load_taxonomies(self.data_dir)
        self.assertIn("dysfunctions", tax)
        self.assertIn("behaviors", tax)
        self.assertIn("values", tax)
        self.assertIn("sdlc", tax)
        self.assertEqual(len(tax["dysfunctions"]), 8)
        self.assertEqual(len(tax["behaviors"]), 10)

    def test_provenance_gate(self):
        corpus = load_quote_corpus(self.data_dir)
        self.assertGreater(len(corpus), 30)
        for doi, entry in corpus.items():
            self.assertTrue("sentences" in entry or "provenance" in entry)
            if "provenance" in entry and entry["provenance"]:
                self.assertIn("source_api", entry["provenance"])

    def test_get_candidate_sentences(self):
        corpus = load_quote_corpus(self.data_dir)
        doi = "10.1017/s0140525x01003922" # Cowan 2001
        candidates = get_candidate_sentences(doi, corpus, limit=5)
        self.assertGreater(len(candidates), 0)
        self.assertLessEqual(len(candidates), 5)
        for sid, txt in candidates.items():
            self.assertTrue(sid.startswith("s"))
            self.assertGreater(len(txt), 10)

if __name__ == "__main__":
    unittest.main()
