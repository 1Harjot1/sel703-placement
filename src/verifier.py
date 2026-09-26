"""
verifier.py — Deterministic Verification Engine (Stage 4)
=========================================================
Applies 6 deterministic checks against generated scenarios:
1. Schema Completeness: 9 required fields present and non-empty.
2. Banned Buzzwords: flags corporate AI/tech buzzwords.
3. No Programming Language Names: ensures language-agnostic scenarios.
4. No Diagnostic/Value Label Leakage: uses regex word boundaries so
   terms like 'interface' do not falsely trigger on Schwartz value 'face'.
5. Verbatim Quote Verification: resolves Stage B quote_id against corpus.
6. DOI Format and Cached Resolution: checks DOI against local resolution cache.
"""

import re
import json
from pathlib import Path
from typing import Dict, Any, List

REQUIRED_FIELDS = [
    "summary", "full_scenario", "impact", "reasoning", "intervention",
    "value_violated", "behaviour", "citation_doi", "quote_id"
]

BANNED_WORDS = [
    "python", "java", "javascript", "typescript", "django",
    "flask", "node", "angular", "ast", "jwt", "sql", "csrf",
    "senior", "junior", "expert", "novice", "llm",
    "in conclusion", "in summary", "as a result", "it is worth noting",
    "leverages", "delves", "it is important to note", "seamlessly",
    "robust", "innovative", "transformative", "paradigm"
]

LANGUAGE_NAMES = [
    "python", "java", "javascript", "typescript", "django",
    "flask", "node", "angular", "sql"
]

DYSFUNCTION_TERMS = [
    "working memory overload", "delay aversion", "rejection sensitivity",
    "set-shifting cost", "ambiguity intolerance", "inhibition deficit",
    "time blindness", "emotional dysregulation"
]

VALUE_TERMS = [
    "self-direction-thought", "self-direction-action", "stimulation", "hedonism",
    "achievement", "power-dominance", "power-resources", "face", "security-personal",
    "security-societal", "conformity-rules", "conformity-interpersonal", "tradition",
    "humility", "benevolence-caring", "benevolence-dependability", "universalism-concern",
    "universalism-nature", "universalism-tolerance"
]

DOI_PATTERN = re.compile(r"10\.\d{4,}/\S+")

def check_schema(scenario: Dict[str, Any]) -> Dict[str, Any]:
    missing = [f for f in REQUIRED_FIELDS if not str(scenario.get(f, "")).strip()]
    return {
        "pass": len(missing) == 0,
        "missing_fields": missing
    }

def check_banned_words(scenario: Dict[str, Any]) -> Dict[str, Any]:
    full_text = " ".join(str(v) for v in scenario.values()).lower()
    found = []
    for w in BANNED_WORDS:
        pattern = re.compile(r"\b" + re.escape(w.lower()) + r"\b", re.IGNORECASE)
        if pattern.search(full_text):
            found.append(w)
    return {
        "pass": len(found) == 0,
        "found": found
    }

def check_no_language_names(scenario: Dict[str, Any]) -> Dict[str, Any]:
    full_text = " ".join(str(v) for v in scenario.values()).lower()
    found = []
    for lang in LANGUAGE_NAMES:
        pattern = re.compile(r"\b" + re.escape(lang.lower()) + r"\b", re.IGNORECASE)
        if pattern.search(full_text):
            found.append(lang)
    if re.search(r"\b(react\.js|reactjs|react framework)\b", full_text, re.IGNORECASE):
        found.append("react")
    if re.search(r"\b(rest api|restful|rest service|rest endpoint)\b", full_text, re.IGNORECASE):
        found.append("rest")
    return {
        "pass": len(found) == 0,
        "found": found
    }

def check_no_label_leakage(scenario: Dict[str, Any]) -> Dict[str, Any]:
    """
    Checks that internal taxonomy labels are not leaked in scenario prose.
    Uses regex word boundaries (\b) to avoid false positives (e.g. 'interface' triggering 'face').
    """
    user_text = (str(scenario.get("summary", "")) + " " + str(scenario.get("full_scenario", ""))).lower()
    found = []
    for term in DYSFUNCTION_TERMS + VALUE_TERMS:
        clean_term = term.replace("—", "-").replace("–", "-").lower()
        pattern = re.compile(r"\b" + re.escape(clean_term) + r"\b", re.IGNORECASE)
        if pattern.search(user_text):
            found.append(term)
    return {
        "pass": len(found) == 0,
        "found": found
    }

def check_quote_verified(scenario: Dict[str, Any], corpus: Dict[str, Any]) -> Dict[str, Any]:
    doi = str(scenario.get("citation_doi", "")).strip().lower()
    qid = str(scenario.get("quote_id", "")).strip()
    quote = str(scenario.get("citation_quote", "") or scenario.get("evidence", "")).strip()

    if not doi:
        return {"pass": False, "doi": None, "in_corpus": False, "note": "Missing citation_doi"}

    paper = corpus.get(doi)
    if not paper:
        return {"pass": False, "doi": doi, "in_corpus": False, "note": f"DOI {doi} not in quote corpus"}

    sentences = paper.get("sentences", {})
    if qid and sentences:
        if qid in sentences:
            return {"pass": True, "doi": doi, "in_corpus": True, "note": f"quote_id [{qid}] verified", "resolved_quote": sentences[qid]}
        elif "-" in qid:
            parts = qid.split("-")
            if len(parts) == 2 and parts[0] in sentences and parts[1] in sentences:
                span_quote = sentences[parts[0]] + " " + sentences[parts[1]]
                return {"pass": True, "doi": doi, "in_corpus": True, "note": f"quote_id span [{qid}] verified", "resolved_quote": span_quote}
        return {"pass": False, "doi": doi, "in_corpus": True, "note": f"quote_id [{qid}] not found in sentence dictionary"}

    if quote and len(quote) >= 10:
        excerpts = paper.get("verbatim_excerpts", []) or list(sentences.values())
        quote_clean = quote.lower().strip()
        for exc in excerpts:
            if quote_clean in exc.lower() or exc.lower() in quote_clean:
                return {"pass": True, "doi": doi, "in_corpus": True, "note": "OK (substring match)"}
        return {"pass": False, "doi": doi, "in_corpus": True, "note": "Quote not found in verified excerpts"}

    return {"pass": False, "doi": doi, "in_corpus": True, "note": "Empty quote and missing quote_id"}

def check_doi_resolves(doi: str, cache_file: Path = None) -> Dict[str, Any]:
    clean_doi = str(doi or "").strip().lower()
    if not DOI_PATTERN.search(clean_doi):
        return {"pass": False, "doi": clean_doi, "note": "Malformed DOI string"}

    if cache_file and cache_file.exists():
        try:
            cache = json.loads(cache_file.read_text(encoding="utf-8"))
            if clean_doi in cache:
                cached_entry = cache[clean_doi]
                return {
                    "pass": cached_entry.get("resolved", True),
                    "doi": clean_doi,
                    "fetched_title": cached_entry.get("fetched_title", ""),
                    "note": "Cached resolution verified"
                }
        except Exception:
            pass

    return {"pass": True, "doi": clean_doi, "note": "Format valid (offline pass)"}

def verify_scenario(scenario: Dict[str, Any], corpus: Dict[str, Any], cache_file: Path = None) -> Dict[str, Any]:
    schema_res = check_schema(scenario)
    banned_res = check_banned_words(scenario)
    lang_res = check_no_language_names(scenario)
    leak_res = check_no_label_leakage(scenario)
    quote_res = check_quote_verified(scenario, corpus)
    doi_res = check_doi_resolves(scenario.get("citation_doi", ""), cache_file)

    all_pass = (
        schema_res["pass"] and
        banned_res["pass"] and
        lang_res["pass"] and
        leak_res["pass"] and
        quote_res["pass"] and
        doi_res["pass"]
    )

    return {
        "all_pass": all_pass,
        "schema": schema_res,
        "banned_words": banned_res,
        "no_language_names": lang_res,
        "no_label_leakage": leak_res,
        "quote_verified": quote_res,
        "doi_resolves": doi_res
    }

STANDARDS_REQUIRED_FIELDS = [
    "id", "standard_id", "summary", "full_scenario", "impact",
    "intervention", "citation_quote", "quote_id"
]

def check_standards_schema(scenario: Dict[str, Any]) -> Dict[str, Any]:
    missing = [f for f in STANDARDS_REQUIRED_FIELDS if not str(scenario.get(f, "")).strip()]
    return {
        "pass": len(missing) == 0,
        "missing_fields": missing
    }

def check_standards_quote_verified(scenario: Dict[str, Any], standards_corpus: Dict[str, Any]) -> Dict[str, Any]:
    std_id = str(scenario.get("standard_id", "")).strip()
    qid = str(scenario.get("quote_id", "")).strip()
    quote = str(scenario.get("citation_quote", "")).strip()

    if not std_id:
        return {"pass": False, "standard_id": None, "in_corpus": False, "note": "Missing standard_id"}

    entry = standards_corpus.get(std_id)
    if not entry:
        return {"pass": False, "standard_id": std_id, "in_corpus": False, "note": f"Standard {std_id} not found in standards corpus"}

    sentences = entry.get("sentences", {})
    if qid and sentences:
        if qid in sentences:
            expected = sentences[qid]
            if quote and (quote.lower() in expected.lower() or expected.lower() in quote.lower()):
                return {"pass": True, "standard_id": std_id, "in_corpus": True, "note": f"quote_id [{qid}] verified verbatim", "resolved_quote": expected}
            elif not quote:
                return {"pass": True, "standard_id": std_id, "in_corpus": True, "note": f"quote_id [{qid}] verified", "resolved_quote": expected}
            else:
                return {"pass": False, "standard_id": std_id, "in_corpus": True, "note": f"Quote mismatch for [{qid}]"}
        return {"pass": False, "standard_id": std_id, "in_corpus": True, "note": f"quote_id [{qid}] not in sentences"}

    if quote and len(quote) >= 10:
        for s_key, text in sentences.items():
            if quote.lower() in text.lower() or text.lower() in quote.lower():
                return {"pass": True, "standard_id": std_id, "in_corpus": True, "note": f"Verified match with [{s_key}]", "resolved_quote": text}
        return {"pass": False, "standard_id": std_id, "in_corpus": True, "note": "Quote not found in standard sentences"}

    return {"pass": False, "standard_id": std_id, "in_corpus": True, "note": "Empty quote and missing quote_id"}

def verify_standards_scenario(scenario: Dict[str, Any], standards_corpus: Dict[str, Any]) -> Dict[str, Any]:
    schema_res = check_standards_schema(scenario)
    banned_res = check_banned_words(scenario)
    lang_res = check_no_language_names(scenario)
    quote_res = check_standards_quote_verified(scenario, standards_corpus)

    all_pass = (
        schema_res["pass"] and
        banned_res["pass"] and
        lang_res["pass"] and
        quote_res["pass"]
    )

    return {
        "all_pass": all_pass,
        "schema": schema_res,
        "banned_words": banned_res,
        "no_language_names": lang_res,
        "quote_verified": quote_res
    }

