# Decoherence Trajectory Investigation

**Date**: 2026-01-29
**Commits**: `420c961`, `13141a5`, `239467d`, `8da4873`

## Goal

Execute Investigation 1 from the quantum research program: trace how quantum complexity $C_q(\gamma)$ evolves under dephasing from the pure quantum value ($\gamma=0$) to a fully dephased state ($\gamma=1$).

Key questions:
1. What is the functional form of $C_q(\gamma)$?
2. Is the trajectory convex, concave, or linear?
3. How does it depend on process parameters?

## What We Did

1. **Created `notebooks/decoherence_trajectory.ipynb`** - Complete investigation notebook with:
   - Perturbed Coin trajectories at p = 0.1, 0.2, 0.3, 0.4, 0.5
   - Comparison with Golden Mean and Even Process
   - Concavity analysis via numerical second derivatives
   - Signal state overlap analysis
   - Density matrix examination for anomalous cases

2. **Fixed validation plan table** - The original `validation-plan.md` had $C_q$ values that violated the hierarchy $E \leq C_q \leq C_\mu$. Corrected using analytic formulas.

3. **Discovered the Even Process anomaly** - For processes with orthogonal signal states, dephasing can *increase* entropy beyond $C_\mu$!

## Thought Process

Started by implementing the simplest case: perturbed coin at various p values. The `decoherence_trajectory()` function was already in place from earlier work, so just needed to call it and plot.

When I saw all curves were concave, wanted to verify quantitatively. Used numerical second derivatives - confirmed $d^2 C_q / d\gamma^2 < 0$ everywhere.

Then wondered: is this universal? Added Golden Mean and Even Process for comparison.

## Wrong Turns

**The Even Process surprise**: Expected all trajectories to start at $C_q$ and end at $C_\mu$. But the Even Process showed $C_q(\gamma=1) = 1.585$ vs $C_\mu = 0.918$!

Initially thought this was a bug. But examining the density matrix revealed:
- At $\gamma=0$: eigenvalues {0, 0, 1/3, 2/3}, entropy = 0.918
- At $\gamma=1$: eigenvalues {0, 1/3, 1/3, 1/3}, entropy = 1.585

Dephasing removes off-diagonal coherences in the product Hilbert space, but this doesn't "return to classical" — it spreads the eigenvalues more uniformly, increasing entropy!

## Key Insight

**Dephasing ≠ classicalization**. The "classical complexity" $C_\mu$ is the entropy of the stationary distribution over causal states. The dephased density matrix is something different — it's the original quantum state with coherences removed, not the classical mixed state.

This matters for interpretation: the decoherence trajectory only meaningfully interpolates between quantum and classical for processes with non-orthogonal signal states (i.e., processes that have quantum advantage).

## Open Questions

1. **Is concavity provable?** Can we derive $C_q''(\gamma) < 0$ analytically for all processes with quantum advantage?

2. **What's the correct classical endpoint?** If dephasing doesn't give $C_\mu$, what operation does? Maybe we need to project onto the computational basis in a different way.

3. **Physical interpretation**: What does the trajectory shape tell us about fragility of quantum advantage under real decoherence mechanisms (not just dephasing)?

## Next Steps

1. Add unit tests for `decoherence_trajectory()` with known values
2. Investigate the mathematical structure: why is it concave?
3. Consider alternative decoherence channels (amplitude damping, depolarizing)
4. Update the framework document with these findings
