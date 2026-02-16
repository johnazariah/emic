---
title: "emic: A Python Framework for Epsilon-Machine Inference and Characterization"
tags:
  - Python
  - computational mechanics
  - epsilon-machine
  - causal states
  - complexity
  - stochastic processes
  - hidden Markov models
authors:
  - name: John Azariah
    orcid: 0009-0007-9870-1970
    affiliation: 1
affiliations:
  - name: University of Technology Sydney, Australia
    index: 1
date: 15 February 2026
bibliography: paper.bib
---

# Summary

`emic` (Epsilon Machine Inference & Characterization) is a Python library for
constructing and analyzing epsilon-machines — the minimal, optimal predictors of
stochastic processes introduced by Crutchfield and Young
[@crutchfield1989inferring]. An epsilon-machine partitions process histories into
*causal states*, equivalence classes that yield identical conditional predictions
of future observations [@shalizi2001computational]. The resulting model is the
smallest unifilar hidden Markov model of the process, and its Shannon entropy —
the *statistical complexity* $C_\mu$ — quantifies the minimum memory required
for optimal prediction.

`emic` provides five inference algorithms, a suite of information-theoretic
analysis measures, built-in stochastic process generators, composable data
pipelines, and multiple visualization and export formats. It is designed for
researchers and students in complexity science, statistical physics, information
theory, and related disciplines who need a modern, tested, and extensible
toolkit for computational mechanics.

# Statement of Need

Computational mechanics [@crutchfield1994calculi; @shalizi2001computational]
offers a principled framework for discovering hidden structure in sequential
data. Despite three decades of theoretical development — spanning physics,
neuroscience, linguistics, and finance — accessible software has lagged behind.
The original CSSR reference implementation
[@shalizi2004algorithm; available at https://github.com/stites/CSSR, mirrored
from http://bactra.org/CSSR/] is a single-algorithm C++ program, last updated in
2008, that is difficult to extend and no longer actively maintained. The
canonical Python library from Crutchfield's group, CMPy [@cmpy], is no longer
available — its website and source code have been taken offline. No existing
maintained package provides multiple inference algorithms, rigorous golden-test
validation against known processes, or a unified API for both inference and
analysis.

`emic` fills this gap. It targets three audiences: (1) researchers exploring
computational mechanics who need reliable, validated inference; (2) students
learning the theory through hands-on experimentation; and (3) practitioners
applying epsilon-machine analysis to empirical data.

# State of the Field

The following table compares `emic` to existing software in the computational
mechanics and complexity analysis landscape.

: Comparison of software for computational mechanics and complexity analysis. \label{landscape}

| Package | Language | $\varepsilon$-Machine Inference | Algorithms | $C_\mu$, $h_\mu$ | Tests | Registry | Maintained |
|:--------|:---------|:-------------------------------:|:-----------|:-----------------:|:-----:|:--------:|:----------:|
| **emic** | Python | **Yes** | CSSR, Spectral, CSM, BSI, NSD | **Yes** | **194** | **PyPI** | **Yes** |
| CSSR [@shalizi2004algorithm] | C++ | Yes | CSSR | Yes | No | No | No (2008) |
| transCSSR [@darmon2023transcssr] | Python | Yes | CSSR (transducers) | Indirect | No | No | Yes |
| CMPy [@cmpy] | Python | Yes | CSSR, Bayesian | Yes | Unknown | No | No (defunct) |
| cbayes [@strelioff2014bayesian] | Python | Yes | BSI | Indirect | No | No | No (2014) |
| dit [@james2018dit] | Python | No | — (measures only) | From distributions | Yes | PyPI | Partial |
| ComplexityMeasures.jl [@datseris2025cm] | Julia | No | — (ordinal patterns) | Permutation-based | Yes | Julia | Yes |

Several packages address adjacent problems without performing epsilon-machine
inference from data. `dit` [@james2018dit] is a comprehensive discrete
information theory library — co-authored by Crutchfield — that computes over 100
measures from explicit probability distributions but does not infer causal
states from time series. `ComplexityMeasures.jl` [@datseris2025cm] provides
ordinal-pattern-based entropy and statistical complexity in Julia but uses the
Bandt–Pompe symbolization framework rather than Crutchfield's causal-state
formalism. JIDT [@lizier2014jidt] offers transfer entropy and mutual information
estimation in Java with multi-language bindings, targeting information dynamics
rather than epsilon-machine construction. `GenTex` applies epsilon-machine
construction to image co-occurrence matrices for texture analysis, but is
restricted to that domain and has not been updated since 2019.

Among tools that do perform epsilon-machine inference, `transCSSR`
[@darmon2023transcssr] extends CSSR to input–output transducers but implements
only a single algorithm and does not compute complexity measures directly.
`cbayes` implements Bayesian structural inference but depends on the now-defunct
CMPy and has not been updated since 2014.

`emic` is the only maintained package that combines multiple inference
algorithms, direct computation of complexity measures, validated golden tests
against canonical processes, and a composable pipeline API — all in a single,
installable Python library.

# Software Design

`emic` is structured around three design principles:

**Immutability.** Core types — `EpsilonMachine`, `CausalState`, `Transition`,
`Distribution` — are frozen dataclasses. This eliminates aliasing bugs, makes
objects hashable, and simplifies reasoning about correctness.

**Protocol-based extensibility.** Inference algorithms and data sources conform
to Python `Protocol` types rather than inheriting from abstract base classes.
Users can add new algorithms or sources without modifying existing code, and
static type checkers (Pyright, strict mode) verify conformance at development
time.

**Pipeline composition.** The `>>` operator chains sources, transforms, and
consumers into declarative workflows:

```python
from emic.sources import GoldenMeanSource, TakeN
from emic.inference import CSSR, CSSRConfig
from emic.analysis import analyze

source = GoldenMeanSource(p=0.5, _seed=42)
data = source >> TakeN(10_000)
result = CSSR(CSSRConfig(max_history=5)).infer(data)
summary = analyze(result.machine)
```

All five inference algorithms — CSSR [@shalizi2004algorithm], Spectral
[@hsu2012spectral], CSM, BSI [@strelioff2014bayesian], and NSD — return a
common `InferenceResult` wrapping an `EpsilonMachine`, enabling uniform
downstream analysis ($C_\mu$, $h_\mu$, excess entropy) and export (Graphviz
DOT, TikZ, Mermaid, LaTeX tables, JSON).

A CLI tool (`emic-experiment`) and experiment registry support reproducible
benchmarking across algorithms, sample sizes, and processes, with structured
result storage.

# Research Impact Statement

`emic` was developed as part of a doctoral research programme at the University
of Technology Sydney investigating computational mechanics and its quantum
extensions. It has been used to validate the fundamental theorems of
computational mechanics — prescience, minimality, uniqueness, and the bound $E
\le C_\mu$ — against four canonical processes (Golden Mean, Even Process, Biased
Coin, Periodic), producing numerical results reported in a companion review
paper [@azariah2026review]. A separate technical report [@azariah2026technical]
documents the library's architecture, algorithm-comparison benchmarks, and
convergence analysis in detail.

The package is available on PyPI (`pip install emic`), with full API
documentation at https://johnazariah.github.io/emic/. The test suite comprises
194 tests (unit, integration, golden-test, and property-based via Hypothesis)
with over 90 % line coverage. Strict static typing is enforced via Pyright.

# AI Usage Disclosure

GitHub Copilot (Claude) was used during the development of `emic` for code
generation, refactoring, test scaffolding, documentation drafting, and
assistance with this paper. All AI-generated outputs were reviewed, edited, and
validated by the author, who made all core design decisions.

# Acknowledgements

The author thanks James Crutchfield, Cosma Shalizi, and their collaborators for
the foundational theory that `emic` implements, and the `dit` development team
for their complementary work on information-theoretic measures.

# References
