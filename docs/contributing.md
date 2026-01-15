# Contributing

Thank you for your interest in contributing to `emic`!

## Development Setup

1. Clone the repository:

```bash
git clone https://github.com/johnazariah/emic.git
cd emic
```

2. Install with development dependencies:

```bash
uv sync --dev
```

3. Install pre-commit hooks:

```bash
uv run pre-commit install
```

## Code Style

- **Formatting**: We use [Ruff](https://github.com/astral-sh/ruff) for formatting
- **Linting**: Ruff for linting as well
- **Type checking**: [Pyright](https://github.com/microsoft/pyright) in strict mode
- **Docstrings**: Google style

Pre-commit hooks automatically check these before each commit.

## Running Tests

```bash
# All tests
uv run pytest

# With coverage
uv run pytest --cov=src/emic --cov-report=term-missing

# Specific test file
uv run pytest tests/unit/test_cssr.py -v
```

## Documentation

Build docs locally:

```bash
uv run mkdocs serve
```

Then visit http://localhost:8000

### Docstring Requirements

All public APIs must have Google-style docstrings:

```python
def my_function(param: str) -> int:
    """Short description.

    Longer description if needed.

    Args:
        param: Description of parameter.

    Returns:
        Description of return value.

    Raises:
        ValueError: When something is wrong.

    Example:
        >>> my_function("test")
        42
    """
```

## Architecture

See `.project/adr/` for Architecture Decision Records explaining design choices.

See `.project/specifications/` for detailed feature specifications.

## Pull Request Process

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make your changes
4. Ensure tests pass: `uv run pytest`
5. Ensure linting passes: `uv run ruff check src tests`
6. Commit with conventional commits: `git commit -m "feat: add new feature"`
7. Push and create a PR

## Commit Messages

We use [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation only
- `test:` Adding tests
- `refactor:` Code refactoring
- `chore:` Maintenance tasks

## Questions?

Open an issue on GitHub or reach out to the maintainers.
