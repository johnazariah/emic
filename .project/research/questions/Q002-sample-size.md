# Q002: Sample size requirements for reliable inference

## Status: Active

## Context

Epsilon-machine inference requires sufficient data to:
- Observe all states
- Estimate transition probabilities accurately
- Distinguish genuine states from finite-sample artifacts

## Sub-questions

- **Q002a**: How does state count converge with sample size?
- **Q002b**: What sample size gives 95% probability of correct inference?
- **Q002c**: How do Cμ and hμ estimates converge?
- **Q002d**: Is there systematic bias at finite samples?
- **Q002e**: How does required sample size scale with process complexity?

## Key Factors

1. **True number of states** — More states need more data
2. **Transition probabilities** — Rare transitions need more samples
3. **Algorithm parameters** — significance, max_history
4. **Entropy rate** — Higher entropy = faster mixing

## Related

- **Experiments**: `convergence`
- **Hypotheses**: H004, H005
- **Papers**: emic-framework (Section 4)
