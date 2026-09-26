"""
benchmark/parse_16_sessions.py
==============================
Parses eval-dataset-16-sessions.md into structured JSON (benchmark/dataset_16_structured.json).
Preserves verbatim prompt and response texts, multi-turn sequences, and human labels.
Authoritative source remains eval-dataset-16-sessions.md.
"""

import os
import re
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SOURCE_PATH = os.path.join(BASE_DIR, "eval-dataset-16-sessions.md")
OUTPUT_PATH = os.path.join(BASE_DIR, "dataset_16_structured.json")

with open(SOURCE_PATH, "r", encoding="utf-8") as f:
    full_text = f.read()

# Split into sessions by "## Session X — ..."
session_blocks = re.split(r'\n(?=## Session \d+ — )', full_text)
# The first element is the introduction and summary table
intro_block = session_blocks[0]
session_blocks = session_blocks[1:]

parsed_sessions = []

for block in session_blocks:
    # 1. Session ID and Title
    header_match = re.search(r'## Session (\d+) — ([^\n]+)', block)
    if not header_match:
        continue
    session_id = int(header_match.group(1))
    
    # 2. Metadata fields
    task_shape_match = re.search(r'\*\*Task shape:\*\*\s*([^\n]+)', block)
    task_shape = task_shape_match.group(1).strip() if task_shape_match else ""
    
    criterion_match = re.search(r'\*\*Criterion tested:\*\*\s*([^\n]+)', block)
    criterion_tested = criterion_match.group(1).strip() if criterion_match else ""
    
    # 3. Human Label and Rationale
    # Find "**My label:** <text>"
    label_match = re.search(r'\*\*My label:\*\*\s*([^\n]+(?:\n(?!\n|\*\*|##|---)[^\n]+)*)', block)
    human_rationale_full = label_match.group(1).strip() if label_match else ""
    
    # Categorize label into "No violation | Partial | Violation"
    first_sentence = human_rationale_full.split(".")[0].lower() if human_rationale_full else ""
    if "no violation" in first_sentence:
        human_label = "No violation"
    elif "partial" in first_sentence or "borderline" in first_sentence:
        human_label = "Partial"
    elif "violation" in first_sentence:
        human_label = "Violation"
    else:
        human_label = human_rationale_full[:30]

    # 4. Turns
    turns = []
    
    # Check if multi-turn (Sessions 7 and 9)
    if "Turn 1 prompt:" in block:
        # Multi-turn parsing
        turn_matches = list(re.finditer(r'\*\*Turn (\d+) prompt(?:\s*\([^)]*\))?:\*\*', block))
        for i, tm in enumerate(turn_matches):
            t_num = tm.group(1)
            # Find corresponding response
            resp_pattern = rf'\*\*Turn {t_num} response(?:\s*\([^)]*\))?:\*\*'
            resp_match = re.search(resp_pattern, block)
            if not resp_match:
                continue
            
            prompt_start = tm.end()
            prompt_end = resp_match.start()
            prompt_content = block[prompt_start:prompt_end].strip()
            # Clean leading quote markers if present
            prompt_content = re.sub(r'^>\s*', '', prompt_content, flags=re.MULTILINE).strip()
            
            # Response end is either next turn prompt or Ground truth
            resp_start = resp_match.end()
            if i + 1 < len(turn_matches):
                resp_end = turn_matches[i+1].start()
            else:
                gt_match = re.search(r'\*\*Ground truth(?:\s*\([^)]*\))?:\*\*', block)
                resp_end = gt_match.start() if gt_match else len(block)
                
            resp_content = block[resp_start:resp_end].strip()
            # If response is blockquoted, strip blockquote markers
            if resp_content.startswith(">"):
                resp_lines = [re.sub(r'^>\s?', '', l) for l in resp_content.split("\n")]
                resp_content = "\n".join(resp_lines).strip()
                
            turns.append({"role": "developer", "content": prompt_content})
            turns.append({"role": "assistant", "content": resp_content})
    else:
        # Single-turn parsing
        prompt_match = re.search(r'\*\*Prompt sent:\*\*\s*(.*?)(?=\n\*\*Full response:\*\*)', block, re.DOTALL)
        if prompt_match:
            prompt_content = prompt_match.group(1).strip()
            prompt_content = re.sub(r'^>\s*', '', prompt_content, flags=re.MULTILINE).strip()
        else:
            prompt_content = ""
            
        resp_match = re.search(r'\*\*Full response(?:\s*\([^)]*\))?:\*\*\s*(.*?)(?=\n\*\*Ground truth)', block, re.DOTALL)
        if resp_match:
            resp_content = resp_match.group(1).strip()
            if resp_content.startswith(">"):
                resp_lines = [re.sub(r'^>\s?', '', l) for l in resp_content.split("\n")]
                resp_content = "\n".join(resp_lines).strip()
        else:
            resp_content = ""
            
        turns.append({"role": "developer", "content": prompt_content})
        turns.append({"role": "assistant", "content": resp_content})
        
    session_obj = {
        "session_id": session_id,
        "task_shape": task_shape,
        "criterion_tested": criterion_tested,
        "turns": turns,
        "human_label": human_label,
        "human_rationale": human_rationale_full
    }
    parsed_sessions.append(session_obj)

# Sort by session_id
parsed_sessions.sort(key=lambda s: s["session_id"])

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(parsed_sessions, f, indent=2, ensure_ascii=False)

print(f"Successfully parsed {len(parsed_sessions)} sessions into {OUTPUT_PATH}")
for s in parsed_sessions:
    turns_count = len(s["turns"])
    print(f"  Session {s['session_id']:02d}: {s['criterion_tested']:<35} | {s['human_label']:<15} | {turns_count} turns")
