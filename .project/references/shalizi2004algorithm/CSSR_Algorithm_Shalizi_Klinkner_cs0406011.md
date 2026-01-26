# Blind Construction of Optimal Nonlinear Recursive Predictors for Discrete Sequences

**Authors:** Cosma Rohilla Shalizi, Kristina Lisa Shalizi
**Affiliation:** Center for the Study of Complex Systems / Statistics Department, University of Michigan
**Source:** arXiv:cs/0406011v1 [cs.LG], UAI 2004 (pp. 504-511)
**Date:** 6 Jun 2004

---

## Abstract

We present a new method for nonlinear prediction of discrete random sequences under minimal structural assumptions. We give a mathematical construction for optimal predictors of such processes, in the form of hidden Markov models. We then describe an algorithm, CSSR (Causal-State Splitting Reconstruction), which approximates the ideal predictor from data. We discuss the reliability of CSSR, its data requirements, and its performance in simulations. Finally, we compare our approach to existing methods using variable-length Markov models and cross-validated hidden Markov models, and show theoretically and experimentally that our method delivers results superior to the former and at least comparable to the latter.

---

## 1. Introduction

The prediction of discrete sequential data is an important problem in many fields, including bioinformatics, neuroscience (spike trains), and nonlinear dynamics (symbolic dynamics). Existing prediction methods, with the exception of variable-length Markov model (VLMM) methods, make strong assumptions about the nature of the data-generating process.

This paper presents an algorithm for the blind construction of asymptotically optimal nonlinear predictors of discrete sequences. These predictors take the form of minimal sufficient statistics, naturally arranged into a hidden Markov model (HMM).

The source code and documentation for an implementation of CSSR are at http://bactra.org/CSSR/.

---

## 2. Optimal Nonlinear Predictors

Consider a sequence of random variables $X_t$ drawn from a discrete alphabet $\mathcal{A}$. A predictive statistic is a function $\eta$ on the past measurements $X_{-\infty}^t$.

**Key Definitions:**

- **Sufficient statistic**: One which maximizes mutual information $I[\eta(X_{-\infty}^t); X_{t+1}^\infty]$
- **Minimal sufficient statistic**: One which can be calculated from any other sufficient statistic
- **Causal states**: Equivalence classes where two histories $x^-$ and $y^-$ are equivalent when:
  $$P(X_{t+1}^\infty | X_{-\infty}^t = x^-) = P(X_{t+1}^\infty | X_{-\infty}^t = y^-)$$

**Properties of Causal States:**

1. $\{S_t\}$ is a Markov process
2. The causal states are recursively calculable; there is a function $T$ such that $S_{t+1} = T(S_t, X_{t+1})$
3. One can represent the observed process $X$ as a random function of the causal state process (HMM representation)
4. The causal states form a deterministic (unifilar) machine

---

## 3. Causal-State Splitting Reconstruction (CSSR)

### Algorithm Overview

CSSR estimates an HMM with causal state properties from sequence data. It starts by "assuming" the process is IID with one causal state, and adds states when statistical tests show the current set is not sufficient.

**Inputs:**
- Sequence $\bar{x}$ of length $N$ from alphabet $\mathcal{A}$ of size $k$
- Maximum history length $L_{max}$
- Significance level $\alpha$

### Three Phases

**Phase I (Initialization):**
- $L \leftarrow 0$, $\Sigma \leftarrow \{\{\emptyset\}\}$

**Phase II (Sufficiency):**
- Iteratively tests null hypothesis:
  $$P(X_t | X_{t-L}^{t-1} = ax_{t-L+1}^{t-1}) = P(X_t | \hat{S} = \hat{\varepsilon}(x_{t-L+1}^{t-1}))$$
- Uses chi-squared or Kolmogorov-Smirnov tests
- If rejected, creates new states or reassigns histories

**Phase III (Recursion):**
- Removes transient states
- Refines states until transitions are deterministic

### Time Complexity

Total time complexity: $O(k^{2L_{max}+1}) + O(N)$

- **Linear in data size $N$**
- Phase I: $O(N)$ — single pass through data to build parse tree
- Phase II: $O(k^{L_{max}})$
- Phase III: $O(k^{2L_{max}+1})$ in worst case

---

## 4. Convergence and Performance

### Assumptions for Convergence

1. The process is conditionally stationary
2. The process has only finitely many causal states
3. Every state contains at least one suffix of finite length $\Lambda$

### Convergence Result

Under these assumptions, the reconstructed causal states converge in probability:
$$P(\exists x^- : \varepsilon(x^-) \neq \hat{\varepsilon}(x^-)) \rightarrow 0$$
as $N \rightarrow \infty$.

**Key findings:**
- Probability of wrong structure goes to zero **exponentially in $N$**
- Prediction error (total variation distance) scales as $N^{-1/2}$

### Data Requirements

If the process has entropy rate $h$, a sufficient condition for convergence is:
$$L(N) \leq \frac{\log N}{h + \varepsilon}$$

Conservative estimate using alphabet size $k$:
$$L_{max} \leq \frac{\log N}{\log k}$$

---

## 5. Experimental Results

### 5.1 Test Processes

**Even Process** (Figure 2):
- 2 causal states
- State 1: Emit A (stay in 1) or B (go to 2) with probability 0.5 each
- State 2: Always emit B, go to 1
- Not equivalent to any finite-order Markov chain (strictly sofic)

**Seven-State Process** (Figure 3):
- Used in human sequence prediction studies [16]
- Each state defined by a single suffix
- All transition probabilities are multiples of 1/16

### 5.2 Results: Even Process

[Figure 4: States inferred vs $L_{max}$ and $N$ — see original PDF]

| $N$ | States Inferred | Notes |
|-----|-----------------|-------|
| $10^2$ | Variable (1-2+) | CSSR never gets states right with $\alpha = 10^{-3}$ |
| $10^3$ | ~2 (sporadic) | Sometimes correct |
| $10^4$ | 2 | Correct |
| $10^5$ | 2 | Correct |
| $10^6$ | 2 | Correct |

**Prediction Error Scaling:**
- Error measured as total-variation distance between predicted and actual distributions over length-10 words
- Error scales as $N^{-1/2}$ (confirmed in Figure 5)
- For $L_{max} < 3$, CSSR cannot find correct states
- With $\alpha = 10^{-3}$: N = 100 never works, N = 1000 sporadic

### 5.3 Comparison with Cross-Validation

**Table 1: Even Process Performance**

| $N$ | $d_{CV}$ | $d_{CSSR}$ | $\hat{s}_{CV}$ | $\hat{s}_{CSSR}$ |
|-----|----------|------------|----------------|------------------|
| $10^2$ | $1.27 \pm 0.23$ | $1.10 \pm 0.23$ | $6.6 \pm 1.5$ | $1.6 \pm 1.0$ |
| $10^3$ | $1.25 \pm 0.41$ | $0.19 \pm 0.23$ | $5.6 \pm 1.7$ | $2.2 \pm 0.1$ |
| $10^4$ | $1.15 \pm 0.02$ | $0.02 \pm 0.02$ | $2.0 \pm 0$ | $2.0 \pm 0$ |

- $d$: total-variation distance (0 ≤ d ≤ 2)
- $\hat{s}$: number of states inferred
- Minimal states needed: 2

**Table 2: Seven-State Process Performance**

| $N$ | $d_{CV}$ | $d_{CSSR}$ | $\hat{s}_{CV}$ | $\hat{s}_{CSSR}$ |
|-----|----------|------------|----------------|------------------|
| $10^2$ | $1.41 \pm 0.23$ | $0.70 \pm 0.12$ | $4.5 \pm 2.1$ | $5.1 \pm 1.5$ |
| $10^3$ | $1.40 \pm 0.17$ | $0.21 \pm 0.06$ | $5.8 \pm 2.7$ | $6.6 \pm 0.8$ |
| $10^4$ | $1.40 \pm 0.11$ | $0.06 \pm 0.01$ | $2.3 \pm 0.7$ | $7.2 \pm 0.6$ |

**Key Observations:**
- CSSR achieves much lower prediction error than cross-validated HMMs
- CSSR finds correct state count at $N = 10^4$
- Cross-validation tends to over-fit at small $N$ and under-fit at large $N$

### 5.4 Comparison with Variable-Length Markov Models

**Key advantage of CSSR over VLMMs:**
- Each VLMM state = single suffix
- Each causal state can contain **multiple suffixes**
- For Even Process: causal states contain infinitely many suffixes
- VLMMs cannot capture strictly sofic processes
- VLMMs produce unbounded state growth on Even Process as $L_{max}$ increases

---

## 6. Conclusion

**Key Contributions:**
1. CSSR constructs optimal nonlinear predictors from sequence data
2. Time complexity linear in data size $N$
3. Reliably infers processes with finitely many causal states
4. Predictive performance comparable to or better than cross-validated EM
5. Handles strictly sofic processes that VLMMs cannot represent

**Future Directions:**
1. Initialize with prior knowledge about system dynamics
2. Extend to POMDPs (controlled dynamical systems)

---

## Key Performance Figures Summary

| Metric | Value | Condition |
|--------|-------|-----------|
| Convergence rate | Exponential in $N$ | For correct structure |
| Prediction error scaling | $O(N^{-1/2})$ | Total variation distance |
| Minimum $N$ for Even Process | ~$10^3$ sporadic, $10^4$ reliable | With $\alpha = 10^{-3}$, $L_{max} \geq 3$ |
| Data requirement | $L_{max} \leq \log N / \log k$ | Conservative bound |
| Time complexity | $O(N) + O(k^{2L_{max}+1})$ | Linear in data |

---

## References

[1] C. R. Shalizi. *Causal Architecture, Complexity and Self-Organization in Time Series and Cellular Automata*. PhD thesis, University of Wisconsin-Madison, 2001.

[2] C. R. Shalizi, K. L. Shalizi, and J. P. Crutchfield. "An algorithm for pattern discovery in time series." Technical Report 02-10-060, Santa Fe Institute, 2002. arxiv.org/abs/cs.LG/0210025.

[5] J. P. Crutchfield and K. Young. "Inferring statistical complexity." *Physical Review Letters*, 63:105–108, 1989.

[6] C. R. Shalizi and J. P. Crutchfield. "Computational mechanics: Pattern and prediction, structure and simplicity." *Journal of Statistical Physics*, 104:817–879, 2001.

[16] J. Feldman and J. F. Hanna. "The structure of responses to a sequence of binary events." *Journal of Mathematical Psychology*, 3:371–387, 1966.
