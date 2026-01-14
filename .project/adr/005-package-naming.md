# ADR-005: Package Naming

## Status
**Accepted** — 2026-01-14

## Context

We need a name for the Python package that will be:
- Published on PyPI
- Used in import statements
- Referenced in documentation and papers
- Memorable for the community

### Requirements

- Short and easy to type
- Meaningful connection to epsilon-machines / computational mechanics
- Available on PyPI (to be verified before publication)
- Works well in code: `import emic` / `from emic import ...`

## Decision

**The package will be named `emic`.**

### Rationale

**`emic`** works on multiple levels:

1. **Acronym**: **E**psilon **M**achine **I**nference & **C**haracterization
   - Directly describes what the package does

2. **Linguistic meaning**: In linguistics/anthropology, "emic" refers to analysis *from within the system* — understanding a culture or language on its own terms, as participants experience it
   - This resonates deeply with computational mechanics: ε-machines reveal the *intrinsic* computational structure of a process, not an externally imposed model
   - The "emic" perspective is about discovering structure that's *already there*

3. **Phonetic similarity**: Sounds like "ε-mic" (epsilon-machine)

4. **Practical benefits**:
   - 4 characters — minimal typing
   - Easy to pronounce
   - Distinctive and memorable
   - Likely available on PyPI

## Usage

```python
import emic
from emic import infer_cssr, EpsilonMachine
from emic.sources import GoldenMeanSource
from emic.analysis import statistical_complexity
```

## Consequences

### Positive
- Memorable, meaningful name with depth for those who discover the etymology
- Short import statements
- Distinctive in the Python ecosystem

### Negative
- May require explanation for those unfamiliar with the linguistic term
- Need to verify PyPI availability before first release

### Neutral
- Documentation should briefly explain the name's meaning

## References
- [Emic and etic (Wikipedia)](https://en.wikipedia.org/wiki/Emic_and_etic)
- Pike, K. L. (1967). *Language in Relation to a Unified Theory of the Structure of Human Behavior*
