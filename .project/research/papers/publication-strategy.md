# Publication Strategy

**Created:** January 23, 2026
**Status:** Active Planning

---

## Overview

Three complementary documents serving different audiences and purposes:

| Document | Audience | Purpose | Venue |
|----------|----------|---------|-------|
| **Tutorial** | Students, researchers new to field | Teach computational mechanics | University seminars, workshops |
| **Research Paper** | Academic community | Review & validate Crutchfield/Shalizi | Journal (Entropy, JMLR) |
| **Technical Report** | Practitioners, thesis committee | Document emic's contribution | Thesis chapter, arXiv |

---

## 1. Tutorial: "A Practical Guide to Computational Mechanics"

### Purpose
Pedagogical introduction for university presentations. Build intuition before formalism.

### Audience
- Graduate students in physics, CS, complexity science
- Researchers curious about the field
- Practitioners wanting to apply these ideas

### Tone
Conversational, worked examples, "why does this matter?"

### Structure (Draft)
1. **The Problem**: Finding hidden structure in randomness
2. **Intuition**: What is a "state" of a process?
3. **Information Theory Refresher**: Just enough H, I, conditional entropy
4. **Causal States**: The equivalence relation, with pictures
5. **The ε-Machine**: Minimal predictive model
6. **Worked Example 1**: Golden Mean (binary, simple)
7. **Worked Example 2**: Even Process (slightly harder)
8. **Measures**: Cμ (memory) and hμ (randomness)
9. **The Key Theorems**: Prescience + Minimality (intuitive proofs)
10. **Inference**: How CSSR works (algorithm walkthrough)
11. **Hands-On**: Running emic on your data
12. **Further Reading**: Where to go next

### Key Features
- Many diagrams and state machines
- Python code that runs
- Exercises with solutions
- Avoids measure theory

### Length
~30 pages / 50 slides equivalent

---

## 2. Research Paper: "Computational Mechanics: A Modern Review"

### Purpose
Rigorous exposition of Crutchfield & Shalizi's theoretical framework with:
- Clear mathematical presentation
- Modern perspective (25 years later)
- Numerical validation of key theorems

### Audience
- Researchers in statistical physics, information theory, ML
- Those who want to cite a clear reference

### Tone
Formal, precise, theorem-proof style

### Structure (Draft)
1. **Abstract**
2. **Introduction**: Historical context, why this matters now
3. **Mathematical Preliminaries**:
   - Stochastic processes
   - Information measures (H, I, E)
   - Hidden Markov Models
4. **Causal States**:
   - Definition via equivalence relation
   - Properties (Lemmas)
5. **The ε-Machine**:
   - Formal construction
   - Unifilarity
6. **Fundamental Theorems**:
   - **Theorem 1** (Prescience): Causal states are sufficient statistics
   - **Theorem 2** (Minimality): ε-machine has minimal Cμ
   - **Theorem 3** (Uniqueness): Up to isomorphism
   - **Theorem 4** (Bound): E ≤ Cμ
7. **Complexity Measures**:
   - Statistical complexity Cμ
   - Entropy rate hμ
   - Excess entropy E
   - Relationships and interpretations
8. **Numerical Validation**:
   - Golden Mean, Even Process, Periodic
   - Theorem verification
   - Convergence analysis
9. **Discussion**:
   - Connections to other frameworks (HMMs, MDL, Kolmogorov)
   - Open questions
10. **Conclusion**

### Key Features
- Full proofs or proof sketches with citations
- Reproducible numerical experiments
- Comparison table: CM vs related frameworks
- Extensive bibliography (~50+ refs)

### Length
~20 pages (journal format)

### Target Venue
- Primary: Entropy (MDPI) — open access, good fit
- Alternative: Journal of Statistical Physics, Chaos

---

## 3. Technical Report: "emic: A Python Framework for ε-Machine Inference"

### Purpose
Document the `emic` library's design, implementation, and validation. Forms a thesis chapter.

### Audience
- Thesis committee
- Practitioners who want to use/extend emic
- Future maintainers

### Tone
Technical but accessible, software engineering + science

### Structure (Draft)
1. **Abstract**
2. **Introduction**:
   - Gap: Theory exists, tools don't
   - Contribution: Production-quality Python library
3. **Background**:
   - Brief CM recap (reference the research paper)
   - Existing tools (CSSR Perl, others)
   - Why a new implementation?
4. **Architecture**:
   - Design principles (immutability, protocols, composition)
   - Core types: `Symbol`, `StateId`, `EpsilonMachine`
   - Pipeline composition with `>>`
5. **Inference Algorithms**:
   - CSSR (primary)
   - Spectral Learning
   - Causal State Merging
   - Bayesian Structural Inference
   - Naive State Discovery
   - Comparison table
6. **Validation**:
   - Golden tests methodology
   - Known processes: BiasedCoin, GoldenMean, EvenProcess, Periodic
   - Convergence analysis
   - Noise robustness
7. **Performance**:
   - Benchmarks
   - Scaling behavior
8. **Case Studies**:
   - Real-world data application (TBD)
9. **API Reference**:
   - Key classes and functions
   - Usage examples
10. **Discussion**:
    - Limitations
    - Future work (quantum extension)
11. **Conclusion**

### Key Features
- Architecture diagrams
- Code listings with explanations
- Benchmark tables
- Test coverage report
- Reproducibility: all experiments runnable

### Length
~40 pages (thesis chapter format)

---

## Relationships Between Documents

```
                    ┌──────────────────┐
                    │    Tutorial      │
                    │  (Pedagogical)   │
                    └────────┬─────────┘
                             │ "for rigorous treatment, see..."
                             ▼
                    ┌──────────────────┐
                    │  Research Paper  │
                    │   (Theoretical)  │
                    └────────┬─────────┘
                             │ "for implementation, see..."
                             ▼
                    ┌──────────────────┐
                    │ Technical Report │
                    │  (emic library)  │
                    └──────────────────┘
```

Cross-references:
- Tutorial → Paper: "See [Paper] for proofs"
- Paper → Report: "Validated using emic [Report]"
- Report → Paper: "Based on theory in [Paper]"

---

## Shared Assets

### Figures (reusable across documents)
- [ ] Golden Mean state diagram
- [ ] Even Process state diagram
- [ ] Periodic(n) state diagrams
- [ ] Complexity-entropy plane
- [ ] CSSR algorithm flowchart
- [ ] emic architecture diagram
- [ ] Convergence curves (states vs n)

### Tables (reusable)
- [ ] Canonical processes: states, Cμ, hμ
- [ ] Algorithm comparison
- [ ] Theorem summary

### Code (validated, reusable)
- [ ] Golden Mean inference example
- [ ] Even Process inference example
- [ ] Measure computation example
- [ ] Pipeline composition example

---

## Timeline (Proposed)

| Phase | Duration | Deliverable |
|-------|----------|-------------|
| 1. Shared assets | 1 week | Figures, tables, validated code |
| 2. Tutorial draft | 2 weeks | Complete first draft |
| 3. Paper draft | 3 weeks | Complete first draft |
| 4. Report draft | 2 weeks | Complete first draft |
| 5. Review cycle | 2 weeks | Internal review, revision |
| 6. Submission | - | Tutorial: slides; Paper: journal; Report: thesis |

---

## Next Actions

1. [x] Create this planning document
2. [ ] Set up directory structure for all three
3. [ ] Create shared assets directory
4. [ ] Generate validated figures
5. [ ] Draft Tutorial outline (detailed)
6. [ ] Draft Paper outline (detailed)
7. [ ] Draft Report outline (detailed)

---

## Notes

- The existing content in `experiments/paper_verification/tex/` is a mix — salvage good parts
- Need to run EXP-003 (paper verification) to populate numerical results
- Consider Quarto for the tutorial (renders to slides + HTML + PDF)
- All three should use the same notation and terminology

