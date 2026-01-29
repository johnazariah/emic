# Quantum Computing Deep Dive

*An intuition-first introduction to quantum computing*

---

## What This Is

This is not a textbook. It's a conceptual guide that builds intuition from first principles.

The core insight: **density matrices reveal everything**.
- Diagonal = classical probability
- Off-diagonal = quantum coherence

Once you see this, quantum mechanics stops being mysterious.

## Roadmap

### Part I: Foundations
1. [Classical Uncertainty](01-classical-uncertainty.md) — Probability, entropy, information
2. [The Quantum Twist](02-quantum-twist.md) — Complex amplitudes and interference
3. [The Density Matrix](03-density-matrix.md) — The one object that captures everything
4. [Entropy and Purity](04-entropy-purity.md) — Measuring "how quantum" something is

### Part II: Core Concepts
5. [Measurement](05-measurement.md) — Forcing diagonality
6. [Composite Systems](06-composite-systems.md) — Tensor products
7. [Entanglement](07-entanglement.md) — States that can't be factored
8. [Decoherence](08-decoherence.md) — How quantum becomes classical

### Part III: Computation
9. [Quantum Gates](09-quantum-gates.md) — Unitary rotations
10. [Interference as Computation](10-interference.md) — The core trick
11. [Quantum Algorithms](11-algorithms.md) — What they actually do
12. [Why Quantum Speedup?](12-why-speedup.md) — When it helps, when it doesn't

### Part IV: Connections
13. [Quantum vs Classical Complexity](13-quantum-vs-classical-complexity.md) — Why $C_q < C_\mu$
14. [Error Correction](14-error-correction.md) — Protecting coherence
15. [Open Questions](15-open-questions.md) — What we don't know

## Prerequisites

- Basic linear algebra (matrices, eigenvalues)
- Probability (distributions, entropy)
- Complex numbers (magnitude, phase)

No physics background needed.

## The Punchline

If you take away one thing:

> **Diagonal = classical. Off-diagonal = quantum.**

Everything else is elaboration.

---

*See [Specification 021](../../specifications/021-quantum-computing-deep-dive.md) for project details.*
