# TASK B.2: Formal Written Justification — The 8 Executive Dysfunctions

**Audience:** Dr. Davoud / Examiners / Reviewers  
**Author:** Harjot Singh Chauhan  
**Context:** Publication Methodology Defense & Scope Justification

---

## 1. Methodology Paragraph (For SIT723 Paper Methodology Section)

> **Derivation of the Executive Dysfunction Set:**  
> In cognitive psychology, no single, universally standardized taxonomy of executive dysfunction exists that can be adopted wholesale for software engineering contexts. Rather than synthesizing an ungrounded ad-hoc list, our taxonomy was derived by systematically assembling eight validated constructs from five foundational empirical models in cognitive science and neuropsychology. The core dimensions of **Working Memory Overload**, **Set-Shifting Cost**, and **Inhibition Deficit** reflect the canonical three-component "unity and diversity" model of executive function established by Miyake et al. (2000). To capture the temporal and affective self-regulatory difficulties observed in neurodivergent developers (notably ADHD and autism), we incorporated **Time Blindness** and **Emotional Dysregulation** from Barkley's (1997) extended behavioral inhibition model, alongside **Delay Aversion** from Sonuga-Barke's (2002, 2003) dual-pathway reinforcement-sensitivity framework. Finally, we integrated **Rejection Sensitivity** from Downey and Feldman's (1996) interpersonal processing model and **Ambiguity Intolerance** from Carleton et al.'s (2007) Intolerance of Uncertainty Scale (IUS). Each of the eight constructs is grounded in primary empirical literature with extracted verbatim findings, establishing a direct theoretical chain linking cognitive barriers to developer workflow disruptions.

---

## 2. Direct Written Defense: "Why Exactly These Eight, and Why Not More or Fewer?"

### Why Not Fewer?
Each of the eight dysfunctions targets a distinct, non-redundant cognitive vulnerability during human-AI co-programming:
- *Working memory overload* affects short-term information retention during multi-file navigation.
- *Set-shifting cost* affects the reconfiguration time required when an AI suggests abrupt plan switches.
- *Inhibition deficit* affects the ability to suppress automated acceptance of plausible but buggy AI code.
- *Time blindness* affects temporal horizon forecasting and task-duration estimation during AI debugging.
- *Emotional dysregulation* affects recovery from sudden build or pipeline failures caused by hallucinated dependencies.
- *Delay aversion* affects persistence during indeterminate or unranked multi-option assistant waiting states.
- *Rejection sensitivity* affects the developer's interpretation of critical assistant correction tone.
- *Ambiguity intolerance* affects decision paralysis when assistants return under-specified alternatives.

Collapsing or reducing these constructs would erase crucial behavioural differences that software engineering environments uniquely exacerbate.

### Why Not More?
The decision to bound the taxonomy at eight constructs is a **grounded scope decision**, not an ontological claim that these are the only executive dysfunctions that exist.

Every additional candidate construct requires:
1. Validated, high-citation psychological papers published in recognized psychology/cognitive science venues.
2. Direct empirical extraction of body-text findings documenting comparison or impairment effects (e.g. response time, error rate, working memory span).
3. Plausible, non-overlapping manifestation in software engineering workflows.

While candidate constructs such as *Prospective Memory Deficits* or *Processing Speed Fluctuations* exist in the broader neuropsychological literature, they were excluded from this release because our reference corpus prioritized constructs with the strongest empirical consensus and clearest application to AI-assisted coding tools. Expanding the set in future iterations remains architecturally supported by the pipeline's generation grid.
