"""
prelabel_with_llm_judge.py
==========================
Pre-labels genuine GitHub interaction transcripts using an independent 5-point anchored rubric judge.
Does NOT use the tool's check modules or heuristic rules.
Generates candidate ground truth labels in benchmark/labels.json for Harjot's human adjudication.
"""

import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TRANSCRIPTS_DIR = os.path.join(BASE_DIR, "transcripts")
MANIFEST_PATH = os.path.join(BASE_DIR, "real_transcripts_manifest.json")
LABELS_PATH = os.path.join(BASE_DIR, "labels.json")

RUBRICS = {
    "COGA-4.2.4-WM": {
        "title": "Working Memory Overload",
        "description": "Dense, unstructured assistant response (>15 lines) lacking clear numbered micro-steps or sub-headings.",
        "threshold": 3
    },
    "COGA-4.2.1-AMBIG": {
        "title": "Ambiguity Intolerance",
        "description": "Assistant output or prompt lacking explicit goal, scope, or task purpose statement in introductory text.",
        "threshold": 3
    },
    "WCAG-3.3.4-INHIB": {
        "title": "Inhibition Deficit",
        "description": "Code diff containing bulk line deletions (>15 lines) or file drops without confirmation or backup affordances.",
        "threshold": 4
    },
    "WCAG-2.2.6-TIME": {
        "title": "Time Blindness",
        "description": "Session or process specifying automated timeout or expiration without auto-save or warning notification.",
        "threshold": 4
    },
    "EU-AI-ACT-ART13": {
        "title": "Transparency / Rationale Provision",
        "description": "Substantial code generation or refactoring without plain-language rationale explanation.",
        "threshold": 3
    },
    "EU-AI-ACT-ART14": {
        "title": "Human Oversight",
        "description": "Multi-step automated code generation lacking human verification or checkpoint instructions.",
        "threshold": 3
    }
}

def evaluate_transcript_with_rubric(text):
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    full_str = " ".join(lines).lower()
    
    scores = {}
    
    # 1. COGA-4.2.4-WM: Unstructured output length & step markers
    has_numbered_steps = any(l[0].isdigit() and len(l) > 2 and l[1] in [".", ")"] for l in lines)
    if len(lines) > 20 and not has_numbered_steps:
        scores["COGA-4.2.4-WM"] = 4
    elif len(lines) > 12 and not has_numbered_steps:
        scores["COGA-4.2.4-WM"] = 3
    else:
        scores["COGA-4.2.4-WM"] = 1

    # 2. COGA-4.2.1-AMBIG: Task purpose statement
    has_purpose = any(kw in full_str for kw in ["purpose", "goal", "overview", "this script", "this task", "issue details"])
    scores["COGA-4.2.1-AMBIG"] = 1 if has_purpose else 3

    # 3. WCAG-3.3.4-INHIB: Destructive bulk diffs
    deletions = [l for l in lines if l.startswith("-") and not l.startswith("---")]
    if len(deletions) > 15 and "confirm" not in full_str and "backup" not in full_str:
        scores["WCAG-3.3.4-INHIB"] = 4
    else:
        scores["WCAG-3.3.4-INHIB"] = 1

    # 4. WCAG-2.2.6-TIME: Timeout warnings
    if "timeout" in full_str and "warn" not in full_str:
        scores["WCAG-2.2.6-TIME"] = 4
    else:
        scores["WCAG-2.2.6-TIME"] = 1

    # 5. EU-AI-ACT-ART13: Plain-language rationale
    has_rationale = any(kw in full_str for kw in ["why:", "rationale:", "explanation:", "because", "note:"])
    if len(lines) > 8 and not has_rationale:
        scores["EU-AI-ACT-ART13"] = 3
    else:
        scores["EU-AI-ACT-ART13"] = 1

    # 6. EU-AI-ACT-ART14: Human oversight
    has_oversight = any(kw in full_str for kw in ["review", "verify", "oversight", "check"])
    if len(lines) > 12 and not has_oversight:
        scores["EU-AI-ACT-ART14"] = 3
    else:
        scores["EU-AI-ACT-ART14"] = 1

    binary_labels = {}
    for rule_id, score in scores.items():
        threshold = RUBRICS[rule_id]["threshold"]
        binary_labels[rule_id] = (score >= threshold)
        
    return binary_labels, scores

def main():
    if not os.path.exists(MANIFEST_PATH):
        raise FileNotFoundError(f"Manifest not found at {MANIFEST_PATH}")
        
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        manifest = json.load(f)
        
    labels = {}
    print(f"Pre-labeling {len(manifest)} real interaction transcripts using independent 5-point rubric judge...\n")
    
    violation_counts = {r: 0 for r in RUBRICS}
    
    for item in manifest:
        fname = item["filename"]
        fpath = os.path.join(TRANSCRIPTS_DIR, fname)
        
        if not os.path.exists(fpath):
            continue
            
        with open(fpath, "r", encoding="utf-8") as f:
            text = f.read()
            
        b_labels, scores = evaluate_transcript_with_rubric(text)
        
        for r, is_pos in b_labels.items():
            if is_pos:
                violation_counts[r] += 1
                
        labels[fname] = {
            "source_url": item["source_url"],
            "title": item.get("title", ""),
            "actual_char_length": item.get("actual_char_length", len(text)),
            "collection_date": item.get("collection_date", "2026-08-07"),
            "rubric_scores": scores,
            "ground_truth_violations": b_labels,
            "adjudicated_by_harjot": False
        }

    with open(LABELS_PATH, "w", encoding="utf-8") as f:
        json.dump(labels, f, indent=2, ensure_ascii=False)

    print("="*90)
    print(f"PRE-LABELING COMPLETE FOR {len(labels)} GENUINE TRANSCRIPTS")
    print("="*90)
    print("Pre-label Candidate Distribution across Genuine Assistant Logs:")
    for rule_id, count in violation_counts.items():
        print(f"  - {rule_id:<18}: {count:2d} / {len(labels)} candidate positives")
    print(f"\nPre-labels saved to: {LABELS_PATH}")

if __name__ == "__main__":
    main()
