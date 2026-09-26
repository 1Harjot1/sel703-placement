"""
benchmark/verify_session_15_input.py
====================================
Prints the exact raw text fed to the tool for Session 15,
and verifies zero leakage of human labels, predictions, or ground truth.
"""

import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_PATH = os.path.join(BASE_DIR, "dataset_16_structured.json")

with open(DATASET_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

s15 = [s for s in data if s["session_id"] == 15][0]

transcript_blocks = []
for turn in s15["turns"]:
    role_label = "Developer" if turn["role"] == "developer" else "Assistant"
    transcript_blocks.append(f"[{role_label}]:\n{turn['content']}")
full_input_to_tool = "\n\n".join(transcript_blocks)

# Check for forbidden strings
forbidden = [
    "human_label",
    "human_rationale",
    "My label",
    "My prediction",
    "Ground truth",
    "Violation"
]

leakage_findings = [w for w in forbidden if w in full_input_to_tool]

print("="*80)
print("SESSION 15 INPUT VERIFICATION AUDIT")
print("="*80)
print(f"Total Character Count Fed to Tool: {len(full_input_to_tool)}")
print(f"Forbidden Strings Detected:        {leakage_findings if leakage_findings else 'NONE (Zero Leakage)'}")
print("="*80)
print("\n--- EXACT VERBATIM INPUT STRING FED TO TOOL FOR SESSION 15 ---\n")
print(full_input_to_tool)
print("\n--- END OF INPUT STRING ---\n")
