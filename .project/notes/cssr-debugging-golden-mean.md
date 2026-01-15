# CSSR Debugging: Golden Mean Process

**Date**: January 2026
**Related**: `notebooks/debug_cssr_golden_mean.ipynb`

## Problem Statement

The CSSR algorithm was inferring **3 states** for the Golden Mean process instead of the expected **2 states**.

### Expected Machine (Golden Mean with p=0.5)

The Golden Mean process forbids consecutive 1s. It should have exactly 2 causal states:

- **State A** (last symbol was 0): Can emit 0 or 1 with ~50/50 probability
- **State B** (last symbol was 1): Must emit 0 with probability 1.0

```
     0 (0.5)
    ┌──────┐
    ▼      │
   [A] ────┤
    │      │
    │ 1    │
    │(0.5) │
    ▼      │
   [B] ────┘
      0 (1.0)
```

**Theoretical entropy rate**: $h_\mu = H(p) / (1 + p) = 1.0 / 1.5 ≈ 0.667$ bits/symbol

---

## Debugging Process

### Step 1: Suffix Tree Statistics

Generated 10,000 symbols from Golden Mean (p=0.5, seed=42):

```
Data length: 10000
Symbol counts: 0=6644, 1=3356
Consecutive 1s: 0 (verified - forbidden)
```

Suffix tree statistics clearly showed two distinct distribution types:

**Histories ending in 0** (~50/50 distribution):
| History | P(0) | P(1) |
|---------|------|------|
| `(0,)` | 0.4950 | 0.5050 |
| `(1,0)` | 0.5054 | 0.4946 |
| `(0,0)` | 0.4843 | 0.5157 |
| `(0,1,0)` | 0.5052 | 0.4948 |
| `(1,0,0)` | 0.4844 | 0.5156 |
| `(0,0,0)` | 0.4843 | 0.5157 |

**Histories ending in 1** (deterministic):
| History | P(0) | P(1) |
|---------|------|------|
| `(1,)` | 1.0000 | 0.0000 |
| `(0,1)` | 1.0000 | 0.0000 |
| `(1,0,1)` | 1.0000 | 0.0000 |
| `(0,0,1)` | 1.0000 | 0.0000 |

### Step 2: Trace Algorithm Execution

Running CSSR with `max_history=3, significance=0.05`:

```
Initial: 1 state (all histories in S0)

Iter 1 after split: 2 states
Iter 1 after merge: 2 states
    (): S0 -> S2
    (0,): S0 -> S2
    (1,): S0 -> S1
    ...

Iter 2 after split: 3 states  <-- Problem here!
Iter 2 after merge: 3 states
    (): S2 -> S4           <-- () split from others
    (0,): S2 -> S3
    ...

Iter 3: Converged with 3 states
```

The algorithm converged to **3 states** instead of 2.

### Step 3: Root Cause Identification

**The empty history `()` was the culprit.**

Comparing distributions:
```
(): P(0)=0.6645, P(1)=0.3355  (stationary distribution)
(0,): P(0)=0.4950, P(1)=0.5050  (conditional on last=0)
(1,): P(0)=1.0000, P(1)=0.0000  (conditional on last=1)
```

Chi-squared test between `()` and `(0,)`:
```
(): {0: 13288, 1: 6710}
(0,): {0: 3288, 1: 3355}

Do they differ (α=0.05)? True
```

**Key Insight**: The empty history `()` reflects the **stationary distribution** of the process (a mixture of causal states), not a single causal state. Since its distribution differs from both `(0,)` and `(1,)`, the chi-squared test correctly identifies it as distinct—but this is semantically wrong for causal state inference.

---

## Solution

### Fix 1: Exclude Empty History from Partitioning

Modified `_initialize_partition()` in `src/emic/inference/cssr/algorithm.py`:

```python
def _initialize_partition(self, suffix_tree: SuffixTree[A]) -> StatePartition:
    """
    Initialize partition by grouping similar histories.

    Note: The empty history () is excluded because it represents
    the stationary mixture of causal states, not a single state.
    """
    partition = StatePartition()

    # Collect histories with sufficient counts, excluding empty history
    valid_histories: list[tuple[A, ...]] = []
    for history in suffix_tree.all_histories():
        if len(history) == 0:
            continue  # Exclude empty history
        stats = suffix_tree.get_stats(history)
        if stats and stats.count >= self.config.min_count:
            valid_histories.append(history)

    # ... rest of initialization
```

### Fix 2: Compute Stationary Distribution Correctly

The `EpsilonMachineBuilder.build()` was defaulting to uniform distribution instead of computing the true stationary distribution. Added `_compute_stationary_distribution()` using power iteration:

```python
def _compute_stationary_distribution(self) -> dict[StateId, float]:
    """Compute stationary distribution by solving π = π P using power iteration."""
    # Build transition matrix P[i][j] = prob from state i to state j
    # Power iteration until convergence
    # Returns {state_id: probability}
```

---

## Verification

After fixes, CSSR correctly infers:

```
Number of states: 2 (expected: 2) ✓

Machine structure:
  S1 (after 1):
    --0 (p=1.0000)--> S2
  S2 (after 0):
    --1 (p=0.5051)--> S1
    --0 (p=0.4949)--> S2

Stationary distribution: {'S1': 0.3356, 'S2': 0.6644}

Entropy rate: 0.6644 (expected: 0.6667) ✓
```

---

## Key Takeaways

1. **Empty history is special**: In CSSR, the empty history `()` represents the stationary mixture of all causal states, not a specific causal state. It must be excluded from state equivalence testing.

2. **Stationary distribution matters**: Entropy rate calculation requires the correct stationary distribution, not uniform. Use power iteration to compute π = πP.

3. **Chi-squared test works correctly**: The test correctly identified `()` as having a different distribution. The bug was in including `()` in the first place.

4. **Standard CSSR**: The literature confirms that CSSR partitions histories of length 1 to L, not including the empty history.

---

## Test Coverage

The debug notebook `notebooks/debug_cssr_golden_mean.ipynb` serves as a regression test and reference implementation. Run all cells to verify CSSR behavior.

All 194 tests pass after these fixes.
