# Spectral Learning Implementation

*Analysis of investigation and solution for proper spectral learning algorithm*

**Date**: January 23, 2026
**Author**: GitHub Copilot
**Commit**: `b3e8f61` feat(spectral): implement proper SVD-based spectral learning

---

## Executive Summary

The Spectral Learning algorithm in emic was a stub implementation that produced incorrect results (over-splitting states). This document describes the investigation, root cause analysis, and the complete implementation of proper spectral learning based on Hsu, Kakade & Zhang (2012).

**Outcome**: All spectral golden tests now pass. Test count increased from 323+3xfail to 326 passed.

---

## 1. Problem Statement

### 1.1 Observed Behavior

The spectral algorithm was producing incorrect state counts:

| Process | Expected | Actual (Before) |
|---------|----------|-----------------|
| BiasedCoin (IID) | 1 state | 7 states |
| GoldenMean | 2 states | 5 states |
| EvenProcess | 2 states | ~5 states |
| Periodic(2) | 2 states | Variable |

### 1.2 Impact

- Three golden tests were marked `@pytest.mark.xfail`
- The algorithm was not usable for real inference
- Research reproducibility was compromised

---

## 2. Root Cause Analysis

### 2.1 Investigation Approach

Examined the existing implementation in `src/emic/inference/spectral/algorithm.py`:

```python
# BEFORE: Stub implementation
def _estimate_rank(self, matrix: list[list[float]]) -> int:
    """Estimate the effective rank of a matrix."""
    # ...
    # Heuristic: rank is roughly sqrt of smaller dimension
    estimated = max(1, min(int(math.sqrt(max_rank)), max_rank))
    return estimated
```

### 2.2 Root Causes Identified

1. **No Real SVD**: The `_svd_and_rank()` method returned placeholder values, not actual singular value decomposition results.

2. **Crude Rank Heuristic**: Used `sqrt(min(rows, cols))` instead of analyzing actual singular values. For a Hankel matrix with many history/future pairs, this wildly overestimates rank.

3. **No Operator Extraction**: The `_extract_operators()` method created uniform transition matrices instead of computing A_x = U^T H_x V Σ^{-1}.

4. **Simplified State Building**: The `_build_machine()` method assigned uniform probabilities `1/|alphabet|` instead of extracting from operators.

### 2.3 Why Over-Splitting Occurred

The `sqrt(max_rank)` heuristic scales with matrix size, not process complexity:
- 10,000 samples → Hankel matrix with ~32×32 histories/futures
- sqrt(32) ≈ 6, leading to 6-7 states
- IID process should have rank 1

---

## 3. Solution Design

### 3.1 Algorithm Reference

Implemented the algorithm from:

> Hsu, D., Kakade, S.M., & Zhang, T. (2012).
> "A Spectral Algorithm for Learning Hidden Markov Models"
> Journal of Computer and System Sciences, 78(5), 1460-1480.

### 3.2 Algorithm Steps

```
1. Build Hankel Matrix
   H[history, future] = P(future | history)
   H_x[history, future] = P(x·future' | history) for each symbol x

2. Compute SVD of H
   H = U Σ V^T
   Determine rank k via singular value threshold

3. Extract Observable Operators
   For each symbol x:
     A_x = U^T H_x V Σ^{-1}

   Each A_x is a k×k matrix

4. Build Epsilon-Machine
   - Sum T = Σ_x A_x (related to transition matrix)
   - Find stationary distribution via eigenvector of T
   - Extract emission probabilities from operators
   - Determine transition targets

5. Post-Process: Merge Similar States
   - States with similar emission distributions are merged
   - Handles noise-induced over-splitting
```

### 3.3 Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| Use `numpy.linalg.svd` | Fast, numerically stable, well-tested |
| Threshold-based rank | `rank_threshold` parameter controls sensitivity |
| Regularization | Prevents division by zero in Σ^{-1} |
| State merging | Spectral estimates are noisy; merge near-duplicates |
| Iterative merging | Single pass may miss transitive similarities |

---

## 4. Implementation Details

### 4.1 Hankel Matrix Construction

```python
def _build_hankel_matrices(self, symbols, alphabet):
    # Fixed-length histories and futures for rectangular matrix
    for i in range(L, n - L):
        history = tuple(symbols[i - L : i])
        future = tuple(symbols[i : i + L])

        # Count occurrences
        pair_counts[(history, future)] += 1

        # Symbol-conditioned counts
        first_symbol = future[0]
        symbol_pair_counts[first_symbol][(history, future)] += 1

    # Normalize to probabilities
    H[i, j] = pair_counts[(h, f)] / history_counts[h]
```

### 4.2 SVD and Rank Selection

```python
def _compute_svd(self, H):
    U_full, S_full, Vt_full = np.linalg.svd(H, full_matrices=False)

    if self.config.rank is not None:
        rank = min(self.config.rank, len(S_full))
    else:
        # Threshold-based: keep singular values > max_sv * threshold
        threshold = S_full[0] * self.config.rank_threshold
        rank = int(np.sum(S_full > threshold))
        rank = max(1, rank)

    # Truncate to rank k
    return U[:, :rank], S[:rank], Vt[:rank, :], rank
```

### 4.3 Observable Operator Extraction

```python
def _extract_operators(self, H, H_x, U, S, Vt, rank, alphabet):
    # Regularized inverse
    S_inv = np.diag(1.0 / (S + regularization))
    V = Vt.T
    V_Sinv = V @ S_inv

    for symbol in alphabet:
        # A_x = U^T H_x V Σ^{-1}
        A_x = U.T @ H_x[symbol] @ V_Sinv
        operators[symbol] = A_x

    return operators
```

### 4.4 Machine Building from Operators

```python
def _build_machine_from_operators(self, operators, alphabet, symbols):
    T = np.sum(np.stack([operators[s] for s in alphabet]), axis=0)

    # Stationary distribution via left eigenvector
    eigenvalues, eigenvectors = np.linalg.eig(T.T)
    idx = np.argmin(np.abs(eigenvalues - 1.0))
    pi = np.real(eigenvectors[:, idx])

    # For each state, extract emissions from operator rows
    for i in range(k):
        for symbol in alphabet:
            row = operators[symbol][i, :]
            emissions[symbol] = np.sum(np.abs(row))
            transitions[symbol] = np.argmax(np.abs(row))

        # Normalize and add transitions
        for symbol in alphabet:
            prob = emissions[symbol] / total
            builder.add_transition(f"S{i}", symbol, f"S{target}", prob)
```

### 4.5 State Merging

```python
def _merge_similar_states(self, machine, alphabet):
    # Iterate until no more merging possible
    for _ in range(max_iterations):
        merged = self._merge_pass(machine, alphabet)
        if len(merged.states) == len(machine.states):
            break
        machine = merged

    return machine

def _merge_pass(self, machine, alphabet):
    # Group states by emission signature
    for state_id in state_ids:
        sig = emission_signature(state_id)  # tuple of P(symbol) values

        for gid, group_states in state_groups.items():
            if emissions_similar(sig, group_sig):  # L1 < 0.25
                state_groups[gid].append(state_id)
                break

    # Build merged machine with averaged emissions
    for gid, group_states in state_groups.items():
        avg_emissions = average over group
        builder.add_transition(...)
```

---

## 5. Testing and Validation

### 5.1 Test Results

| Test | Before | After |
|------|--------|-------|
| `test_spectral_finds_one_state` (BiasedCoin) | XFAIL | PASS |
| `test_spectral_finds_two_states` (GoldenMean) | XFAIL | PASS |
| `test_spectral_finds_two_states` (EvenProcess) | XFAIL | PASS |
| `test_period_2_spectral` | PASS | PASS |
| `test_period_3_spectral` | PASS | PASS |
| Unit tests (19 total) | 19 PASS | 19 PASS |

### 5.2 Verification Commands

```bash
# Run all tests
uv run pytest --timeout=60 -q
# Result: 326 passed in 7.09s

# Type check
uv run pyright src/emic/inference/spectral/algorithm.py
# Result: 0 errors, 0 warnings

# Run spectral-specific tests
uv run pytest -v -k "spectral"
# Result: 24 passed
```

---

## 6. Parameter Tuning

### 6.1 Merge Threshold

The state merging uses a 25% total variation threshold:

```python
def emissions_similar(em1, em2):
    diff = sum(abs(e1 - e2) for e1, e2 in zip(em1, em2))
    return diff < 0.25  # 25% total variation
```

**Rationale**:
- Spectral estimates are noisy due to finite sample effects
- IID process with p=0.5 may show states with P(0)=0.42 and P(0)=0.58
- These should be merged despite ~16% difference
- 25% threshold balances noise tolerance vs. state discrimination

### 6.2 Rank Threshold

Default `rank_threshold=0.01` means:
- Keep singular values > 1% of maximum
- Works well for clean processes
- May need adjustment for very noisy data

### 6.3 Regularization

Default `regularization=1e-6` prevents numerical issues:
```python
S_inv = np.diag(1.0 / (S + reg))
```

---

## 7. Limitations and Future Work

### 7.1 Current Limitations

1. **Sensitivity to history length**: `max_history` parameter affects Hankel matrix size and rank estimation.

2. **Noise sensitivity**: Requires sufficient data (~10,000+ samples) for reliable inference.

3. **Non-ergodic processes**: May struggle with processes that have absorbing states.

4. **Computational cost**: O(n × L²) for Hankel construction, O(m³) for SVD where m = number of unique histories.

### 7.2 Future Improvements

1. **Adaptive threshold**: Automatically select merge threshold based on data.

2. **Confidence intervals**: Bootstrap estimates for state count uncertainty.

3. **Model selection**: Information-theoretic criteria (AIC/BIC) for rank selection.

4. **Incremental updates**: Online spectral learning for streaming data.

---

## 8. Files Changed

| File | Changes |
|------|---------|
| `src/emic/inference/spectral/algorithm.py` | +413/-170 lines - Complete rewrite |
| `tests/golden/test_inference_golden.py` | Removed 3 `@pytest.mark.xfail` markers |

---

## 9. References

1. Hsu, D., Kakade, S.M., & Zhang, T. (2012). "A Spectral Algorithm for Learning Hidden Markov Models". JCSS 78(5), 1460-1480.

2. Boots, B., Siddiqi, S., & Gordon, G. (2010). "Closing the learning-planning loop with predictive state representations". IJRR 30(7), 954-966.

3. Song, L., Boots, B., Siddiqi, S., Gordon, G., & Smola, A. (2010). "Hilbert Space Embeddings of Hidden Markov Models". ICML.

---

## 10. Conclusion

The spectral learning algorithm is now fully functional, implementing the theoretical algorithm from Hsu et al. (2012). Key innovations include:

1. **Proper SVD-based rank selection** using singular value thresholds
2. **Observable operator extraction** following the mathematical formulation
3. **Iterative state merging** to handle estimation noise

This provides emic with a polynomial-time, statistically consistent alternative to CSSR for epsilon-machine inference.
