# ADR-001: Programming Language Selection

## Status
**Accepted** — 2026-01-14

## Context

We are building an open-source experimental framework for epsilon-machine construction and analysis based on Crutchfield's computational mechanics. The framework must serve:

1. **Researchers** who want to tweak, extend, and compose custom pipelines
2. **Students and curious learners** who want to understand emergence as a property of computational sophistication

### Requirements Gathered

- The framework must be **extensible** — new algorithms, sources, and analyses can be plugged in
- Pipeline stages must be **composable** — users can build custom pipelines from modular components
- Sequence generators must be **pluggable** with support for different alphabet types
- Symbolic representation should be possible (different alphabets, exact computation)
- Must integrate with **LaTeX** for paper generation
- Must support **Jupyter notebooks** for educational content and publishing
- Code must be **functional and typed** with comprehensive tests
- Must be accessible to a wide audience

### Options Considered

#### Option A: Python with Functional Discipline
- Use Python 3.11+ with modern typing features
- Apply functional programming patterns via conventions and libraries
- Leverage scientific ecosystem (NumPy, SymPy, NetworkX, Matplotlib)

#### Option B: Scala
- Full parametric polymorphism and algebraic data types
- Native functional composition (for-comprehensions, monads)
- JVM ecosystem, Java interop

#### Option C: F#
- Excellent type system with type providers
- .NET ecosystem
- Native functional programming

## Decision

**We will use Python 3.11+ with strict functional discipline.**

### Rationale

| Factor | Python | Scala/F# |
|--------|--------|----------|
| Scientific Ecosystem | ✅ Excellent (NumPy, SciPy, NetworkX, SymPy, Matplotlib) | ⚠️ Limited |
| Jupyter/Notebooks | ✅ First-class support | ⚠️ Possible but awkward |
| Audience Accessibility | ✅ Very high (lingua franca of science) | ⚠️ Higher barrier |
| Type System | ⚠️ Gradual typing (mypy/pyright) | ✅ Full static typing |
| Functional Composition | ⚠️ Manual (requires discipline) | ✅ Native |
| LaTeX Integration | ✅ Easy | ⚠️ Doable but more work |

**Key insight**: The target audience (researchers and students) predominantly uses Python. The educational goal requires Jupyter notebooks, which are Python-native. The scientific libraries we need are best-in-class in Python.

### Mitigations for Python's Weaknesses

1. **Type Safety**: Use `pyright` in strict mode, enforce in CI
2. **Functional Patterns**: Use `returns` library for `Result`/`Maybe` monads
3. **Immutability**: Use frozen `dataclass` and `NamedTuple` throughout
4. **Composition**: Define custom `|` or `>>` operators for pipeline composition
5. **Testing**: Property-based testing with `hypothesis` to catch type-related bugs
6. **Future Escape Hatch**: Critical algorithms can be ported to Rust (via PyO3) if performance requires

## Consequences

### Positive
- Immediate access to best-in-class scientific libraries
- Low barrier to entry for target audience
- First-class Jupyter notebook support
- Large community for support and contributions

### Negative
- Type errors caught at runtime, not compile time (mitigated by strict type checking)
- Functional patterns require discipline, not enforced by language
- Performance ceiling lower than compiled languages (mitigated by NumPy vectorization and optional Rust extensions)

### Neutral
- Team must agree on and follow functional coding conventions
- Need to document patterns for contributors

## References
- [Python typing documentation](https://docs.python.org/3/library/typing.html)
- [returns library](https://github.com/dry-python/returns)
- [pyright](https://github.com/microsoft/pyright)
