# Computational Mechanics Review

This project produces a comprehensive literature review of computational mechanics,
documenting the theoretical foundations and practical implementation in the `emic` library.

## Papers

The project produces three related documents targeting different audiences:

| Paper | Audience | Status |
|-------|----------|--------|
| [tutorial/](tutorial/) | Newcomers, students | In progress |
| [technical-report/](technical-report/) | Practitioners, users | In progress |
| [review-paper/](review-paper/) | Researchers, academics | Planned |
| [emic-framework/](emic-framework/) | Software engineers | Planned |

All papers share:
- The same bibliography ([shared/bibliography/](shared/bibliography/))
- The same experimental data ([experiments/](experiments/))
- Consistent notation and terminology

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
cd tutorial/tex && latexmk -pdf tutorial.tex
cd technical-report/tex && latexmk -pdf technical-report.tex
```

## Publication Strategy

See [publication-strategy.md](publication-strategy.md) for the overall plan.
