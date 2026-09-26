"""
tool/runner.py
==============
Main execution engine for the Cognitive-Access Testing Tool.
Executes static accessibility checks and optional Gemini-judged checks against input interaction files.
Supports:
  - Deterministic-only fallback when no GEMINI_API_KEY is configured.
  - Gemini LLM-judged evaluation when GEMINI_API_KEY is available in env or .env.
Outputs structured 3-tier diagnostic reports.
"""

import os
from .criteria.loader import CriteriaLoader
from .checks.prompt_check import PromptCheck
from .checks.diff_check import DiffCheck
from .checks.timeout_check import TimeoutCheck
from .checks.transparency_check import TransparencyCheck
from .checks.scope_check import ScopeCheck
from .checks.gemini_judge import GeminiJudge

class TestRunner:
    def __init__(self, mode="all"):
        self.mode = mode.lower()  # "all", "deterministic", or "gemini"
        self.loader = CriteriaLoader()
        self.prompt_check = PromptCheck(self.loader)
        self.diff_check = DiffCheck(self.loader)
        self.timeout_check = TimeoutCheck(self.loader)
        self.transparency_check = TransparencyCheck(self.loader)
        self.scope_check = ScopeCheck(self.loader)
        self.gemini_judge = GeminiJudge(self.loader)

    def run_tests(self, target_filepath):
        if not os.path.exists(target_filepath):
            raise FileNotFoundError(f"Target file not found: {target_filepath}")

        with open(target_filepath, "r", encoding="utf-8") as f:
            content = f.read()

        all_violations = []
        execution_notices = []

        # Parse conversation turns if present
        prompt_text = ""
        assistant_text = content
        if "[Developer]:" in content and "[Assistant]:" in content:
            parts = content.split("[Assistant]:", 1)
            prompt_text = parts[0].replace("[Developer]:", "").strip()
            assistant_text = parts[1].strip()
        elif "Prompt:" in content and "Response:" in content:
            parts = content.split("Response:", 1)
            prompt_text = parts[0].replace("Prompt:", "").strip()
            assistant_text = parts[1].strip()

        # 1. Deterministic Checks (Always available, zero-cost, offline)
        if self.mode in ["all", "deterministic"]:
            all_violations.extend(self.prompt_check.evaluate_prompt_transcript(content))
            
            if "-" in content or "+" in content:
                all_violations.extend(self.diff_check.evaluate_diff(content))
                
            all_violations.extend(self.timeout_check.evaluate_config(content))
            all_violations.extend(self.transparency_check.evaluate_ai_output(content))
            all_violations.extend(self.scope_check.evaluate_scope(prompt_text, assistant_text))

        # 2. Gemini LLM-Judged Checks (Free tier via GEMINI_API_KEY in env or .env)
        if self.mode in ["all", "gemini"]:
            if self.gemini_judge.has_api_key():
                judge_result = self.gemini_judge.evaluate_transcript(content)
                if judge_result.get("status") == "SUCCESS":
                    # Filter out duplicate rule IDs if already caught by deterministic checks
                    existing_rules = {v["rule_id"] for v in all_violations}
                    for v in judge_result.get("violations", []):
                        if v["rule_id"] not in existing_rules:
                            all_violations.append(v)
                else:
                    execution_notices.append(judge_result.get("message", "Gemini evaluation fell back to deterministic."))
            else:
                execution_notices.append(
                    "No GEMINI_API_KEY detected in env or .env file. Running in DETERMINISTIC-ONLY fallback mode."
                )

        # Format 3-tier diagnostic report
        report = {
            "target_file": target_filepath,
            "mode": self.mode,
            "gemini_active": self.gemini_judge.has_api_key() and self.mode in ["all", "gemini"],
            "execution_notices": execution_notices,
            "total_violations": len(all_violations),
            "high_severity_count": len([v for v in all_violations if v.get("severity") == "HIGH"]),
            "medium_severity_count": len([v for v in all_violations if v.get("severity") == "MEDIUM"]),
            "violations": all_violations
        }
        return report
