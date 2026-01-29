# Quantum Advantage Taxonomy: Complete Characterization

**Date**: 2026-01-29
**Commits**: `c5c840d`, `6ff69e7`, `921b3cb`, `d518b8a`

## Goal

Validate the quantum complexity implementation against multiple process types and characterize precisely when quantum advantage occurs.

## What We Did

1. **Extended test suite from 30 to 53 tests**
   - Added `TestEvenProcess` (4 tests): orthogonal signal states
   - Added `TestPeriodicProcesses` (11 tests): deterministic processes
   - Added `TestQuantumAdvantageTaxonomy` (5 tests): conditions for advantage
   - Added `TestSignalStateOverlap` (3 tests): overlap formula verification

2. **Ran comprehensive validation notebook**
   - Validated 10 processes across 4 categories
   - Generated visualization comparing $C_\mu$ vs $C_q$
   - Documented taxonomy in markdown cells

3. **Ran decoherence trajectory investigation**
   - Confirmed trajectories are strictly concave
   - Discovered Even Process anomaly ($C_q(1) > C_\mu$)

## Thought Process

Started by running the existing validation notebook, then systematically added more process types to understand the pattern. The key question was: "What distinguishes processes WITH quantum advantage from those WITHOUT?"

Tested:
- IID (biased coin) → no advantage
- Deterministic (periodic) → no advantage
- Even process (2 states, asymmetric) → no advantage
- Golden mean (2 states, asymmetric) → HAS advantage
- Perturbed coin (2 states, symmetric) → HAS advantage

The pattern emerged: it's not about number of states, it's about **whether paths merge**.

## Key Insight

**Quantum advantage occurs if and only if signal states have non-zero overlap.**

Mathematically: $\Delta_q > 0$ ⟺ $\exists j \neq k: \langle s_j | s_k \rangle > 0$

This happens when different causal states can **both** transition to the **same** future state via the **same** symbol. In graph terms: "paths merge."

## The Overlap Formula

$$\langle s_j | s_k \rangle = \sum_{x,l} \sqrt{T^{(x)}_{jl} T^{(x)}_{kl}}$$

Non-zero when $\exists x, l$ such that both $T^{(x)}_{jl} > 0$ AND $T^{(x)}_{kl} > 0$.

## Taxonomy

| Process Type | States | Advantage | Reason |
|--------------|--------|-----------|--------|
| IID | 1 | ❌ | Pure signal state → $C_q = 0$ |
| Deterministic | N | ❌ | Unique outputs → orthogonal |
| Even Process | 2 | ❌ | $S_1$ can only emit 1 → disjoint futures |
| Golden Mean | 2 | ✅ 40% | Both states can reach $S_0$ via 0 |
| Perturbed Coin | 2 | ✅ up to 100% | Symmetric merging → max overlap |

## Wrong Turns

1. Initially thought "2 states = quantum advantage" but Even Process disproves this
2. Thought decoherence trajectory always gives $C_q(1) = C_\mu$, but learned this only holds for special cases

## Physical Interpretation

The quantum advantage represents **information destined to be lost**.

When two different histories will inevitably merge into the same future, a classical model must distinguish them anyway. A quantum model encodes them non-orthogonally — just distinguishable enough for correct predictions, but no more.

It's like two roads merging into one highway: a classical counter remembers which road each car came from, even though that information becomes irrelevant once they're on the highway.

## Open Questions

1. **Is there a simple graph-theoretic criterion?** Something like "the transition graph is not co-deterministic" (reverse graph has non-deterministic transitions)?

2. **Can we compute overlap without constructing signal states?** Direct formula from transition matrices?

3. **What's the relationship between overlap and advantage?** Is $\Delta_q$ monotonic in max overlap?

## Next Steps

1. Write up "quantum advantage explained" guide for docs
2. Test more exotic processes (Ising model, R-k processes)
3. Explore the co-determinism / co-unifilarity connection
4. Consider property-based tests with Hypothesis

## Files Changed

- `tests/unit/test_quantum.py`: 53 tests (was 30)
- `notebooks/quantum_validation.ipynb`: Full validation with analysis
- `.project/notes/2026-01-29T07-25-decoherence-trajectory-findings.md`: Earlier findings
