# emic

**E**psilon **M**achine **I**nference & **C**haracterization

A Python framework for constructing and analyzing epsilon-machines based on computational mechanics.

## What is an Epsilon-Machine?

An **epsilon-machine** (ε-machine) is the minimal, optimal predictor of a stochastic process. Introduced by James Crutchfield and collaborators, ε-machines capture the intrinsic computational structure hidden in sequential data.

<div class="grid cards" markdown>

-   :material-magnify:{ .lg .middle } **Inference**

    ---

    Reconstruct ε-machines from observed sequences using the CSSR algorithm

    [:octicons-arrow-right-24: Learn more](guide/inference.md)

-   :material-chart-bar:{ .lg .middle } **Analysis**

    ---

    Compute complexity measures: statistical complexity (Cμ), entropy rate (hμ), excess entropy

    [:octicons-arrow-right-24: Learn more](guide/analysis.md)

-   :material-dice-multiple:{ .lg .middle } **Sources**

    ---

    Built-in stochastic process generators and empirical data loading

    [:octicons-arrow-right-24: Learn more](guide/sources.md)

-   :material-pipe:{ .lg .middle } **Pipelines**

    ---

    Compose workflows with the `>>` operator

    [:octicons-arrow-right-24: Learn more](guide/pipelines.md)

</div>

## Quick Example

```python
from emic.sources import GoldenMeanSource
from emic.inference import CSSR, CSSRConfig
from emic.analysis import analyze

# Generate data from the Golden Mean process
source = GoldenMeanSource(p=0.5, seed=42)

# Infer the epsilon-machine
config = CSSRConfig(max_history=5, significance=0.001)
result = CSSR(config).infer(source.take(10_000))

# Analyze
summary = analyze(result.machine)
print(f"States: {len(result.machine.states)}")
print(f"Cμ = {summary.statistical_complexity:.4f}")
```

## Installation

```bash
pip install emic
```

## Key Concepts

- **Causal states**: Equivalence classes of histories that yield identical predictions
- **Statistical complexity** (Cμ): The entropy of the causal state distribution
- **Entropy rate** (hμ): The irreducible randomness in the process
- **Unifilarity**: Given a state and symbol, the next state is deterministic

## References

- Crutchfield, J.P. (1994). ["The Calculus of Emergence"](https://doi.org/10.1016/0167-2789(94)90273-9). *Physica D*.
- Shalizi, C.R. & Crutchfield, J.P. (2001). ["Computational Mechanics: Pattern and Prediction, Structure and Simplicity"](https://arxiv.org/abs/cond-mat/9907176). *Journal of Statistical Physics*.
