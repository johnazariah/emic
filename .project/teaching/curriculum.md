# Quantum Computational Mechanics: A 12-Week Curriculum

*Preparing for publication through deep understanding*

**Student**: John Azariah
**Instructor**: Claude (AI Professor)
**Duration**: January 29 - April 29, 2026
**Goal**: Master every nuance needed to defend and publish quantum CM research

---

## Philosophy

This is not a survey course. We will:

1. **Read primary sources** — The actual papers, not summaries
2. **Derive, not memorize** — You'll re-derive key results yourself
3. **Connect to code** — Every concept maps to your emic implementation
4. **Anticipate reviewers** — What questions will they ask?

---

## Assessment of Starting Point

You currently understand:
- ✅ Classical epsilon-machines and CSSR
- ✅ Statistical complexity $C_\mu$, entropy rate $h_\mu$
- ✅ That quantum models can be more efficient
- ✅ How to compute $C_q$ (you wrote the code)

You need to deeply understand:
- ⬜ Why the signal state construction works (mathematical proof)
- ⬜ The physical meaning of non-orthogonal encoding
- ⬜ Excess entropy $E$ and its role as fundamental bound
- ⬜ Crypticity $\chi$ and its physical interpretation
- ⬜ The irreversibility theorem (Gu et al.)
- ⬜ Causal asymmetry (Thompson et al.)
- ⬜ The landscape of open problems

---

## Weekly Structure

Each week:
- **Reading**: 1-2 papers or paper sections (assigned in advance)
- **Lecture**: Discussion of key concepts (~1 hour)
- **Exercise**: Derivation or calculation to solidify understanding
- **Reflection**: What would a reviewer ask? What's still unclear?

---

# Part I: Foundations (Weeks 1-3)

## Week 1: What is Computational Mechanics?

**Learning Objectives:**
- Articulate the central question of computational mechanics
- Define causal states precisely
- Understand why ε-machines are optimal classical predictors

**Reading:**
- Crutchfield & Young (1989) "Inferring Statistical Complexity" — Sections 1-3
- Shalizi & Crutchfield (2001) "Computational Mechanics" — Definition sections

**Key Questions:**
1. What is a causal state? (Not the formal definition — the intuition)
2. Why can't we do better than the ε-machine classically?
3. What does "optimal" mean here — optimal for what?

**Exercise:**
Derive the ε-machine for the Golden Mean process from first principles. Show that the two states you get are the only causal states.

**Paper Deep Dive:**
`.project/references/` — We'll identify the exact sections to read

---

## Week 2: The Complexity Hierarchy

**Learning Objectives:**
- Define $C_\mu$, $E$, $h_\mu$, and $\chi$ precisely
- Understand the inequality $E \leq C_\mu$
- Explain what crypticity measures physically

**Reading:**
- James, Crutchfield, et al. (2011) "Anatomy of a Bit" — Full paper
- Crutchfield & Feldman (2003) "Regularities Unseen" — Crypticity sections

**Key Questions:**
1. Why is $E$ a lower bound on any model's memory?
2. What is crypticity measuring? Give a physical example.
3. Why does the ε-machine "waste" $\chi$ bits?

**Exercise:**
For the perturbed coin with $p=0.3$:
- Calculate $C_\mu$, $E$, $h_\mu$, $\chi$ by hand
- Verify against emic's output
- Draw the information diagram

---

## Week 3: Hidden Markov Models and Unifilarity

**Learning Objectives:**
- Understand the relationship between HMMs and ε-machines
- Define unifilarity and explain why it matters
- Understand co-unifilarity (reverse unifilarity)

**Reading:**
- Travers & Crutchfield (2011) "Equivalence of History and Generator ε-Machines"
- Upper & Crutchfield — Mixed states and non-unifilarity

**Key Questions:**
1. What makes ε-machines special among HMMs?
2. Why does unifilarity enable efficient simulation?
3. What happens when you reverse time — is the reverse ε-machine unifilar?

**Exercise:**
- Show that the Golden Mean ε-machine is unifilar
- Construct its reverse and show it is NOT unifilar
- Relate this to causal asymmetry (preview of Week 8)

---

# Part II: The Quantum Leap (Weeks 4-6)

## Week 4: Why Quantum? The Central Insight

**Learning Objectives:**
- Understand non-orthogonal quantum states
- Explain why quantum encoding can save memory
- Connect to the irreversibility condition

**Reading:**
- Gu et al. (2012) "Quantum mechanics can reduce the complexity" — Full paper
- Your deep dive Chapter 5-6 as supplementary

**Key Questions:**
1. What physical principle allows quantum advantage?
2. Why can't classical systems use "non-orthogonal" encoding?
3. What does the irreversibility theorem actually say?

**Exercise:**
Derive the signal states for the perturbed coin by hand. Compute $\langle s_0 | s_1 \rangle$ and verify it matches $2\sqrt{p(1-p)}$.

**Paper Deep Dive:**
Go through Gu et al. equation by equation. Which equations do you not fully understand?

---

## Week 5: The Q-Machine Construction

**Learning Objectives:**
- Construct the q-machine from an ε-machine
- Compute the density matrix $\rho$
- Calculate $C_q$ via von Neumann entropy

**Reading:**
- Gu et al. (2012) — Supplementary material (detailed construction)
- Tan et al. (2014) "Towards Quantifying Complexity" — Alternative perspective

**Key Questions:**
1. Why is the Hilbert space $\mathcal{H} = \mathcal{H}_\text{symbol} \otimes \mathcal{H}_\text{state}$?
2. Why do we use $\sqrt{T^{(x)}_{jk}}$ not $T^{(x)}_{jk}$?
3. What's the physical meaning of the density matrix eigenvalues?

**Exercise:**
For the Golden Mean process:
- Construct the signal states explicitly
- Compute the density matrix
- Find eigenvalues and calculate $C_q$
- Verify against emic

---

## Week 6: Bounds and Optimality

**Learning Objectives:**
- Prove $E \leq C_q \leq C_\mu$
- Understand when $C_q = E$ (optimal quantum)
- Understand when $C_q = C_\mu$ (no advantage)

**Reading:**
- Gu et al. (2012) — Theorem proofs
- Garner et al. (2017) "Provably Unbounded Memory Advantage"

**Key Questions:**
1. Why is $E$ the fundamental lower bound even for quantum?
2. What class of processes achieves $C_q = E$?
3. Garner shows unbounded advantage — what's the construction?

**Exercise:**
Prove that for the perturbed coin, $C_q \to E$ as $p \to 0.5$. (Hint: compute both quantities in this limit.)

---

# Part III: Advanced Topics (Weeks 7-9)

## Week 7: The Overlap Criterion (Your Contribution)

**Learning Objectives:**
- Formalize the signal state overlap criterion
- Connect to graph-theoretic properties of ε-machines
- Understand why some 2-state processes have no advantage

**Reading:**
- Your validation notebook analysis
- Your taxonomy notes

**Key Questions:**
1. State the overlap criterion precisely as a theorem
2. What's the graph-theoretic interpretation (co-determinism)?
3. Is this criterion in the literature, or is it novel?

**Exercise:**
Survey 10 processes. For each:
- Predict quantum advantage (yes/no) using the criterion
- Verify with emic
- Document any edge cases

---

## Week 8: Causal Asymmetry

**Learning Objectives:**
- Define forward vs backward complexity: $C_q^+$ and $C_q^-$
- Understand causal asymmetry $\Delta C_q = C_q^+ - C_q^-$
- Explain the thermodynamic connection

**Reading:**
- Thompson et al. (2018) "Causal Asymmetry in a Quantum World" — Full paper
- Crutchfield (2012) "Between Order and Chaos"

**Key Questions:**
1. Why can quantum models break time-symmetry?
2. What's the physical meaning of causal asymmetry?
3. How does this connect to the arrow of time?

**Exercise:**
For the Golden Mean:
- Construct the reverse ε-machine
- Compute $C_q^+$ and $C_q^-$
- Calculate causal asymmetry

---

## Week 9: Extreme Cases and Limitations

**Learning Objectives:**
- Understand unbounded advantage constructions
- Know the limitations of current q-machine theory
- Identify open problems

**Reading:**
- Aghamohammadi et al. (2017) "Extreme Quantum Advantage" (Ising model)
- Garner et al. (2017) — Full construction

**Key Questions:**
1. What makes the Ising model special?
2. Are there processes where quantum provides no advantage?
3. What can't current theory handle?

**Exercise:**
Implement the simplest "extreme advantage" process in emic and verify.

---

# Part IV: Toward Publication (Weeks 10-12)

## Week 10: Literature Synthesis

**Learning Objectives:**
- Map the research landscape (who did what, when)
- Identify your unique contribution
- Position your work relative to existing literature

**Reading:**
- All paper introductions and conclusions (skim for positioning)
- Your literature synthesis document

**Key Questions:**
1. What's the "story arc" of this field (2012-2024)?
2. Where does your work fit?
3. What claims can you make that are novel?

**Exercise:**
Write a 1-page "related work" section for your paper.

---

## Week 11: Anticipating Reviewers

**Learning Objectives:**
- Identify potential criticisms
- Prepare rigorous responses
- Strengthen weak points

**Activity:**
I play devil's advocate reviewer. You defend your work.

**Potential Reviewer Questions:**
1. "How is this different from Gu et al. 2012?"
2. "The overlap criterion seems obvious — what's the contribution?"
3. "Why should physicists care about computational mechanics?"
4. "How would you verify this experimentally?"

**Exercise:**
Write responses to 5 likely reviewer objections.

---

## Week 12: Paper Outline and Next Steps

**Learning Objectives:**
- Structure your paper
- Identify remaining experiments/figures needed
- Plan the writing process

**Deliverables:**
- Detailed paper outline
- List of figures with captions
- Timeline for writing

**Final Assessment:**
You explain the entire quantum CM story to me, from $E \leq C_q \leq C_\mu$ to your specific contributions, without notes.

---

# Appendix: Reading List by Paper

## Must Read Completely
1. Gu et al. (2012) — Foundational
2. Thompson et al. (2018) — Causal asymmetry
3. James et al. (2011) — "Anatomy of a Bit"

## Read Key Sections
4. Garner et al. (2017) — Unbounded advantage construction
5. Tan et al. (2014) — Alternative q-machine perspective
6. Aghamohammadi et al. (2017) — Ising model

## Background/Reference
7. Crutchfield & Young (1989) — Original CM paper
8. Shalizi & Crutchfield (2001) — Computational mechanics review
9. Crutchfield & Feldman (2003) — Regularities unseen

---

# How to Use This Curriculum

Each session:
1. I'll check if you did the reading
2. We'll discuss key concepts (Socratic method)
3. You'll work through exercises
4. We'll identify what's still unclear

**Ready to start Week 1?**
