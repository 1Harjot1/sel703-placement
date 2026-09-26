# Placement Context & Engineering Infrastructure (SEL703)

This document describes the engineering objectives, scope, and technical infrastructure delivered during the research assistant placement.

---

## 1. Placement Scope & Engineering Objectives

- **Placement Unit:** SEL703 Professional Practice (School of Information Technology, Deakin University)
- **Role:** Research Assistant
- **Supervisor:** Dr. Davoud Mougouei
- **Focus:** Research software engineering, deterministic verification pipelines, and reusable tooling infrastructure.

The core objective of this placement was to design, implement, and validate a production-grade scenario generation and verification pipeline capable of producing structurally grounded, citation-verified benchmarks without hallucination.

---

## 2. Infrastructure Provenance & Packaging Rationale

1. **Engineering Context:**  
   The scenario generation pipeline was developed during the placement to solve structural reliability challenges in LLM-assisted benchmark synthesis, specifically preventing citation hallucinations, buzzword contamination, and sampling skew.

2. **Placement Deliverable Focus:**  
   SEL703 assesses the capacity to engineer robust, maintainable, and reusable software systems:
   - Constructing decoupled, modular pipeline components (`corpus_loader`, `verifier`, `generator`, `rater`, `filter`).
   - Enforcing deterministic static verification with zero tolerance for silent errors.
   - Creating comprehensive unit test regression suites.
   - Demonstrating zero-shot cross-domain reusability across international regulatory standards.
   - Providing accessible interactive interfaces for researchers and evaluators.

---

## 3. Core Technical Contributions Packaged in This Repository

- **Interactive CLI Wizard (`ui/wizard.py`):** An accessible, zero-friction interface enabling researchers to configure dimensions, run generations, and inspect grounded citations without writing custom scripts.
- **Automated Verification Test Suite (`tests/`):** 15 unit tests covering provenance gating, regex word-boundary label checks, quote-first lookup, and cross-domain standards.
- **Decoupled Architecture & Schema:** Clean modular separation across `corpus_loader`, `verifier`, `generator`, `rater`, and `filter`.
- **Word-Boundary Bug Remediation:** Identifying and documenting the substring match false positive on `"interface"` (`SCN-0176`, `SCN-0451`) and resolving it via word boundaries (`\bface\b`) in `src/verifier.py`.
- **Cross-Domain Transfer Proof (`examples/cross_domain_demo/`):** Demonstrating general-purpose reusability by transferring the pipeline to international regulatory and accessibility standards (W3C COGA, WCAG 2.2, EU AI Act), achieving a 14/14 (100.0%) deterministic pass rate.
