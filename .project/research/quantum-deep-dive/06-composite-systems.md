# Chapter 6: Composite Systems

*When dimensions multiply*

---

## The Setup

So far we've dealt with single quantum systems. Now we need to describe multiple systems together.

This is where quantum mechanics departs most dramatically from classical physics—and where entanglement lurks.

---

## Classical Composition

Classically, combining two systems is simple:

- System A has states $\{a_1, a_2, \ldots, a_n\}$
- System B has states $\{b_1, b_2, \ldots, b_m\}$
- Combined system has states $\{(a_i, b_j)\}$ — all pairs

The joint probability distribution is a table with $n \times m$ entries.

If the systems are independent: $P(a_i, b_j) = P(a_i) P(b_j)$.

---

## Quantum Composition: Tensor Products

In quantum mechanics, we use the **tensor product** $\otimes$:

$$\mathcal{H}_{AB} = \mathcal{H}_A \otimes \mathcal{H}_B$$

If $\mathcal{H}_A$ has dimension $d_A$ and $\mathcal{H}_B$ has dimension $d_B$, then:

$$\dim(\mathcal{H}_{AB}) = d_A \times d_B$$

### Basis States

If $\{|i\rangle_A\}$ is a basis for A and $\{|j\rangle_B\}$ is a basis for B, then:

$$\{|i\rangle_A \otimes |j\rangle_B\} = \{|i,j\rangle\} = \{|ij\rangle\}$$

is a basis for AB.

For two qubits: basis is $\{|00\rangle, |01\rangle, |10\rangle, |11\rangle\}$ — four states.

---

## Tensor Product: Explicit Construction

For vectors:

$$|a\rangle \otimes |b\rangle = \begin{pmatrix} a_1 \\ a_2 \end{pmatrix} \otimes \begin{pmatrix} b_1 \\ b_2 \end{pmatrix} = \begin{pmatrix} a_1 b_1 \\ a_1 b_2 \\ a_2 b_1 \\ a_2 b_2 \end{pmatrix}$$

For matrices:

$$A \otimes B = \begin{pmatrix} A_{11} B & A_{12} B \\ A_{21} B & A_{22} B \end{pmatrix}$$

This is the **Kronecker product**—each element of A multiplies the entire matrix B.

### Worked Example: Two Qubits

$$|0\rangle \otimes |0\rangle = \begin{pmatrix} 1 \\ 0 \end{pmatrix} \otimes \begin{pmatrix} 1 \\ 0 \end{pmatrix} = \begin{pmatrix} 1 \\ 0 \\ 0 \\ 0 \end{pmatrix} = |00\rangle$$

$$|0\rangle \otimes |1\rangle = \begin{pmatrix} 1 \\ 0 \end{pmatrix} \otimes \begin{pmatrix} 0 \\ 1 \end{pmatrix} = \begin{pmatrix} 0 \\ 1 \\ 0 \\ 0 \end{pmatrix} = |01\rangle$$

---

## Product States

A **product state** (also called separable pure state) has the form:

$$|\psi_{AB}\rangle = |\psi_A\rangle \otimes |\psi_B\rangle$$

The density matrix:

$$\rho_{AB} = \rho_A \otimes \rho_B$$

This represents two independent systems. Measuring A tells you nothing about B.

### Example: Independent Qubits

Qubit A in $|+\rangle = \frac{1}{\sqrt{2}}(|0\rangle + |1\rangle)$
Qubit B in $|0\rangle$

$$|\psi_{AB}\rangle = |+\rangle \otimes |0\rangle = \frac{1}{\sqrt{2}}(|00\rangle + |10\rangle)$$

Measuring A gives 0 or 1 with 50% each.
Measuring B always gives 0.
The outcomes are uncorrelated.

---

## Non-Product States: A Glimpse of Entanglement

Consider:

$$|\Phi^+\rangle = \frac{1}{\sqrt{2}}(|00\rangle + |11\rangle)$$

Can this be written as $|\psi_A\rangle \otimes |\psi_B\rangle$?

Let's try: if $|\psi_A\rangle = \alpha|0\rangle + \beta|1\rangle$ and $|\psi_B\rangle = \gamma|0\rangle + \delta|1\rangle$, then:

$$|\psi_A\rangle \otimes |\psi_B\rangle = \alpha\gamma|00\rangle + \alpha\delta|01\rangle + \beta\gamma|10\rangle + \beta\delta|11\rangle$$

For this to equal $|\Phi^+\rangle$, we need:
- $\alpha\gamma = \frac{1}{\sqrt{2}}$
- $\alpha\delta = 0$
- $\beta\gamma = 0$
- $\beta\delta = \frac{1}{\sqrt{2}}$

From $\alpha\delta = 0$: either $\alpha = 0$ or $\delta = 0$.
But if $\alpha = 0$, then $\alpha\gamma = 0 \neq \frac{1}{\sqrt{2}}$.
If $\delta = 0$, then $\beta\delta = 0 \neq \frac{1}{\sqrt{2}}$.

**Contradiction!** The state $|\Phi^+\rangle$ cannot be factored.

This is **entanglement**—we'll explore it fully in Chapter 7.

---

## Density Matrices for Composite Systems

A general two-system density matrix is a $d_A d_B \times d_A d_B$ matrix.

For two qubits, this is a $4 \times 4$ matrix in the basis $\{|00\rangle, |01\rangle, |10\rangle, |11\rangle\}$.

### Product State Density Matrix

$$\rho_A \otimes \rho_B = \begin{pmatrix} \rho_A^{11} \rho_B & \rho_A^{12} \rho_B \\ \rho_A^{21} \rho_B & \rho_A^{22} \rho_B \end{pmatrix}$$

### Example

If $\rho_A = |+\rangle\langle +| = \frac{1}{2}\begin{pmatrix} 1 & 1 \\ 1 & 1 \end{pmatrix}$ and $\rho_B = |0\rangle\langle 0| = \begin{pmatrix} 1 & 0 \\ 0 & 0 \end{pmatrix}$:

$$\rho_{AB} = \rho_A \otimes \rho_B = \frac{1}{2}\begin{pmatrix} 1 & 0 & 1 & 0 \\ 0 & 0 & 0 & 0 \\ 1 & 0 & 1 & 0 \\ 0 & 0 & 0 & 0 \end{pmatrix}$$

---

## The Partial Trace: Ignoring a Subsystem

Given $\rho_{AB}$, what if we only care about system A?

The **partial trace** extracts the reduced density matrix:

$$\rho_A = \text{Tr}_B(\rho_{AB}) = \sum_j \langle j|_B \rho_{AB} |j\rangle_B$$

This "traces out" system B.

### Why Partial Trace?

The partial trace ensures that all predictions for system A alone are consistent:

$$\langle O_A \rangle = \text{Tr}(O_A \otimes I_B \cdot \rho_{AB}) = \text{Tr}(O_A \cdot \rho_A)$$

Any observable on A gives the same expectation value whether we use $\rho_{AB}$ or $\rho_A$.

### Worked Example: Tracing Out One Qubit

Start with $|\Phi^+\rangle = \frac{1}{\sqrt{2}}(|00\rangle + |11\rangle)$:

$$\rho_{AB} = |\Phi^+\rangle\langle\Phi^+| = \frac{1}{2}\begin{pmatrix} 1 & 0 & 0 & 1 \\ 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 \\ 1 & 0 & 0 & 1 \end{pmatrix}$$

Trace out B:

$$\rho_A = \text{Tr}_B(\rho_{AB}) = \langle 0|_B \rho_{AB} |0\rangle_B + \langle 1|_B \rho_{AB} |1\rangle_B$$

After calculation:

$$\rho_A = \frac{1}{2}\begin{pmatrix} 1 & 0 \\ 0 & 1 \end{pmatrix} = \frac{I}{2}$$

**Remarkable!** The global state is pure ($|\Phi^+\rangle$), but the local state of A is maximally mixed!

This is the signature of entanglement: local uncertainty despite global purity.

---

## Connection to Computational Mechanics

In computational mechanics, we often deal with composite systems:

**Symbol × State Index**: The q-machine state lives in a tensor product:

$$|s_j\rangle = \sum_x T_{xj} |x\rangle \otimes |j\rangle$$

where $|x\rangle$ is a symbol and $|j\rangle$ is a causal state index.

**Past × Future**: Mutual information $I(\overleftarrow{X}; \overrightarrow{X})$ involves the joint distribution of past and future—a composite system.

The tensor product structure is fundamental to understanding how information flows between past and future.

---

## Key Takeaway

> **Composite systems live in tensor product spaces.**
>
> - Dimensions multiply: $d_{AB} = d_A \times d_B$
> - Product states factor: $|\psi_{AB}\rangle = |\psi_A\rangle \otimes |\psi_B\rangle$
> - Non-product states are entangled
> - Partial trace extracts subsystem descriptions
>
> Entanglement creates local uncertainty from global purity—a purely quantum phenomenon.

---

## Common Misconceptions

### "Tensor product is just Cartesian product"

Similar idea, but tensor products have more structure. The coefficients can create superpositions that can't be factored—that's entanglement.

### "A mixed local state means the global state is mixed"

No! A pure entangled state has pure global density matrix but mixed reduced density matrices. Purity is not preserved under partial trace.

### "Two qubits means twice the information"

Actually, two qubits can store more than twice the information in some senses (superdense coding). The tensor product structure enables non-classical correlations.

### "The partial trace loses information"

It loses information about correlations with the traced-out system. This is physical—if you don't have access to B, you genuinely can't know about A-B correlations.

---

## Code Example

```python
import numpy as np

def tensor_product(A, B):
    """Tensor (Kronecker) product of two matrices or vectors."""
    return np.kron(A, B)

def partial_trace_B(rho_AB, dim_A, dim_B):
    """Trace out system B from a composite density matrix."""
    rho_A = np.zeros((dim_A, dim_A), dtype=complex)
    for j in range(dim_B):
        # Project onto |j⟩_B
        proj = np.zeros((dim_B, 1))
        proj[j] = 1
        # ⟨j|_B ρ_AB |j⟩_B
        operator = tensor_product(np.eye(dim_A), proj.T)
        rho_A += operator @ rho_AB @ operator.conj().T
    return rho_A

# Two qubit basis states
ket_0 = np.array([[1], [0]])
ket_1 = np.array([[0], [1]])

# Product state: |+⟩ ⊗ |0⟩
ket_plus = (ket_0 + ket_1) / np.sqrt(2)
psi_product = tensor_product(ket_plus, ket_0)
rho_product = psi_product @ psi_product.conj().T

print("Product state |+⟩ ⊗ |0⟩:")
print(f"ρ_AB =\n{np.round(rho_product.real, 3)}")
rho_A = partial_trace_B(rho_product, 2, 2)
print(f"ρ_A (after tracing out B) =\n{np.round(rho_A, 3)}")

# Entangled state: (|00⟩ + |11⟩)/√2
ket_00 = tensor_product(ket_0, ket_0)
ket_11 = tensor_product(ket_1, ket_1)
psi_bell = (ket_00 + ket_11) / np.sqrt(2)
rho_bell = psi_bell @ psi_bell.conj().T

print("\nEntangled state (|00⟩ + |11⟩)/√2:")
print(f"ρ_AB =\n{np.round(rho_bell.real, 3)}")
rho_A_bell = partial_trace_B(rho_bell, 2, 2)
print(f"ρ_A (after tracing out B) =\n{np.round(rho_A_bell, 3)}")
print("→ Maximally mixed! Pure global state, mixed local state.")
```

---

## What's Next

In [Chapter 7: Entanglement](07-entanglement.md), we'll dive deep into the states that can't be factored—and see why they're so central to quantum information.

---

*[← Previous: Measurement](05-measurement.md) | [Back to Overview](00-overview.md) | [Next: Entanglement →](07-entanglement.md)*
