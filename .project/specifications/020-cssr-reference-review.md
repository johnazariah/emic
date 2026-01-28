# SPEC-020: CSSR Reference Implementation Review

**Status**: Draft
**Created**: 2026-01-28
**Priority**: Low (current implementation works correctly)

## Objective

Review and potentially refactor the CSSR implementation to more closely align with the reference C++ implementation (stites/CSSR), improving code clarity and maintainability.

## Background

The current CSSR implementation (`src/emic/inference/cssr/algorithm.py`) achieves 100% accuracy on benchmark processes but was developed incrementally with bug fixes. A worktree-based rewrite following the reference implementation was started but abandoned in favor of keeping the working version.

### Reference Implementation

- **Repository**: https://github.com/stites/CSSR
- **Paper**: Shalizi & Klinkner (2004) "Blind Construction of Optimal Nonlinear Recursive Predictors"
- **Language**: C++

### Reference Implementation Phases

The C++ implementation follows these explicit phases:

1. **InitialFrequencies** - Create initial state with unconditional distribution
2. **CalcNewDist** (level by level) - Compare each history to parent first, then other states
3. **DestroyShortHists** - Remove histories shorter than max_length - 1
4. **CheckConnComponents** - Remove transient (non-recurrent) states
5. **Determinize** - Split states with histories having different future transitions
6. **CheckConnComponents** - Remove transient states again
7. **StoreTransitions** - Build final state machine

## Current Implementation Status

| Aspect | Status | Notes |
|--------|--------|-------|
| Correctness | ✅ 100% | Passes all golden tests, 100% accuracy on benchmarks |
| Test Coverage | ✅ Good | Unit tests, golden tests, property tests |
| Code Clarity | ⚠️ Fair | Phases less explicit than reference |
| Documentation | ⚠️ Fair | Could better map to paper/reference |

## Proposed Changes

### Option A: Cosmetic Refactor (Recommended)

Minimal changes for clarity without risking regressions:

1. **Update docstrings** to explicitly list the 7 phases
2. **Add phase comments** in `infer()` method marking each phase
3. **Rename internal methods** to match reference naming where helpful
4. **Add algorithm walkthrough** in documentation

### Option B: Structural Refactor

More significant changes matching reference structure:

1. Replace `StatePartition` with explicit `CSSRState` dataclass
2. Restructure `infer()` to have clear phase separation
3. Match variable naming to reference implementation
4. Add intermediate state logging for debugging

## Verification Plan

Any refactoring must pass:

1. All existing unit tests (`tests/unit/test_inference_cssr.py`)
2. All golden tests (`tests/golden/test_inference_golden.py`)
3. Benchmark accuracy (100% on Golden Mean, Even, Biased Coin at N≥10K)
4. Property-based tests with Hypothesis

## References

- [CSSR Paper](https://arxiv.org/abs/cs/0406011) - Original algorithm description
- [stites/CSSR](https://github.com/stites/CSSR) - Reference C++ implementation
- [CSSR Deep Dive](../../docs/guide/cssr-deep-dive.md) - Current documentation

## Decision Log

| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-01-28 | Created spec, deferred refactoring | Current implementation works; Spectral fix was higher priority |

## Next Steps

1. Read through reference C++ implementation in detail
2. Document mapping between our methods and reference phases
3. Decide between Option A (cosmetic) or Option B (structural)
4. If Option B, create feature branch and implement incrementally
