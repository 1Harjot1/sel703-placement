"""
rater.py — Nominal Anchored LLM Rating Engine (Stage 5)
=======================================================
Implements 5-point nominal anchored rating evaluating:
1. RELEVANCE (Evidence-based Interpretive Distance):
   - Verified (5): Direct reference to cited psychology evidence; no interpretation needed.
   - Supported (4): Traceable to cited psychology evidence with minor interpretation.
   - Partial (3): Traceable to cited psychology evidence with some interpretation.
   - Doubtful (2): Traceable with significant interpretation.
   - Unfounded (1): Not traceable to cited evidence.

2. PLAUSIBILITY (Likelihood):
   - Certain (5), Likely (4), Possible (3), Unlikely (2), Implausible (1).

3. SPECIFICITY (Level of Detail):
   - Specific (5), Detailed (4), General (3), Broad (2), Vague (1).
"""

from typing import Dict, Any

NOMINAL_RUBRICS = {
    "relevance": {
        5: "Verified",
        4: "Supported",
        3: "Partial",
        2: "Doubtful",
        1: "Unfounded"
    },
    "plausibility": {
        5: "Certain",
        4: "Likely",
        3: "Possible",
        2: "Unlikely",
        1: "Implausible"
    },
    "specificity": {
        5: "Specific",
        4: "Detailed",
        3: "General",
        2: "Broad",
        1: "Vague"
    }
}

def rate_scenario_heuristically(scenario: Dict[str, Any]) -> Dict[str, str]:
    """
    Nominal rater fallback when external LLM judge is not called.
    Retrieves authentic rater values if already present, or computes
    anchored nominal ratings based on evidence link and narrative depth.
    """
    if "relevance" in scenario and "plausibility" in scenario and "specificity" in scenario:
        return {
            "relevance": scenario["relevance"],
            "plausibility": scenario["plausibility"],
            "specificity": scenario["specificity"]
        }

    evidence = str(scenario.get("evidence", "") or scenario.get("citation_quote", "")).strip()
    full_text = str(scenario.get("full_scenario", "")).strip()

    # Heuristic nominal mapping
    if len(evidence) > 40 and str(scenario.get("quote_id", "")).startswith("s"):
        rel = "Supported"
    elif len(evidence) > 10:
        rel = "Partial"
    else:
        rel = "Doubtful"

    plaus = "Likely" if len(full_text) > 200 else "Possible"
    spec = "Specific" if len(full_text) > 300 else "Detailed"

    return {
        "relevance": rel,
        "plausibility": plaus,
        "specificity": spec
    }
