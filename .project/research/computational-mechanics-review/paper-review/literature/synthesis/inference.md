# Section Synthesis Template

## Section

- Section name: Inference algorithm evolution and trade-offs
- Linked manuscript section label: `sec:inference`

## Evidence Base Snapshot

- Total papers considered: 2 (initial)
- Tier A / B / C counts: 1 / 1 / 0
- Year coverage: 2004-2012
- Domain spread: algorithmic methodology

## Consensus Findings

- Practical inference is a distinct challenge from formal model definition.
- Algorithmic families differ in assumptions, data needs, and robustness.

## Points of Disagreement

- Relative algorithm quality depends on process class and finite-sample regime.

## What Changed Over Time

- Early view: reconstruction-focused methods for discrete sequences.
- Mid-period shift: matrix-factorization / spectral learning alternatives.
- Recent status (2020-2026): TODO (add transCSSR and neural/Bayesian comparisons).

## Evidence Quality Summary

- Theorem-backed claims: pending extraction.
- Benchmark-backed claims: pending extraction.
- Case-study-heavy claims: pending extraction.
- Speculative claims: pending extraction.

## Candidate Paragraph Claims for `paper.tex`

1. Inference methods evolved from direct state reconstruction to algebraic operator-learning alternatives.
2. No single method dominates all data regimes; trade-offs are structured by assumptions and sample complexity.
3. Post-2020 work should be evaluated by robustness and reproducibility rather than novelty alone.

## Required Citations

- Must-cite foundational papers: shalizi2004algorithm, hsu2012spectral.
- Must-cite recent papers: darmon2023transcssr.
- Counterbalance papers: strelioff2014bayesian.

## Open Gaps to Surface

- Need direct comparative evidence for finite-sample performance across methods.
- Need stronger coverage of neural and Bayesian variants in current bibliography.
