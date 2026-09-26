# SEL703 Professional Practice — Consolidated Logbook

**Student:** Harjot Singh  
**Placement:** Research Assistant (unpaid), under Dr. Davoud Mougouei, Deakin University  
**Placement start:** 7 July 2026  
**Hours target:** 225 (30 working days full-time equivalent)  
**Placement focus:** Operationalising cognitive accessibility and AI-governance standards (W3C COGA, WCAG 2.2, EU AI Act) for neurodivergent developers using LLM coding assistants through a 3-tier taxonomy (`guideline → cognitive concept → Schwartz value`) and a Python-based accessibility testing tool.

---

## Week 1 — 7 July – 13 July 2026

### Activities
- Attended kick-off meeting with supervisor Dr. Davoud Mougouei to confirm placement scope, hours requirement (225 hours), and core deliverables. Confirmed placement work would focus on operationalising cognitive accessibility and AI-governance standards into an actionable taxonomy mapping standards recommendations to Schwartz human values.
- Reviewed placement logistics: 225-hour requirement, portfolio deliverables (goal-setting doc, logbook, final report + exit interview), and the optional graded tasks (G1 social responsibility, G2 self-reflection and supervisor evaluation) required for higher grades.
- Reviewed W3C COGA "Making Content Usable for People with Cognitive and Learning Disabilities" as the primary standards source for extracting cognitive-accessibility design patterns applicable to LLM interaction. Identified the "predictable interfaces" pattern as directly relevant to reducing cognitive load during LLM-assisted development.
- Started an initial survey of related standards: WCAG 2.2 (ISO/IEC 40500:2025), EN 301 549, and the EU AI Act's provisions relevant to disabled/neurodivergent users, to build a candidate source list for the extraction task.

### Judgements and decisions made
- Decided to scope the placement's core deliverable around a **tool demonstration paper** (~4 pages, ICSE/ASE/FSE tool-demo track style) rather than a full empirical validation study, consistent with supervisor's guidance that real-user validation is deferred to future work.
- Decided the countermeasure taxonomy would use the Schwartz Theory of Basic Human Values as the foundational values framework.

### Reflection
- Placement activities over the first weeks consist exclusively of research, standards extraction, taxonomy mapping, prototype development, reporting, and supervisor meetings.
- Time management and maintaining steady progress across literature synthesis and tool prototyping is the primary focus.

### CPD activity
- Initial review of professional standards and workplace expectations for Research Assistant roles at Deakin University.

---

## Week 2 — 14 July – 20 July 2026

### Activities
- Created and committed initial repository scaffold for `sel703-placement` on GitHub (`2026-07-15`), organizing folders for documentation, logbooks, taxonomy mappings, and plugin/tool source code.
- Developed and committed `taxonomy/coga_extract.py` script for automated pattern extraction from W3C COGA standard.
- Generated raw candidate extraction pool of 27 patterns (`raw_extraction.json`) from W3C COGA across all 8 design objectives.
- Performed initial manual review of extractions on 15–16 July 2026, filtering pool to 7 verified COGA entries (`commit f74e0bb`, `22646e5`, `24bb012`).
- Expanded taxonomy to 10 entries by adding verbatim requirements from W3C WCAG 2.2 (SC 2.2.6, SC 3.3.4) and EU AI Act (Articles 13 & 14) (`commit feee98d`), achieving cross-standard grounding.
- Reviewed reference paper (Perera et al., IEEE RE 2019, DOI `10.1109/RE.2019.00053`) mapping GDPR rights to Schwartz human values as the methodological template.

### Judgements and decisions made
- Decided to keep initial taxonomy pool focused (~10 verified entries) to respect supervisor's half-day effort constraint rather than attempting exhaustive extraction.
- Decided to include full provenance fields (`source_standard`, `standard_section`, `source_url`, `section_url`) for all entries to ensure end-to-end traceability.
- Decided to enforce `verified_by_harjot: false` by default for all automated taxonomy scripts until manual human verification is completed.

### Reflection
- The extraction pipeline established a solid foundation across three independent standards.
- Realised that manual review is indispensable: raw LLM extractions occasionally propose forced or overlapping value mappings that must be refined by human judgement.

### CPD activity
- Reviewed Deakin's Placement Preparation Module content on professional communication and workplace ethics in preparation for logbook and reflection tasks throughout the placement.

---

## Week 3 — 21 July – 27 July 2026

### Dated Entry: Supervisor Meeting — 23 July 2026
- **Meeting Date:** 23 July 2026
- **Attendees:** Dr. Davoud Mougouei, Harjot Singh
- **Key Focus:** Review of initial taxonomy mapping (`mapping.json`) and discussion of deliverable scope. Supervisor feedback highlighted the requirement to introduce a formal three-tier mapping structure (`guideline → cognitive-science concept → Schwartz value`) to bridge standard recommendations with human values rigorously.
- *Note:* Detailed discussion points and meeting notes held offline by Harjot.

### Activities
- **Repository Evidence:** No git commits were recorded in the SEL703 placement repository during this calendar week. (Note: Supervisor meetings are periodic; 3 weeks elapsed between formal SEL703 discussions).
- Reviewed supervisor feedback from the 23 July meeting regarding the theoretical link between cognitive accessibility guidelines and Schwartz human values.
- Analyzed the methodological template (Perera et al., IEEE RE 2019) to understand how explicit vs. implicit value links are categorized and reported.
- Worked on standards extraction and literature review on executive dysfunction mechanisms (Working Memory Overload, Inhibition Deficit, Ambiguity Intolerance).

### Judgements and decisions made
- Agreed to pivot the theoretical framework of the taxonomy from a direct 2-tier mapping (`guideline → Schwartz value`) to a 3-tier structure (`guideline → cognitive concept → Schwartz value`) per supervisor instruction.
- Confirmed that SEL703 placement hours are dedicated strictly to placement research, development, reporting, literature review, and supervisor meetings.

### Reflection
- The supervisor meeting on 23 July clarified a crucial methodological requirement: jumping directly from UI guidelines to high-level Schwartz human values lacks psychological grounding unless mediated by established cognitive-science concepts (e.g., Working Memory Overload, Inhibition Deficit, Ambiguity Intolerance).
- Need to ensure all future taxonomy updates explicitly cite DOI-backed cognitive psychology literature for the middle tier.

### CPD activity
- Engaged in self-directed study on psychological frameworks of executive dysfunction (Barkley, Cowan, Monsell, Carleton) to prepare for middle-tier taxonomy mapping.

---

## Week 4 — 28 July – 3 August 2026

### Dated Entry: Supervisor Meeting — 31 July 2026
- **Meeting Date:** 31 July 2026
- **Attendees:** Dr. Davoud Mougouei, Harjot Singh
- **Key Focus:** Discussion on project framing and ICSE 2027 Demonstrations track submission strategy. Evaluated the distinction between an "enforcement plugin" (which requires user productivity studies out of scope for this placement) and an "accessibility testing tool" (which evaluates interface compliance deterministically without requiring empirical participant studies).
- *Note:* Detailed transcript records held offline by Harjot.

### Activities
- **Repository Evidence:** No git commits were recorded in the SEL703 placement repository during this calendar week.
- Evaluated deliverable framing: enforcement plugin vs. automated accessibility testing tool.
- Examined W3C COGA and WCAG 2.2 success criteria to evaluate how compliance checks can be formulated programmatically.
- Continued literature review on cognitive accessibility criteria and standards.

### Judgements and decisions made
- **Strategic Deliverable Pivot:** Formally pivoted placement deliverable from an "enforcement plugin" to a **Python-based cognitive accessibility testing tool**.
- Rationale: An enforcement plugin implies productivity benefits for neurodivergent developers (requiring human participant evaluation, which is out of scope). A testing tool reports interface violations against standards (demonstrable static/dynamic evaluation), matching ICSE Tool Demo track expectations without requiring a user study.
- Decided that the tool architecture will evaluate LLM coding assistant outputs/interfaces against the 3-tier taxonomy.

### Reflection
- The deliverable pivot decided in the 31 July meeting provides a much safer and stronger paper story for ICSE 2027 Demonstrations track.
- By framing the tool as a diagnostic tester (analogous to Accessibility Insights or axe-core, but for cognitive accessibility), we can evaluate real LLM assistant outputs deterministically.

### CPD activity
- Reviewed literature on automated accessibility evaluation tools (axe-core, Accessibility Insights) and demo track guidelines for ICSE/ASE.

---

## Week 5 — 4 August – 7 August 2026

### Activities
- **Repository Audit & Execution Setup:** Audited existing SEL703 placement codebase and taxonomy assets on 7 August 2026.
- Developed automated build script (`taxonomy/build_taxonomy_mapping.py`) to restructure `taxonomy/mapping.json` into the 3-tier schema (`guideline → cognitive concept → Schwartz value`).
- Resolved all quote text programmatically via lookup IDs (`concept_quote_id`) from the verified quote corpus (`quote_corpus_verified.json`), eliminating hand-typed quotes.
- Formulated standards extraction pipeline for verbatim text storage in `extractions/` (`w3c_coga.json`, `w3c_wcag22.json`, `eu_ai_act.json`).
- Drafted tool-demonstration paper outline (`docs/paper_outline.md`) targeting ICSE 2027 Demonstrations track.
- Formulated `tool/` testing tool prototype architecture in Python.

### Judgements and decisions made
- Decided to strictly enforce verbatim requirements in `extractions/` without paraphrasing to preserve auditability.
- Maintained `verified_by_harjot: false` by default across all taxonomy entries until explicit human verification is performed.
- Applied Perera et al. (IEEE RE 2019) Table I value definitions for all Schwartz human values (e.g., Security–Personal: "Safety in one's immediate environment.").
- Scoped the testing tool to evaluate LLM interface transcripts/prompts/outputs and report traceable chains (`Standard → Section → Cognitive Concept → Schwartz Value`).

### Reflection
- The realignment of tasks in Week 5 brings the placement back on track for the ICSE 2027 Demonstrations track paper draft.
- Programmatic quote resolution via lookup IDs ensures 100% sentence-level auditability against verified source papers.

### CPD activity
- Reviewed ICSE 2027 Tool Demonstrations call for papers requirements and reporting standards for theoretical tool demos.

---

*Logbook maintained on a weekly cadence. Next entry: Week 6 (8 – 14 August 2026).*
