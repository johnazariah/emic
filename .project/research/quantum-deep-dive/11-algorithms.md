# Chapter 11: Quantum Algorithms

*What they do, why they work*

---

## The Landscape

Quantum algorithms fall into several families:

| Family | Key Technique | Speedup | Examples |
|--------|---------------|---------|----------|
| **Oracular** | Amplitude amplification | Quadratic | Grover search, quantum counting |
| **Fourier-based** | QFT, period finding | Exponential | Shor (factoring), HHL (linear systems) |
| **Variational** | Classical-quantum hybrid | Problem-dependent | VQE, QAOA |
| **Simulation** | Hamiltonian evolution | Exponential | Quantum chemistry, materials |

We'll examine the most important ones.

---

## Grover's Algorithm

### Problem
Find a marked item in an unsorted list of $N$ items.

### Speedup
Classical: $O(N)$ queries. Quantum: $O(\sqrt{N})$ queries.

### Why It Works

Start with uniform superposition. Each Grover iteration:
1. **Oracle**: Flip sign of marked item
2. **Diffusion**: Reflect about mean amplitude

This is "amplitude amplification"—the marked item's amplitude grows while others shrink.

### Geometry

In the 2D plane of (marked, unmarked):
- Oracle: reflection about the unmarked axis
- Diffusion: reflection about the uniform superposition

Two reflections = rotation toward the marked state.

### Optimality

Grover's quadratic speedup is **provably optimal** for unstructured search. No quantum algorithm can do better without additional structure.

### Applications
- Database search
- Satisfiability (with caveats)
- Cryptographic key search
- Subroutine in other algorithms

---

## Shor's Algorithm

### Problem
Factor an integer $N = pq$ (product of two primes).

### Speedup
Classical: Sub-exponential. Quantum: Polynomial $O(n^3)$.

### Why It Works

Factoring reduces to **period finding**: find $r$ such that $a^r \equiv 1 \pmod{N}$.

The quantum part:
1. Create superposition $\sum_x |x\rangle |a^x \mod N\rangle$
2. Apply Quantum Fourier Transform to first register
3. Measure to get information about $r$

The QFT converts periodicity into amplitude peaks. Non-period frequencies destructively interfere.

### The Breakthrough

Finding the period of $a^x \mod N$ takes exponential classical time (best known).

The QFT does it in polynomial quantum time by leveraging:
- Superposition (evaluate at all $x$ simultaneously)
- Interference (QFT concentrates amplitude at period-related values)

### Implications

Shor's algorithm breaks RSA encryption. This motivated:
- Post-quantum cryptography research
- The race to build quantum computers
- The race to deploy quantum-resistant encryption

---

## Quantum Simulation

### Problem
Simulate the time evolution of a quantum system with Hamiltonian $H$: $|\psi(t)\rangle = e^{-iHt}|\psi(0)\rangle$.

### Speedup
Classical: Exponential in system size. Quantum: Polynomial.

### Why It Works

A quantum computer is itself a quantum system. It naturally implements quantum evolution.

For local Hamiltonians (sum of few-body terms):
$$H = \sum_j H_j$$

Use Trotter decomposition:
$$e^{-iHt} \approx (e^{-iH_1 t/n} e^{-iH_2 t/n} \cdots)^n$$

Each $e^{-iH_j \Delta t}$ is a few-qubit gate. The error decreases with $n$.

### Feynman's Vision

Richard Feynman proposed quantum computers precisely for this purpose:

> "Nature isn't classical, dammit, and if you want to make a simulation of nature, you'd better make it quantum mechanical."

### Applications
- Quantum chemistry (molecular energies, reaction dynamics)
- Materials science (superconductivity, magnetism)
- Drug discovery (protein folding, binding energies)
- Fundamental physics (lattice gauge theories)

---

## Variational Quantum Eigensolver (VQE)

### Problem
Find the ground state energy of a Hamiltonian $H$.

### Approach
Hybrid classical-quantum:
1. Quantum computer prepares a parameterized state $|\psi(\theta)\rangle$
2. Measures energy $\langle H \rangle = \langle\psi(\theta)|H|\psi(\theta)\rangle$
3. Classical optimizer adjusts $\theta$ to minimize energy
4. Repeat until converged

### Why It's Practical

- Shallow circuits (work on near-term noisy devices)
- Noise can be partially mitigated
- Quantum advantage unclear but promising for chemistry

### The Trade-off

VQE trades guaranteed speedup for practical implementability. It may not be exponentially faster, but it might solve useful problems sooner.

---

## HHL Algorithm (Linear Systems)

### Problem
Solve $Ax = b$ for $x$, where $A$ is an $N \times N$ matrix.

### Speedup
Classical: $O(N)$ to $O(N^3)$ depending on method. Quantum: $O(\log N)$ (exponential speedup).

### Caveats
The output is the quantum state $|x\rangle$, not the classical vector. To read out $x$ takes $O(N)$ time anyway.

Useful when:
- You only need a few properties of $x$ (like $\langle x|M|x \rangle$ for some $M$)
- $|x\rangle$ is input to another quantum algorithm

### How It Works
1. Encode $b$ as quantum state $|b\rangle$
2. Use phase estimation to get eigenvalues of $A$
3. Invert eigenvalues coherently
4. Uncompute to get $|x\rangle \propto A^{-1}|b\rangle$

### Applications
- Machine learning (kernel methods, recommendation systems)
- Optimization (portfolio optimization)
- Differential equations (finite element methods)

---

## Quantum Machine Learning

### Promise
Exponential speedups for certain ML tasks.

### Reality
Most claimed speedups have caveats:
- Input must be quantum-accessible (not classical data)
- Output is often quantum state, not classical answer
- "Dequantization" results show some speedups are illusory

### Genuine Advantages
- Quantum kernels for classification
- Quantum neural networks (expressive power)
- Quantum sampling (Boltzmann machines)

The field is rapidly evolving. Genuine advantage for practical ML remains to be demonstrated.

---

## Algorithm Comparison

| Algorithm | Problem | Speedup | Qubits Needed | Practical? |
|-----------|---------|---------|---------------|------------|
| Grover | Unstructured search | Quadratic | $O(n)$ | Near-term |
| Shor | Factoring | Exponential | $O(n)$ | Long-term |
| Simulation | Quantum dynamics | Exponential | $O(n)$ | Near-term |
| VQE | Ground states | TBD | $O(n)$ | Now |
| HHL | Linear systems | Exponential* | $O(\log N)$ | Long-term |

*With caveats about input/output.

---

## Connection to Computational Mechanics

How do quantum algorithms relate to computational mechanics?

**Simulation of stochastic processes**: A q-machine is a quantum model of a classical stochastic process. To simulate the process, you'd implement the q-machine as a quantum circuit.

**Complexity as circuit depth**: The quantum complexity $C_q$ relates to the quantum resources needed. Lower $C_q$ means the process can be simulated with less quantum memory.

**Inference as algorithm**: Future work might develop quantum algorithms for ε-machine inference—learning the structure of a process from data.

**Entropy rate as uncertainty**: The entropy rate $h_\mu$ measures irreducible randomness. Quantum algorithms can't compress this—it's genuine information content.

---

## Key Takeaway

> **Different quantum algorithms exploit different types of structure.**
>
> - **Grover**: Amplitude amplification for unstructured search → quadratic speedup
> - **Shor**: QFT for period finding → exponential speedup for structured number theory
> - **Simulation**: Natural quantum dynamics → exponential speedup for quantum systems
> - **Variational**: Hybrid optimization → practical near-term applications
>
> Quantum advantage requires structure. The algorithm must be matched to the problem.

---

## Common Misconceptions

### "Quantum computers solve NP-complete problems efficiently"

No evidence for this. Grover gives only quadratic speedup for SAT. Exponential speedups need more structure than NP-completeness provides.

### "More qubits = faster"

Qubits enable larger problem instances, not faster solutions to fixed-size problems. The algorithm determines the speedup.

### "Quantum machine learning will be revolutionary"

Maybe, but current claims often don't survive scrutiny. True quantum advantage for practical ML is an open question.

### "Quantum computers will replace classical computers"

No. They're specialized tools for specific problem types. Classical computers will remain essential.

---

## What's Next

In [Chapter 12: Why Quantum Speedup?](12-why-speedup.md), we'll synthesize what we've learned to understand when quantum computers help and when they don't.

---

*[← Previous: Interference as Computation](10-interference.md) | [Back to Overview](00-overview.md) | [Next: Why Quantum Speedup? →](12-why-speedup.md)*
