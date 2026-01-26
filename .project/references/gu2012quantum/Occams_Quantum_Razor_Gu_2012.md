# Occam's Quantum Razor: How Quantum Mechanics Can Reduce the Complexity of Classical Models

**Authors:** Mile Gu, Karoline Wiesner, Elisabeth Rieper, and Vlatko Vedral
**Affiliations:**
- Center for Quantum Technology, National University of Singapore
- Centre for Complexity Sciences, University of Bristol
- University of Oxford
**Source:** arXiv:1102.1994v5 [quant-ph]; Nature Communications 3, 763 (2012)
**Date:** April 2, 2012

---

## Abstract

Mathematical models are an essential component of quantitative science. They generate predictions about the future, based on information available in the present. In the spirit of Occam's razor, simpler is better; should two models make identical predictions, the one that requires less input is preferred. Yet, for almost all stochastic processes, even the provably optimal classical models waste information. The amount of input information they demand exceeds the amount of predictive information they output. We systematically construct quantum models that break this classical bound, and show that the system of minimal entropy that simulates such processes must necessarily feature quantum dynamics. This indicates that many observed phenomena could be significantly simpler than classically possible should quantum effects be involved.

---

## 1. Introduction

### Occam's Razor and Models

Occam's razor—"plurality is not to be posited without necessity"—is an important heuristic in science. In Newton's words: "We are to admit no more causes of natural things than such as are both true and sufficient to explain their appearances."

### Models and Simulators

A mathematical model is an algorithmic abstraction of observable output. The relationship between models and simulators:

1. **Model**: A stochastic function $f$ mapping present data to future predictions
2. **Simulator**: Physical realization of the model

If a model demands input entropy $C$, its physical realization must have capacity to store that information.

### The Efficiency Problem

For almost all stochastic processes, optimal classical models **waste information**:
- Input information demanded > Predictive information output
- This waste is unavoidable classically

---

## 2. Framework

### Stochastic Processes

A dynamical system observed at discrete times $t \in \mathbb{Z}$:
- Outcomes: $x_t \in \Sigma$ (alphabet)
- Past: $\overleftarrow{x} = \ldots x_{-3} x_{-2} x_{-1}$
- Future: $\overrightarrow{x} = x_0 x_1 x_2 \ldots$

### Predictive Information

The **excess entropy** (predictive information):
$$E = I(\overleftarrow{X} : \overrightarrow{X})$$

This is the mutual information between past and future—the minimum information about the past needed to predict the future optimally.

### Statistical Complexity

The **statistical complexity** $C_\mu$ is the entropy of the causal state distribution in the optimal classical model (ε-machine):
$$C_\mu = H(\mathcal{S})$$

### The Classical Bound

For classical models:
$$C_\mu \geq E$$

The gap $C_\mu - E$ represents **wasted information**—stored information that doesn't contribute to prediction.

---

## 3. Quantum Advantage

### Quantum Models

A quantum model encodes the past in a quantum state:
$$\overleftarrow{x} \mapsto |\phi_{\overleftarrow{x}}\rangle$$

The **quantum statistical complexity**:
$$C_q = S(\rho)$$
where $\rho$ is the average quantum state and $S$ is von Neumann entropy.

### Breaking the Classical Bound

**Main Result**: For many processes:
$$C_q < C_\mu$$

Quantum models can be strictly more efficient than any classical model.

### Approaching the Ideal

In some cases:
$$C_q \to E$$

The quantum model can approach the fundamental limit (predictive information) that classical models cannot reach.

---

## 4. Construction of Quantum Models

### The q-Machine

For a classical ε-machine with causal states $\{s_i\}$ and transitions, construct:

1. **Quantum causal states**: $|s_i\rangle$ (not necessarily orthogonal)
2. **Unitary evolution**: Implements transitions
3. **Measurement**: Produces output symbols

### Why Quantum is Better

Classical models must distinguish causal states that have different pasts but identical futures. Quantum models can use **non-orthogonal states** for such cases, reducing the distinguishability (and hence entropy).

---

## 5. Examples

### The Perturbed Coin

A coin with bias $p$ that occasionally (probability $\epsilon$) switches to bias $1-p$:

| Metric | Value |
|--------|-------|
| Predictive information $E$ | Finite, small |
| Classical complexity $C_\mu$ | Can be arbitrarily large |
| Quantum complexity $C_q$ | Approaches $E$ |

### General Result

For almost all stochastic processes:
- Classical: $C_\mu > E$ (waste is generic)
- Quantum: $C_q$ can approach $E$ (waste eliminated)

---

## 6. Implications

### Operational Consequences

1. **Simulation efficiency**: Quantum simulators can require less memory
2. **Complexity measures**: Classical complexity may overestimate true process complexity
3. **Thermodynamics**: Connections to work extraction and heat dissipation

### Fundamental Questions

- Is the quantum advantage observable in nature?
- What physical processes exploit this efficiency?
- Are biological systems operating near quantum limits?

---

## Key Concepts

| Concept | Symbol | Definition |
|---------|--------|------------|
| Excess entropy | $E$ | Mutual information between past and future |
| Statistical complexity | $C_\mu$ | Entropy of classical ε-machine states |
| Quantum complexity | $C_q$ | Von Neumann entropy of quantum model |
| Cryptic order | $\chi = C_\mu - E$ | Information stored but not predictive |

---

## Key Inequalities

$$E \leq C_q \leq C_\mu$$

- Left inequality: Fundamental limit (information conservation)
- Right inequality: Quantum advantage (provably better than classical)

---

## Connection to ε-Machines

This paper extends computational mechanics by:
1. Defining quantum analogues of causal states
2. Proving quantum models can be more efficient
3. Constructing explicit quantum simulators

The ε-machine remains the optimal *classical* model; the q-machine is its quantum successor.

---

## References

Key citations:
1. Crutchfield, J. P. & Young, K. (1989). Inferring statistical complexity. *Phys. Rev. Lett.* 63, 105
2. Shalizi, C. R. & Crutchfield, J. P. (2001). Computational mechanics. *Phys. Rev. E* 63, 041104
3. Crutchfield, J. P. (1994). The calculi of emergence. *Physica D* 75, 11–54

---

*Extracted from: gu2012quantum.pdf*
