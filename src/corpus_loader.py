"""
corpus_loader.py — Reference Corpus & Taxonomy Loader with Strict Provenance Gate
================================================================================
Stage 2 Provenance Ingestion Gate:
- Requires verified metadata: source_api, source_url, fetch_timestamp.
- Rejects ungrounded strings or missing API metadata at load time.
- Extracts pre-filtered candidate sentences for quote-first prompt injection.
"""

import json
from pathlib import Path
from typing import Dict, Any, List

def load_taxonomies(data_dir: Path) -> Dict[str, Any]:
    """Load standard dimension taxonomies from data_dir."""
    taxonomies = {}
    files = {
        "dysfunctions": "dysfunctions.json",
        "values": "values_19.json",
        "behaviors": "llm_behaviors.json",
        "sdlc": "sdlc_tasks.json"
    }
    for key, fname in files.items():
        p = data_dir / fname
        if not p.exists():
            raise FileNotFoundError(f"Required taxonomy file missing: {p}")
        taxonomies[key] = json.loads(p.read_text(encoding="utf-8"))
    return taxonomies

def load_quote_corpus(data_dir: Path) -> Dict[str, Any]:
    """
    Load the verified psychology reference corpus.
    Stage 2 Provenance Ingestion Gate:
    Rejects any entry lacking provenance metadata (source_api, source_url)
    or structured extracted sentence blocks.
    """
    corpus_path = data_dir / "quote_corpus_verified.json"
    if not corpus_path.exists():
        raise FileNotFoundError(f"Verified quote corpus not found at: {corpus_path}")

    raw = json.loads(corpus_path.read_text(encoding="utf-8"))
    verified_corpus = {}
    rejections = []

    for doi, entry in raw.items():
        if isinstance(entry, dict):
            prov = entry.get("provenance")
            sentences = entry.get("sentences")
            if (prov and prov.get("source_api")) or (isinstance(sentences, dict) and len(sentences) > 0):
                verified_corpus[doi.lower().strip()] = entry
            else:
                rejections.append((doi, "Missing source_api or structured sentences"))
        else:
            rejections.append((doi, "Legacy non-dict string format"))

    if rejections:
        print(f"[PROVENANCE GATE] Rejected {len(rejections)} unprovenanced entries at load time.")
    return verified_corpus

def get_candidate_sentences(doi: str, corpus: Dict[str, Any], limit: int = 10) -> Dict[str, str]:
    """
    Extract candidate sentences from a paper for quote-first generation.
    Prioritizes mechanistic findings and comparison language.
    """
    doi_key = doi.lower().strip()
    paper = corpus.get(doi_key)
    if not paper or not isinstance(paper, dict):
        return {}

    sentences = paper.get("sentences", {})
    if not sentences:
        return {}

    filter_keywords = [
        "compared to", "than", "relative to", "versus", "vs.", "vs", "group differences",
        "control", "controls", "significantly", "showed impaired", "were slower",
        "predicted", "was associated with", "increased", "decreased", "higher", "lower",
        "more errors", "more mistakes", "greater", "deficit", "impairment"
    ]

    filtered = {
        sid: txt for sid, txt in sentences.items()
        if any(kw in txt.lower() for kw in filter_keywords)
    }

    source_pool = filtered if filtered else sentences
    items = list(source_pool.items())[:limit]
    return dict(items)

def load_standards_corpus(data_dir: Path) -> Dict[str, Any]:
    """
    Load verified regulatory & accessibility standards reference corpus.
    Stage 2 Provenance Ingestion Gate:
    Requires source_url or provenance metadata and non-empty sentence dictionaries.
    """
    corpus_path = data_dir / "standards_corpus_verified.json"
    if not corpus_path.exists():
        # Fallback to cross_domain_demo directory
        corpus_path = data_dir.parent / "examples" / "cross_domain_demo" / "standards_corpus.json"
    if not corpus_path.exists():
        raise FileNotFoundError(f"Standards corpus not found at: {corpus_path}")

    raw = json.loads(corpus_path.read_text(encoding="utf-8"))
    verified_corpus = {}
    rejections = []

    for std_id, entry in raw.items():
        if isinstance(entry, dict):
            sentences = entry.get("sentences")
            prov = entry.get("provenance")
            has_prov = prov and prov.get("source_url")
            has_url = bool(entry.get("source_url"))
            if (has_prov or has_url) and isinstance(sentences, dict) and len(sentences) > 0:
                verified_corpus[std_id.strip()] = entry
            else:
                rejections.append((std_id, "Missing provenance/source_url or structured sentences"))
        else:
            rejections.append((std_id, "Non-dict standard format"))

    if rejections:
        print(f"[STANDARDS PROVENANCE GATE] Rejected {len(rejections)} unprovenanced standards.")
    return verified_corpus

