# A Spectral Algorithm for Learning Hidden Markov Models

**Authors:** Daniel Hsu, Sham M. Kakade, and Tong Zhang
**Affiliations:**
- Rutgers University
- University of Pennsylvania
**Source:** arXiv:0811.4413v6 [cs.LG]; Journal of Computer and System Sciences, 78(5):1460-1480, 2012
**Date:** July 6, 2012

---

## Abstract

Hidden Markov Models (HMMs) are one of the most fundamental and widely used statistical tools for modeling discrete time series. In general, learning HMMs from data is computationally hard (under cryptographic assumptions), and practitioners typically resort to search heuristics which suffer from the usual local optima issues. We prove that under a natural separation condition (bounds on the smallest singular value of the HMM parameters), there is an efficient and provably correct algorithm for learning HMMs. The sample complexity of the algorithm does not explicitly depend on the number of distinct (discrete) observations—it implicitly depends on this quantity through spectral properties of the underlying HMM. This makes the algorithm particularly applicable to settings with a large number of observations, such as those in natural language processing where the space of observation is sometimes the words in a language. The algorithm is also simple, employing only a singular value decomposition and matrix multiplications.

---

## 1. Introduction

### The HMM Learning Problem

Hidden Markov Models are the workhorse statistical model for discrete time series, with applications in:
- Automatic speech recognition
- Natural language processing (NLP)
- Genomic sequence modeling

The learning problem: estimate the model using only observation samples from the underlying distribution.

### Why Current Methods Fall Short

- **EM/Baum-Welch**: Local search heuristics, suffer from local optima
- **General hardness**: Learning HMMs is computationally hard under cryptographic assumptions
- **But**: Hardness results apply to pathological HMMs unlikely in practice

### This Paper's Contribution

A **spectral algorithm** that:
1. Is efficient (polynomial time)
2. Is provably correct under natural conditions
3. Uses only SVD and matrix multiplications
4. Has sample complexity independent of observation space size

---

## 2. Hidden Markov Model Definition

### Model Components

- **Hidden states**: $[m] = \{1, \ldots, m\}$
- **Observations**: $[n] = \{1, \ldots, n\}$ where $m \leq n$
- **Transition matrix**: $T \in \mathbb{R}^{m \times m}$ with $T_{ij} = \Pr[h_{t+1} = i | h_t = j]$
- **Observation matrix**: $O \in \mathbb{R}^{n \times m}$ with $O_{ij} = \Pr[x_t = i | h_t = j]$
- **Initial distribution**: $\vec{\pi} \in \mathbb{R}^m$ with $\pi_i = \Pr[h_1 = i]$

### Conditional Independence

1. Current hidden state depends only on previous hidden state
2. Current observation depends only on current hidden state

---

## 3. The Spectral Algorithm

### Key Insight

The relationship between past and future observations reveals information about hidden states through their **spectral structure**.

### Algorithm Overview

1. **Compute correlation matrices** between observations at different times
2. **Perform SVD** on the correlation matrix between past and future
3. **Recover observation operators** that represent how observations transform beliefs about hidden states

### Observable Representation

Instead of explicitly recovering $T$ and $O$, learn an **observable operator model**:

$$\Pr[x_1, x_2, \ldots, x_t] = \vec{1}^\top A_{x_t} \cdots A_{x_2} A_{x_1} \vec{\pi}'$$

where $A_x$ are observable operators derived from the spectral decomposition.

---

## 4. Sample Complexity

### Main Result

The algorithm learns an approximate model with:
- **Sample complexity**: Polynomial in $m$, $1/\epsilon$, $1/\delta$
- **No explicit dependence** on observation space size $n$

### Spectral Conditions Required

1. **Observation matrix rank**: $O$ has rank $m$ (observations distinguish states)
2. **Transition matrix rank**: $T$ has rank $m$
3. **Singular value bounds**: Smallest singular values bounded away from zero

---

## 5. Theoretical Guarantees

### Approximation of Joint Distributions

For observation sequences of length $t$:
$$\|P_{true}(x_1, \ldots, x_t) - P_{learned}(x_1, \ldots, x_t)\|_{TV} \leq \epsilon \cdot \text{poly}(t)$$

### Approximation of Conditional Distributions

For predicting $x_t$ given history:
$$\|P_{true}(x_t | x_1, \ldots, x_{t-1}) - P_{learned}(x_t | x_1, \ldots, x_{t-1})\|_{TV} \leq \epsilon$$

The conditional error is **asymptotically bounded** (doesn't grow with $t$).

---

## 6. Connection to Related Work

### Subspace Identification

From control theory: spectral methods for learning linear dynamical systems (Kalman filters). Key idea: SVD/CCA between past and future observations.

### Observable Operator Models

Represent probability of sequences as products of matrix operators:
- Schützenberger (1961): Multiplicity automata
- Jaeger (2000): Observable Operator Models
- Littman et al. (2001): Predictive State Representations

### Comparison to Mossel & Roch (2006)

Both use same rank conditions, but this algorithm:
- Handles large observation spaces better
- Avoids explicit recovery of $O$ and $T$
- More sample-efficient

---

## 7. Algorithm Details

### Step 1: Estimate Correlation Matrices

From data, estimate:
- $P_{21}$: Correlation between consecutive observations
- $P_{3,1}$: Correlation between observations separated by one step
- $P_{3x1}$: Three-way correlations

### Step 2: Singular Value Decomposition

Compute SVD of $P_{21}$:
$$P_{21} = U \Sigma V^\top$$

The left singular vectors $U$ span the "observation space" projected to hidden state space.

### Step 3: Recover Observable Operators

For each observation $x$:
$$A_x = U^\top P_{3x1} (U^\top P_{21})^{-1}$$

These operators satisfy the multiplication property for computing sequence probabilities.

---

## Key Concepts

| Concept | Definition |
|---------|------------|
| **Spectral learning** | Using eigenvalue/SVD decomposition to learn latent structure |
| **Observable operators** | Matrices $A_x$ encoding observation dynamics |
| **Rank condition** | Requirement that $O$ and $T$ have full rank $m$ |
| **CCA** | Canonical Correlation Analysis between past and future |

---

## Significance for emic

This paper provides:
1. **Alternative to CSSR**: A fundamentally different approach to learning HMM-like models
2. **Provable guarantees**: Polynomial sample complexity with error bounds
3. **Scalability**: Handles large observation spaces efficiently
4. **Simplicity**: Only requires SVD and matrix operations

The spectral approach complements CSSR by:
- Working directly with matrix representations
- Avoiding iterative refinement
- Providing theoretical error bounds

---

## References

Key citations:
1. Baum, L. E. & Eagon, J. A. (1967). An inequality with applications to statistical estimation for probabilistic functions
2. Rabiner, L. R. (1989). A tutorial on hidden Markov models
3. Jaeger, H. (2000). Observable operator models for discrete stochastic time series
4. Littman, M. L. et al. (2001). Predictive representations of state

---

*Extracted from: hsu2012spectral.pdf*
