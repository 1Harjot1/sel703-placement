"""
generator.py — Quote-Selection-Before-Writing Prompt Harness & Generation Engine
================================================================================
Implements Stage 1 (Input Grid) and Stage 3 (Quote-First Generation):
- Populates grid combos: Dysfunction x Behavior, rotated across SDLC tasks and values.
- Injects numbered candidate sentences [s1] ... [s10] into prompt context.
- Requires model to select citation_doi and quote_id before generating scenario prose.
- Supports live LLM execution (OpenAI/Gemini) or offline authentic benchmark replay.
"""

import json
import os
import random
from pathlib import Path
from typing import Dict, Any, List, Optional
import pandas as pd

SYSTEM_PROMPT_TEMPLATE = """You are an expert empirical researcher evaluating cognitive accessibility in AI-assisted software engineering.
Generate an authentic developer scenario where a coding assistant behavior triggers a cognitive accessibility barrier for a neurodivergent software developer.

CONSTRAINTS & RULES:
1. Grounding-First: You MUST select an available sentence from the provided psychology reference paper. Set 'citation_doi' to the paper's DOI and 'quote_id' to the chosen sentence ID (e.g., 's10').
2. The scenario MUST be language-agnostic: NEVER mention specific programming languages (Python, Java, etc.) or frameworks.
3. NEVER use corporate buzzwords ('seamlessly', 'robust', 'paradigm', 'innovative').
4. Return ONLY a valid JSON object matching the required schema.

REQUIRED JSON SCHEMA:
{
  "summary": "Brief 1-2 sentence overview of the barrier",
  "full_scenario": "Detailed first-person narrative of the developer workflow, interaction, and mechanism",
  "impact": "Concrete software engineering consequence",
  "reasoning": "Why a developer with this cognitive profile experiences this barrier vs a neurotypical developer",
  "intervention": "Actionable tool feature or design remediation",
  "value_violated": "Human value implicated from Schwartz taxonomy",
  "behaviour": "{{LLM_BEHAVIOR_NAME}}",
  "citation_doi": "{{CITATION_DOI}}",
  "quote_id": "{{QUOTE_ID}}"
}
"""

def build_prompt_payload(combo: Dict[str, Any], corpus: Dict[str, Any], candidate_sentences: Dict[str, str], doi: str) -> Dict[str, str]:
    dys = combo["dysfunction"]
    beh = combo["behavior"]
    sdlc = combo["sdlc"]
    val = combo["value"]

    sentences_block = "\n".join([f"  * [{sid}] \"{txt}\"" for sid, txt in candidate_sentences.items()])
    if not sentences_block:
        sentences_block = "  [No pre-filtered candidate sentences available for this paper]"

    user_instructions = f"""--- SCENARIO SPECIFICATION ---
- Executive Dysfunction: {dys.get('name')}
  Mechanism: {dys.get('mechanism_text')}
- AI Assistant Behavior: {beh.get('name')}
  Description: {beh.get('description')}
- SDLC Task: {sdlc.get('full_name', sdlc.get('task_name'))}
- Schwartz Human Value Threatened: {val.get('name')}

--- AVAILABLE PSYCHOLOGY EVIDENCE (Select one quote_id and citation_doi) ---
Paper DOI: {doi}
Available Sentences:
{sentences_block}

Task: Write the scenario choosing one specific sentence [sX] above as your quote_id.
"""
    return {
        "system": SYSTEM_PROMPT_TEMPLATE.replace("{{LLM_BEHAVIOR_NAME}}", beh.get("name", "")),
        "user": user_instructions
    }

def generate_scenario_offline(combo: Dict[str, Any], data_dir: Path) -> Dict[str, Any]:
    """
    Offline authentic scenario provider:
    Retrieves an authentic validated scenario from final_180.csv matching the grid combo,
    ensuring 100% deterministic reproducibility without requiring external API keys.
    """
    csv_path = data_dir / "final_180.csv"
    if not csv_path.exists():
        raise FileNotFoundError(f"final_180.csv not found at: {csv_path}")

    df = pd.read_csv(csv_path)
    dys_name = combo["dysfunction"].get("name", "").lower()
    beh_name = combo["behavior"].get("name", "").lower()

    # Search for matching scenario in final_180.csv
    match = df[(df["dysfunction"].str.lower() == dys_name) & (df["behavior"].str.lower() == beh_name)]
    if match.empty:
        match = df[df["dysfunction"].str.lower() == dys_name]
    if match.empty:
        match = df.iloc[[0]]

    row = match.iloc[0]
    return {
        "sid": row["sid"],
        "summary": row["concern"],
        "full_scenario": row["logic"],
        "impact": row["impact"],
        "reasoning": row["logic"],
        "intervention": row["intervention"],
        "value_violated": row["value_item"],
        "behaviour": row["behavior"],
        "citation_doi": row["citation_doi"],
        "quote_id": row["quote_id"],
        "evidence": row["evidence"],
        "relevance": row["relevance"],
        "plausibility": row["plausibility"],
        "specificity": row["specificity"]
    }

def generate_scenario_live(combo: Dict[str, Any], corpus: Dict[str, Any], candidate_sentences: Dict[str, str], doi: str) -> Dict[str, Any]:
    """
    Live generation using OpenAI or Google Gemini if API key is present in environment.
    Falls back to offline generator if no API key is set.
    """
    api_key_openai = os.getenv("OPENAI_API_KEY")
    api_key_gemini = os.getenv("GEMINI_API_KEY")

    if not api_key_openai and not api_key_gemini:
        print("[GENERATOR] No API key detected (OPENAI_API_KEY or GEMINI_API_KEY). Using authentic offline benchmark engine.")
        data_dir = Path(__file__).parent / "data"
        return generate_scenario_offline(combo, data_dir)

    payload = build_prompt_payload(combo, corpus, candidate_sentences, doi)

    if api_key_openai:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=api_key_openai)
            resp = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": payload["system"]},
                    {"role": "user", "content": payload["user"]}
                ],
                response_format={"type": "json_object"},
                temperature=0.7
            )
            content = resp.choices[0].message.content
            return json.loads(content)
        except Exception as e:
            print(f"[GENERATOR WARNING] OpenAI generation failed ({e}). Falling back to offline authentic exemplar.")
            data_dir = Path(__file__).parent / "data"
            return generate_scenario_offline(combo, data_dir)

    # Gemini fallback
    if api_key_gemini:
        try:
            import urllib.request
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key_gemini}"
            prompt_text = payload["system"] + "\n\n" + payload["user"] + "\n\nReturn JSON only."
            req_data = json.dumps({"contents": [{"parts": [{"text": prompt_text}]}]}).encode("utf-8")
            req = urllib.request.Request(url, data=req_data, headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=15) as r:
                res = json.loads(r.read().decode("utf-8"))
                text = res["candidates"][0]["content"]["parts"][0]["text"]
                # Clean code fences
                text = text.replace("```json", "").replace("```", "").strip()
                return json.loads(text)
        except Exception as e:
            print(f"[GENERATOR WARNING] Gemini generation failed ({e}). Falling back to offline authentic exemplar.")
            data_dir = Path(__file__).parent / "data"
            return generate_scenario_offline(combo, data_dir)
