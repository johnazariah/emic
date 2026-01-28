# Key Papers in Quantum Computational Mechanics

*Annotated bibliography for the quantum emergence research area*

---

## Foundational Papers

### 1. Occam's Quantum Razor (Gu et al., 2012)
**Full title**: "Quantum mechanics can reduce the complexity of classical models"

**Authors**: Mile Gu, Karoline Wiesner, Elisabeth Rieper, Vlatko Vedral

**Source**: Nature Communications 3, 763 (2012) | [arXiv:1102.1994](https://arxiv.org/abs/1102.1994)

**Key results**:
- Proves quantum models can be strictly more efficient than classical epsilon-machines
- Introduces the quantum statistical complexity $C_q = S(\rho)$
- Establishes the hierarchy: $E \leq C_q \leq C_\mu$
- Shows quantum models can approach the fundamental limit $E$

**Relevance to emic**:
- Central paper for the quantum extension
- Provides explicit construction of q-machines
- Perturbed coin example is a key validation target

**Notes**: Already summarized in `.project/references/gu2012quantum/`

---

### 2. Towards Quantifying Complexity with Quantum Mechanics (Tan et al., 2014)
**Authors**: Ryan Tan, Daniel R. Terno, Jayne Thompson, Vlatko Vedral, Mile Gu

**Source**: EPJ Plus 129, 191 (2014) | [arXiv:1404.6255](https://arxiv.org/abs/1404.6255)

**Key results**:
- Proposes new complexity measure based on quantum epsilon-machines
- Applies to system undergoing constant thermalization
- Quantum measure aligns better with intuitive complexity

**Relevance to emic**:
- Provides concrete examples for validation
- Suggests alternative complexity measures to implement

**Status**: To read

---

### 3. Unbounded Memory Advantage in Stochastic Simulation (Garner et al., 2017)
**Authors**: Andrew J. P. Garner, Qing Liu, Jayne Thompson, Vlatko Vedral, Mile Gu

**Source**: New J. Phys. 19, 103009 (2017) | [arXiv:1609.04408](https://arxiv.org/abs/1609.04408)

**Key results**:
- Quantum processors with fixed finite memory can simulate to arbitrarily high precision
- Proves **unbounded** memory advantage over best classical simulator
- Uses tools from computational mechanics

**Relevance to emic**:
- Strongest result on quantum advantage
- Important validation target
- Connects to continuous-variable processes

**Status**: To read

---

### 4. Causal Asymmetry in a Quantum World (Thompson et al., 2018)
**Authors**: Jayne Thompson et al.

**Source**: [arXiv, likely 2018]

**Key results**:
- Studies temporal asymmetry in quantum causal models
- Connects to thermodynamic arrow of time

**Relevance to emic**:
- Already in references: `.project/references/thompson2018causal/`
- Connects to bidirectional machine analysis

**Status**: To read

---

## Crutchfield-Gu Collaborations

These papers represent the direct collaboration between the two main research groups.

### 5. Causal Asymmetry in a Quantum World (Thompson et al., 2018) ⭐
**Authors**: Jayne Thompson, Andrew J. P. Garner, John R. Mahoney, **James P. Crutchfield**, Vlatko Vedral, **Mile Gu**

**Source**: Phys. Rev. X 8, 031013 (2018) | [arXiv:1712.02368](https://arxiv.org/abs/1712.02368)

**Key results**:
- Causal asymmetry: memory to predict forward ≠ memory to retrodict backward
- There's a privileged temporal direction where memory costs are minimal
- **Quantum models can eliminate this asymmetry entirely**
- Even when classical overhead is unbounded, quantum models achieve bounded memory

**Relevance to emic**:
- Direct connection to bidirectional machine analysis (planned in M5)
- Shows quantum advantage extends to temporal asymmetry
- Key validation target for emic's quantum extension

**Status**: Already in references as `thompson2018causal/`

---

### 6. Thermodynamic Machine Learning (Boyd, Crutchfield, Gu, 2022)
**Authors**: A. B. Boyd, **James P. Crutchfield**, **Mile Gu**

**Source**: New J. Phys. 24, 013013 (2022) | [arXiv link TBD]

**Key results**:
- Connects epsilon-machines to thermodynamic work extraction
- Maximum work production as learning objective
- Links statistical complexity to thermodynamic costs

**Relevance to emic**:
- Thermodynamic interpretation of complexity measures
- Future direction for emic's quantum extension

**Status**: To acquire and read

---

### 7. Thermodynamic Overfitting and Generalization (Boyd, Crutchfield, Gu et al., 2025)
**Authors**: A. B. Boyd, **James P. Crutchfield**, **Mile Gu**, et al.

**Source**: New J. Phys. (2025)

**Key results**:
- Energetics of predictive intelligence
- Addresses overfitting in thermodynamic learning context
- Covers both classical and quantum HMMs

**Relevance to emic**:
- Most recent Crutchfield-Gu collaboration
- Connects to model selection and generalization

**Status**: To acquire and read (very recent!)

---

### 8. Strong and Weak Optimizations (Loomis & Crutchfield, 2019)
**Authors**: Samuel Loomis, **James P. Crutchfield**

**Source**: J. Stat. Phys. (2019) | [arXiv:1808.08639](https://arxiv.org/abs/1808.08639)

**Key results**:
- ε-machine is **strongly minimal** classically (minimizes all Rényi measures)
- **No strongly minimal quantum model exists** for some processes
- Quantum memory optimization depends on which measure is used

**Relevance to emic**:
- Critical for understanding quantum model non-uniqueness
- Guides choice of complexity measure for quantum extension
- Shows ε-machine's special classical status doesn't transfer to quantum

**Status**: To read (high priority)

---

### 9. Extreme Quantum Memory Advantage for Rare-Event Sampling (Aghamohammadi et al., 2018)
**Authors**: C. Aghamohammadi, S. P. Loomis, J. R. Mahoney, **J. P. Crutchfield**

**Source**: Phys. Rev. X 8, 011025 (2018)

**Key results**:
- Extreme quantum advantage for rare-event sampling
- Memory advantage can be arbitrarily large

**Relevance to emic**:
- Shows specific application where quantum shines
- Connects to importance sampling and rare events

**Status**: To read

---

### 10. Extreme Quantum Advantage with Long-Range Interaction (Aghamohammadi et al., 2017)
**Authors**: C. Aghamohammadi, J. R. Mahoney, **J. P. Crutchfield**

**Source**: Scientific Reports 7, 6735 (2017)

**Key results**:
- Long-range correlations → large quantum advantage
- Explicit constructions for specific process classes

**Relevance to emic**:
- Identifies structural features predicting quantum advantage
- Good validation targets

**Status**: To read

---

## Extended Reading List

### Computational Mechanics Foundations
- Crutchfield & Young (1989) - "Inferring statistical complexity" - Original epsilon-machine paper
- Shalizi & Crutchfield (2001) - "Computational mechanics" - Comprehensive theory
- Crutchfield (1994) - "Calculi of emergence" - Philosophical foundations

### Quantum Extensions
- **Aghamohammadi et al. (2018)** - "Extreme Quantum Memory Advantage for Rare-Event Sampling"
- **Mahoney et al. (2016)** - "Quantum Information in the Randomness of Quantum Processes"
- **Binder et al. (2018)** - "Practical Unitary Simulator for Non-Markovian Complex Processes"
- **Riechers & Crutchfield (2021)** - "Spectral Simplicity of Apparent Complexity" (metadynamics)

### Quantum Information Foundations
- Cerf & Adami (1997) - Quantum conditional probability
- Wilde (2017) - "Quantum Information Theory" (textbook)

### Recent Developments (2020-2026)
- **Inferring Kernel ε-Machines** (Jurgens & Brodu, 2024) - [arXiv:2410.01076](https://arxiv.org/abs/2410.01076)
- **Quantum Causal Unravelling** (Bai et al., 2022) - [arXiv:2109.13166](https://arxiv.org/abs/2109.13166)
- **Entanglement, Complexity, and Causal Asymmetry** (Williams, 2022) - [arXiv:2204.06742](https://arxiv.org/abs/2204.06742)

---

## Papers to Acquire

| Paper | arXiv | Priority |
|-------|-------|----------|
| Boyd, Crutchfield, Gu (2022) - Thermodynamic ML | TBD | High |
| Boyd, Crutchfield, Gu (2025) - Overfitting | TBD | High |
| Loomis & Crutchfield (2019) - Strong/Weak Opt | 1808.08639 | High |
| Aghamohammadi et al. (2018) - Rare Events | TBD | Medium |
| Mahoney et al. (2016) | TBD | Medium |
| Binder et al. (2018) | TBD | Medium |

---

## Reading Plan

### Priority 1: Core Crutchfield-Gu Papers
1. **Thompson et al. (2018)** - Causal Asymmetry [arXiv:1712.02368] - already in refs
2. **Loomis & Crutchfield (2019)** - Strong/Weak Optimizations [arXiv:1808.08639]
3. **Boyd, Crutchfield, Gu (2022)** - Thermodynamic Machine Learning

### Priority 2: Foundational Quantum Advantage
4. Re-read Gu et al. (2012) - extract all equations for re-derivation
5. Garner et al. (2017) - Unbounded memory advantage
6. Tan et al. (2014) - Quantum complexity measures

### Priority 3: Applications & Extensions
7. Aghamohammadi et al. (2017, 2018) - Long-range & rare events
8. Boyd et al. (2025) - Most recent work
9. Survey 2020-2026 developments

---

## Key Insight from Literature

The Crutchfield-Gu collaboration bridges two communities:
- **Crutchfield (UC Davis)**: Classical computational mechanics, ε-machines, emergence
- **Gu (NUS Singapore)**: Quantum information, quantum simulation, thermodynamics

Their joint work (especially Thompson et al. 2018 and Loomis & Crutchfield 2019) reveals that:
1. Quantum models break classical bounds on causal asymmetry
2. No unique "quantum ε-machine" exists (unlike classical case)
3. Thermodynamics provides operational interpretation

This is the bridge emic needs to cross to extend to quantum.

---

*Last updated: 2026-01-27*
