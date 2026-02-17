# Project Journal

*A chronological record of work done on the emic project.*

---

## 2026

### February 17, 2026

**Session Focus**: Review Sprint 2 — Domain-Oriented Expansion

**Completed**:

1. **Bibliography expansion (Sprint 2)**
   - Added **22** additional references to shared bibliography
   - Total shared bibliography now **76** entries (up from 54)
   - Prioritized computational-mechanics-adjacent works and domain-signaled candidates

2. **Evidence card production**
   - Generated **20** new evidence cards from Sprint 2 additions
   - Total evidence cards now **49**

3. **Coverage tracking updates**
   - Updated citation ledger with new totals and revised gaps
   - Recorded caveat that several domain papers are lower-confidence fits and require stricter manual triage before manuscript use

**Files Updated**:
- `.project/research/computational-mechanics-review/shared/bibliography/references.bib`
- `.project/research/computational-mechanics-review/paper-review/literature/cards/*` (20 new files)
- `.project/research/computational-mechanics-review/paper-review/literature/citation-ledger.md`

**Next Steps**:
1. Run quality triage pass on Sprint 2 additions (retain/remove/replace)
2. Replace lower-confidence domain-adjacent entries with direct epsilon-machine application papers where possible
3. Draft synthesis updates for applications and recent-advances sections

### February 16, 2026

**Session Focus**: Review Paper Reset to State-of-the-Art Standard

**Completed**:

1. **Clean-slate review manuscript scaffold**
    - Replaced `paper-review/paper.tex` with a review-native structure focused on:
       - protocol and scope
       - historical evolution
       - inference-method synthesis
       - formal extensions
       - application landscape
       - recent advances (2020--2026)
       - open-problem matrix
    - Removed tutorial-style proof-heavy framing from the review draft baseline

2. **Hard requirements for review quality**
    - Updated `paper-review/README.md` to formalize minimum review criteria:
       - 100+ unique references (target 120+)
       - balanced coverage across foundations/methods/extensions/applications
       - explicit evidence-quality grading
       - actionable research agenda output

3. **Global prompt-level guardrails for future drafting**
    - Updated `.github/prompts/paper.prompt.md` with a dedicated
       “Review Paper Standard (Critical)” section
    - Added required workflow for citation-balance tracking and synthesis-table-first drafting

**Files Updated**:
- `.project/research/computational-mechanics-review/paper-review/paper.tex`
- `.project/research/computational-mechanics-review/paper-review/README.md`
- `.github/prompts/paper.prompt.md`

**Next Steps**:
1. Populate synthesis tables with first-pass literature mapping
2. Build category-wise citation ledger toward 120+ references
3. Draft comparative prose section-by-section from the populated tables

**Progress Update (same session)**:

- Built first executable seed queue at `paper-review/literature/seed-queue.md`
- Confirmed current bibliography baseline is 29 entries (shortfall to 120+ tracked explicitly)
- Added first four starter Tier-A evidence cards:
   - `crutchfield1989inferring`
   - `shalizi2001computational`
   - `shalizi2004algorithm`
   - `gu2012quantum`
- Instantiated first two live synthesis notes:
   - `paper-review/literature/synthesis/foundations.md`
   - `paper-review/literature/synthesis/inference.md`
- Updated review README to link the new seed queue

**Sprint 1 Execution (same session)**:

- Added **25** metadata-verified references to shared bibliography:
   - Source: DOI-resolved metadata (OpenAlex-backed retrieval)
   - Shared bibliography total moved from **29 → 54** entries
- Generated **20** new evidence cards in `paper-review/literature/cards/`
- Updated `paper-review/literature/citation-ledger.md` with sprint totals, provisional category balance, and gap-to-target tracking
- Noted current strategic gap: strong physics/quantum concentration, under-coverage in biology, linguistics, finance, and neuroscience applications

**Session Focus**: Release Process Hardening, Publication Consistency, and Journal Stewardship

**Completed**:

1. **Release workflow split and packaging policy**
   - Updated package release flow to attach a JOSS submission bundle (`paper.md` + `paper.bib` tarball) instead of paper PDFs
   - Added dedicated publications workflow to build/version/upload tutorial, review, and technical PDFs separately
   - Aligned release checklist and release prompt with the split between software release artifacts and publication artifacts

2. **Cross-paper consistency standardization**
   - Switched JOSS paper to shared bibliography source of truth
   - Standardized citation key naming convention references in prompts/checklists
   - Updated stale software citation metadata in shared bibliography
   - Standardized canonical author identity fields across papers (name, affiliation, ORCID, email)

3. **Shared governance assets for repeatability**
   - Added canonical author profile file: `shared/metadata/author-profile.yaml`
   - Added shared AI disclosure snippets for Markdown and LaTeX
   - Added new-paper checklist for consistent setup
   - Added reusable `journal-steward-agent` prompt and integrated it into paper authoring guidance

4. **Paper source hygiene and build validation**
   - Added/standardized AI usage disclosure in non-JOSS papers via shared snippet
   - Reduced warning noise in LaTeX sources (caption hypcap, hyperref PDF string handling, fancyhdr headheight)
   - Verified all three LaTeX papers still build after changes

**Files Created**:
- `.github/workflows/publications.yml`
- `.github/prompts/journal-steward-agent.prompt.md`
- `.project/research/computational-mechanics-review/shared/metadata/author-profile.yaml`
- `.project/research/computational-mechanics-review/shared/snippets/ai-usage-disclosure.md`
- `.project/research/computational-mechanics-review/shared/snippets/ai-usage-disclosure.tex`
- `.project/research/computational-mechanics-review/paper-framework/new-paper-checklist.md`

**Files Updated (high impact)**:
- `.github/workflows/release.yml`
- `.github/prompts/release.prompt.md`
- `.github/prompts/paper.prompt.md`
- `.project/research/computational-mechanics-review/release-checklist.md`
- `.project/research/computational-mechanics-review/paper-joss/paper.md`
- `.project/research/computational-mechanics-review/paper-technical/paper.tex`
- `.project/research/computational-mechanics-review/paper-review/paper.tex`
- `.project/research/computational-mechanics-review/paper-tutorial/paper.tex`

**Next Steps**:
1. Trigger `publications.yml` on next release to validate end-to-end PDF publication path
2. Optional cleanup of remaining non-blocking LaTeX warnings if desired
3. Proceed with patch release tagging after final changelog review

**Session Focus**: Patch Release 0.5.1 Ceremony and Quality Gates

**Completed**:

1. **Release validation gates executed (release.prompt.md)**
   - README smoke test passed
   - Documentation build passed in strict mode
   - Full test suite passed (`408 passed`)
   - Coverage verified at `90.82%` (threshold `82%`)
   - Type checks and pre-commit hooks passed

2. **Release metadata finalized**
   - Added `0.5.1` release notes to `CHANGELOG.md`
   - Bumped package version from `0.5.0` to `0.5.1` in `pyproject.toml`
   - Refreshed lockfile metadata (`uv.lock`) and normalized formatting/newlines in touched files

3. **Post-tag CI parity fix**
   - Diagnosed release workflow failure to `ruff format --check src tests` mismatch on two test files
   - Applied CI-equivalent Ruff formatting in:
     - `tests/golden/test_inference_golden.py`
     - `tests/unit/test_sources_synthetic.py`
   - Re-ran CI-equivalent lint checks locally to confirm pass before follow-up push

**Next Steps**:
1. Push formatter hotfix commit
2. Re-point `v0.5.1` tag to release-ready commit
3. Re-run and verify release workflow artifacts

**Session Focus**: Lock-Step Publication Automation and Post-JOSS Toggle

**Completed**:

1. **Lock-step publication orchestration**
   - Updated `release.yml` to call reusable `publications.yml` after GitHub release creation
   - Publication PDFs now upload in the same release run for synchronized software + paper artifacts

2. **Post-submission JOSS flexibility**
   - Added conditional JOSS bundle packaging gate in `release.yml`:
     - Build bundle by default
     - Skip automatically when repository variable `JOSS_SUBMISSION_COMPLETE=true`
   - Added manual dispatch override input `include_joss_bundle` for release workflow

3. **Publication CI reproducibility fix**
   - Diagnosed `Publications` workflow failure to missing non-versioned benchmark figure PDFs
   - Made technical paper self-contained by switching to local `paper-technical/figures/*.pdf` paths
   - Added required benchmark figure PDFs to `paper-technical/figures/`
   - Verified technical paper build succeeds locally after path update

4. **JOSS draft workflow noise reduction**
   - Updated `draft-paper.yml` to ignore release tags (`v*`) so JOSS draft builds do not run on every release tag push

5. **Process docs alignment**
   - Updated release prompt/checklist to document lock-step publications and `JOSS_SUBMISSION_COMPLETE` behavior

**Next Steps**:
1. Commit and push workflow/doc/figure updates
2. Re-run `Publications` for `v0.5.1` to attach tutorial/review/technical PDFs
3. Verify release assets include package, JOSS bundle policy-compliant artifacts, and publication PDFs

**Session Focus**: Technical Report Test/Coverage Stats Automation

**Completed**:

1. **Automated test/coverage macro refresh for technical paper**
   - Added `experiments/benchmarks/update_test_stats.py` to compute:
     - Total tests
     - Unit/golden/integration/property test counts
     - Coverage percentage
   - Script updates `paper-technical/generated/benchmark-data.tex` macros directly

2. **Integrated stats refresh into build pipeline**
   - Updated `build-all.sh` so `make techreport` refreshes test/coverage macros before LaTeX build
   - Eliminates stale hardcoded test/coverage numbers in technical report builds

3. **Technical paper hardcoded value cleanup**
   - Replaced remaining fixed test-count/coverage text with macros in `paper-technical/paper.tex`
   - Updated validation table to use dynamic suite-count macros

4. **Validation**
   - Ran updater successfully (now reports current values)
   - Verified `make techreport` succeeds end-to-end with automated refresh

**Next Steps**:
1. Commit and push automation updates
2. Optionally add a lightweight CI check ensuring generated benchmark-data macros are fresh

### January 28, 2026

**Session Focus**: Quantum Research Program Specification

**Completed**:

1. **Full PDF Extraction**
   - Discovered previous "extractions" were AI summaries (2-10 lines/page)
   - Re-extracted all 16 PDFs properly (~50-80 lines/page)
   - Created `extract_pdf.py` tool for future extractions
   - Created `CATALOG.md` index organized by topic

2. **Literature Synthesis**
   - Read key papers: Gu 2012, Thompson 2018, Aghamohammadi 2017/2018
   - Synthesized the technical insight: non-orthogonal encoding eliminates crypticity
   - Identified the causal asymmetry result (quantum restores time-symmetry)

3. **Novel Research Questions Identified**
   - **Decoherence Trajectory**: How does $C_q \to C_\mu$ under noise?
   - **Taxonomy**: What predicts quantum advantage?
   - **Robustness**: How sensitive is $C_q$ to ε-machine errors?
   - **Primary Target**: $C_q$ estimation from finite samples (never done)

4. **Research Program Specification**
   - Created Spec 016: Quantum Research Program
   - Detailed algorithm for decoherence trajectory investigation
   - Pseudocode for q-machine construction
   - Success criteria and expected outputs
   - Four investigations building toward novel contribution

**Key Insight**: The decoherence trajectory investigation builds all infrastructure needed for the harder inference problem, while potentially producing a standalone publishable result.

**Files Created/Modified**:
- `.project/specifications/016-quantum-research-program.md` (new)
- `.project/references/CATALOG.md` (new)
- `.project/references/extract_pdf.py` (new)
- `.project/references/*/..._full.md` (16 full extractions)
- `.project/plan/ROADMAP.md` (updated M6/M7)
- `.project/research/quantum-emergence/README.md` (updated)

**Next Steps**:
1. Implement Investigation 1: Decoherence Trajectory
2. Build quantum types (`QuantumCausalState`, `QuantumEpsilonMachine`)
3. Run trajectory analysis on canonical processes
4. Analyze for phase transitions / universality

---

### January 27, 2026

**Session Focus**: Quantum Emergence Research Area

**Completed**:

1. **Created new research area: quantum-emergence/**
   - Focus on extending emic toward quantum computational mechanics
   - Goal: Re-derive Mile Gu's results on quantum memory advantage
   - Structure: review/, experiments/, theory/, implementation/

2. **Literature Review Setup**
   - Created annotated bibliography of key papers
   - Documented core concepts: $C_q$, quantum causal states, crypticity
   - Key papers: Gu et al. (2012), Tan et al. (2014), Garner et al. (2017)

3. **Mathematical Framework**
   - Documented the key inequality: $E \leq C_q \leq C_\mu$
   - Crypticity $\chi = C_\mu - E$ as target for quantum elimination
   - Non-orthogonal encoding as source of quantum advantage

**Key Insight**: The gap between statistical complexity ($C_\mu$) and excess entropy ($E$) represents information waste that quantum models can eliminate. emic already computes both quantities—adding crypticity computation is a natural next step.

**Files Created**:
- `.project/research/quantum-emergence/README.md`
- `.project/research/quantum-emergence/review/README.md`
- `.project/research/quantum-emergence/review/key-papers.md`
- `.project/research/quantum-emergence/review/concepts.md`

**Next Steps**:
1. Add crypticity ($\chi = C_\mu - E$) to emic's analysis module
2. Read and summarize key papers in detail
3. Identify validation targets (perturbed coin, etc.)
4. Design quantum epsilon-machine representation

---

### January 26, 2026 (Evening)

**Session Focus**: General-Purpose Benchmarking Tool

**Completed**:

1. **ADR-008: Benchmarking Tool Architecture**
   - Documented design decision for thin core + rich experiments approach
   - Key principle: Data collection separated from formatting
   - Output: Timestamped Parquet/JSON results + metadata.yaml
   - Downstream consumers (papers, CI) handle their own formatting

2. **Implemented `emic.experiments` Module**
   - `schema.py`: BenchmarkResult dataclass, ResultsWriter, Parquet/JSON I/O
   - `registry.py`: ProcessRegistry and AlgorithmRegistry for declarative registration
   - `config.py`: YAML-based ExperimentConfig and BenchmarkConfig
   - `runner.py`: Core runner with SIGALRM timeout handling, progress tracking
   - `cli.py`: CLI entry point (`emic-benchmark`)

3. **CLI Features**
   - `emic-benchmark --all`: Run all experiments
   - `emic-benchmark accuracy`: Run specific experiment
   - `emic-benchmark --quick`: Skip slow algorithms, use reduced sample sizes
   - `emic-benchmark --list`: List available experiments
   - Results saved to `experiments/results/<timestamp>/`
   - `latest` symlink for convenience

4. **Default Experiments**
   - accuracy: Measure algorithm accuracy on canonical processes
   - convergence: How accuracy changes with sample size
   - scalability: Runtime scaling with data size

5. **Tests**
   - Added 17 unit tests for benchmarks module
   - All 351 tests passing

**Files Created**:
- `src/emic/benchmarks/__init__.py`
- `src/emic/benchmarks/schema.py`
- `src/emic/benchmarks/registry.py`
- `src/emic/benchmarks/config.py`
- `src/emic/benchmarks/runner.py`
- `src/emic/benchmarks/cli.py`
- `tests/unit/test_benchmarks.py`
- `.project/adr/008-benchmarking-tool.md`
- `experiments/results/.gitkeep`

**Files Modified**:
- `pyproject.toml`: Added `emic-benchmark` script entry point, `benchmarks` optional deps

**Branch**: `feature/benchmarks` (worktree at `/workspace/worktrees/benchmarks`)

**Next Steps**:
- Merge to main after review
- Migrate existing paper benchmarks to use new tool
- Add more experiment types as needed

---

### January 26, 2026

**Session Focus**: CSSR Algorithm Correctness & Benchmarking

**Completed**:

1. **CSSR Algorithm Validation Against Shalizi (2004)**
   - Verified emic CSSR matches published benchmarks
   - Key result: At N=10,000, CSSR correctly finds 2 states for Even Process and Golden Mean
   - This matches Shalizi's Table 1 showing 100% correct at N=10^4, α=10^-3, L≥3

2. **Quick Benchmark Script**
   - Created `scripts/quick_benchmark.py` for fast validation (~1 minute vs 6+ hours for full benchmark)
   - Tests CSSR, Spectral, and CSM on Even Process, Golden Mean, Biased Coin
   - Sample sizes: N=1K, 10K, 100K
   - Results:
     - CSSR: 67% overall, 100% at N≥100K
     - Spectral: 100% across all sample sizes (best performer)
     - CSM: 56% overall

3. **Documentation Updates**
   - Updated `docs/guide/cssr-deep-dive.md` with new Section 11 "Algorithm Correctness and Benchmarks"
   - Added validation tables showing Shalizi benchmark comparison
   - Documented sample size sensitivity guidelines

4. **Technical Report Updates**
   - Updated `benchmark-data.tex` with corrected macro values
   - Test count: 326 → 334
   - Updated correctness percentages: Spectral now 100%, CSSR 67%
   - Updated test table in technical-report.tex

**Key Findings**:
- CSSR performance is highly sample-size dependent
- At N < 1,000: Over-splitting due to statistical fluctuation
- At N = 10,000: Matches Shalizi published benchmarks
- At N ≥ 100,000: Reliable reconstruction
- Spectral Learning consistently outperforms CSSR at all sample sizes

**Files Modified**:
- `scripts/quick_benchmark.py` — new file
- `docs/guide/cssr-deep-dive.md` — added Section 11
- `.project/research/computational-mechanics-review/technical-report/tex/generated/benchmark-data.tex`
- `.project/research/computational-mechanics-review/technical-report/tex/technical-report.tex`

**Test Results**:
- 334 tests passing
- All golden tests for CSSR pass at appropriate sample sizes

**Notes**:
- Full benchmark (experiments/benchmarks/run.py) takes 6+ hours due to BSI and large sample sizes
---

### January 24, 2026

**Session Focus**: Comprehensive Tutorial Development

**Completed**:

1. **Tutorial Rewrite** — Complete overhaul of tutorial document
   - Now covers all 6 Shalizi theorems (Prescience, Minimality, Uniqueness, Min Stochasticity, Bound, Control)
   - Added Bayesian perspective with Dirichlet-Multinomial framework
   - Structured into 6 Parts: Foundations → Causal States → Theorems → Measures → Inference → Examples
   - ~800 lines of LaTeX with custom environments (keyidea, intuition, theorembox, etc.)

2. **Spell Checker Config** — Added `.vscode/settings.json` with `cSpell.words` for academic names (Crutchfield, Shalizi, Siddiqi, etc.)

**Key Content Added to Tutorial**:
- Part I: Probability refresher, information theory (H, I, conditional entropy)
- Part II: Causal equivalence, causal states, morphs, ε-machine, unifilarity
- Part III: All 6 theorems with intuitive explanations and proof sketches
- Part IV: Cμ, hμ, complexity-entropy plane visualization
- Part V: CSSR algorithm + Bayesian (BSI) with Gibbs sampling explanation
- Part VI: Worked examples (BiasedCoin, GoldenMean, EvenProcess, Periodic)

**Files Modified**:
- `.project/research/papers/tutorial/tex/main.tex` — complete rewrite
- `.vscode/settings.json` — new file

**Notes**:
---


**Session Focus**: Publication Strategy & Paper Writing Infrastructure

**Completed**:

1. **Mac Devcontainer Fix** (early session)
   - Fixed missing `postStartCommand.sh` in `.devcontainer/`
   - Added Podman `runArgs` workaround for Mac compatibility
   - Tagged as v0.2.1-mac-safe

2. **Golden Tests for All Algorithms**
   - Extended `tests/golden/test_inference_golden.py` with BSI, NSD, Spectral tests
   - Spectral tests initially xfailed due to stub implementation

3. **Visualization Gallery**
   - Created `docs/gallery.md` with state machine diagrams
   - Added to MkDocs navigation

4. **Proper Spectral Learning Implementation**
   - Rewrote `src/emic/inference/spectral/algorithm.py` (+413/-170 lines)
   - Implemented Hsu, Kakade & Zhang 2012 algorithm with numpy.linalg.svd
   - Observable operators: A_x = U^T H_x V Σ^{-1}
   - State merging with 25% total variation threshold
   - All 326 tests now pass (removed 3 xfail markers)

5. **Publication Strategy**
   - Created `.project/research/papers/publication-strategy.md`
   - Defined three complementary documents:
     - **Tutorial**: "A Practical Guide to Computational Mechanics" — for university presentations
     - **Research Paper**: "Computational Mechanics: A Modern Review" — journal submission
     - **Technical Report**: "emic: A Python Framework" — thesis chapter
   - Set up directory structure with LaTeX templates
   - Created shared bibliography (20+ references)

**Created Files**:
- `.project/research/papers/publication-strategy.md` — master planning doc
- `.project/research/papers/shared/bibliography/references.bib` — shared citations
- `.project/research/papers/tutorial/tex/main.tex` — pedagogical guide template
- `.project/research/papers/review-paper/tex/main.tex` — formal paper template
- `.project/research/papers/technical-report/tex/main.tex` — thesis chapter template
- `.project/notes/spectral-learning-implementation.md` — algorithm analysis

**Test Results**:
- 326 tests passing
- pyright: 0 errors
- All algorithms validated on golden processes

**Notes**:
- The three documents form a hierarchy: Tutorial → Paper → Report
- Each references the others appropriately
- Shared assets (figures, tables, code) avoid duplication
- Existing content in `experiments/paper_verification/tex/` can be salvaged

**Next Steps**:
- Run EXP-003 to populate numerical validation tables
- Generate figures programmatically for reproducibility
- Draft Tutorial Sections 1-6 (narrative content)
- Complete proofs in Research Paper

---

### January 15, 2026 (Session 3)

**Session Focus**: Implementing All Alternative Inference Algorithms (Spec 010)

**Completed**:
- Implemented all four alternative inference algorithms from Spec 010:

1. **Spectral Learning** (`src/emic/inference/spectral/`)
   - Hankel matrix construction from sequence statistics
   - Simplified SVD via power iteration (no numpy dependency)
   - Observable operator extraction
   - Automatic rank selection via singular value threshold
   - `SpectralConfig` with max_history, rank_threshold, rank, regularization, min_count

2. **Bayesian Structural Inference (BSI)** (`src/emic/inference/bsi/`)
   - Gibbs sampling over state assignments
   - Dirichlet-multinomial likelihood
   - BIC-based model selection for number of states
   - `BSIConfig` with max_states, max_history, alpha_prior, n_samples, burnin, thin, seed

3. **Neural State Discovery (NSD)** (`src/emic/inference/nsd/`)
   - History embeddings from predictive distributions
   - K-means++ clustering with automatic k selection
   - Information-theoretic cluster scoring
   - `NSDConfig` with max_states, history_length, embedding_dim, n_iterations, convergence_threshold, seed

4. **Causal State Merging (CSM)** — completed in Session 2

- All algorithms implement `InferenceAlgorithm` protocol
- All support pipeline syntax: `sequence >> Algorithm(config)`
- All use `EpsilonMachineBuilder` to construct machines

**Updated Exports**:
- `emic.inference` now exports: CSSR, CSM, BSI, NSD, Spectral (+ configs)
- All accessible via unified interface

**Created Multivariate Study Specification**:
- Spec 015: Multivariate Inference Study
- Defines comprehensive comparison across all 5 algorithms
- 6 ground truth processes with varying parameters
- 7 sample sizes from 100 to 100,000
- Full factorial and reduced (Latin hypercube) designs
- Analysis plan with convergence curves, Pareto frontiers, sensitivity analysis
- Estimated ~15,000 experiments for reduced design

**Test Results**:
- All 226 tests passing
- pyright: 0 errors (22 warnings from generics)
- Smoke test verified all algorithms work on real data

**Algorithm Performance (Smoke Test)**:
- BSI: 1 state for biased coin ✓
- NSD: 2 states for golden mean ✓
- Spectral: 5 states for golden mean (needs tuning)

**Notes**:
- Spectral learning is a simplified implementation without numpy
- Full SVD would require adding numpy as dependency
- BSI and NSD are stochastic — results vary with seed
- All algorithms would benefit from golden tests

**Next Steps**:
- Add unit tests for Spectral, BSI, NSD
- Add golden tests for new algorithms
- Run pilot multivariate study
- Tune algorithm defaults for better performance

---

### January 15, 2026 (Session 2)

**Session Focus**: Implementing Spec 010 — CSM Algorithm

**Completed**:
- Implemented Causal State Merging (CSM) algorithm
  - Created `src/emic/inference/csm/` module
  - `CSMConfig` with history_length, merge_threshold, distance_metric, min_count, hierarchical
  - Four distance metrics: KL divergence, Hellinger, total variation, chi-squared
  - Full pipeline support via `__rrshift__` operator

- Algorithm features:
  - Bottom-up approach (vs CSSR's top-down splitting)
  - Starts with finest partition (each history = one state)
  - Iteratively merges closest pairs below threshold
  - Consistent with InferenceAlgorithm protocol

- Added comprehensive tests:
  - 18 unit tests in `test_inference_csm.py`
  - 14 golden tests in `test_inference_golden.py`
  - Tests for config validation, inference, pipeline, distance metrics
  - Cross-validation tests comparing CSM and CSSR

- Updated exports:
  - Added CSM and CSMConfig to `emic.inference.__init__.py`
  - Both algorithms now accessible via unified interface

**Test Results**:
- 226 tests passing (up from 212)
- No regressions
- pyright: 0 errors

**Notes**:
- CSM complements CSSR well — different approach, similar results
- Both find correct state counts for known processes
- Next steps: Spectral learning, then BSI

---

### January 15, 2026

**Session Focus**: Planning, specifications, and project organization

**Completed**:
- Created Spec 010: Alternative Inference Mechanisms
  - Defined BSI, Spectral, CSM, and NSD algorithms
  - Established unified interface and comparison matrix

- Created Spec 011: Experiments and Empirical Validation
  - Defined 6 experiment categories
  - Outlined paper figures

- Created Spec 012: Re-Derivation of Computational Mechanics
  - Listed 5 core theorems to derive
  - Identified novel research directions

- Created Spec 013: Experiment Ideas Catalog
  - Prioritized experiments by effort
  - Created recommended sequence

- Created Spec 014: Quantum Computational Mechanics
  - Defined quantum extension roadmap
  - Established 5-phase approach to quantum emergence

- Reorganized project management structure:
  - Moved ROADMAP.md to `.project/plan/`
  - Created `.project/record/` for JOURNAL.md
  - Created specification index (000-index.md)

- Created standards documents in `.project/standards/`:
  - coding.md — Code style, types, architecture
  - documentation.md — Docstrings, README, MkDocs
  - experimentation.md — Experiment protocol
  - governance.md — Project organization, workflow
  - specifications.md — Spec format

- Created `.github/copilot-instructions.md` for AI assistants

**Decisions**:
- Quantum emergence is the long-term target
- Will proceed piece-wise: classical → mixed states → quantum
- CSM is first alternative algorithm to implement
- Project structure now follows plan/record/standards/specifications pattern

**Notes**:
- v0.1.1 successfully released on PyPI
- v0.1.0 yanked due to README documentation link issues
- All CI workflows passing
- Full project context now documented for future AI sessions

---

### January 14, 2026

**Session Focus**: v0.1.1 release

**Completed**:
- Fixed README documentation links (pointed to correct docs URL)
- Released v0.1.1 to PyPI
- User yanked v0.1.0 from PyPI

**Notes**:
- Release workflow working correctly
- TestPyPI made optional in workflow

---

### January 13, 2026

**Session Focus**: First public release

**Completed**:
- Bumped version to 0.1.0
- Created CHANGELOG.md
- Updated pyproject.toml status to Alpha
- Configured release workflow for trusted publishing
- Made CI workflow reusable (added workflow_call)
- Tagged and released v0.1.0

**Issues Encountered**:
- CI workflow not reusable → fixed with workflow_call trigger
- README had old documentation links → led to v0.1.1

---

### January 12, 2026

**Session Focus**: Documentation infrastructure

**Completed**:
- Set up mkdocs with Material theme
- Created full documentation structure:
  - Getting started guide
  - User guide (sources, inference, analysis, pipelines)
  - API reference with mkdocstrings
  - Contributing guide
- Created docs.yml workflow for GitHub Pages
- Added docs build check to CI
- Fixed index.md Material icons issue

**Notes**:
- Documentation deployed to johnazariah.github.io/emic/
- User manually enabled GitHub Pages in repo settings

---

### January 11, 2026

**Session Focus**: README refresh and CI fixes

**Completed**:
- Fixed ruff format errors in errors.py
- Updated README with:
  - Working code examples
  - Current project status
  - Correct etymology pronunciation ("EE-mik")
  - Coverage badge

---

### January 10, 2026

**Session Focus**: CSSR algorithm fixes

**Completed**:
- Fixed empty history handling bug
- Implemented post_merge optimization for state reduction
- Fixed finite-sample state inflation in Even Process

**Tests**: 194 tests passing, 90% coverage

---

### Earlier Work

*[Pre-journal entries not recorded]*

---

## Template

```markdown
### [DATE]

**Session Focus**: [Brief description]

**Completed**:
- Item 1
- Item 2

**In Progress**:
- Item (X% complete)

**Blocked**:
- Item - reason

**Decisions**:
- Decision made and rationale

**Notes**:
- Any other relevant information
```
