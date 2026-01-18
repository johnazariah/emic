# Specification 016: Performance Optimization

## Overview

This specification defines the performance optimization strategy for emic, including parallelization opportunities, implementation priorities, and benchmarking infrastructure.

**Related ADR**: [ADR-007: Parallelization Strategy](../adr/007-parallelization-strategy.md)

---

## Motivation

As emic moves toward production use and larger datasets, we need:

1. **Identified bottlenecks** with measured impact
2. **Clear optimization priorities** based on effort vs. impact
3. **Benchmarking infrastructure** to measure improvements
4. **Guidelines** for contributors on performance-sensitive code

---

## Current Performance Profile

### Computational Complexity

| Algorithm | Time Complexity | Space Complexity | Notes |
|-----------|-----------------|------------------|-------|
| CSSR | O(n × L² × k) | O(|Σ|^L) | n=length, L=max_history, k=states |
| CSM | O(n × L + h² × |Σ|) | O(h × |Σ|) | h=unique histories |
| BSI | O(iterations × h × k) | O(h × |Σ|) | MCMC sampling |
| Spectral | O(n × L + m×n×min(m,n)) | O(m × n) | SVD dominates |
| NSD | O(n × L + h × k × iterations) | O(h × |Σ|) | k-means clustering |

### Measured Bottlenecks (Typical 50K sequence)

| Operation | % Time | Current Implementation |
|-----------|--------|------------------------|
| Suffix tree build | 30-40% | Pure Python loops |
| Statistical tests | 20-30% | Pure Python, repeated |
| State comparisons | 15-25% | O(k²) pairwise |
| Stationary distribution | 5-10% | Pure Python matrix ops |
| Machine construction | 5-10% | Acceptable |

---

## Optimization Targets

### Target 1: Suffix Tree Construction

**Location**: [src/emic/inference/cssr/suffix_tree.py](../../src/emic/inference/cssr/suffix_tree.py)

**Current Code**:
```python
def build_from_sequence(self, symbols: list[A]) -> None:
    n = len(symbols)
    for i in range(n - 1):
        next_symbol = symbols[i + 1]
        for length in range(min(i + 1, self.max_depth) + 1):
            start = i - length + 1
            if start < 0:
                continue
            history = tuple(symbols[start : i + 1])
            self.add_observation(history, next_symbol)
```

**Problem**: Python loop overhead, tuple creation in inner loop

**Solution Options**:

1. **NumPy sliding window** (Phase 1):
   ```python
   from numpy.lib.stride_tricks import sliding_window_view

   symbols_arr = np.array(symbols)
   for length in range(1, self.max_depth + 1):
       windows = sliding_window_view(symbols_arr[:-1], length)
       next_syms = symbols_arr[length:]
       # Batch process windows
   ```

2. **Numba JIT** (Phase 3):
   ```python
   @numba.jit(nopython=True)
   def _build_suffix_counts(symbols, max_depth):
       # Compile to machine code
   ```

**Expected Improvement**: 3-10x

---

### Target 2: Stationary Distribution

**Location**: [src/emic/types/machine.py](../../src/emic/types/machine.py) `_compute_stationary_distribution`

**Current Code**:
```python
for _ in range(1000):
    pi_new = [0.0] * n
    for j in range(n):
        for i in range(n):
            pi_new[j] += pi[i] * P[i][j]
    # ...
```

**Problem**: O(n²) Python loops for matrix-vector multiplication

**Solution** (Phase 1):
```python
import numpy as np

def _compute_stationary_distribution(self) -> dict[StateId, float]:
    state_ids = list(self._states.keys())
    n = len(state_ids)
    if n == 0:
        return {}
    if n == 1:
        return {state_ids[0]: 1.0}

    # Build transition matrix
    state_idx = {sid: i for i, sid in enumerate(state_ids)}
    P = np.zeros((n, n))

    for sid, transitions in self._states.items():
        i = state_idx[sid]
        for t in transitions:
            if t.target in state_idx:
                j = state_idx[t.target]
                P[i, j] += t.probability

    # Validate stochastic matrix
    row_sums = P.sum(axis=1)
    if not np.allclose(row_sums, 1.0, atol=0.01):
        return dict.fromkeys(state_ids, 1.0 / n)

    # Power iteration with NumPy
    pi = np.ones(n) / n
    for _ in range(1000):
        pi_new = pi @ P
        pi_new /= pi_new.sum()  # Normalize
        if np.allclose(pi, pi_new, atol=1e-10):
            break
        pi = pi_new

    return {state_ids[i]: float(pi[i]) for i in range(n)}
```

**Expected Improvement**: 10-50x for machines with >10 states

---

### Target 3: Spectral SVD

**Location**: [src/emic/inference/spectral/algorithm.py](../../src/emic/inference/spectral/algorithm.py) `_svd_and_rank`

**Current Code**: Placeholder pure-Python implementation

**Solution** (Phase 1):
```python
from scipy.linalg import svd
import numpy as np

def _svd_and_rank(
    self,
    hankel: dict[tuple[tuple[A, ...], tuple[A, ...]], float],
) -> tuple[np.ndarray, np.ndarray, np.ndarray, int]:
    # Build dense matrix
    histories = sorted(set(h for h, _ in hankel))
    futures = sorted(set(f for _, f in hankel))

    m, n = len(histories), len(futures)
    if m == 0 or n == 0:
        return np.array([[]]), np.array([1.0]), np.array([[]]), 1

    history_idx = {h: i for i, h in enumerate(histories)}
    future_idx = {f: j for j, f in enumerate(futures)}

    matrix = np.zeros((m, n))
    for (h, f), val in hankel.items():
        matrix[history_idx[h], future_idx[f]] = val

    # SVD via scipy (uses LAPACK)
    U, s, Vt = svd(matrix, full_matrices=False)

    # Determine rank
    if self.config.rank is not None:
        rank = min(self.config.rank, len(s))
    else:
        threshold = self.config.rank_threshold * s[0] if len(s) > 0 else 0
        rank = int(np.sum(s > threshold))
        rank = max(1, rank)

    return U[:, :rank], s[:rank], Vt[:rank, :], rank
```

**Expected Improvement**: 10-100x, plus correctness improvement

---

### Target 4: Distance Matrix Computation (CSM)

**Location**: [src/emic/inference/csm/algorithm.py](../../src/emic/inference/csm/algorithm.py) `_compute_all_distances`

**Current Code**: Sequential pairwise computation

**Solution** (Phase 2 - Parallelization):
```python
from concurrent.futures import ProcessPoolExecutor
from itertools import combinations

def _compute_all_distances(self, ...) -> dict[tuple[str, str], float]:
    state_ids = list(partition.keys())
    pairs = list(combinations(state_ids, 2))

    # Prepare data for parallel computation
    pair_data = [
        (s1, s2, state_to_histories, history_stats)
        for s1, s2 in pairs
    ]

    with ProcessPoolExecutor() as executor:
        results = executor.map(self._compute_pair_distance, pair_data)

    return {
        (min(s1, s2), max(s1, s2)): dist
        for (s1, s2, _, _), dist in zip(pair_data, results)
    }
```

**Expected Improvement**: 2-4x on multi-core systems

---

### Target 5: BSI Parallel Chains

**Location**: [src/emic/inference/bsi/algorithm.py](../../src/emic/inference/bsi/algorithm.py)

**Current Code**: Single MCMC chain

**Solution** (Phase 2):
```python
from concurrent.futures import ProcessPoolExecutor

def _infer_with_n_states(self, ...) -> tuple[EpsilonMachine[A], float]:
    n_chains = min(4, os.cpu_count() or 1)

    def run_chain(seed: int) -> tuple[float, dict]:
        rng = random.Random(seed)
        # Run MCMC...
        return best_log_posterior, best_trans_counts

    with ProcessPoolExecutor(max_workers=n_chains) as executor:
        chain_results = list(executor.map(
            run_chain,
            [self.config.seed + i for i in range(n_chains)]
        ))

    # Select best chain
    best_idx = max(range(n_chains), key=lambda i: chain_results[i][0])
    return self._build_machine(chain_results[best_idx][1], ...)
```

**Expected Improvement**: ~n_chains speedup (2-4x typically)

---

## Benchmarking Infrastructure

### Benchmark Suite

Create `benchmarks/` directory with standardized benchmarks:

```python
# benchmarks/bench_cssr.py
import time
from emic.inference import CSSR, CSSRConfig
from emic.sources.synthetic import GoldenMeanSource
from emic.sources.transforms import TakeN

SIZES = [1_000, 10_000, 50_000, 100_000]
HISTORY_LENGTHS = [3, 5, 7, 10]

def benchmark_cssr():
    results = []
    for n in SIZES:
        for L in HISTORY_LENGTHS:
            source = GoldenMeanSource(p=0.5, _seed=42)
            sequence = list(TakeN(n)(source))

            config = CSSRConfig(max_history=L, significance=0.01)
            cssr = CSSR(config)

            start = time.perf_counter()
            result = cssr.infer(sequence)
            elapsed = time.perf_counter() - start

            results.append({
                'n': n,
                'L': L,
                'time_s': elapsed,
                'states': len(result.machine.states),
            })

    return results
```

### Performance Regression Tests

Add to CI:

```yaml
# .github/workflows/benchmark.yml
name: Performance Benchmarks

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  benchmark:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v4
      - run: uv sync
      - run: uv run python -m benchmarks.run_all
      - uses: benchmark-action/github-action-benchmark@v1
        with:
          tool: 'customSmallerIsBetter'
          output-file-path: benchmarks/results.json
```

### Performance Assertions

```python
# tests/performance/test_perf_regression.py
import pytest
from benchmarks.bench_cssr import benchmark_cssr_single

@pytest.mark.slow
def test_cssr_10k_under_1_second():
    """CSSR on 10K sequence should complete in <1s."""
    elapsed = benchmark_cssr_single(n=10_000, L=5)
    assert elapsed < 1.0, f"CSSR took {elapsed:.2f}s, expected <1s"

@pytest.mark.slow
def test_cssr_50k_under_5_seconds():
    """CSSR on 50K sequence should complete in <5s."""
    elapsed = benchmark_cssr_single(n=50_000, L=5)
    assert elapsed < 5.0, f"CSSR took {elapsed:.2f}s, expected <5s"
```

---

## Implementation Plan

### Phase 1: NumPy/SciPy Integration (Week 1)

| Task | File | Estimated Time |
|------|------|----------------|
| NumPy stationary distribution | `types/machine.py` | 2 hours |
| SciPy SVD in Spectral | `inference/spectral/algorithm.py` | 2 hours |
| NumPy distance metrics | `inference/csm/algorithm.py` | 2 hours |
| Benchmarking infrastructure | `benchmarks/` | 4 hours |
| Performance tests | `tests/performance/` | 2 hours |

**Deliverable**: 5-50x improvement on key operations, benchmark baseline

### Phase 2: Parallelization (Week 2-3, if needed)

| Task | File | Estimated Time |
|------|------|----------------|
| Parallel MCMC chains | `inference/bsi/algorithm.py` | 1 day |
| Parallel distance matrix | `inference/csm/algorithm.py` | 1 day |
| joblib batch inference | `inference/` | 1 day |
| Parallel suffix tree option | `inference/cssr/suffix_tree.py` | 2 days |

**Trigger**: Phase 1 results show remaining bottlenecks

### Phase 3: Numba/Cython (Week 4+, if needed)

| Task | File | Estimated Time |
|------|------|----------------|
| Numba suffix tree | `inference/cssr/suffix_tree.py` | 3 days |
| Numba statistical tests | `inference/cssr/tests.py` | 2 days |
| Optional Cython module | New package | 1 week |

**Trigger**: Phase 2 insufficient for target performance

---

## Configuration

### Performance-Related Config Options

```python
@dataclass(frozen=True)
class PerformanceConfig:
    """Global performance configuration."""

    use_numpy: bool = True
    """Use NumPy for matrix operations when available."""

    parallel: bool = False
    """Enable parallel processing where available."""

    n_workers: int | None = None
    """Number of parallel workers. None = auto-detect."""

    use_numba: bool = False
    """Use Numba JIT compilation if available."""
```

### Per-Algorithm Options

```python
@dataclass(frozen=True)
class CSSRConfig:
    # ... existing fields ...

    parallel_build: bool = False
    """Build suffix tree in parallel (requires multiprocessing)."""

@dataclass(frozen=True)
class BSIConfig:
    # ... existing fields ...

    n_chains: int = 1
    """Number of parallel MCMC chains."""
```

---

## Success Metrics

| Metric | Current | Phase 1 Target | Phase 2 Target |
|--------|---------|----------------|----------------|
| CSSR 10K seq, L=5 | ~2s | <0.5s | <0.2s |
| CSSR 50K seq, L=5 | ~10s | <2s | <1s |
| CSM 10K seq, L=5 | ~3s | <1s | <0.5s |
| BSI 10K seq, k=5 | ~5s | <3s | <1s |
| Spectral 10K seq | ~2s | <0.5s | <0.3s |

---

## Guidelines for Contributors

### Performance-Sensitive Code

1. **Prefer NumPy operations** over Python loops for numerical work
2. **Avoid creating objects in tight loops** — pre-allocate where possible
3. **Use generators** for large sequences to avoid memory pressure
4. **Profile before optimizing** — use `cProfile` or `py-spy`

### Benchmarking New Features

1. Add benchmark case to `benchmarks/` for new algorithms
2. Run benchmarks before and after significant changes
3. Document expected complexity in docstrings

### Review Checklist

- [ ] No Python loops where NumPy would work
- [ ] No repeated dictionary lookups in inner loops
- [ ] Memory-efficient for large sequences
- [ ] Benchmark added for new computational code

---

## References

- NumPy performance tips: https://numpy.org/doc/stable/user/quickstart.html
- Numba documentation: https://numba.readthedocs.io/
- Python profiling: https://docs.python.org/3/library/profile.html
- concurrent.futures: https://docs.python.org/3/library/concurrent.futures.html
