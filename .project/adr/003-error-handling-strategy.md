# ADR-003: Error Handling Strategy

## Status
**Accepted** — 2026-01-14

## Context

We need to decide how to handle errors throughout the framework. This affects:
- Pipeline composition (how errors propagate)
- User experience (clarity of error messages)
- Code complexity (verbosity vs. safety)
- Testing (how we verify error conditions)

### Requirements

- Errors in pipelines should be **clear** and **informative**
- Different audiences need different error experiences:
  - Researchers: detailed errors for debugging
  - Learners: friendly explanations
- Must distinguish between:
  - **Domain errors**: expected failures (insufficient data, non-convergence)
  - **Programming errors**: bugs (type mismatches, invalid arguments)

### Options Considered

#### Option A: Pure Result Types Everywhere
```python
def process(x: T) -> Result[U, Error]:
    ...

# Composition via bind/map
result = (
    source.generate()
    .bind(infer_machine)
    .map(compute_complexity)
)
```

**Pros**: Fully explicit, composable, type-safe
**Cons**: Verbose without monadic sugar (no do-notation in Python), unfamiliar, library dependency

#### Option B: Exceptions with Rich Error Types
```python
def process(x: T) -> U:
    if error_condition:
        raise InferenceError("message", context=...)
    return result
```

**Pros**: Pythonic, familiar, concise, works with try/except
**Cons**: Hidden control flow (but idiomatic for Python)

#### Option C: Hybrid (Result + Exceptions)
Mix of Result types for some operations, exceptions for others.

**Cons**: Two mental models, inconsistent API, confusing for users

## Decision

**We adopt Option B: Idiomatic Python Exceptions with Rich Error Types**

### Rationale

Result types (Option A) are elegant in languages with monadic syntactic sugar (Haskell's `do`, Scala's `for`, F#'s `let!`). Without this, Python code becomes verbose:

```python
# What we'd have to write in Python
result1 = step1(input)
if isinstance(result1, Failure):
    return result1
result2 = step2(result1.unwrap())
if isinstance(result2, Failure):
    return result2
# ... tedious and error-prone
```

Python's exception system is well-understood, works with the language's control flow, and is what users expect. We can still have **structured, informative errors** using a proper exception hierarchy with rich context.

### Detailed Strategy

#### 1. Exception Hierarchy

All framework exceptions inherit from a common base:

```python
class EpsilonMachineError(Exception):
    """Base exception for all epsilon-machine framework errors."""
    
    def __init__(self, message: str, **context: Any):
        super().__init__(message)
        self.message = message
        self.context = context
    
    def explain(self) -> str:
        """Return a user-friendly explanation of the error."""
        return self.message


class InferenceError(EpsilonMachineError):
    """Errors during epsilon-machine inference."""
    pass


class InsufficientDataError(InferenceError):
    """Not enough data to perform inference."""
    
    def __init__(self, required: int, provided: int, **context: Any):
        super().__init__(
            f"Insufficient data: need {required} symbols, got {provided}",
            required=required,
            provided=provided,
            **context
        )
        self.required = required
        self.provided = provided
    
    def explain(self) -> str:
        return (
            f"The sequence is too short for reliable inference. "
            f"You provided {self.provided} symbols, but the algorithm "
            f"needs at least {self.required}. Try using a longer sequence."
        )


class NonConvergenceError(InferenceError):
    """Algorithm did not converge within iteration limit."""
    
    def __init__(self, iterations: int, tolerance: float, **context: Any):
        super().__init__(
            f"Did not converge after {iterations} iterations (tol={tolerance})",
            iterations=iterations,
            tolerance=tolerance,
            **context
        )
```

#### 2. Error Categories

| Exception | When | Example |
|-----------|------|---------|
| `InsufficientDataError` | Too few observations | Sequence shorter than required for L-history |
| `NonConvergenceError` | Algorithm didn't stabilize | CSSR splitting didn't terminate |
| `InvalidSequenceError` | Malformed input | Symbols outside declared alphabet |
| `NumericalError` | Floating-point issues | Probability doesn't sum to 1 |
| `SerializationError` | I/O failures | Corrupt file, invalid format |
| `ValueError` | Invalid arguments | `max_history < 1` |
| `TypeError` | Wrong types | Passing int where Sequence expected |

#### 3. Usage Patterns

**Basic usage (let exceptions propagate):**
```python
machine = infer_cssr(sequence, max_history=5)
complexity = compute_statistical_complexity(machine)
```

**Handling specific errors:**
```python
try:
    machine = infer_cssr(sequence, max_history=5)
except InsufficientDataError as e:
    print(e.explain())  # User-friendly message
    print(f"Details: needed {e.required}, got {e.provided}")
except InferenceError as e:
    print(f"Inference failed: {e}")
```

**Context managers for pipelines:**
```python
from contextlib import contextmanager

@contextmanager
def inference_context(on_error: Callable[[EpsilonMachineError], None] = None):
    """Wrap pipeline execution with error handling."""
    try:
        yield
    except EpsilonMachineError as e:
        if on_error:
            on_error(e)
        else:
            raise

# Usage
with inference_context(on_error=lambda e: print(e.explain())):
    machine = infer_cssr(sequence, max_history=5)
```

#### 4. Pipeline Composition

Pipelines work naturally with Python's exception propagation:

```python
# Clean pipeline - exceptions bubble up automatically
def analyze_sequence(sequence: Iterable[A], config: Config) -> AnalysisResult:
    machine = infer_cssr(sequence, config.max_history)
    return AnalysisResult(
        machine=machine,
        complexity=compute_statistical_complexity(machine),
        entropy_rate=compute_entropy_rate(machine),
    )

# Caller decides how to handle errors
try:
    result = analyze_sequence(my_sequence, config)
except InferenceError as e:
    # Handle gracefully
    result = AnalysisResult.failed(reason=e)
```

#### 5. Notebook-Friendly Helpers

For Jupyter, provide helpers that give friendly output:

```python
def try_infer(
    sequence: Iterable[A],
    max_history: int,
    explain_errors: bool = True
) -> EpsilonMachine[A] | None:
    """Try to infer a machine, with friendly error handling for notebooks."""
    try:
        return infer_cssr(sequence, max_history)
    except EpsilonMachineError as e:
        if explain_errors:
            from IPython.display import display, Markdown
            display(Markdown(f"**Inference failed:** {e.explain()}"))
        return None
```

#### 6. Logging Integration

Errors integrate with Python's logging:

```python
import logging

logger = logging.getLogger("emic")

def infer_cssr(...) -> EpsilonMachine[A]:
    try:
        # ... inference logic
    except Exception as e:
        logger.error(f"Inference failed: {e}", exc_info=True)
        raise InferenceError("Internal error during inference") from e
```

## Consequences

### Positive
- **Idiomatic**: Follows Python conventions users already know
- **Simple**: One error model, not two
- **Rich errors**: Structured exceptions with context and explanations
- **Composable**: Exceptions propagate naturally through pipelines
- **Debuggable**: Full stack traces, `raise ... from` chaining
- **No dependencies**: Uses Python builtins only

### Negative
- **Not explicit in signatures**: Must read docs/code to know what raises
- **Easy to ignore**: Callers can forget to handle (but this is true of all Python)

### Mitigations
- Document exceptions in docstrings using `Raises:` section
- Provide `try_*` variants that return `None` on failure
- Comprehensive tests for error paths

### Neutral
- Need to define and document exception hierarchy
- Tests cover exception raising and handling

## References
- [Python Exception Hierarchy](https://docs.python.org/3/library/exceptions.html)
- [PEP 3134 – Exception Chaining](https://peps.python.org/pep-3134/)
- [Google Python Style Guide - Exceptions](https://google.github.io/styleguide/pyguide.html#24-exceptions)
