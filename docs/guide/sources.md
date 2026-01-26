# Sources

Sources provide data for epsilon-machine inference. `emic` supports both **synthetic** sources (with known theoretical machines) and **empirical** sources (from real data).

## Synthetic Sources

Synthetic sources generate data from well-understood stochastic processes. They also provide their `true_machine` for comparison with inferred results.

### Golden Mean Process

The Golden Mean process forbids consecutive 1s:

```python
from emic.sources import GoldenMeanSource, TakeN

source = GoldenMeanSource(p=0.5, _seed=42)
data = TakeN(10_000)(source)

# Access the theoretical machine
true_machine = source.true_machine
print(f"True states: {len(true_machine.states)}")  # 2 states
```

**Parameters:**

- `p`: Probability of emitting 0 from state A (default: 0.5)
- `_seed`: Random seed for reproducibility

### Even Process

The Even Process requires 1s to appear in runs of even length:

```python
from emic.sources import EvenProcessSource, TakeN

source = EvenProcessSource(p=0.5, _seed=42)
data = TakeN(10_000)(source)
```

!!! note "Finite Sample Effects"
    The Even Process may infer more than 2 states with finite data.
    This is expected behavior documented in Shalizi & Crutchfield (2001).
    Use `post_merge=True` in CSSR config to merge equivalent states.

### Biased Coin

An i.i.d. Bernoulli process (1 state):

```python
from emic.sources import BiasedCoinSource, TakeN

source = BiasedCoinSource(p=0.7, _seed=42)  # 70% probability of 1
data = TakeN(1000)(source)
```

### Periodic Process

A deterministic repeating pattern:

```python
from emic.sources import PeriodicSource, TakeN

source = PeriodicSource(pattern=(0, 1, 0, 1, 1))  # Period of 5
data = TakeN(15)(source)  # Get 3 complete cycles
```

## Empirical Sources

Load data from sequences:

```python
from emic.sources import SequenceData

# From a tuple of symbols
data = SequenceData(symbols=(0, 1, 0, 0, 1, 0, 1))

# From a string (each character is a symbol)
data = SequenceData.from_string("AABBA")
# list(data) -> ['A', 'A', 'B', 'B', 'A']

# From a binary string
data = SequenceData.from_binary_string("01010")
# list(data) -> [0, 1, 0, 1, 0]
```

## Transforms

Transform sources using the `>>` operator or function call syntax:

### TakeN

Take the first N symbols from a source:

```python
from emic.sources import GoldenMeanSource, TakeN

source = GoldenMeanSource(p=0.5, _seed=42)
data = TakeN(1000)(source)  # Get exactly 1000 symbols
# Or with pipeline operator:
data = source >> TakeN(1000)
```

### SkipN

Skip initial symbols (burn-in):

```python
from emic.sources import GoldenMeanSource, SkipN, TakeN

source = GoldenMeanSource(p=0.5, _seed=42)
# Skip first 100 symbols, then take 1000
skipped = SkipN(100)(source)
data = TakeN(1000)(skipped)
```

### Pipeline Composition

Transforms can be chained with the `>>` operator:

```python
from emic.sources import GoldenMeanSource, SkipN, TakeN

data = GoldenMeanSource(p=0.5, _seed=42) >> SkipN(100) >> TakeN(1000)
```

### BitFlipNoise

Add observation noise to test robustness:

```python
from emic.sources import GoldenMeanSource, TakeN, BitFlipNoise

source = GoldenMeanSource(p=0.5, _seed=42)

# Add 5% bit-flip noise (binary symmetric channel)
noisy = source >> BitFlipNoise(flip_prob=0.05, seed=123) >> TakeN(10_000)
```

**Parameters:**

- `flip_prob`: Probability of flipping each symbol (0.0 to 0.5)
- `seed`: Random seed for reproducibility

!!! tip "Noise Robustness"
    Use `BitFlipNoise` to study how inference algorithms degrade under observation noise.
    Most algorithms maintain >80% accuracy up to 10% noise levels.

## Creating Custom Sources

Implement the `SequenceSource` protocol:

```python
from collections.abc import Iterator
from emic.sources import SequenceSource

class MySource:
    """Custom stochastic source."""

    @property
    def alphabet(self) -> frozenset[int]:
        return frozenset({0, 1})

    def __iter__(self) -> Iterator[int]:
        while True:
            yield self._generate_next()

    def _generate_next(self) -> int:
        # Your generation logic here
        return 0
```

For sources with known theoretical machines, you can also inherit from `StochasticSource`:

```python
from emic.sources import StochasticSource
from emic.types import EpsilonMachine

class MyStochasticSource(StochasticSource[int]):
    @property
    def true_machine(self) -> EpsilonMachine[int]:
        # Build and return the known epsilon-machine
        ...
```
