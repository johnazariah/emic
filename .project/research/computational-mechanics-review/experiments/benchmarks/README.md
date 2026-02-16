# Regenerating Paper Benchmarks

```bash
cd .project/research/computational-mechanics-review/experiments/benchmarks
make fast   # ~5 min (skip BSI)
make        # ~30 min (full)
```

## Prompt

```
Regenerate the paper benchmarks:

cd .project/research/computational-mechanics-review/experiments/benchmarks && make fast
```

## What This Does

1. **Runs all experiments** via `emic-experiment`
2. **Generates LaTeX tables** in `paper-technical/generated/`

## Output

| File | Content |
|------|---------|
| `tab-state-counts.tex` | State counts at N=100K |
| `tab-correctness.tex` | Correctness summary |
| `tab-correctness-detail.tex` | Detailed by sample size |
| `tab-runtime.tex` | Runtime comparison |
| `macros.tex` | Key statistics |

## Algorithms

| Algorithm | Speed | Accuracy |
|-----------|-------|----------|
| Spectral | Fast | Best |
| CSSR | Fast | Good |
| CSM | Fast | OK |
| BSI | Slow | Good |
