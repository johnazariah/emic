# Experiment: Convergence Analysis

## ID: EXP-001

## Question

How do inferred state count and complexity measures converge to true values as sample size increases?

## Status: Subsumed by Benchmarks

**Note**: This experiment is now covered by `experiments/benchmarks/`, which sweeps
sample sizes from 100 to 1,000,000 across all algorithms and processes.

Key findings from benchmarks:
- **Spectral** achieves 100% correctness at N ≥ 10,000
- **CSSR** achieves 95% at N = 1,000 but degrades for Even Process at high N
- **NSD** stable at 75% across all sample sizes
- **CSM** improves from 15% at N=100 to 50% at N ≥ 10,000
- **BSI** stable at 25% regardless of sample size

See `benchmarks/results/` and the technical report for detailed analysis.

## Original Design

### Processes

| Process | True States | True Cμ | True hμ |
|---------|-------------|---------|---------|
| BiasedCoin(0.5) | 1 | 0.000 | 1.000 |
| GoldenMean(0.5) | 2 | 0.918 | 0.667 |
| EvenProcess(0.5) | 2 | 0.918 | 0.667 |
| Periodic(5) | 5 | 2.322 | 0.000 |

### Parameters

- **Sample sizes**: 100, 500, 1000, 5000, 10000, 50000
- **Repetitions**: 50 per condition
- **Algorithm**: CSSR(max_history=5, significance=0.001)

### Metrics

- Mean inferred states ± std
- Mean Cμ ± std
- Mean hμ ± std
- Probability of correct state count

## Results

*Experiment not yet run*

## Conclusions

*To be written after analysis*
