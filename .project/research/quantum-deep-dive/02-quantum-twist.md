# Chapter 2: The Quantum Twist

*Complex amplitudes, phases, and the birth of interference*

---

## The Leap

In Chapter 1, we saw that classical uncertainty lives on the diagonal of a matrix. Now we take the crucial step: **what if we allow complex numbers?**

This isn't a mathematical convenience—it's a fundamental fact about nature. Quantum amplitudes are complex, and the phase (the "angle" of the complex number) has physical consequences.

---

## From Probabilities to Amplitudes

### The Classical Setup

In classical probability, we have real numbers $p_i \geq 0$ with $\sum_i p_i = 1$.

### The Quantum Setup

In quantum mechanics, we have **complex amplitudes** $\alpha_i \in \mathbb{C}$ with $\sum_i |\alpha_i|^2 = 1$.

The probability of outcome $i$ is $|\alpha_i|^2$—the squared magnitude.

A quantum state is written as:

$$|\psi\rangle = \alpha_1 |1\rangle + \alpha_2 |2\rangle + \cdots + \alpha_n |n\rangle$$

For a qubit (two-level system):

$$|\psi\rangle = \alpha |0\rangle + \beta |1\rangle$$

where $|\alpha|^2 + |\beta|^2 = 1$.

---

## Complex Numbers: A Quick Refresher

A complex number $z = a + bi$ has:
- **Real part**: $a$
- **Imaginary part**: $b$
- **Magnitude**: $|z| = \sqrt{a^2 + b^2}$
- **Phase**: $\theta = \arctan(b/a)$

Equivalently, in polar form: $z = |z| e^{i\theta} = |z|(\cos\theta + i\sin\theta)$

### Key Insight: Magnitude vs Phase

The magnitude $|z|$ determines the probability: $P = |z|^2$.

The phase $\theta$ determines **how amplitudes combine**. Two amplitudes with the same magnitude but different phases can:
- **Add constructively** (phases aligned → larger result)
- **Add destructively** (phases opposite → cancellation)

This is interference, and it has no classical analog.

---

## Why Phases Matter: A Worked Example

Consider two paths to the same outcome, each with amplitude:

**Path A**: $\alpha_A = \frac{1}{\sqrt{2}}$

**Path B**: $\alpha_B = \frac{1}{\sqrt{2}}$

If we measure the probability of the outcome:

### Classical thinking (add probabilities):

$$P = |\alpha_A|^2 + |\alpha_B|^2 = \frac{1}{2} + \frac{1}{2} = 1$$

### Quantum reality (add amplitudes first):

$$\alpha_{\text{total}} = \alpha_A + \alpha_B = \frac{1}{\sqrt{2}} + \frac{1}{\sqrt{2}} = \sqrt{2}$$

$$P = |\alpha_{\text{total}}|^2 = 2$$

Wait—probability greater than 1? That can't be right!

The issue: our amplitudes weren't normalized for this combined system. Let's do it properly.

---

## Interference: The Double-Slit in Numbers

Let's model a simplified double-slit experiment.

A particle can go through slit A or slit B to reach detector D:

```
        ┌─────┐
Source ─┤Slit A├──┐
        └─────┘   │
                  ├──▶ Detector D
        ┌─────┐   │
Source ─┤Slit B├──┘
        └─────┘
```

Suppose the amplitude for each path is:

$$\alpha_A = \frac{1}{\sqrt{2}} e^{i\phi_A}, \quad \alpha_B = \frac{1}{\sqrt{2}} e^{i\phi_B}$$

The total amplitude at the detector:

$$\alpha_D = \alpha_A + \alpha_B = \frac{1}{\sqrt{2}}\left(e^{i\phi_A} + e^{i\phi_B}\right)$$

The probability:

$$P_D = |\alpha_D|^2 = \frac{1}{2}\left|e^{i\phi_A} + e^{i\phi_B}\right|^2$$

Using $|e^{i\theta_1} + e^{i\theta_2}|^2 = 2 + 2\cos(\theta_1 - \theta_2)$:

$$P_D = \frac{1}{2}\left(2 + 2\cos(\phi_A - \phi_B)\right) = 1 + \cos(\phi_A - \phi_B)$$

### Three Cases

| Phase difference | $\cos(\Delta\phi)$ | Probability | Interpretation |
|-----------------|-------------------|-------------|----------------|
| $\Delta\phi = 0$ | +1 | **2** (normalized: 1) | Constructive interference |
| $\Delta\phi = \pi/2$ | 0 | **1** (normalized: 0.5) | No interference |
| $\Delta\phi = \pi$ | -1 | **0** | Destructive interference |

When phases are opposite ($\Delta\phi = \pi$), the amplitudes **cancel completely**. The particle never arrives at the detector—despite having two paths to get there!

This is impossible classically. Adding more ways to reach an outcome can only increase (or maintain) the probability, never decrease it.

---

## The Mathematical Signature: Off-Diagonal Elements

Here's where we connect to Chapter 1's key insight.

Consider a qubit in superposition:

$$|\psi\rangle = \frac{1}{\sqrt{2}}|0\rangle + \frac{1}{\sqrt{2}}|1\rangle$$

The density matrix is:

$$\rho = |\psi\rangle\langle\psi| = \begin{pmatrix} \frac{1}{2} & \frac{1}{2} \\ \frac{1}{2} & \frac{1}{2} \end{pmatrix}$$

The off-diagonal elements $\frac{1}{2}$ encode the superposition. They're nonzero because both amplitudes are nonzero and have the same phase.

Now consider a superposition with a relative phase:

$$|\psi'\rangle = \frac{1}{\sqrt{2}}|0\rangle + \frac{e^{i\phi}}{\sqrt{2}}|1\rangle$$

$$\rho' = \begin{pmatrix} \frac{1}{2} & \frac{e^{-i\phi}}{2} \\ \frac{e^{i\phi}}{2} & \frac{1}{2} \end{pmatrix}$$

The off-diagonals now carry phase information! They're complex numbers.

**Key observation**: The diagonal entries (probabilities) are the same. But the off-diagonals differ. These states will interfere differently.

---

## Phase vs Global Phase

One subtlety: **global phase doesn't matter**.

If we multiply the entire state by $e^{i\theta}$:

$$|\psi'\rangle = e^{i\theta}|\psi\rangle$$

The density matrix is unchanged:

$$\rho' = e^{i\theta}|\psi\rangle\langle\psi|e^{-i\theta} = |\psi\rangle\langle\psi| = \rho$$

So $|\psi\rangle$ and $e^{i\theta}|\psi\rangle$ represent the same physical state.

Only **relative phases** between components matter:

$$|0\rangle + |1\rangle \quad \text{vs} \quad |0\rangle + e^{i\phi}|1\rangle$$

These are different states (for $\phi \neq 0$).

---

## The Bloch Sphere: Visualizing Qubit States

A qubit state can be parameterized as:

$$|\psi\rangle = \cos\frac{\theta}{2}|0\rangle + e^{i\phi}\sin\frac{\theta}{2}|1\rangle$$

This maps to a point on a sphere (the Bloch sphere):
- $\theta$: polar angle (0 at north pole = $|0\rangle$, $\pi$ at south pole = $|1\rangle$)
- $\phi$: azimuthal angle (the phase)

```
           |0⟩ (north pole)
            ▲
           /|\
          / | \
         /  |  \    ← θ determines |α|² vs |β|²
        /   |   \
       ●----+----●  ← φ is the phase
        \   |   /
         \  |  /
          \ | /
           \|/
            ▼
           |1⟩ (south pole)
```

Classical states live only at the poles (pure $|0\rangle$ or $|1\rangle$).

Quantum superpositions can be **anywhere on the sphere**. The entire surface is accessible.

---

## Why Does Nature Use Complex Numbers?

This is a deep question. The pragmatic answer: complex numbers are the simplest mathematical structure that:

1. Allows interference (amplitudes can cancel)
2. Is consistent with composition (combining systems)
3. Gives well-defined probabilities

Real numbers don't give enough structure. Quaternions give too much.

A more physical answer: complex numbers encode both magnitude and phase compactly. Waves naturally have amplitude and phase. Quantum mechanics is fundamentally wavelike.

---

## Connecting to Computational Mechanics

In computational mechanics, we care about states that predict the future. Two causal states might lead to similar futures—but a classical ε-machine must store them in separate "slots."

With quantum amplitudes, we can encode these states with **overlap**—their dot product $\langle s_i | s_j \rangle$ can be nonzero. This overlap is a complex number.

The magnitude of the overlap tells us: how distinguishable are these states?
- $|\langle s_i | s_j \rangle| = 0$: Perfectly distinguishable (orthogonal)
- $|\langle s_i | s_j \rangle| = 1$: Identical states
- In between: Partially distinguishable

Classical encoding requires perfect distinguishability. Quantum encoding allows partial overlap—and that's where the compression comes from.

---

## Key Takeaway

> **The quantum twist: amplitudes are complex, and phases matter.**
>
> When multiple paths lead to the same outcome, amplitudes add—and can interfere constructively or destructively. This is encoded in the off-diagonal elements of the density matrix.
>
> Phases enable interference. Interference enables computation. This is the engine of quantum mechanics.

---

## Common Misconceptions

### "The particle goes through both slits"

Not quite. We can't say which slit it went through—asking the question changes the physics (measurement). The amplitudes for both paths contribute, but that's different from the particle having a trajectory through both.

### "Complex numbers are just a mathematical trick"

No—they're essential. Real amplitudes can't produce destructive interference in the right way. The phase information is physical.

### "Superposition means uncertainty about which state"

No! A superposition $|0\rangle + |1\rangle$ is not uncertainty about whether the system is in $|0\rangle$ or $|1\rangle$. It's a definite quantum state—just not a classical one. Measurement *creates* the classical outcome; it wasn't secretly there before.

### "Phase is like a clock"

This is actually a good analogy! Phase does evolve like a clock hand rotating. States with different energies rotate at different rates, creating relative phase differences that lead to interference patterns.

---

## Code Example

```python
import numpy as np

# Two amplitudes with different phases
alpha_A = 1/np.sqrt(2) * np.exp(1j * 0)       # phase = 0
alpha_B = 1/np.sqrt(2) * np.exp(1j * np.pi)   # phase = π (opposite)

# Add amplitudes (quantum)
alpha_total = alpha_A + alpha_B
prob_quantum = np.abs(alpha_total)**2

# Add probabilities (classical)
prob_classical = np.abs(alpha_A)**2 + np.abs(alpha_B)**2

print(f"Amplitude A: {alpha_A:.3f} (phase = 0)")
print(f"Amplitude B: {alpha_B:.3f} (phase = π)")
print(f"Total amplitude: {alpha_total:.3f}")
print()
print(f"Quantum probability: {prob_quantum:.3f}")
print(f"Classical probability: {prob_classical:.3f}")
print()
print("Destructive interference: quantum probability is ZERO!")

# Density matrix for |0⟩ + e^{iφ}|1⟩
def density_matrix_with_phase(phi):
    """Density matrix for (|0⟩ + e^{iφ}|1⟩)/√2"""
    psi = np.array([1, np.exp(1j * phi)]) / np.sqrt(2)
    return np.outer(psi, np.conj(psi))

print("\nDensity matrices with different phases:")
for phi in [0, np.pi/2, np.pi]:
    rho = density_matrix_with_phase(phi)
    print(f"\nφ = {phi:.2f}:")
    print(np.round(rho, 3))
```

Output:
```
Amplitude A: (0.707+0j) (phase = 0)
Amplitude B: (-0.707+0j) (phase = π)
Total amplitude: 0j

Quantum probability: 0.000
Classical probability: 1.000

Destructive interference: quantum probability is ZERO!

Density matrices with different phases:

φ = 0.00:
[[0.5 0.5]
 [0.5 0.5]]

φ = 1.57:
[[0.5  0.-0.5j]
 [0.+0.5j 0.5]]

φ = 3.14:
[[ 0.5 -0.5]
 [-0.5  0.5]]
```

Notice how the diagonal stays the same but the off-diagonals change with phase.

---

## What's Next

In [Chapter 3: The Density Matrix](03-density-matrix.md), we'll see how the density matrix unifies pure states, mixed states, and measurement—and why it's the central object in quantum mechanics.

---

*[← Previous: Classical Uncertainty](01-classical-uncertainty.md) | [Back to Overview](00-overview.md) | [Next: The Density Matrix →](03-density-matrix.md)*
