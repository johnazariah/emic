# Experiment: Paper Result Verification

## ID: EXP-003

## Question

Can we numerically reproduce the theoretical results from the foundational computational mechanics papers?

## Status: Planned

## Target Results

### Analytical Values

| Process | States | Cμ (bits) | hμ (bits) |
|---------|--------|-----------|-----------|
| BiasedCoin(0.5) | 1 | 0.000 | 1.000 |
| BiasedCoin(0.3) | 1 | 0.000 | 0.881 |
| GoldenMean(0.5) | 2 | 0.918 | 0.667 |
| EvenProcess(0.5) | 2 | 0.918 | 0.667 |
| Periodic(3) | 3 | 1.585 | 0.000 |
| Periodic(5) | 5 | 2.322 | 0.000 |

### Theorems to Verify

1. **E ≤ Cμ** — Excess entropy bounded by statistical complexity
2. **Entropy convergence** — H(X^L)/L → hμ as L → ∞
3. **Unifilarity** — All inferred machines are unifilar

## Design

### Analytical Comparison

For each process:
1. Compute Cμ, hμ from `true_machine`
2. Compare to analytical formulas
3. Tolerance: |computed - analytical| < 0.001

### Excess Entropy Bound

1. Estimate E from data (mutual information)
2. Compute Cμ from inferred machine
3. Verify E ≤ Cμ

### Entropy Rate Convergence

1. Compute H(X^L) for L = 1, 2, ..., 20
2. Plot H(X^L)/L vs L
3. Verify convergence to hμ

## Results

*Experiment not yet run*

## Conclusions

*To be written after analysis*
