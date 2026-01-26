# H002: High noise causes under-splitting (state collapse)

## Status: Untested

## Statement

At high noise levels (ε > 0.2), CSSR will infer FEWER states than the true process, because noise washes out the structure and makes all histories look similar.

## Prediction

For Golden Mean process (2 true states):
- ε = 0.20: 2 states (still correct, or slight under)
- ε = 0.30: 1-2 states (structure degraded)
- ε = 0.40: 1 state (looks like IID)
- ε = 0.50: 1 state (definitely IID)

## Rationale

At ε = 0.5, the output is completely random regardless of input, so the "noisy Golden Mean" is indistinguishable from a biased coin.

The transition should be smooth: as ε increases, the conditional distributions P(future|past) become more uniform, so more histories get merged.

## Test Protocol

**Experiment**: `noise_robustness/bitflip_states`

**Parameters**:
- Process: GoldenMeanSource(p=0.5)
- Sample size: n = 10,000
- Noise levels: ε ∈ [0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5]
- Repetitions: 50 per condition

**Success metric**: mean(inferred_states) < 1.5 at ε = 0.4

## Result

*To be filled after experiment*

## Combined with H001

Together, H001 and H002 predict a **non-monotonic** relationship:
- ε small → over-splitting (more states)
- ε medium → approximately correct
- ε large → under-splitting (fewer states)

## Related

- Question: Q001
- Complementary hypothesis: H001
