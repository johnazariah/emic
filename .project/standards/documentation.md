# Documentation Standards

*Standards for project documentation.*

---

## Documentation Layers

| Layer | Location | Audience | Purpose |
|-------|----------|----------|---------|
| API Reference | `docs/api/` | Developers | Auto-generated from docstrings |
| User Guide | `docs/guide/` | Users | How to use the library |
| Specifications | `.project/specifications/` | Contributors | Design decisions |
| Standards | `.project/standards/` | Contributors | Process and conventions |
| Journal | `.project/record/` | Team | Work history |

---

## Docstring Standards

### Google Style

```python
def function(arg1: str, arg2: int = 10) -> bool:
    """Short description (one line).

    Longer description if needed. Can span multiple
    paragraphs.

    Args:
        arg1: Description of arg1.
        arg2: Description of arg2. Defaults to 10.

    Returns:
        Description of return value.

    Raises:
        ValueError: When arg1 is empty.

    Example:
        >>> function("hello", 20)
        True

    Note:
        Additional information.
    """
```

### Class Docstrings

```python
class MyClass:
    """Short description.

    Longer description of the class purpose and usage.

    Attributes:
        attr1: Description of attr1.
        attr2: Description of attr2.

    Example:
        >>> obj = MyClass(10)
        >>> obj.method()
    """
```

---

## README Standards

### Structure

1. **Title and badges**
2. **One-line description**
3. **Installation**
4. **Quick start example**
5. **Features**
6. **Documentation link**
7. **Contributing**
8. **License**

### Example

```markdown
# Project Name

[![CI](badge-url)](ci-url)
[![PyPI](badge-url)](pypi-url)

Brief description of what the project does.

## Installation

\`\`\`bash
pip install package-name
\`\`\`

## Quick Start

\`\`\`python
from package import main_function
result = main_function(data)
\`\`\`

## Documentation

Full documentation at [docs-url](docs-url).
```

---

## MkDocs Configuration

### Site Structure

```yaml
nav:
  - Home: index.md
  - Getting Started: getting-started.md
  - User Guide:
    - Topic 1: guide/topic1.md
    - Topic 2: guide/topic2.md
  - API Reference:
    - Module 1: api/module1.md
  - Contributing: contributing.md
```

### API Pages

```markdown
# Module Name

::: package.module
    options:
      show_source: true
      members_order: source
```

---

## Changelog Standards

### Format

```markdown
# Changelog

## [Unreleased]

### Added
- New features

### Changed
- Changes to existing features

### Fixed
- Bug fixes

### Removed
- Removed features

## [1.0.0] - 2026-01-15

### Added
- Initial release
```

### Guidelines

- Keep a running "Unreleased" section
- Use semantic versioning
- Link to issues/PRs where relevant
- Write for users, not developers

---

## Writing Style

### Tone

- Clear and concise
- Active voice preferred
- Present tense for descriptions
- Imperative for instructions

### Examples

- ✅ "Returns the computed value"
- ❌ "This function will return the computed value"
- ✅ "Run the tests with pytest"
- ❌ "You should run the tests with pytest"

### Code Examples

- Always tested (via doctest or separate tests)
- Minimal but complete
- Show expected output
- Handle imports explicitly
