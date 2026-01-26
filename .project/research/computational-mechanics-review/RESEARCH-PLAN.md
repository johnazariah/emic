# Research Plan: Computational Mechanics Review

**Project:** Documenting epsilon-machine theory and the emic library
**Status:** Active
**Started:** January 2026
**Updated:** January 25, 2026

---

## Goal

Produce a comprehensive body of work that:
1. Explains computational mechanics to new audiences (tutorial)
2. Documents the emic library for practitioners (technical report)
3. Reviews the theoretical foundations for researchers (review paper)
4. Describes the software framework for engineers (emic-framework paper)

All outputs share experimental data, bibliography, and consistent notation.

---

## Work Log

### January 25, 2026

**Codebase Cleanup & Reorganization**
- Removed `experiments/paper_verification/` (superseded by tutorial)
- Reorganized research folder structure:
  - Created `computational-mechanics-review/` as unified project
  - Moved all papers, experiments, and shared resources under one umbrella
  - Consolidated convergence and noise_robustness as sub-experiments
- Updated all path references in Makefile and analyze scripts
- Downloaded 12 reference PDFs to `.project/references/`
- Created this research plan

**Tutorial Updates**
- Added CSM (Causal State Merging) section with algorithm explanation and code examples
- Added NSD (Neural State Discovery) section with algorithm explanation and code examples
- Updated SpectralConfig code example to use new adaptive API (removed obsolete `max_future` param)
- Replaced 2-algorithm comparison table with comprehensive 5-algorithm table
- Fixed `\eM` undefined macro → `$\eps$-machine`
- Removed placeholder appendices (Solutions, Proofs) - to be added when complete
- Tutorial now compiles cleanly: 31 pages

### January 24, 2026

**Benchmark Automation Pipeline**
- Created `experiments/benchmarks/Makefile` with targets: `benchmarks`, `analyze`, `report`
- Created `analyze_results.py` to generate LaTeX tables from benchmark JSON
- Generated 4 LaTeX tables:
  - `tab-state-counts.tex` - state counts at N=100K
  - `tab-correctness.tex` - correctness summary by algorithm/process
  - `tab-correctness-detail.tex` - detailed results by sample size
  - `tab-perf-summary.tex` - runtime and accuracy summary
- Created `benchmark-data.tex` with LaTeX macros for auto-updating prose
- Updated technical report to use `\input{}` for generated tables
- Added test stats collection (326 tests, 87% coverage) to macros

**Spectral Algorithm Improvements**
- Refactored Spectral algorithm for better sample efficiency
- Added adaptive `max_history` and `min_count` based on sample size
- Improved belief state clustering for state extraction
- Result: Spectral now achieves 98% correctness at N ≥ 1K (up from ~40%)

### January 23, 2026

**Benchmark Suite Execution**
- Ran full benchmark suite: 5 algorithms × 4 processes × 5 sample sizes × 5 reps
- Total: 500 inference runs
- Results saved to `experiments/benchmarks/results/`
- Key findings:
  - Spectral: 85% overall, 100% at N ≥ 10K
  - CSSR: 82% overall, degrades on Even Process at high N
  - NSD: 73% overall, fails on Periodic
  - CSM: 39% overall
  - BSI: 32% overall

### Earlier Work (Pre-January 23)

**emic Library Development**
- Implemented 5 inference algorithms: CSSR, Spectral, CSM, BSI, NSD
- Created source generators: BiasedCoin, GoldenMean, EvenProcess, Periodic
- Built pipeline composition with `>>` operator
- Achieved 326 tests, 87% coverage
- Released v0.2.1 on PyPI

**Initial Paper Drafts**
- Tutorial: ~1500 lines covering probability, information theory, theorems, CSSR, Spectral, BSI
- Technical report: Algorithm documentation, initial benchmarks
- Review paper: Outline only
- emic-framework paper: Outline only

---

## Current State

### Papers

| Paper | Status | Pages | Notes |
|-------|--------|-------|-------|
| [tutorial/](tutorial/) | Draft | 31 | Theory + all 5 algorithms documented |
| [technical-report/](technical-report/) | Draft | ~40 | Benchmarks integrated, LaTeX macros working |
| [review-paper/](review-paper/) | Outline | - | Not started |
| [emic-framework/](emic-framework/) | Outline | - | Not started |

### Experiments

| Experiment | Status | Notes |
|------------|--------|-------|
| benchmarks | **Complete** | 5 algorithms × 4 processes × 5 sample sizes |
| convergence | Subsumed | Covered by benchmarks (N: 100 → 1M) |
| noise_robustness | Planned | Needs BitFlipNoise transform |

### Key Results (from benchmarks)

- **Spectral**: 98% correct at N ≥ 1K, 100% at N ≥ 10K (best overall)
- **CSSR**: 80% at N ≥ 1K, degrades on Even Process at high N
- **NSD**: 75% stable across all sample sizes
- **CSM**: 45% at N ≥ 1K
- **BSI**: 25% at N ≥ 1K

---

## Phase 1: Complete Tutorial & Technical Report (Current)

### Tutorial - Remaining Work
- [ ] Review for consistency with benchmark results
- [ ] Add more worked examples (Even Process, Periodic)
- [ ] Create figures for state diagrams
- [ ] Write exercises (optional)

### Technical Report - Remaining Work
- [ ] Complete Appendix B (detailed benchmark analysis)
- [ ] Add architecture diagrams
- [ ] Add case study with real data (optional)
- [ ] Review prose against auto-generated macros

### Experiments - Remaining Work
- [ ] Run noise robustness experiment (requires implementing BitFlipNoise)
- [ ] Generate convergence plots from existing benchmark data

---

## Phase 2: Review Paper (Future)

The review paper will:
- Provide rigorous mathematical treatment
- Include full proofs of key theorems
- Survey the literature (25+ years since Crutchfield 1989)
- Compare to related frameworks (HMMs, MDL, Kolmogorov complexity)

**Dependencies:** Tutorial and technical report should be stable first.

---

## Phase 3: emic Framework Paper (Future)

Software paper for Journal of Open Source Software or similar:
- Focus on API design and extensibility
- Performance benchmarks
- Installation and usage guide

**Dependencies:** Library should be stable (v1.0 release).

---

## Build Pipeline

```bash
# From experiments/benchmarks/
make benchmarks    # Run all benchmarks (~10 min)
make analyze       # Generate LaTeX tables + macros
make report        # Compile technical report

# Build individual papers
cd tutorial/tex && latexmk -pdf tutorial.tex
cd technical-report/tex && latexmk -pdf technical-report.tex
```

---

## References

Key papers are downloaded in `../../references/`:
- Shannon 1948 (information theory)
- Crutchfield 1989, 1994 (computational mechanics foundations)
- Shalizi 2001, 2004 (CSSR algorithm)
- Hsu 2012 (spectral learning)
- And 8 more...

---

## Questions to Address

From `questions/`:
- **Q001**: How does noise affect inference? → Planned experiment
- **Q002**: What sample size is needed? → Answered by benchmarks
- **Q003**: Can we reproduce theoretical results? → Validated in benchmarks

From `hypotheses/`:
- **H001**: Low noise causes over-splitting → Untested
- **H002**: High noise causes state collapse → Untested
