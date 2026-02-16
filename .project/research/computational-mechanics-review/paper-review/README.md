# Research Paper: Computational Mechanics — State-of-the-Art Review

**Status:** Clean-slate scaffold (February 2026)
**Target:** Journal review article (Entropy / J. Stat. Phys. / Chaos)
**Format:** LaTeX article (two-column)

## Objective

This paper is a field checkpoint, not a tutorial.
It must synthesise how Computational Mechanics has evolved, what has been validated, which extensions are credible, and where applications have achieved practical traction.

## Minimum Review Standard

- **Reference volume:** at least **100 unique references** (target: 120+)
- **Coverage balance:** foundations, inference methods, formal extensions, and applications
- **Evidence grading:** distinguish theorem-level results, empirical validation, and speculative claims
- **Temporal synthesis:** include a dedicated section on what changed in 2020–2026
- **Actionable output:** include open-problem matrix with blockers and near-term experiments

## Manuscript Structure (`paper.tex`)

1. Scope and review protocol
2. Foundational trajectory
3. Inference algorithm evolution and trade-offs
4. Formal extensions beyond classical settings
5. Application landscape across domains
6. Recent results (2020–2026)
7. Open problems and research agenda
8. Conclusion

## Build

```bash
cd .project/research/computational-mechanics-review/paper-review
latexmk -pdf paper.tex
```

Output PDF: `paper.pdf`

## Bibliography Workflow

- Canonical source: `../shared/bibliography/references.bib`
- Add new entries there (do not create local `.bib` files)
- Use project citation keys: `{first-author-name}{year}[{tag}]`
- Include DOI whenever available

## Drafting Workflow

1. Fill synthesis tables first (algorithm, application, open-problem matrix)
2. Expand each section with comparative narrative, not proof-heavy exposition
3. Track reference counts by category until coverage targets are met
4. Build and inspect `paper.pdf` after each substantial pass

## Relationship to Other Papers

- `paper-tutorial/`: pedagogical and concept-first
- `paper-review/`: broad literature synthesis and state-of-the-art map
- `paper-technical/`: implementation and benchmark details
