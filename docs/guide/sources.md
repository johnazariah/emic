# Sources

Sources provide data for epsilon-machine inference. `emic` supports both **synthetic** sources (with known theoretical machines) and **empirical** sources (from real data).

## Synthetic Sources

Synthetic sources generate data from well-understood stochastic processes. They also provide their `true_machine` for comparison with inferred results.

### Golden Mean Process

The Golden Mean process forbids consecutive 1s:

```python
from emic.sources import GoldenMeanSource

source = GoldenMeanSource(p=0.5, seed=42)
data = source.take(10_000)

# Access the theoretical machine
true_machine = source.true_machine
print(f"True states: {len(true_machine.states)}")  # 2 states
```

**Parameters:**

- `p`: Probability of emitting 1 when in state that allows it (default: 0.5)
- `seed`: Random seed for reproducibility

### Even Process

The Even Process requires an even number of 1s between consecutive 0s:

```python
from emic.sources import EvenProcessSource

source = EvenProcessSource(p=0.5, seed=42)
data = source.take(10_000)
```

!!! note "Finite Sample Effects"
    The Even Process may infer more than 2 states with finite data.
    This is expected behavior documented in Shalizi & Crutchfield (2001).
    Use `post_merge=True` in CSSR config to merge equivalent states.

### Biased Coin

An i.i.d. Bernoulli process (1 state):

```python
from emic.sources import BiasedCoinSource

source = BiasedCoinSource(p=0.7, seed=42)  # 70% probability of 1
```

### Periodic Process

A deterministic repeating pattern:

```python
from emic.sources import PeriodicSource

source = PeriodicSource(pattern=[0, 1, 0, 1, 1])  # Period of 5
```

## Empirical Sources

Load data from sequences or files:

```python
from emic.sources import SequenceData

# From a list
data = SequenceData([0, 1, 0, 0, 1, 0, 1])

# From a string (binary)
data = SequenceData.from_string("0100101")

# From a file
data = SequenceData.from_file("data.txt")
```

## Transforms

Transform sources using the `>>` operator or methods:

### Take

Limit the number of symbols:

```python
from emic.sources import GoldenMeanSource

source = GoldenMeanSource(p=0.5)
data = source.take(1000)  # Get exactly 1000 symbols
```

### Skip

Skip initial symbols (burn-in):

```python
source = GoldenMeanSource(p=0.5)
data = source.skip(100).take(1000)  # Skip 100, then take 1000
```

## Creating Custom Sources

Implement the `Source` protocol:

```python
from typing import Iterator
from emic.sources import Source
from emic.types import Symbol, EpsilonMachine

class MySource(Source):
    @property
    def alphabet(self) -> tuple[Symbol, ...]:
        return (0, 1)

    @property
    def true_machine(self) -> EpsilonMachine | None:
        return None  # Or provide if known

    def __iter__(self) -> Iterator[Symbol]:
        while True:
            yield self._generate_next()
```
