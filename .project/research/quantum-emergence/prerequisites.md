# Prerequisites: Classical Gaps to Fix Before Quantum Work

*Gaps in emic's classical implementation that must be addressed before quantum extension*

---

## Overview

Before implementing quantum complexity measures ($C_q$, causal asymmetry, etc.), we need a correct classical foundation. This document identifies specific gaps in the current emic implementation.

**Priority order:**
1. Fix excess entropy computation (critical - currently returns wrong values)
2. Implement crypticity properly (depends on #1)
3. Add reverse machine construction (needed for causal asymmetry)
4. Consider bidirectional analysis infrastructure

---

## Gap 1: Excess Entropy Computation (CRITICAL)

### Current State

In [measures.py](../../src/emic/analysis/measures.py#L130-L147):

```python
def excess_entropy(machine: EpsilonMachine[A]) -> float:
    """
    ...
    For unifilar machines (which epsilon-machines are):
    E = Cμ (statistical complexity equals excess entropy)
    ...
    """
    # For unifilar machines, excess entropy equals statistical complexity
    return statistical_complexity(machine)
```

**This is WRONG.**

### The Error

The code assumes: *"For unifilar machines, E = Cμ"*

This confuses two properties:
- **Unifilarity**: Past uniquely determines current state → $H[S | \overleftarrow{S}] = 0$
- **Crypticity = 0**: Future uniquely determines current state → $H[S | \overrightarrow{S}] = 0$

Every ε-machine is unifilar by construction, but most have nonzero crypticity!

### The Math

From Shalizi & Crutchfield (2001), Theorem 5:

$$E = I(\overleftarrow{S}; \overrightarrow{S}) = H[S] - H[S | \overrightarrow{S}] = C_\mu - \chi$$

where:
- $E$ = excess entropy (mutual information between past and future)
- $C_\mu = H[S]$ = statistical complexity
- $\chi = H[S | \overrightarrow{S}]$ = crypticity (how much state info is hidden from future)

Equality $E = C_\mu$ holds **if and only if** $\chi = 0$, meaning the future determines the state.

### Concrete Example: Perturbed Coin

The perturbed coin has:
- $C_\mu = 1$ bit (two equally likely states)
- $E = 1 - H_s(p)$ where $H_s(p) = -p\log p - (1-p)\log(1-p)$

For $p = 0.4$:
- $C_\mu = 1$ bit
- $H_s(0.4) = 0.971$ bits
- $E = 0.029$ bits
- $\chi = 0.971$ bits

The current code would return $E = 1$ bit, which is **35× too large**!

### Impact

Since crypticity is computed as `c_mu - e`:
- Current: $\chi = C_\mu - C_\mu = 0$ (always zero!)
- Correct: $\chi = C_\mu - E$ (usually positive)

This breaks the quantum research because:
- Crypticity $\chi$ measures "classical waste" that quantum eliminates
- If $\chi = 0$, there's no quantum advantage (which is false)
- Validation against papers will fail

### How to Fix

Computing excess entropy properly requires either:

**Option A: Limit computation (exact for infinite data)**

$$E = \lim_{L \to \infty} I(X_{-L}^{-1}; X_0^{L-1})$$

This requires computing block entropies at increasing lengths and extrapolating.

**Option B: From ε-machine structure**

From Crutchfield & Feldman (2003), for finite-state processes:

$$E = C_\mu + h_\mu \cdot \tau - H_{L}$$

where $\tau$ is a characteristic convergence time and $H_L$ is block entropy.

**Option C: Via reverse machine (most principled)**

$$E = C_\mu + C_\mu^+ - I(S^-; S^+)$$

where:
- $C_\mu^+$ = complexity of reverse-time ε-machine
- $S^-$ = forward causal state
- $S^+$ = reverse causal state
- $I(S^-; S^+)$ = mutual information between them

This requires building the reverse machine.

### Recommended Approach

For the quantum work, we need at least Option C because:
1. Causal asymmetry = $C_\mu^+ - C_\mu$ (requires reverse machine anyway)
2. Thompson et al. (2018) studies bidirectional machines extensively
3. Most principled and matches the literature

---

## Gap 2: Crypticity Computation

### Current State

Crypticity is computed in [summary.py](../../src/emic/analysis/summary.py#L96):

```python
crypticity=c_mu - e,
```

This is correct **in formula** but gives wrong results because `e` is wrong (Gap 1).

### After Fixing Gap 1

Once excess entropy is correct, this formula will work. No additional changes needed.

### Alternative Direct Computation

Crypticity can also be computed directly as:

$$\chi = H[S | \overrightarrow{S}]$$

This measures uncertainty about the current state given complete knowledge of the future. For finite-state machines, this can be computed from the reverse machine.

---

## Gap 3: Reverse Machine Construction

### Why Needed

The **reverse-time ε-machine** captures the structure of retrodiction (predicting the past from the future). It's essential for:

1. **Excess entropy** (Option C above)
2. **Causal asymmetry**: $\Delta C = C_\mu^+ - C_\mu^-$
3. **Bidirectional complexity**: Thompson et al. (2018) key metric

### What It Is

Given a stationary process, there's a "time-reversed" process with:
- Reversed arrow of time: future becomes past
- Its own causal states (reverse causal states)
- Its own ε-machine (the **retrodictive** or **reverse** machine)

### Construction

From Shalizi & Crutchfield (2001), Appendix C:

1. Define reverse equivalence: pasts with same *past*-prediction distributions
2. Build reverse causal states from these equivalences
3. Compute reverse transitions and stationary distribution

For an already-known ε-machine, the reverse machine can be derived without re-running CSSR.

### Implementation Sketch

```python
@dataclass(frozen=True)
class ReverseMachine(Generic[A]):
    """Reverse-time epsilon-machine."""
    forward_machine: EpsilonMachine[A]
    reverse_states: tuple[CausalState[A], ...]
    state_mapping: dict[StateId, frozenset[StateId]]  # reverse → forward
```

Key computation: the joint distribution over (forward state, reverse state) pairs.

### Priority

**High** — needed for both correct excess entropy and causal asymmetry.

---

## Gap 4: Bidirectional Analysis Infrastructure

### Why Needed

Thompson et al. (2018) — a key paper for quantum extension — studies bidirectional machines that can predict forward AND retrodict backward.

Key finding: Quantum models can achieve bidirectional prediction with bounded memory even when classical requires unbounded.

### What's Needed

1. **Joint state representation**: Track both forward and reverse states
2. **Bidirectional complexity**: $C_\mu^\pm$ measures
3. **Information flow analysis**: How information moves between directions

### Implementation Sketch

```python
@dataclass(frozen=True)
class BidirectionalMachine(Generic[A]):
    """Combined forward and reverse epsilon-machine."""
    forward: EpsilonMachine[A]
    reverse: EpsilonMachine[A]
    joint_distribution: dict[tuple[StateId, StateId], float]

    @property
    def causal_asymmetry(self) -> float:
        """ΔC = C_μ⁺ - C_μ⁻"""
        return self.reverse.statistical_complexity - self.forward.statistical_complexity

    @property
    def excess_entropy(self) -> float:
        """E = C_μ⁻ + C_μ⁺ - I(S⁻; S⁺)"""
        c_fwd = statistical_complexity(self.forward)
        c_rev = statistical_complexity(self.reverse)
        mutual_info = self._compute_joint_mutual_info()
        return c_fwd + c_rev - mutual_info
```

### Priority

**Medium** — builds on Gap 3, enables full Thompson et al. validation.

---

## Implementation Plan

### Phase 1: Minimal Fix (Required for Quantum Work)

1. **Acknowledge the bug** in docstrings
2. **Add warning** when `excess_entropy()` is called
3. **Implement stub** that raises `NotImplementedError` for non-trivial cases
4. **Add known-value tests** that currently fail (mark as xfail)

### Phase 2: Core Fix (Block Entropy Method)

1. Implement block entropy computation $H(X_0^{L-1})$
2. Implement block mutual information $I(X_{-L}^{-1}; X_0^{L-1})$
3. Extrapolate to limit using known convergence properties
4. Validate against simple processes (biased coin, golden mean)

### Phase 3: Full Implementation (Reverse Machine)

1. Implement reverse machine construction
2. Compute joint (forward, reverse) state distribution
3. Derive excess entropy and crypticity from joint structure
4. Enable causal asymmetry computation

### Phase 4: Quantum Foundation

With correct classical measures, we can:
1. Compute $\chi = C_\mu - E$ correctly → predicts quantum advantage
2. Build q-machines with known validation targets
3. Verify $C_q \leq C_\mu$ with equality when $\chi = 0$

---

## Validation Cases

| Process | $C_\mu$ | $E$ | $\chi$ | Notes |
|---------|---------|-----|--------|-------|
| Fair coin | 0 | 0 | 0 | No memory needed |
| Biased coin ($p$) | 0 | 0 | 0 | Still no memory |
| Golden mean | 0.918 | ? | ? | Need to verify |
| Even process | 1.0 | ? | ? | Need to verify |
| Perturbed coin ($p=0.4$) | 1.0 | 0.029 | 0.971 | High crypticity |
| Perturbed coin ($p=0.1$) | 1.0 | 0.531 | 0.469 | From Gu et al. |

---

## References

1. Shalizi, C.R. & Crutchfield, J.P. "Computational Mechanics: Pattern and Prediction, Structure and Simplicity." J. Stat. Phys. 104, 817 (2001)
2. Crutchfield, J.P. & Feldman, D.P. "Regularities Unseen, Randomness Observed." Chaos 13, 25 (2003)
3. Thompson, J. et al. "Causal Asymmetry in a Quantum World." Phys. Rev. X 8, 031013 (2018)

---

*Document version: 1.0*
*Created: 2026-01-28*
*Status: Action required before quantum implementation*
