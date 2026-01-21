# Specification Index

## Overview

This directory contains **technical design specifications** for the `emic` project.

> **Note**: Research planning has moved to `.project/research/` and experiments to `experiments/`. See [Spec 019](019-research-organization.md) for the reorganization.

---

## Specifications

### Infrastructure

| Spec | Title | Status |
|------|-------|--------|
| [001](001-devcontainer.md) | Dev Container Setup | ✅ Complete |
| [001a](001a-ci-cd-testing.md) | CI/CD & Testing | ✅ Complete |
| [008](008-documentation.md) | Documentation Infrastructure | ✅ Complete |
| [019](019-research-organization.md) | Research Organization System | ✅ Complete |

### Core Design

| Spec | Title | Status |
|------|-------|--------|
| [002](002-core-types.md) | Core Types | ✅ Complete |
| [003](003-source-protocol.md) | Source Protocol | ✅ Complete |
| [004](004-inference-protocol.md) | Inference Protocol | ✅ Complete |
| [005](005-analysis-protocol.md) | Analysis Protocol | ✅ Complete |
| [006](006-output-protocol.md) | Output Protocol | ✅ Complete |
| [007](007-pipeline-composition.md) | Pipeline Composition | ✅ Complete |

### Algorithm Design

| Spec | Title | Status |
|------|-------|--------|
| [010](010-alternative-inference.md) | Alternative Inference Algorithms | ✅ Complete |
| [016](016-performance-optimization.md) | Performance Optimization | 📝 Planning |

### Research (Archived — see `.project/research/`)

The following specs have been migrated to the new research organization:

| Old Spec | New Location |
|----------|--------------|
| [009](009-research-paper.md) | `.project/research/papers/emic-framework/` |
| [011](011-experiments.md) | `experiments/` |
| [012](012-crutchfield-derivation.md) | `.project/research/papers/derivation/` |
| [013](013-experiment-ideas.md) | `.project/research/questions/` |
| [014](014-quantum-computational-mechanics.md) | `.project/research/questions/Q-quantum.md` |
| [015](015-multivariate-inference-study.md) | `.project/research/questions/Q-multivariate.md` |
| [017](017-rederiving-paper-results.md) | `experiments/paper_verification/` |
| [018](018-noise-robustness-analysis.md) | `experiments/noise_robustness/` |

---

## Related Directories

| Directory | Purpose |
|-----------|---------|
| `.project/research/` | Research questions, hypotheses, paper drafts |
| `.project/references/` | Source papers (PDF, markdown) |
| `experiments/` | Reproducible experiments with configs and results |

- ✅ Complete — Implemented and tested
- 🚧 In Progress — Actively being developed
- 📝 Planning — Specified but not yet started
- 💡 Idea — Rough concept, needs specification
