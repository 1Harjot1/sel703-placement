"""
tool/criteria/loader.py
=======================
Loads and indexes the 3-tier taxonomy mapping definitions dynamically.
Guarantees EVERY quote text is resolved at runtime from quote_corpus_verified.json by ID.
NO QUOTE STRINGS ARE HARDCODED.
"""

import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MAPPING_PATH = os.path.normpath(os.path.join(BASE_DIR, "..", "..", "taxonomy", "mapping.json"))
CORPUS_PATH = os.path.normpath(os.path.join(BASE_DIR, "..", "..", "..", "VC", "pipeline", "quote_corpus_verified.json"))


class CriteriaLoader:
    def __init__(self, mapping_path=MAPPING_PATH, corpus_path=CORPUS_PATH):
        self.mapping_path = mapping_path
        self.corpus_path = corpus_path
        self.criteria = []
        self.corpus = {}
        self.load_corpus()
        self.load_criteria()

    def load_corpus(self):
        if not os.path.exists(self.corpus_path):
            raise FileNotFoundError(f"Corpus file not found at {self.corpus_path}")
        with open(self.corpus_path, "r", encoding="utf-8") as f:
            self.corpus = json.load(f)

    def load_criteria(self):
        if not os.path.exists(self.mapping_path):
            raise FileNotFoundError(f"Mapping file not found at {self.mapping_path}")
        with open(self.mapping_path, "r", encoding="utf-8") as f:
            raw_criteria = json.load(f)

        # Dynamically resolve quote text from corpus by concept_quote_id
        resolved = []
        for c in raw_criteria:
            quote_id = c.get("concept_quote_id", "")
            if ":" not in quote_id:
                raise ValueError(f"Invalid concept_quote_id format: {quote_id}")
            
            doi, sid = quote_id.split(":")
            if doi not in self.corpus:
                raise KeyError(f"DOI {doi} from quote_id {quote_id} not found in quote corpus")
            if sid not in self.corpus[doi]["sentences"]:
                raise KeyError(f"Sentence ID {sid} for DOI {doi} not found in quote corpus")
                
            entry = dict(c)
            # Overwrite concept_quote dynamically from corpus
            entry["concept_quote"] = self.corpus[doi]["sentences"][sid]
            entry["source_printed_title"] = self.corpus[doi].get("printed_title", "")
            entry["source_printed_authors"] = self.corpus[doi].get("printed_authors", "")
            entry["source_pdf_filename"] = self.corpus[doi].get("pdf_filename", "")
            resolved.append(entry)

        self.criteria = resolved

    def get_by_concept(self, concept_name):
        matches = [c for c in self.criteria if c.get("cognitive_concept", "").lower() == concept_name.lower()]
        if not matches:
            raise KeyError(f"No mapping entry found for cognitive concept: {concept_name}")
        return matches[0]

    def get_by_rule_id(self, rule_id):
        return [c for c in self.criteria if c.get("rule_id", "").lower() == rule_id.lower()]

    def get_rule_metadata(self, rule_id):
        rule_map = {
            "coga-4.2.4-wm": "Working Memory Overload",
            "coga-4.2.1-ambig": "Ambiguity Intolerance",
            "wcag-3.3.4-inhib": "Inhibition Deficit",
            "wcag-2.2.6-time": "Time Blindness",
            "eu-ai-act-art13": "Ambiguity Intolerance",
            "eu-ai-act-art14": "Planning Deficit",
            "coga-4.5.3-scope": "Planning Deficit"
        }
        concept = rule_map.get(rule_id.lower())
        if concept:
            try:
                return self.get_by_concept(concept)
            except KeyError:
                pass
        # Fallback to first criterion if not found
        return self.criteria[0] if self.criteria else {}

    def all_criteria(self):
        return self.criteria

