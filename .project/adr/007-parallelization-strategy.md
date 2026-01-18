# ADR-007: Parallelization and Performance Strategy

## Status
**Accepted** — 2026-01-18

## Context

As the emic framework matures toward production use and larger datasets, we need to assess:

1. **Current performance characteristics** of inference algorithms
2. **Parallelization opportunities** in the codebase
3. **Whether to rewrite in a compiled language** (F#, Scala, Rust)

### Performance Analysis Conducted

A comprehensive analysis of the codebase identified these computational hotspots:

| Component | Current Complexity | Parallelization Potential |
|-----------|-------------------|---------------------------|
| Suffix tree construction | O(n × L) | HIGH — embarrassingly parallel |
| State pairwise comparisons | O(k²) | MEDIUM — k typically small |
| CSM distance matrix | O(h²) | HIGH — independent computations |
| BSI MCMC sampling | O(iterations × histories) | HIGH — parallel chains |
| Spectral SVD | O(m × n × min(m,n)) | HIGH — use BLAS/LAPACK |
| Stationary distribution | O(n² × iterations) | HIGH — matrix operations |

### Language Alternatives Considered

#### Option A: Rewrite in F#
- Excellent type system, functional-first
- Good quantum computing story (Q# integration)
- Weaker scientific ecosystem than Python

#### Option B: Rewrite in Scala
- Strong type system, JVM ecosystem
- Good parallelism primitives (Akka, parallel collections)
- Limited scientific libraries

#### Option C: Stay in Python with Optimization
- Leverage NumPy/SciPy for vectorization
- Use multiprocessing for parallelism
- Optional Numba/Cython for hot loops
- Keep development velocity high

#### Option D: Hybrid with Rust Extensions
- Critical paths in Rust via PyO3
- Python for orchestration and UI
- Best of both worlds, but higher complexity

## Decision

**We will stay in Python and optimize incrementally (Option C).**

If performance requirements exceed what Python can deliver, we will add Rust extensions (Option D) for specific bottlenecks rather than full rewrite.

### Rationale

| Factor | Stay in Python | Rewrite (F#/Scala) |
|--------|----------------|-------------------|
| Development velocity | ✅ High | ❌ Months of rewrite |
| Scientific ecosystem | ✅ NumPy/SciPy/Matplotlib | ⚠️ Limited equivalents |
| Target audience | ✅ Researchers expect Python | ⚠️ Higher barrier |
| Current data sizes | ✅ 50K symbols is fine | Overkill for current needs |
| Optimization headroom | ✅ 10-50x via NumPy/Numba | Marginal additional gain |
| Jupyter integration | ✅ Native | ⚠️ Awkward |
| Time to results | ✅ Days | ❌ Months |

**Key insight**: Current bottlenecks are not language-related — they're algorithmic patterns that don't leverage NumPy properly. The pure-Python implementations (stationary distribution, SVD placeholder) can be replaced with NumPy/SciPy calls for 10-100x speedup without changing languages.

### When to Revisit

Consider compiled language rewrite if:
- Sequence lengths regularly exceed **10M symbols**
- Real-time streaming inference is required (**sub-millisecond latency**)
- Production deployment at scale (**millions of sequences/day**)
- Quantum extension (M6/M7) would benefit from **F#/Q# integration**

## Implementation Strategy

### Phase 1: NumPy/SciPy Integration (Immediate)

1. **Stationary distribution**: Replace Python loops with `pi @ P` matrix multiplication
2. **Spectral SVD**: Use `scipy.linalg.svd` instead of placeholder
3. **Distance computations**: Vectorize KL/Hellinger with NumPy

**Estimated effort**: 1-2 days
**Expected speedup**: 5-50x for affected operations

### Phase 2: Multiprocessing (If Needed)

1. **Parallel MCMC chains** for BSI
2. **Parallel distance matrix** computation for CSM
3. **joblib integration** for batch inference

**Estimated effort**: 1 week
**Expected speedup**: 2-4x on multi-core systems

### Phase 3: Numba/Cython (If Still Needed)

1. **JIT-compile** tight inner loops (suffix tree, statistical tests)
2. **Cython** for suffix tree if still bottleneck

**Estimated effort**: 1-2 weeks
**Expected speedup**: 5-20x for affected loops

### Phase 4: Rust Extensions (Future, If Required)

1. Identify remaining bottlenecks after Phase 1-3
2. Implement critical paths in Rust via PyO3
3. Maintain Python API compatibility

**Trigger**: Phase 1-3 insufficient for requirements

## Consequences

### Positive
- Maintains development velocity during research phase
- Keeps codebase accessible to research community
- Preserves Jupyter notebook workflow
- Clear optimization roadmap with measurable gates

### Negative
- Performance ceiling eventually limited by Python/NumPy
- Some optimization work needed to realize potential
- Must resist premature optimization

### Neutral
- Need to add benchmarking infrastructure to measure improvements
- Should document performance characteristics for users

## Related

- [ADR-001: Programming Language Selection](001-programming-language.md) — Original language decision
- [Specification 016: Performance Optimization](../specifications/016-performance-optimization.md) — Detailed implementation plan

## References

- NumPy documentation: https://numpy.org/doc/
- SciPy linear algebra: https://docs.scipy.org/doc/scipy/reference/linalg.html
- Numba documentation: https://numba.pydata.org/
- PyO3 (Rust-Python bindings): https://pyo3.rs/
