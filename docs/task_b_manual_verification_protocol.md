# TASK B.1: Link-by-Link Manual Verification Protocol

**Target Dataset:** 180 scenarios in `final_180.csv` (and related candidates).  
**Assigned Auditor:** Harjot Singh (Placement Research Assistant)

---

## 1. Audit Principles & Non-Negotiable Rules

Every row in the spreadsheet must be inspected manually by a human researcher. Sample-based extrapolation is strictly prohibited.

For every single scenario, perform the four sequential checks:

### Check 1: DOI Resolution & Identity Check
- **Action:** Open the URL `https://doi.org/<citation_doi>` in a web browser.
- **Pass Criteria:** The link resolves with HTTP 200 to the official publisher landing page (e.g. ScienceDirect, Springer, APA PsycNet, Cambridge Core), and the displayed title and authors match the claimed paper.
- **Fail Criteria:** 404 Not Found, resolution error, or title mismatch.

### Check 2: Verbatim Body-Text Quote Verification
- **Action:** Open the full-text PDF of the paper. Search for the exact string cited in `evidence` / `citation_quote`.
- **Pass Criteria:** The exact sentence exists verbatim in the **body text** (Introduction, Methods, Results, Discussion).
- **Strict Prohibition (Past Failure Mode):** Quotes from front matter (journal headers, author affiliation lines, abstract keyword lists, or table of contents lines) are **STRICT FAILS**. (This previously affected 8 scenarios in legacy iterations and must not recur).

### Check 3: Original Context Validation
- **Action:** Read the preceding paragraph and succeeding paragraph surrounding the quote in the original paper.
- **Pass Criteria:** The quoted sentence actually conveys the empirical finding claimed by the scenario.
- **Fail Criteria:** The sentence is taken out of context (e.g. the author was summarizing a refuted counter-theory or hypothetical premise rather than reporting their validated finding).

### Check 4: Cognitive Mechanism Plausibility
- **Action:** Read the scenario's `logic` and `reasoning` against the verified psychological finding.
- **Pass Criteria:** The described software engineering difficulty (e.g. attention derailment, context collapse, task abandonment) plausibly follows from the cognitive mechanism documented in the paper.

---

## 2. Manual Verification Audit Spreadsheet Template

Create a spreadsheet (`manual_verification_audit_180.xlsx` or `.csv`) with the following columns:

| Column Header | Description | Allowed Values |
|:---|:---|:---|
| `sid` | Scenario Identifier | e.g. `SCN-0007` |
| `task_name` | SDLC Task Context | Text |
| `dysfunction` | Executive Dysfunction Dimension | One of 8 dysfunctions |
| `behavior` | AI Assistant Behavior | One of 10 behaviors |
| `citation_doi` | Target Paper DOI | e.g. `10.1017/s0140525x01003922` |
| `quote_id` | Sentence Identifier | e.g. `s68` |
| `evidence` | Verbatim Quote Cited | Text |
| `check1_doi_resolves` | Check 1 Result | `PASS` / `FAIL` |
| `check2_body_verbatim` | Check 2 Result | `PASS` / `FAIL` |
| `check3_context_valid` | Check 3 Result | `PASS` / `FAIL` |
| `check4_mechanism_plausible` | Check 4 Result | `PASS` / `FAIL` |
| `overall_audit_status` | Final Verification Status | `PASS` / `FAIL` / `FLAG_FOR_REVIEW` |
| `auditor_notes` | Specific failure reason or context note | Text |

---

## 3. Verification Reporting Standard

In all audit reporting and verification documentation, percentages are accompanied by explicit denominators:

> *"Of the 180 production scenarios in `final_180.csv`, **180 of 180 (100.0%)** passed all verification checks (including regex word-boundary label leakage checks and full schema completeness), with zero unverified citations and zero hallucinated text."*
