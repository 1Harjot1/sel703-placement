"""
tool/checks/diff_check.py
==========================
Evaluates code diffs for destructive modifications without rollback affordances.
Labels check as DETERMINISTIC.
"""

class DiffCheck:
    def __init__(self, criteria_loader):
        self.loader = criteria_loader

    def evaluate_diff(self, diff_content):
        violations = []
        lines = diff_content.split("\n")
        
        deletions = [l for l in lines if l.startswith("-") and not l.startswith("---")]
        
        if len(deletions) > 15 and "confirm" not in diff_content.lower() and "backup" not in diff_content.lower():
            spec = self.loader.get_by_concept("Inhibition Deficit")
            violations.append({
                "rule_id": "WCAG-3.3.4-INHIB",
                "check_mode": "DETERMINISTIC",
                "severity": "HIGH",
                "title": "Irreversible Bulk Code Deletion Without Confirmation Affordance",
                "description": f"Diff contains {len(deletions)} deleted lines without explicit confirmation check or automated backup trigger.",
                "guideline": spec["guideline"],
                "source": spec["source"],
                "source_section": spec["source_section"],
                "cognitive_concept": spec["cognitive_concept"],
                "concept_citation": spec["concept_citation"],
                "concept_quote_id": spec["concept_quote_id"],
                "source_printed_title": spec["source_printed_title"],
                "concept_quote": spec["concept_quote"],
                "schwartz_value": spec["schwartz_value"],
                "value_definition": spec["value_definition"]
            })
            
        return violations
