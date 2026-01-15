# Standards Index

*Index of project standards documents.*

---

## Standards

| Document | Purpose |
|----------|---------|
| [Coding](coding.md) | Code style, types, architecture |
| [Documentation](documentation.md) | Docstrings, README, MkDocs |
| [Experimentation](experimentation.md) | Experiment design and execution |
| [Governance](governance.md) | Project organization, workflow |
| [Specifications](specifications.md) | Design specification format |

---

## Quick Reference

### Before Writing Code

1. Check for relevant [specification](../specifications/)
2. Follow [coding standards](coding.md)
3. Write tests first

### Before Committing

1. Run `uv run ruff format .`
2. Run `uv run ruff check . --fix`
3. Run `uv run pyright`
4. Run `uv run pytest`

### Before Starting an Experiment

1. Write hypothesis
2. Define metrics
3. Set random seed
4. Follow [experimentation protocol](experimentation.md)

### After a Work Session

1. Update [journal](../record/JOURNAL.md)
2. Update [roadmap](../plan/ROADMAP.md) if needed
