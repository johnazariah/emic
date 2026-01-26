# Q001: How does noise affect epsilon-machine inference?

## Status: Active

## Context

Real-world data always contains measurement noise. Understanding how inference algorithms behave under noise is critical for:
- Interpreting results from empirical data
- Setting appropriate algorithm parameters
- Knowing when to trust inferred structure

## Sub-questions

- **Q001a**: At what noise level does CSSR fail to find correct state count?
- **Q001b**: Which algorithm (CSSR, CSM, BSI, Spectral) is most robust?
- **Q001c**: Does noise cause over-splitting or under-splitting?
- **Q001d**: Can we detect that a sequence is noisy?
- **Q001e**: Can we estimate the noise rate from data?

## Noise Models

1. **Bit-flip (BSC)** — Each symbol flipped with probability ε
2. **Erasure** — Symbols randomly deleted
3. **Insertion** — Random symbols inserted
4. **State-dependent** — Noise rate varies by hidden state
5. **Burst** — Noise occurs in clusters

## Related

- **Experiments**: `noise_robustness`
- **Hypotheses**: H001, H002, H003
- **Papers**: noise-robustness (planned)
- **References**: Shalizi PhD thesis, Chapter 5
