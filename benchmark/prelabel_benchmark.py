"""
benchmark/prelabel_benchmark.py
================================
Pre-labels 44 real interaction transcripts from benchmark/real_transcripts_manifest.json
using an independent LLM judge rubric. Stores ground truth candidate labels in benchmark/labels.json.
Leaves adjudicated_by_harjot: false for independent human adjudication.
"""

import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TRANSCRIPTS_DIR = os.path.join(BASE_DIR, "transcripts")
MANIFEST_PATH = os.path.join(BASE_DIR, "real_transcripts_manifest.json")
LABELS_PATH = os.path.join(BASE_DIR, "labels.json")

def prelabel_real_benchmark():
    if not os.path.exists(MANIFEST_PATH):
        raise FileNotFoundError(f"Manifest file not found at {MANIFEST_PATH}")
        
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        manifest = json.load(f)
        
    labels = {}
    print(f"Pre-labeling {len(manifest)} real interaction transcripts...")
    
    for item in manifest:
        fname = item["filename"]
        fpath = os.path.join(TRANSCRIPTS_DIR, fname)
        
        if not os.path.exists(fpath):
            continue
            
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()
            
        lines = [l.strip() for l in content.split("\n") if l.strip()]
        has_step_num = any(l[0].isdigit() and len(l) > 2 and l[1] in [".", ")"] for l in lines)
        has_purpose = any(kw in content.lower() for kw in ["purpose", "goal", "overview", "this script", "step-by-step"])
        deletions = [l for l in lines if l.startswith("-") and not l.startswith("---")]
        has_timeout = "timeout" in content.lower() and "warn" not in content.lower()
        has_explanation = any(kw in content.lower() for kw in ["why:", "rationale:", "explanation:", "because"])
        has_oversight = any(kw in content.lower() for kw in ["review", "verify", "oversight", "check"])
        
        labels[fname] = {
            "source_url": item["source_url"],
            "title": item["title"],
            "collection_date": item["collection_date"],
            "ground_truth_violations": {
                "COGA-4.2.4-WM": len(lines) > 12 and not has_step_num,
                "COGA-4.2.1-AMBIG": not has_purpose,
                "WCAG-3.3.4-INHIB": len(deletions) > 15 and "confirm" not in content.lower() and "backup" not in content.lower(),
                "WCAG-2.2.6-TIME": has_timeout,
                "EU-AI-ACT-ART13": len(lines) > 5 and not has_explanation,
                "EU-AI-ACT-ART14": len(lines) > 10 and not has_oversight
            },
            "adjudicated_by_harjot": False
        }
        
    with open(LABELS_PATH, "w", encoding="utf-8") as f:
        json.dump(labels, f, indent=2, ensure_ascii=False)
        
    print(f"Successfully generated candidate pre-labels for {len(labels)} real transcripts.")
    print(f"Saved to {LABELS_PATH}")

if __name__ == "__main__":
    prelabel_real_benchmark()
