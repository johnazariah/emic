# Quantum Research Session Handoff

*Use this prompt to continue the quantum research work in a new session.*

---

## Context Prompt

```
I'm continuing work on the emic quantum research branch. Here's where we are:

## Project State

- **Branch**: `quantum-research` (15 commits ahead of main)
- **Last commit**: `50602b4` - spec(021): quantum computing deep dive
- **All tests passing**: 421 tests

## What We Built This Session

1. **Fixed `excess_entropy()`** - Was returning C_μ incorrectly. Now uses block entropy convergence.

2. **Quantum complexity module** (`src/emic/analysis/quantum.py`):
   - `quantum_signal_states()` - Construct |s_j⟩ for each causal state
   - `quantum_density_matrix()` - Compute ρ = Σ π_j |s_j⟩⟨s_j|
   - `quantum_complexity()` - Von Neumann entropy S(ρ)
   - `decoherence_trajectory()` - Track C_q(γ) under dephasing

3. **Perturbed Coin source** (`src/emic/sources/synthetic/perturbed_coin.py`) - Canonical quantum advantage example

4. **Decoherence trajectory investigation** (`notebooks/decoherence_trajectory.ipynb`):
   - All trajectories are **concave** for processes with quantum advantage
   - Signal state overlap predicts quantum advantage
   - **Key finding**: Even Process anomaly - dephasing can exceed C_μ for orthogonal signal states

5. **QC Primer updates** - Added "Critical Intuition" section explaining:
   - Diagonal matrix = classical probability
   - Off-diagonal = quantum coherence
   - This is THE key insight for understanding quantum advantage

6. **New spec 021**: Quantum Computing Deep Dive - intuition-first QC introduction

## Key Files

- `.project/specifications/020-quantum-research-program.md` - Research plan
- `.project/specifications/021-quantum-computing-deep-dive.md` - QC intro spec
- `.project/research/quantum-emergence/qc-primer.md` - Updated primer
- `.project/research/quantum-deep-dive/00-overview.md` - Deep dive roadmap
- `notebooks/quantum_validation.ipynb` - Validates C_q implementation
- `notebooks/decoherence_trajectory.ipynb` - Investigation 1 results

## Next Steps (pick one)

1. **Write quantum deep dive chapters** - Start with Chapter 1 (Classical Uncertainty)
2. **Add unit tests for quantum measures** - Test against analytic formulas
3. **Investigate concavity mathematically** - Can we prove C_q''(γ) < 0?
4. **Alternative decoherence channels** - Try depolarizing, amplitude damping
5. **Continue research program** - Investigation 2 or 3 from spec 020

## Critical Intuition to Remember

The whole quantum advantage story:
- Classical ε-machines store states in orthogonal "slots" (diagonal matrix)
- Quantum q-machines can overlap states (off-diagonal coherences)
- Overlap = compression = C_q < C_μ
- Decoherence kills off-diagonals, destroying the advantage

Ask me what I'd like to work on next.
```

---

## Quick Commands

```bash
# Check status
cd /workspace/worktrees/quantum-research && git status && git log --oneline -5

# Run tests
uv run pytest tests/ -x -q

# Run quantum validation notebook
# Open notebooks/quantum_validation.ipynb

# Check recent notes
ls -la .project/notes/ | tail -5
```

## Session Notes Location

- `.project/notes/2026-01-29T01-01-decoherence-trajectory-investigation.md`
- `.project/record/JOURNAL.md` (updated with session summary)
