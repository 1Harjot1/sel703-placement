# SEL703 Professional Practice — Placement Repository
**Student:** Harjot Singh  
**Supervisor:** Dr. Davoud Mougouei  
**Placement Start:** 7 July 2026  
**Placement Focus:** Operationalizing accessibility standards (W3C COGA, WCAG 2.2) and AI-governance standards (EU AI Act) for neurodivergent developers using LLM coding assistants.

---

## Repository Structure

- `docs/` — Methodology documents, design specifications, and the draft of the tool-demo paper.
- `logbook/` — Weekly placement logbook entries and supervisor sign-offs.
- `plugin/` — Source code for the IDE plugin prototype.
- `references/` — PDF copies of source accessibility standards and cited research papers.
- `taxonomy/` — The verified countermeasure mapping mapping COGA recommendations to Schwartz values.

---

## Quick Start

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Set up environment:
   Configure your OpenAI API key in `VC/.env`.
3. Run the COGA extraction pipeline:
   ```bash
   cd taxonomy
   python coga_extract.py
   ```
