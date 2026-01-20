# Update Public-Facing Documentation

Systematically review and update all documentation to ensure it accurately reflects the current state of the codebase.

**Goal**: Every public API, feature, and capability should be documented in:
1. Docstrings (source of truth)
2. User guides (how to use it)
3. API reference (complete reference)
4. README (high-level overview)

---

## Phase 1: Discover Public API

Build a complete picture of what needs to be documented.

1. **Find all public exports**:
   ```bash
   # Main package exports
   grep -E "^from|^__all__" src/emic/__init__.py

   # Each submodule's exports
   for module in src/emic/*/; do
       echo "=== $module ==="
       grep -E "^from|^__all__" "${module}__init__.py" 2>/dev/null || echo "(no __init__.py)"
   done
   ```

2. **Find all public classes and functions**:
   ```bash
   # Classes (excluding private _Foo)
   grep -rE "^class [A-Z]" src/emic/ --include="*.py" | grep -v "^class _"

   # Public functions (excluding private _foo)
   grep -rE "^def [a-z]" src/emic/ --include="*.py" | grep -v "^def _"
   ```

3. **Create inventory** — list every public item that needs documentation:
   - Classes (algorithms, configs, data types)
   - Functions (analysis, utilities)
   - Protocols (interfaces for extension)

---

## Phase 2: Audit Docstrings

Docstrings are the source of truth. They must be **complete** AND **accurate**.

### 2.1 Check docstrings exist

```bash
uv run python scripts/check_docstrings.py 2>&1 || echo "Script not found, manual check needed"
```

### 2.2 Verify docstrings match implementation

For each public class/function, verify the docstring is **accurate**:

1. **Read the implementation** alongside the docstring
2. **Check parameter documentation matches actual parameters**:
   ```bash
   # For a class, compare __init__ signature to docstring Args/Attributes
   # Example check for a specific file:
   grep -A 30 "class SomeClass" src/emic/module/file.py
   ```

3. **Verify described behavior matches actual behavior**:
   - Run the docstring examples to confirm they work
   - Check edge cases mentioned are actually handled
   - Confirm return types match what's documented

4. **Check for stale documentation**:
   - Parameters that were renamed or removed
   - Default values that changed
   - Behavior that was modified
   - New parameters not yet documented

### 2.3 Validate docstring examples execute

For each docstring with an `Example` or `Examples` section:

```bash
# Use doctest to verify examples in docstrings
uv run python -m doctest src/emic/module/file.py -v 2>&1 | head -50

# Or run pytest with doctest
uv run pytest --doctest-modules src/emic/ -v 2>&1 | head -100
```

Fix any examples that fail.

### 2.4 Cross-reference with type hints

Docstrings should agree with type annotations:

```bash
# Run pyright to ensure types are valid
uv run pyright src/emic/

# Manually verify: if a function has `def foo(x: int) -> str:`,
# the docstring should document x as int and return as str
```

### 2.5 Docstring completeness checklist

For each public symbol, verify:

| Check | Class | Function | Protocol |
|-------|-------|----------|----------|
| One-line summary | ✓ | ✓ | ✓ |
| Extended description (if complex) | ✓ | ✓ | ✓ |
| All parameters documented | ✓ | ✓ | - |
| Parameter types match signature | ✓ | ✓ | - |
| Default values documented | ✓ | ✓ | - |
| Return type documented | - | ✓ | - |
| Raises section (if applicable) | ✓ | ✓ | - |
| Example that executes | ✓ | ✓ | ✓ |
| Attributes section | ✓ (dataclass) | - | - |
| Methods to implement | - | - | ✓ |

### 2.6 Fix inaccurate docstrings

When fixing a docstring:

1. Read the full implementation to understand actual behavior
2. Update the description to match what the code does
3. Ensure all parameters are listed with correct types and defaults
4. Add/update examples that demonstrate real usage
5. Run the example to verify it works

---

## Phase 3: Audit User Guides

User guides explain *how* and *when* to use features.

### 3.1 List all guide pages

```bash
find docs/guide -name "*.md" -exec echo "=== {} ===" \; -exec head -20 {} \;
```

### 3.2 For each guide, verify coverage

For each guide page, compare against the corresponding module:

| Guide | Module | Check |
|-------|--------|-------|
| `docs/guide/inference.md` | `src/emic/inference/` | All algorithms documented? |
| `docs/guide/sources.md` | `src/emic/sources/` | All sources documented? |
| `docs/guide/analysis.md` | `src/emic/analysis/` | All measures documented? |
| `docs/guide/pipelines.md` | `src/emic/pipeline.py` | Pipeline usage explained? |

### 3.3 Update each guide

For each undocumented feature, add:

1. **Section header** with the feature name
2. **Brief explanation** of what it does and when to use it
3. **Code example** showing basic usage
4. **Configuration options** (if applicable)
5. **Comparison** to alternatives (if applicable)

### 3.4 Verify code examples work

```bash
# Extract and test Python code blocks from guides
for guide in docs/guide/*.md; do
    echo "=== Testing $guide ==="
    # Manual: copy code examples and run them
done
```

---

## Phase 4: Audit API Reference

API reference should expose all public symbols via mkdocstrings.

### 4.1 List current API pages

```bash
find docs/api -name "*.md" -exec echo "=== {} ===" \; -exec cat {} \;
```

### 4.2 Compare exports to documented members

For each API page, check that the `members` list matches `__all__`:

```bash
# Example: check inference
echo "=== Exports ==="
grep -A 50 "^__all__" src/emic/inference/__init__.py | head -30

echo "=== Documented ==="
grep -A 20 "members:" docs/api/inference.md
```

### 4.3 Update API pages

Ensure each API page includes all public symbols:

```markdown
::: emic.modulename
    options:
      members:
        - Symbol1
        - Symbol2
        # ... all from __all__
```

---

## Phase 5: Audit README

README is the first thing users see — keep it current but concise.

1. **Read current README**:
   ```bash
   cat README.md
   ```

2. **Verify sections**:
   - [ ] **Features list** — mentions all major capabilities
   - [ ] **Installation** — correct commands
   - [ ] **Quick start** — working example
   - [ ] **Supported X** tables — complete and accurate
   - [ ] **Links** — point to correct documentation URLs

3. **Test quick start example**:
   ```bash
   # Copy the quick start code from README and run it
   uv run python -c "
   # <paste quick start code here>
   "
   ```

4. **Update if needed** — README should be high-level; details go in guides.

---

## Phase 6: Audit Getting Started

Getting started is the first tutorial users follow.

1. **Read current content**:
   ```bash
   cat docs/getting-started.md
   ```

2. **Verify**:
   - [ ] Installation instructions match pyproject.toml
   - [ ] First example is simple and works
   - [ ] Progressively introduces concepts
   - [ ] Links to deeper guides

3. **Test all code examples** in the getting started guide.

---

## Phase 7: Build and Validate

1. **Build docs with strict mode**:
   ```bash
   uv run mkdocs build --strict 2>&1
   ```

2. **Fix any warnings or errors**:
   - Missing references
   - Broken links
   - Undefined symbols

3. **Serve locally and spot-check**:
   ```bash
   uv run mkdocs serve &
   sleep 3
   echo "Docs available at http://127.0.0.1:8000"
   ```

   Manually verify:
   - Navigation works
   - Code blocks render correctly
   - API docs show full signatures

---

## Phase 8: Final Verification

Run all quality checks:

```bash
# Type checking
uv run pyright src/

# Tests pass
uv run pytest -x -q

# Docs build clean
uv run mkdocs build --strict

# Linting
uv run ruff check src/ docs/
```

---

## Output: Summary Report

After completing all phases, provide a summary:

```markdown
## Documentation Update Summary

### Docstrings
- Fixed: X classes/functions
- Status: ✅ Complete / ⚠️ Issues remain

### User Guides
- Updated: [list of files]
- Added sections for: [list of features]
- Status: ✅ Complete / ⚠️ Issues remain

### API Reference
- Updated: [list of files]
- Added members: [list of symbols]
- Status: ✅ Complete / ⚠️ Issues remain

### README
- Changes: [summary]
- Status: ✅ Current / ⚠️ Needs update

### Validation
- [ ] mkdocs build --strict passes
- [ ] All code examples tested
- [ ] pyright passes
- [ ] pytest passes

### Remaining Issues
- [any issues that need follow-up]
```

---

## Completion Checklist

- [ ] All public symbols have docstrings
- [ ] All features documented in user guides
- [ ] All public symbols in API reference
- [ ] README reflects current capabilities
- [ ] Getting started works for new users
- [ ] mkdocs builds without warnings
- [ ] All code examples execute successfully
