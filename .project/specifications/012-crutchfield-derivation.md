# Specification 012: Re-Derivation of Computational Mechanics

## Overview

This specification outlines a parallel research track to re-derive the foundational results of computational mechanics from first principles, with the goals of:

1. **Deep understanding** — Internalize the theory by reconstructing it
2. **Pedagogical clarity** — Create accessible derivations for the paper
3. **Potential extensions** — Identify opportunities for novel contributions
4. **Verification** — Confirm our implementation matches theory

---

## Core Theorems to Derive

### Theorem 1: Causal States are Sufficient Statistics

**Statement**: The causal state σ(←x) is a sufficient statistic for predicting →X given ←x.

**Approach**:
1. Define predictive equivalence relation ∼ε
2. Show that histories in the same equivalence class have identical conditional distributions
3. Prove sufficiency via the factorization theorem

**Key Insight**: σ captures exactly what's needed for prediction — no more, no less.

---

### Theorem 2: ε-Machine is the Minimal Unifilar Presentation

**Statement**: Among all unifilar HMMs generating process P, the ε-machine has minimal entropy H[S].

**Approach**:
1. Define unifilarity: given (state, symbol), next state is deterministic
2. Show any unifilar presentation refines the causal state partition
3. Prove entropy minimality follows from coarsest partition property

**Key Insight**: Statistical complexity Cμ is the *minimum* memory required for optimal prediction.

---

### Theorem 3: Cμ ≤ E (Statistical Complexity Bounds Excess Entropy)

**Statement**: The statistical complexity is bounded above by the excess entropy.

**Approach**:
1. Define excess entropy E = I[←X; →X]
2. Show Cμ = H[S] where S is the causal state
3. Use data processing inequality: I[←X; →X] ≥ I[S; →X] = H[S]

**Note**: This can be strengthened to Cμ ≤ E with equality iff process is "causally reversible".

---

### Theorem 4: Entropy Rate from ε-Machine

**Statement**: hμ = Σ_s π_s H[X | S=s] where π is the stationary distribution.

**Approach**:
1. Start from hμ = lim H[X_n | X_1, ..., X_{n-1}]
2. Use Markov property of causal states
3. Show limit equals conditional entropy given current state

---

### Theorem 5: CSSR Consistency

**Statement**: CSSR recovers the true ε-machine as data → ∞.

**Approach**:
1. Show suffix tree statistics converge to true distributions
2. Show χ² tests correctly identify (non-)equivalence asymptotically
3. Prove partition converges to causal state partition

**Reference**: Shalizi & Klinkner (2004), but derive from scratch.

---

## Derivation Structure

### Part I: Foundations

#### Chapter 1: Stochastic Processes
- Definitions: stationary, ergodic, mixing
- Entropy: H[X], conditional H[X|Y], mutual I[X;Y]
- Entropy rate: hμ = lim H[X_n | past]

#### Chapter 2: Predictive Equivalence
- Histories and futures: ←x, →x
- Predictive distribution: P(→X | ←x)
- Equivalence relation: ←x ∼ε ←y iff P(→X | ←x) = P(→X | ←y)

#### Chapter 3: Causal States
- Definition: σ(←x) = [←x]_ε (equivalence class)
- Causal state set: S = {σ(←x) : ←x ∈ A^-}
- Proof: |S| ≤ |A|^L for L-Markov processes

### Part II: ε-Machine Structure

#### Chapter 4: Transition Dynamics
- Labeled transitions: s --x--> s' with probability T(s' | s, x)
- Unifilarity: T(s' | s, x) ∈ {0, 1}
- Proof of unifilarity from causal state definition

#### Chapter 5: Minimality
- State entropy: H[S]
- Comparison with other representations
- Proof of minimality

#### Chapter 6: Complexity Measures
- Statistical complexity: Cμ = H[S]
- Entropy rate: hμ
- Excess entropy: E = I[←X; →X]
- Relationships and bounds

### Part III: Inference

#### Chapter 7: CSSR Algorithm
- Suffix tree construction
- Homogeneity testing
- Splitting and merging
- Convergence proof

#### Chapter 8: Alternative Approaches
- Bayesian inference
- Spectral methods
- Information-theoretic bounds on sample complexity

### Part IV: Extensions

#### Chapter 9: Mixed States
- Beyond unifilarity
- ε-transducers
- Bidirectional machines

#### Chapter 10: Continuous Time
- Rate matrices
- Continuous-valued observations

---

## Novel Directions to Explore

### Direction 1: Differential Computational Mechanics

**Idea**: Extend to continuous-valued processes using differential entropy.

**Questions**:
- What's the analog of causal states for continuous X?
- Is there a minimal sufficient statistic theorem?
- How does discretization affect inference?

---

### Direction 2: Quantum Computational Mechanics

**Idea**: Causal states for quantum processes.

**Questions**:
- How do quantum correlations change the picture?
- Is there a quantum ε-machine?
- Connection to quantum Markov chains?

---

### Direction 3: Computational Mechanics of Networks

**Idea**: ε-machines for graph-structured processes.

**Questions**:
- Spatial ε-machines?
- Causal states for graph signals?
- Connection to graphical models?

---

### Direction 4: Online/Streaming Inference

**Idea**: Update ε-machine incrementally as data arrives.

**Questions**:
- Can we maintain sufficient statistics online?
- Adaptive state count?
- Forgetting for non-stationary processes?

---

### Direction 5: Causal Inference Connection

**Idea**: Link computational mechanics to Pearl's causal inference.

**Questions**:
- Are causal states related to causal graphs?
- Intervention semantics for ε-machines?
- Counterfactuals in computational mechanics?

---

## Deliverables

### Written Derivations

Location: `docs/theory/` or `paper/appendix/`

Format: LaTeX with detailed proofs

### Verification Code

```python
# Numerical verification of theorems
def verify_theorem_3():
    """Verify Cμ ≤ E for various processes."""
    for process in [GoldenMean, EvenProcess, ...]:
        machine = process.true_machine
        summary = analyze(machine)
        assert summary.statistical_complexity <= summary.excess_entropy + 1e-10
```

### Tutorial Notebooks

- `theory/01_causal_states.ipynb` — Interactive exploration of causal states
- `theory/02_complexity_measures.ipynb` — Visualizing Cμ, hμ, E
- `theory/03_cssr_walkthrough.ipynb` — Step-by-step CSSR execution

---

## Timeline

| Week | Focus |
|------|-------|
| 1 | Foundations: entropy, processes, equivalence |
| 2 | Causal states and ε-machine definition |
| 3 | Minimality proofs |
| 4 | Complexity measures and bounds |
| 5 | CSSR derivation and consistency |
| 6 | Extensions and novel directions |

---

## Key References

1. **Crutchfield, J.P. & Young, K. (1989)**. "Inferring Statistical Complexity". *Phys. Rev. Lett.*

2. **Shalizi, C.R. & Crutchfield, J.P. (2001)**. "Computational Mechanics: Pattern and Prediction, Structure and Simplicity". *J. Stat. Phys.*

3. **Crutchfield, J.P. (2012)**. "Between Order and Chaos". *Nature Physics.*

4. **Marzen, S. & Crutchfield, J.P. (2020)**. "Inference, Prediction, and Entropy Rate Estimation of Continuous-Time, Discrete-Event Processes".

5. **Strelioff, C.C. & Crutchfield, J.P. (2014)**. "Bayesian Structural Inference for Hidden Processes".
