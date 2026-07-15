# SEL703 Professional Practice — Logbook

**Student:** Harjot Singh  
**Placement:** Research Assistant (unpaid), under Dr. Davoud Mougouei, Deakin University  
**Placement start:** 7 July 2026  
**Hours target:** 225 (30 working days full-time equivalent)  
**Placement focus:** Building a tool/plugin that operationalises accessibility and AI-governance standards for neurodivergent developers using LLM coding assistants. Complements ongoing SIT723 research on scenario generation.

---

## Week 1 — 7 July – 13 July 2026

**Activities**
- Attended kick-off meeting with supervisor Dr. Davoud Mougouei to confirm placement scope and deliverables. Confirmed the placement work would produce a "countermeasure tree" — a mapping of actionable recommendations from accessibility and AI-governance standards to Schwartz human values — mirroring the "attack tree" (scenarios/concerns) being built in the parallel SIT723 research project.
- Reviewed placement logistics: 225-hour requirement, portfolio deliverables (goal-setting doc, logbook, final report + exit interview), and the two optional graded tasks (G1 social responsibility, G2 self-reflection and supervisor evaluation) required for higher grades.
- Reviewed W3C COGA "Making Content Usable for People with Cognitive and Learning Disabilities" as the primary standards source for extracting cognitive-accessibility design patterns applicable to LLM interaction. Identified the "predictable interfaces" pattern as directly relevant to reducing cognitive load during LLM-assisted development.
- Started an initial survey of related standards: WCAG 2.2 (ISO/IEC 40500:2025), EN 301 549, and the EU AI Act's provisions relevant to disabled/neurodivergent users, to build a candidate source list for the extraction task.

**Judgements and decisions made**
- Decided to scope the placement's core deliverable around a **tool demonstration paper** (~4 pages, ICSE/ASE/FSE tool-demo track style) rather than a full empirical validation study, consistent with supervisor's guidance that real-user validation is deferred to a future project.
- Decided the countermeasure taxonomy would reuse the Schwartz Theory of Basic Human Values already established in the SIT723 project, both to maintain methodological consistency and to make the two deliverables directly reusable across each other.

**Reflection**
- The scope of the placement is well-defined but the two units (SEL703 and SIT723) run in parallel under the same supervisor, so time management across research argfict production and placement deliverables is the primary risk. The unit guides show minimal overlap in required outputs, so both need distinct tracking.
- Identified a gap I need to address early: I do not yet have API access to run the AI-assisted extraction of recommendations from the standards documents. This needs to be resolved with supervisor next meeting.

---

## Week 2 — 14 July – 20 July 2026

**Activities**
- Reviewed the reference paper Davoud provided that manually maps GDPR articles to Schwartz human values. This paper is the methodological template for the placement's extraction and mapping process — same manual mapping approach but AI-assisted this time, with manual verification.
- Read the neurodivergent-developer paper published at ICSE-SEIS 2025 to understand the state of prior work in this venue and to identify what an ICSE-SEIS-standard contribution looks like for this problem space.
- Drafted the initial structure of the tool-demo paper: (1) motivation grounded in Human-in-the-Loop oversight failure for neurodivergent developers, (2) taxonomy construction methodology (standards → recommendations → Schwartz values → tool features), (3) implemented feature subset, (4) discussion and future work.
- Reviewed candidate IDE/plugin implementation targets: prompt-injection-based enforcement of familiar-API constraints, structured (non-verbose) LLM output, and diff-size limits. All three map directly to identified cognitive-load reduction patterns.
- Attempted initial extraction of W3C COGA patterns manually to test whether the "half a day" AI-assisted approach recommended by supervisor is achievable — confirmed the manual work is tractable but AI assistance would significantly reduce time cost. Blocked on API access to complete this step properly.
- Started planning the separate SEL703 GitHub repository structure as requested by supervisor to keep placement deliverables clearly distinct from the SIT723 research repository.

**Judgements and decisions made**
- Decided to keep the initial countermeasure taxonomy deliberately small (targeting ~5-10 verified recommendations mapped to values) rather than exhaustive, per supervisor's explicit instruction that the initial mapping should not consume more than half a day of effort. The taxonomy is designed to be springboarded from the parallel SIT723 scenarios once available.
- Decided to structure the SEL703 repository around four artefact folders: `docs/` (methodology writeup and tool-demo paper draft), `taxonomy/` (recommendation-to-value mapping data), `plugin/` (implementation code), and `references/` (source standards and cited papers), with logbook and reflection material tracked separately.

**Reflection**
- Two weeks in and the theoretical scaffolding is clearer than the practical progress. The API-access blocker is the single biggest thing gating actual output — I need to raise this directly with the supervisor at the next meeting rather than continuing to work around it. Supervisor previously offered to run inference on his own machine if I provided the code; that offer is worth accepting explicitly rather than hoping the access resolves itself.
- Realised the placement work and the research paper need to be scheduled against each other, not in parallel as separate streams. The SIT723 human evaluation window (~1 month) is going to consume most of August, which means the placement's tool implementation needs to fit around it. Drafted a combined week-by-week plan (see accompanying planning document) to make the interlock explicit.

**CPD activity**
- Reviewed Deakin's Placement Preparation Module content on professional communication and workplace ethics in preparation for logbook and reflection tasks throughout the placement.

---

*Logbook is maintained on a weekly cadence. Next entry: Week 3 (21 – 27 July). Supervisor sign-off scheduled at placement mid-point per SEL703 unit requirements.*
