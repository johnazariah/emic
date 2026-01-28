# Quantum Computational Mechanics Research Program

You are helping with the `emic` project - a Python library for computational mechanics (inferring epsilon-machines from time series data). We are extending it to support quantum complexity measures.

## Context

Computational mechanics studies the structure of stochastic processes through "epsilon-machines" - minimal predictive models. Recent research (Gu et al. 2012, Thompson et al. 2018) shows that quantum models can be strictly more efficient than classical ones. The quantum statistical complexity $C_q$ can be less than the classical $C_\mu$, with the gap representing "classical waste" that quantum encoding eliminates.

## Your Task

Execute the research program specified in:
`.project/specifications/020-quantum-research-program.md`

This specification contains:
- Research questions and rationale
- Deliverable artifacts with file paths
- Detailed algorithm for Investigation 1 (Decoherence Trajectory)
- Type definitions and pseudocode
- Success criteria

## Priority Order for Artifacts

1. **QC Primer** (`.project/research/quantum-emergence/qc-primer.md`) - Quantum computing foundations needed for this work. Focus on density matrices, von Neumann entropy, and decoherence channels. Include worked examples with actual numbers.

2. **Prerequisites** (`.project/research/quantum-emergence/prerequisites.md`) - Gaps in emic's classical implementation that must be fixed first (excess entropy computation is currently wrong).

3. **Technical Deep Dive** (`docs/guide/quantum-advantage-explained.md`) - Explain why quantum models are more efficient. Use the perturbed coin example with concrete numbers.

4. **Mathematical Framework** (`.project/research/quantum-emergence/framework.md`) - Precise definitions for implementation.

5. **Literature Synthesis** (`.project/research/quantum-emergence/synthesis.md`) - Timeline of key results, main players, what's proven vs conjectured.

6. **Validation Plan** (`.project/research/quantum-emergence/validation-plan.md`) - Golden test cases with known values from papers.

7. **Design Specification** (`.project/specifications/017-quantum-extension.md`) - Types, API, dependencies for implementation.

## Key Resources

- Full paper extractions in `.project/references/*/..._full.md`
- Paper catalog: `.project/references/CATALOG.md`
- Existing concepts doc: `.project/research/quantum-emergence/review/concepts.md`
- Key papers doc: `.project/research/quantum-emergence/review/key-papers.md`
- Current emic analysis code: `src/emic/analysis/measures.py`

## Key Papers to Reference

1. **Gu et al. 2012** - "Occam's Quantum Razor" (foundational) - `.project/references/gu2012quantum/`
2. **Thompson et al. 2018** - "Causal Asymmetry in a Quantum World" (Crutchfield-Gu collaboration) - `.project/references/thompson2018causal/`
3. **Garner et al. 2017** - "Unbounded Memory Advantage" - `.project/references/garner2017unbounded/`
4. **Tan et al. 2014** - "Towards Quantifying Complexity with Quantum Mechanics" - `.project/references/tan2014towards/`
5. **Aghamohammadi et al. 2017** - "Extreme Quantum Advantage" (Ising model) - `.project/references/aghamohammadi2017extreme/`

## Novel Research Direction

Our ultimate goal is answering: **"Can we estimate quantum complexity $C_q$ directly from finite data?"** This has never been done.

The decoherence trajectory investigation (Investigation 1 in the spec) builds the infrastructure needed while potentially producing a standalone publishable result.

## The Core Technical Insight

Classical ε-machines must distinguish causal states orthogonally (perfectly distinguishable). But when two states can transition to the same future state, the information distinguishing them is **irreversibly lost**. Classical models store this information anyway - it's "waste."

Quantum models encode states **non-orthogonally** - they only distinguish states to the degree needed for correct output statistics. This eliminates the waste, giving $C_q < C_\mu$.

## Style Guidelines

- Follow project standards in `.project/standards/`
- Use LaTeX math notation in markdown (e.g., `$C_\mu$`, `$$E = I(\overleftarrow{X}; \overrightarrow{X})$$`)
- Include concrete numerical examples, not just formulas
- Cross-reference between documents
- The audience is a developer/researcher who knows classical computational mechanics but not quantum

## Research Notes & Breadcrumbs

**Critical**: This is exploratory research into uncharted territory. Capture reasoning, not just results.

After completing work, create a note in `.project/notes/` with filename format:
`YYYY-MM-DDTHH-MM-<short-description>.md`

Each note should include:

1. **Discovery process** - How did you find/understand this? What led you here?
2. **Wrong turns** - What approaches failed? What misconceptions did you have?
3. **Reasoning chain** - The "wait, that can't be right" moments and how they resolved
4. **Key insights** - The "aha" that made things click
5. **Implementation notes** - Gotchas, edge cases, things that surprised you
6. **References** - Which papers/equations were consulted

**Why this matters**: Future sessions (human or AI) will need to understand not just *what* was done but *why* and *how*. The exploration is as valuable as the conclusion.

**Example**: When fixing `excess_entropy()`, the note captured:
- The bug was found while writing prerequisites docs (not while looking for bugs)
- The conceptual error: confusing "unifilar" with "co-unifilar"
- A wrong turn: naive block entropy calculation that gave E = C_μ
- The fix: finding equation (27) in the James et al. paper
- A gotcha: PYTHONPATH shadowing the worktree code

## Starting Point

Start with the **QC Primer** - it's foundational for everything else. The primer should be a working reference with:
- Ket/bra notation
- Density matrices
- Von Neumann entropy (with eigenvalue computation example)
- Decoherence channels (dephasing step-by-step)
- Connection to computational mechanics concepts

Then proceed through the priority list, checking off each deliverable.
