# Technical Report: emic — A Python Framework for ε-Machine Inference

**Status:** Draft complete (62 pages)
**Target:** arXiv, then thesis chapter
**Format:** LaTeX report (single-column)

## Build

```bash
latexmk -pdf paper.tex
```

## Structure

- **Chapter 1:** Introduction
- **Chapter 2:** Background
- **Chapter 3:** Architecture
- **Chapter 4:** Inference Algorithms
- **Chapter 5:** Validation
- **Chapter 6:** Usage
- **Chapter 7:** Performance Evaluation
- **Chapter 8:** Conclusion
- **Appendix A:** API Reference
- **Appendix B:** Computational Mechanics: A Modern Review (self-contained theory with full proofs)

## Appendix B

Appendix B contains the full text of the computational mechanics review, merged here to make the technical report self-contained. It includes:
- Mathematical preliminaries (stochastic processes, information theory, HMMs)
- Causal states and ε-machine construction
- Complete proofs: prescience, minimality, uniqueness, E ≤ Cμ
- Complexity measures and their relationships
- Numerical validation and algorithm comparison
- Related frameworks (MDL, Kolmogorov, PSRs)

The review paper (`../paper-review/`) is being developed separately as a standalone journal submission.

## Dependencies

- LaTeX with `latexmk` and `biber`
- Packages: mathpazo, amsmath, amsthm, biblatex, tikz, booktabs, listings, hyperref, cleveref
- Bibliography: `../shared/bibliography/references.bib`
- Figures: `figures/` and `../experiments/benchmarks/results/figures/`
