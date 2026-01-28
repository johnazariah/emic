# Quantum Computational Mechanics Research Program

*Research specification for extending emic to quantum complexity measures*

---

## Executive Summary

This document specifies a research program to extend `emic` into quantum computational mechanics. The goal is to investigate novel questions about the relationship between classical and quantum complexity measures, culminating in the first tool capable of estimating quantum complexity from empirical data.

---

## Deliverable Artifacts

The following artifacts should be produced as part of this research program, in priority order:

### Priority 1: Prerequisites (Gaps Analysis)
**Deliverable:** `.project/research/quantum-emergence/prerequisites.md`

*Must fix classical foundation before quantum work*

Content:
- Current state of excess entropy computation (it's incorrect in emic)
- Reverse machine construction (needed for causal asymmetry)
- Mixed-state representation (if needed)
- Bidirectional machine analysis
- Any CSSR improvements needed

---

### Priority 1b: Quantum Computing Primer
**Deliverable:** `.project/research/quantum-emergence/qc-primer.md`

*Foundational QC concepts needed for this research (not a general QC course)*

Content:

**States and Representations**
- Ket notation $|ψ\rangle$ and bra notation $\langle ψ|$
- State vectors as complex amplitudes
- Superposition: $|\psi\rangle = \alpha|0\rangle + \beta|1\rangle$ with $|\alpha|^2 + |\beta|^2 = 1$
- Tensor products: $|x\rangle \otimes |k\rangle$ for composite systems
- Why non-orthogonal states can't be perfectly distinguished

**Density Matrices**
- Pure states: $\rho = |\psi\rangle\langle\psi|$
- Mixed states: $\rho = \sum_i p_i |\psi_i\rangle\langle\psi_i|$
- Properties: $\text{Tr}(\rho) = 1$, $\rho^\dagger = \rho$, positive semi-definite
- Purity: $\text{Tr}(\rho^2) \leq 1$, equality for pure states

**Entropy Measures**
- Von Neumann entropy: $S(\rho) = -\text{Tr}(\rho \log \rho)$
- Relationship to Shannon entropy (diagonal = classical)
- Why $S(\rho) \leq \log d$ (dimension bound)
- Subadditivity and other properties

**Quantum Channels (Decoherence)**
- Kraus operators: $\mathcal{E}(\rho) = \sum_k K_k \rho K_k^\dagger$
- Dephasing channel: kills off-diagonal elements
- Depolarizing channel: mixes toward maximally mixed state
- Amplitude damping: models energy loss
- Physical interpretation: interaction with environment

**Measurement**
- Projective measurement: $P_m = |m\rangle\langle m|$
- Probability of outcome: $p_m = \text{Tr}(P_m \rho)$
- Post-measurement state: $\rho' = P_m \rho P_m / p_m$
- Why measurement destroys superposition

**Connections to Computational Mechanics**
- Classical causal states → orthogonal quantum states (distinguishable)
- Quantum causal states → non-orthogonal (partially distinguishable)
- Classical HMM transition → quantum channel
- Shannon entropy of distribution → von Neumann entropy of density matrix
- Statistical complexity $C_\mu$ → quantum complexity $C_q$

**Worked Examples**
- Two-state system (qubit) calculations
- Computing von Neumann entropy from eigenvalues
- Applying dephasing channel step by step
- The perturbed coin q-machine states (explicit vectors)

**What We Don't Need**
- Quantum gates and circuits (we're not doing computation)
- Entanglement measures (beyond what density matrices provide)
- Quantum algorithms (Shor, Grover, etc.)
- Fault tolerance and error correction
- Quantum hardware details

---

### Priority 2: Technical Deep Dive - "Why Quantum is Better"
**Deliverable:** `docs/guide/quantum-advantage-explained.md`

*Audience: Developers and researchers approaching emic*

Content:
- The information-theoretic argument (crypticity as classical waste)
- The non-orthogonal encoding insight (with worked example)
- The irreversibility condition from Gu et al.
- Visual: state space diagram showing classical orthogonal vs quantum non-orthogonal encoding
- Concrete example: perturbed coin walkthrough with numbers

---

### Priority 3: Mathematical Framework Document
**Deliverable:** `.project/research/quantum-emergence/framework.md`

*Precise definitions for implementation*

Content:
- Formal definitions: $C_\mu$, $E$, $\chi$, $C_q$, $C_q^+$, $C_q^-$
- The q-machine construction algorithm (step by step)
- Signal state formula and derivation
- Von Neumann entropy computation
- Relationship between classical and quantum representations

---

### Priority 4: Design Specification - Quantum Extension to emic
**Deliverable:** `.project/specifications/017-quantum-extension.md`

*What to build and how*

Content:
- New types needed (`QuantumCausalState`, `QuantumEpsilonMachine`)
- New measures to implement ($E$, $\chi$, $C_q$, causal asymmetry)
- API design (how users would interact with quantum features)
- Dependencies (numpy for linear algebra? separate quantum library?)
- Integration points with existing emic architecture

---

### Priority 5: Validation Plan
**Deliverable:** `.project/research/quantum-emergence/validation-plan.md`

*How we know it's correct*

Content:
- Golden test cases with known values from papers:
  - Perturbed coin (various parameters)
  - Golden mean process
  - Even process
  - Ising model configurations
- Numerical tolerances
- Property-based test ideas
- Comparison against published figures/tables

---

### Priority 6: Literature Synthesis
**Deliverable:** `.project/research/quantum-emergence/synthesis.md`

*What we know from the field*

Content:
- Timeline of key results (2012 → 2018 → present)
- The main players (Crutchfield group, Gu/Vedral group, collaborations)
- Key inequalities and what they mean
- Open problems identified in the papers
- Which results are proven vs conjectured

---

### Priority 7: Research Paper Outline (Optional/Long-term)
**Deliverable:** `.project/research/quantum-emergence/paper-outline.md`

*If pursuing publication*

Content:
- Positioning: "emic as a tool for quantum CM research"
- Contribution: open-source implementation + new experiments
- Target venue (e.g., New Journal of Physics, PRX Quantum)
- What experiments would be novel

---

## Research Questions

### Primary Target: Quantum Complexity Estimation from Finite Samples

> **"Can we infer quantum complexity $C_q$ directly from finite data, and how does estimation error propagate?"**

**Why novel:** All existing work constructs q-machines from *known* classical ε-machines. Nobody has tackled inference from samples.

**Why important:** Would make emic the first tool to estimate quantum complexity from empirical data, bridging theory and application.

**Approach:** Use emic to infer ε-machine → construct q-machine → compute $\hat{C}_q$ → study error propagation.

---

### Stepping Stone 1: Decoherence Trajectory (First Investigation)

> **"How does $C_q \to C_\mu$ as a function of decoherence? Is there a universal trajectory?"**

**Why tractable:** We control all variables; purely computational.

**Why valuable:**
- Builds the quantum infrastructure needed for later work
- May reveal phase transitions or universality classes
- Connects quantum foundations to computational mechanics
- Potentially publishable standalone result

---

### Stepping Stone 2: Taxonomy of Quantum Advantage

> **"Which structural features of an ε-machine predict large quantum advantage?"**

**Current knowledge:**
- Perturbed coin → unbounded advantage
- Some processes → no advantage
- No classification theorem exists

**Candidate predictors:**
- Number of "merging" transitions (futures become indistinguishable)
- Crypticity $\chi = C_\mu - E$
- Spectral properties of transition matrix
- Topological features of state graph (loops, branching)

**Why valuable:** Would allow predicting quantum advantage without full q-machine construction.

---

### Stepping Stone 3: Robustness to Model Mismatch

> **"How robust is quantum advantage when the inferred ε-machine is approximate?"**

**Setup:** If CSSR gives an ε-machine with small errors, does the derived q-machine still beat the actual classical optimum?

**Why valuable:**
- Practical concern for real applications
- Easier than full inference theory
- Informs tolerance requirements for inference

---

### Future Directions (Not in Scope Now)

**Bidirectional Quantum Machines:**
> "Is there a single quantum representation that optimally predicts AND retrodicts simultaneously?"

Thompson et al. showed quantum eliminates causal asymmetry. Open: unified bidirectional representation?

**Crypticity as Resource:**
> "Is crypticity useful for something? Can it be converted to a different resource?"

Speculation: May relate to thermodynamic work, communication complexity, or error correction.

**Quantum Inference Algorithms:**
> "Is there a direct quantum analog of CSSR that infers q-machines without classical intermediate?"

Would require quantum tomography integration - long-term goal.

---

## Investigation 1: Decoherence Trajectory (Detailed Specification)

### Objective

Map the trajectory of quantum complexity $C_q(\gamma)$ as a function of decoherence strength $\gamma \in [0,1]$, for multiple canonical processes.

### Mathematical Setup

#### Classical ε-Machine
Given process $P(\overleftarrow{X}, \overrightarrow{X})$ with:
- Causal states $\mathcal{S} = \{s_1, \ldots, s_N\}$
- Transition matrices $T^{(x)}_{ij} = P(s_j, x | s_i)$
- Stationary distribution $\pi$
- Classical complexity $C_\mu = H(\pi) = -\sum_i \pi_i \log_2 \pi_i$

#### Q-Machine Construction (Gu et al. 2012)

For each causal state $s_j$, define quantum signal state:

$$|s_j\rangle = \sum_{k=1}^{N} \sum_{x \in \Sigma} \sqrt{T^{(x)}_{jk}} |x\rangle \otimes |k\rangle$$

where:
- $|x\rangle$ is the symbol basis (dimension $|\Sigma|$)
- $|k\rangle$ is the state index basis (dimension $N$)

The average quantum state (density matrix):

$$\rho = \sum_{j=1}^{N} \pi_j |s_j\rangle\langle s_j|$$

Quantum complexity:

$$C_q = S(\rho) = -\text{Tr}(\rho \log_2 \rho)$$

#### Decoherence Channel

Apply dephasing in the computational basis with strength $\gamma$:

$$\mathcal{E}_\gamma(\rho) = (1-\gamma)\rho + \gamma \sum_i |i\rangle\langle i| \rho |i\rangle\langle i|$$

where $\{|i\rangle\}$ is the computational basis of the Hilbert space.

Alternative channels to explore:
- **Depolarizing:** $\mathcal{E}_\gamma(\rho) = (1-\gamma)\rho + \gamma \frac{I}{d}$
- **Amplitude damping:** Models energy dissipation

#### Decohered Complexity

$$C_q(\gamma) = S(\mathcal{E}_\gamma(\rho))$$

At $\gamma = 0$: $C_q(0) = C_q$ (pure quantum)
At $\gamma = 1$: $C_q(1) = ?$ (should approach $C_\mu$ under full dephasing)

### Test Processes

| Process | $C_\mu$ | $E$ | $\chi$ | Expected $C_q$ | Notes |
|---------|---------|-----|--------|----------------|-------|
| Biased Coin ($p$) | 0 | 0 | 0 | 0 | No memory needed |
| Golden Mean | $\approx 0.918$ | ? | ? | ? | Two states, known |
| Even Process | $\approx 1.0$ | ? | ? | ? | Two states |
| Perturbed Coin | $O(1/\epsilon)$ | Finite | Large | $\approx E$ | Unbounded advantage |
| Simple Nonunifilar Source | $\infty$ | Finite | $\infty$ | ? | Infinite classical |
| RIP Process | ? | ? | ? | ? | From literature |

### Algorithm

```
DECOHERENCE_TRAJECTORY(epsilon_machine, gamma_values):
    # Step 1: Extract classical parameters
    states = epsilon_machine.states
    N = len(states)
    Sigma = epsilon_machine.alphabet
    T = transition_matrices(epsilon_machine)  # dict: symbol -> NxN matrix
    pi = stationary_distribution(epsilon_machine)

    # Step 2: Construct Hilbert space
    # Dimension = |Sigma| * N
    d = len(Sigma) * N

    # Step 3: Construct signal states
    signal_states = {}  # j -> vector of length d
    for j, state in enumerate(states):
        psi_j = zeros(d, dtype=complex)
        for x, symbol in enumerate(Sigma):
            for k in range(N):
                amplitude = sqrt(T[symbol][j, k])
                index = x * N + k  # tensor product indexing
                psi_j[index] = amplitude
        signal_states[j] = psi_j

    # Step 4: Construct average density matrix
    rho = zeros((d, d), dtype=complex)
    for j in range(N):
        psi = signal_states[j]
        rho += pi[j] * outer(psi, psi.conj())

    # Step 5: Compute C_q for each gamma
    results = []
    for gamma in gamma_values:
        rho_decohered = apply_dephasing(rho, gamma)
        C_q_gamma = von_neumann_entropy(rho_decohered)
        results.append((gamma, C_q_gamma))

    return results

APPLY_DEPHASING(rho, gamma):
    d = rho.shape[0]
    diagonal = diag(diag(rho))  # extract diagonal as matrix
    return (1 - gamma) * rho + gamma * diagonal

VON_NEUMANN_ENTROPY(rho):
    eigenvalues = eigvalsh(rho)  # Hermitian eigenvalues
    # Filter small/negative eigenvalues (numerical noise)
    eigenvalues = eigenvalues[eigenvalues > 1e-12]
    return -sum(lam * log2(lam) for lam in eigenvalues)
```

### Expected Outputs

#### Data Files
```
experiments/quantum/decoherence/
├── golden_mean_trajectory.json
├── even_process_trajectory.json
├── perturbed_coin_eps0.1_trajectory.json
├── perturbed_coin_eps0.01_trajectory.json
└── ...
```

Format:
```json
{
  "process": "golden_mean",
  "parameters": {"p": 0.5},
  "C_mu": 0.918,
  "C_q": 0.XXX,
  "trajectory": [
    {"gamma": 0.0, "C_q_gamma": 0.XXX},
    {"gamma": 0.1, "C_q_gamma": 0.XXX},
    ...
  ]
}
```

#### Figures

**Figure 1: Trajectory Comparison**
- X-axis: $\gamma$ (0 to 1)
- Y-axis: $C_q(\gamma)$ in bits
- Multiple curves: different processes
- Horizontal lines: $C_\mu$ for each process (asymptote)

**Figure 2: Quantum Advantage Decay**
- X-axis: $\gamma$
- Y-axis: $C_\mu - C_q(\gamma)$ (advantage)
- Shows how advantage degrades with decoherence

**Figure 3: Normalized Trajectories**
- Y-axis: $(C_q(\gamma) - C_q) / (C_\mu - C_q)$ (0 to 1)
- Tests universality hypothesis

### Success Criteria

1. **Validation:** $C_q(0)$ matches published values for known processes
2. **Limit:** $C_q(1) \approx C_\mu$ (full dephasing recovers classical)
3. **Monotonicity:** $C_q(\gamma)$ is non-decreasing in $\gamma$
4. **Discovery:** Identify any phase transitions, universality, or surprising behavior

### Open Questions to Answer

1. Is the trajectory convex, concave, or neither?
2. Is there a critical $\gamma^*$ where behavior changes?
3. Do different decoherence channels give different trajectories?
4. Is there a universal scaling when normalized?
5. Does high crypticity $\chi$ correlate with steeper trajectories?

---

## Infrastructure Required

### New Module: `emic.quantum`

```
src/emic/quantum/
├── __init__.py
├── types.py          # QuantumCausalState, QuantumEpsilonMachine
├── construction.py   # construct_qmachine()
├── measures.py       # quantum_complexity(), quantum_advantage()
├── channels.py       # apply_dephasing(), apply_depolarizing()
└── utils.py          # von_neumann_entropy(), partial_trace()
```

### Dependencies

- `numpy` (already available) - linear algebra
- No additional quantum libraries needed for this investigation

### Type Definitions

```python
@dataclass(frozen=True)
class QuantumCausalState:
    """Quantum state associated with a causal state."""
    classical_id: StateId
    state_vector: np.ndarray  # Complex, shape (d,)

    @property
    def dimension(self) -> int:
        return len(self.state_vector)

@dataclass(frozen=True)
class QuantumEpsilonMachine:
    """Q-machine representation."""
    classical_machine: EpsilonMachine
    quantum_states: dict[StateId, QuantumCausalState]
    hilbert_dimension: int

    @cached_property
    def density_matrix(self) -> np.ndarray:
        """Average density matrix rho = sum_i pi_i |s_i><s_i|"""
        ...

    @cached_property
    def quantum_complexity(self) -> float:
        """C_q = S(rho)"""
        ...
```

---

## Timeline

| Week | Milestone |
|------|-----------|
| 1 | Implement quantum types and q-machine construction |
| 2 | Implement decoherence channels and von Neumann entropy |
| 3 | Run experiments on canonical processes |
| 4 | Analysis, visualization, write-up |

---

## Relation to Subsequent Investigations

```
┌─────────────────────────────────────────────────────────────────┐
│  Investigation 1: Decoherence Trajectory                       │
│  ─────────────────────────────────────                          │
│  Builds: quantum types, q-machine construction, C_q computation│
│  Answers: How does C_q → C_μ under noise?                       │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  Investigation 2: Taxonomy of Quantum Advantage                 │
│  ─────────────────────────────────────────────                  │
│  Uses: q-machine construction from Investigation 1              │
│  Adds: Feature extraction, correlation analysis                 │
│  Answers: What predicts C_μ - C_q?                              │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  Investigation 3: Robustness to Model Mismatch                  │
│  ─────────────────────────────────────────────                  │
│  Uses: q-machine construction, C_q computation                  │
│  Adds: Perturbation analysis, error propagation                 │
│  Answers: How sensitive is C_q to ε-machine errors?             │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  Investigation 4: Quantum Complexity from Finite Samples        │
│  ───────────────────────────────────────────────────────        │
│  Uses: All infrastructure + robustness analysis                 │
│  Adds: Bootstrap confidence intervals, bias correction          │
│  Answers: Can we estimate C_q from data? Sample complexity?     │
└─────────────────────────────────────────────────────────────────┘
```

---

## References

1. Gu, M. et al. "Quantum mechanics can reduce the complexity of classical models." Nature Communications 3, 762 (2012)
2. Thompson, J. et al. "Causal Asymmetry in a Quantum World." Phys. Rev. X 8, 031013 (2018)
3. Garner, A.J.P. et al. "Unbounded Memory Advantage in Stochastic Simulation." New J. Phys. 19, 103009 (2017)
4. Tan, R. et al. "Towards Quantifying Complexity with Quantum Mechanics." EPJ Plus 129, 191 (2014)
5. Aghamohammadi, C. et al. "Extreme Quantum Advantage when Simulating Strongly Coupled Classical Systems." Sci. Reports 7, 6735 (2017)

---

*Document version: 1.0*
*Created: 2026-01-28*
*Status: Ready for implementation*
