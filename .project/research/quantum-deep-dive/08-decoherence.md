# Chapter 8: Decoherence

*How quantum becomes classical*

---

## The Central Question

We've built up quantum mechanics: superposition, density matrices, entanglement. But the classical world doesn't look quantum. Cats don't appear in superpositions. Pointers point to definite positions.

How does the classical world emerge from quantum mechanics?

The answer is **decoherence**—the destruction of quantum coherence through interaction with the environment.

---

## The Mechanism

Here's the core idea:

1. A quantum system interacts with its environment
2. The environment "learns" which state the system is in
3. This creates entanglement between system and environment
4. Tracing out the environment kills the system's off-diagonals

**Result**: The system's density matrix becomes (approximately) diagonal in some preferred basis. Classical behavior emerges.

---

## A Simple Model

Consider a qubit (system S) interacting with an environment (E).

Initial state: system in superposition, environment in a reference state:
$$|\Psi_0\rangle = (\alpha|0\rangle_S + \beta|1\rangle_S) \otimes |E_0\rangle$$

After interaction, the environment becomes correlated with the system:
$$|\Psi\rangle = \alpha|0\rangle_S|E_0\rangle + \beta|1\rangle_S|E_1\rangle$$

where $|E_0\rangle$ and $|E_1\rangle$ are different environment states.

The total state is pure, but the system's reduced state:
$$\rho_S = \text{Tr}_E(|\Psi\rangle\langle\Psi|)$$

If $\langle E_0|E_1\rangle = 0$ (environment states orthogonal):
$$\rho_S = |\alpha|^2|0\rangle\langle 0| + |\beta|^2|1\rangle\langle 1|$$

**Perfectly diagonal!** The off-diagonals vanished.

If $\langle E_0|E_1\rangle = r$ (partial overlap):
$$\rho_S = \begin{pmatrix} |\alpha|^2 & \alpha\beta^* r \\ \alpha^*\beta r^* & |\beta|^2 \end{pmatrix}$$

Off-diagonals reduced by factor $|r|$.

---

## The Decoherence Timescale

In real systems, the environment consists of many degrees of freedom (photons, phonons, molecules). The overlap $\langle E_0|E_1\rangle$ decreases exponentially fast:

$$\langle E_0(t)|E_1(t)\rangle \approx e^{-t/\tau_D}$$

where $\tau_D$ is the **decoherence time**.

For macroscopic objects at room temperature, $\tau_D$ is incredibly short—femtoseconds or less. Superpositions decohere before we can observe them.

For isolated atoms in vacuum, $\tau_D$ can be seconds or longer—long enough for quantum experiments.

---

## Quantum Channels: The Mathematical Description

Decoherence is described by **quantum channels**—completely positive trace-preserving (CPTP) maps.

The Kraus representation:
$$\mathcal{E}(\rho) = \sum_k K_k \rho K_k^\dagger$$

where $\sum_k K_k^\dagger K_k = I$.

### The Dephasing Channel

The simplest decoherence model:

$$\mathcal{E}_\gamma(\rho) = (1-\gamma)\rho + \gamma Z\rho Z$$

where $Z = \begin{pmatrix} 1 & 0 \\ 0 & -1 \end{pmatrix}$ is the Pauli Z matrix and $\gamma \in [0, 1/2]$.

Effect on off-diagonals:
$$\rho_{01} \to (1-2\gamma)\rho_{01}$$

With $\gamma = 1/2$, off-diagonals vanish completely.

### Equivalent Form

$$\mathcal{E}_\gamma(\rho) = \begin{pmatrix} \rho_{00} & (1-2\gamma)\rho_{01} \\ (1-2\gamma)\rho_{10} & \rho_{11} \end{pmatrix}$$

Diagonals unchanged, off-diagonals suppressed.

---

## Other Decoherence Channels

### Amplitude Damping

Models energy loss (e.g., photon emission):
$$K_0 = \begin{pmatrix} 1 & 0 \\ 0 & \sqrt{1-\gamma} \end{pmatrix}, \quad K_1 = \begin{pmatrix} 0 & \sqrt{\gamma} \\ 0 & 0 \end{pmatrix}$$

Drives the system toward $|0\rangle$ while also killing coherence.

### Depolarizing Channel

Complete randomization with probability $p$:
$$\mathcal{E}_p(\rho) = (1-p)\rho + \frac{p}{3}(X\rho X + Y\rho Y + Z\rho Z)$$

Shrinks the Bloch vector uniformly toward the center.

### Generalized Dephasing

For d-dimensional systems:
$$\mathcal{E}_\gamma(\rho) = (1-\gamma)\rho + \gamma \sum_i |i\rangle\langle i|\rho|i\rangle\langle i|$$

Extracts diagonal with probability $\gamma$.

---

## Pointer Basis: Which States Are Classical?

Decoherence picks out a **preferred basis**—the states that don't decohere.

These are eigenstates of the system-environment interaction. For a position-dependent interaction, the pointer basis is position. For spin-magnetic field interaction, it's spin along the field.

The environment "monitors" the system in this basis, creating records.

This explains why we see particles with definite positions (not momentum superpositions): the environment couples to position.

---

## Decoherence vs Measurement

Decoherence looks like measurement:
- Both kill off-diagonals
- Both produce classical-looking states

But there are differences:
- Measurement gives a definite outcome (we learn it)
- Decoherence creates a mixed state (we don't learn which branch)

Decoherence explains **why** measurement produces classical outcomes—the apparatus is a complex environment that decoheres the measured system.

---

## Connection to Computational Mechanics

Here's where it all comes together.

**Quantum advantage via coherence**: The q-machine achieves $C_q < C_\mu$ because signal states overlap (off-diagonals in $\rho$).

**Decoherence destroys advantage**: As $\rho$ dephases, off-diagonals shrink, eigenvalues spread, entropy increases toward $C_\mu$.

**The decoherence trajectory**: Track $C_q(\gamma)$ as dephasing strength increases from 0 to 1. This shows how quantum advantage dissolves.

In our investigations, we found:
- Trajectories are **concave** for states with quantum advantage
- At $\gamma = 1$, the state is classical and $C_q = C_\mu$
- The rate of entropy increase depends on signal state overlap

This connects fundamental physics (decoherence) to information theory (complexity measures).

---

## The Environment as Witness

A deep insight from decoherence theory: the environment acts as a **witness** or **record** of the system state.

When the system is in $|0\rangle$, the environment evolves to $|E_0\rangle$.
When it's in $|1\rangle$, the environment evolves to $|E_1\rangle$.

The environment has "measured" the system—there are now records everywhere.

This is why quantum effects are fragile: they require isolation from everything.

---

## Quantum Darwinism

A related idea: **quantum Darwinism** (Zurek).

The environment doesn't just record the system state once—many independent fragments of the environment record it.

This proliferation of records is why classical information is objective—many observers can independently verify it.

Quantum information is fragile precisely because it hasn't been copied to the environment.

---

## Key Takeaway

> **Decoherence is entanglement with the environment, traced out.**
>
> - System-environment interaction creates entanglement
> - Tracing out the environment kills system's off-diagonals
> - The system becomes classical (in the pointer basis)
> - Decoherence time $\tau_D$ is very short for macroscopic objects
>
> This is the quantum-to-classical transition. It's not mysterious—it's partial trace.
>
> For computational mechanics: decoherence destroys quantum advantage by eliminating the coherences that enable $C_q < C_\mu$.

---

## Common Misconceptions

### "Decoherence solves the measurement problem"

It explains why we don't see macroscopic superpositions, but it doesn't explain why we get one definite outcome rather than another. That's the residual measurement problem.

### "Decoherence is dissipation"

Related but distinct. Dissipation involves energy loss. Decoherence can happen without energy loss (pure dephasing). Both involve environment interaction.

### "Decoherence is irreversible"

In principle, it's reversible—the total system+environment state is still pure. In practice, the environment has too many degrees of freedom to track.

### "Quantum computers need zero decoherence"

They need decoherence times much longer than gate times. Quantum error correction can fight decoherence to some extent.

### "Classical physics is fundamental"

No—classical physics emerges from quantum mechanics via decoherence. Quantum mechanics is more fundamental.

---

## Code Example

```python
import numpy as np

def dephasing_channel(rho, gamma):
    """
    Apply dephasing channel with strength gamma ∈ [0, 1].
    gamma = 0: no decoherence
    gamma = 1: complete decoherence (fully diagonal)
    """
    diagonal = np.diag(np.diag(rho))
    return (1 - gamma) * rho + gamma * diagonal

def von_neumann_entropy(rho):
    eigenvalues = np.linalg.eigvalsh(rho)
    eigenvalues = eigenvalues[eigenvalues > 1e-10]
    return -np.sum(eigenvalues * np.log2(eigenvalues))

# Start with a pure superposition
psi = np.array([1, 1], dtype=complex) / np.sqrt(2)
rho_0 = np.outer(psi, np.conj(psi))

print("Decoherence trajectory:")
print("=" * 50)
print(f"{'γ':<8} {'ρ_01':<15} {'Entropy (bits)':<15}")
print("-" * 50)

for gamma in [0.0, 0.25, 0.5, 0.75, 1.0]:
    rho = dephasing_channel(rho_0, gamma)
    S = von_neumann_entropy(rho)
    print(f"{gamma:<8.2f} {rho[0,1].real:<15.3f} {S:<15.3f}")

print("\nAs γ increases:")
print("  - Off-diagonals shrink to zero")
print("  - Entropy increases from 0 to 1 bit")
print("  - Quantum → Classical")

# Quantum advantage example
print("\n" + "=" * 50)
print("Quantum advantage under decoherence:")
print("=" * 50)

# Perturbed coin signal states
p = 0.3
s0 = np.array([np.sqrt(1-p), np.sqrt(p)])
s1 = np.array([np.sqrt(p), np.sqrt(1-p)])
rho_q = 0.5 * np.outer(s0, s0) + 0.5 * np.outer(s1, s1)

C_mu = 1.0  # Classical complexity

print(f"{'γ':<8} {'C_q':<12} {'C_μ':<12} {'Advantage':<12}")
print("-" * 50)

for gamma in [0.0, 0.25, 0.5, 0.75, 1.0]:
    rho = dephasing_channel(rho_q, gamma)
    C_q = von_neumann_entropy(rho)
    advantage = C_mu - C_q
    print(f"{gamma:<8.2f} {C_q:<12.3f} {C_mu:<12.3f} {advantage:<12.3f}")

print("\nDecoherence destroys quantum advantage!")
```

---

## What's Next

We've now completed **Part II: Core Concepts**. You understand:
- Measurement (forcing diagonality)
- Composite systems (tensor products)
- Entanglement (non-factorizable states)
- Decoherence (environment-induced classicality)

In **Part III: Computation**, we'll see how these concepts enable quantum algorithms:
- [Chapter 9: Quantum Gates](09-quantum-gates.md) — Unitary transformations
- [Chapter 10: Interference as Computation](10-interference.md) — The core trick
- [Chapter 11: Quantum Algorithms](11-algorithms.md) — Deutsch-Jozsa, Grover, Shor
- [Chapter 12: Why Quantum Speedup?](12-why-speedup.md) — When it helps

---

*[← Previous: Entanglement](07-entanglement.md) | [Back to Overview](00-overview.md) | [Next: Quantum Gates →](09-quantum-gates.md)*
