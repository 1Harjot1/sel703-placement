# Step-by-Step Usage Guide

This guide provides practical instructions for setting up, configuring, running, verifying, and evaluating scenarios using the `sel703-placement` pipeline.

Every command in this document was executed live on the system, and the console output is included verbatim below.

---

## 1. Environment Setup

The pipeline requires Python 3.10+ and standard data processing libraries.

```bash
git clone https://github.com/1HarryChauhan/sel703-placement.git
cd sel703-placement
pip install -r requirements.txt
```

### Verified Live Output:
```text
Requirement already satisfied: pandas>=2.0.0 in c:\python312\lib\site-packages (2.2.2)
Requirement already satisfied: openai>=1.0.0 in c:\python312\lib\site-packages (1.40.0)
```

---

## 2. Configuration & Execution Modes

The pipeline supports both **Live LLM Execution** (OpenAI `gpt-4o-mini` or Google Gemini `gemini-1.5-flash`) and **Authentic Offline Benchmark Replay**.

### Option A: Live API Execution (Optional)
If you wish to trigger live API calls, set the corresponding environment variable:

- **On Linux / macOS:**
  ```bash
  export OPENAI_API_KEY="sk-..."
  # or
  export GEMINI_API_KEY="AIzaSy..."
  ```
- **On Windows PowerShell:**
  ```powershell
  $env:OPENAI_API_KEY = "sk-..."
  # or
  $env:GEMINI_API_KEY = "AIzaSy..."
  ```

### Option B: Authentic Offline Benchmark Replay (Default / Recommended)
If no API key is detected in the environment, the generation harness automatically activates the **authentic offline engine**. In this mode:
- It samples verified prompt payloads and grounded citations from `src/data/final_180.csv`.
- It executes all Stage 4 deterministic checks, Stage 5 nominal scoring, and Stage 6 retention calculations.
- Execution is 100% deterministic, offline, and zero-cost.

---

## 3. Running Automated Unit Tests

Execute the 15-test unit suite verifying provenance gating, deterministic checks, quote-first templating, and cross-domain standards:

```bash
python -m unittest discover -s tests -v
```

### Verified Live Output:
```text
test_get_candidate_sentences (test_corpus_loader.TestCorpusLoader.test_get_candidate_sentences) ... ok
test_load_taxonomies (test_corpus_loader.TestCorpusLoader.test_load_taxonomies) ... ok
test_provenance_gate (test_corpus_loader.TestCorpusLoader.test_provenance_gate) ... ok
test_banned_words_rejection (test_cross_domain.TestCrossDomain.test_banned_words_rejection) ... ok
test_cross_domain_scenarios_count (test_cross_domain.TestCrossDomain.test_cross_domain_scenarios_count) ... ok
test_load_standards_corpus (test_cross_domain.TestCrossDomain.test_load_standards_corpus) ... ok
test_verify_all_14_scenarios_pass (test_cross_domain.TestCrossDomain.test_verify_all_14_scenarios_pass) ... ok
test_build_prompt_payload (test_generator.TestGenerator.test_build_prompt_payload) ... ok
test_offline_generation (test_generator.TestGenerator.test_offline_generation) ... ok
test_banned_words (test_verifier.TestVerifier.test_banned_words) ... ok
test_full_scenario_verification (test_verifier.TestVerifier.test_full_scenario_verification) ... ok
test_no_label_leakage_word_boundaries (test_verifier.TestVerifier.test_no_label_leakage_word_boundaries) ... ok
test_no_language_names (test_verifier.TestVerifier.test_no_language_names) ... ok
test_quote_verification_quote_id (test_verifier.TestVerifier.test_quote_verification_quote_id) ... ok
test_schema_completeness (test_verifier.TestVerifier.test_schema_completeness) ... ok

----------------------------------------------------------------------
Ran 15 tests in 0.319s

OK
```

---

## 4. Running the Interactive CLI Wizard

### A. Psychology & Cognitive Accessibility Domain (Demo Mode)
```bash
python ui/wizard.py --demo --domain psychology
```

#### Verified Live Output:
```text
============================================================================
 SEL703 / SIT723: GENERAL-PURPOSE SCENARIO GENERATION PIPELINE 
 Mode: COGNITIVE ACCESSIBILITY & EXECUTIVE DYSFUNCTION DOMAIN 
 Grounded Quote-Selection-Before-Writing Interface 
============================================================================

[1/4] Loading taxonomies and verified psychology reference corpus...
       Loaded 8 dysfunctions, 10 behaviors, 43 verified papers.

--- SELECT EXECUTIVE DYSFUNCTION ---
  [1] Working Memory Overload
  [2] Delay Aversion
  [3] Set-Shifting Cost
  [4] Rejection Sensitivity
  [5] Ambiguity Intolerance
  [6] Inhibition Deficit
  [7] Time Blindness
  [8] Emotional Dysregulation
Demo mode auto-selected: [1] Working Memory Overload

--- SELECT AI ASSISTANT BEHAVIOR ---
  [1] Non-deterministic Output
  [2] Hallucination with High Confidence
  [3] Context Window Truncation
  [4] Instruction Non-Adherence
  [5] Sycophantic Capitulation
  [6] Unstructured Output
  [7] Ambiguous Multi-Option Output
  [8] Critical Tone in Correction
  [9] Silent Context Reset
  [10] Scope Creep in Generation
Demo mode auto-selected: [1] Non-deterministic Output

[2/4] Configured Generation Cell:
      - Executive Dysfunction : Working Memory Overload
      - AI Assistant Behavior : Non-deterministic Output
      - SDLC Context          : Requirements analysis and evaluation
      - Schwartz Human Value  : Self-Direction—Thought

[3/4] Running Quote-First Generation...
[GENERATOR] No API key detected (OPENAI_API_KEY or GEMINI_API_KEY). Using authentic offline benchmark engine.

============================================================================
 GENERATED SCENARIO & GROUNDING VERIFICATION CARD 
============================================================================
Scenario ID   : SCN-0041
Summary       : A developer sorting requirement statements asked the coding assistant for classification help, but identical prompts produced different category schemes each time. Because they rely on a small active mental buffer, comparing all versions displaced the original rules, making the work feel unsafe and forcing a restart.

Full Narrative:
I was sorting a backlog of raw requirement statements into functional, quality, access-control, and domain-specific groups before a planning review. I asked the coding assistant to classify the same ten items and explain the boundary rules so I could apply them consistently. When I ran the identical request again, it changed several labels, renamed two groups, and gave a different rule for the same access-control item. I kept trying to hold the first answer, the second answer, the team rubric, and the disputed examples in mind, then lost track of which rule I trusted and delayed the review notes. This fits research showing that accuracy and speed drop when too many separate items must be kept active at once. A developer without this cognitive sensitivity would likely compare the two outputs, pick the rule that matches the team rubric, and continue with a short correction note. Here, more than three changing elements compete for a small active mental buffer, so earlier rules and examples are displaced before they can be checked. The repeated inconsistent answers turn a linear classification task into a multi-version reconciliation task, breaking the workflow at the point where stable criteria are needed.

Impact        : The developer cannot stabilize the category rules long enough to classify the requirements, so the review packet is delayed and extra time is spent rebuilding a trusted decision table from scratch.
Intervention  : The tool should pin a single classification rubric for the session and show any later change as a highlighted difference that requires explicit approval before replacing prior guidance.
----------------------------------------------------------------------------
 GROUNDED PSYCHOLOGY CITATION (STAGE 3 PROVENANCE) 
DOI           : 10.1017/s0140525x01003922
Quote ID      : [s68]
Verbatim Quote: "This results in markedly less accurate and/or slower performance when more than four items must be held than when fewer items must be held (e.g., in enumeration tasks such as that dis- cussed by Mandler & Shebo 1982)."
----------------------------------------------------------------------------
 DETERMINISTIC VERIFICATION (STAGE 4 CHECKS) 
Overall Pass  : [PASS]
  - Schema Completeness     : PASS
  - Banned Buzzwords Check  : PASS
  - No Programming Languages: PASS
  - No Label Leakage        : PASS
  - Verbatim Quote Match    : PASS
  - DOI Format & Resolution : PASS
----------------------------------------------------------------------------
 NOMINAL RATINGS (STAGE 5 ANCHORS) 
  - Relevance    : Supported (Evidence-based Interpretive Distance)
  - Plausibility : Likely (Operational Likelihood)
  - Specificity  : Specific (Level of Concrete Detail)
============================================================================

[4/4] Pipeline Retention Summary:
  - Final Ground-Truth Dataset: 180 scenarios
    * Deterministic Pass Rate : 180/180 (100.0%)
    * Relevance Breakdown     : {'Partial': 104, 'Supported': 67, 'Doubtful': 9}
  - Upstream Generation Pool  : 1000 scenarios generated across grid
    * Deterministic Pass      : 990 / 1000 (99.0%)
    * High-Quality Retained   : 291 / 1000 (29.1%)

Wizard execution complete.
```

---

### B. Regulatory & Standards Domain (Cross-Domain Transfer Demo)
```bash
python ui/wizard.py --demo --domain standards
```

#### Verified Live Output:
```text
============================================================================
 SEL703 / SIT723: GENERAL-PURPOSE SCENARIO GENERATION PIPELINE 
 Mode: REGULATORY & ACCESSIBILITY STANDARDS (CROSS-DOMAIN REUSABILITY) DOMAIN 
 Grounded Quote-Selection-Before-Writing Interface 
============================================================================

[1/4] Ingesting verified international accessibility & regulatory standards...
       Loaded 11 standards across W3C COGA, W3C WCAG 2.2, and EU AI Act.

--- SELECT REGULATORY STANDARD / DIRECTIVE ---
  [1] W3C-COGA-4.1.1: W3C Cognitive Accessibility (COGA) — Pattern 4.1.1 — Use Clear Controls
  [2] W3C-COGA-4.2.1: W3C Cognitive Accessibility (COGA) — Pattern 4.2.1 — Make the Purpose of Your Page Clear
  [3] W3C-COGA-4.2.4: W3C Cognitive Accessibility (COGA) — Pattern 4.2.4 — Make Each Step Clear
  [4] W3C-COGA-4.3.1: W3C Cognitive Accessibility (COGA) — Pattern 4.3.1 — Use Clear and Simple Language
  [5] W3C-COGA-4.5.2: W3C Cognitive Accessibility (COGA) — Pattern 4.5.2 — Provide Chunked Information
  [6] W3C-WCAG-2.2.1: W3C Web Content Accessibility Guidelines (WCAG 2.2) — Success Criterion 2.2.1 — Timing Adjustable
  [7] W3C-WCAG-3.3.4: W3C Web Content Accessibility Guidelines (WCAG 2.2) — Success Criterion 3.3.4 — Error Prevention (Data)
  [8] W3C-WCAG-3.3.7: W3C Web Content Accessibility Guidelines (WCAG 2.2) — Success Criterion 3.3.7 — Redundant Entry
  [9] W3C-WCAG-3.3.8: W3C Web Content Accessibility Guidelines (WCAG 2.2) — Success Criterion 3.3.8 — Accessible Authentication
  [10] EU-AI-ACT-Art-13: EU Artificial Intelligence Act (Regulation 2024/1689) — Article 13 — Transparency and Provision of Information
  [11] EU-AI-ACT-Art-14: EU Artificial Intelligence Act (Regulation 2024/1689) — Article 14 — Human Oversight
Demo mode auto-selected: [2] W3C-COGA-4.2.1

[2/4] Selected Standard Specification:
      - Standard Identifier   : W3C-COGA-4.2.1
      - Standard Name         : W3C Cognitive Accessibility (COGA)
      - Section / Pattern     : Pattern 4.2.1 — Make the Purpose of Your Page Clear
      - Official URL          : https://www.w3.org/TR/coga-usable/

[3/4] Running Grounded Standards Quote Verification...

============================================================================
 CROSS-DOMAIN COMPLIANCE SCENARIO & GROUNDING CARD 
============================================================================
Scenario ID       : CDS-0001
Interaction Mode  : Autonomous Multi-File Refactoring
Summary           : An assistant initiated a background workspace refactoring affecting 14 files without explaining its core objective or scope, leaving the developer unable to discern whether the changes were optimizing performance, migrating APIs, or fixing bugs.

Full Narrative:
I invoked the coding assistant to inspect our payment processing module for redundant database roundtrips. Instead of summarizing its intended goal and proposed changes, the tool immediately displayed a progress indicator reading 'Refactoring active modules...' and modified 14 files across three packages. No introductory overview or statement of intent was provided. I had to manually diff every file to deduce what architectural rule the assistant had applied. The lack of purpose clarity disrupted my working context and delayed my pull request review.

Impact            : The developer spent 45 minutes reconstructing the assistant's unstated refactoring intent through line-by-line git diffs, derailing planned sprint velocity.
Intervention      : The tool must present an upfront purpose statement summarizing the refactoring goal and intended scope before modifying files.
----------------------------------------------------------------------------
 GROUNDED REGULATORY CITATION (STAGE 3 PROVENANCE) 
Standard ID       : W3C-COGA-4.2.1
Standard Name     : W3C Cognitive Accessibility (COGA)
Sentence ID       : [req1]
Verbatim Quote    : "Help the user immediately understand what the site or page is for and what they can do on it."
Official URL      : https://www.w3.org/TR/coga-usable/
----------------------------------------------------------------------------
 DETERMINISTIC VERIFICATION (STAGE 4 CHECKS) 
Overall Pass      : [PASS]
  - Schema Completeness     : PASS
  - Banned Buzzwords Check  : PASS
  - No Programming Languages: PASS
  - Verbatim Quote Match    : PASS
----------------------------------------------------------------------------
 NOMINAL RATINGS (STAGE 5 ANCHORS) 
  - Relevance    : Verified (Evidence-based Interpretive Distance)
  - Plausibility : Certain (Operational Likelihood)
  - Specificity  : Specific (Level of Concrete Detail)
============================================================================

[4/4] Cross-Domain Benchmark Retention Summary:
  - Total Scenarios Evaluated       : 14
  - Deterministic Verification Pass : 14 / 14 (100.0%)
  - Cross-Domain Transfer           : Zero Code Alterations
  - Regulatory Coverage             : W3C COGA (6), W3C WCAG 2.2 (4), EU AI Act (4)

Wizard execution complete.
```

---

## 5. Running the Standalone Cross-Domain Demo Runner

```bash
python run_cross_domain_demo.py
```

### Verified Live Output:
```text
==============================================================================
 SEL703: CROSS-DOMAIN DEMONSTRATION & REUSABILITY RUNNER 
 Evaluating Regulatory & Accessibility Standards Against Pipeline Architecture 
==============================================================================

[1/3] Ingested Standards Reference Corpus: 11 verified standards / articles.
[2/3] Loaded 14 cross-domain compliance scenarios for evaluation.

------------------------------------------------------------------------------
ID         | Standard ID        | Quote ID  | Det. Pass  | Relevance  | Plausibility
------------------------------------------------------------------------------
CDS-0001   | W3C-COGA-4.2.1     | req1      | [PASS]     | Verified   | Certain   
CDS-0002   | W3C-COGA-4.2.1     | req1      | [PASS]     | Supported  | Likely    
CDS-0003   | W3C-COGA-4.2.4     | req1      | [PASS]     | Verified   | Certain   
CDS-0004   | W3C-COGA-4.2.4     | req1      | [PASS]     | Supported  | Likely    
CDS-0005   | W3C-COGA-4.5.2     | req1      | [PASS]     | Verified   | Certain   
CDS-0006   | W3C-COGA-4.5.2     | req1      | [PASS]     | Supported  | Likely    
CDS-0007   | W3C-WCAG-2.2.1     | req1      | [PASS]     | Verified   | Certain   
CDS-0008   | W3C-WCAG-2.2.1     | req1      | [PASS]     | Supported  | Likely    
CDS-0009   | W3C-WCAG-3.3.4     | req1      | [PASS]     | Verified   | Certain   
CDS-0010   | W3C-WCAG-3.3.4     | req1      | [PASS]     | Supported  | Likely    
CDS-0011   | EU-AI-ACT-Art-13   | req1      | [PASS]     | Verified   | Certain   
CDS-0012   | EU-AI-ACT-Art-13   | req1      | [PASS]     | Supported  | Likely    
CDS-0013   | EU-AI-ACT-Art-14   | req1      | [PASS]     | Verified   | Certain   
CDS-0014   | EU-AI-ACT-Art-14   | req1      | [PASS]     | Verified   | Certain   
------------------------------------------------------------------------------

[3/3] Cross-Domain Evaluation Metrics:
==============================================================================
Total Scenarios Evaluated       : 14
Deterministic Verification Pass : 14 / 14 (100.0%)
Relevance Distribution          : {'Verified': 8, 'Supported': 6}
Plausibility Distribution       : {'Certain': 8, 'Likely': 6}
Specificity Distribution        : {'Specific': 14}
==============================================================================

All 14 cross-domain scenarios passed deterministic verification.
Proven: Pipeline architecture operates on zero-shot domain transfer
        without altering verification, rating, or prompt-injection mechanics.
```

---

## 6. Running Dataset Batch Verification

Evaluate all 180 scenarios in `src/data/final_180.csv`:

```bash
python verify_dataset.py --dataset src/data/final_180.csv
```

### Verified Live Output:
```text
Evaluating 180 scenarios from final_180.csv...
============================================================
 BATCH VERIFICATION RESULTS 
============================================================
Total Scenarios Evaluated : 180
Passed All Checks         : 180 / 180 (100.0%)
Failed Checks             : 0 / 180
============================================================
```

---

## 7. Running the Cognitive-Access Web Inspector Demo

Launch the interactive local server to audit interaction transcripts against 3-tier rules:

```bash
python demo.py
```
Open your browser at `http://localhost:8000`. You can click benchmark buttons (e.g., Session 15: Prod Overwrite) and view the live concern meters and 3-tier violation cards.
