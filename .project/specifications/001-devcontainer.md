# Specification 001: Development Container

## Status
📋 Draft

## Overview
A devcontainer configuration that provides a reproducible development environment for:
- Python development with modern tooling
- LaTeX document generation for papers and results
- Jupyter notebook support for interactive exploration

## Requirements

### Python Environment
- **Python Version**: 3.11+ (for modern typing features like `Self`, `TypeVarTuple`)
- **Package Manager**: `uv` (fast, modern Python package manager)
- **Type Checking**: `pyright` or `mypy` in strict mode
- **Testing**: `pytest` with `pytest-cov` for coverage
- **Formatting**: `ruff` (linting + formatting)
- **Functional Programming**: Consider `returns` or `toolz` libraries

### LaTeX Environment
- **Distribution**: TeX Live (full or science scheme)
- **Build Tool**: `latexmk` for automated builds
- **Editor Support**: LaTeX Workshop extension
- **Bibliography**: BibTeX/BibLaTeX support

### Jupyter Support
- **Kernel**: IPython kernel linked to project environment
- **Extensions**: Jupyter extension for VS Code

### VS Code Extensions
- Python (ms-python.python)
- Pylance (ms-python.pylance)
- Jupyter (ms-toolsai.jupyter)
- LaTeX Workshop (james-yu.latex-workshop)
- Ruff (charliermarsh.ruff)
- Git Graph (mhutchie.git-graph)

## Container Base
- Use `mcr.microsoft.com/devcontainers/python:3.11` as base
- Add TeX Live via apt or dedicated layer
- Consider multi-stage build if image size is a concern

## Directory Structure
```
.devcontainer/
├── devcontainer.json      # Main configuration
├── Dockerfile             # Custom container build
├── postCreateCommand.sh   # Setup script after container creation
└── requirements-dev.txt   # Development dependencies
```

## Acceptance Criteria
- [ ] Container builds successfully
- [ ] Python environment with type checking works
- [ ] pytest discovers and runs tests
- [ ] LaTeX documents compile with latexmk
- [ ] Jupyter notebooks run with project kernel
- [ ] All VS Code extensions install and function

## Notes
- Keep image size reasonable (< 4GB if possible)
- Cache pip/uv downloads for faster rebuilds
- Consider GPU support as optional extension for future ML work
