# Reviewer Presentation Deck Structure & Video Script

A comprehensive 9-part presentation and video narration script for external expert raters evaluating the scenario dataset.

---

## Slide 1: Introduction to Schwartz Human Values

### Visual Elements
- Dark navy background (`#0b132b`), clean typography, emerald green accents (`#48cae4`).
- Circular diagram illustrating the Schwartz Basic Human Values framework (10 basic values / 19 refined subvalues).

### Narration Script
> "Welcome, and thank you sincerely for dedicating your time and expertise to this evaluation study.
> In software engineering, code quality and functional correctness have traditionally dominated research on AI coding assistants. However, software development is fundamentally a human activity. When developers interact with AI tools, their core human values—such as autonomy, competence, personal security, and peace of mind—are directly implicated.
> In this study, we ground our evaluation in Shalom Schwartz's theory of basic human values, the most internationally validated framework in social psychology. Each scenario you will evaluate describes an authentic developer workflow where an AI coding assistant's behavior threatens a fundamental human value, such as *Self-Direction in Thought*, *Personal Security*, or *Achievement*.
> Our goal is to establish an empirically verified benchmark of how these value concerns manifest for neurodivergent developers."

---

## Slide 2: Why These Eight Executive Dysfunctions?

### Visual Elements
- Two-column card layout displaying the 8 dysfunctions mapped to their empirical sources.
- Highlight box stating: *"A Grounded Scope Decision, Not an Exclusive Claim."*

### Narration Script
> "A central question in this study is: why these eight executive dysfunctions?
> In cognitive psychology, there is no single monolithic taxonomy of executive dysfunction. Rather than inventing an arbitrary list, our taxonomy synthesizes five foundational, peer-reviewed models:
> 1. The classic three-component model by Miyake and colleagues: *Working Memory Overload*, *Set-Shifting Cost*, and *Inhibition Deficit*.
> 2. Barkley's clinical executive function model: *Time Blindness* and *Emotional Dysregulation*.
> 3. Sonuga-Barke's reinforcement sensitivity model: *Delay Aversion*.
> 4. Downey and Feldman's construct of *Rejection Sensitivity*.
> 5. Carleton's intolerance of uncertainty scale: *Ambiguity Intolerance*.
> We selected these eight because each has robust, published empirical grounding and a direct, observable impact on modern software development. This is a disciplined scope decision, not a claim that no other cognitive difficulties exist."

---

## Slides 3–10: Individual Dysfunction Breakdowns

*(Each slide follows the established format: Definition -> Empirical Quote -> SE Manifestation)*

### Slide 3: Working Memory Overload
- **Source:** Cowan (2001), *Behavioral and Brain Sciences* (DOI: `10.1017/s0140525x01003922`).
- **Verbatim Quote:** *"This results in markedly less accurate and/or slower performance when more than four items must be held than when fewer items must be held..."*
- **SE Manifestation:** An assistant returns non-deterministic classification schemes during requirements review, exceeding the developer's 4-item buffer and forcing a complete workflow restart.

### Slide 4: Delay Aversion
- **Source:** Sonuga-Barke et al. (2004), *Clinical Psychology Review* (DOI: `10.1016/j.cpr.2004.11.001`).
- **Verbatim Quote:** *"Children with AD/HD perform poorer under partial and delayed reinforcement, since the intensity of reward is lower..."*
- **SE Manifestation:** The assistant provides three equally weighted, unranked options and refuses to recommend one; indeterminate payoff timing induces acute task abandonment.

### Slide 5: Set-Shifting Cost
- **Source:** Monsell (2003), *Trends in Cognitive Sciences* (DOI: `10.1016/s1364-6613(03)00028-7`).
- **Verbatim Quote:** *"To change tasks, some process or processes of 'task-set reconfiguration' must happen before appropriate task-specific processes can proceed."*
- **SE Manifestation:** Conflicting API recommendation signatures force the developer to discard an active mental model and incur repeated mental reconfiguration overhead.

### Slide 6: Rejection Sensitivity
- **Source:** Downey & Feldman (1996), *Journal of Personality and Social Psychology* (DOI: `10.1037/0022-3514.70.6.1327`).
- **Verbatim Quote:** *"Perceived rejection is then likely to prompt both affective and behavioral overreactions, which may include withdrawal of support..."*
- **SE Manifestation:** Unstructured, critical assistant feedback during PR reviews is perceived as personal incompetence, triggering task avoidance and delayed specification review.

### Slide 7: Ambiguity Intolerance
- **Source:** Carleton et al. (2007), *Journal of Anxiety Disorders* (DOI: `10.1016/j.janxdis.2006.03.014`).
- **Verbatim Quote:** *"Intolerance of uncertainty reflects a dispositional fear of the unknown, where ambiguous situations are perceived as threatening."*
- **SE Manifestation:** Vague architecture refactoring suggestions lack clear boundaries, creating decision paralysis.

### Slide 8: Inhibition Deficit
- **Source:** Barkley (1997), *Psychological Bulletin* (DOI: `10.1037/0033-2909.121.1.65`).
- **Verbatim Quote:** *"Behavioral inhibition is critical for the cross-temporal organization of behavior and resistance to distraction."*
- **SE Manifestation:** Rapid code autocompletion stream overwhelms inhibitory gating, leading to acceptance of hallucinated method calls.

### Slide 9: Time Blindness
- **Source:** Barkley (1997), *ADHD and the Nature of Self-Control*.
- **SE Manifestation:** Silent assistant timeouts and open-ended generation loops distort developer time-horizon tracking.

### Slide 10: Emotional Dysregulation
- **Source:** Shaw et al. (2014), *American Journal of Psychiatry*.
- **SE Manifestation:** Abrupt context resets and discarded draft sessions trigger severe frustration, derailing the coding day.

---

## Final Section: How to Rate (Rater Instructions)

### Narration Script (To Be Read Aloud Exactly)
> *"Now, let us walk through exactly how to evaluate each scenario.
> For each scenario, read the scenario first. Then read which value it is said to affect.
> **Do not try to fix the problem or suggest an intervention** — that is not your task here.
> Instead, do your own quick check: does the described difficulty genuinely match how this dysfunction is understood in the research? You are welcome to look up the dysfunction yourself if you want to check.
> Then rate the scenario on three dimensions using the explicit definitions provided:
> 
> 1. **RELEVANCE:** Is the described barrier traceable to the cited psychology evidence? (Verified, Supported, Partial, Doubtful, or Unfounded).
> 2. **PLAUSIBILITY:** Is this workflow difficulty plausible in modern software engineering? (Certain, Likely, Possible, Unlikely, or Implausible).
> 3. **SPECIFICITY:** Is the scenario described with sufficient concrete, actionable detail? (Specific, Detailed, General, Broad, or Vague).
> 
> Once again, thank you for your critical and honest judgement. Your evaluations directly shape the validity of this benchmark."*

---

## Video Production Notes

1. **Format:** High-resolution screen recording (1080p / 60fps) with synchronized voiceover narration.
2. **Visual Consistency:** Use the established SIT723 presentation deck theme: dark navy canvas (`#0b132b`), emerald/cyan highlights (`#48cae4`), and high-contrast white body text.
3. **Pacing:** Allocate approximately 45–60 seconds per dysfunction section. Keep transitions smooth and unhurried.
4. **Conclusion Statement:** Conclude by explaining that all rater scores will undergo median aggregation and inter-rater reliability analysis ($Cohen's\ \kappa$) before publication.
