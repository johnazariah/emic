# Release Checklist

Steps for releasing a new version of `emic` and its associated publications.

---

## Pre-release

- [ ] Run `/.github/prompts/release.prompt.md` Phase 1–3 and capture outputs
- [ ] All tests pass: `uv run pytest`
- [ ] Type check clean: `uv run pyright`
- [ ] Lint clean: `uv run ruff check . && uv run ruff format --check .`
- [ ] Coverage ≥ 82%: `uv run pytest --cov=src/emic --cov-report=term-missing`
- [ ] CHANGELOG.md updated with new version section
- [ ] Version bumped in `pyproject.toml`
- [ ] Documentation builds: `uv run mkdocs build`
- [ ] Shared bibliography consistency check:
  - `paper-joss/paper.md` frontmatter points to `../shared/bibliography/references.bib`
  - Citation key format is `{first-author-name}{year}[{tag}]`

## JOSS Paper

- [ ] `paper-joss/paper.md` YAML frontmatter is correct:
  - `date` matches release date
  - `bibliography: ../shared/bibliography/references.bib` is set
  - Author ORCID and affiliation are current
- [ ] Shared bibliography references are complete (no placeholder arXiv IDs)
  - `shared/bibliography/references.bib`
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
- [ ] Shared bibliography updated with arXiv eprint ID:
  ```bibtex
  eprint = {2602.XXXXX},
  archiveprefix = {arXiv},
  ```

## Release

- [ ] Create and push tag: `git tag v0.X.0 && git push origin v0.X.0`
- [ ] GitHub Actions:
  - CI passes
  - JOSS submission bundle built (`paper.md` + `paper.bib` tarball)
  - Package published to PyPI
  - GitHub Release created with:
    - `.tar.gz` and `.whl` package artifacts
    - `emic-joss-submission-X.Y.Z.tar.gz` attached
- [ ] PDF papers are published via `.github/workflows/publications.yml` (not attached to package release)
- [ ] Verify PyPI install: `pip install emic==0.X.0`

## Post-release

- [ ] Archive release on Zenodo (for DOI — required by JOSS)
- [ ] Submit to JOSS at https://joss.theoj.org/papers/new
  - Repository URL: `https://github.com/johnazariah/emic`
  - Mention associated arXiv publications in submission notes
- [ ] Update JOURNAL.md with release notes
- [ ] Update ROADMAP.md with completed milestones
