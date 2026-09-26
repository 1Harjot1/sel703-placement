"""
tool/checks/transparency_check.py
==================================
Evaluates AI output for explicit rationale explanations and human oversight triggers.
Labels checks as LLM_JUDGED.
"""

class TransparencyCheck:
    def __init__(self, criteria_loader):
        self.loader = criteria_loader

    def evaluate_ai_output(self, ai_output_text):
        violations = []
        lines = [l.strip() for l in ai_output_text.split("\n") if l.strip()]
        
        has_explanation = any(kw in ai_output_text.lower() for kw in ["why:", "rationale:", "explanation:", "because", "note:"])
        has_oversight = any(kw in ai_output_text.lower() for kw in ["review", "verify", "oversight", "check"])
        
        if len(lines) > 5 and not has_explanation:
            spec = self.loader.get_by_concept("Ambiguity Intolerance")
            violations.append({
                "rule_id": "EU-AI-ACT-ART13",
                "check_mode": "LLM_JUDGED",
                "severity": "MEDIUM",
                "title": "Opaque AI Output Lacks Plain-Language Rationale",
                "description": "AI assistant generated complex output without accompanying plain-language explanation of its reasoning.",
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
            
        if len(lines) > 10 and not has_oversight:
            spec = self.loader.get_by_concept("Planning Deficit")
            violations.append({
                "rule_id": "EU-AI-ACT-ART14",
                "check_mode": "LLM_JUDGED",
                "severity": "HIGH",
                "title": "Missing Human Oversight Checkpoint",
                "description": "AI assistant generated multi-step code changes without embedding an explicit human verification checkpoint.",
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
