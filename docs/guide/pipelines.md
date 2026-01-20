# Pipelines

The `emic` framework uses the `>>` operator to compose operations into pipelines.

## Basic Pipeline

```python
from emic.sources import GoldenMeanSource, TakeN
from emic.inference import CSSR, CSSRConfig
from emic.analysis import analyze

# Generate data
source = GoldenMeanSource(p=0.5, _seed=42)
data = source >> TakeN(10_000)

# Infer machine
result = CSSR(CSSRConfig(max_history=5)).infer(data)

# Analyze
summary = analyze(result.machine)
print(summary)
```

## Pipeline Stages

A typical workflow flows through these stages:

```
Source → Transform → Data → Inference → Machine → Analysis → Summary
```

### Stage 1: Source

Sources produce infinite symbol sequences:

```python
from emic.sources import GoldenMeanSource

source = GoldenMeanSource(p=0.5, _seed=42)
```

### Stage 2: Transform

Transforms convert sources to finite data:

```python
from emic.sources import TakeN, SkipN

# Take first 10,000 symbols
data = source >> TakeN(10_000)

# Or skip burn-in, then take
data = source >> SkipN(1000) >> TakeN(10_000)
```

### Stage 3: Inference

Inference algorithms consume data and produce an `InferenceResult`:

```python
from emic.inference import CSSR, CSSRConfig

result = CSSR(CSSRConfig(max_history=5)).infer(data)
# result.machine contains the inferred epsilon-machine
# result.converged indicates if algorithm converged
```

### Stage 4: Analysis

The `analyze` function computes complexity measures:

```python
from emic.analysis import analyze

summary = analyze(result.machine)
print(f"Cμ = {summary.statistical_complexity:.4f}")
```

## Transform Chains

Chain transforms using the `>>` operator:

```python
from emic.sources import GoldenMeanSource, SkipN, TakeN

# Skip burn-in, then take samples
data = GoldenMeanSource(p=0.5, _seed=42) >> SkipN(1000) >> TakeN(10_000)
```

Or use function call syntax:

```python
source = GoldenMeanSource(p=0.5, _seed=42)
skipped = SkipN(1000)(source)
data = TakeN(10_000)(skipped)
```

## Full Example

```python
from emic.sources import GoldenMeanSource, TakeN
from emic.inference import CSSR, CSSRConfig
from emic.analysis import analyze
from emic.output import render_state_diagram

# Configure
source = GoldenMeanSource(p=0.5, _seed=42)
config = CSSRConfig(max_history=5, significance=0.001)

# Generate data
data = source >> TakeN(10_000)

# Infer
result = CSSR(config).infer(data)
print(f"States: {len(result.machine.states)}")
print(f"Converged: {result.converged}")

# Analyze
summary = analyze(result.machine)
print(f"Cμ = {summary.statistical_complexity:.4f}")

# Visualize
diagram = render_state_diagram(result.machine)
diagram.render("output", format="png")
```

## The Pipeline Class

For more complex workflows, use the `Pipeline` class:

```python
from emic import Pipeline

# Create a pipeline from a sequence of operations
pipeline = Pipeline([
    lambda x: x * 2,
    lambda x: x + 1,
])

result = pipeline(5)  # (5 * 2) + 1 = 11
```

### Pipeline Utilities

```python
from emic import identity, tap

# Identity function (pass-through)
result = identity(value)  # Returns value unchanged

# Tap function (side-effect without modifying value)
logged = tap(print)(value)  # Prints value, returns value
```

## Debugging Pipelines

Break apart pipelines to inspect intermediate results:

```python
from emic.sources import GoldenMeanSource, TakeN
from emic.inference import CSSR, CSSRConfig
from emic.analysis import analyze

# Step by step
source = GoldenMeanSource(p=0.5, _seed=42)
data = TakeN(10_000)(source)
print(f"Data length: {len(data)}")

config = CSSRConfig(max_history=5)
inference_result = CSSR(config).infer(data)
print(f"Converged: {inference_result.converged}")
print(f"States: {len(inference_result.machine.states)}")

summary = analyze(inference_result.machine)
print(f"Cμ = {summary.statistical_complexity:.4f}")
```

## Pipeline Composition with `>>`

Most `emic` objects support the `>>` operator:

| Left Side | Right Side | Result |
|-----------|------------|--------|
| Source | TakeN/SkipN | SequenceData |
| SequenceData | TakeN | SequenceData |
| SequenceData | Inference | InferenceResult |

```python
# Sources compose with transforms
data = GoldenMeanSource() >> TakeN(1000)

# SequenceData composes with inference
result = data >> CSSR(config)  # Returns InferenceResult
```
