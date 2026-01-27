# Key Concepts in Quantum Computational Mechanics

*Mathematical definitions and framework for extending emic to quantum*

---

## Classical Foundations (emic current)

### Stochastic Process
A discrete-time process producing symbols $x_t \in \Sigma$ (alphabet).
- **Past**: $\overleftarrow{x} = \ldots x_{-2} x_{-1}$
- **Future**: $\overrightarrow{x} = x_0 x_1 x_2 \ldots$

### Causal States
Equivalence classes of histories with identical predictive distributions:
$$\sigma(\overleftarrow{x}) = [\overleftarrow{x}]_\sim \quad \text{where} \quad \overleftarrow{x} \sim \overleftarrow{y} \iff P(\overrightarrow{X}|\overleftarrow{x}) = P(\overrightarrow{X}|\overleftarrow{y})$$

### Epsilon-Machine (εM)
The minimal unifilar HMM built from causal states:
- States: $\mathcal{S} = \{s_1, s_2, \ldots\}$
- Transitions: $T^{(x)}_{ij} = P(s_j, x | s_i)$
- Stationary distribution: $\pi$

### Statistical Complexity
$$C_\mu = H(\mathcal{S}) = -\sum_i \pi_i \log \pi_i$$

Entropy of the causal state distribution—memory required for optimal prediction.

### Entropy Rate
$$h_\mu = H(X_0 | \overleftarrow{X}) = H(X_0 | S)$$

Irreducible randomness per symbol.

### Excess Entropy (Predictive Information)
$$E = I(\overleftarrow{X}; \overrightarrow{X})$$

Mutual information between past and future—fundamental lower bound on memory.

### Crypticity
$$\chi = C_\mu - E$$

Information stored in the epsilon-machine that doesn't contribute to prediction. This is the **classical waste** that quantum models can eliminate.

---

## Quantum Extensions

### Quantum Causal States
Encode histories in quantum states:
$$\overleftarrow{x} \mapsto |\phi_{\overleftarrow{x}}\rangle$$

Key insight: States with different pasts but identical futures can be **non-orthogonal**, reducing distinguishability and hence entropy.

### Quantum Epsilon-Machine (q-machine)
Construction:
1. Assign quantum state $|s_i\rangle$ to each causal state (not necessarily orthogonal)
2. Define unitary evolution implementing transitions
3. Measurement produces output symbols

The average quantum state:
$$\rho = \sum_i \pi_i |s_i\rangle\langle s_i|$$

### Quantum Statistical Complexity
$$C_q = S(\rho) = -\text{Tr}(\rho \log \rho)$$

Von Neumann entropy of the quantum model's state.

### Key Inequality
$$E \leq C_q \leq C_\mu$$

- **Left**: Fundamental limit (information conservation)
- **Right**: Quantum advantage (can be strict)

### Why Quantum is Better
Classical models must **distinguish** causal states that lead to different pasts. If two causal states have:
- Different pasts
- Identical futures

Then classically they must be orthogonal (distinguishable). But quantum allows non-orthogonal encoding, reducing the entropy.

---

## Quantum Advantage Examples

### The Perturbed Coin
A coin with bias $p$ that occasionally (probability $\epsilon$) flips to bias $1-p$.

| Regime | $C_\mu$ | $E$ | $C_q$ | Advantage |
|--------|---------|-----|-------|-----------|
| Small $\epsilon$ | $O(1/\epsilon)$ | Finite | $\approx E$ | Unbounded |

This is the canonical example where quantum advantage is **unbounded**.

### General Statement
For almost all stochastic processes:
- Classical: $C_\mu > E$ (waste is generic)
- Quantum: $C_q$ can approach $E$ (waste eliminated)

---

## Implementation Strategy for emic

### Near-term (Classical)
1. **Add crypticity computation**: $\chi = C_\mu - E$
2. **Validate E computation**: Ensure excess entropy matches literature
3. **Identify high-crypticity processes**: These are targets for quantum advantage

### Medium-term (Quantum Representation)
1. **QuantumCausalState type**: Density matrices instead of probability vectors
2. **q-machine representation**: Non-orthogonal state assignments
3. **$C_q$ computation**: Von Neumann entropy of average state

### Long-term (Quantum Inference)
1. **Tomography integration**: Infer quantum states from measurement data
2. **Quantum process validation**: Compare inferred $C_q$ to theoretical values
3. **Emergence studies**: Track $C_q$ vs $C_\mu$ through decoherence

---

## Open Questions

1. **Constructive algorithm**: Given a classical εM, what's the optimal q-machine construction?
2. **Continuous variables**: How does quantum advantage extend to real-valued processes?
3. **Mixed states**: What about non-pure quantum causal states?
4. **Inference from data**: Can we infer q-machines directly from time series?
5. **Thermodynamics**: What's the thermodynamic cost of quantum simulation?

---

## Notation Summary

| Symbol | Meaning |
|--------|---------|
| $C_\mu$ | Classical statistical complexity |
| $C_q$ | Quantum statistical complexity |
| $E$ | Excess entropy (predictive information) |
| $h_\mu$ | Entropy rate |
| $\chi$ | Crypticity ($C_\mu - E$) |
| $\rho$ | Density matrix |
| $S(\rho)$ | Von Neumann entropy |
| $\mathcal{S}$ | Set of causal states |
| $\pi$ | Stationary distribution over states |

---

*Last updated: 2026-01-27*
