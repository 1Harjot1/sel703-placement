"""
coga_extract.py
================
Task B: AI-assisted extraction of W3C COGA design patterns → Schwartz value mapping.

Source: W3C "Making Content Usable for People with Cognitive and Learning Disabilities"
        https://www.w3.org/TR/coga-usable/

Purpose: Produce a small (~5-10 pairs), manually verified taxonomy of:
  - Concrete actionable recommendation from COGA
  - Schwartz Basic Human Value it protects
  - Executive dysfunction it mitigates
  - One-line LLM/IDE operationalization idea

Per supervisor instruction: half-day cap. Target ~5-10 verified pairs, NOT exhaustive.
Output: mapping.json (verified) + extractions/raw_extraction.json (AI-proposed, unverified)

API: gpt-5.4-mini only (cheapest, good enough for extraction). Estimated cost < $0.01.
Key loaded from: f:/deakin_sem5/reasrach/code/VC/.env
"""

import json
import os
import asyncio
import time
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv(r"f:\deakin_sem5\reasrach\code\VC\.env")
client = AsyncOpenAI(api_key=os.environ["OPENAI_API_KEY"])

BASE = os.path.dirname(os.path.abspath(__file__))
TAXONOMY_DIR = os.path.join(BASE, "..", "taxonomy")
EXTRACTIONS_DIR = os.path.join(TAXONOMY_DIR, "extractions")
os.makedirs(EXTRACTIONS_DIR, exist_ok=True)

RAW_OUT = os.path.join(EXTRACTIONS_DIR, "raw_extraction.json")
VERIFIED_OUT = os.path.join(TAXONOMY_DIR, "mapping.json")
LOG_PATH = os.path.join(BASE, "..", "..", "VC", "pipeline", "api_usage_log.md")

EVAL_MODEL = "gpt-5.4-mini"

# ============================================================
# COGA OBJECTIVES — 8 sections with their design patterns
# Extracted manually from W3C COGA Table of Contents
# Source: https://www.w3.org/TR/coga-usable/
# ============================================================
COGA_OBJECTIVES = [
    {
        "objective_id": 1,
        "objective": "Help Users Understand What Things Are and How to Use Them",
        "patterns": [
            "Make the Purpose of Your Page Clear",
            "Use a Familiar Hierarchy and Design",
            "Use a Consistent Visual Design",
            "Make Each Step Clear",
            "Clearly Identify Controls and Their Use",
            "Make the Relationship Clear Between Controls and the Content They Affect",
            "Use Icons that Help the User"
        ]
    },
    {
        "objective_id": 2,
        "objective": "Help Users Find What They Need",
        "patterns": [
            "Make it Easy to Find the Most Important Tasks and Features",
            "Make the Site Hierarchy Easy to Understand and Navigate",
            "Use a Clear and Understandable Page Structure",
            "Make it Easy to Find the Most Important Actions and Information on the Page",
            "Break Media into Chunks",
            "Provide Search"
        ]
    },
    {
        "objective_id": 3,
        "objective": "Use Clear and Understandable Content",
        "patterns": [
            "Use Clear Words",
            "Use a Simple Tense and Voice",
            "Avoid Double Negatives or Nested Clauses",
            "Use Literal Language",
            "Keep Text Succinct",
            "Use Clear Unambiguous Formatting and Punctuation",
            "Include Symbols and Letters Necessary to Decipher the Words",
            "Provide Summary of Long Documents and Media",
            "Separate Each Instruction",
            "Use White Spacing",
            "Ensure Foreground Content is Not Obscured by Background",
            "Explain Implied Content",
            "Provide Alternatives for Numerical Concepts"
        ]
    },
    {
        "objective_id": 4,
        "objective": "Help Users Avoid Mistakes and Know How to Correct Them",
        "patterns": [
            "Ensure Controls and Content Do Not Move Unexpectedly",
            "Let Users Go Back",
            "Notify Users of Costs at Start of Task",
            "Design to Prevent Mistakes",
            "Make it Easy to Undo Errors",
            "Use Clear Visible Labels",
            "Use Clear Step-by-step Instructions",
            "Accept Different Input Formats",
            "Avoid Data Loss and Timeouts",
            "Provide Feedback",
            "Help the User Stay Safe",
            "Use Familiar Metrics and Units"
        ]
    },
    {
        "objective_id": 5,
        "objective": "Help Users Focus",
        "patterns": [
            "Limit Interruptions",
            "Make Short Critical Paths",
            "Avoid Too Much Content",
            "Provide Information So a User Can Complete and Prepare for a Task"
        ]
    },
    {
        "objective_id": 6,
        "objective": "Ensure Processes Do Not Rely on Memory",
        "patterns": [
            "Provide a Login that Does Not Rely on Memory or Other Cognitive Skills",
            "Allow the User a Simple Single Step Login",
            "Provide a Login Alternative with Less Words",
            "Let Users Avoid Navigating Voice Menus",
            "Do Not Rely on Users Calculations or Memorizing Information"
        ]
    },
    {
        "objective_id": 7,
        "objective": "Provide Help and Support",
        "patterns": [
            "Provide Human Help",
            "Provide Alternative Content for Complex Information and Tasks",
            "Clearly State the Results and Disadvantages of Actions Options and Selections",
            "Provide Help for Forms and Non-standard Controls",
            "Make It Easy to Find Help and Give Feedback",
            "Provide Help with Directions",
            "Provide Reminders"
        ]
    },
    {
        "objective_id": 8,
        "objective": "Support Adaptation and Personalization",
        "patterns": [
            "Let Users Control When the Content Moves or Changes",
            "Enable APIs and Extensions",
            "Support Simplification",
            "Support a Personalized and Familiar Interface"
        ]
    }
]

SCHWARTZ_VALUES = [
    "Self-Direction—Thought", "Self-Direction—Action", "Stimulation", "Hedonism",
    "Achievement", "Power—Dominance", "Power—Resources", "Face",
    "Security—Personal", "Security—Societal", "Tradition", "Conformity—Rules",
    "Conformity—Interpersonal", "Humility", "Benevolence—Dependability",
    "Benevolence—Caring", "Universalism—Concern", "Universalism—Nature",
    "Universalism—Tolerance"
]

EXECUTIVE_DYSFUNCTIONS = [
    "Working Memory Overload", "Inhibition Deficit", "Set-Shifting Cost",
    "Time Blindness", "Delay Aversion", "Ambiguity Intolerance",
    "Emotional Dysregulation", "Rejection Sensitivity", "Planning Deficit",
    "Cognitive Flexibility Deficit"
]

EXTRACTION_PROMPT = """You are a research assistant helping map W3C COGA (Web Content Accessibility Guidelines for Cognitive Disabilities) design patterns to Schwartz Theory of Basic Human Values, for the purpose of operationalizing accessibility requirements in LLM-assisted software development tools.

The W3C COGA standard objective is: "{objective}"

The specific design pattern is: "{pattern}"

Your task: Propose a mapping of this pattern to:
1. The most relevant Schwartz Basic Human Value it protects (pick ONE from the list below)
2. The executive dysfunction it primarily mitigates (pick ONE from the list below)
3. A one-line operationalization: how would this pattern manifest as a concrete LLM or AI coding assistant behavior?
4. A one-sentence justification for the Schwartz value mapping

Available Schwartz values: {schwartz_values}

Available executive dysfunctions: {dysfunctions}

Return ONLY a JSON object with exactly these fields:
{{
  "coga_objective": "{objective}",
  "coga_pattern": "{pattern}",
  "schwartz_value": "<exact value name from the list>",
  "executive_dysfunction": "<exact dysfunction name from the list>",
  "llm_operationalization": "<one sentence describing how an LLM coding assistant should implement this>",
  "value_mapping_justification": "<one sentence explaining why this Schwartz value is the right mapping>"
}}"""

api_log_entries = []

def log_call(model, purpose, approx_input_tokens, approx_output_tokens):
    api_log_entries.append({
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "model": model,
        "purpose": purpose,
        "approx_input_tokens": approx_input_tokens,
        "approx_output_tokens": approx_output_tokens
    })

async def extract_one(objective: str, pattern: str, sem) -> dict:
    prompt = EXTRACTION_PROMPT.format(
        objective=objective,
        pattern=pattern,
        schwartz_values=", ".join(SCHWARTZ_VALUES),
        dysfunctions=", ".join(EXECUTIVE_DYSFUNCTIONS)
    )
    async with sem:
        try:
            resp = await client.chat.completions.create(
                model=EVAL_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
                response_format={"type": "json_object"}
            )
            raw = resp.choices[0].message.content
            log_call(EVAL_MODEL, f"COGA extraction: {pattern[:40]}", len(prompt) // 4, len(raw) // 4)
            parsed = json.loads(raw)
            parsed["_extraction_status"] = "ai_proposed_unverified"
            return parsed
        except Exception as e:
            log_call(EVAL_MODEL, f"COGA extraction [ERROR]: {pattern[:40]}", 0, 0)
            return {
                "coga_objective": objective,
                "coga_pattern": pattern,
                "_extraction_status": "error",
                "_error": str(e)
            }

async def run_extraction():
    print("=" * 60)
    print("TASK B: SEL703 COGA -> Schwartz Value Extraction")
    print("=" * 60)
    print(f"Source: W3C COGA (8 objectives, 41 patterns)")
    print(f"Model: {EVAL_MODEL} (cheapest, appropriate for extraction)")
    print(f"Per supervisor: half-day cap, target 5-10 VERIFIED pairs only")
    print()

    sem = asyncio.Semaphore(10)
    all_tasks = []

    for obj in COGA_OBJECTIVES:
        for pattern in obj["patterns"]:
            all_tasks.append(extract_one(obj["objective"], pattern, sem))

    print(f"Sending {len(all_tasks)} extraction requests to {EVAL_MODEL}...")
    raw_results = await asyncio.gather(*all_tasks)

    # Save raw (unverified) results
    with open(RAW_OUT, "w", encoding="utf-8") as f:
        json.dump(raw_results, f, indent=2, ensure_ascii=False)

    successful = [r for r in raw_results if r.get("_extraction_status") == "ai_proposed_unverified"]
    errors = [r for r in raw_results if r.get("_extraction_status") == "error"]

    print(f"\nExtraction complete: {len(successful)} successful, {len(errors)} errors")
    print(f"Raw results saved to: {RAW_OUT}")
    print()

    # ============================================================
    # MANUAL VERIFICATION STEP
    # Print all proposed mappings for human review
    # Per brief: do NOT skip this step even under time pressure
    # ============================================================
    print("=" * 60)
    print("MANUAL VERIFICATION REQUIRED - review each mapping below")
    print("The verified pairs will be saved to mapping.json")
    print("=" * 60)
    print()

    # Show a preview of the first 15 mappings for quick review
    # (Full list is in raw_extraction.json for offline review)
    print("PREVIEW: First 15 AI-proposed mappings (full list in raw_extraction.json)")
    print("-" * 60)
    for i, r in enumerate(successful[:15], 1):
        print(f"{i:2}. [{r.get('coga_pattern', '?')}]")
        print(f"     -> Schwartz: {r.get('schwartz_value', '?')}")
        print(f"     -> Dysfunction: {r.get('executive_dysfunction', '?')}")
        print(f"     -> LLM: {r.get('llm_operationalization', '?')}")
        print()

    # For automated output: save the first 10 as the "candidate verified set"
    # NOTE: These MUST be manually reviewed before being presented as verified
    # Flag is set to "candidate_for_verification" not "verified"
    candidate_set = []
    for r in successful[:10]:
        r_copy = dict(r)
        r_copy["_extraction_status"] = "candidate_for_verification"
        r_copy["_verification_note"] = "MUST be manually reviewed before marking as verified"
        candidate_set.append(r_copy)

    with open(VERIFIED_OUT, "w", encoding="utf-8") as f:
        json.dump(candidate_set, f, indent=2, ensure_ascii=False)

    print()
    print(f"Candidate set (10 pairs, unverified) saved to: {VERIFIED_OUT}")
    print()
    print("WARNING - IMPORTANT: Before the meeting, open mapping.json and:")
    print("   1. Read each mapping critically")
    print("   2. Delete any that feel forced or unclear")
    print("   3. Change _extraction_status to 'verified' only for ones you'd defend")
    print("   4. Keep the rest as 'rejected' with a brief note why")
    print()
    print("Target: 5-10 verified pairs for the meeting. Quality > quantity.")
    print()

    # Save updated API log
    # Append to existing log if it exists
    existing_log = ""
    if os.path.exists(LOG_PATH):
        with open(LOG_PATH, "r", encoding="utf-8") as f:
            existing_log = f.read()

    new_entries = f"\n\n## Task B — COGA Extraction ({time.strftime('%Y-%m-%d')})\n\n"
    new_entries += "| Time | Model | Purpose | ~Input Tokens | ~Output Tokens |\n"
    new_entries += "|:---|:---|:---|---:|---:|\n"
    for e in api_log_entries:
        new_entries += f"| {e['timestamp']} | {e['model']} | {e['purpose']} | {e['approx_input_tokens']} | {e['approx_output_tokens']} |\n"
    total_in = sum(e['approx_input_tokens'] for e in api_log_entries)
    total_out = sum(e['approx_output_tokens'] for e in api_log_entries)
    new_entries += f"\n**Task B Total:** {total_in} input tokens, {total_out} output tokens\n"

    with open(LOG_PATH, "w", encoding="utf-8") as f:
        f.write(existing_log + new_entries)

    print(f"API usage log updated: {LOG_PATH}")
    print(f"Total Task B API calls: {len(api_log_entries)}")

if __name__ == "__main__":
    asyncio.run(run_extraction())
