"""
benchmark/evaluate_tool_benchmark.py
=====================================
Evaluates the SEL703 testing tool against benchmark/labels.json.
Calculates Precision, Recall, and F1 score per criterion and overall.
"""

import os
import json
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TOOL_DIR = os.path.join(BASE_DIR, "..")
sys.path.insert(0, TOOL_DIR)

from tool.runner import TestRunner

LABELS_PATH = os.path.join(BASE_DIR, "labels.json")
TRANSCRIPTS_DIR = os.path.join(BASE_DIR, "transcripts")
RESULTS_PATH = os.path.join(BASE_DIR, "evaluation_results.json")

def evaluate():
    if not os.path.exists(LABELS_PATH):
        raise FileNotFoundError(f"Labels file not found at {LABELS_PATH}")
        
    with open(LABELS_PATH, "r", encoding="utf-8") as f:
        labels_data = json.load(f)
        
    runner = TestRunner()
    
    criterion_stats = {}
    
    for fname, item in labels_data.items():
        fpath = os.path.join(TRANSCRIPTS_DIR, fname)
        gt = item.get("ground_truth_violations", {})
        
        report = runner.run_tests(fpath)
        detected_rule_ids = set(v["rule_id"] for v in report["violations"])
        
        for rule_id, is_gt_pos in gt.items():
            if rule_id not in criterion_stats:
                criterion_stats[rule_id] = {"tp": 0, "fp": 0, "fn": 0, "tn": 0}
                
            is_pred_pos = rule_id in detected_rule_ids
            
            if is_gt_pos and is_pred_pos:
                criterion_stats[rule_id]["tp"] += 1
            elif not is_gt_pos and is_pred_pos:
                criterion_stats[rule_id]["fp"] += 1
            elif is_gt_pos and not is_pred_pos:
                criterion_stats[rule_id]["fn"] += 1
            else:
                criterion_stats[rule_id]["tn"] += 1

    print("="*90)
    print("SEL703 TESTING TOOL BENCHMARK EVALUATION RESULTS")
    print("="*90)
    print(f"| {'Criterion Rule ID':<22} | {'TP':<4} | {'FP':<4} | {'FN':<4} | {'Precision':<10} | {'Recall':<10} | {'F1-Score':<10} |")
    print("|" + "-"*24 + "|" + "-"*6 + "|" + "-"*6 + "|" + "-"*6 + "|" + "-"*12 + "|" + "-"*12 + "|" + "-"*12 + "|")
    
    total_tp = sum(s["tp"] for s in criterion_stats.values())
    total_fp = sum(s["fp"] for s in criterion_stats.values())
    total_fn = sum(s["fn"] for s in criterion_stats.values())
    
    macro_precision = []
    macro_recall = []
    macro_f1 = []
    
    for rule_id, s in criterion_stats.items():
        p = s["tp"] / (s["tp"] + s["fp"]) if (s["tp"] + s["fp"]) > 0 else 1.0
        r = s["tp"] / (s["tp"] + s["fn"]) if (s["tp"] + s["fn"]) > 0 else 1.0
        f1 = (2 * p * r) / (p + r) if (p + r) > 0 else 0.0
        
        macro_precision.append(p)
        macro_recall.append(r)
        macro_f1.append(f1)
        
        print(f"| {rule_id:<22} | {s['tp']:<4} | {s['fp']:<4} | {s['fn']:<4} | {p:<10.2f} | {r:<10.2f} | {f1:<10.2f} |")
        
    overall_p = total_tp / (total_tp + total_fp) if (total_tp + total_fp) > 0 else 1.0
    overall_r = total_tp / (total_tp + total_fn) if (total_tp + total_fn) > 0 else 1.0
    overall_f1 = (2 * overall_p * overall_r) / (overall_p + overall_r) if (overall_p + overall_r) > 0 else 0.0
    
    print("-" * 90)
    print(f"| {'OVERALL BENCHMARK':<22} | {total_tp:<4} | {total_fp:<4} | {total_fn:<4} | {overall_p:<10.2f} | {overall_r:<10.2f} | {overall_f1:<10.2f} |")
    print("=" * 90)
    
    res = {
        "overall_precision": round(overall_p, 4),
        "overall_recall": round(overall_r, 4),
        "overall_f1": round(overall_f1, 4),
        "per_criterion": criterion_stats
    }
    
    with open(RESULTS_PATH, "w", encoding="utf-8") as f:
        json.dump(res, f, indent=2, ensure_ascii=False)
        
    print(f"\nSaved evaluation metrics to {RESULTS_PATH}")

if __name__ == "__main__":
    evaluate()
