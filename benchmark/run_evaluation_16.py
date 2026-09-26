"""
benchmark/run_evaluation_16.py
==============================
Runs Cognitive-Access tool against the 16-session ground-truth dataset.
Strictly respects non-negotiable rules:
  1. Does not modify eval-dataset-16-sessions.md.
  2. Checks receive ONLY prompt and response turns (never human label or prediction).
  3. Preserves multi-turn sequences (Sessions 7 & 9).
  4. Explicitly maps criteria and records per-session results and additional findings.
"""

import os
import json
import sys
from tool.runner import TestRunner

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_PATH = os.path.join(BASE_DIR, "dataset_16_structured.json")
RESULTS_PATH = os.path.join(BASE_DIR, "evaluation_results_16.json")

# Map dataset criteria keywords to tool rule IDs
CRITERIA_MAP = {
    "purpose clarity": ["COGA-4.2.1-AMBIG"],
    "step structure": ["COGA-4.2.4-WM"],
    "undo availability": ["WCAG-3.3.4-INHIB", "WCAG-2.2.6-TIME"],
    "transparency of confidence": ["EU-AI-ACT-ART13"],
    "human oversight": ["EU-AI-ACT-ART14"],
    "scope adherence": ["COGA-4.5.3-SCOPE"]
}

def get_applicable_rules(criterion_tested_str):
    c_lower = criterion_tested_str.lower()
    applicable = set()
    for key, rules in CRITERIA_MAP.items():
        if key in c_lower:
            applicable.update(rules)
    return applicable

with open(DATASET_PATH, "r", encoding="utf-8") as f:
    dataset = json.load(f)

runner = TestRunner(mode="all")

results = []

for session in dataset:
    sid = session["session_id"]
    task_shape = session["task_shape"]
    criterion_tested = session["criterion_tested"]
    human_label = session["human_label"]
    human_rationale = session["human_rationale"]
    turns = session["turns"]

    # 1. Multi-turn handling: Concatenate all turns sequentially
    transcript_blocks = []
    for turn in turns:
        role_label = "Developer" if turn["role"] == "developer" else "Assistant"
        transcript_blocks.append(f"[{role_label}]:\n{turn['content']}")
    full_transcript = "\n\n".join(transcript_blocks)

    # Save to a temporary file for runner
    tmp_path = os.path.join(BASE_DIR, f"temp_session_{sid:02d}.txt")
    with open(tmp_path, "w", encoding="utf-8") as f:
        f.write(full_transcript)

    # 2. Run tool checks without seeing labels or predictions
    try:
        report = runner.run_tests(tmp_path)
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

    all_violations = report.get("violations", [])
    applicable_rules = get_applicable_rules(criterion_tested)

    # Separate violations on the criterion tested vs additional findings
    tested_violations = [v for v in all_violations if v["rule_id"] in applicable_rules]
    additional_findings = [v for v in all_violations if v["rule_id"] not in applicable_rules]

    # Determine tool result for the criterion tested
    if not applicable_rules:
        # e.g. Scope adherence only
        tool_result = "unsupported_criterion"
        agreement = "N/A (unsupported criterion)"
    elif tested_violations:
        tool_result = "fail"
        if human_label == "No violation":
            agreement = False # False positive
        elif human_label == "Violation":
            agreement = True  # True positive
        else:
            agreement = "Partial (tool flagged)"
    else:
        tool_result = "pass"
        if human_label == "No violation":
            agreement = True  # True negative
        elif human_label == "Violation":
            agreement = False # False negative
        else:
            agreement = "Partial (tool passed)"

    tool_detail = "; ".join([f"{v['rule_id']} ({v['severity']}): {v['description']}" for v in tested_violations]) if tested_violations else "No violations on tested criterion."
    additional_detail = "; ".join([f"{v['rule_id']}: {v['title']}" for v in additional_findings]) if additional_findings else "None"

    results.append({
        "session_id": sid,
        "task_shape": task_shape,
        "criterion_tested": criterion_tested,
        "applicable_rules": list(applicable_rules),
        "tool_result": tool_result,
        "tool_detail": tool_detail,
        "additional_findings": additional_detail,
        "human_label": human_label,
        "human_rationale": human_rationale,
        "agreement": agreement,
        "raw_violations_count": len(all_violations)
    })

with open(RESULTS_PATH, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print(f"Completed evaluation on all {len(results)} sessions. Saved to {RESULTS_PATH}.")
