# Quantum Complexity Implementation

**Date**: 2026-01-28 / 2026-01-29
**Commits**: `617a0df`, `a044930`

## Goal

Implement quantum complexity measures ($C_q$, $\Delta_q$) for epsilon-machines, starting with the perturbed coin as the canonical validation case. This is foundational infrastructure for the quantum computational mechanics research program.

## What We Did

### 1. Fixed `excess_entropy()` (commit `617a0df`)

The existing implementation was **wrong** - it claimed $E = C_\mu$ for unifilar machines. This is incorrect; that's only true for *co-unifilar* machines (zero crypticity).

- Rewrote using block entropy convergence: $E = \lim_{L \to \infty} [H(X_0^{L-1}) - L \cdot h_\mu]$
- Added `block_entropy(machine, length)` for computing $H(X_0^{L-1})$
- Added `crypticity(machine)` returning $\chi = C_\mu - E$

### 2. Added Perturbed Coin Source

Created `PerturbedCoinSource` - the simplest process with quantum advantage:
- Two states (S0, S1) with symmetric transitions
- Known analytic formulas for all measures
- $C_\mu = 1$ bit always, $C_q$ varies with $p$

### 3. Implemented Quantum Measures (commit `a044930`)

New module `src/emic/analysis/quantum.py`:
- `quantum_signal_states()` - construct $|s_j\rangle$ for each causal state
- `quantum_density_matrix()` - compute $\rho = \sum_j \pi_j |s_j\rangle\langle s_j|$
- `quantum_complexity()` - von Neumann entropy $S(\rho)$
- `quantum_advantage()` - $\Delta_q = C_\mu - C_q$
- `decoherence_trajectory()` - track $C_q(\gamma)$ as $\gamma \to 1$
- `dephasing_channel()` - apply $\mathcal{D}_\gamma(\rho)$

### 4. Created Validation Notebook

`notebooks/quantum_validation.ipynb` with:
- Classical measure validation for perturbed coin
- Quantum complexity vs analytic formula (exact match!)
- Decoherence trajectory visualization
- Golden Mean analysis
- Summary table for multiple processes

## Thought Process

Started with the research program spec (`q001-quantum-research-program.md`) which laid out priorities. The first real task was implementing $C_q$.

But while writing the prerequisites doc, I traced through `excess_entropy()` and noticed it just returned `statistical_complexity()`. That couldn't be right...

**Reasoning chain**:
1. Every ε-machine is unifilar by definition
2. If $E = C_\mu$ for all unifilar machines, then $\chi = 0$ always
3. But papers report non-zero crypticity for Golden Mean, perturbed coin, etc.
4. Therefore the code is wrong, not the papers

This led to fixing `excess_entropy()` before implementing quantum measures - the right call, since we need correct $E$ to validate the hierarchy $E \leq C_q \leq C_\mu$.

## Wrong Turns

### 1. Naive block entropy calculation

My first attempt at understanding block entropy gave:
$$H(X_0^{L-1}) = H(S_0) + (L-1) \cdot h_\mu = C_\mu + (L-1) \cdot h_\mu$$

Which gives $E = C_\mu$... exactly the wrong answer!

**The issue**: This assumes we know the initial state. But block entropy is computed *without* knowing the state - we marginalize over the stationary distribution.

### 2. Validation plan table errors

The validation plan table (supposedly from Gu et al. 2012) had $C_q$ values that violated $E \leq C_q$! For example, at $p=0.10$ it claimed $C_q = 0.469$ but $E = 0.531$.

Our implementation gives $C_q = 0.722$, which correctly satisfies the hierarchy. The table was wrong.

### 3. PYTHONPATH shadowing

Tests were passing but using the wrong code! `/workspace/src` was on PYTHONPATH and shadowing the worktree's local changes. Had to `unset PYTHONPATH` to test properly.

## Key Insight

The quantum signal state construction is elegant:
$$|s_j\rangle = \sum_{k,x} \sqrt{T^{(x)}_{jk}} |x\rangle \otimes |k\rangle$$

Each causal state maps to a vector whose components are square roots of transition probabilities. States that can transition to the same target on the same symbol have non-zero overlap - this is the irreversibility condition that enables quantum advantage.

The density matrix $\rho = \sum_j \pi_j |s_j\rangle\langle s_j|$ is a 4×4 matrix (for 2 states, 2 symbols), but only a 2×2 subspace is non-zero. Its eigenvalues give $C_q$ via von Neumann entropy.

## Open Questions

1. **Why did the validation plan table have wrong values?** Need to check original Gu et al. paper figures more carefully.

2. **Is $C_q(1) = C_\mu$ exact or approximate?** Our decoherence trajectory shows $C_q(1) = 1.0$ for perturbed coin, matching $C_\mu$. Is this always true, or just for this symmetric case?

3. **How to validate Golden Mean $C_q$?** We get $C_q = 0.550$ but don't have a reference value. Need to derive analytically or find in literature.

4. **Spectral methods for $C_q$?** Current implementation enumerates all blocks, which is exponential. Could use matrix methods for larger systems.

## Next Steps

1. Fix the validation plan table with correct $C_q$ values
2. Add unit tests for quantum measures
3. Validate against more processes (Even, Ising spin chain if available)
4. Start Investigation 1: full decoherence trajectory analysis
5. Consider adding `quantum` optional dependency group for scipy/qutip
