# Causal Asymmetry in a Quantum World

**Authors:** Jayne Thompson, Andrew J. P. Garner, John R. Mahoney, James P. Crutchfield, Vlatko Vedral, and Mile Gu
**Affiliations:**
- Centre for Quantum Technologies, National University of Singapore
- Austrian Academy of Sciences
- Complexity Sciences Center, UC Davis
- University of Oxford
- Nanyang Technological University
**Source:** arXiv:1712.02368v2 [quant-ph]
**Date:** July 21, 2018

---

## Abstract

Causal asymmetry is one of the great surprises in predictive modelling: the memory required to predict the future differs from the memory required to retrodict the past. There is a privileged temporal direction for modelling a stochastic process where memory costs are minimal. Models operating in the other direction incur an unavoidable memory overhead. Here we show that this overhead can vanish when quantum models are allowed. Quantum models forced to run in the less natural temporal direction not only surpass their optimal classical counterparts, but also any classical model running in reverse time. This holds even when the memory overhead is unbounded, resulting in quantum models with unbounded memory advantage.

---

## 1. Introduction

### The Puzzle of Time's Arrow

How can we observe an asymmetry in the temporal order of events when physics at the quantum level is time-symmetric? The source of time's barbed arrow is a longstanding puzzle in foundational science.

**Causal asymmetry** offers a provocative perspective: it asks how Occam's razor—the principle of assuming no more causes than necessary—can privilege one particular temporal direction over another.

### Key Question

If we want to model a process causally (making statistically correct future predictions based only on past information), what is the minimum past information we must store? Are we forced to store more data if we model events in one particular temporal order over the other?

---

## 2. Causal Asymmetry in Classical Models

### The Cannonball Example (Symmetric)

A cannonball in free fall: to model its future trajectory, we need only its current position and velocity. This remains true even in reverse-time—an example of **causal symmetry**.

### The Shattering Glass Example (Asymmetric)

A glass shattering on the floor:
- **Forward direction**: Future distribution of shards depends only on current position, velocity, and orientation
- **Reverse direction**: May need to track information about each shard to infer prior trajectory

This potential divergence is quantified in **computational mechanics**.

### Quantifying Causal Asymmetry

Let:
- $C^+$ = statistical complexity for forward-time (causal) model
- $C^-$ = statistical complexity for reverse-time (retrocausal) model

**Causal asymmetry**: $\Delta C = C^- - C^+ \neq 0$ in general

The asymmetry can be **unbounded**—this phenomenon is cited as a candidate source of time's arrow.

---

## 3. Quantum Models Can Eliminate Causal Asymmetry

### Main Result

The memory overhead from causal asymmetry can vanish when quantum models are used. Specifically:

**Theorem**: For stochastic processes exhibiting classical causal asymmetry, there exist quantum models that:
1. Surpass optimal classical models running in the "less natural" direction
2. Can achieve unbounded memory advantage over classical retrocausal models

### Implications

- Causal asymmetry may be a consequence of **classicality constraints**, not fundamental physics
- Quantum mechanics provides a more parsimonious framework for modeling stochastic processes
- The arrow of time may have different status in quantum vs. classical descriptions

---

## 4. Technical Framework

### Classical ε-Machines

The optimal classical predictor (ε-machine) maps histories to causal states:
$$\epsilon: \overleftarrow{x} \mapsto s \in \mathcal{S}$$

Statistical complexity: $C_\mu = H(\mathcal{S})$ (entropy of the causal state distribution)

### Quantum ε-Machines

A quantum model encodes causal states in a quantum system:
$$\overleftarrow{x} \mapsto |\sigma_{\overleftarrow{x}}\rangle$$

The quantum statistical complexity:
$$C_q = S(\rho)$$
where $\rho = \sum_s p_s |\sigma_s\rangle\langle\sigma_s|$ and $S$ is the von Neumann entropy.

### Key Inequality

$$C_q \leq C_\mu$$

with equality only for special cases. The quantum advantage comes from the ability to encode non-orthogonal states.

---

## 5. Example: Perturbed Coins Process

A process where:
- A biased coin is flipped repeatedly
- With small probability $p$, the bias switches

This process exhibits:
- Finite $C^+$ (forward complexity)
- $C^- \to \infty$ as observation precision increases (unbounded reverse complexity)

**Quantum result**: A quantum retrocausal model can have finite complexity even when $C^- = \infty$.

---

## Key Concepts

| Concept | Definition |
|---------|------------|
| **Causal model** | Predicts future from past information |
| **Retrocausal model** | "Predicts" past from future information |
| **Statistical complexity** $C_\mu$ | Memory required by optimal classical model |
| **Causal asymmetry** $\Delta C$ | Difference between forward and reverse complexity |
| **Quantum statistical complexity** $C_q$ | Memory required by optimal quantum model |

---

## Significance

1. **Foundational**: Challenges the view that time's arrow emerges from information-theoretic considerations alone
2. **Practical**: Quantum models can be exponentially more efficient for certain prediction tasks
3. **Conceptual**: Suggests that apparent temporal asymmetry may be an artifact of classical descriptions

---

## Connection to Computational Mechanics

This paper extends the ε-machine framework to quantum systems, building on:
- Crutchfield & Young (1989): "Inferring Statistical Complexity"
- Shalizi & Crutchfield (2001): "Computational Mechanics"
- Gu et al. (2012): "Occam's Quantum Razor"

---

## References

Key citations from the paper:
1. Crutchfield, J. P. & Young, K. (1989). Inferring statistical complexity. *Phys. Rev. Lett.* 63, 105
2. Shalizi, C. R. & Crutchfield, J. P. (2001). Computational mechanics. *Phys. Rev. E* 63, 041104
3. Gu, M. et al. (2012). Quantum mechanics can reduce the complexity of classical models. *Nat. Commun.* 3, 762

---

*Extracted from: thompson2018causal.pdf*
