# Decoherence Trajectory Investigation Findings

**Date**: 2026-01-29
**Commits**: c5c840d

## Goal

Run the decoherence trajectory investigation from spec q001 to understand how $C_q(\gamma)$ interpolates between quantum and classical complexity under dephasing.

## What We Did

1. Ran the existing `notebooks/decoherence_trajectory.ipynb` with full cell execution
2. Analyzed trajectories for:
   - Perturbed coin (p = 0.1, 0.2, 0.3, 0.4, 0.5)
   - Golden mean process
   - Even process
3. Computed second derivatives to verify concavity
4. Discovered unexpected behavior for even process

## Key Findings

### 1. Trajectories Are Strictly Concave

All second derivatives are negative:
```
p=0.1: d²C_q/dγ² at γ=0.1: -0.73, at γ=0.5: -0.57
p=0.3: d²C_q/dγ² at γ=0.1: -3.80, at γ=0.5: -1.53
p=0.5: d²C_q/dγ² at γ=0.1: -7.64, at γ=0.5: -1.92
```

Physical interpretation: Quantum advantage decays **faster initially** and **slower later**. The first bits of decoherence are most damaging.

### 2. Even Process Anomaly

The even process has:
- Zero quantum advantage ($C_q = C_\mu = 0.918$)
- Zero signal state overlap (states are orthogonal)
- But $C_q(1) = 1.585 > C_\mu$!

**Why?** The density matrix lives in $\mathcal{H}_\text{states} \otimes \mathcal{H}_\text{symbols}$ (4D for even process). Dephasing removes off-diagonal coherences in this space, but the diagonal entropy $H(\text{diag}(\rho))$ is NOT the same as $H(\pi)$.

For even process:
- $\text{diag}(\rho) = (0, 1/3, 1/3, 1/3)$
- $H(\text{diag}(\rho)) = \log_2(3) \approx 1.585$
- But $\pi = (2/3, 1/3)$, so $H(\pi) \approx 0.918$

### 3. Why Perturbed Coin Works

For perturbed coin with uniform stationary distribution $\pi = (0.5, 0.5)$:
- $\text{diag}(\rho) = (0, 0.5, 0.5, 0)$
- $H(\text{diag}(\rho)) = 1$ bit = $H(\pi) = C_\mu$

The accident of uniform $\pi$ makes $C_q(1) = C_\mu$.

## Thought Process

Started by running the existing notebook, expecting all trajectories to interpolate from $C_q$ to $C_\mu$. When the even process showed $C_q(1) > C_\mu$, initially thought it was a bug.

Investigated by:
1. Checking the density matrix structure
2. Comparing diagonal entries to stationary distribution
3. Realizing the tensor product structure creates mismatch

The key insight: **dephasing in Hilbert space ≠ returning to classical model**

## Wrong Turns

1. Initially thought dephasing should always give $C_q(1) = C_\mu$
2. Considered "fixing" the dephasing channel to dephase in a different basis
3. Realized this is actually correct behavior — the dephasing channel describes physical decoherence, not abstract projection to classical complexity

## Key Insight

The decoherence trajectory is about **physical quantum coherence decay**, not about measuring "how classical" a model is. For processes with non-trivial state structure, full dephasing can give **higher** entropy than the classical complexity because it's measuring entropy in a higher-dimensional space.

The trajectory $C_q(0) \to C_q(1)$ is meaningful for understanding:
- How robust quantum advantage is to noise
- What fraction of quantum coherence is needed for advantage
- The "fragility" of quantum memory savings

But it's NOT a trajectory toward $C_\mu$ in general.

## Open Questions

1. **What basis should dephasing use?** Could define dephasing in the signal-state basis instead of computational basis. Would this give $C_q(1) = C_\mu$?

2. **Is there a modified trajectory that always interpolates to $C_\mu$?** Perhaps using the depolarizing channel instead?

3. **What's the physical significance of $H(\text{diag}(\rho))$?** It's the entropy of the joint (state, symbol) distribution marginalized over quantum coherences.

## Next Steps

1. Consider implementing dephasing in the signal-state basis
2. Document this finding in the quantum advantage guide
3. Add a warning to `decoherence_trajectory()` docstring about edge cases
4. Explore depolarizing channel as alternative
