# Specification Standards

*Standards for writing design specifications.*

---

## Purpose

Specifications document design decisions **before** implementation. They:
- Capture requirements and constraints
- Enable review and discussion
- Serve as reference during implementation
- Record rationale for future understanding

---

## Specification Structure

### Header

```markdown
# Specification NNN: Title

## Overview

One-paragraph summary of what this specification covers.

## Motivation

Why is this needed? What problem does it solve?
```

### Body Sections

Choose relevant sections:

```markdown
## Requirements

What must be true for this to be successful?

## Design

Technical approach and architecture.

## Interface

Public API with type signatures.

## Implementation

Key algorithms or data structures.

## Alternatives Considered

Other approaches and why they were rejected.

## Open Questions

Unresolved issues to address.

## References

External resources, papers, prior art.
```

### Footer

```markdown
## Status

- [ ] Reviewed
- [ ] Approved
- [ ] Implemented
- [ ] Tested
```

---

## Numbering

| Range | Category |
|-------|----------|
| 001-099 | Infrastructure |
| 100-199 | Core Types |
| 200-299 | Algorithms |
| 300-399 | Analysis |
| 400-499 | Visualization |
| 500-599 | Experimentation |
| 900-999 | Research/Future |

---

## Code in Specifications

### Interface Definitions

Show the public API:

```python
@dataclass(frozen=True)
class Config:
    """Configuration for the algorithm."""
    param: int = 10

class Algorithm:
    """Brief description."""

    def method(self, input: InputType) -> OutputType:
        """What the method does."""
        ...
```

### Pseudocode

For complex algorithms:

```
1. Initialize data structure
2. For each element in input:
   a. Process element
   b. Update state
3. Return result
```

---

## Review Process

1. **Draft** — Author writes initial spec
2. **Review** — Discuss in PR or meeting
3. **Revise** — Address feedback
4. **Approve** — Mark approved, ready for implementation
5. **Update** — Revise if implementation diverges

---

## Linking

- Link from specs to implementation: `Implemented in src/emic/module.py`
- Link from code to specs: `# See Spec 004: Inference Protocol`
- Cross-reference related specs: `See also: Spec 003`
