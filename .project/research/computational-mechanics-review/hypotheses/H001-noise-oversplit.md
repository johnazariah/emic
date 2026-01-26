# H001: CSSR over-splits states at low noise levels

## Status: Untested

## Statement

When bit-flip noise is added at low levels (ε < 0.1), CSSR will infer MORE states than the true process has, because noise creates spurious patterns that appear statistically significant.

## Prediction

For Golden Mean process (2 true states):
- ε = 0.00: 2 states (correct)
- ε = 0.01: 2-3 states (slight over-splitting)
- ε = 0.05: 3-5 states (moderate over-splitting)
- ε = 0.10: 4-8 states (significant over-splitting)

## Test Protocol

**Experiment**: `noise_robustness/bitflip_states`

**Parameters**:
- Process: GoldenMeanSource(p=0.5)
- Sample size: n = 10,000
- Noise levels: ε ∈ [0, 0.01, 0.02, 0.05, 0.1, 0.15, 0.2]
- Repetitions: 50 per condition
- Algorithm: CSSR(max_history=5, significance=0.001)

**Success metric**: mean(inferred_states) > 2.5 at ε = 0.05

## Result

*To be filled after experiment*

## Implications

**If supported**:
- Need noise-aware parameter tuning (higher significance threshold)
- Consider post-merge step for noisy data
- Report confidence intervals on state count

**If refuted**:
- CSSR more robust than expected
- Statistical testing effectively rejects noise patterns

## Related

- Question: Q001
- Counter-hypothesis: H002
