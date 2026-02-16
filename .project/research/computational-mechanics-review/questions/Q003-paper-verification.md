# Q003: Reproducing theoretical results from the literature

## Status: Active

## Context

The foundational papers by Crutchfield and Shalizi establish theoretical results that should be verifiable with `emic`. Reproducing these validates both the theory and our implementation.

## Target Results

### From Shalizi & Crutchfield (2000)

1. **Theorem 1**: Causal states are maximally prescient
2. **Theorem 2**: Causal states have minimal statistical complexity
3. **Theorem 5**: E ≤ Cμ (excess entropy bound)
4. **Theorem 6**: Control theorem (Ashby's law)

### From Crutchfield (1994) "Calculi of Emergence"

1. **Figure 4**: Complexity-entropy diagram shape
2. **Statistical complexity formula**: Cμ = H[S] where S is causal state
3. **Known process values**: Golden Mean, Even Process, Period-k

## Sub-questions

- **Q003a**: Do computed Cμ values match analytical formulas?
- **Q003b**: Does E ≤ Cμ hold numerically for all processes?
- **Q003c**: Can we reproduce the complexity-entropy diagram?
- **Q003d**: Does entropy rate converge as predicted?

## Related

- **Experiments**: `paper_verification`
- **References**: `.project/references/`
- **Papers**: paper-framework (Section 2), derivation (planned)
