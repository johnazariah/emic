# Mathematical Framework for Quantum Computational Mechanics

*Precise definitions for implementation in emic*

---

## Overview

This document provides rigorous mathematical definitions for implementing quantum complexity measures. It serves as a reference for the `emic.quantum` module.

**Notation conventions:**
- Random variables: uppercase ($X$, $S$)
- Realizations: lowercase ($x$, $s$)
- Quantum states: kets ($|s\rangle$)
- Density matrices: Greek ($\rho$, $\sigma$)
- Entropies: $H$ (Shannon), $S$ (von Neumann)

---

## Part 1: Classical Foundations

### 1.1 Stochastic Process

A **stochastic process** is a joint probability distribution over past and future:

$$P(\overleftarrow{X}, \overrightarrow{X})$$

where:
- $\overleftarrow{X} = \ldots X_{-2} X_{-1}$ (semi-infinite past)
- $\overrightarrow{X} = X_0 X_1 X_2 \ldots$ (semi-infinite future)
- Each $X_t$ takes values in finite alphabet $\Sigma$

### 1.2 Causal States

The **causal equivalence relation** on histories:

$$\overleftarrow{x} \sim \overleftarrow{y} \iff P(\overrightarrow{X} | \overleftarrow{X} = \overleftarrow{x}) = P(\overrightarrow{X} | \overleftarrow{X} = \overleftarrow{y})$$

A **causal state** is an equivalence class:

$$S_j = \{ \overleftarrow{x} : \epsilon(\overleftarrow{x}) = j \}$$

where $\epsilon: \overleftarrow{X} \to \mathcal{S}$ is the causal state function.

### 1.3 Epsilon-Machine

An **ε-machine** is the tuple $(\mathcal{S}, \Sigma, T, \pi)$ where:

- $\mathcal{S} = \{S_1, \ldots, S_N\}$: set of causal states
- $\Sigma = \{x_1, \ldots, x_m\}$: output alphabet
- $T^{(x)}_{jk} = P(S_k, x | S_j)$: transition probability from $S_j$ to $S_k$ while emitting $x$
- $\pi = (\pi_1, \ldots, \pi_N)$: stationary distribution over causal states

**Properties:**
- Unifilar: for each $(S_j, x)$, at most one $S_k$ with $T^{(x)}_{jk} > 0$
- Generates process: iterating transitions produces correct statistics

### 1.4 Classical Complexity Measures

**Statistical Complexity:**
$$C_\mu = H(\mathcal{S}) = -\sum_{j=1}^{N} \pi_j \log_2 \pi_j$$

**Entropy Rate:**
$$h_\mu = H(X_0 | S) = \sum_{j=1}^{N} \pi_j H(X | S = S_j)$$

where $H(X | S = S_j) = -\sum_{x \in \Sigma} P(x|S_j) \log_2 P(x|S_j)$ and $P(x|S_j) = \sum_k T^{(x)}_{jk}$.

**Excess Entropy:**
$$E = I(\overleftarrow{X}; \overrightarrow{X})$$

The mutual information between past and future. Fundamental lower bound on memory.

**Crypticity:**
$$\chi = C_\mu - E = H(S | \overrightarrow{X})$$

Information about causal state not revealed by the future.

---

## Part 2: Quantum States and Entropy

### 2.1 Quantum State Vectors

A **pure quantum state** is a unit vector in Hilbert space $\mathcal{H}$:

$$|\psi\rangle \in \mathcal{H}, \quad \langle\psi|\psi\rangle = 1$$

For our purposes, $\mathcal{H} = \mathbb{C}^d$ for finite dimension $d$.

### 2.2 Density Matrices

A **density matrix** represents a (possibly mixed) quantum state:

$$\rho = \sum_i p_i |\psi_i\rangle\langle\psi_i|$$

**Properties:**
1. Hermitian: $\rho^\dagger = \rho$
2. Unit trace: $\text{Tr}(\rho) = 1$
3. Positive semi-definite: eigenvalues $\lambda_j \geq 0$

### 2.3 Von Neumann Entropy

For density matrix $\rho$ with eigenvalues $\{\lambda_j\}$:

$$S(\rho) = -\text{Tr}(\rho \log_2 \rho) = -\sum_j \lambda_j \log_2 \lambda_j$$

**Properties:**
- $S(\rho) \geq 0$
- $S(\rho) = 0$ iff $\rho$ is pure
- $S(\rho) \leq \log_2 d$ (equality for maximally mixed)

---

## Part 3: Q-Machine Construction

### 3.1 Signal States

Given ε-machine $(\mathcal{S}, \Sigma, T, \pi)$, define Hilbert space:

$$\mathcal{H} = \mathcal{H}_\Sigma \otimes \mathcal{H}_\mathcal{S}$$

with dimension $d = |\Sigma| \times N$.

The **quantum signal state** for causal state $S_j$ is:

$$|s_j\rangle = \sum_{k=1}^{N} \sum_{x \in \Sigma} \sqrt{T^{(x)}_{jk}} |x\rangle \otimes |k\rangle$$

where:
- $|x\rangle$: orthonormal basis for symbol space ($x \in \Sigma$)
- $|k\rangle$: orthonormal basis for state index space ($k \in \{1, \ldots, N\}$)

**Normalization check:**
$$\langle s_j | s_j \rangle = \sum_{k,x} T^{(x)}_{jk} = 1 \quad ✓$$

### 3.2 Overlaps Between Signal States

$$\langle s_j | s_l \rangle = \sum_{k=1}^{N} \sum_{x \in \Sigma} \sqrt{T^{(x)}_{jk} T^{(x)}_{lk}}$$

**Key insight:** Overlap is nonzero when both $S_j$ and $S_l$ can transition to the same state $S_k$ on the same symbol $x$. This is the **irreversibility condition**.

### 3.3 Average Density Matrix

The q-machine's state ensemble:

$$\rho = \sum_{j=1}^{N} \pi_j |s_j\rangle\langle s_j|$$

This is generally a mixed state (unless all signal states are identical).

### 3.4 Quantum Statistical Complexity

$$C_q = S(\rho) = -\text{Tr}(\rho \log_2 \rho)$$

**The Key Inequality:**
$$E \leq C_q \leq C_\mu$$

- Left: Information-theoretic bound (no model can use less than $E$)
- Right: Quantum advantage (strict when ε-machine is irreversible)

---

## Part 4: Complexity Measures

### 4.1 Quantum Advantage

The **quantum memory advantage**:

$$\Delta_q = C_\mu - C_q$$

Measures bits saved by using quantum encoding.

**Theorem (Gu et al. 2012):** $\Delta_q > 0$ if and only if the ε-machine satisfies the irreversibility condition.

### 4.2 Bidirectional Measures

For the **reverse-time process**, swap past ↔ future and reverse symbol order.

**Retrodictive statistical complexity:**
$$C_\mu^+ = H(\mathcal{S}^+)$$

where $\mathcal{S}^+$ are the reverse causal states.

**Predictive statistical complexity:**
$$C_\mu^- = H(\mathcal{S}^-) = C_\mu$$

(Using notation from Thompson et al. 2018)

**Causal asymmetry:**
$$\Delta C = |C_\mu^+ - C_\mu^-|$$

### 4.3 Quantum Causal Asymmetry

Define quantum retrodictive complexity $C_q^+$ from reverse q-machine.

**Theorem (Thompson et al. 2018):** Quantum models can eliminate causal asymmetry:

$$C_q^+ = C_q^- = C_q$$

even when $\Delta C$ is unbounded.

---

## Part 5: Decoherence Channels

### 5.1 Quantum Channel Formalism

A **quantum channel** $\mathcal{E}$ transforms density matrices:

$$\mathcal{E}(\rho) = \sum_k K_k \rho K_k^\dagger$$

where Kraus operators satisfy $\sum_k K_k^\dagger K_k = I$.

### 5.2 Dephasing Channel

The **dephasing channel** with strength $\gamma \in [0,1]$:

$$\mathcal{D}_\gamma(\rho) = (1-\gamma)\rho + \gamma \sum_i |i\rangle\langle i| \rho |i\rangle\langle i|$$

In the computational basis $\{|i\rangle\}$:

$$[\mathcal{D}_\gamma(\rho)]_{jk} = \begin{cases}
\rho_{jk} & \text{if } j = k \\
(1-\gamma)\rho_{jk} & \text{if } j \neq k
\end{cases}$$

**Effect:** Suppresses off-diagonal coherences by factor $(1-\gamma)$.

**Limits:**
- $\gamma = 0$: identity (no decoherence)
- $\gamma = 1$: complete dephasing, $\rho \to \text{diag}(\rho)$

### 5.3 Decohered Complexity

$$C_q(\gamma) = S(\mathcal{D}_\gamma(\rho))$$

**Properties:**
- $C_q(0) = C_q$ (pure quantum)
- $C_q(1) = H(\text{diag}(\rho))$ (fully classical)
- $C_q(\gamma)$ is monotonically non-decreasing in $\gamma$

### 5.4 Depolarizing Channel

Alternative decoherence model:

$$\mathcal{P}_\gamma(\rho) = (1-\gamma)\rho + \gamma \frac{I}{d}$$

Mixes toward maximally mixed state.

---

## Part 6: Algorithms

### 6.1 Q-Machine Construction

```
CONSTRUCT_QMACHINE(epsilon_machine):
    Input: ε-machine with states S, alphabet Σ, transitions T, distribution π
    Output: Quantum states {|s_j⟩}, density matrix ρ, complexity C_q

    N = |S|
    m = |Σ|
    d = N × m  # Hilbert space dimension

    # Construct signal states
    for j in 1..N:
        |s_j⟩ = zero_vector(d)
        for k in 1..N:
            for x in Σ:
                idx = index(x) × N + k  # tensor product indexing
                |s_j⟩[idx] = sqrt(T[x][j,k])

    # Construct average density matrix
    ρ = zero_matrix(d, d)
    for j in 1..N:
        ρ += π[j] × outer(|s_j⟩, conjugate(|s_j⟩))

    # Compute quantum complexity
    eigenvalues = hermitian_eigenvalues(ρ)
    eigenvalues = filter(λ > ε, eigenvalues)  # numerical tolerance
    C_q = -sum(λ × log2(λ) for λ in eigenvalues)

    return {|s_j⟩}, ρ, C_q
```

### 6.2 Decoherence Trajectory

```
DECOHERENCE_TRAJECTORY(ρ, gamma_values):
    Input: Density matrix ρ, list of γ ∈ [0,1]
    Output: List of (γ, C_q(γ)) pairs

    results = []
    d = dimension(ρ)

    for γ in gamma_values:
        # Apply dephasing
        ρ_decohered = (1 - γ) × ρ + γ × diagonal_matrix(diagonal(ρ))

        # Compute entropy
        eigenvalues = hermitian_eigenvalues(ρ_decohered)
        eigenvalues = filter(λ > ε, eigenvalues)
        C_q_gamma = -sum(λ × log2(λ) for λ in eigenvalues)

        results.append((γ, C_q_gamma))

    return results
```

### 6.3 Reverse Machine Construction

```
CONSTRUCT_REVERSE_MACHINE(epsilon_machine):
    Input: Forward ε-machine
    Output: Reverse ε-machine

    # This is non-trivial and requires:
    # 1. Computing reverse causal states
    # 2. Computing reverse transitions
    # See Shalizi & Crutchfield (2001) Appendix C

    # For known processes (golden mean, even, perturbed coin),
    # reverse machines can be constructed analytically

    raise NotImplementedError("Full algorithm TBD")
```

---

## Part 7: Tensor Product Indexing

### 7.1 Convention

For $|x\rangle \otimes |k\rangle$ with $x \in \{0, \ldots, m-1\}$ and $k \in \{0, \ldots, N-1\}$:

$$\text{index}(x, k) = x \times N + k$$

Total dimension: $d = m \times N$.

### 7.2 Matrix Representation

The density matrix $\rho$ has block structure:

$$\rho = \begin{pmatrix}
\rho_{00} & \rho_{01} & \cdots \\
\rho_{10} & \rho_{11} & \cdots \\
\vdots & \vdots & \ddots
\end{pmatrix}$$

where $\rho_{xy}$ is an $N \times N$ block corresponding to symbol pair $(x, y)$.

---

## Part 8: Worked Example - Golden Mean Process

### 8.1 Classical Machine

States: $S_0$ (last symbol was 0 or start), $S_1$ (last symbol was 1)

Transitions:
- From $S_0$: emit 0 → $S_0$ with prob $p$, emit 1 → $S_1$ with prob $1-p$
- From $S_1$: emit 0 → $S_0$ with prob 1 (forced)

Transition matrices:
$$T^{(0)} = \begin{pmatrix} p & 0 \\ 1 & 0 \end{pmatrix}, \quad T^{(1)} = \begin{pmatrix} 0 & 1-p \\ 0 & 0 \end{pmatrix}$$

Stationary distribution: $\pi_0 = \frac{1}{2-p}$, $\pi_1 = \frac{1-p}{2-p}$

For $p = 0.5$: $\pi_0 = 2/3$, $\pi_1 = 1/3$

$$C_\mu = -\frac{2}{3}\log_2\frac{2}{3} - \frac{1}{3}\log_2\frac{1}{3} \approx 0.918 \text{ bits}$$

### 8.2 Quantum States

Hilbert space: $\mathbb{C}^4$ (2 symbols × 2 states)

Basis: $|0,0\rangle, |0,1\rangle, |1,0\rangle, |1,1\rangle$

Signal states:
$$|s_0\rangle = \sqrt{p}|0,0\rangle + \sqrt{1-p}|1,1\rangle = \sqrt{0.5}|0,0\rangle + \sqrt{0.5}|1,1\rangle$$
$$|s_1\rangle = |0,0\rangle$$

Overlap:
$$\langle s_0 | s_1 \rangle = \sqrt{p} = \sqrt{0.5} \approx 0.707$$

### 8.3 Density Matrix

$$\rho = \frac{2}{3}|s_0\rangle\langle s_0| + \frac{1}{3}|s_1\rangle\langle s_1|$$

In the $\{|0,0\rangle, |1,1\rangle\}$ subspace:

$$\rho = \frac{2}{3} \begin{pmatrix} 0.5 & 0.5 \\ 0.5 & 0.5 \end{pmatrix} + \frac{1}{3} \begin{pmatrix} 1 & 0 \\ 0 & 0 \end{pmatrix} = \begin{pmatrix} 2/3 & 1/3 \\ 1/3 & 1/3 \end{pmatrix}$$

Eigenvalues: solve $\det(\rho - \lambda I) = 0$

$$\lambda^2 - \lambda + \frac{2}{9} - \frac{1}{9} = 0 \implies \lambda^2 - \lambda + \frac{1}{9} = 0$$

$$\lambda = \frac{1 \pm \sqrt{1 - 4/9}}{2} = \frac{1 \pm \sqrt{5/9}}{2} \approx 0.873, 0.127$$

$$C_q = -0.873 \log_2(0.873) - 0.127 \log_2(0.127) \approx 0.543 \text{ bits}$$

**Quantum advantage:** $C_\mu - C_q \approx 0.375$ bits (41% reduction)

---

## Part 9: Implementation Notes

### 9.1 Numerical Considerations

- Use `numpy.linalg.eigvalsh` for Hermitian eigenvalues
- Filter eigenvalues below tolerance $\epsilon \approx 10^{-12}$ to avoid $0 \log 0$
- Density matrices should be validated: Hermitian, unit trace, positive semi-definite

### 9.2 Type Definitions

```python
@dataclass(frozen=True)
class QuantumCausalState:
    classical_id: StateId
    state_vector: np.ndarray  # shape (d,), complex

@dataclass(frozen=True)
class QuantumEpsilonMachine:
    classical_machine: EpsilonMachine
    quantum_states: dict[StateId, QuantumCausalState]
    hilbert_dimension: int

    @cached_property
    def density_matrix(self) -> np.ndarray:
        """ρ = Σ πⱼ |sⱼ⟩⟨sⱼ|"""
        ...

    @cached_property
    def quantum_complexity(self) -> float:
        """Cq = S(ρ)"""
        ...
```

### 9.3 Dependencies

- `numpy`: Linear algebra, eigenvalue computation
- No external quantum libraries needed for this scope

---

## References

1. Gu, M. et al. "Quantum mechanics can reduce the complexity of classical models." Nature Communications 3, 762 (2012)
2. Thompson, J. et al. "Causal Asymmetry in a Quantum World." Phys. Rev. X 8, 031013 (2018)
3. Shalizi, C.R. & Crutchfield, J.P. "Computational Mechanics: Pattern and Prediction, Structure and Simplicity." J. Stat. Phys. 104, 817 (2001)
4. Nielsen, M.A. & Chuang, I.L. *Quantum Computation and Quantum Information* (Cambridge, 2000)

---

*Document version: 1.0*
*Created: 2026-01-28*
*Status: Ready for implementation*
