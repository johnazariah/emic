# Specification 021: Quantum Computing Deep Dive

*An intuition-first introduction to quantum computing*

**Status**: Complete
**Created**: 2026-01-29
**Location**: `.project/research/quantum-deep-dive/`

---

## Motivation

Existing quantum computing educational resources fall into three camps:

1. **Physics-first**: Schrödinger equation → wavefunctions → qubits. Rigorous but slow.
2. **Circuits-first**: "Qubits are like coins!" → gates → algorithms. Operational but no understanding.
3. **Linear algebra-first**: Vectors, matrices, tensor products. Correct but dry.

None build **conceptual intuition** from first principles. This deep dive aims to fill that gap.

## Core Insight

**Start with density matrices, not kets.**

The density matrix makes the classical/quantum boundary *visible*:
- Diagonal entries = classical probabilities
- Off-diagonal entries = quantum coherence

This single representation unifies pure states, mixed states, measurement, and decoherence.

## Target Audience

- Developers who know linear algebra and probability
- Researchers in computational mechanics wanting quantum background
- Anyone frustrated by "a qubit is 0 and 1 at the same time" non-explanations

## Structure

### Part I: Foundations

| Chapter | Title | Core Intuition |
|---------|-------|----------------|
| 1 | Classical Uncertainty | Probability vectors, Shannon entropy, what "information" means |
| 2 | The Quantum Twist | Complex amplitudes, why phases matter, interference |
| 3 | The Density Matrix | The one object that captures everything. Diagonal = classical, off-diagonal = quantum |
| 4 | Entropy and Purity | Von Neumann entropy, how to measure "how quantum" something is |

### Part II: Core Concepts

| Chapter | Title | Core Intuition |
|---------|-------|----------------|
| 5 | Measurement | Forcing the matrix to become diagonal. Projection operators. |
| 6 | Composite Systems | Tensor products. When dimensions multiply. |
| 7 | Entanglement | States that can't be factored. "Spooky" correlations demystified. |
| 8 | Decoherence | Environment measures you. Off-diagonals decay. The quantum→classical transition. |

### Part III: Computation

| Chapter | Title | Core Intuition |
|---------|-------|----------------|
| 9 | Quantum Gates | Unitary matrices. Rotations on the Bloch sphere (and beyond). |
| 10 | Interference as Computation | The trick: paths that give wrong answers cancel out. |
| 11 | Quantum Algorithms | Deutsch-Jozsa, Grover, Shor — what they actually do. |
| 12 | Why Quantum Speedup? | When interference helps vs. when it doesn't. |

### Part IV: Connections (Optional)

| Chapter | Title | Core Intuition |
|---------|-------|----------------|
| 13 | Quantum vs Classical Complexity | Back to computational mechanics: why $C_q < C_\mu$ |
| 14 | Error Correction | Protecting coherence from decoherence. |
| 15 | Open Questions | What we still don't understand. |

## Principles

1. **Intuition before formalism**: Every equation must be preceded by a conceptual explanation
2. **Concrete examples**: Numbers, not just symbols. Work things out explicitly.
3. **Build incrementally**: Each chapter depends only on previous ones
4. **Density matrices central**: Not an afterthought — the main character
5. **No hand-waving**: If we can't explain it clearly, admit it

## Format

Each chapter:
- ~1000-2000 words
- At least one worked numerical example
- "Key Takeaway" summary box
- "Common Misconceptions" section
- Optional: code snippet demonstrating the concept

## Deliverables

```
.project/research/quantum-deep-dive/
├── 00-overview.md           # Introduction and roadmap
├── 01-classical-uncertainty.md
├── 02-quantum-twist.md
├── 03-density-matrix.md
├── 04-entropy-purity.md
├── 05-measurement.md
├── 06-composite-systems.md
├── 07-entanglement.md
├── 08-decoherence.md
├── 09-quantum-gates.md
├── 10-interference.md
├── 11-algorithms.md
├── 12-why-speedup.md
└── figures/                 # Diagrams, Bloch spheres, etc.
```

## Success Criteria

A reader who completes the deep dive should be able to:

1. Look at a density matrix and immediately identify what's classical vs quantum
2. Explain why measurement destroys superposition (in terms of matrices)
3. Explain entanglement without using "spooky action at a distance"
4. Understand why quantum computers are faster for *some* problems but not all
5. Read quantum computing papers without getting lost in notation

## Dependencies

- Basic linear algebra (matrix multiplication, eigenvalues)
- Probability (distributions, entropy)
- Complex numbers (magnitude, phase)

No physics background required.

## Spin-Out Potential

If this grows beyond this project's scope, it could become:
- A standalone repo with Jupyter notebooks
- A series of blog posts
- A self-paced online course
- Eventually: a short book

For now, it lives here as a research artifact.

---

## Notes

The key pedagogical insight from our discussion:

> "Diagonal matrix = classical. Off-diagonals = quantum coherence = the thing that enables everything quantum."

This should be the recurring refrain throughout.
