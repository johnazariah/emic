# Shared Publication Assets

This directory contains figures, tables, and code snippets shared across all three publications.

## Structure

```
shared/
├── figures/           # Reusable diagrams and plots
│   ├── state-machines/    # ε-machine diagrams
│   ├── plots/             # Convergence, complexity-entropy
│   └── architecture/      # emic design diagrams
├── tables/            # LaTeX table fragments
├── code/              # Validated Python examples
└── bibliography/      # Shared .bib file
```

## Figure Generation

All figures should be generated programmatically from `scripts/generate_figures.py` for reproducibility.

## Usage

Include in LaTeX documents using relative paths:
```latex
\includegraphics{../shared/figures/state-machines/golden-mean.pdf}
```

