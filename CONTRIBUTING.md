# Contributing to emic

Thank you for your interest in contributing to emic!

For full details on development setup, code style, testing, and the pull request process, see the **[Contributing Guide](https://johnazariah.github.io/emic/contributing/)**.

## Quick Start

```bash
git clone https://github.com/johnazariah/emic.git
cd emic
uv sync --dev
uv run pre-commit install
```

## Before Submitting

```bash
uv run ruff format . && uv run ruff check . --fix  # Format & lint
uv run pyright                                       # Type check
uv run pytest                                        # Tests (400+, 90% coverage)
```

All commits must pass formatting, type checks, and tests in CI.

## License

By contributing, you agree that your contributions will be licensed under the [MIT License](LICENSE).
