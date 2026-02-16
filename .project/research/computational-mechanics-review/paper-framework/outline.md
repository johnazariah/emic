# Paper: emic Framework

## Working Title

"emic: A Python Framework for Epsilon-Machine Inference and Computational Mechanics"

## Target Venue

- arXiv preprint (initial)
- Journal of Statistical Software or Entropy (submission)

## Status: Drafting Outline

## Paper Setup Requirements

- Use canonical author metadata from `../shared/metadata/author-profile.yaml`
- Use shared bibliography at `../shared/bibliography/references.bib`
- Include AI usage disclosure from shared snippets in `../shared/snippets/`
- Follow `new-paper-checklist.md` before drafting content

## Abstract

*To be written*

## Claims Registry

Each claim in the paper must link to supporting evidence.

| ID | Claim | Evidence | Status |
|----|-------|----------|--------|
| C1 | CSSR correctly infers Golden Mean with n > 5000 | EXP-001 | Untested |
| C2 | Cμ matches analytical values within 1% | EXP-003 | Untested |
| C3 | E ≤ Cμ holds for all tested processes | EXP-003 | Untested |
| C4 | CSSR tolerates noise up to ε ≈ 0.1 | EXP-002 | Untested |

## Outline

### 1. Introduction
- Motivation: Hidden structure in stochastic processes
- Gap: Theory exists but tools are inaccessible
- Contribution: Open-source Python framework

### 2. Background
- Computational mechanics foundations
- Causal states and epsilon-machines
- Complexity measures (Cμ, hμ, E)

### 3. The emic Framework
- Architecture and design
- Core types and protocols
- Pipeline composition

### 4. Empirical Validation
- Convergence analysis (EXP-001)
- Known process verification (EXP-003)
- Algorithm comparison (EXP-004)

### 5. Case Studies
- Real-world data applications
- Noise robustness (EXP-002)

### 6. Discussion
- Limitations
- Future work

### 7. Conclusion

## Figures (Planned)

1. Architecture diagram
2. State diagrams for canonical processes
3. Convergence curves (states vs n)
4. Complexity-entropy diagram
5. Noise robustness curves

## Related

- Research questions: Q002, Q003
- Experiments: EXP-001, EXP-002, EXP-003, EXP-004
