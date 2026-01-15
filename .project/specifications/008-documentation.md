# Specification 008: Documentation

## Overview

This specification defines the documentation deliverables for the `emic` framework, including API reference, user guide, and example notebooks showcasing pipelining and inference mechanisms.

## Deliverables

### 1. API Reference

**Location**: `docs/api/`

Auto-generated from docstrings using `mkdocs` + `mkdocstrings`.

#### Required Docstrings

All public APIs must have Google-style docstrings:

```python
def analyze(machine: EpsilonMachine) -> AnalysisSummary:
    """Compute complexity measures for an epsilon-machine.

    Calculates statistical complexity, entropy rate, and excess entropy
    using the stationary distribution over causal states.

    Args:
        machine: The epsilon-machine to analyze. Must be unifilar
            (deterministic given state and symbol).

    Returns:
        An AnalysisSummary containing all computed measures.

    Raises:
        ValueError: If the machine has no states.

    Example:
        >>> from emic.sources import GoldenMeanSource
        >>> from emic.analysis import analyze
        >>> source = GoldenMeanSource(p=0.5)
        >>> summary = analyze(source.true_machine)
        >>> print(f"Cμ = {summary.statistical_complexity:.4f}")
        Cμ = 0.9183
    """
```

#### Module Documentation

Each `__init__.py` must have a module-level docstring:

```python
"""Epsilon-machine inference algorithms.

This module provides algorithms for inferring epsilon-machines from
data sequences. The primary algorithm is CSSR (Causal State Splitting
Reconstruction).

Classes:
    CSSR: The CSSR inference algorithm.
    CSSRConfig: Configuration for CSSR.
    InferenceResult: Result container with pipeline support.

Example:
    >>> from emic.inference import CSSR, CSSRConfig
    >>> config = CSSRConfig(max_history=5)
    >>> result = CSSR(config).infer(data)
    >>> print(f"Inferred {len(result.machine.states)} states")
"""
```

### 2. User Guide

**Location**: `docs/guide/`

#### Chapters

1. **getting-started.md**
   - Installation (`pip install emic`)
   - First example: Golden Mean
   - Core concepts: epsilon-machine, causal state, unifilarity

2. **sources.md**
   - Synthetic sources and their `true_machine` property
   - Empirical sources from files/strings
   - Reproducibility with seeds
   - Transform pipeline (`>>` operator)

3. **inference.md**
   - CSSR algorithm overview
   - Configuration parameters and their effects
   - Interpreting results (convergence, state count)
   - Known limitations and tuning

4. **analysis.md**
   - Statistical complexity (Cμ)
   - Entropy rate (hμ)
   - Excess entropy (E)
   - Comparing true vs inferred machines

5. **visualization.md** (Phase 6)
   - State diagram rendering
   - LaTeX/TikZ export
   - Jupyter integration

6. **pipelines.md**
   - The `>>` operator philosophy
   - Composing sources, transforms, inference, analysis
   - Example pipelines

7. **advanced.md**
   - Custom sources
   - Custom inference algorithms
   - Extending the framework

### 3. How-To Guides

**Location**: `docs/howto/`

Practical, task-oriented guides for extending the framework.

#### 3.1 `howto-custom-source.md`
**Purpose**: Guide users in creating custom sequence sources

```python
"""How to create a custom sequence source.

This guide shows how to implement your own stochastic process
as a sequence source that integrates with the emic pipeline.
"""

from typing import Iterator
from emic.core import Symbol, EpsilonMachine
from emic.sources import StochasticSource

class MyCustomSource(StochasticSource[int]):
    """A custom source that generates symbols from your process.

    Args:
        param1: Description of first parameter.
        param2: Description of second parameter.
        _seed: Random seed for reproducibility.
    """

    def __init__(self, param1: float, param2: int, *, _seed: int | None = None):
        super().__init__(_seed=_seed)
        self._param1 = param1
        self._param2 = param2
        # Initialize your internal state here

    def _generate(self) -> Iterator[int]:
        """Generate symbols from your process.

        This is the core method - implement your process logic here.
        Use self._rng for random number generation to ensure reproducibility.
        """
        state = 0  # Your internal state
        while True:
            # Your generation logic
            if self._rng.random() < self._param1:
                symbol = 0
                state = (state + 1) % self._param2
            else:
                symbol = 1
                state = 0
            yield symbol

    @property
    def true_machine(self) -> EpsilonMachine:
        """Return the theoretical epsilon-machine for this process.

        This is optional but recommended - it allows comparing
        inferred machines against the ground truth.
        """
        from emic.core import EpsilonMachineBuilder

        builder = EpsilonMachineBuilder()
        # Build your true machine here
        # ...
        return builder.build()

# Usage in pipeline
source = MyCustomSource(param1=0.5, param2=3, _seed=42)
data = list(itertools.islice(source, 10000))
```

**Key Points**:
- Inherit from `StochasticSource[T]` where T is your symbol type
- Implement `_generate()` as an infinite iterator
- Use `self._rng` for all randomness (ensures seed reproducibility)
- Optionally implement `true_machine` for ground-truth comparison

#### 3.2 `howto-custom-inferrer.md`
**Purpose**: Guide users in creating custom inference algorithms

```python
"""How to create a custom inference algorithm.

This guide shows how to implement your own epsilon-machine
inference algorithm that integrates with the emic pipeline.
"""

from typing import Sequence
from dataclasses import dataclass
from emic.core import Symbol, EpsilonMachine
from emic.inference import InferenceResult

@dataclass(frozen=True)
class MyInferrerConfig:
    """Configuration for MyInferrer.

    Args:
        param1: Description of parameter.
        tolerance: Convergence tolerance.
    """
    param1: int = 10
    tolerance: float = 1e-6

class MyInferrer:
    """A custom epsilon-machine inference algorithm.

    Implements [cite your algorithm paper here].

    Args:
        config: Configuration parameters.
    """

    def __init__(self, config: MyInferrerConfig | None = None):
        self._config = config or MyInferrerConfig()

    def infer(self, data: Sequence[Symbol]) -> InferenceResult:
        """Infer an epsilon-machine from data.

        Args:
            data: The input sequence of symbols.

        Returns:
            InferenceResult containing the inferred machine and metadata.
        """
        # Step 1: Build your data structures
        # Step 2: Run your inference algorithm
        # Step 3: Construct the epsilon-machine

        from emic.core import EpsilonMachineBuilder

        builder = EpsilonMachineBuilder()
        # ... build machine from your inference ...
        machine = builder.build()

        # Return result with metadata
        return InferenceResult(
            machine=machine,
            converged=True,  # Did the algorithm converge?
            iterations=100,  # How many iterations?
            diagnostics={"my_metric": 0.95},  # Optional diagnostics
        )

    def __rrshift__(self, data: Sequence[Symbol]) -> InferenceResult:
        """Enable pipeline syntax: data >> MyInferrer()"""
        return self.infer(data)

# Usage
config = MyInferrerConfig(param1=20, tolerance=1e-8)
inferrer = MyInferrer(config)
result = inferrer.infer(data)

# Or with pipeline
result = data >> MyInferrer(config)
```

**Key Points**:
- Create a frozen dataclass for configuration
- Implement `infer(data) -> InferenceResult`
- Implement `__rrshift__` for pipeline support
- Return `InferenceResult` with convergence info and diagnostics

#### 3.3 `howto-custom-analyzer.md`
**Purpose**: Guide users in creating custom analysis measures

```python
"""How to create custom analysis measures.

This guide shows how to add your own complexity measures
or analysis functions to the emic framework.
"""

from emic.core import EpsilonMachine
from emic.analysis import AnalysisSummary

def my_custom_measure(machine: EpsilonMachine) -> float:
    """Compute a custom complexity measure.

    This measure calculates [describe your measure].

    Mathematical definition:
        M = sum_s π(s) * f(s)

    Args:
        machine: The epsilon-machine to analyze.

    Returns:
        The computed measure value.

    References:
        [1] Author, "Paper Title", Journal, Year.
    """
    from emic.analysis.measures import compute_stationary_distribution

    # Get the stationary distribution over states
    pi = compute_stationary_distribution(machine)

    # Compute your measure
    result = 0.0
    for state in machine.states:
        # Your computation here
        result += pi[state.id] * some_function(state)

    return result

# To integrate with analyze(), extend AnalysisSummary
@dataclass(frozen=True)
class ExtendedSummary(AnalysisSummary):
    """Extended analysis summary with custom measures."""
    my_measure: float = 0.0

def extended_analyze(machine: EpsilonMachine) -> ExtendedSummary:
    """Analyze with additional custom measures."""
    from emic.analysis import analyze

    base = analyze(machine)
    custom = my_custom_measure(machine)

    return ExtendedSummary(
        num_states=base.num_states,
        num_transitions=base.num_transitions,
        statistical_complexity=base.statistical_complexity,
        entropy_rate=base.entropy_rate,
        excess_entropy=base.excess_entropy,
        my_measure=custom,
    )

# Usage
summary = extended_analyze(machine)
print(f"My measure: {summary.my_measure:.4f}")
```

**Key Points**:
- Create a function `f(machine) -> float` for single measures
- Use `compute_stationary_distribution()` for π(s)
- Extend `AnalysisSummary` for integrated analysis
- Document mathematical definitions and references

#### 3.4 `howto-custom-visualizer.md`
**Purpose**: Guide users in creating custom visualization outputs

```python
"""How to create custom visualizations.

This guide shows how to create custom renderers for
epsilon-machines in different formats.
"""

from emic.core import EpsilonMachine

def to_mermaid(machine: EpsilonMachine) -> str:
    """Render epsilon-machine as Mermaid diagram.

    Mermaid is a text-based diagramming tool supported by
    GitHub, GitLab, and many documentation systems.

    Args:
        machine: The epsilon-machine to render.

    Returns:
        Mermaid diagram source code.

    Example:
        >>> print(to_mermaid(golden_mean.true_machine))
        stateDiagram-v2
            A --> A : 0 | 0.50
            A --> B : 1 | 0.50
            B --> A : 0 | 1.00
    """
    lines = ["stateDiagram-v2"]

    for state in machine.states:
        for transition in state.transitions:
            prob = transition.probability
            symbol = transition.symbol
            target = transition.target
            lines.append(f"    {state.id} --> {target} : {symbol} | {prob:.2f}")

    return "\n".join(lines)

def to_d3_json(machine: EpsilonMachine) -> dict:
    """Export epsilon-machine for D3.js visualization.

    Returns a dictionary suitable for D3 force-directed graphs.
    """
    nodes = [{"id": s.id, "group": 1} for s in machine.states]
    links = []

    for state in machine.states:
        for t in state.transitions:
            links.append({
                "source": state.id,
                "target": t.target,
                "symbol": str(t.symbol),
                "probability": t.probability,
            })

    return {"nodes": nodes, "links": links}

class JupyterMachineDisplay:
    """Rich display for epsilon-machines in Jupyter.

    Renders as an interactive diagram in Jupyter notebooks.
    """

    def __init__(self, machine: EpsilonMachine):
        self._machine = machine

    def _repr_html_(self) -> str:
        """HTML representation for Jupyter."""
        # Use SVG or embedded visualization
        from emic.output import render_state_diagram
        svg = render_state_diagram(self._machine, format="svg")
        return svg

    def _repr_mimebundle_(self, **kwargs):
        """Multiple format representations."""
        return {
            "text/html": self._repr_html_(),
            "text/plain": str(self._machine),
        }

# Usage
print(to_mermaid(machine))

# In Jupyter
from IPython.display import display
display(JupyterMachineDisplay(machine))
```

**Key Points**:
- Create functions `to_format(machine) -> str` for text formats
- Use `_repr_html_()` for Jupyter integration
- Export structured data (JSON) for JavaScript visualizations
- Consider both static (SVG, TikZ) and interactive (D3, Plotly) outputs

### 4. Example Notebooks

**Location**: `notebooks/`

#### 4.1 `demo_inference.ipynb` ✅
Already created. Demonstrates basic inference and analysis.

#### 4.2 `pipeline_showcase.ipynb`
**Purpose**: Demonstrate end-to-end pipelines

```python
# Pipeline 1: Source → Transform → Inference → Analysis
result = (
    GoldenMeanSource(p=0.5, _seed=42)
    >> TakeN(10000)
    >> CSSR(CSSRConfig(max_history=5))
    >> analyze
)

# Pipeline 2: File → Inference → Comparison
empirical = SequenceData.from_file("data/sequence.txt")
inferred = (empirical >> CSSR() >> analyze)
true_machine = GoldenMeanSource(p=0.5).true_machine
compare(analyze(true_machine), inferred)

# Pipeline 3: Multiple inference algorithms
from emic.inference import CSSR, BayesianInference  # future

algorithms = [
    ("CSSR", CSSR(CSSRConfig(max_history=5))),
    ("Bayesian", BayesianInference(prior=...)),  # future
]

for name, algo in algorithms:
    result = data >> algo >> analyze
    print(f"{name}: {result.num_states} states, Cμ={result.statistical_complexity:.4f}")
```

#### 4.3 `complexity_landscape.ipynb`
**Purpose**: Explore how complexity varies with process parameters

- Vary `p` in Golden Mean from 0 to 1
- Plot Cμ, hμ, E as functions of p
- Compare theoretical vs inferred values

#### 4.4 `inference_comparison.ipynb` (Future)
**Purpose**: Compare inference algorithms

- CSSR vs Bayesian vs Spectral
- Accuracy vs data length
- Convergence characteristics

### 5. README Updates

The main `README.md` should include:

```markdown
## Quick Start

```python
from emic.sources import GoldenMeanSource
from emic.inference import CSSR, CSSRConfig
from emic.analysis import analyze

# Generate data from the Golden Mean process
source = GoldenMeanSource(p=0.5, _seed=42)
data = list(source.take(10000))

# Infer the epsilon-machine
result = CSSR(CSSRConfig(max_history=5)).infer(data)
print(f"Inferred {result.machine.num_states} states")

# Analyze complexity
summary = analyze(result.machine)
print(f"Statistical Complexity: {summary.statistical_complexity:.4f} bits")
print(f"Entropy Rate: {summary.entropy_rate:.4f} bits/symbol")
```

## Features

- **Inference**: CSSR algorithm for epsilon-machine reconstruction
- **Analysis**: Statistical complexity, entropy rate, excess entropy
- **Sources**: Golden Mean, Even Process, Periodic, Biased Coin
- **Pipelines**: Composable `>>` operator for clean workflows
- **Visualization**: State diagrams, LaTeX export (coming soon)

## Documentation

- [User Guide](docs/guide/)
- [API Reference](docs/api/)
- [Example Notebooks](notebooks/)
```

## Implementation Notes

### Documentation Tooling

```toml
# pyproject.toml additions
[project.optional-dependencies]
docs = [
    "mkdocs>=1.5",
    "mkdocs-material>=9.0",
    "mkdocstrings[python]>=0.24",
]
```

### Build Commands

```bash
# Serve docs locally
mkdocs serve

# Build static site
mkdocs build
```

### CI Integration

Add to `.github/workflows/ci.yml`:

```yaml
docs:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - uses: astral-sh/setup-uv@v4
    - run: uv sync --extra docs
    - run: mkdocs build --strict
```

## Acceptance Criteria

- [ ] All public APIs have docstrings with examples
- [ ] User guide covers all major features
- [ ] How-to guide for custom sources with working example
- [ ] How-to guide for custom inferrers with pipeline support
- [ ] How-to guide for custom analyzers with measure extension
- [ ] How-to guide for custom visualizers with Jupyter integration
- [ ] Pipeline notebook demonstrates composition
- [ ] Complexity landscape notebook shows parameter exploration
- [ ] README has working quick-start example
- [ ] `mkdocs build` succeeds without warnings
- [ ] Documentation deployed to GitHub Pages
