# SEL703 Professional Practice — Week 4 Logbook

**Student:** Harjot Singh  
**Placement:** Research Assistant (unpaid), under Dr. Davoud Mougouei, Deakin University  
**Period:** 28 July – 3 August 2026  

---

## Dated Entry: Supervisor Meeting — 31 July 2026

- **Meeting Date:** 31 July 2026
- **Attendees:** Dr. Davoud Mougouei, Harjot Singh
- **Key Focus:** Discussion on project framing and ICSE 2027 Demonstrations track submission strategy. Evaluated the distinction between an "enforcement plugin" (which requires user productivity studies out of scope for this placement) and an "accessibility testing tool" (which evaluates interface compliance deterministically without requiring empirical participant studies).
- *Note:* Detailed transcript records held offline by Harjot.

## Activities

- **Repository Evidence:** No git commits were recorded in the SEL703 placement repository during this calendar week.
- Evaluated deliverable framing: enforcement plugin vs. automated accessibility testing tool.
- Examined W3C COGA and WCAG 2.2 success criteria to evaluate how compliance checks can be formulated programmatically.
- Continued literature review on cognitive accessibility criteria and standards.

## Judgements and decisions made

- **Strategic Deliverable Pivot:** Formally pivoted placement deliverable from an "enforcement plugin" to a **Python-based cognitive accessibility testing tool**.
- Rationale: An enforcement plugin implies productivity benefits for neurodivergent developers (requiring human participant evaluation, which is out of scope). A testing tool reports interface violations against standards (demonstrable static/dynamic evaluation), matching ICSE Tool Demo track expectations without requiring a user study.
- Decided that the tool architecture will evaluate LLM coding assistant outputs/interfaces against the 3-tier taxonomy.

## Reflection

- The deliverable pivot decided in the 31 July meeting provides a much safer and stronger paper story for ICSE 2027 Demonstrations track.
- By framing the tool as a diagnostic tester (analogous to Accessibility Insights or axe-core, but for cognitive accessibility), we can evaluate real LLM assistant outputs deterministically.

## CPD activity

- Reviewed literature on automated accessibility evaluation tools (axe-core, Accessibility Insights) and demo track guidelines for ICSE/ASE.
