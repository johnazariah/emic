# Specification 007: Pipeline Composition

## Status
📋 Draft

## Overview

This specification defines how pipeline stages compose together using the `>>` operator, enabling fluent, readable workflows.

```python
result = (
    GoldenMeanSource(p=0.5, seed=42)
    >> TakeN(10_000)
    >> CSSR(CSSRConfig(max_history=5))
    >> analyze
    >> to_latex_table
)
```

## Design Principles

- **Operator overloading**: Use `>>` for left-to-right composition
- **Type-safe**: Compositions checked by type system
- **Lazy where possible**: Computation deferred until needed
- **Debuggable**: Intermediate values accessible

---

## 1. The `>>` Operator

### Implementation Strategy

Python's `>>` operator is implemented via `__rshift__` (on the left operand) or `__rrshift__` (on the right operand).

For pipelines, we use `__rshift__` on pipeline-aware objects:

```python
class Pipeable(Protocol[T]):
    """An object that can participate in pipelines."""
    
    def __rshift__(self, other: Callable[[T], U]) -> U:
        """Pipe self into a callable."""
        ...
```

### Base Mixin

```python
from typing import TypeVar, Callable, Generic

T = TypeVar('T')
U = TypeVar('U')

class PipeableMixin(Generic[T]):
    """
    Mixin that adds pipeline support via >> operator.
    
    Classes that inherit this can be used as the left side of >>.
    The right side must be a callable that accepts the object.
    """
    
    def __rshift__(self, other: Callable[['PipeableMixin[T]'], U]) -> U:
        return other(self)
    
    def pipe(self, *funcs: Callable) -> Any:
        """
        Apply a sequence of functions.
        
        Alternative to chained >> for programmatic composition.
        """
        result: Any = self
        for f in funcs:
            result = f(result)
        return result
```

---

## 2. Stage Types

### 2.1 Sources (Start of Pipeline)

Sources produce data. They implement `__rshift__` to pass themselves to transforms.

```python
class SequenceSource(PipeableMixin[Iterator[A]], Protocol[A]):
    """Sources are pipeable."""
    
    def __iter__(self) -> Iterator[A]: ...
    
    @property
    def alphabet(self) -> frozenset[A]: ...
```

Example:
```python
GoldenMeanSource(p=0.5) >> TakeN(1000)
#                       └─ TakeN receives the source
```

### 2.2 Transforms (Middle of Pipeline)

Transforms are callables that take input and produce output. They should also be pipeable for chaining.

```python
@dataclass(frozen=True)
class TakeN(Generic[A]):
    """Transform: take first N elements."""
    
    n: int
    
    def __call__(self, source: SequenceSource[A]) -> 'SequenceData[A]':
        from itertools import islice
        symbols = tuple(islice(source, self.n))
        return SequenceData(symbols, _alphabet=source.alphabet)
```

For transforms to be chainable on the right side of `>>`, the output must also be pipeable:

```python
@dataclass(frozen=True)
class SequenceData(PipeableMixin['SequenceData[A]'], Generic[A]):
    """Finite sequence - also pipeable."""
    
    symbols: tuple[A, ...]
    _alphabet: frozenset[A] | None = None
    
    def __iter__(self) -> Iterator[A]:
        return iter(self.symbols)
```

### 2.3 Inference (Produces Results)

Inference algorithms are callables that produce `InferenceResult`:

```python
@dataclass
class CSSR(Generic[A]):
    config: CSSRConfig
    
    def __call__(
        self, 
        source: Iterable[A]
    ) -> InferenceResult[A]:
        return self.infer(source)
    
    # Also support being on the right side
    def __rrshift__(self, source: Iterable[A]) -> InferenceResult[A]:
        return self(source)
```

### 2.4 Analysis (Functions on Machines)

Analysis functions are plain callables:

```python
def analyze(machine: EpsilonMachine[A]) -> AnalysisSummary:
    ...

def statistical_complexity(machine: EpsilonMachine[A]) -> float:
    ...
```

To use in pipelines, `InferenceResult` must be pipeable and extract the machine:

```python
@dataclass(frozen=True)
class InferenceResult(PipeableMixin['InferenceResult[A]'], Generic[A]):
    machine: EpsilonMachine[A]
    # ... other fields
    
    def __rshift__(self, other: Callable) -> Any:
        # If other expects a machine, pass the machine
        # If other expects InferenceResult, pass self
        import inspect
        sig = inspect.signature(other)
        params = list(sig.parameters.values())
        if params and 'machine' in str(params[0].annotation).lower():
            return other(self.machine)
        # Try with machine first
        try:
            return other(self.machine)
        except TypeError:
            return other(self)
```

Or more simply, provide explicit extraction:

```python
# Explicit machine extraction
result = (
    source
    >> TakeN(10_000)
    >> CSSR(config)
)
machine = result.machine
summary = analyze(machine)
```

---

## 3. Pipeline Builder

For complex pipelines, provide a builder pattern:

```python
from typing import Callable, Any

class Pipeline(Generic[A]):
    """
    A reusable pipeline that can be applied to multiple sources.
    
    Example:
        >>> pipeline = (
        ...     Pipeline[int]()
        ...     .take(10_000)
        ...     .infer(CSSR(CSSRConfig(max_history=5)))
        ...     .analyze()
        ... )
        >>> 
        >>> result1 = pipeline.run(GoldenMeanSource(p=0.3))
        >>> result2 = pipeline.run(GoldenMeanSource(p=0.7))
    """
    
    def __init__(self) -> None:
        self._steps: list[Callable] = []
    
    def take(self, n: int) -> 'Pipeline[A]':
        """Add a TakeN step."""
        self._steps.append(TakeN(n))
        return self
    
    def skip(self, n: int) -> 'Pipeline[A]':
        """Add a SkipN step."""
        self._steps.append(SkipN(n))
        return self
    
    def infer(self, algorithm: InferenceAlgorithm[A]) -> 'Pipeline[A]':
        """Add an inference step."""
        self._steps.append(algorithm)
        return self
    
    def analyze(self) -> 'Pipeline[A]':
        """Add analysis step."""
        self._steps.append(lambda r: (r, analyze(r.machine)))
        return self
    
    def run(self, source: SequenceSource[A]) -> Any:
        """Execute the pipeline on a source."""
        result: Any = source
        for step in self._steps:
            result = step(result)
        return result
    
    def __call__(self, source: SequenceSource[A]) -> Any:
        return self.run(source)
```

---

## 4. Error Propagation

Errors propagate naturally through pipelines via Python exceptions:

```python
try:
    result = (
        source
        >> TakeN(100)  # Too few samples
        >> CSSR(CSSRConfig(max_history=5))
    )
except InsufficientDataError as e:
    print(e.explain())
```

For pipelines that should collect errors without stopping:

```python
from dataclasses import dataclass
from typing import Union

@dataclass
class PipelineError:
    """Represents a pipeline failure."""
    stage: str
    error: Exception

@dataclass
class SafePipeline(Generic[A]):
    """A pipeline that catches and reports errors."""
    
    steps: list[tuple[str, Callable]]
    
    def run(self, source: SequenceSource[A]) -> Union[Any, PipelineError]:
        result: Any = source
        for name, step in self.steps:
            try:
                result = step(result)
            except Exception as e:
                return PipelineError(stage=name, error=e)
        return result
```

---

## 5. Parallel Pipelines

For running multiple analyses on the same source:

```python
from typing import NamedTuple

class ParallelResults(NamedTuple):
    """Results from parallel pipeline branches."""
    results: dict[str, Any]

def parallel(**branches: Callable) -> Callable:
    """
    Create a parallel pipeline stage.
    
    Example:
        >>> results = (
        ...     source
        ...     >> TakeN(10_000)
        ...     >> CSSR(config)
        ...     >> parallel(
        ...         complexity=statistical_complexity,
        ...         entropy=entropy_rate,
        ...         diagram=render_state_diagram,
        ...     )
        ... )
        >>> print(results['complexity'])
    """
    def apply(input: Any) -> dict[str, Any]:
        return {name: func(input) for name, func in branches.items()}
    return apply
```

---

## 6. Debugging Pipelines

### Tap (Inspect Without Modifying)

```python
def tap(func: Callable[[T], None]) -> Callable[[T], T]:
    """
    Create a tap that inspects values without modifying them.
    
    Example:
        >>> result = (
        ...     source
        ...     >> TakeN(10_000)
        ...     >> tap(lambda seq: print(f"Sequence length: {len(seq)}"))
        ...     >> CSSR(config)
        ...     >> tap(lambda r: print(f"Found {len(r.machine)} states"))
        ...     >> analyze
        ... )
    """
    def wrapper(value: T) -> T:
        func(value)
        return value
    return wrapper
```

### Log

```python
import logging

def log(
    message: str = "Pipeline stage",
    level: int = logging.DEBUG,
) -> Callable[[T], T]:
    """Log a value passing through the pipeline."""
    logger = logging.getLogger("emic.pipeline")
    
    def wrapper(value: T) -> T:
        logger.log(level, f"{message}: {type(value).__name__}")
        return wrapper
    return wrapper
```

---

## 7. Type Safety

With proper type annotations, type checkers can validate pipelines:

```python
from typing import TypeVar, Callable, overload

A = TypeVar('A')
B = TypeVar('B')
C = TypeVar('C')

# The >> operator with proper types
class Pipeable(Generic[A]):
    @overload
    def __rshift__(self, other: Callable[[A], B]) -> B: ...
    
    def __rshift__(self, other: Callable[[A], Any]) -> Any:
        return other(self)
```

Type checkers will catch errors like:
```python
# Type error: CSSR expects Iterable, got float
result = (
    1.0  # Wrong type!
    >> CSSR(config)
)
```

---

## 8. Module Structure

```
emic/pipeline/
├── __init__.py           # Re-exports
├── base.py               # PipeableMixin, Pipeable protocol
├── builder.py            # Pipeline builder class
├── operators.py          # tap, log, parallel
└── safe.py               # SafePipeline with error handling
```

---

## 9. Usage Examples

### Basic Pipeline

```python
from emic.sources import GoldenMeanSource, TakeN
from emic.inference import CSSR, CSSRConfig
from emic.analysis import analyze

# Fluent pipeline
summary = (
    GoldenMeanSource(p=0.5, seed=42)
    >> TakeN(50_000)
    >> CSSR(CSSRConfig(max_history=5))
    >> (lambda r: analyze(r.machine))
)

print(summary)
```

### Reusable Pipeline

```python
from emic.pipeline import Pipeline

# Define once
standard_analysis = (
    Pipeline[int]()
    .take(50_000)
    .infer(CSSR(CSSRConfig(max_history=5)))
    .analyze()
)

# Apply to multiple sources
for p in [0.3, 0.5, 0.7]:
    source = GoldenMeanSource(p=p, seed=42)
    result = standard_analysis(source)
    print(f"p={p}: Cμ={result.statistical_complexity:.4f}")
```

### Debugging Pipeline

```python
from emic.pipeline import tap

result = (
    GoldenMeanSource(p=0.5, seed=42)
    >> tap(lambda s: print(f"Source: {s}"))
    >> TakeN(10_000)
    >> tap(lambda seq: print(f"Sequence: {len(list(seq))} symbols"))
    >> CSSR(CSSRConfig(max_history=5))
    >> tap(lambda r: print(f"Machine: {len(r.machine)} states"))
    >> (lambda r: analyze(r.machine))
)
```

---

## Acceptance Criteria

- [ ] `>>` operator works for all stage types
- [ ] Type annotations pass pyright strict mode
- [ ] `PipeableMixin` works as documented
- [ ] `Pipeline` builder provides fluent API
- [ ] `tap` and `log` debugging helpers work
- [ ] `parallel` branching works
- [ ] Error propagation is clear
- [ ] Documentation with examples
- [ ] Unit tests for composition

## Dependencies

- Python 3.11+ (for modern typing)
- No external dependencies

## Related Specifications

- Spec 003: Source Protocol (pipeline entry)
- Spec 004: Inference Protocol (pipeline middle)
- Spec 005: Analysis Protocol (pipeline end)
- Spec 006: Output Protocol (pipeline end)
