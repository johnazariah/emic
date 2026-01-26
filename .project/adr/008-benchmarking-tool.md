# ADR-008: Benchmarking Tool Architecture

## Status
**Accepted** — 2026-01-26

## Context

The emic library includes multiple inference algorithms (CSSR, Spectral, BSI, CSM) that need systematic validation against known processes. We currently have ad-hoc benchmark scripts scattered across research projects that:

1. Duplicate logic for running algorithms on test processes
2. Generate outputs in inconsistent formats
3. Couple data collection with paper-specific formatting
4. Lack timeout handling (some runs take 6+ hours)
5. Make it difficult to track performance regressions

### Requirements

1. **Reproducibility**: Benchmark runs must be timestamped with full metadata (git commit, versions, configs)
2. **Extensibility**: Easy to add new algorithms, processes, and experiment types
3. **Robustness**: Timeout handling for slow algorithms, partial results on failure
4. **Decoupling**: Separate data collection from downstream consumption (papers, CI, notebooks)
5. **Minimal dependencies**: Core module should not require heavy dependencies
6. **CLI interface**: Simple command-line usage for common operations

### Options Considered

#### Option A: Monolithic Script
Extend existing `run.py` scripts with more features.

- ✅ Simple, no new abstractions
- ❌ Continues coupling data collection with formatting
- ❌ Hard to compose different experiment types

#### Option B: Full Framework with Plugins
Rich plugin system with formatters, hooks at every stage, template engines.

- ✅ Maximum flexibility
- ❌ Over-engineered for our needs
- ❌ Complex plugin API to maintain

#### Option C: Thin Core + Rich Experiments (Hybrid)
Minimal core library for data collection; downstream scripts handle formatting.

- ✅ Clean separation of concerns
- ✅ Core stays small and stable
- ✅ Each paper/consumer owns its formatting logic
- ✅ Easy to test (validate schema, not string output)

## Decision

**We will implement Option C: a thin benchmarking core that only collects data.**

### Architecture

```
src/emic/benchmarks/
├── __init__.py     # Public API
├── schema.py       # BenchmarkResult dataclass, Parquet I/O
├── registry.py     # Process + algorithm registries
├── config.py       # YAML experiment config parsing
├── runner.py       # Core runner with timeout handling
└── cli.py          # Entry point: emic-benchmark
```

### Output Format

Each run creates a timestamped folder:

```
experiments/results/2026-01-26T14-32-05/
├── metadata.yaml    # Git commit, Python version, CLI args, duration
├── results.parquet  # Standardized schema (all experiment data)
└── latest -> .      # Symlink updated after each run
```

### Data Schema

```python
@dataclass(frozen=True)
class BenchmarkResult:
    experiment: str        # "accuracy", "convergence"
    algorithm: str         # "cssr", "spectral", "bsi"
    process: str           # "even_process", "golden_mean"
    n_samples: int         # Data length used
    metric: str            # "cmu", "hmu", "state_count", "duration_s"
    value: float           # Measured value
    ground_truth: float | None  # Expected value (if known)
    error: str | None      # Exception message (if failed)
    timestamp: datetime    # When this row was recorded
```

### Key Design Decisions

1. **Parquet output**: Columnar format, efficient, self-describing, pandas-native
2. **No formatting in core**: Papers/consumers implement their own `generate_tables.py`
3. **Timestamped folders**: Each run is isolated; `latest` symlink for convenience
4. **Registries via YAML**: Processes and algorithms defined declaratively
5. **SIGALRM timeouts**: Consistent with existing pattern in research scripts

### CLI Interface

```bash
# Run all registered experiments
emic-benchmark --all

# Run specific experiment
emic-benchmark accuracy

# Quick mode (reduced parameter space)
emic-benchmark --quick

# Custom timeout per algorithm run
emic-benchmark --timeout 60

# Specify output directory
emic-benchmark --output-dir ./my-results
```

## Consequences

### Positive

- **Decoupled concerns**: Data collection vs. formatting are independent
- **Reproducible**: Full metadata captured with every run
- **Extensible**: Add processes/algorithms by editing YAML registries
- **Testable**: Validate data schema, not string formatting
- **Replayable**: Re-run formatters on old data without re-running benchmarks

### Negative

- **Two-step for papers**: Must run benchmark, then run paper's formatter
- **Parquet dependency**: Adds `pyarrow` or `fastparquet` as optional dependency
- **Learning curve**: Users must understand the registry system

### Mitigations

- Provide example consumer scripts for common formats (LaTeX, Markdown)
- Make Parquet optional (fall back to JSON if not installed)
- Document registry format clearly with examples

## References

- Existing benchmark scripts: `.project/research/computational-mechanics-review/experiments/benchmarks/run.py`
- Shalizi (2004) benchmark methodology
- Parquet format: https://parquet.apache.org/
