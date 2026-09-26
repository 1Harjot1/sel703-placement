# SEL703 Professional Practice — Week 5 Logbook

**Student:** Harjot Singh  
**Placement:** Research Assistant (unpaid), under Dr. Davoud Mougouei, Deakin University  
**Period:** 4 August – 7 August 2026  

---

## Activities

- **Repository Audit & Execution Setup:** Audited existing SEL703 placement codebase and taxonomy assets on 7 August 2026.
- Developed automated build script (`taxonomy/build_taxonomy_mapping.py`) to restructure `taxonomy/mapping.json` into the 3-tier schema (`guideline → cognitive concept → Schwartz value`).
- Resolved all quote text programmatically via lookup IDs (`concept_quote_id`) from the verified quote corpus (`quote_corpus_verified.json`), eliminating hand-typed quotes.
- Formulated standards extraction pipeline for verbatim text storage in `extractions/` (`w3c_coga.json`, `w3c_wcag22.json`, `eu_ai_act.json`).
- Drafted tool-demonstration paper outline (`docs/paper_outline.md`) targeting ICSE 2027 Demonstrations track.
- Formulated `tool/` testing tool prototype architecture in Python.

## Judgements and decisions made

- Decided to strictly enforce verbatim requirements in `extractions/` without paraphrasing to preserve auditability.
- Maintained `verified_by_harjot: false` by default across all taxonomy entries until explicit human verification is performed.
- Applied Perera et al. (IEEE RE 2019) Table I value definitions for all Schwartz human values (e.g., Security–Personal: "Safety in one's immediate environment.").
- Scoped the testing tool to evaluate LLM interface transcripts/prompts/outputs and report traceable chains (`Standard → Section → Cognitive Concept → Schwartz Value`).

## Reflection

- The realignment of tasks in Week 5 brings the placement back on track for the ICSE 2027 Demonstrations track paper draft.
- Programmatic quote resolution via lookup IDs ensures 100% sentence-level auditability against verified source papers.

## CPD activity

- Reviewed ICSE 2027 Tool Demonstrations call for papers requirements and reporting standards for theoretical tool demos.
