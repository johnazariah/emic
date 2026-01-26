# Anatomy of a Bit: Information in a Time Series Observation

**Authors:** Ryan G. James, Christopher J. Ellison, and James P. Crutchfield
**Affiliations:**
- Complexity Sciences Center, UC Davis
- Physics Department, UC Davis
- Santa Fe Institute
**Source:** arXiv:1105.2988v1 [cs.IT]; Chaos 21, 037109 (2011)
**Date:** May 16, 2011

---

## Abstract

Appealing to several multivariate information measures—some familiar, some new here—we analyze the information embedded in discrete-valued stochastic time series. We dissect the uncertainty of a single observation to demonstrate how the measures' asymptotic behavior sheds structural and semantic light on the generating process's internal information dynamics. The measures scale with the length of time window, which captures both intensive (rates of growth) and subextensive components. We provide interpretations for the components, developing explicit relationships between them. We also identify the informational component shared between the past and the future that is not contained in a single observation. The existence of this component directly motivates the notion of a process's effective (internal) states and indicates why one must build models.

---

## 1. Introduction

### The Fundamental Question

In a time series of observations, what can we learn from just a single observation?

### Two Extremes

1. **Coin flips**: A single observation tells nothing about past or future—one bit out of infinite total
2. **Periodic process** (alternating 0s and 1s): A single observation tells everything—can reconstruct entire series

Most systems fall between these extremes.

---

## 2. A Measurement: A Synopsis

### Information Storage Basics

For $k$ possible outputs:
- **Raw storage**: $\log_2 k$ bits per measurement
- **Compressed storage**: $H[X]$ bits per measurement (Shannon entropy)
- **Optimal storage**: $h_\mu$ bits per measurement (entropy rate)

### Redundancy

The difference $R_\infty = \log_2 k - h_\mu$ represents compressible information.

### Key Decomposition

[Figure 1: Dissecting information in a single measurement $X$ — see original PDF]

The information in $X$ decomposes into:
- What can be predicted from the past
- What can be retrodicted from the future
- What is genuinely random

---

## 3. Information Measures

### Shannon Entropy

For a random variable $X$ with distribution $P$:
$$H[X] = -\sum_x P(x) \log_2 P(x)$$

### Block Entropy

For length-$\ell$ words:
$$H(\ell) = -\sum_{x^\ell} P(x^\ell) \log_2 P(x^\ell)$$

### Entropy Rate

The irreducible information per symbol:
$$h_\mu = \lim_{\ell \to \infty} \frac{H(\ell)}{\ell}$$

### Mutual Information

$$I[X; Y] = H[X] + H[Y] - H[X, Y]$$

### Total Correlation (Multi-Information)

For variables $X_1, \ldots, X_n$:
$$T[X_1; \ldots; X_n] = \sum_i H[X_i] - H[X_1, \ldots, X_n]$$

Measures redundancy among all variables.

---

## 4. The Anatomy of a Bit

### Decomposing $H[X]$

The entropy of a single observation decomposes into:

$$H[X] = h_\mu + b_\mu$$

where:
- $h_\mu$: **Entropy rate** (irreducible randomness)
- $b_\mu$: **Bound information rate** (predictable structure)

### Further Decomposition of Bound Information

$$b_\mu = \rho_\mu + \sigma_\mu$$

where:
- $\rho_\mu$: **Predictive information rate** (information about future)
- $\sigma_\mu$: **Retrodictive information rate** (information about past)

### The Ephemeral Information

Some randomness in $X$ has no predictive or retrodictive value:
$$r_\mu = h_\mu - w_\mu$$

where $w_\mu$ is the **structural information rate**.

---

## 5. Information Diagram

[Figure 2: The complete anatomy of information in a measurement — see original PDF]

### Asymptotic Components

| Component | Symbol | Meaning |
|-----------|--------|---------|
| Entropy rate | $h_\mu$ | Irreducible randomness per symbol |
| Bound information rate | $b_\mu$ | Predictable structure per symbol |
| Predictive information rate | $\rho_\mu$ | Forward-useful information |
| Excess entropy | $E$ | Total predictive information (subextensive) |
| Statistical complexity | $C_\mu$ | Memory required for prediction |

### Key Relationships

$$C_\mu \geq E$$

with equality only for special processes.

---

## 6. Why Build Models?

### The Synergistic Information Problem

The paper identifies information **shared between past and future but not contained in any single observation**.

This synergistic component:
1. Cannot be extracted from individual measurements
2. Requires tracking internal states
3. Directly motivates ε-machine construction

### Effective States

The existence of synergistic information implies:
- A single observation is insufficient for optimal prediction
- Internal (hidden) states must be inferred
- Models must maintain memory of relevant history

---

## 7. Connections to Computational Mechanics

### Statistical Complexity $C_\mu$

The entropy of the causal state distribution:
$$C_\mu = H[\mathcal{S}]$$

This quantifies the memory required for optimal prediction.

### Excess Entropy $E$

The mutual information between past and future:
$$E = I[\overleftarrow{X}; \overrightarrow{X}]$$

This is the total predictive information in the process.

### Cryptic Order $\chi$

The information stored but not used for prediction:
$$\chi = C_\mu - E$$

### Bound on Complexity

$$h_\mu \leq E \leq C_\mu$$

---

## 8. Examples

### IID Process (Fair Coin)

- $H[X] = 1$ bit
- $h_\mu = 1$ bit
- $E = 0$ (no predictive information)
- $C_\mu = 0$ (no memory needed)

### Period-2 Process (Alternating)

- $H[X] = 1$ bit
- $h_\mu = 0$ (fully predictable)
- $E = 1$ bit (phase is predictive)
- $C_\mu = 1$ bit (must remember phase)

### Golden Mean Process

- Non-trivial structure
- $0 < h_\mu < H[X]$
- $C_\mu > E > 0$
- Demonstrates synergistic information

---

## Key Concepts

| Concept | Symbol | Definition |
|---------|--------|------------|
| **Entropy rate** | $h_\mu$ | Limiting entropy per symbol |
| **Bound information** | $b_\mu$ | $H[X] - h_\mu$ |
| **Excess entropy** | $E$ | $I[\overleftarrow{X}; \overrightarrow{X}]$ |
| **Statistical complexity** | $C_\mu$ | $H[\mathcal{S}]$ (causal state entropy) |
| **Cryptic order** | $\chi$ | $C_\mu - E$ |

---

## Significance

This paper:
1. **Unifies** multiple information measures in a coherent framework
2. **Motivates** ε-machine construction from first principles
3. **Distinguishes** different types of information in time series
4. **Connects** measurement-level analysis to state-level analysis

---

## References

Key citations:
1. Shannon, C. E. (1948). A mathematical theory of communication
2. Crutchfield, J. P. & Young, K. (1989). Inferring statistical complexity
3. Shalizi, C. R. & Crutchfield, J. P. (2001). Computational mechanics

---

*Extracted from: james2011anatomy.pdf*
