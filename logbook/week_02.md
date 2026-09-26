# SEL703 Professional Practice — Week 2 Logbook

**Student:** Harjot Singh  
**Placement:** Research Assistant (unpaid), under Dr. Davoud Mougouei, Deakin University  
**Period:** 14 July – 20 July 2026  

---

## Activities

- Created and committed initial repository scaffold for `sel703-placement` on GitHub (`2026-07-15`), organizing folders for documentation, logbooks, taxonomy mappings, and plugin/tool source code.
- Developed and committed `taxonomy/coga_extract.py` script for automated pattern extraction from W3C COGA standard.
- Generated raw candidate extraction pool of 27 patterns (`raw_extraction.json`) from W3C COGA across all 8 design objectives.
- Performed initial manual review of extractions on 15–16 July 2026, filtering pool to 7 verified COGA entries (`commit f74e0bb`, `22646e5`, `24bb012`).
- Expanded taxonomy to 10 entries by adding verbatim requirements from W3C WCAG 2.2 (SC 2.2.6, SC 3.3.4) and EU AI Act (Articles 13 & 14) (`commit feee98d`), achieving cross-standard grounding.
- Reviewed reference paper (Perera et al., IEEE RE 2019, DOI `10.1109/RE.2019.00053`) mapping GDPR rights to Schwartz human values as the methodological template.

## Judgements and decisions made

- Decided to keep initial taxonomy pool focused (~10 verified entries) to respect supervisor's half-day effort constraint rather than attempting exhaustive extraction.
- Decided to include full provenance fields (`source_standard`, `standard_section`, `source_url`, `section_url`) for all entries to ensure end-to-end traceability.
- Decided to enforce `verified_by_harjot: false` by default for all automated taxonomy scripts until manual human verification is completed.

## Reflection

- The extraction pipeline established a solid foundation across three independent standards.
- Realised that manual review is indispensable: raw LLM extractions occasionally propose forced or overlapping value mappings that must be refined by human judgement.

## CPD activity

- Reviewed Deakin's Placement Preparation Module content on professional communication and workplace ethics in preparation for logbook and reflection tasks throughout the placement.
