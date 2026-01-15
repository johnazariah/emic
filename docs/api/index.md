# API Reference

This section provides complete API documentation for all public modules in `emic`.

## Modules

- [`emic.sources`](sources.md) — Data sources and transforms
- [`emic.inference`](inference.md) — CSSR algorithm and inference
- [`emic.analysis`](analysis.md) — Complexity measures and analysis
- [`emic.types`](types.md) — Core types (EpsilonMachine, CausalState, etc.)
- [`emic.output`](output.md) — Visualization and export

## Quick Import Guide

```python
# Sources
from emic.sources import (
    GoldenMeanSource,
    EvenProcessSource,
    BiasedCoinSource,
    PeriodicSource,
    SequenceData,
)

# Inference
from emic.inference import CSSR, CSSRConfig

# Analysis
from emic.analysis import analyze, Analyzer, AnalysisSummary

# Types
from emic.types import EpsilonMachine, CausalState, Alphabet

# Output
from emic.output import render_diagram, to_latex, to_json
```
