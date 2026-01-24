# CSSR Even Process Over-Splitting Issue

*Analysis of unexpected CSSR behavior on Even Process at large N*

**Date**: January 24, 2026
**Discovered during**: EXP-005 Algorithm Performance Benchmarks

---

## 1. Problem Statement

CSSR produces the correct 2-state machine for Even Process at small sample sizes but **over-splits to 4 states** at larger sample sizes.

### 1.1 Benchmark Results

| Sample Size | States Found | Expected | Correct? |
|-------------|--------------|----------|----------|
| 100 | 2 | 2 | ✓ |
| 1,000 | 2 | 2 | ✓ |
| 10,000 | 4 | 2 | ✗ |
| 100,000 | 4 | 2 | ✗ |
| 1,000,000 | 4 | 2 | ✗ |

### 1.2 Counter-Intuitive

More data should improve inference, not degrade it. This is a **red flag** suggesting either:
1. A bug in the implementation
2. Hyperparameter sensitivity (significance level)
3. A fundamental issue with how CSSR handles the Even Process structure

---

## 2. Even Process Structure

The Even Process has two causal states:
- **State A** (even number of 1s seen): Can emit 0 (prob p) or 1 (prob 1-p)
- **State B** (odd number of 1s seen): Must emit 0 (prob 1.0)

Ground truth ε-machine:
```
A --0,p--> A
A --1,1-p--> B
B --0,1.0--> A
```

---

## 3. Hypothesis: Significance Threshold Issue

CSSR uses statistical hypothesis testing (chi-squared or similar) to decide if two histories have distinguishable future distributions. The significance level is set to `0.001` (very stringent).

**Possible mechanism:**
1. With more data, statistical power increases
2. Tiny, statistically significant differences become detectable
3. Histories that should be merged get kept separate
4. Result: spurious state splitting

### 3.1 Test This Hypothesis

Try running with higher significance (more lenient):
```python
# Current
CSSRConfig(max_history=5, significance=0.001)

# Try
CSSRConfig(max_history=5, significance=0.01)  # 10x more lenient
CSSRConfig(max_history=5, significance=0.05)  # Standard alpha
```

---

## 4. Alternative Hypothesis: History Length

With `max_history=5`, longer histories may create spurious distinctions:
- History "01010" vs "10101" might show tiny frequency differences
- At large N, these become "significant" but not meaningful

### 4.1 Test This Hypothesis

Try shorter history:
```python
CSSRConfig(max_history=3, significance=0.001)
```

---

## 5. Comparison with Other Processes

CSSR correctly handles these at all sample sizes:
- Golden Mean (2 states): 100% correct at all N
- Biased Coin (1 state): 100% correct at all N
- Periodic (3 states): 100% correct at all N

**What's special about Even Process?**
- Has a deterministic transition (B→A with prob 1.0)
- Has asymmetric emission structure
- State B only emits 0

This asymmetry might create edge cases in the hypothesis testing.

---

## 6. Next Steps

1. **Diagnostic run**: Print CSSR's partition at each step to see where extra states come from
2. **Parameter sweep**: Test significance levels {0.001, 0.01, 0.05, 0.1}
3. **Compare with reference**: Check if original CSSR implementation has same issue
4. **Add golden test**: Mark current behavior as known-failing

---

## 7. Impact

- CSSR overall correctness: 85% (17/20)
- Without Even Process issue: would be 95% (19/20)
- This is the primary weakness in CSSR

---

## 8. References

- EXP-005 benchmark results: `/workspace/experiments/benchmarks/results/`
- CSSR algorithm: `/workspace/src/emic/inference/cssr/algorithm.py`
- Original CSSR paper: Shalizi & Klinkner (2004)
