# Defect Report: DEF-001 — excess_entropy returns C_μ instead of E

## Summary

`emic.analysis.measures.excess_entropy()` incorrectly returns the statistical
complexity C_μ for all inputs, based on the false mathematical claim that
E = C_μ for unifilar machines. This causes crypticity (χ = C_μ - E) to be
reported as zero for every process, which is wrong for almost all non-trivial
stochastic processes.

## Severity

**High** — a core analysis measure returns incorrect values. Blocks the
quantum computational mechanics research path (computing C_q requires
correct E and χ).

## Root Cause

In `src/emic/analysis/measures.py`, lines 128–147:

```python
def excess_entropy(machine: EpsilonMachine[A]) -> float:
    """For unifilar machines (which epsilon-machines are):
    E = Cμ (statistical complexity equals excess entropy)"""
    return statistical_complexity(machine)
```

The docstring and implementation assume E = C_μ for unifilar machines.
This is **mathematically incorrect**.

### Why E ≠ C_μ in General

E = I(Past; Future) is the mutual information between the entire past and
future of the process. C_μ = H(S) is the entropy of the causal state
distribution.

The relationship is:

    E ≤ C_μ       (always)
    χ = C_μ - E   (crypticity, generically > 0)

Crypticity is zero only for very special processes (e.g., IID processes
where C_μ = 0 = E, or certain renewal processes). For the canonical test
processes in emic:

| Process | C_μ | E (correct) | χ (correct) | E (emic reports) | χ (emic reports) |
|---------|-----|-------------|-------------|------------------|------------------|
| Biased Coin | 0.0 | 0.0 | 0.0 | 0.0 ✓ | 0.0 ✓ |
| Golden Mean (p=0.5) | ~0.918 | ~0.459 | ~0.459 | 0.918 ✗ | 0.000 ✗ |
| Even Process (p=0.5) | ~0.918 | ~0.459 | ~0.459 | 0.918 ✗ | 0.000 ✗ |
| Periodic (0,1) | 1.0 | 1.0 | 0.0 | 1.0 ✓ | 0.0 ✓ |

The bug is invisible for IID and deterministic processes, which is why it
survived testing.

### The Confusion

"Unifilar" means that given the current state and the emitted symbol, the
next state is deterministic. This is a property of the epsilon-machine's
*forward* transitions. It does NOT imply E = C_μ.

The condition E = C_μ would require the *reverse* epsilon-machine (predicting
the past from the future) to also have complexity C_μ, and for the forward
and reverse causal states to be in bijection — which is not generally true.

Reference: Crutchfield (2009) "Time's Barbed Arrow" — defines crypticity
and proves χ > 0 is generic.

## Blast Radius

### Directly Affected

1. **`excess_entropy()`** — returns wrong value (C_μ instead of E)
2. **`AnalysisSummary.crypticity`** — always 0 (computed as `c_mu - e`)
3. **`AnalysisSummary.excess_entropy`** — always equals C_μ

### Downstream Consumers

4. **`analyze()` in summary.py** — populates wrong E and χ in summary
5. **LaTeX output** (`output/latex.py`) — exports wrong E
6. **Notebooks** — `demo_inference.ipynb`, `debug_even_process.ipynb` display wrong values

### Tests That Encode the Error

7. `tests/unit/test_analysis.py::test_excess_entropy_equals_complexity_for_unifilar`
   — asserts `abs(c_mu - e) < 1e-10` on Golden Mean. **This test is wrong.**
8. `tests/unit/test_analysis.py` line 101 — asserts `abs(summary.crypticity) < 1e-10`
   with comment "Unifilar => chi = 0". **This test is wrong.**

### NOT Affected

- **Inference algorithms** (CSSR, CSM, BSI, NSD, Spectral) — do not use
  excess_entropy. All inferred machines are correct.
- **C_μ computation** — correct.
- **h_μ computation** — correct.
- **State counts and transitions** — correct.

### Documentation

- `docs/guide/complexity-measures-explained.md` — correctly defines E and χ
  and shows correct expected values (E ≈ 0.459
  for Golden Mean). These values are aspirational — the code does not currently
  produce them. Documentation will self-correct once the code is fixed.

## Correct Computation of E

Excess entropy for a unifilar (epsilon-machine) can be computed via the
**mixed-state presentation** approach:

### Method 1: Block Entropy Convergence

    E = lim_{L→∞} [ H(X_1, ..., X_L) - L · h_μ ]

Compute H(X_1, ..., X_L) for increasing L using the transition matrices,
subtract L · h_μ, and observe convergence. Practical for small state spaces.

### Method 2: Forward-Reverse Causal State Joint Entropy

    E = C_μ + C_μ⁺ - H(S⁻, S⁺)

where:
- C_μ⁺ = statistical complexity of the reverse (time-reversed) epsilon-machine
- H(S⁻, S⁺) = joint entropy of forward and reverse causal states

This requires constructing the reverse epsilon-machine, which involves
computing the time-reversed transition probabilities and re-partitioning
into reverse causal states.

### Method 3: Spectral Method (Matrix-Based)

For a unifilar machine with transition matrices T^(x), the excess entropy
can be computed from the eigenstructure of the combined transition matrix.
This is the most efficient method for machines with known structure.

### Recommended Approach

Method 1 (block entropy convergence) is the simplest to implement correctly
and can be validated against known analytical values. Method 3 is more
efficient for larger machines.

## Fix Requirements

1. **Implement correct `excess_entropy()`** using one of the methods above.
2. **Validate against known analytical values:**
   - Golden Mean (p=0.5): E ≈ 0.4591 bits
   - Even Process (p=0.5): E ≈ 0.4591 bits
   - Biased Coin: E = 0 (trivial case, already correct)
   - Periodic: E = C_μ (special case where χ = 0)
3. **Fix the two incorrect tests** in `test_analysis.py`.
4. **Add new tests** asserting correct E and χ for Golden Mean and Even Process.
5. **Verify notebook outputs** still render correctly with new values.
6. **Consider adding `crypticity()` as a standalone measure** in measures.py
   (currently only computed in `analyze()`).

## References

- Crutchfield, J. P. (2009). "Time's Barbed Arrow." — Defines crypticity,
  proves χ > 0 is generic.
- James, R. G., Burke, K. & Crutchfield, J. P. (2014). "Anatomy of a Bit."
  — Full information decomposition using causal states.
- Shalizi, C. R. & Crutchfield, J. P. (2001). "Computational Mechanics."
  — Proves E ≤ C_μ.

## Discovery Context

Found during review coaching session (2026-03-09) while tracing the
information anatomy from Shalizi 2001 through to Gu 2012's quantum advantage
hierarchy E ≤ C_q ≤ C_μ. The bug makes it impossible to compute the
crypticity gap that quantum models exploit.
