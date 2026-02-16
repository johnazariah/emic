# Computational Mechanics Review

This project produces a comprehensive literature review of computational mechanics,
documenting the theoretical foundations and practical implementation in the `emic` library.

## Papers

The project produces three related documents targeting different audiences:

| Paper | Audience | Status |
|-------|----------|--------|
| [paper-tutorial/](tutorial/) | Newcomers, students | In progress |
| [paper-technical/](paper-technical/) | Practitioners, users | In progress |
| [paper-review/](paper-review/) | Researchers, academics | Planned |
| [paper-framework/](paper-framework/) | Software engineers | Planned |

All papers share:
- The same bibliography ([shared/bibliography/](shared/bibliography/))
- The same experimental data ([experiments/](experiments/))
- Canonical author profile ([shared/metadata/author-profile.yaml](shared/metadata/author-profile.yaml))
- Standard AI disclosure snippets ([shared/snippets/](shared/snippets/))
- Consistent notation and terminology

When starting a new paper, follow the checklist in
[`paper-framework/new-paper-checklist.md`](paper-framework/new-paper-checklist.md).

## Experiments

| Experiment | Purpose | Status |
|------------|---------|--------|
| [benchmarks/](experiments/benchmarks/) | Algorithm performance comparison | Complete |
| [convergence/](experiments/convergence/) | Sample size convergence analysis | Planned |
| [noise_robustness/](experiments/noise_robustness/) | Noise tolerance study | Planned |

## Building

```bash
# Run benchmarks and generate LaTeX tables
cd experiments/benchmarks
make report

# Build individual papers
cd paper-tutorial && latexmk -pdf paper.tex
cd paper-technical/tex && latexmk -pdf paper.tex
```

## Publication Strategy

See [publication-strategy.md](publication-strategy.md) for the overall plan.
