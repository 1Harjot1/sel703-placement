"""
tool/checks/timeout_check.py
=============================
Evaluates session timeouts and timing configurations for Time Blindness support.
Labels check as DETERMINISTIC.
"""

class TimeoutCheck:
    def __init__(self, criteria_loader):
        self.loader = criteria_loader

    def evaluate_config(self, config_content):
        violations = []
        c_lower = config_content.lower()
        
        has_timeout = "timeout" in c_lower or "expire" in c_lower
        has_warning = "warn" in c_lower or "notice" in c_lower or "preserve" in c_lower or "autosave" in c_lower
        
        if has_timeout and not has_warning:
            spec = self.loader.get_by_concept("Time Blindness")
            violations.append({
                "rule_id": "WCAG-2.2.6-TIME",
                "check_mode": "DETERMINISTIC",
                "severity": "HIGH",
                "title": "Unwarned Session Timeout Risk",
                "description": "System specifies automated session timeout without state auto-save or warning notification affordances.",
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
