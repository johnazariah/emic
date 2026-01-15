# Inference

The `emic` framework uses the **CSSR** (Causal State Splitting Reconstruction) algorithm to infer epsilon-machines from data.

## CSSR Algorithm Overview

CSSR works by:

1. Building a suffix tree from observed sequences
2. Initializing each unique history as a potential causal state
3. Iteratively merging states with statistically indistinguishable futures
4. Splitting states when distributions differ significantly

## Basic Usage

```python
from emic.inference import CSSR, CSSRConfig

config = CSSRConfig(
    max_history=5,
    significance=0.001,
)

result = CSSR(config).infer(data)
```

## Configuration Parameters

### `max_history`

Maximum history length (L) to consider. Longer histories capture more complex structure but require more data.

| Data Size | Recommended `max_history` |
|-----------|---------------------------|
| 1,000 | 3-4 |
| 10,000 | 5-6 |
| 100,000 | 7-8 |

```python
config = CSSRConfig(max_history=5)
```

### `significance`

Significance level (α) for the chi-squared test when comparing distributions. Lower values are more conservative.

| Value | Behavior |
|-------|----------|
| 0.05 | Liberal — may under-split (fewer states) |
| 0.01 | Moderate |
| 0.001 | Conservative — may over-split initially |

```python
config = CSSRConfig(significance=0.001)
```

### `min_count`

Minimum observation count for a history to be considered. Filters out rare histories.

```python
config = CSSRConfig(min_count=5)  # Default: 1
```

### `post_merge`

Enable post-convergence state merging. Useful for processes like Even Process where CSSR may infer extra states due to finite-sample effects.

```python
config = CSSRConfig(post_merge=True)  # Default: True
```

### `merge_significance`

Significance level for post-merge comparisons. If `None`, uses the main `significance` value.

```python
config = CSSRConfig(
    significance=0.001,
    merge_significance=0.01,  # More aggressive merging
)
```

## Inference Result

```python
result = CSSR(config).infer(data)

# Access the inferred machine
machine = result.machine
print(f"States: {len(machine.states)}")

# Check convergence
print(f"Converged: {result.converged}")
print(f"Iterations: {result.iterations}")

# Access diagnostics
print(f"Final partition size: {result.final_partition_size}")
```

## Pipeline Integration

CSSR integrates with the pipeline operator:

```python
from emic.sources import GoldenMeanSource
from emic.inference import CSSR, CSSRConfig

result = GoldenMeanSource(p=0.5) >> CSSR(CSSRConfig(max_history=5))

# result is an InferenceResult
print(result.machine)
```

## Troubleshooting

### Too Many States

If CSSR infers more states than expected:

1. **Increase data**: More samples reduce finite-sample effects
2. **Lower significance**: Use `significance=0.01` or `0.05`
3. **Enable post-merge**: `post_merge=True` merges equivalent states
4. **Check `max_history`**: May be too high for your data size

### Too Few States

If CSSR infers fewer states than expected:

1. **Increase `max_history`**: May not capture full structure
2. **Raise significance**: Use `significance=0.001`
3. **Lower `min_count`**: May be filtering important histories

### Non-Convergence

If `result.converged` is False:

1. **Increase `max_iterations`**: Default is usually sufficient
2. **Check data quality**: Ensure sufficient samples
3. **Examine the process**: Some processes require very long histories

## References

- Shalizi, C.R. & Klinkner, K.L. (2004). "Blind Construction of Optimal Nonlinear Recursive Predictors for Discrete Sequences". *AUAI*.
