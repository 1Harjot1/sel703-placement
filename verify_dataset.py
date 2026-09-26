"""
verify_dataset.py — Run Deterministic Verification Across Dataset
=================================================================
Usage:
    python verify_dataset.py --dataset src/data/final_180.csv
"""

import argparse
from pathlib import Path
import pandas as pd
from src.corpus_loader import load_quote_corpus
from src.verifier import verify_scenario

def run_batch_verify(dataset_path: Path):
    data_dir = Path(__file__).parent / "src" / "data"
    corpus = load_quote_corpus(data_dir)
    cache_file = data_dir / "doi_cache.json"

    df = pd.read_csv(dataset_path)
    total = len(df)
    passed = 0
    failures = []

    print(f"Evaluating {total} scenarios from {dataset_path.name}...")

    for idx, r in df.iterrows():
        scenario = {
            "summary": r.get("concern", r.get("summary", "")),
            "full_scenario": r.get("logic", r.get("full_scenario", "")),
            "impact": r.get("impact", ""),
            "reasoning": r.get("logic", r.get("reasoning", "")),
            "intervention": r.get("intervention", ""),
            "value_violated": r.get("value_item", r.get("value_violated", "")),
            "behaviour": r.get("behavior", r.get("behaviour", "")),
            "citation_doi": r.get("citation_doi", ""),
            "quote_id": r.get("quote_id", ""),
            "evidence": r.get("evidence", r.get("citation_quote", ""))
        }
        res = verify_scenario(scenario, corpus, cache_file)
        if res["all_pass"]:
            passed += 1
        else:
            failures.append((r.get("sid", f"ROW-{idx+1}"), res))

    print("=" * 60)
    print(" BATCH VERIFICATION RESULTS ")
    print("=" * 60)
    print(f"Total Scenarios Evaluated : {total}")
    print(f"Passed All Checks         : {passed} / {total} ({passed/total*100:.1f}%)")
    print(f"Failed Checks             : {len(failures)} / {total}")
    if failures:
        print("\nFailures Detail (First 3):")
        for sid, f in failures[:3]:
            print(f"  * {sid}: {f}")
    print("=" * 60)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Batch Verifier for Scenarios")
    parser.add_argument("--dataset", type=str, default="src/data/final_180.csv", help="Path to CSV dataset")
    args = parser.parse_args()
    run_batch_verify(Path(args.dataset))
