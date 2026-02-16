# Project Roadmap

*Last updated: 2026-01-18*

---

## Vision

Build a comprehensive framework for computational mechanics that bridges classical stochastic processes to quantum emergence, providing tools for understanding structure, complexity, and prediction in dynamical systems.

---

## Current Phase: Classical Foundation

**Goal**: Production-ready classical epsilon-machine inference and analysis.

**Status**: v0.1.1 released on PyPI ✅

---

## Milestones

### ✅ M1: Core Framework (Complete)
- [x] CSSR algorithm implementation
- [x] Epsilon-machine representation
- [x] Complexity measures (Cμ, hμ, E)
- [x] Pipeline composition API
- [x] Documentation site
- [x] PyPI release

### 🚧 M2: Validation & Experimentation (In Progress)
- [x] Expand golden test suite (10+ processes)
- [ ] Convergence analysis experiments
- [ ] Parameter sensitivity characterization
- [ ] Finite-sample bias quantification
- [ ] Visualization gallery

### ✅ M3: Alternative Algorithms (Complete)
- [x] Causal State Merging (CSM)
- [x] Spectral Learning
- [x] Bayesian Structural Inference (BSI)
- [x] Neural State Discovery (NSD)
- [x] Algorithm comparison framework (Spec 015)
- [x] 92% test coverage, 309 tests

### 📝 M4: Research Paper (Planned)
- [ ] Structure and outline
- [ ] Run core experiments
- [ ] Generate figures
- [ ] Write and submit

### 📝 M5: Mixed States & Crypticity (Planned)
- [ ] Non-unifilar machine representation
- [ ] Mixed-state inference
- [ ] Crypticity computation
- [ ] Bidirectional analysis

### 💡 M6: Quantum Extension (Future)
*See [Spec 016](../specifications/016-quantum-research-program.md) for detailed research program*

**Investigation 1: Decoherence Trajectory** (First target)
- [ ] Quantum types (`QuantumCausalState`, `QuantumEpsilonMachine`)
- [ ] Q-machine construction from ε-machine
- [ ] Decoherence channels (dephasing, depolarizing)
- [ ] $C_q(\gamma)$ trajectory analysis
- [ ] Phase transition / universality analysis

**Investigation 2: Taxonomy of Quantum Advantage**
- [ ] Feature extraction from ε-machines
- [ ] Correlation analysis: structure vs advantage
- [ ] Classification of processes by quantum advantage

**Investigation 3: Robustness to Model Mismatch**
- [ ] Error propagation from ε-machine to q-machine
- [ ] Sensitivity analysis
- [ ] Tolerance requirements

### 💡 M7: Quantum Complexity Estimation (Future)
*Novel research direction: first tool to estimate $C_q$ from data*

**Investigation 4: Quantum Complexity from Finite Samples**
- [ ] Bootstrap confidence intervals for $C_q$
- [ ] Bias correction for finite samples
- [ ] Sample complexity analysis
- [ ] Comparison to classical $C_\mu$ estimation

---

## Timeline

```
2026 Q1 (Jan-Mar)
├── Jan: M2/M3 - Experiments and algorithms ✅
├── Feb: M4 - Paper draft, multivariate study
└── Mar: M4 - Paper submission

2026 Q2 (Apr-Jun)
├── Apr: M5 - Mixed states
├── May: M5 - Crypticity
└── Jun: M6 - Quantum foundations

2026 Q3 (Jul-Sep)
├── Jul-Sep: M6/M7 - Quantum development

2026 Q4 (Oct-Dec)
├── Oct-Dec: M7 - Emergence studies, Paper 2
```

---

## Next Actions

### This Week (Jan 18-24)
1. [ ] Run pilot multivariate study (Spec 015, reduced design)
2. [ ] Add golden tests for BSI, NSD, Spectral algorithms
3. [ ] Create visualization gallery for state diagrams
4. [ ] Prepare v0.2.0 release with new algorithms

### Next Week (Jan 25-31)
1. [ ] Run full convergence experiments
2. [ ] Generate parameter sensitivity plots
3. [ ] Begin paper outline (M4)

---

## Open Questions

1. **Multivariate study scope**: Full factorial (635k runs) or reduced design (15k runs)?
2. **Real-world data**: Which domain to focus on? (Finance, genomics, neuro?)
3. **Paper venue**: Target journal/conference?
4. **Quantum scope**: Which toy model first?

---

## Recent Achievements

### Session: Jan 15-18, 2026
- ✅ Implemented 4 alternative algorithms (CSM, BSI, NSD, Spectral)
- ✅ Created comprehensive test suite (309 tests, 92% coverage)
- ✅ Designed multivariate study (Spec 015)
- ✅ Added CSM demonstration notebook

---

## Resources

- [Specifications](.project/specifications/000-index.md)
- [Journal](JOURNAL.md)
- [Documentation](https://johnazariah.github.io/emic/)
