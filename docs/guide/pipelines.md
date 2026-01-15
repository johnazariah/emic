# Pipelines

The `emic` framework uses the `>>` operator to compose operations into pipelines.

## Basic Pipeline

```python
from emic.sources import GoldenMeanSource
from emic.inference import CSSR, CSSRConfig
from emic.analysis import Analyzer

result = (
    GoldenMeanSource(p=0.5, seed=42)
    >> CSSR(CSSRConfig(max_history=5))
    >> Analyzer()
)
```

## Pipeline Stages

A typical pipeline flows through these stages:

```
Source → Data → Inference → Machine → Analysis → Summary
```

### Stage 1: Source

Sources produce symbol sequences:

```python
source = GoldenMeanSource(p=0.5, seed=42)
```

### Stage 2: Inference

CSSR consumes data and produces an `InferenceResult`:

```python
result = source >> CSSR(config)
# result.machine contains the inferred epsilon-machine
```

### Stage 3: Analysis

Analyzer consumes a machine and produces analysis:

```python
analysis = source >> CSSR(config) >> Analyzer()
# analysis.summary contains complexity measures
```

## Transform Chains

Chain transforms on sources:

```python
# Skip burn-in, then take samples
data = (
    GoldenMeanSource(p=0.5)
    .skip(1000)
    .take(10_000)
)
```

Or with the `>>` operator:

```python
from emic.sources.transforms import Skip, Take

data = GoldenMeanSource(p=0.5) >> Skip(1000) >> Take(10_000)
```

## Full Example

```python
from emic.sources import GoldenMeanSource
from emic.inference import CSSR, CSSRConfig
from emic.analysis import Analyzer
from emic.output import render_diagram

# Configure
source = GoldenMeanSource(p=0.5, seed=42)
config = CSSRConfig(max_history=5, significance=0.001)

# Run pipeline
result = source >> CSSR(config) >> Analyzer()

# Access results
print(f"States: {len(result.machine.states)}")
print(f"Cμ = {result.summary.statistical_complexity:.4f}")

# Visualize
render_diagram(result.machine, "output.png")
```

## Pipeline Protocol

Any object implementing `__rshift__` can participate in pipelines:

```python
from emic.pipeline import Pipeable

class MyProcessor(Pipeable):
    def __rshift__(self, other):
        # Process and pass to next stage
        result = self.process()
        return other.receive(result)
```

## Debugging Pipelines

Break apart pipelines to inspect intermediate results:

```python
# Step by step
source = GoldenMeanSource(p=0.5, seed=42)
data = source.take(10_000)
print(f"Data length: {len(data)}")

inference_result = CSSR(config).infer(data)
print(f"Converged: {inference_result.converged}")
print(f"States: {len(inference_result.machine.states)}")

analysis = Analyzer().analyze(inference_result.machine)
print(f"Cμ = {analysis.statistical_complexity:.4f}")
```
