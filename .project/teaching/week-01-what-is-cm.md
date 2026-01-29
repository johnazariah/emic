# Week 1: What is Computational Mechanics?

**Dates**: January 29 - February 5, 2026
**Status**: 🟢 Active

---

## Learning Objectives

By the end of this week, you will be able to:

1. Articulate what computational mechanics is actually trying to do (in one sentence)
2. Define a causal state precisely — both formally and intuitively
3. Explain why the ε-machine is the unique optimal classical predictor
4. Derive the ε-machine for the Golden Mean process from first principles

---

## Reading Assignments

### Primary Reading

**Paper**: Shalizi & Crutchfield (2001) "Computational Mechanics: Pattern and Prediction, Structure and Simplicity"

**File**: [.project/references/shalizi2001computational/shalizi2001computational_full.md](../../references/shalizi2001computational/shalizi2001computational_full.md)

**Sections to read carefully**:
- Section I: Introduction (pages 1-3)
- Section II: What Is Computational Mechanics? (pages 3-8)
- Section III: The Computational Mechanics Framework (pages 8-12)
- Section IV: Causal States (pages 12-16)

**Focus questions while reading**:
1. What is the "intrinsic computation" that a process performs?
2. How do causal states differ from the states of a general HMM?
3. What makes the ε-machine construction canonical?

### Secondary Reading

**Paper**: Crutchfield (1994) "Calculi of Emergence"

**File**: [.project/references/Calculus_Of_Emergence_Crutchfield/Calculus_Of_Emergence_Crutchfield_full.md](../../references/Calculus_Of_Emergence_Crutchfield/Calculus_Of_Emergence_Crutchfield_full.md)

**Sections to skim**:
- Introduction
- Section on "Reconceptualizing Complexity"
- Section on "Computational Mechanics"

This is more philosophical but gives the motivation.

---

## Key Concepts

### 1. The Central Question

Computational mechanics asks: **Given observations of a process, what is its minimal sufficient model for prediction?**

Not just any model. The *minimal* model that loses *no* predictive information.

### 2. Causal States (Intuition)

A **causal state** is an equivalence class of histories that predict the same futures.

$$\overleftarrow{s} \sim_\epsilon \overleftarrow{s}' \iff P(\overrightarrow{X} | \overleftarrow{X} = \overleftarrow{s}) = P(\overrightarrow{X} | \overleftarrow{X} = \overleftarrow{s}')$$

**Intuition**: Two histories are equivalent if they make identical predictions. If you can't distinguish their futures, why distinguish them?

### 3. Why ε-Machines Are Special

The ε-machine is:
- **Minimal**: Fewest states among all predictive models
- **Unifilar**: Next state is determined by current state + output symbol
- **Sufficient**: Captures all predictable structure
- **Unique**: The only model with all these properties

### 4. Statistical Complexity

$$C_\mu = H[\mathcal{S}]$$

The entropy of the causal state distribution. This is the memory required to optimally predict the process.

---

## Exercise: Derive the Golden Mean ε-Machine

The Golden Mean process is a binary sequence where `11` is forbidden.

**Part 1: Enumeration**
List all allowed histories of length 0, 1, 2, 3:
- Length 0: ε (empty)
- Length 1: 0, 1
- Length 2: 00, 01, 10
- Length 3: ?

**Part 2: Predictive Equivalence**
For each history, what is $P(\text{next symbol} = 0 | \text{history})$?

- After "0": Can emit 0 or 1 → $P(\text{next} = 0) = ?$
- After "1": Must emit 0 → $P(\text{next} = 0) = 1$

Which histories have the same predictive distribution?

**Part 3: Causal States**
Identify the equivalence classes. How many causal states are there?

**Part 4: Transition Structure**
Draw the ε-machine. For each state:
- What symbols can be emitted?
- What's the probability of each?
- What state does each transition go to?

**Part 5: Statistical Complexity**
Compute $C_\mu = H[\mathcal{S}]$ where $H$ is Shannon entropy.

*(Don't use emic for this — work it out by hand first, then verify)*

---

## Discussion Questions

After reading, be prepared to discuss:

1. **The philosophical claim**: Shalizi claims that causal states are "real" — they're not just a mathematical convenience but capture the actual structure of the process. Do you buy this?

2. **Minimality vs sufficiency**: Why is it important that the ε-machine is *both* minimal and sufficient? What goes wrong if you have only one?

3. **The comparison to physics**: Computational mechanics is presented as a "physics of information." What does this mean? Is it just marketing, or is there something deeper?

4. **Connection to our code**: Open `src/emic/types/machine.py` and find the `EpsilonMachine` class. How does the implementation reflect the mathematical definition?

---

## What to Bring to Our Discussion

1. Your solution to the Golden Mean exercise
2. One concept you found confusing
3. One insight that surprised you
4. One question about how this connects to quantum

---

## Preview: Why This Matters for Quantum

The quantum advantage comes from *how* you encode causal states.

In Week 4, we'll see that the ε-machine's causal states must be perfectly distinguishable (orthogonal). But if two histories predict *almost* the same futures, why distinguish them perfectly?

The q-machine encodes states non-orthogonally — distinguishing them only as much as prediction requires. The "extra" distinguishability in the classical model is *waste*.

This week's foundation is crucial: you need to understand what causal states are before you can understand what it means to encode them quantumly.

---

## Checklist

- [ ] Read Shalizi & Crutchfield (2001) sections I-IV
- [ ] Skim Crutchfield (1994) "Calculi of Emergence"
- [ ] Complete the Golden Mean exercise
- [ ] Review `EpsilonMachine` class in emic
- [ ] Write down questions for discussion
- [ ] Schedule discussion session

---

*Ready when you are. Let me know when you've done the reading and want to discuss.*
