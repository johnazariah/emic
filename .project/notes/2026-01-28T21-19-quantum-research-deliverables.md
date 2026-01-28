# Quantum Research Program Deliverables

**Date**: 2026-01-28
**Commit**: 8396e71

## Summary

Created 7 priority deliverables for the quantum computational mechanics research program, following the specification in `q001-quantum-research-program.md`.

---

## Context & Motivation

The research program is exploring **quantum computational mechanics** - the idea that quantum models can be more memory-efficient than classical ones. The central result (Gu et al. 2012) is:

$$E \leq C_q \leq C_\mu$$

where:
- $C_\mu$ = classical statistical complexity (memory in classical ε-machine)
- $C_q$ = quantum statistical complexity (memory in optimal quantum model)
- $E$ = excess entropy (mutual information between past and future)

The gap $C_\mu - C_q$ represents "quantum advantage" - memory saved by using quantum encoding.

### Why This Matters

Classical ε-machines must distinguish causal states **orthogonally** (perfectly distinguishable). But sometimes two states eventually merge - the information distinguishing them is lost. Classical models store this information anyway.

Quantum models can encode states **non-orthogonally**. They only distinguish states to the degree needed. This eliminates the "waste."

### The Research Question

The spec poses: *"Can we estimate $C_q$ directly from finite data?"* This has never been done. The plan:

1. First, build infrastructure by implementing quantum complexity measures for *known* ε-machines
2. Study how $C_q$ interpolates to $C_\mu$ under decoherence
3. Eventually, try estimating from data

---

## Documents Created

### Priority 1: QC Primer
**File**: `.project/research/quantum-emergence/qc-primer.md`

Quantum computing foundations needed for quantum computational mechanics:
- Ket/bra notation and Hilbert spaces
- Density matrices (pure vs mixed states)
- Von Neumann entropy with eigenvalue computation examples
- Decoherence channels (dephasing step-by-step)
- Connection to computational mechanics concepts

### Priority 1b: Prerequisites
**File**: `.project/research/quantum-emergence/prerequisites.md`

Identified gaps in emic's classical implementation that must be fixed before quantum work:
- **Critical**: `excess_entropy()` incorrectly returns $C_\mu$ instead of proper $E$
- Explains why this matters: crypticity $\chi = C_\mu - E$ measures classical waste
- Without correct $E$, quantum advantage analysis is impossible

### Priority 2: Technical Deep Dive
**File**: `docs/guide/quantum-advantage-explained.md`

Explains why quantum models are more efficient than classical:
- Uses perturbed coin example with concrete numbers
- Shows non-orthogonal encoding eliminates "classical waste"
- Includes the key inequality: $E \leq C_q \leq C_\mu$

### Priority 3: Mathematical Framework
**File**: `.project/research/quantum-emergence/framework.md`

Precise definitions for implementation:
- Quantum causal states as density matrices
- Von Neumann entropy formulas
- Quantum statistical complexity $C_q$
- Decoherence trajectory formalization

### Priority 4: Literature Synthesis
**File**: `.project/research/quantum-emergence/synthesis.md`

Timeline of key results:
- Main players (Gu, Crutchfield, Mile Gu's group)
- What's proven vs conjectured
- Key papers with contributions

### Priority 5: Validation Plan
**File**: `.project/research/quantum-emergence/validation-plan.md`

Golden test cases with known values from papers:
- Perturbed coin (Gu et al. 2012)
- Golden Mean process
- Ising model (Aghamohammadi et al. 2017)

### Priority 6: Design Specification
**File**: `.project/specifications/q002-quantum-extension.md`

Types, API, and dependencies for implementation:
- `QuantumCausalState` dataclass
- `QuantumMachine` protocol
- Dependency on `qutip` library
- Phased implementation plan

## Key Insight

The core technical insight documented across these files:

> Classical ε-machines must distinguish causal states orthogonally (perfectly distinguishable). But when two states can transition to the same future state, the information distinguishing them is **irreversibly lost**. Classical models store this information anyway - it's "waste."
>
> Quantum models encode states **non-orthogonally** - they only distinguish states to the degree needed for correct output statistics. This eliminates the waste, giving $C_q < C_\mu$.

### How Quantum Encoding Works

The quantum model assigns each causal state $s_i$ a pure state $|\eta_i\rangle$ such that:

$$\langle \eta_i | \eta_j \rangle = \frac{\sum_x \sqrt{P(x|s_i) P(x|s_j)} \langle \eta_{s_i(x)} | \eta_{s_j(x)} \rangle}{1}$$

This recursive formula ensures states are only as distinguishable as needed. The quantum statistical complexity is:

$$C_q = S(\rho) = -\text{tr}(\rho \log_2 \rho)$$

where $\rho = \sum_i \pi_i |\eta_i\rangle\langle\eta_i|$ is the mixed state.

---

## Writing Process

The documents were created in priority order from the spec:

1. **QC Primer** came first - needed to establish quantum foundations before anything else. Focused on density matrices and von Neumann entropy since those are the key tools.

2. **Prerequisites** was written next, and this is where I discovered the excess_entropy bug. While documenting what emic *should* do, I read the code and found it was wrong.

3. **Technical Deep Dive** required thinking about how to explain quantum advantage to someone who knows classical computational mechanics but not quantum. The perturbed coin is the simplest example.

4. **Framework** is the mathematical core - precise definitions for implementation.

5. **Synthesis** required reading through all the papers in `.project/references/` and constructing a timeline.

6. **Validation Plan** extracts known values from papers to use as golden tests.

7. **Design Spec** translates the math into types and APIs.

---

## Next Steps

1. ~~Fix the `excess_entropy()` bug identified in prerequisites~~ ✓ Done (see other note)
2. Implement quantum complexity measures
3. Validate against known values from papers
