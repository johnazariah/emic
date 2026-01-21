# Experiment: Convergence Analysis

## ID: EXP-001

## Question

How do inferred state count and complexity measures converge to true values as sample size increases?

## Status: Planned

## Design

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
