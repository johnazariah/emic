# Chapter 7: Entanglement

*States that can't be factored*

---

## The Central Mystery

Entanglement is often called the most non-classical feature of quantum mechanics. Einstein famously dismissed it as "spooky action at a distance."

But there's nothing spooky about it once you understand: **entanglement is simply correlation that can't be explained classically**.

---

## Definition

A pure state $|\psi_{AB}\rangle$ is **entangled** if it cannot be written as a product:

$$|\psi_{AB}\rangle \neq |\psi_A\rangle \otimes |\psi_B\rangle$$

for any choice of $|\psi_A\rangle$ and $|\psi_B\rangle$.

For mixed states, the definition is more subtle: $\rho_{AB}$ is **separable** if it can be written as:

$$\rho_{AB} = \sum_i p_i \rho_A^{(i)} \otimes \rho_B^{(i)}$$

Otherwise it's entangled.

---

## The Bell States

The four maximally entangled two-qubit states:

$$|\Phi^+\rangle = \frac{1}{\sqrt{2}}(|00\rangle + |11\rangle)$$
$$|\Phi^-\rangle = \frac{1}{\sqrt{2}}(|00\rangle - |11\rangle)$$
$$|\Psi^+\rangle = \frac{1}{\sqrt{2}}(|01\rangle + |10\rangle)$$
$$|\Psi^-\rangle = \frac{1}{\sqrt{2}}(|01\rangle - |10\rangle)$$

These are orthonormal and form a basis for the two-qubit Hilbert space.

They're "maximally entangled" because their reduced density matrices are maximally mixed:

$$\rho_A = \rho_B = \frac{I}{2}$$

Maximum local uncertainty, perfect global purity.

---

## Perfect Correlations

Consider $|\Phi^+\rangle = \frac{1}{\sqrt{2}}(|00\rangle + |11\rangle)$.

If Alice measures her qubit in the $\{|0\rangle, |1\rangle\}$ basis:
- 50% probability of 0, then Bob's qubit is $|0\rangle$
- 50% probability of 1, then Bob's qubit is $|1\rangle$

The outcomes are **perfectly correlated**—if Alice gets 0, Bob gets 0 with certainty.

But neither outcome was predetermined! Before measurement, the joint state was genuinely indefinite.

This is what Einstein found troubling: how can Bob's state "know" what Alice measured?

---

## The Resolution: No Signaling

The correlation is real, but it cannot be used to send information.

From Bob's perspective, before he learns Alice's result:
$$\rho_B = \text{Tr}_A(|\Phi^+\rangle\langle\Phi^+|) = \frac{I}{2}$$

His qubit is maximally mixed—completely random. He can't tell whether Alice has measured or what she got.

Only when Alice and Bob **compare results** (through classical communication) do they discover the correlation.

This is the **no-signaling theorem**: entanglement cannot transmit information faster than light.

---

## Quantifying Entanglement: Entropy of Entanglement

For a pure bipartite state $|\psi_{AB}\rangle$, the **entropy of entanglement** is:

$$E(|\psi_{AB}\rangle) = S(\rho_A) = S(\rho_B)$$

The von Neumann entropy of either reduced density matrix.

Properties:
- $E = 0$ for product states (no entanglement)
- $E = \log_2 d$ for maximally entangled states (dimension $d$)
- For two qubits: $E_{\max} = 1$ bit (the Bell states)

---

## Schmidt Decomposition

Any pure bipartite state can be written as:

$$|\psi_{AB}\rangle = \sum_i \sqrt{\lambda_i} |u_i\rangle_A \otimes |v_i\rangle_B$$

where:
- $\{|u_i\rangle\}$ and $\{|v_i\rangle\}$ are orthonormal bases
- $\lambda_i \geq 0$ are the **Schmidt coefficients**
- The number of nonzero $\lambda_i$ is the **Schmidt rank**

The state is entangled if and only if Schmidt rank > 1.

### Connection to Singular Value Decomposition

Write $|\psi_{AB}\rangle$ as a matrix $M_{ij}$ where $|\psi\rangle = \sum_{ij} M_{ij} |i\rangle_A |j\rangle_B$.

The Schmidt decomposition is just the SVD of M!

The Schmidt coefficients $\sqrt{\lambda_i}$ are the singular values.

---

## Worked Example: Schmidt Decomposition

$$|\Phi^+\rangle = \frac{1}{\sqrt{2}}(|00\rangle + |11\rangle)$$

Already in Schmidt form with:
- $\sqrt{\lambda_1} = \sqrt{\lambda_2} = \frac{1}{\sqrt{2}}$
- $|u_1\rangle = |0\rangle$, $|u_2\rangle = |1\rangle$
- $|v_1\rangle = |0\rangle$, $|v_2\rangle = |1\rangle$

Schmidt rank = 2 → entangled.

Entropy of entanglement:
$$E = -\frac{1}{2}\log_2\frac{1}{2} - \frac{1}{2}\log_2\frac{1}{2} = 1 \text{ bit}$$

Maximally entangled for two qubits.

---

## Monogamy of Entanglement

A key property: **entanglement is monogamous**.

If A is maximally entangled with B, then A cannot be entangled with any third party C.

More precisely, for qubits:
$$E_{A|BC}^2 \geq E_{AB}^2 + E_{AC}^2$$

If $E_{AB} = 1$ (maximum), then $E_{AC} = 0$.

This has profound implications:
- Entanglement is a limited resource
- Quantum cryptography exploits this (eavesdropper detection)
- Tensor networks in many-body physics respect this

---

## Entanglement and Correlation

Classical correlations can be strong too. What makes entanglement special?

**Bell inequalities** provide the answer. Classical correlations (even with hidden variables) satisfy certain bounds. Quantum entanglement violates them.

The CHSH inequality: for classical correlations,
$$|E(a,b) - E(a,b') + E(a',b) + E(a',b')| \leq 2$$

Quantum mechanics allows up to $2\sqrt{2} \approx 2.83$.

This violation has been experimentally confirmed—nature is non-classical.

---

## Connection to Computational Mechanics

In quantum computational mechanics:

**The q-machine state is entangled**: The quantum causal state $|s_j\rangle = \sum_x T_{xj} |x\rangle |j\rangle$ lives in a tensor product of symbol space and state index space. In general, this is entangled.

**Retrodiction uses entanglement**: The time-reversed machine creates correlations between past and future that are fundamentally quantum.

**Excess entropy and entanglement**: The classical excess entropy $E = I(\overleftarrow{X}; \overrightarrow{X})$ measures mutual information between past and future. There's a quantum analog involving entanglement entropy.

The overlap between causal states—which creates quantum advantage—is intimately related to how the states are "pre-entangled" with future outputs.

---

## Key Takeaway

> **Entanglement is correlation without classical explanation.**
>
> - States that can't be factored as $|\psi_A\rangle \otimes |\psi_B\rangle$
> - Local uncertainty despite global purity: $\rho_A = I/d$ for maximally entangled states
> - Quantified by entropy of entanglement: $E = S(\rho_A)$
> - Monogamous: can't share entanglement with multiple parties
> - Violates Bell inequalities: genuinely non-classical
>
> Entanglement is a resource, not a bug.

---

## Common Misconceptions

### "Entanglement enables faster-than-light communication"

No! The no-signaling theorem is ironclad. Correlations exist, but they require classical communication to be useful.

### "Entanglement is about two particles being connected"

Better: entanglement is about the **joint state** being irreducible. It's not a physical connection—it's a property of the state description.

### "Measurement of A affects B"

In one interpretation, yes. But operationally, Bob can't detect any change. His reduced density matrix is unchanged by Alice's measurement.

### "Entanglement is rare/exotic"

Entanglement is ubiquitous! Most multi-particle states in nature are entangled. The challenge is preserving entanglement against decoherence.

### "Entanglement = superposition"

Related but distinct. Superposition is one system in multiple states. Entanglement is multiple systems with non-factorizable joint state.

---

## Code Example

```python
import numpy as np

def tensor_product(A, B):
    return np.kron(A, B)

def partial_trace_B(rho_AB, dim_A, dim_B):
    rho_A = np.zeros((dim_A, dim_A), dtype=complex)
    for j in range(dim_B):
        proj = np.zeros((dim_B, 1))
        proj[j] = 1
        operator = tensor_product(np.eye(dim_A), proj.T)
        rho_A += operator @ rho_AB @ operator.conj().T
    return rho_A

def von_neumann_entropy(rho):
    eigenvalues = np.linalg.eigvalsh(rho)
    eigenvalues = eigenvalues[eigenvalues > 1e-10]
    return -np.sum(eigenvalues * np.log2(eigenvalues))

def entropy_of_entanglement(psi_AB, dim_A, dim_B):
    """Compute entanglement entropy of a pure bipartite state."""
    rho_AB = np.outer(psi_AB, np.conj(psi_AB))
    rho_A = partial_trace_B(rho_AB, dim_A, dim_B)
    return von_neumann_entropy(rho_A)

# Basis states
ket_0 = np.array([1, 0])
ket_1 = np.array([0, 1])

# Bell state |Φ+⟩ = (|00⟩ + |11⟩)/√2
ket_00 = tensor_product(ket_0, ket_0)
ket_11 = tensor_product(ket_1, ket_1)
phi_plus = (ket_00 + ket_11) / np.sqrt(2)

# Product state |+⟩ ⊗ |0⟩
ket_plus = (ket_0 + ket_1) / np.sqrt(2)
product = tensor_product(ket_plus, ket_0)

print("Entanglement entropy comparison:")
print("=" * 40)
print(f"Product state |+⟩⊗|0⟩:  E = {entropy_of_entanglement(product, 2, 2):.3f} bits")
print(f"Bell state |Φ+⟩:        E = {entropy_of_entanglement(phi_plus, 2, 2):.3f} bits")

# Partially entangled state
# |ψ⟩ = cos(θ)|00⟩ + sin(θ)|11⟩
print("\nPartially entangled states:")
for theta_deg in [0, 15, 30, 45]:
    theta = np.radians(theta_deg)
    psi = np.cos(theta) * ket_00 + np.sin(theta) * ket_11
    E = entropy_of_entanglement(psi, 2, 2)
    print(f"  θ = {theta_deg:2d}°: E = {E:.3f} bits")
```

---

## What's Next

In [Chapter 8: Decoherence](08-decoherence.md), we'll see how entanglement with the environment destroys quantum coherence—the mechanism by which quantum becomes classical.

---

*[← Previous: Composite Systems](06-composite-systems.md) | [Back to Overview](00-overview.md) | [Next: Decoherence →](08-decoherence.md)*
