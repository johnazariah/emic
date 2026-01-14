# Specification 001a: CI/CD Pipeline & Testing Strategy

## Status
📋 Draft

## Overview

This specification defines the continuous integration, continuous deployment pipeline, and testing strategy for the `emic` package. The goal is to ensure code quality, maintain high test coverage, and enable confident releases.

---

## 1. Test Framework Selection

### Decision: pytest + hypothesis

**pytest** is the de facto standard for Python testing:
- Rich plugin ecosystem
- Excellent fixture support
- Clear, readable test output
- Native support for parametrized tests

**hypothesis** for property-based testing:
- Already identified in ADR-001 as a dependency
- Essential for testing mathematical properties of epsilon machines
- Generates edge cases automatically
- Perfect for testing invariants (e.g., "probabilities sum to 1")

### Additional Testing Tools

| Tool | Purpose |
|------|---------|
| `pytest-cov` | Coverage measurement and reporting |
| `pytest-xdist` | Parallel test execution |
| `pytest-timeout` | Prevent hanging tests |
| `hypothesis` | Property-based testing |

---

## 2. Test Organization

### Directory Structure

```
tests/
├── conftest.py              # Shared fixtures
├── unit/                    # Unit tests (fast, isolated)
│   ├── test_core_types.py
│   ├── test_distributions.py
│   ├── test_causal_states.py
│   └── test_machines.py
├── integration/             # Integration tests (component interaction)
│   ├── test_inference_pipeline.py
│   ├── test_source_to_machine.py
│   └── test_analysis_chain.py
├── property/                # Property-based tests (hypothesis)
│   ├── test_distribution_properties.py
│   ├── test_machine_invariants.py
│   └── test_pipeline_composition.py
├── golden/                  # Known-answer tests
│   ├── test_golden_mean.py
│   ├── test_even_process.py
│   └── data/                # Expected outputs
│       ├── golden_mean_p05.json
│       └── even_process.json
└── notebooks/               # Notebook execution tests
    └── test_notebooks_execute.py
```

### Test Categories (pytest markers)

```python
# conftest.py
import pytest

def pytest_configure(config):
    config.addinivalue_line("markers", "unit: fast, isolated unit tests")
    config.addinivalue_line("markers", "integration: component integration tests")
    config.addinivalue_line("markers", "property: hypothesis property-based tests")
    config.addinivalue_line("markers", "golden: known-answer regression tests")
    config.addinivalue_line("markers", "slow: tests that take > 1 second")
    config.addinivalue_line("markers", "notebooks: notebook execution tests")
```

---

## 3. Test Strategy

### 3.1 Unit Tests

Fast, isolated tests for individual components:

```python
# tests/unit/test_distributions.py
import pytest
from emic.core import Distribution

class TestDistribution:
    def test_creation_normalizes(self):
        d = Distribution({'a': 2, 'b': 2})
        assert d['a'] == pytest.approx(0.5)
        assert d['b'] == pytest.approx(0.5)

    def test_empty_distribution_raises(self):
        with pytest.raises(ValueError, match="cannot be empty"):
            Distribution({})

    def test_entropy_uniform(self):
        d = Distribution({'a': 0.5, 'b': 0.5})
        assert d.entropy() == pytest.approx(1.0)  # log2(2) = 1
```

### 3.2 Property-Based Tests

Use Hypothesis to test mathematical invariants:

```python
# tests/property/test_distribution_properties.py
from hypothesis import given, strategies as st
from emic.core import Distribution

@given(st.dictionaries(
    st.text(min_size=1, max_size=1),
    st.floats(min_value=0.01, max_value=100),
    min_size=1,
    max_size=10
))
def test_distribution_sums_to_one(weights):
    d = Distribution(weights)
    assert sum(d.values()) == pytest.approx(1.0)

@given(st.dictionaries(
    st.text(min_size=1, max_size=1),
    st.floats(min_value=0.01, max_value=100),
    min_size=1,
    max_size=10
))
def test_entropy_non_negative(weights):
    d = Distribution(weights)
    assert d.entropy() >= 0
```

### 3.3 Golden Tests (Known-Answer)

Verify against known theoretical results:

```python
# tests/golden/test_golden_mean.py
import pytest
from emic.sources import GoldenMeanSource, TakeN
from emic.inference import CSSR, CSSRConfig

@pytest.mark.golden
def test_golden_mean_two_states():
    """Golden Mean process should infer exactly 2 causal states."""
    source = GoldenMeanSource(p=0.5, seed=42)
    result = source >> TakeN(50_000) >> CSSR(CSSRConfig(max_history=5))

    assert len(result.machine.states) == 2

@pytest.mark.golden
def test_golden_mean_entropy_rate():
    """Golden Mean entropy rate should match theoretical value."""
    source = GoldenMeanSource(p=0.5, seed=42)
    result = source >> TakeN(100_000) >> CSSR(CSSRConfig(max_history=5))

    # H(p) = -p*log2(p) - (1-p)*log2(1-p) for p=0.5 is 1.0
    # But for Golden Mean it's different
    # Theoretical: H = 0.5 * log2(2) = 0.5 bits
    assert result.machine.entropy_rate() == pytest.approx(0.5, rel=0.05)
```

### 3.4 Integration Tests

Test component interactions:

```python
# tests/integration/test_inference_pipeline.py
import pytest
from emic.sources import GoldenMeanSource, TakeN
from emic.inference import CSSR, CSSRConfig
from emic.analysis import analyze

@pytest.mark.integration
def test_full_pipeline_executes():
    """Verify complete pipeline from source to analysis."""
    result = (
        GoldenMeanSource(p=0.5, seed=42)
        >> TakeN(10_000)
        >> CSSR(CSSRConfig(max_history=3))
    )

    summary = analyze(result.machine)

    assert summary.statistical_complexity >= 0
    assert summary.entropy_rate >= 0
    assert len(summary.states) >= 1
```

### 3.5 Notebook Tests

Ensure notebooks execute without errors:

```python
# tests/notebooks/test_notebooks_execute.py
import pytest
from pathlib import Path
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor

NOTEBOOKS_DIR = Path(__file__).parent.parent.parent / "notebooks"

@pytest.mark.notebooks
@pytest.mark.slow
@pytest.mark.parametrize("notebook", list(NOTEBOOKS_DIR.glob("*.ipynb")))
def test_notebook_executes(notebook):
    """Each notebook should execute without errors."""
    with open(notebook) as f:
        nb = nbformat.read(f, as_version=4)

    ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
    ep.preprocess(nb, {'metadata': {'path': str(NOTEBOOKS_DIR)}})
```

---

## 4. Coverage Requirements

### Minimum Coverage Thresholds

| Metric | Threshold | Rationale |
|--------|-----------|-----------|
| Line coverage | ≥ 90% | High coverage for library code |
| Branch coverage | ≥ 85% | Ensure conditional logic tested |
| Core types | 100% | Critical mathematical correctness |

### Coverage Configuration

```toml
# pyproject.toml additions
[tool.coverage.run]
source = ["src/emic"]
branch = true
omit = [
    "*/tests/*",
    "*/__init__.py",
]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise NotImplementedError",
    "if TYPE_CHECKING:",
    "@overload",
]
fail_under = 90
show_missing = true

[tool.coverage.html]
directory = "htmlcov"
```

---

## 5. CI/CD Pipeline (GitHub Actions)

### 5.1 Workflow: CI (on every push/PR)

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install uv
        uses: astral-sh/setup-uv@v4

      - name: Set up Python
        run: uv python install 3.11

      - name: Install dependencies
        run: uv sync --dev

      - name: Run ruff check
        run: uv run ruff check src tests

      - name: Run ruff format check
        run: uv run ruff format --check src tests

      - name: Run pyright
        run: uv run pyright src

  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.11", "3.12", "3.13"]

    steps:
      - uses: actions/checkout@v4

      - name: Install uv
        uses: astral-sh/setup-uv@v4

      - name: Set up Python ${{ matrix.python-version }}
        run: uv python install ${{ matrix.python-version }}

      - name: Install dependencies
        run: uv sync --dev

      - name: Run tests with coverage
        run: |
          uv run pytest tests/ \
            --cov=src/emic \
            --cov-report=xml \
            --cov-report=html \
            --cov-fail-under=90 \
            -v

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v4
        with:
          token: ${{ secrets.CODECOV_TOKEN }}
          files: ./coverage.xml
          fail_ci_if_error: true

  test-notebooks:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install uv
        uses: astral-sh/setup-uv@v4

      - name: Set up Python
        run: uv python install 3.11

      - name: Install dependencies
        run: uv sync --dev

      - name: Run notebook tests
        run: uv run pytest tests/notebooks/ -v -m notebooks
```

### 5.2 Workflow: Release (on version tags)

```yaml
# .github/workflows/release.yml
name: Release

on:
  push:
    tags:
      - 'v*'

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install uv
        uses: astral-sh/setup-uv@v4

      - name: Set up Python
        run: uv python install 3.11

      - name: Build package
        run: uv build

      - name: Upload artifacts
        uses: actions/upload-artifact@v4
        with:
          name: dist
          path: dist/

  test-release:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install uv
        uses: astral-sh/setup-uv@v4

      - name: Download artifacts
        uses: actions/download-artifact@v4
        with:
          name: dist
          path: dist/

      - name: Install from wheel
        run: |
          uv venv
          uv pip install dist/*.whl

      - name: Test import
        run: uv run python -c "import emic; print(emic.__version__)"

  publish-testpypi:
    needs: test-release
    runs-on: ubuntu-latest
    environment: testpypi
    permissions:
      id-token: write
    steps:
      - name: Download artifacts
        uses: actions/download-artifact@v4
        with:
          name: dist
          path: dist/

      - name: Publish to TestPyPI
        uses: pypa/gh-action-pypi-publish@release/v1
        with:
          repository-url: https://test.pypi.org/legacy/

  publish-pypi:
    needs: publish-testpypi
    runs-on: ubuntu-latest
    environment: pypi
    permissions:
      id-token: write
    steps:
      - name: Download artifacts
        uses: actions/download-artifact@v4
        with:
          name: dist
          path: dist/

      - name: Publish to PyPI
        uses: pypa/gh-action-pypi-publish@release/v1

  github-release:
    needs: publish-pypi
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - uses: actions/checkout@v4

      - name: Download artifacts
        uses: actions/download-artifact@v4
        with:
          name: dist
          path: dist/

      - name: Create GitHub Release
        uses: softprops/action-gh-release@v1
        with:
          files: dist/*
          generate_release_notes: true
```

### 5.3 Workflow: Docs (on main push)

```yaml
# .github/workflows/docs.yml
name: Documentation

on:
  push:
    branches: [main]

jobs:
  docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install uv
        uses: astral-sh/setup-uv@v4

      - name: Set up Python
        run: uv python install 3.11

      - name: Install dependencies
        run: uv sync --dev

      # Future: Generate API docs with mkdocs or sphinx
      # - name: Build docs
      #   run: uv run mkdocs build

      # - name: Deploy to GitHub Pages
      #   uses: peaceiris/actions-gh-pages@v3
      #   with:
      #     github_token: ${{ secrets.GITHUB_TOKEN }}
      #     publish_dir: ./site
```

---

## 6. Badge Configuration

Add these badges to README.md:

```markdown
[![CI](https://github.com/johnazariah/emic/actions/workflows/ci.yml/badge.svg)](https://github.com/johnazariah/emic/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/johnazariah/emic/branch/main/graph/badge.svg)](https://codecov.io/gh/johnazariah/emic)
[![PyPI version](https://badge.fury.io/py/emic.svg)](https://badge.fury.io/py/emic)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
```

---

## 7. Local Development Commands

### pytest.ini / pyproject.toml configuration

```toml
# pyproject.toml additions
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = [
    "-ra",
    "--strict-markers",
    "--strict-config",
]
markers = [
    "unit: fast, isolated unit tests",
    "integration: component integration tests",
    "property: hypothesis property-based tests",
    "golden: known-answer regression tests",
    "slow: tests that take > 1 second",
    "notebooks: notebook execution tests",
]
filterwarnings = [
    "error",
    "ignore::DeprecationWarning",
]
```

### Developer Commands

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src/emic --cov-report=html

# Run only fast tests
uv run pytest -m "unit and not slow"

# Run property-based tests with more examples
uv run pytest -m property --hypothesis-profile=ci

# Run specific test file
uv run pytest tests/unit/test_distributions.py -v

# Run tests in parallel
uv run pytest -n auto
```

---

## 8. Hypothesis Profiles

```python
# conftest.py additions
from hypothesis import settings, Verbosity

# CI profile: more examples, longer deadline
settings.register_profile(
    "ci",
    max_examples=500,
    deadline=None,
    suppress_health_check=[],
)

# Dev profile: faster feedback
settings.register_profile(
    "dev",
    max_examples=50,
    deadline=500,
)

# Load profile from environment
settings.load_profile(os.getenv("HYPOTHESIS_PROFILE", "dev"))
```

---

## 9. Pre-commit Hooks

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.5.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-toml
      - id: check-added-large-files

  - repo: local
    hooks:
      - id: pyright
        name: pyright
        entry: uv run pyright src
        language: system
        types: [python]
        pass_filenames: false
```

---

## 10. Test Fixtures Strategy

### Shared Fixtures

```python
# tests/conftest.py
import pytest
from emic.sources import GoldenMeanSource
from emic.core import EpsilonMachine, CausalState, Distribution

@pytest.fixture
def golden_mean_source():
    """Standard Golden Mean source for testing."""
    return GoldenMeanSource(p=0.5, seed=42)

@pytest.fixture
def simple_machine():
    """A minimal valid epsilon machine for testing."""
    state_a = CausalState(
        name="A",
        transitions={0: ("B", 0.5), 1: ("A", 0.5)}
    )
    state_b = CausalState(
        name="B",
        transitions={0: ("A", 1.0)}
    )
    return EpsilonMachine(
        states=frozenset([state_a, state_b]),
        initial_state="A",
        alphabet=frozenset([0, 1])
    )

@pytest.fixture
def sample_sequence():
    """A known sequence for deterministic tests."""
    return tuple([0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1])
```

---

## Acceptance Criteria

- [ ] pytest and hypothesis configured in pyproject.toml
- [ ] Coverage thresholds enforced (≥90% line, ≥85% branch)
- [ ] GitHub Actions CI workflow runs on all PRs
- [ ] GitHub Actions Release workflow publishes to PyPI
- [ ] Codecov integration displays coverage badge
- [ ] Pre-commit hooks configured
- [ ] Test directory structure created
- [ ] conftest.py with shared fixtures
- [ ] At least one test per test category (unit, property, golden, integration)

---

## Dependencies

### Development Dependencies

```toml
# pyproject.toml [project.optional-dependencies] or [tool.uv.dev-dependencies]
[tool.uv.dev-dependencies]
pytest = ">=8.0"
pytest-cov = ">=5.0"
pytest-xdist = ">=3.5"
pytest-timeout = ">=2.3"
hypothesis = ">=6.100"
nbformat = ">=5.10"
nbconvert = ">=7.16"
pre-commit = ">=3.7"
```

---

## Related Specifications

- Spec 001: DevContainer (development environment)
- ADR-001: Programming Language (Python testing ecosystem)
- ADR-003: Error Handling (exception testing patterns)

---

## Future Enhancements

- **Mutation testing**: Use `mutmut` to verify test quality
- **Benchmarking**: Add `pytest-benchmark` for performance tests
- **Snapshot testing**: For complex output validation
- **Documentation testing**: Test code examples in docstrings
