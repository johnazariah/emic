# Closing the Learning-Planning Loop with Predictive State Representations

**Authors:** Byron Boots, Sajid M. Siddiqi, and Geoffrey J. Gordon
**Affiliations:**
- Machine Learning Department, Carnegie Mellon University
- Robotics Institute, Carnegie Mellon University
**Source:** arXiv:0912.2385v1 [cs.LG]
**Date:** December 12, 2009

---

## Abstract

A central problem in artificial intelligence is that of planning to maximize future reward under uncertainty in a partially observable environment. In this paper we propose and demonstrate a novel algorithm which accurately learns a model of such an environment directly from sequences of action-observation pairs. We then close the loop from observations to actions by planning in the learned model and recovering a policy which is near-optimal in the original environment. Specifically, we present an efficient and statistically consistent spectral algorithm for learning the parameters of a Predictive State Representation (PSR). We demonstrate the algorithm by learning a model of a simulated high-dimensional, vision-based mobile robot planning task, and then perform approximate point-based planning in the learned PSR. Analysis of our results shows that the algorithm learns a state space which efficiently captures the essential features of the environment.

---

## 1. Introduction

### The Central Problem

Planning a sequence of actions to maximize future reward under uncertainty in partially observable environments.

### The Two Curses

1. **Curse of dimensionality**: For $n$ states, optimal policy is a function of $(n-1)$-dimensional belief distribution
2. **Curse of history**: Number of distinct policies grows exponentially in planning horizon

### Why Predictive State Representations?

**PSRs** and **Observable Operator Models (OOMs)** offer advantages:
- Greater representational capacity than POMDPs
- At least as compact representations
- Observable quantities (no latent variables)
- Compatible with approximate planning techniques

---

## 2. Predictive State Representations

### Definition

A PSR is a compact description of a dynamical system using **predictions of observable tests**.

**Test**: An ordered sequence of action-observation pairs $\tau = a_1 o_1 \ldots a_k o_k$

**History**: Past action-observation sequence $h = a_1^h o_1^h \ldots a_t^h o_t^h$

**Prediction**: Probability of test succeeding given history and actions

### Core Tests

A set of **core tests** $Q$ has the property that for any test $\tau$, there exists a function:
$$p(\tau^O | h || \tau^A) = f_\tau(p(Q^O | h || Q^A))$$

The **prediction vector** is a sufficient statistic:
$$p(Q^O | h || Q^A) = [p(q_1^O | h || q_1^A), \ldots, p(q_{|Q|}^O | h || q_{|Q|}^A)]^\top$$

### Linear PSRs

Functions $f_{aoq}$ are linear in the prediction vector:
$$f_{aoq}(p(Q^O | h || Q^A)) = m_{aoq}^\top p(Q^O | h || Q^A)$$

**Update rule** (Bayes):
$$p(Q^O | ho || a, Q^A) = \frac{M_{ao} p(Q^O | h || Q^A)}{m_\infty^\top M_{ao} p(Q^O | h || Q^A)}$$

---

## 3. Transformed PSRs

### Definition

**Transformed PSRs (TPSRs)** maintain linear combinations of test probabilities as sufficient statistics.

### Advantage

Given core tests, the parameter learning problem can be solved in **closed form** using spectral methods.

### Connection to Subspace Identification

TPSRs are closely related to:
- Linear Dynamical Systems (LDS)
- Hidden Markov Model representations
- Observable Operator Models

---

## 4. The Spectral Learning Algorithm

### Key Matrices

Define empirical estimates:
- $P_{T,H}$: Joint probabilities of tests and histories
- $P_{T,ao,H}$: Joint probabilities including action-observation pair

### Algorithm Steps

1. **Collect data**: Sequences of action-observation pairs
2. **Compute SVD**: $P_{T,H} \approx U \Sigma V^\top$
3. **Extract state representation**: Use $U$ to project to low-dimensional space
4. **Learn operators**: Estimate $M_{ao}$ matrices for each action-observation pair

### Statistical Consistency

The algorithm is **provably consistent**: as data increases, learned model converges to true model.

---

## 5. Planning in Learned PSRs

### Point-Based Value Iteration

Apply approximate planning algorithms designed for POMDPs:
1. Sample belief points in PSR state space
2. Compute value function over sampled points
3. Generalize to full state space

### From Observations to Actions

The complete loop:
1. **Learn**: PSR model from observation sequences
2. **Plan**: Compute near-optimal policy in learned model
3. **Act**: Execute policy in original environment

---

## 6. Experimental Results

### Robot Navigation Task

- High-dimensional visual observations
- Continuous observation space
- Partial observability

### Results

The spectral algorithm:
1. Learns compact state representation
2. Captures essential environmental features
3. Enables successful planning
4. Outperforms EM-based alternatives

### Key Finding

This is the **first research combining**:
- Principled, consistent model learning
- Positive results on challenging high-dimensional problem
- Closing the loop from observations to actions without human intervention

---

## 7. Comparison to Other Approaches

| Approach | Learning | Planning | Limitations |
|----------|----------|----------|-------------|
| EM for HMMs | Local optima | Yes | Doesn't scale |
| Model-free RL | N/A | Implicit | No model |
| MCMC for DBNs | Consistent | Yes | Too slow |
| **Spectral PSR** | **Consistent** | **Yes** | **None major** |

---

## Connection to Computational Mechanics

### Similarities to ε-Machines

- Both represent processes via sufficient statistics
- Both capture predictive information
- Both aim for minimal representations

### Differences

| Aspect | ε-Machines (CSSR) | PSRs |
|--------|-------------------|------|
| State definition | Equivalence classes of histories | Prediction vectors |
| Learning | Iterative splitting/merging | Spectral (closed-form) |
| Representations | Discrete states | Continuous state space |
| Guarantees | Asymptotic consistency | Finite-sample bounds |

### Complementary Strengths

- CSSR: Better interpretability, explicit causal states
- Spectral PSR: Better scalability, theoretical guarantees

---

## Key Concepts

| Concept | Definition |
|---------|------------|
| **Test** | Observable action-observation sequence |
| **Core tests** | Minimal set of tests that span prediction space |
| **Prediction vector** | Probabilities of core tests (sufficient statistic) |
| **Linear PSR** | PSR with linear update functions |
| **TPSR** | Transformed PSR with spectral learning |

---

## Significance for emic

This paper provides:
1. **Alternative representation**: PSRs complement ε-machines
2. **Spectral learning**: Closed-form solution vs. iterative CSSR
3. **Planning integration**: Direct connection to decision-making
4. **Scalability**: Handles high-dimensional observations

---

## References

Key citations:
1. Littman, M. L. et al. (2001). Predictive representations of state
2. Jaeger, H. (2000). Observable operator models for discrete stochastic time series
3. Singh, S. et al. (2004). Predictive state representations: A new theory for modeling dynamical systems

---

*Extracted from: boots2011closing.pdf*
