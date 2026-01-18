# Prepare and Execute a Release

Analyze changes since the last release, prepare documentation, validate quality, and execute the release ceremony.

## Phase 1: Analyze Release Scope

1. **Get the current version** from `pyproject.toml`:
   ```bash
   grep '^version' pyproject.toml
   ```

2. **List changes since last release**:
   ```bash
   git log $(git describe --tags --abbrev=0)..HEAD --oneline
   ```

3. **Categorize changes** and determine version bump:

   | Change Type | Version Bump | Examples |
   |-------------|--------------|----------|
   | Breaking API changes | **MAJOR** (X.0.0) | Removed functions, changed signatures |
   | New features, new algorithms | **MINOR** (0.X.0) | New inference algorithms, new sources |
   | Bug fixes, docs, tests | **PATCH** (0.0.X) | Fixed edge cases, improved coverage |

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

2. **Verify README.md** is current:
   - Installation instructions correct
   - Examples work with new features
   - Badges will update automatically

3. **Check docs site** builds correctly:
   ```bash
   uv run mkdocs build --strict
   ```

4. **Verify API documentation** covers new exports:
   - Check `src/emic/__init__.py` exports
   - Check `src/emic/inference/__init__.py` exports
   - Ensure all public APIs have docstrings

---

## Phase 3: Quality Validation

1. **Run full test suite**:
   ```bash
   uv run pytest --tb=short
   ```
   - All tests must pass
   - Note coverage percentage

2. **Run type checking**:
   ```bash
   uv run pyright
   ```
   - 0 errors required
   - Warnings acceptable

3. **Run linting and formatting**:
   ```bash
   uv run ruff format . && uv run ruff check .
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
   ```
   - Check `dist/` contains wheel and sdist

6. **Report quality status**:
   ```
   ## Quality Validation

   | Check | Status |
   |-------|--------|
   | Tests | ✅ 309 passed |
   | Coverage | ✅ 92% |
   | Types | ✅ 0 errors |
   | Lint | ✅ Clean |
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
   ```

3. **Create annotated tag**:
   ```bash
   git tag -a vX.Y.Z -m "Release vX.Y.Z

   Highlights:
   - Feature 1
   - Feature 2
   - Bug fix 1"
   ```

4. **Push commit and tag**:
   ```bash
   git push origin main
   git push origin vX.Y.Z
   ```

5. **Monitor CI/CD pipeline**:
   ```bash
   # Check GitHub Actions status
   gh run list --limit 5
   ```

---

## Phase 5: Monitor and Verify

1. **Watch the release workflow**:
   ```bash
   gh run watch
   ```

2. **If pipeline fails**:
   - Get failure details: `gh run view <run-id> --log-failed`
   - Fix the issue
   - Delete the tag: `git tag -d vX.Y.Z && git push origin :refs/tags/vX.Y.Z`
   - Re-tag and push after fix

3. **Verify PyPI publication**:
   ```bash
   # Wait ~2 minutes after workflow completes
   pip index versions emic
   ```

4. **Verify installation works**:
   ```bash
   pip install emic==X.Y.Z --upgrade
   python -c "import emic; print(emic.__version__)"
   ```

5. **Check documentation deployment**:
   - Visit https://johnazariah.github.io/emic/
   - Verify new features are documented

6. **Report final status**:
   ```
   ## Release Complete ✅

   - **Version**: X.Y.Z
   - **PyPI**: https://pypi.org/project/emic/X.Y.Z/
   - **Docs**: https://johnazariah.github.io/emic/
   - **Tag**: https://github.com/johnazariah/emic/releases/tag/vX.Y.Z

   ### Post-release tasks:
   - [ ] Announce on social media
   - [ ] Update roadmap
   - [ ] Close related issues/PRs
   ```

---

## Rollback Procedure

If a release has critical issues after publication:

1. **Yank the release** (doesn't delete, just hides from default install):
   ```bash
   # Go to PyPI project page and yank the version
   # Or use: pip install twine && twine yank emic X.Y.Z
   ```

2. **Create hotfix**:
   ```bash
   git checkout -b hotfix/X.Y.(Z+1)
   # Fix the issue
   git commit -m "fix: critical issue in X.Y.Z"
   ```

3. **Release patch version** following the same ceremony.

---

## Automation Notes

This prompt works with GitHub Actions workflows:
- `.github/workflows/ci.yml` - Runs tests on every push
- `.github/workflows/release.yml` - Publishes to PyPI on tag push
- `.github/workflows/docs.yml` - Deploys docs on main push

The release workflow uses PyPI trusted publishing (no tokens needed).

---

## Checklist Summary

Before tagging:
- [ ] CHANGELOG.md updated
- [ ] All tests pass
- [ ] Types check passes
- [ ] Lint passes
- [ ] Docs build
- [ ] Package builds
- [ ] Version bumped in pyproject.toml

After tagging:
- [ ] CI/CD pipeline succeeds
- [ ] Package appears on PyPI
- [ ] Installation works
- [ ] Docs are updated
