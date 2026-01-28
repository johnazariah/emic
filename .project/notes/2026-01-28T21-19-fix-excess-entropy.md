# Fix: Excess Entropy Using Block Entropy Convergence

**Date**: 2026-01-28
**Commit**: 617a0df

## Summary

Fixed a critical bug in `excess_entropy()` that was returning $C_\mu$ instead of the correct excess entropy $E$. This fix is essential for the quantum extension work.

---

## Discovery Process

The bug was discovered while writing the **prerequisites document** for quantum work. I was documenting what emic *should* do, and traced through the `excess_entropy()` code. That's when I noticed it just returned `statistical_complexity()` with a comment claiming "for unifilar machines, E = C_μ."

**First reaction**: *Wait, that can't be right.*

Here's the reasoning chain that led to finding the bug:

1. **Every ε-machine is unifilar by definition** - that's what makes it an ε-machine. So if E = C_μ for all unifilar machines, then E = C_μ *always*, making crypticity χ = 0 always.

2. **But papers report non-zero crypticity.** The Golden Mean has significant crypticity. That's literally the point of several Crutchfield papers.

3. **So either the papers are wrong, or the code is wrong.** Given Crutchfield's decades of work, I was pretty confident it was the code.

4. **Tracing the conceptual error**: The code confused "unifilar" (past determines state) with "co-unifilar" (future determines state). These are different! For E = C_μ you need *both*.

### The Wrong Turn

My first attempt at understanding led me astray. I tried the "naive" block entropy calculation:

$$H(X_0^{L-1}) = H(S_0) + \sum_{k=0}^{L-2} H(X_k | S_k) = C_\mu + (L-1) \cdot h_\mu$$

Which gives $E = C_\mu$... exactly the wrong answer!

**The issue**: This assumes we *know* the initial state. But block entropy $H(X_0^{L-1})$ is the entropy of the block when we *don't* know the state - we only have the stationary distribution over states.

### Finding the Right Formula

Went to the James, Ellison, Crutchfield (2011) "Anatomy of a Bit" paper in `.project/references/`. Found equation (27):

$$E = \sum_{\ell=1}^{\infty} (h_\ell - h_\mu)$$

where $h_\ell = H(X_{\ell-1} | X_0^{\ell-2})$ is the conditional entropy given the *observed history*, not the state.

This is the key insight: $h_\ell$ converges to $h_\mu$ from above. The "excess" at each step sums to give $E$.

Equivalently:
$$H(L) = E + L \cdot h_\mu + \text{(transient terms)}$$

So we compute block entropies, subtract $L \cdot h_\mu$, and watch it converge to $E$.

---

## The Problem

The previous implementation incorrectly claimed:

> "For unifilar machines, E = C_μ"

This is **wrong**. It confused two different properties:

| Property | Meaning |
|----------|---------|
| **Unifilarity** | Given past, state is unique |
| **Zero crypticity** | Given future, state is unique (co-unifilarity) |

All ε-machines are unifilar by definition, but most have positive crypticity ($\chi > 0$).

## The Fix

Rewrote `excess_entropy()` using block entropy convergence (James et al. 2011):

$$E = \lim_{L \to \infty} [H(X_0^{L-1}) - L \cdot h_\mu]$$

The excess entropy is the subextensive component of block entropy growth - the part that doesn't scale with block length.

## New Functions Added

### `block_entropy(machine, length) -> float`
Computes block entropy $H(X_0^{L-1})$ by enumerating all L-blocks and computing their probability distribution.

### `crypticity(machine) -> float`
Computes $\chi = C_\mu - E$, the "hidden" information in causal states that doesn't contribute to prediction.

## Verified Values

For the **Golden Mean process** (p=0.5):

| Measure | Value | Description |
|---------|-------|-------------|
| $C_\mu$ | 0.918 bits | Statistical complexity |
| $h_\mu$ | 0.667 bits/symbol | Entropy rate |
| $E$ | 0.252 bits | Excess entropy |
| $\chi$ | 0.667 bits | Crypticity |

**Key invariant verified**: $E + \chi = C_\mu$ ✓

For **IID processes** (fair coin):
- $E = 0$ (no past-future correlation)
- $\chi = 0$ (no hidden information)

## Why This Matters for Quantum Work

Crypticity $\chi$ measures exactly the "classical waste" that quantum models eliminate:

$$C_q = C_\mu - \chi = E$$

Wait, that's not quite right either. The correct relationship is:

$$E \leq C_q \leq C_\mu$$

The quantum statistical complexity $C_q$ sits between $E$ and $C_\mu$. The crypticity $\chi = C_\mu - E$ represents the **maximum possible** quantum advantage - how much memory a perfect quantum model could save.

Without correct $E$ and $\chi$ values, we cannot:
1. Compute upper bounds on quantum advantage
2. Validate against known results in papers
3. Study the decoherence trajectory from $C_q$ to $C_\mu$

## Files Changed

- `src/emic/analysis/measures.py` - Rewrote `excess_entropy()`, added `block_entropy()`, `crypticity()`
- `src/emic/analysis/__init__.py` - Exported new functions
- `tests/unit/test_analysis.py` - Removed incorrect test, added new tests for $E \leq C_\mu$ and positive crypticity

## Tests

All 410 tests pass, including new tests:
- `test_excess_entropy_iid_is_zero` - IID processes have E = 0
- `test_excess_entropy_leq_complexity` - E ≤ C_μ always
- `test_golden_mean_has_positive_crypticity` - Golden Mean has χ > 0

## References

- James, R. G., Ellison, C. J., & Crutchfield, J. P. (2011). "Anatomy of a bit: Information in a time series observation." *Chaos*, 21(3).
- Crutchfield, J. P., & Feldman, D. P. (2003). "Regularities unseen, randomness observed: Levels of entropy convergence." *Chaos*, 13(1).

---

## Implementation Notes

The `block_entropy()` function enumerates all possible L-blocks, which is exponential in L. For large alphabets or long blocks, this becomes intractable.

**Current approach**: If $|\mathcal{A}|^L > 100000$, fall back to asymptotic approximation. This works because excess entropy convergences quickly for finite-state machines.

**Future improvement**: Could use matrix methods. The block entropy can be computed via:
$$H(X_0^{L-1}) = \text{tr}(\text{something involving } T^L)$$
but I didn't work out the exact formula. The enumeration approach is correct and tractable for our current use cases.

**PYTHONPATH gotcha**: During testing, discovered that `/workspace/src` was on PYTHONPATH, shadowing the worktree's code. Tests were passing but using the wrong (buggy) implementation! Had to `unset PYTHONPATH` to test properly. This is a dev environment issue to watch for.
