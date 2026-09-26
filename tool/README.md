# Cognitive Accessibility Testing Tool for LLM Coding Assistants

A Python-based accessibility testing framework that evaluates an LLM coding assistant's interaction interface and generated outputs against cognitive accessibility requirements derived from published standards (W3C COGA, WCAG 2.2, EU AI Act).

---

## Tool Architecture

```
tool/
├── criteria/          # Criterion definitions loaded from taxonomy/mapping.json
├── checks/            # Evaluation engines (static, structural, and transcript checks)
├── report/            # Report generators (console, Markdown, JSON)
└── tests/             # Test suites and demo evaluation targets
```

---

## Theoretical Traceability

Each violation reported by the tool traces through a 3-tier chain:

`Standard & Guideline → Cognitive-Science Concept → Schwartz Basic Human Value`

---

## Status

Scaffolding prepared. Evaluation checks will be instantiated against `taxonomy/mapping.json` once human verification (`verified_by_harjot: true`) is complete.
