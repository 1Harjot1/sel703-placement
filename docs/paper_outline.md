# ICSE 2027 Demonstrations Track — Paper Outline

**Title:** *Cognitive-Access: A 3-Tier Accessibility Testing Tool for LLM-Driven Assistant Interactions*  
**Authors:** Harjot Chauhan, Davoud Mougouei  
**Target Venue:** ICSE 2027 Tool Demonstrations Track (4 pages, double-blind / single-blind per track guidelines)

---

## Abstract
LLM-driven coding assistants (e.g., GitHub Copilot, Cursor) frequently generate dense code suggestions, bulk refactoring diffs, and unprompted deletions without structuring step-by-step guidance or providing transparent rationales. For neurodivergent developers—particularly those with ADHD and anxiety—these outputs induce working memory overload, executive dysfunction, and intolerance of uncertainty. In this demonstration, we present **Cognitive-Access**, an automated testing tool that evaluates LLM assistant interaction transcripts and code diffs against a 3-tier accessibility framework linking international standards (W3C COGA, WCAG 2.2, EU AI Act, EN 301 549) to cognitive-science mechanisms and Schwartz Human Values. The tool combines deterministic static checks with a fine-tuned 7B open-weight LLM judge (`Accessibility-Judge-LLM`) trained on real developer interaction logs.

---

## 1. Introduction & Motivation
- Background: Rapid adoption of AI coding assistants in software engineering.
- Problem Statement: Absence of cognitive accessibility standards in automated AI assistant testing.
- Novelty: Moving beyond physical accessibility (screen readers, color contrast) to cognitive accessibility grounded in empirical cognitive science.

---

## 2. 3-Tier Mapping Architecture
- **Tier 1 (Standards Layer):** W3C COGA (4.2.1, 4.2.4), WCAG 2.2 (SC 3.3.4, SC 2.2.6), EU AI Act (Art 13, Art 14), EN 301 549 (Cl 11.7).
- **Tier 2 (Cognitive-Science Layer):** Grounded in empirical literature:
  - Working Memory Capacity (Cowan 2001, $4 \pm 1$ chunks)
  - Intolerance of Uncertainty (Carleton 2006)
  - Executive Function & Inhibition Deficits (Barkley 1997)
  - Time Perception & Time Blindness (Smith et al. 2002)
- **Tier 3 (Schwartz Human Values Layer):** Mapping accessibility outcomes to universal human values (*Security-Personal*, *Self-Direction-Thought*).
- **Document Identity:** Primary keys enforced by printed PDF page 1 titles rather than unverified API metadata.

---

## 3. System Architecture & Fine-Tuned Accessibility Judge Model
- **Deterministic Static Checks (`[DETERMINISTIC]`):** RegEx and AST parsers for unbuffered bulk deletions (`WCAG-3.3.4-INHIB`) and unannounced timeouts (`WCAG-2.2.6-TIME`).
- **Fine-Tuned Judge Model (`[LLM_JUDGED]`):**
  - Fine-tuning dataset formatted from real developer interaction transcripts (`fine_tuning/train.jsonl`, `val.jsonl`).
  - QLoRA fine-tuning on Qwen 2.5 7B / Llama 3.1 8B (`fine_tuning/train_lora.py`).
  - Local inference integration in `tool/checks/finetuned_judge.py`.

---

## 4. Evaluation & Benchmark Results
- Benchmark Dataset: 20 genuine developer transcripts collected from Stack Overflow (`benchmark/transcripts/`).
- Metric Reporting: Precision, Recall, $F_1$-score across deterministic and LLM-judged criteria.
- Empirical Failure Mode Analysis: Discussion of boundary false positives on raw stack trace logs.

---

## 5. Tool Demonstration & User Flow
- CLI execution walkthrough with `python -m tool.cli --target <transcript>`.
- Visualization of 3-tier traceability output in terminal logs.
- GitHub Action integration for CI/CD pipelines.

---

## 6. Conclusion & Future Work
- Summary of contributions.
- Video demonstration link and open-source repository link (`github.com/1HarryChauhan/sel703-placement`).
