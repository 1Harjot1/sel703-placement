"""
tool/cli.py
===========
Command-line interface for the Cognitive-Access Testing Tool (ICSE 2027 Demo Track).
Displays check mode ([DETERMINISTIC] vs [LLM_JUDGED]) and full 3-tier traceability.
Usage:
  python -m tool.cli test <filepath> [--mode all|deterministic|gemini]
  python -m tool.cli report <filepath> [--mode all|deterministic|gemini]
"""

import sys
import json
import os
from .runner import TestRunner

def main():
    if len(sys.argv) < 3:
        print("Cognitive-Access Testing Tool (ICSE 2027 Tool Demonstrations Track)")
        print("Usage: python -m tool.cli [test|report] <target_filepath> [--mode all|deterministic|gemini]")
        sys.exit(1)

    command = sys.argv[1].lower()
    filepath = sys.argv[2]
    
    mode = "all"
    if "--mode" in sys.argv:
        m_idx = sys.argv.index("--mode")
        if m_idx + 1 < len(sys.argv):
            mode = sys.argv[m_idx + 1].lower()

    runner = TestRunner(mode=mode)
    
    try:
        report = runner.run_tests(filepath)
    except Exception as e:
        print(f"Error running evaluation: {e}")
        sys.exit(1)

    if command == "test":
        print("="*90)
        print("COGNITIVE-ACCESS TESTING TOOL REPORT (ICSE 2027 DEMO TRACK)")
        print("="*90)
        print(f"Target File:       {report['target_file']}")
        print(f"Execution Mode:    {report['mode'].upper()}")
        print(f"Gemini LLM Judge:  {'ACTIVE (Free Tier)' if report['gemini_active'] else 'FALLBACK (Deterministic-Only)'}")
        
        if report.get("execution_notices"):
            for notice in report["execution_notices"]:
                print(f"Notice:            {notice}")
                
        print(f"\nTotal Violations:  {report['total_violations']}")
        print(f"  - High Severity:   {report['high_severity_count']}")
        print(f"  - Medium Severity: {report['medium_severity_count']}\n")

        for idx, v in enumerate(report["violations"], 1):
            mode_tag = f"[{v.get('check_mode', 'DETERMINISTIC')}]"
            print(f"[{idx}] {v['rule_id']} {mode_tag} ({v.get('severity', 'MEDIUM')}) — {v['title']}")
            print(f"    Description:        {v.get('description', '')}")
            print(f"    Tier 1 Standard:    {v.get('source', '')} {v.get('source_section', '')} ({v.get('guideline', '')})")
            print(f"    Tier 2 Concept:     {v.get('cognitive_concept', '')} ({v.get('concept_citation', '')})")
            print(f"    Tier 2 Quote ID:    {v.get('concept_quote_id', '')}")
            print(f"    Tier 2 Source Title:{v.get('source_printed_title', '')}")
            quote_snip = v.get('concept_quote', '')
            print(f"    Tier 2 Quote Text:  \"{quote_snip[:90]}...\"" if len(quote_snip) > 90 else f"    Tier 2 Quote Text:  \"{quote_snip}\"")
            print(f"    Tier 3 Value:       {v.get('schwartz_value', '')} (\"{v.get('value_definition', '')}\")")
            print("-" * 90)

    elif command == "report":
        print(json.dumps(report, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
