# Project Governance

*Standards for project organization and workflow.*

---

## Directory Structure

```
emic/
├── .devcontainer/          # Dev container configuration
├── .github/
│   └── workflows/          # CI/CD workflows
├── .project/               # Project management
│   ├── adr/                # Architecture Decision Records
│   ├── notes/              # Working notes
│   ├── plan/               # Roadmap and planning
│   ├── record/             # Journal and history
│   ├── references/         # External references
│   ├── specifications/     # Design specifications
│   └── standards/          # Process standards
├── docs/                   # MkDocs documentation
├── experiments/            # Experiment artifacts
├── scripts/                # Development scripts
├── src/emic/               # Source code
└── tests/                  # Test suite
```

---

## Planning Workflow

### Roadmap

Location: `.project/plan/ROADMAP.md`

- Updated weekly
- Contains milestones with status
- Tracks next actions
- Lists open questions

### Specifications

Location: `.project/specifications/`

Process:
1. Write spec before implementing significant features
2. Number sequentially (NNN-name.md)
3. Review and iterate
4. Mark status in spec
5. Update index

### Journal

Location: `.project/record/JOURNAL.md`

- Entry per working session
- Capture: completed, decisions, blockers
- Reverse chronological order
- Use template for consistency

---

## Git Workflow

### Branch Strategy

```
main (protected)
  ├── feature/add-algorithm
  ├── fix/edge-case-bug
  └── docs/update-guide
```

### Commit Messages

```
<type>: <short description>

<optional body>

<optional footer>
```

Types: `feat`, `fix`, `docs`, `test`, `refactor`, `chore`

### Pull Requests

- Reference related issues
- Include test coverage
- Pass all CI checks
- Squash merge to main

---

## Release Process

### Version Numbering

Semantic versioning: `MAJOR.MINOR.PATCH`

- MAJOR: Breaking API changes
- MINOR: New features, backward compatible
- PATCH: Bug fixes

### Release Checklist

1. [ ] Update version in `pyproject.toml`
2. [ ] Update CHANGELOG.md
3. [ ] Create release PR
4. [ ] Merge to main
5. [ ] Tag release: `git tag v1.2.3`
6. [ ] Push tag: `git push origin v1.2.3`
7. [ ] Verify GitHub Actions publish

---

## CI/CD

### Continuous Integration

Runs on every push:
- Formatting check (ruff format)
- Linting (ruff check)
- Type checking (pyright)
- Tests (pytest)
- Docs build (mkdocs)

### Continuous Deployment

On tag push (`v*`):
- Build package
- Publish to PyPI
- Deploy documentation

---

## Code Review

### Guidelines

- Review within 24 hours
- Be constructive
- Focus on:
  - Correctness
  - Test coverage
  - Documentation
  - API design

### Approval

- One approval required for merge
- Author merges after approval
- Squash commits
