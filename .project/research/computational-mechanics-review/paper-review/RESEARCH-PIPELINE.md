# Review Research Pipeline

This document defines the operating system for building a review-grade literature synthesis (100+ references, target 120+).

## Objective

Produce a defensible state-of-the-art checkpoint for Computational Mechanics by combining systematic discovery, structured extraction, and evidence-weighted synthesis.

## Model Stack

Use a two-model workflow:

1. **Primary synthesis model**
   - Purpose: paper triage, extraction, section synthesis
   - Recommended: GPT-5.3-class reasoning model

2. **Independent verifier model**
   - Purpose: contradiction checks, missing-literature checks, confidence audit
   - Recommended: a second strong long-context model from a different provider

Rule: any strong claim in the review should survive both model passes and at least one direct source check.

## Throughput Plan (Target: 120+ References)

Use three depth tiers:

- **Tier A (deep read):** 25 papers
  - Full-method and full-results extraction
  - Used for major claims and synthesis anchors
- **Tier B (focused read):** 40 papers
  - Abstract, methods, key results, limitations
  - Used for trend and comparison support
- **Tier C (rapid screen):** 55+ papers
  - Relevance tag, one key contribution, confidence note
  - Used for breadth and citation coverage

## Weekly Cadence

- **Day 1:** discovery and queue building
- **Day 2-4:** extraction (evidence cards)
- **Day 5:** synthesis notes by section
- **Day 6:** verifier pass and contradiction audit
- **Day 7:** bibliography cleanup and manuscript integration

Minimum weekly output:

- 6 Tier A cards
- 10 Tier B cards
- 12 Tier C cards
- 2 section synthesis notes

## Stages

### Stage 1 — Seed Set

Create an initial set from canonical papers and references already in `shared/bibliography/references.bib`.
Split seeds into: foundations, inference, extensions, applications, recent advances (2020+).

### Stage 2 — Citation Chaining

For each seed, perform:

- backward chaining (references it cites)
- forward chaining (papers citing it)

Stop chaining a branch when two consecutive papers add no new methods, domains, or evidence classes.

### Stage 3 — Triage and Tiering

Assign each candidate to Tier A/B/C based on novelty, influence, and relevance to review questions.
Record decisions in the citation ledger.

### Stage 4 — Evidence Cards

Use `literature/evidence-card-template.md`.
One card per paper, one file per citation key.
Do not write prose for the manuscript yet.

### Stage 5 — Synthesis Notes

Use `literature/synthesis-note-template.md` for each review section.
Synthesis notes merge findings across cards and mark consensus versus uncertainty.

### Stage 6 — Manuscript Integration

Populate manuscript tables first.
Then convert synthesis notes into prose in `paper.tex`.
Every paragraph-level claim should map back to evidence cards.

## Quality Gates

Before each major draft checkpoint, verify:

1. **Coverage gate**: category counts on track for 120+ references
2. **Balance gate**: applications and extensions not overshadowed by foundations
3. **Evidence gate**: claims labelled theorem-backed, benchmark-backed, case-study, or speculative
4. **Recency gate**: at least 20 references from 2020-2026
5. **Audit gate**: independent verifier review completed for section claims

## File Conventions

- Evidence cards: `literature/cards/<citekey>.md`
- Synthesis notes: `literature/synthesis/<section>.md`
- Coverage tracker: `literature/citation-ledger.md`

Create directories as needed and keep names stable so scripts/agents can index them later.

## Definition of Done for the Review Literature Phase

Literature phase is complete when all are true:

- 120+ unique references in shared bibliography
- Coverage targets satisfied per category
- All manuscript sections have synthesis notes
- Open-problem matrix filled with evidence-backed blockers
- Verifier pass complete with unresolved contradictions explicitly documented
