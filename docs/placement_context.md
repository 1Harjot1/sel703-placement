# Placement Context & Infrastructure Reuse (SEL703 vs. SIT723)

This document makes the institutional framing and reuse of this codebase explicit, defensible, and transparent.

---

## 1. Distinct Academic Functions

| Dimension | SEL703 Placement Unit | SIT723 Research Project |
|:---|:---|:---|
| **Primary Assessment** | Research Assistant Competency & Technical Engineering | Independent Research Contribution & Findings |
| **Deliverable Focus** | Reusable infrastructure, verifiable test suites, interactive tooling, and rigorous documentation | Empirical dataset, statistical findings, qualitative taxonomy, and publication manuscript |
| **Core Evaluation** | Can the student engineer, verify, package, and document research tools for other researchers to use? | Did the research advance the state of the art in cognitive accessibility for software engineering? |
| **Supervisory Guidance** | Focused on development, testing, and packaging | Focused on research methodology and paper writing |

---

## 2. Provenance & Packaging Rationale

1. **Original Engineering Context:**  
   This generation pipeline was originally engineered during the research assistant placement to support the scenario-generation and citation-verification requirements of the **SIT723** project on cognitive accessibility in AI coding assistants.

2. **Why It Is Packaged Under SEL703:**  
   SEL703 explicitly assesses the ability to deliver production-grade research engineering: building clean pipelines, writing reproducible test harnesses, preventing hallucinated data through structural design, and authoring exhaustive technical documentation. Documenting and packaging this infrastructure directly demonstrates research-assistant competency without claiming a second independent research finding.

3. **Where Findings Are Reported:**  
   The empirical research findings, qualitative themes, and statistical analyses belong strictly to **SIT723** and are reported in the SIT723 research manuscript.

---

## 3. What is Unique to the SEL703 Packaging

The standalone packaging contains substantial engineering created specifically for this placement deliverable:
- **Interactive CLI Wizard (`ui/wizard.py`):** An accessible, zero-friction interface enabling external researchers to configure dimensions, run generations, and inspect grounded psychology citations without reading source code.
- **Automated Verification Test Suite (`tests/`):** 15 unit tests verifying provenance gating, regex word-boundary label checks, quote-first lookup, and cross-domain standards.
- **Decoupled Architecture & Schema:** Modular separation of concerns across `corpus_loader`, `verifier`, `generator`, `rater`, and `filter`.
- **Word-Boundary Bug Remediation:** Identifying and documenting the substring match false positive on `"interface"` and fixing it in `src/verifier.py`.
- **Cross-Domain Demonstration (`examples/cross_domain_demo/`):** Demonstrating zero-shot domain transfer by applying the pipeline architecture to international regulatory and accessibility standards (W3C COGA, WCAG 2.2, EU AI Act) with 14 compliance scenarios passing deterministic checks at 100.0%.
