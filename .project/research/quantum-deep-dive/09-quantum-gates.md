# Chapter 9: Quantum Gates

*Unitary transformations on the Bloch sphere and beyond*

---

## Computation as Transformation

Classical computation transforms bit strings: $f: \{0,1\}^n \to \{0,1\}^m$.

Quantum computation transforms quantum states: $U: \mathcal{H} \to \mathcal{H}$.

The key constraint: quantum evolution must be **unitary**—reversible and norm-preserving.

---

## Unitary Matrices

A matrix $U$ is unitary if:

$$U^\dagger U = U U^\dagger = I$$

Properties:
- **Reversible**: $U^{-1} = U^\dagger$
- **Preserves inner products**: $\langle U\psi | U\phi \rangle = \langle \psi | \phi \rangle$
- **Preserves norm**: $\|U|\psi\rangle\| = \||\psi\rangle\|$
- **Eigenvalues on unit circle**: $|\lambda| = 1$

Evolution of density matrices:

$$\rho \to U\rho U^\dagger$$

---

## Single-Qubit Gates

### The Pauli Gates

$$X = \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}, \quad Y = \begin{pmatrix} 0 & -i \\ i & 0 \end{pmatrix}, \quad Z = \begin{pmatrix} 1 & 0 \\ 0 & -1 \end{pmatrix}$$

- **X (NOT)**: Flips $|0\rangle \leftrightarrow |1\rangle$. Rotation by $\pi$ around X-axis.
- **Y**: Rotation by $\pi$ around Y-axis.
- **Z**: Phase flip. $|0\rangle \to |0\rangle$, $|1\rangle \to -|1\rangle$. Rotation by $\pi$ around Z-axis.

### Hadamard Gate

$$H = \frac{1}{\sqrt{2}}\begin{pmatrix} 1 & 1 \\ 1 & -1 \end{pmatrix}$$

Creates superposition:
- $H|0\rangle = |+\rangle = \frac{1}{\sqrt{2}}(|0\rangle + |1\rangle)$
- $H|1\rangle = |-\rangle = \frac{1}{\sqrt{2}}(|0\rangle - |1\rangle)$

Rotation by $\pi$ around the axis halfway between X and Z.

### Phase Gates

$$S = \begin{pmatrix} 1 & 0 \\ 0 & i \end{pmatrix}, \quad T = \begin{pmatrix} 1 & 0 \\ 0 & e^{i\pi/4} \end{pmatrix}$$

Add phase to $|1\rangle$. S is "quarter turn," T is "eighth turn."

### General Rotation

Any single-qubit gate can be written as:

$$U(\theta, \phi, \lambda) = \begin{pmatrix} \cos(\theta/2) & -e^{i\lambda}\sin(\theta/2) \\ e^{i\phi}\sin(\theta/2) & e^{i(\phi+\lambda)}\cos(\theta/2) \end{pmatrix}$$

This parameterizes all of SU(2).

---

## The Bloch Sphere Picture

Single-qubit gates are rotations of the Bloch sphere.

A rotation by angle $\theta$ around axis $\hat{n} = (n_x, n_y, n_z)$:

$$R_{\hat{n}}(\theta) = \cos(\theta/2)I - i\sin(\theta/2)(n_x X + n_y Y + n_z Z)$$

- X gate: $R_X(\pi)$
- Y gate: $R_Y(\pi)$
- Z gate: $R_Z(\pi)$
- Hadamard: Rotation by $\pi$ around $(\hat{x} + \hat{z})/\sqrt{2}$

---

## Two-Qubit Gates

### CNOT (Controlled-NOT)

$$\text{CNOT} = \begin{pmatrix} 1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 0 & 1 \\ 0 & 0 & 1 & 0 \end{pmatrix}$$

If control qubit is $|1\rangle$, flip target qubit.

$$|00\rangle \to |00\rangle, \quad |01\rangle \to |01\rangle, \quad |10\rangle \to |11\rangle, \quad |11\rangle \to |10\rangle$$

**Creates entanglement**: $\text{CNOT}(H \otimes I)|00\rangle = \frac{1}{\sqrt{2}}(|00\rangle + |11\rangle)$

### Controlled-Z (CZ)

$$\text{CZ} = \begin{pmatrix} 1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & -1 \end{pmatrix}$$

Applies Z to target if control is $|1\rangle$. Symmetric under qubit exchange.

### SWAP

$$\text{SWAP} = \begin{pmatrix} 1 & 0 & 0 & 0 \\ 0 & 0 & 1 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 0 & 1 \end{pmatrix}$$

Exchanges two qubits: $|01\rangle \leftrightarrow |10\rangle$.

---

## Universal Gate Sets

A set of gates is **universal** if any unitary can be approximated to arbitrary precision by compositions of gates from the set.

Examples:
- $\{H, T, \text{CNOT}\}$
- $\{H, \text{Toffoli}\}$ (Toffoli = controlled-controlled-NOT)
- Any single-qubit rotation + any entangling two-qubit gate

The Solovay-Kitaev theorem: any gate can be approximated with $O(\log^c(1/\epsilon))$ gates from a universal set.

---

## Quantum Circuits

Quantum algorithms are expressed as **circuits**—sequences of gates applied to qubits.

```
|0⟩ ─── H ───●─── M
             │
|0⟩ ─────────X─── M
```

This circuit:
1. Applies H to qubit 1: $|00\rangle \to |+0\rangle = \frac{1}{\sqrt{2}}(|00\rangle + |10\rangle)$
2. Applies CNOT: $\frac{1}{\sqrt{2}}(|00\rangle + |11\rangle) = |\Phi^+\rangle$
3. Measures both qubits

Result: Bell state creation and measurement.

---

## Gates vs Channels

**Gates** (unitary) are reversible and preserve purity:
$$\rho \to U\rho U^\dagger$$

**Channels** (CPTP maps) include noise and measurement:
$$\rho \to \sum_k K_k \rho K_k^\dagger$$

Real quantum computers apply noisy channels, not perfect gates. The challenge is to compute despite noise.

---

## Connection to Computational Mechanics

In computational mechanics, we don't usually think of "gates" because we're analyzing processes, not designing algorithms.

But there's a connection:

**Transition operators**: The ε-machine evolves by transition matrices. The q-machine evolves by unitary operators (for the coherent part) plus measurements (for the output).

**Quantum simulation**: To simulate a stochastic process on a quantum computer, you'd implement the q-machine as a circuit.

**Complexity of simulation**: The quantum complexity $C_q$ relates to how much "quantum memory" (qubits) you need to simulate the process.

---

## Key Takeaway

> **Quantum gates are unitary transformations—reversible, norm-preserving operations.**
>
> - Single-qubit gates: rotations on the Bloch sphere (X, Y, Z, H, S, T)
> - Two-qubit gates: create entanglement (CNOT, CZ)
> - Universal sets: can approximate any unitary
>
> Quantum circuits compose gates to implement algorithms.

---

## Common Misconceptions

### "Quantum gates are like classical logic gates"

Partially. Some (like CNOT) have classical analogs. But quantum gates are always reversible, and they operate on superpositions, not just basis states.

### "You need many types of gates"

Any universal set suffices. {H, T, CNOT} can build everything (approximately).

### "Gates are instantaneous"

In real hardware, gates take time and have errors. Gate fidelity and gate time are key metrics.

### "Measurement is a gate"

Measurement is not unitary—it's irreversible and collapses superpositions. It's a different kind of operation.

---

## Code Example

```python
import numpy as np

# Pauli gates
I = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)

# Hadamard
H = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)

# Phase gates
S = np.array([[1, 0], [0, 1j]], dtype=complex)
T = np.array([[1, 0], [0, np.exp(1j * np.pi / 4)]], dtype=complex)

# CNOT (control=first qubit)
CNOT = np.array([
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 0, 1],
    [0, 0, 1, 0]
], dtype=complex)

def apply_gate(gate, state):
    """Apply a gate to a state vector."""
    return gate @ state

def tensor_product(A, B):
    return np.kron(A, B)

# Create Bell state
ket_0 = np.array([1, 0], dtype=complex)
ket_00 = tensor_product(ket_0, ket_0)

# Step 1: H on first qubit
state = tensor_product(H @ ket_0, ket_0)
print("After H ⊗ I:")
print(f"  State: {state}")

# Step 2: CNOT
state = CNOT @ state
print("\nAfter CNOT:")
print(f"  State: {state}")
print("  This is |Φ+⟩ = (|00⟩ + |11⟩)/√2!")

# Verify it's entangled
rho = np.outer(state, np.conj(state))
rho_A = rho[:2, :2] + rho[2:4, 2:4]  # Simplified partial trace
print(f"\nReduced ρ_A:\n{rho_A}")
print("Maximally mixed → maximally entangled!")
```

---

## What's Next

In [Chapter 10: Interference as Computation](10-interference.md), we'll see how quantum algorithms exploit interference—the core trick that makes quantum computers powerful.

---

*[← Previous: Decoherence](08-decoherence.md) | [Back to Overview](00-overview.md) | [Next: Interference as Computation →](10-interference.md)*
