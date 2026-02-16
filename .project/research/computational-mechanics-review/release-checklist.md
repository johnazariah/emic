# Release Checklist

Steps for releasing a new version of `emic` and its associated publications.

---

## Pre-release

- [ ] All tests pass: `uv run pytest`
- [ ] Type check clean: `uv run pyright`
- [ ] Lint clean: `uv run ruff check . && uv run ruff format --check .`
- [ ] Coverage ≥ 82%: `uv run pytest --cov=src/emic --cov-report=term-missing`
- [ ] CHANGELOG.md updated with new version section
- [ ] Version bumped in `pyproject.toml`
- [ ] Documentation builds: `uv run mkdocs build`

## JOSS Paper

- [ ] `paper-joss/paper.md` YAML frontmatter is correct:
  - `date` matches release date
  - `bibliography: paper.bib` is set
  - Author ORCID and affiliation are current
- [ ] `paper-joss/paper.bib` references are complete (no placeholder arXiv IDs)
- [ ] Word count is 750–1750 words
- [ ] All required JOSS sections present:
  - Summary
  - Statement of Need
  - State of the Field
  - Software Design
  - Research Impact Statement
  - AI Usage Disclosure
  - Acknowledgements
  - References
- [ ] JOSS PDF builds locally:
  ```bash
  docker run --rm --volume "$PWD/joss:/data" \
      --user "$(id -u):$(id -g)" --env JOURNAL=joss \
      openjournals/inara
  ```
- [ ] Paper renders correctly (table, math, citations all resolve)

## Associated Publication (arXiv)

- [ ] Technical report final draft reviewed (includes Appendix B: CM review)
- [ ] arXiv package builds:
  ```bash
  cd .project/research/computational-mechanics-review
  make arxiv
  ```
- [ ] arXiv package verifies (compile from source):
  ```bash
  make verify
  ```
- [ ] Technical report submitted to arXiv and arXiv ID obtained
- [ ] `paper-joss/paper.bib` updated with arXiv eprint ID:
  ```bibtex
  eprint = {2602.XXXXX},
  archiveprefix = {arXiv},
  ```

## Release

- [ ] Create and push tag: `git tag v0.X.0 && git push origin v0.X.0`
- [ ] GitHub Actions:
  - CI passes
  - JOSS paper PDF built (check `draft-paper.yml` action)
  - Package published to PyPI
  - GitHub Release created with:
    - `.tar.gz` and `.whl` package artifacts
    - `paper.pdf` (JOSS paper) attached
- [ ] Verify PyPI install: `pip install emic==0.X.0`

## Post-release

- [ ] Archive release on Zenodo (for DOI — required by JOSS)
- [ ] Submit to JOSS at https://joss.theoj.org/papers/new
  - Repository URL: `https://github.com/johnazariah/emic`
  - Mention associated arXiv publications in submission notes
- [ ] Update JOURNAL.md with release notes
- [ ] Update ROADMAP.md with completed milestones
