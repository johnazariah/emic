# Prepare and Execute a Python Package Release

Analyze changes since the last release, prepare documentation, validate quality, and execute the release ceremony.

---

## Phase 1: Analyze Release Scope

1. **Get the current version** from `pyproject.toml`:
   ```bash
   grep '^version' pyproject.toml
   ```

2. **List changes since last release**:
   ```bash
   LAST_TAG=$(git describe --tags --abbrev=0 2>/dev/null || echo "")
   if [ -n "$LAST_TAG" ]; then
       git log "$LAST_TAG..HEAD" --oneline
   else
       git log --oneline -20
   fi
   ```

3. **Categorize changes** and determine version bump:

   | Change Type | Version Bump | Examples |
   |-------------|--------------|----------|
   | Breaking API changes | **MAJOR** (X.0.0) | Removed functions, changed signatures, renamed modules |
   | New features | **MINOR** (0.X.0) | New algorithms, new sources, new analysis functions |
   | Bug fixes, docs, tests | **PATCH** (0.0.X) | Fixed edge cases, improved coverage, typo fixes |

4. **Report recommendation** to user:
   ```
   ## Release Analysis

   Current version: X.Y.Z
   Recommended bump: MINOR → X.(Y+1).0

   ### Changes included:
   - feat: ...
   - fix: ...
   - docs: ...

   ### Breaking changes: None / [list them]
   ```

5. **Ask for confirmation** before proceeding.

---

## Phase 2: Prepare Documentation

1. **Update CHANGELOG.md** with new version section:
   ```markdown
   ## [X.Y.Z] - YYYY-MM-DD

   ### Added
   - New feature 1
   - New feature 2

   ### Changed
   - Changed behavior 1

   ### Fixed
   - Bug fix 1

   ### Deprecated
   - Deprecated feature 1 (if any)
   ```

2. **Validate README.md** is current:

   a. **Check feature coverage** — Ensure all major features are documented:
      - Read README.md and compare against `src/<package>/__init__.py` exports
      - New algorithms, sources, or functions should be mentioned
      - If README is missing new features, update it

   b. **Verify code examples work**:
      ```bash
      # Extract and test key examples from README
      uv run python -c "
      # Paste key examples from README here to verify they run
      from <package> import main_function
      # Quick smoke test
      "
      ```

   c. **Check installation instructions** match current setup:
      - Verify `pip install <package>` works
      - Verify optional dependencies are documented (e.g., `<package>[viz]`, `<package>[docs]`)

   d. **Verify badges** point to correct URLs:
      - PyPI version badge
      - CI status badge
      - Coverage badge (if applicable)
      - Documentation badge (if applicable)

   e. **Check version references** — Ensure no hardcoded old versions remain

3. **Check docs site** builds correctly (if using mkdocs/sphinx):
   ```bash
   uv run mkdocs build --strict
   # or: uv run sphinx-build -W docs docs/_build
   ```

4. **Review and update guide documentation**:
   - Check `docs/guide/` for completeness
   - Ensure new features are documented in relevant guides
   - Verify examples use current API patterns
   - Update algorithm recommendation tables if benchmarks changed
   - Add new transforms/sources to sources guide

5. **Verify API documentation** covers new exports:
   - Check `src/<package>/__init__.py` exports
   - Ensure all public APIs have docstrings
   - Update `docs/api/*.md` if new modules were added

---

## Phase 3: Quality Validation

1. **Run full test suite**:
   ```bash
   uv run pytest --tb=short
   ```
   - All tests must pass
   - Note coverage percentage if tracked

2. **Run type checking**:
   ```bash
   uv run pyright
   # or: uv run mypy src/
   ```
   - 0 errors required
   - Warnings acceptable

3. **Run linting and formatting**:
   ```bash
   uv run ruff format --check .
   uv run ruff check .
   ```
   - No errors allowed

4. **Run pre-commit hooks**:
   ```bash
   uv run pre-commit run --all-files
   ```
   - All hooks must pass

5. **Build package** to verify:
   ```bash
   uv build
   ls -la dist/
   ```
   - Check `dist/` contains wheel (.whl) and sdist (.tar.gz)

6. **Report quality status**:
   ```
   ## Quality Validation

   | Check | Status |
   |-------|--------|
   | Tests | ✅ XXX passed |
   | Coverage | ✅ XX% |
   | Types | ✅ 0 errors |
   | Lint | ✅ Clean |
   | Format | ✅ Clean |
   | Pre-commit | ✅ Passed |
   | Build | ✅ Success |
   ```

---

## Phase 4: Execute Release

1. **Bump version** in `pyproject.toml`:
   ```bash
   # Edit pyproject.toml to update version = "X.Y.Z"
   ```

2. **Commit version bump**:
   ```bash
   git add pyproject.toml CHANGELOG.md
   git commit -m "chore: bump version to X.Y.Z"
   git push origin main
   ```

3. **Create annotated tag**:
   ```bash
   git tag -a vX.Y.Z -m "Release vX.Y.Z

   Highlights:
   - Feature 1
   - Feature 2
   - Bug fix 1"
   ```

4. **Push tag to trigger release workflow**:
   ```bash
   git push origin vX.Y.Z
   ```

---

## Phase 5: Monitor and Verify

1. **Watch the release workflow**:
   ```bash
   gh run list --limit 5
   gh run watch  # Interactive watch
   ```

2. **If pipeline fails**:
   ```bash
   # Get failure details
   gh run view <run-id> --log-failed

   # Fix the issue, then delete and recreate tag
   git tag -d vX.Y.Z
   git push origin --delete vX.Y.Z

   # After fix, re-tag and push
   git tag -a vX.Y.Z -m "Release vX.Y.Z"
   git push origin vX.Y.Z
   ```

3. **Verify PyPI publication**:
   ```bash
   # Wait ~2 minutes after workflow completes
   pip index versions <package>
   ```

4. **Verify installation works**:
   ```bash
   # In a clean virtual environment
   pip install <package>==X.Y.Z
   python -c "import <package>; print(<package>.__version__)"
   ```

5. **Check documentation deployment** (if applicable):
   - Visit documentation site
   - Verify new features are documented
   - Check API reference is updated

6. **Build and upload research papers** (if applicable):

   Build all papers in `.project/research/computational-mechanics-review/`:
   ```bash
   # Build all three papers
   cd /workspace/.project/research/computational-mechanics-review/paper-technical && latexmk -pdf paper.tex
   cd /workspace/.project/research/computational-mechanics-review/paper-tutorial && latexmk -pdf paper.tex
   cd /workspace/.project/research/computational-mechanics-review/paper-review && latexmk -pdf paper.tex
   ```

   Copy with versioned names and upload:
   ```bash
   VERSION=X.Y.Z
   PAPERS_DIR=/workspace/.project/research/computational-mechanics-review

   # Copy PDFs with versioned names
   cp "$PAPERS_DIR/paper-technical/out/paper.pdf" "/tmp/emic-technical-report-$VERSION.pdf"
   cp "$PAPERS_DIR/paper-tutorial/paper.pdf" "/tmp/emic-tutorial-$VERSION.pdf"
   cp "$PAPERS_DIR/paper-review/paper.pdf" "/tmp/emic-review-paper-$VERSION.pdf"

   # Upload all papers to release
   gh release upload "v$VERSION" \
     "/tmp/emic-technical-report-$VERSION.pdf" \
     "/tmp/emic-tutorial-$VERSION.pdf" \
     "/tmp/emic-review-paper-$VERSION.pdf" \
     --clobber
   ```

   **Papers included**:
   | Paper | Description |
   |-------|-------------|
   | `emic-technical-report-X.Y.Z.pdf` | Complete library documentation (~50 pages) |
   | `emic-tutorial-X.Y.Z.pdf` | Computational mechanics introduction (~32 pages) |
   | `emic-review-paper-X.Y.Z.pdf` | Academic review of computational mechanics |

7. **Report final status**:
   ```
   ## Release Complete ✅

   - **Version**: X.Y.Z
   - **PyPI**: https://pypi.org/project/<package>/X.Y.Z/
   - **Docs**: https://<user>.github.io/<package>/
   - **Release**: https://github.com/<user>/<package>/releases/tag/vX.Y.Z

   ### Post-release tasks:
   - [ ] Announce on social media
   - [ ] Update roadmap
   - [ ] Close related issues/PRs
   ```

---

## Pre-Release Versions

For pre-releases, use PEP 440 suffixes:
- `.dev1` for development releases
- `a1`, `a2` for alpha releases
- `b1`, `b2` for beta releases
- `rc1`, `rc2` for release candidates

Example:
```bash
# In pyproject.toml: version = "1.1.0a1"
git tag -a v1.1.0a1 -m "Alpha: New inference algorithms"
git push origin v1.1.0a1
```

---

## Rollback Procedure

If a release has critical issues after publication:

1. **Yank the release** (hides from default install, doesn't delete):
   ```bash
   # Via PyPI web interface, or:
   pip install twine
   twine yank <package> X.Y.Z -r pypi
   ```

2. **Create hotfix**:
   ```bash
   git checkout -b hotfix/X.Y.(Z+1)
   # Fix the issue
   git commit -m "fix: critical issue in X.Y.Z"
   git checkout main
   git merge hotfix/X.Y.(Z+1)
   git push origin main
   ```

3. **Release patch version** following the same ceremony.

---

## Automation Notes

This prompt works with GitHub Actions workflows:
- `.github/workflows/ci.yml` - Runs tests on every push
- `.github/workflows/release.yml` - Publishes to PyPI on tag push
- `.github/workflows/docs.yml` - Deploys docs on main push (if applicable)

The release workflow typically uses PyPI trusted publishing (no tokens needed).

Example release workflow structure:
```yaml
on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    runs-on: ubuntu-latest
    permissions:
      id-token: write  # For trusted publishing
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v4
      - run: uv build
      - uses: pypa/gh-action-pypi-publish@release/v1
```

---

## Checklist Summary

**Before tagging:**
- [ ] All tests pass
- [ ] Type checking passes (0 errors)
- [ ] Linting/formatting clean
- [ ] Pre-commit hooks pass
- [ ] Package builds successfully
- [ ] Docs build (if applicable)
- [ ] CHANGELOG.md updated
- [ ] README.md is current
- [ ] Version bumped in pyproject.toml
- [ ] Changes committed and pushed

**After tagging:**
- [ ] CI/CD pipeline succeeds
- [ ] Package appears on PyPI
- [ ] Installation works (`pip install <package>==X.Y.Z`)
- [ ] Import works (`python -c "import <package>"`)
- [ ] Docs are updated (if applicable)
- [ ] GitHub Release created
