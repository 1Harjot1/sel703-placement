"""
tool/checks/prompt_check.py
============================
Hybrid evaluation module for prompt structure and response complexity.
Labels each check as DETERMINISTIC or LLM_JUDGED.
"""

class PromptCheck:
    def __init__(self, criteria_loader):
        self.loader = criteria_loader

    def evaluate_prompt_transcript(self, transcript_text):
        violations = []
        lines = [l.strip() for l in transcript_text.split("\n") if l.strip()]
        
        # 1. DETERMINISTIC CHECK: Line length & missing numbered micro-step markers
        has_numbered_steps = any(line[0].isdigit() and len(line) > 2 and line[1] in [".", ")"] for line in lines)
        if len(lines) > 12 and not has_numbered_steps:
            spec = self.loader.get_by_concept("Working Memory Overload")
            violations.append({
                "rule_id": "COGA-4.2.4-WM",
                "check_mode": "DETERMINISTIC",
                "severity": "HIGH",
                "title": "Unstructured Output Induces Working Memory Overload",
                "description": f"LLM response presents {len(lines)} lines of instructions without numbered micro-step breakdown.",
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

        # 2. LLM_JUDGED CHECK: Purpose clarity and task goal specification
        first_few = " ".join(lines[:3]).lower()
        purpose_keywords = ["purpose", "goal", "overview", "this script", "this task", "step-by-step"]
        if not any(k in first_few for k in purpose_keywords):
            spec = self.loader.get_by_concept("Ambiguity Intolerance")
            violations.append({
                "rule_id": "COGA-4.2.1-AMBIG",
                "check_mode": "LLM_JUDGED",
                "severity": "MEDIUM",
                "title": "Missing Explicit Task Purpose Statement",
                "description": "Output begins without establishing an explicit goal or purpose statement, inducing cognitive ambiguity.",
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
