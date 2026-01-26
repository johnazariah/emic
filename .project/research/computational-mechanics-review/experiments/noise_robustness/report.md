# Experiment: Noise Robustness Analysis

## ID: EXP-002

## Question

How do epsilon-machine inference algorithms behave under observation noise?

## Status: Planned (Not Yet Implemented)

**Dependencies**: Requires implementing a `BitFlipNoise` source transform in `emic.sources.transforms`.

## Design

### Noise Models

1. **Bit-flip (BSC)**: Each symbol flipped with probability ε
2. **State-dependent**: Noise rate varies by hidden state

### Sweep Parameters

- **Noise levels**: ε ∈ [0, 0.01, 0.02, 0.05, 0.1, 0.15, 0.2, 0.3, 0.4, 0.5]
- **Sample size**: 10,000 (fixed)
- **Repetitions**: 50 per condition
- **Process**: GoldenMean(p=0.5)

### Algorithms

- CSSR(max_history=5, significance=0.001)
- CSM(max_history=5, significance=0.001)
- BSI(max_states=5, n_samples=100)
- Spectral(max_history=5)

### Metrics

- Mean inferred states vs noise level
- Cμ bias (inferred - true) vs noise level
- Critical noise threshold (εc) per algorithm

## Hypotheses Under Test

- **H001**: Low noise causes over-splitting
- **H002**: High noise causes state collapse

## Results

*Experiment not yet run*

## Conclusions

*To be written after analysis*
