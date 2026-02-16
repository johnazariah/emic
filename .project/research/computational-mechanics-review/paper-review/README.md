# Research Paper: Computational Mechanics — A Modern Review

**Status:** Draft (~25% complete per adviser feedback; currently merged into technical report as Appendix B)
**Target:** Journal (Entropy, J. Stat. Phys., Chaos) — to be developed into a proper standalone review
**Format:** LaTeX article (two-column)
**Pages:** ~10 (estimated)

## Abstract

A self-contained review of Computational Mechanics, including:
- Complete proofs of the fundamental theorems (prescience, minimality, uniqueness, E ≤ Cμ)
- Numerical validation using the `emic` Python library
- Comparison of 5 inference algorithms (CSSR, Spectral, CSM, BSI, NSD)
- Discussion of connections to HMMs, MDL, and Kolmogorov complexity

## Build

```bash
cd tex && make
```

Or manually:
```bash
latexmk -pdf paper.tex
```

## Output

Built PDF: `paper.pdf`

## Structure

1. **Introduction** - Historical context, contributions
2. **Mathematical Preliminaries** - Processes, entropy, HMMs
3. **Causal States** - Definition, equivalence relation
4. **The ε-Machine** - Construction, unifilarity
5. **Fundamental Theorems** - Prescience, minimality, uniqueness, E ≤ Cμ
6. **Complexity Measures** - Cμ, hμ, E, crypticity
7. **Inference Algorithms** - CSSR, Spectral, CSM, BSI, NSD
8. **Numerical Validation** - Canonical processes, convergence, algorithm comparison
9. **Related Frameworks** - HMMs, MDL, Kolmogorov, PSRs
10. **Discussion** - Interpretability, computation, limitations, open questions
11. **Conclusion**

## Dependencies

- LaTeX with `latexmk`
- Packages: mathpazo, amsmath, amsthm, tikz, booktabs, hyperref, cleveref

## Bibliography

Uses shared bibliography: `../../shared/bibliography/references.bib`

## See Also

- [Publication Strategy](../publication-strategy.md) - Overall publication plan
- [Tutorial](../paper-tutorial/) - Pedagogical introduction
- [Technical Report](../paper-technical/) - emic library documentation
