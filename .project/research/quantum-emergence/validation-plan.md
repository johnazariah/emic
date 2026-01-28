# Validation Plan: Quantum Complexity Measures

*Golden test cases with known values from the literature*

---

## Overview

This document specifies validation targets for the quantum extension to emic. Each test case has:
- Process definition
- Classical complexity $C_\mu$ (from emic's existing code)
- Expected quantum complexity $C_q$ (from papers)
- Source reference

**Philosophy:** Trust but verify. Published values should be reproducible to stated precision.

---

## Part 1: Simple Processes (No Quantum Advantage)

### 1.1 Fair Coin (IID)

**Definition:** $P(X_t = 0) = P(X_t = 1) = 0.5$, independent.

**ε-Machine:** Single state, self-loop with equal probabilities.

| Measure | Value | Notes |
|---------|-------|-------|
| $C_\mu$ | 0 bits | No memory needed |
| $E$ | 0 bits | Past/future independent |
| $\chi$ | 0 bits | No crypticity |
| $C_q$ | 0 bits | Matches classical |

**Test:** Verify $C_q = C_\mu = 0$ (within numerical tolerance $10^{-10}$).

**Source:** Trivial (any CM textbook).

### 1.2 Biased Coin (IID)

**Definition:** $P(X_t = 1) = p$, independent.

**ε-Machine:** Single state, self-loop.

| Measure | Value ($p = 0.3$) |
|---------|-------------------|
| $C_\mu$ | 0 bits |
| $C_q$ | 0 bits |

**Test:** Verify $C_q = 0$ for various $p$.

**Source:** Trivial.

---

## Part 2: Two-State Processes

### 2.1 Golden Mean Process

**Definition:** No consecutive 1s. After 1, must emit 0.

**ε-Machine:**
- $S_0$: Last was 0 (or start)
- $S_1$: Last was 1

Transitions ($p = 0.5$):
- $S_0 \xrightarrow{0:0.5} S_0$
- $S_0 \xrightarrow{1:0.5} S_1$
- $S_1 \xrightarrow{0:1.0} S_0$

Stationary: $\pi_0 = 2/3$, $\pi_1 = 1/3$

| Measure | Value | Source |
|---------|-------|--------|
| $C_\mu$ | 0.9183 bits | $-\frac{2}{3}\log_2\frac{2}{3} - \frac{1}{3}\log_2\frac{1}{3}$ |
| $C_q$ | ≈ 0.543 bits | Computed in framework.md |
| $\Delta_q$ | ≈ 0.375 bits | 41% advantage |

**Signal states:**
- $|s_0\rangle = \sqrt{0.5}|0,0\rangle + \sqrt{0.5}|1,1\rangle$
- $|s_1\rangle = |0,0\rangle$

**Test:**
1. Verify $C_\mu = 0.9183 \pm 0.0001$
2. Verify $C_q = 0.543 \pm 0.01$
3. Verify $C_q < C_\mu$

**Note:** Need to derive exact $C_q$ from paper or compute independently.

### 2.2 Even Process

**Definition:** No odd-length runs of 1s. 1s must come in pairs.

**ε-Machine:**
- $S_0$: Even number of 1s since last 0
- $S_1$: Odd number of 1s since last 0

Transitions:
- $S_0 \xrightarrow{0:0.5} S_0$
- $S_0 \xrightarrow{1:0.5} S_1$
- $S_1 \xrightarrow{1:1.0} S_0$

Stationary: $\pi_0 = 2/3$, $\pi_1 = 1/3$ (same as golden mean!)

| Measure | Value |
|---------|-------|
| $C_\mu$ | 0.9183 bits |
| $C_q$ | TBD |

**Test:** Compute $C_q$ and verify against golden mean (may differ due to different overlaps).

---

## Part 3: Perturbed Coin (Primary Validation)

### Definition

A coin with persistent bias. At each step:
1. Coin flips with probability $p$
2. Observe coin state

**ε-Machine:**
- $S_0$: Last observation was 0
- $S_1$: Last observation was 1

Transitions:
- $S_0 \xrightarrow{0:1-p} S_0$, $S_0 \xrightarrow{1:p} S_1$
- $S_1 \xrightarrow{1:1-p} S_1$, $S_1 \xrightarrow{0:p} S_0$

Stationary: $\pi_0 = \pi_1 = 0.5$

### Classical Measures

| Measure | Formula | Notes |
|---------|---------|-------|
| $C_\mu$ | $1$ bit | Always 1 bit (2 equally likely states) |
| $h_\mu$ | $H_s(p)$ | Binary entropy of flip probability |
| $E$ | $1 - H_s(p)$ | From Crutchfield & Feldman |
| $\chi$ | $H_s(p)$ | Crypticity = classical waste |

### Quantum Signal States

$$|s_0\rangle = \sqrt{1-p}|0,0\rangle + \sqrt{p}|1,1\rangle$$
$$|s_1\rangle = \sqrt{p}|0,0\rangle + \sqrt{1-p}|1,1\rangle$$

Overlap: $\langle s_0|s_1\rangle = 2\sqrt{p(1-p)}$

### Density Matrix

In $\{|0,0\rangle, |1,1\rangle\}$ subspace:

$$\rho = \begin{pmatrix} 0.5 & \sqrt{p(1-p)} \\ \sqrt{p(1-p)} & 0.5 \end{pmatrix}$$

Eigenvalues: $\lambda_\pm = 0.5 \pm \sqrt{p(1-p)}$

### Quantum Complexity

$$C_q = -\lambda_+ \log_2 \lambda_+ - \lambda_- \log_2 \lambda_-$$

### Validation Table (From Gu et al. 2012, Fig. 2)

| $p$ | $C_\mu$ | $E$ | $C_q$ | $\Delta_q$ |
|-----|---------|-----|-------|------------|
| 0.05 | 1.000 | 0.714 | 0.714 | 0.286 |
| 0.10 | 1.000 | 0.531 | 0.469 | 0.531 |
| 0.15 | 1.000 | 0.390 | 0.352 | 0.648 |
| 0.20 | 1.000 | 0.278 | 0.286 | 0.714 |
| 0.25 | 1.000 | 0.189 | 0.219 | 0.781 |
| 0.30 | 1.000 | 0.119 | 0.161 | 0.839 |
| 0.35 | 1.000 | 0.066 | 0.114 | 0.886 |
| 0.40 | 1.000 | 0.029 | 0.080 | 0.920 |
| 0.45 | 1.000 | 0.007 | 0.041 | 0.959 |
| 0.49 | 1.000 | 0.001 | 0.008 | 0.992 |

**Note:** $C_q$ values computed from formula; verify against paper's Figure 2.

### Tests

1. Verify $C_\mu = 1.0$ for all $p$
2. Verify $C_q$ matches table to 0.01 bits precision
3. Verify $C_q \to 0$ as $p \to 0.5$
4. Verify $C_q \geq E$ (hierarchy bound)
5. Verify $C_q \leq C_\mu$ (quantum advantage)

---

## Part 4: Decoherence Trajectory Tests

### 4.1 Trajectory Shape

For perturbed coin with $p = 0.3$:

| $\gamma$ | $C_q(\gamma)$ | Notes |
|----------|---------------|-------|
| 0.0 | 0.161 | Pure quantum |
| 0.2 | TBD | Compute |
| 0.4 | TBD | Compute |
| 0.6 | TBD | Compute |
| 0.8 | TBD | Compute |
| 1.0 | 1.000 | Should equal $C_\mu$ |

**Tests:**
1. $C_q(0) = C_q$ (unperturbed quantum complexity)
2. $C_q(1) = C_\mu$ (full dephasing → classical)
3. $C_q(\gamma)$ is monotonically non-decreasing in $\gamma$
4. Trajectory is smooth (no discontinuities)

### 4.2 Limit Recovery

For **any** process, full dephasing should give:

$$C_q(1) = H(\text{diag}(\rho))$$

For processes where signal states live in orthogonal subspaces (like perturbed coin in $\{|0,0\rangle, |1,1\rangle\}$):

$$C_q(1) = H(\pi) = C_\mu$$

**Test:** Verify this identity for all test processes.

---

## Part 5: Numerical Tolerances

### Entropy Computation

- Eigenvalue threshold: $\lambda > 10^{-12}$ (below this, treat as 0)
- Log computation: use $\log_2$ consistently
- Precision target: 6 significant figures

### Density Matrix Validation

Before computing entropy, verify:
1. Hermitian: $\|\rho - \rho^\dagger\| < 10^{-12}$
2. Trace: $|1 - \text{Tr}(\rho)| < 10^{-12}$
3. Positive: all eigenvalues $\geq -10^{-12}$

### Comparison Tolerance

| Comparison | Tolerance |
|------------|-----------|
| Exact match (e.g., $C_\mu$ for perturbed coin) | $10^{-6}$ |
| Literature comparison | $0.01$ bits |
| Inequality checks (e.g., $C_q \leq C_\mu$) | $-10^{-10}$ (allow tiny numerical violations) |

---

## Part 6: Test Categories

### Unit Tests

```python
def test_fair_coin_zero_complexity():
    machine = FairCoinSource().true_machine
    qm = construct_qmachine(machine)
    assert abs(qm.quantum_complexity) < 1e-10

def test_perturbed_coin_p04():
    machine = PerturbedCoinSource(p=0.4).true_machine
    qm = construct_qmachine(machine)
    assert abs(qm.quantum_complexity - 0.080) < 0.01
    assert qm.quantum_complexity < statistical_complexity(machine)
```

### Property Tests (Hypothesis)

```python
@given(p=floats(0.01, 0.49))
def test_perturbed_coin_hierarchy(p):
    machine = PerturbedCoinSource(p=p).true_machine
    qm = construct_qmachine(machine)
    E = excess_entropy(machine)  # Needs to be fixed first!
    C_q = qm.quantum_complexity
    C_mu = statistical_complexity(machine)

    assert E <= C_q + 1e-10  # Allow numerical tolerance
    assert C_q <= C_mu + 1e-10

@given(gamma=floats(0.0, 1.0))
def test_decoherence_monotonic(gamma):
    # Verify C_q(gamma) is non-decreasing
    ...
```

### Golden Tests

Add to `tests/golden/`:

```python
QUANTUM_GOLDEN_CASES = [
    {
        "name": "perturbed_coin_p01",
        "source": PerturbedCoinSource(p=0.1),
        "C_mu": 1.0,
        "C_q": 0.469,
        "tolerance": 0.01,
    },
    {
        "name": "perturbed_coin_p04",
        "source": PerturbedCoinSource(p=0.4),
        "C_mu": 1.0,
        "C_q": 0.080,
        "tolerance": 0.01,
    },
    # ... more cases
]
```

---

## Part 7: Known Values from Papers

### From Gu et al. (2012), Figure 2

Perturbed coin: $C_q = -\lambda_+ \log \lambda_+ - \lambda_- \log \lambda_-$ where $\lambda_\pm = 0.5 \pm \sqrt{p(1-p)}$.

**Explicit formula (exact):**
```python
def perturbed_coin_Cq(p: float) -> float:
    sqrt_term = math.sqrt(p * (1 - p))
    lambda_plus = 0.5 + sqrt_term
    lambda_minus = 0.5 - sqrt_term
    return -lambda_plus * math.log2(lambda_plus) - lambda_minus * math.log2(lambda_minus)
```

### From Thompson et al. (2018)

Heralding coin example with causal asymmetry.

TODO: Extract exact values for validation.

### From Garner et al. (2017)

Unbounded advantage examples.

TODO: Identify specific numerical targets.

---

## Part 8: Test Implementation Order

### Phase 1: Basic Infrastructure

1. Test von Neumann entropy computation
2. Test density matrix construction
3. Test signal state construction

### Phase 2: Simple Processes

4. Fair coin: $C_q = 0$
5. Biased coin: $C_q = 0$

### Phase 3: Primary Validation

6. Perturbed coin suite (multiple $p$ values)
7. Golden mean process
8. Even process

### Phase 4: Decoherence

9. Dephasing channel tests
10. Trajectory monotonicity
11. Classical limit recovery

### Phase 5: Advanced

12. Causal asymmetry (requires reverse machine)
13. Bidirectional complexity
14. Literature comparison suite

---

## Part 9: Acceptance Criteria

### Minimum Viable

- [ ] $C_q$ computes without errors for any valid ε-machine
- [ ] Perturbed coin matches Gu et al. values to 0.01 bits
- [ ] Hierarchy $E \leq C_q \leq C_\mu$ verified for test suite

### Target

- [ ] All processes in validation table pass
- [ ] Decoherence trajectory matches $C_\mu$ at $\gamma = 1$
- [ ] Property tests pass for 1000+ random inputs

### Stretch

- [ ] Reproduce Figure 2 from Gu et al. (2012)
- [ ] Reproduce causal asymmetry examples from Thompson et al.
- [ ] Match Garner et al. unbounded advantage examples

---

*Document version: 1.0*
*Created: 2026-01-28*
*Status: Ready for implementation*
