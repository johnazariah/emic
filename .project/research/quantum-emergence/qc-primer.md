# Quantum Computing Primer for Computational Mechanics

*Foundational quantum concepts needed for this research—not a general QC course*

---

## Overview

This primer covers the quantum mechanics concepts needed to understand why quantum models can be more efficient than classical ones. We focus on:

1. **State representation** — How quantum states differ from classical states
2. **Density matrices** — Mixed states and statistical ensembles
3. **Von Neumann entropy** — The quantum analog of Shannon entropy
4. **Decoherence channels** — How quantum becomes classical
5. **Connection to computational mechanics** — Why this matters for ε-machines

We skip quantum circuits, gates, and algorithms—those aren't needed here.

---

## Part 1: Quantum States

### Ket and Bra Notation

A quantum state is written as a **ket** $|\psi\rangle$, which is a column vector of complex numbers (amplitudes):

$$|\psi\rangle = \begin{pmatrix} \alpha \\ \beta \end{pmatrix}$$

The conjugate transpose is a **bra** $\langle\psi| = (\alpha^*, \beta^*)$, a row vector.

The inner product (overlap) between states is:

$$\langle\phi|\psi\rangle = \phi_1^* \psi_1 + \phi_2^* \psi_2 + \cdots$$

**Key property**: If $\langle\phi|\psi\rangle = 0$, the states are **orthogonal** (perfectly distinguishable). If $|\langle\phi|\psi\rangle| = 1$, they're the same state (up to phase).

### The Computational Basis

For a qubit (2-level system), the standard basis is:

$$|0\rangle = \begin{pmatrix} 1 \\ 0 \end{pmatrix}, \quad |1\rangle = \begin{pmatrix} 0 \\ 1 \end{pmatrix}$$

Any qubit state is a superposition:

$$|\psi\rangle = \alpha|0\rangle + \beta|1\rangle$$

with the normalization constraint $|\alpha|^2 + |\beta|^2 = 1$.

### Why Normalization?

The amplitudes squared give probabilities. If we measure in the $\{|0\rangle, |1\rangle\}$ basis:
- Probability of outcome 0: $|\alpha|^2$
- Probability of outcome 1: $|\beta|^2$

Total probability must be 1.

### Tensor Products: Composite Systems

When combining two systems, their joint state space is the **tensor product**:

$$|x\rangle \otimes |k\rangle = |x, k\rangle = |xk\rangle$$

For a 2-qubit system with $|x\rangle \in \{|0\rangle, |1\rangle\}$ and $|k\rangle \in \{|0\rangle, |1\rangle\}$:

$$\text{Basis: } |00\rangle, |01\rangle, |10\rangle, |11\rangle$$

Dimension: $d_{\text{total}} = d_1 \times d_2$.

In computational mechanics, q-machines use tensor products of symbol space $|x\rangle$ and state index space $|k\rangle$.

### Non-Orthogonal States Cannot Be Perfectly Distinguished

This is **critical** for quantum advantage.

If two states $|\phi\rangle$ and $|\psi\rangle$ satisfy $\langle\phi|\psi\rangle \neq 0$, no measurement can perfectly distinguish them. There's always some probability of confusion.

**Classical states** (like causal states in an ε-machine) must be perfectly distinguishable—they're stored in orthogonal "slots" of memory.

**Quantum states** can overlap, storing information more compactly. This is the source of quantum advantage.

---

## Part 2: Density Matrices

### Pure States

A pure state $|\psi\rangle$ can also be written as a **density matrix**:

$$\rho = |\psi\rangle\langle\psi|$$

This is the outer product—a matrix formed by multiplying the ket by the bra.

**Example**: For $|\psi\rangle = \alpha|0\rangle + \beta|1\rangle$:

$$\rho = |\psi\rangle\langle\psi| = \begin{pmatrix} |\alpha|^2 & \alpha\beta^* \\ \alpha^*\beta & |\beta|^2 \end{pmatrix}$$

The diagonal entries are probabilities. The off-diagonal entries (called **coherences**) encode quantum superposition—they have no classical analog.

### Mixed States

When a system is in state $|\psi_i\rangle$ with classical probability $p_i$, we can't write a single ket. Instead:

$$\rho = \sum_i p_i |\psi_i\rangle\langle\psi_i|$$

This is a **statistical mixture**—different from superposition!

**Key distinction**:
- Superposition: $|\psi\rangle = \alpha|0\rangle + \beta|1\rangle$ (quantum uncertainty)
- Mixture: $\rho = p|0\rangle\langle 0| + (1-p)|1\rangle\langle 1|$ (classical uncertainty)

### Critical Intuition: Superposition vs Mixed State vs Classical Mixture

This is perhaps the most important conceptual distinction in quantum mechanics:

| Type | What it means | Analogy | Matrix signature |
|------|--------------|---------|------------------|
| **Superposition** (pure) | System *is* in a definite quantum state that blends basis states | Coin spinning in air | Off-diagonals, rank 1, $\rho^2 = \rho$ |
| **Mixed state** | Classical uncertainty over which quantum state we're in | Several spinning coins, don't know which one | Can have off-diagonals, rank > 1, $\rho^2 \neq \rho$ |
| **Classical mixture** | Classical uncertainty over which *classical* (basis) state | Coin under cup, already landed | Diagonal only, no off-diagonals |

**The matrix view makes this crystal clear:**

```
Pure |0⟩:                  [1  0]     ← diagonal, in a definite basis state
                           [0  0]

Pure |1⟩:                  [0  0]     ← diagonal, in a definite basis state
                           [0  1]

Superposition (|0⟩+|1⟩)/√2: [0.5  0.5]  ← OFF-DIAGONALS = superposition
                           [0.5  0.5]

Classical 50/50 mixture:   [0.5  0  ]  ← diagonal = classical probability
                           [0    0.5]
```

The last two have **identical diagonals** (same measurement probabilities!) but:
- The superposition can interfere, has lower entropy, is "more ordered"
- The classical mixture cannot interfere, has maximum entropy for 2 states

**Why this matters for computational mechanics:**

In the q-machine density matrix $\rho = \sum_j \pi_j |s_j\rangle\langle s_j|$:
- The $\pi_j$ weights are classical uncertainty (which causal state?)
- Each $|s_j\rangle$ is a superposition in the product space
- The *overlap* between signal states creates off-diagonals in $\rho$
- Those off-diagonals enable compression: $C_q < C_\mu$

**The punchline:** Diagonal matrix = classical. Off-diagonals = quantum coherence = compression opportunity.

### Properties of Density Matrices

Every valid density matrix satisfies:
1. **Hermitian**: $\rho^\dagger = \rho$
2. **Unit trace**: $\text{Tr}(\rho) = 1$
3. **Positive semi-definite**: All eigenvalues $\geq 0$

### Purity

The **purity** is:

$$\gamma = \text{Tr}(\rho^2)$$

- Pure state: $\gamma = 1$
- Maximally mixed (most uncertain): $\gamma = 1/d$ where $d$ is dimension

### The Q-Machine Density Matrix

In computational mechanics, the q-machine's average state is:

$$\rho = \sum_{j=1}^{N} \pi_j |s_j\rangle\langle s_j|$$

where:
- $\pi_j$ is the stationary probability of causal state $s_j$
- $|s_j\rangle$ is the quantum signal state for $s_j$

This is generally a mixed state (statistical ensemble of quantum causal states).

---

## Part 3: Von Neumann Entropy

### Definition

The **von Neumann entropy** is the quantum analog of Shannon entropy:

$$S(\rho) = -\text{Tr}(\rho \log_2 \rho)$$

Since $\rho$ is Hermitian, it can be diagonalized with eigenvalues $\{\lambda_i\}$. Then:

$$S(\rho) = -\sum_i \lambda_i \log_2 \lambda_i$$

(with $0 \log 0 \equiv 0$)

### Properties

1. **Non-negativity**: $S(\rho) \geq 0$
2. **Pure states have zero entropy**: $S(|\psi\rangle\langle\psi|) = 0$
3. **Maximum entropy**: $S(\rho) \leq \log_2 d$ (achieved by maximally mixed state $\rho = I/d$)
4. **Classical limit**: If $\rho$ is diagonal, von Neumann entropy equals Shannon entropy of diagonal

### Worked Example: Computing Von Neumann Entropy

Consider two non-orthogonal states with equal probability:

$$|s_0\rangle = \sqrt{0.7}\,|0\rangle + \sqrt{0.3}\,|1\rangle$$
$$|s_1\rangle = \sqrt{0.3}\,|0\rangle + \sqrt{0.7}\,|1\rangle$$

with $\pi_0 = \pi_1 = 0.5$.

**Step 1**: Compute individual density matrices.

$$|s_0\rangle\langle s_0| = \begin{pmatrix} 0.7 & \sqrt{0.21} \\ \sqrt{0.21} & 0.3 \end{pmatrix} \approx \begin{pmatrix} 0.7 & 0.458 \\ 0.458 & 0.3 \end{pmatrix}$$

$$|s_1\rangle\langle s_1| = \begin{pmatrix} 0.3 & \sqrt{0.21} \\ \sqrt{0.21} & 0.7 \end{pmatrix} \approx \begin{pmatrix} 0.3 & 0.458 \\ 0.458 & 0.7 \end{pmatrix}$$

**Step 2**: Compute the mixed state.

$$\rho = 0.5 \cdot |s_0\rangle\langle s_0| + 0.5 \cdot |s_1\rangle\langle s_1| = \begin{pmatrix} 0.5 & 0.458 \\ 0.458 & 0.5 \end{pmatrix}$$

**Step 3**: Find eigenvalues.

For a 2×2 matrix $\begin{pmatrix} a & b \\ b & a \end{pmatrix}$, eigenvalues are $a \pm b$.

$$\lambda_+ = 0.5 + 0.458 = 0.958$$
$$\lambda_- = 0.5 - 0.458 = 0.042$$

(Check: $\lambda_+ + \lambda_- = 1$ ✓)

**Step 4**: Compute entropy.

$$S(\rho) = -0.958 \log_2(0.958) - 0.042 \log_2(0.042)$$
$$= -0.958 \times (-0.062) - 0.042 \times (-4.57)$$
$$= 0.059 + 0.192 = 0.251 \text{ bits}$$

**Interpretation**: The quantum complexity $C_q = 0.251$ bits. If these were orthogonal classical states with equal probability, we'd need $H = -2 \times 0.5 \log_2(0.5) = 1$ bit. The quantum encoding saves $1 - 0.251 = 0.749$ bits!

### Comparison: Classical vs Quantum

| Representation | States | Distinguishability | Complexity |
|---------------|--------|-------------------|------------|
| Classical | $S_0, S_1$ orthogonal | Perfect | $C_\mu = 1$ bit |
| Quantum | $\|s_0\rangle, \|s_1\rangle$ overlapping | Partial | $C_q = 0.251$ bits |

The overlap $\langle s_0|s_1\rangle = \sqrt{0.21} + \sqrt{0.21} = 0.917$ means these states are almost parallel—hard to distinguish, hence low entropy.

---

## Part 4: Decoherence Channels

### What is Decoherence?

Decoherence is the process by which quantum superpositions become classical mixtures. It happens when a quantum system interacts with an environment.

Physically: information "leaks" to the environment, destroying coherences (off-diagonal elements).

### Kraus Operator Formalism

A quantum channel $\mathcal{E}$ transforms density matrices:

$$\mathcal{E}(\rho) = \sum_k K_k \rho K_k^\dagger$$

where $\{K_k\}$ are **Kraus operators** satisfying $\sum_k K_k^\dagger K_k = I$.

### Dephasing Channel (Most Important for Us)

The dephasing channel with strength $\gamma \in [0,1]$ kills off-diagonal coherences:

$$\mathcal{E}_\gamma(\rho) = (1-\gamma)\rho + \gamma \sum_i |i\rangle\langle i|\rho|i\rangle\langle i|$$

The second term extracts only the diagonal. Equivalently:

$$\mathcal{E}_\gamma(\rho) = (1-\gamma)\rho + \gamma \cdot \text{diag}(\rho)$$

**Physical meaning**: With probability $\gamma$, the environment "measures" which basis state the system is in, destroying superposition.

### Dephasing: Step-by-Step Example

Start with $\rho = \begin{pmatrix} 0.5 & 0.458 \\ 0.458 & 0.5 \end{pmatrix}$ (from our earlier example).

Apply dephasing with $\gamma = 0.5$:

$$\mathcal{E}_{0.5}(\rho) = 0.5 \cdot \begin{pmatrix} 0.5 & 0.458 \\ 0.458 & 0.5 \end{pmatrix} + 0.5 \cdot \begin{pmatrix} 0.5 & 0 \\ 0 & 0.5 \end{pmatrix}$$

$$= \begin{pmatrix} 0.5 & 0.229 \\ 0.229 & 0.5 \end{pmatrix}$$

Eigenvalues: $0.5 \pm 0.229 = 0.729, 0.271$

New entropy:
$$S = -0.729 \log_2(0.729) - 0.271 \log_2(0.271) = 0.328 + 0.515 = 0.843 \text{ bits}$$

With $\gamma = 1$ (full dephasing):

$$\mathcal{E}_1(\rho) = \begin{pmatrix} 0.5 & 0 \\ 0 & 0.5 \end{pmatrix}$$

This is the maximally mixed state for our 2D system. Eigenvalues: $0.5, 0.5$.

$$S = -2 \times 0.5 \log_2(0.5) = 1 \text{ bit}$$

### Dephasing Trajectory Summary

| $\gamma$ | Off-diagonal | Eigenvalues | $S(\rho)$ |
|---------|--------------|-------------|-----------|
| 0 | 0.458 | 0.958, 0.042 | 0.251 bits |
| 0.5 | 0.229 | 0.729, 0.271 | 0.843 bits |
| 1 | 0 | 0.5, 0.5 | 1.000 bits |

**Key observation**: As $\gamma$ increases from 0 to 1, the quantum state becomes more classical and entropy increases from $C_q$ toward $C_\mu$.

### Other Decoherence Channels

**Depolarizing Channel**: Mixes toward the maximally mixed state.

$$\mathcal{E}_\gamma(\rho) = (1-\gamma)\rho + \gamma \frac{I}{d}$$

**Amplitude Damping**: Models energy dissipation (decay to ground state).

$$K_0 = \begin{pmatrix} 1 & 0 \\ 0 & \sqrt{1-\gamma} \end{pmatrix}, \quad K_1 = \begin{pmatrix} 0 & \sqrt{\gamma} \\ 0 & 0 \end{pmatrix}$$

For our research, dephasing is the natural choice—it directly models the loss of quantum coherence that distinguishes $C_q$ from $C_\mu$.

---

## Part 5: Measurement

### Projective Measurement

Measurement in basis $\{|m\rangle\}$ uses projectors $P_m = |m\rangle\langle m|$.

**Probability of outcome $m$**:
$$p_m = \text{Tr}(P_m \rho) = \langle m|\rho|m\rangle$$

**Post-measurement state** (if outcome is $m$):
$$\rho' = \frac{P_m \rho P_m}{\text{Tr}(P_m \rho)}$$

### Why Measurement Destroys Superposition

Before measurement: $|\psi\rangle = \alpha|0\rangle + \beta|1\rangle$

After measuring and getting outcome 0: $|\psi'\rangle = |0\rangle$

The superposition collapses. Information about $\beta$ is lost.

### Connection to Q-Machines

In the q-machine protocol:
1. System is in state $|s_j\rangle = \sum_{x,k} \sqrt{T^{(x)}_{jk}} |x\rangle|k\rangle$
2. Measure the $|x\rangle$ register → get symbol $x$ with correct probability
3. The $|k\rangle$ register collapses to indicate next causal state

This generates the correct output statistics while using less memory than classical.

---

## Part 6: Connections to Computational Mechanics

### The Core Insight

| Classical ε-Machine | Quantum q-Machine |
|--------------------|-------------------|
| Causal states are orthogonal (perfectly distinguishable) | Quantum states can overlap (partially distinguishable) |
| Must store full distinguishing information | Only stores what's needed for prediction |
| Complexity = $C_\mu = H(\mathcal{S})$ (Shannon entropy) | Complexity = $C_q = S(\rho)$ (von Neumann entropy) |

### Why Classical Wastes Information

Consider two causal states $S_j$ and $S_k$ that:
- Have **different pasts** (so classically must be distinguished)
- Can **transition to the same future state** $S_l$ on the same symbol $x$

Classically, we store complete information distinguishing $S_j$ from $S_k$. But once both transition to $S_l$, that distinguishing information is **irreversibly lost**. We stored it for nothing—it's "cryptic" information.

### Quantum Solution

Encode $S_j$ and $S_k$ as **non-orthogonal** quantum states $|s_j\rangle$ and $|s_k\rangle$ with:

$$\langle s_j|s_k\rangle \propto \sqrt{T^{(x)}_{jl} T^{(x)}_{kl}} > 0$$

The overlap is nonzero precisely because both can reach $S_l$. We only distinguish them to the degree necessary—no waste.

### The Key Inequalities

$$E \leq C_q \leq C_\mu$$

- **$E$** = Excess entropy = $I(\overleftarrow{X}; \overrightarrow{X})$ = fundamental information limit
- **$C_q$** = Quantum statistical complexity = $S(\rho)$
- **$C_\mu$** = Classical statistical complexity = $H(\mathcal{S})$

The gap $C_\mu - C_q$ is the quantum advantage.
The gap $C_\mu - E$ is the crypticity (classical waste).

When $C_q = E$, the quantum model is **ideal**—no waste at all.

### The Q-Machine Construction

Given an ε-machine with:
- States $\{S_1, \ldots, S_N\}$
- Alphabet $\Sigma = \{x_1, \ldots, x_m\}$
- Transitions $T^{(x)}_{jk} = P(S_k, x | S_j)$
- Stationary distribution $\pi$

Construct quantum signal states:

$$|s_j\rangle = \sum_{k=1}^{N} \sum_{x \in \Sigma} \sqrt{T^{(x)}_{jk}} |x\rangle \otimes |k\rangle$$

The Hilbert space dimension is $|\Sigma| \times N$.

Average density matrix:

$$\rho = \sum_{j=1}^{N} \pi_j |s_j\rangle\langle s_j|$$

Quantum complexity:

$$C_q = S(\rho) = -\text{Tr}(\rho \log_2 \rho)$$

---

## Part 7: The Perturbed Coin Example

This is the canonical example demonstrating unbounded quantum advantage.

### Setup

A coin with bias $p$ that flips with probability $p$ at each step, then is observed.

- Two causal states: $S_0$ (coin shows 0), $S_1$ (coin shows 1)
- Transitions:
  - From $S_0$: emit 0 and stay with prob $(1-p)$, emit 1 and go to $S_1$ with prob $p$
  - From $S_1$: emit 1 and stay with prob $(1-p)$, emit 0 and go to $S_0$ with prob $p$

### Classical Complexity

Stationary distribution: $\pi_0 = \pi_1 = 0.5$

$$C_\mu = -0.5 \log_2(0.5) - 0.5 \log_2(0.5) = 1 \text{ bit}$$

Always 1 bit, regardless of $p$.

### Excess Entropy

As $p \to 0.5$, the futures become nearly identical:

$$E = 1 - H_s(p)$$

where $H_s(p) = -p \log_2 p - (1-p) \log_2(1-p)$.

As $p \to 0.5$: $H_s(p) \to 1$, so $E \to 0$.

### Quantum States

$$|s_0\rangle = \sqrt{1-p}|0\rangle|0\rangle + \sqrt{p}|1\rangle|1\rangle$$
$$|s_1\rangle = \sqrt{p}|0\rangle|0\rangle + \sqrt{1-p}|1\rangle|1\rangle$$

Wait—let's redo this with the correct tensor structure. The q-machine uses $|x\rangle \otimes |k\rangle$:

$$|s_0\rangle = \sqrt{(1-p)}|0,0\rangle + \sqrt{p}|1,1\rangle$$
$$|s_1\rangle = \sqrt{p}|0,0\rangle + \sqrt{(1-p)}|1,1\rangle$$

Simplified (since we're in a 2D subspace of the 4D space):

$$|s_0\rangle = \sqrt{1-p}|a\rangle + \sqrt{p}|b\rangle$$
$$|s_1\rangle = \sqrt{p}|a\rangle + \sqrt{1-p}|b\rangle$$

where $|a\rangle = |0,0\rangle$ and $|b\rangle = |1,1\rangle$ are orthogonal.

### Overlap

$$\langle s_0|s_1\rangle = \sqrt{(1-p)p} + \sqrt{p(1-p)} = 2\sqrt{p(1-p)}$$

As $p \to 0.5$: $\langle s_0|s_1\rangle \to 1$ (states become identical!)

### Quantum Complexity

$$\rho = 0.5|s_0\rangle\langle s_0| + 0.5|s_1\rangle\langle s_1|$$

Eigenvalues:

$$\lambda_\pm = 0.5 \pm \sqrt{p(1-p)}$$

$$C_q = -\lambda_+ \log_2 \lambda_+ - \lambda_- \log_2 \lambda_-$$

### Numerical Example: $p = 0.4$

$$\sqrt{p(1-p)} = \sqrt{0.24} = 0.490$$
$$\lambda_+ = 0.990, \quad \lambda_- = 0.010$$
$$C_q = -0.990 \log_2(0.990) - 0.010 \log_2(0.010)$$
$$= 0.014 + 0.066 = 0.080 \text{ bits}$$

**Summary for $p = 0.4$**:
- Classical complexity: $C_\mu = 1$ bit
- Quantum complexity: $C_q = 0.080$ bits
- Quantum advantage: $1 - 0.080 = 0.920$ bits (92% reduction!)
- Excess entropy: $E = 1 - H_s(0.4) = 1 - 0.971 = 0.029$ bits

### The Unbounded Advantage

As $p \to 0.5$:
- $C_\mu = 1$ bit (constant)
- $C_q \to 0$ bits
- Advantage $C_\mu - C_q \to 1$ bit

More dramatically, for a lattice of $K$ independent perturbed coins:
- Classical: $K$ bits
- Quantum: $K \cdot C_q$ bits

As $p \to 0.5$, the ratio $C_\mu / C_q \to \infty$. This is **unbounded quantum advantage**.

---

## Summary: What You Need to Remember

1. **Quantum states** are vectors; **density matrices** handle mixtures
2. **Von Neumann entropy** $S(\rho) = -\text{Tr}(\rho \log \rho)$ measures quantum uncertainty
3. **Non-orthogonal states** can't be perfectly distinguished—this enables compression
4. **Dephasing** destroys coherence, increasing entropy toward classical limit
5. **Q-machines** encode causal states non-orthogonally, achieving $C_q \leq C_\mu$
6. The **perturbed coin** shows unbounded advantage as $p \to 0.5$

---

## References

1. Gu, M. et al. "Quantum mechanics can reduce the complexity of classical models." Nature Communications 3, 762 (2012)
2. Nielsen, M. A. & Chuang, I. L. *Quantum Computation and Quantum Information* (Cambridge, 2000)
3. Preskill, J. "Lecture Notes for Physics 219: Quantum Computation" (Caltech)

---

*Document version: 1.0*
*Created: 2026-01-28*
*Status: Complete*
