# API Reference

This section provides complete API documentation for all public modules in `emic`.

## Modules

- [`emic.sources`](sources.md) — Data sources and transforms
- [`emic.inference`](inference.md) — Inference algorithms (CSSR, CSM, BSI, Spectral, NSD)
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
    TakeN,
    SkipN,
    BitFlipNoise,
)

# Inference (multiple algorithms available)
from emic.inference import CSSR, CSSRConfig
from emic.inference import CSM, CSMConfig
from emic.inference import BSI, BSIConfig
from emic.inference import Spectral, SpectralConfig
from emic.inference import NSD, NSDConfig

# Analysis
from emic.analysis import analyze, AnalysisSummary

# Types
from emic.types import EpsilonMachine, CausalState, Alphabet

# Output
from emic.output import render_state_diagram, to_tikz, to_json
```
