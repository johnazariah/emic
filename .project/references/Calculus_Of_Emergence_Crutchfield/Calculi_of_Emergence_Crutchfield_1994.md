# The Calculi of Emergence: Computation, Dynamics, and Induction

**Author:** James P. Crutchfield
**Affiliation:** Physics Department, University of California, Berkeley, California 94720
**Source:** Physica D (1994), Proceedings of the Oji International Seminar on Complex Systems
**Conference:** Complex Systems — from Complex Dynamics to Artificial Reality, 5-9 April 1993, Numazu, Japan
**Report:** SFI 94-03-016

---

## Abstract

Defining structure and detecting the emergence of complexity in nature are inherently subjective, though essential, scientific activities. Despite the difficulties, these problems can be analyzed in terms of how model-building observers infer from measurements the computational capabilities embedded in nonlinear processes. An observer's notion of what is ordered, what is random, and what is complex in its environment depends directly on its computational resources: the amount of raw measurement data, of memory, and of time available for estimation and inference. The discovery of structure in an environment depends more critically and subtly, though, on how those resources are organized. The descriptive power of the observer's chosen (or implicit) computational model class, for example, can be an overwhelming determinant in finding regularity in data.

This paper presents an overview of an inductive framework — hierarchical ε-machine reconstruction — in which the emergence of complexity is associated with the innovation of new computational model classes. Complexity metrics for detecting structure and quantifying emergence, along with an analysis of the constraints on the dynamics of innovation, are outlined. Illustrative examples are drawn from the onset of unpredictability in nonlinear systems, finitary nondeterministic processes, and cellular automata pattern recognition. They demonstrate how finite inference resources drive the innovation of new structures and so lead to the emergence of complexity.

---

## Contents

- **Part I: Innovation, Induction, and Emergence**
  - 1. Emergent?
  - 2. Evolutionary Processes
  - 3. What's in a Model?
  - 4. The Modeling Dilemma
  - 5. A Computational View of Nature
  - 6. Computational Mechanics: Beyond Statistics, Toward Structure
  - 7. Agenda
- **Part II: Mechanism and Computation**
  - 1. Road Maps to Innovation
  - 2. Complexity = Randomness
  - 3. ε-Machine Reconstruction
  - 4. Measuring Predictability and Structure
- **Part III: Toward a Mathematical Theory of Innovation**
  - 1. Reconstructing Language Hierarchies
  - 2. At Each Level in a Hierarchy
  - 3. The ε-Machine Hierarchy
  - 4. The Threshold of Innovation
  - 5. Examples of Hierarchical Learning
- **Part IV: Observations and Hypotheses**
  - 1. Complexity as the Interplay of Order and Chaos
  - 2. Evolutionary Mechanics

---

# Part I: Innovation, Induction, and Emergence

> "Order is not sufficient. What is required, is something much more complex. It is order entering upon novelty; so that the massiveness of order does not degenerate into mere repetition; and so that the novelty is always reflected upon a background of system."
>
> — A. N. Whitehead, *Process and Reality* [1]

How can complexity emerge from a structureless universe? Or, for that matter, how can it emerge from a completely ordered universe? The following proposes a synthesis of tools from dynamical systems, computation, and inductive inference to analyze these questions.

The central puzzle addressed is how we as scientists — or, for that matter, how adaptive agents evolving in populations — ever "discover" anything new in our worlds, when it appears that all we can describe is expressed in the language of our current understanding. This dilemma is analyzed in terms of an open-ended modeling scheme, called **hierarchical ε-machine reconstruction**, that incorporates at its base inductive inference and quantitative measures of computational capability and structure. The key step in the emergence of complexity is the "innovation" of new model classes from old. This occurs when resource limits can no longer support the large models — often patchworks of special cases — forced by a lower-level model class.

The presentation is broken into four parts:
- **Part I** is introductory and attempts to define the problems of discovery and emergence
- **Part II** reviews computation theory and a method to infer computational structure in nonlinear processes
- **Part III** shows formally, and by analyzing examples, how innovation and the emergence of complexity occur in hierarchical processes
- **Part IV** is a summary and a look forward

---

## 1. Emergent?

Some of the most engaging and perplexing natural phenomena are those in which highly-structured collective behavior emerges over time from the interaction of simple subsystems. Flocks of birds flying in lockstep formation and schools of fish swimming in coherent array abruptly turn together with no leader guiding the group [2]. Ants form complex societies whose survival derives from specialized laborers, unguided by a central director [3]. Optimal pricing of goods in an economy appears to arise from agents obeying the local rules of commerce [4].

How does global coordination emerge in these processes? Are common mechanisms guiding the emergence across these diverse phenomena? What languages do contemporary science and mathematics provide to unambiguously describe the different kinds of organization that emerge in such systems?

**Definition:** Emergence is generally understood to be a process that leads to the appearance of structure not directly described by the defining constraints and instantaneous forces that control a system. Over time "something new" appears at scales not directly specified by the equations of motion. An emergent feature also cannot be explicitly represented in the initial and boundary conditions. In short, a feature emerges when the underlying system puts some effort into its creation.

### 1.1 Pattern!

One recent and initially baffling example of emergence is **deterministic chaos**. In this, deterministic equations of motion lead over time to apparently unpredictable behavior. When confronted with chaos, one question immediately demands an answer — Where in the determinism did the randomness come from? The answer is that the effective dynamic, which maps from initial conditions to states at a later time, becomes so complicated that an observer can neither measure the system accurately enough nor compute with sufficient power to predict the future behavior when given an initial condition. The emergence of disorder here is the product of both the complicated behavior of nonlinear dynamical systems and the limitations of the observer [8].

Consider instead an example in which order arises from disorder. In a **self-avoiding random walk** in two dimensions the step-by-step behavior of a particle is specified directly in stochastic equations of motion: at each time it moves one step in a random direction, except the one it just came from. The result, after some period of time, is a path tracing out a self-similar set of positions in the plane. A "fractal" structure emerges from the largely disordered step-by-step motion.

The "newness" in both cases is in the eye of an observer: the observer whose predictions fail or the analyst who notes that the feature of statistical self-similarity captures a commonality across length scales.

### 1.2 Intrinsic Emergence

In pattern formation, the "newness" is always referred outside the system to some observer that anticipates the structures via a fixed palette of possible regularities. By way of analogy with a communication channel, the observer is a receiver that already has the codebook in hand. Any signal sent down the channel that is not already decodable using it is essentially noise, a pattern unrecognized by the observer.

In the emergence of coordinated behavior, though, there is a closure in which the patterns that emerge are important within the system. That is, those patterns take on their "newness" with respect to other structures in the underlying system. Since there is no external referent for novelty or pattern, we can refer to this process as **"intrinsic" emergence**.

What is distinctive about intrinsic emergence is that the patterns formed confer additional functionality which supports global information processing. The hypothesis in the following is that during intrinsic emergence there is an increase in intrinsic computational capability, which can be capitalized on and so lends additional functionality.

**Three notions distinguished:**
1. The intuitive definition of emergence: "something new appears"
2. Pattern formation: an observer identifies "organization" in a dynamical system
3. Intrinsic emergence: the system itself capitalizes on patterns that appear

---

## 2. Evolutionary Processes

One arena that frames the question of intrinsic emergence in familiar terms is biological evolution, which presumes to explain the appearance of highly organized systems from a disorganized primordial soup.

The prototype universe consists of an **environment** and a set of adaptive observers or **"agents"**. An agent is a stochastic dynamical system that attempts to build and maintain a maximally-predictive internal model of its environment. The environment for each agent is the collection of other agents. At any given time an agent's sensorium is a projection of the current environmental state.

[Figure 1: Agent-centric view of the environment — see original PDF]

The basic problem facing an agent is the prediction of future sensory input based on modeling the hidden environmental states and on selecting possible actions. The problem facing the designer of such a prototype universe is how to know if the agents have adapted and how they did so. This requires a quantitative theory of how agents process information and build models.

---

## 3. What's in a Model?

"Model" is being used here in a sense that is somewhat more generous than found in daily scientific practice. There it often refers to an explicit representation — an analog — of a system under study. Here models will be seen in addition as existing implicitly in the dynamics and behavior of a process. Rather than being able to point to (say) an agent's model of its environment, the designer of the prototype universe may have to excavate the "model". To do this one might infer that an agent's responses are in co-relation with its environment, that an agent has memory of the past, that the agent can make decisions, and so on. Thus, "model" here is more "behavioral" than "cognitive".

---

## 4. The Modeling Dilemma

A key modeling dichotomy that runs throughout all of science is that between **order** and **randomness**. A fundamental point is that any act of modeling makes a distinction between data that is accounted for — the ordered part — and data that is not described — the apparently random part.

Nature is seldom so simple. It appears that natural processes are an amalgam of randomness and order. **It is the organization of the interplay between order and randomness that makes nature "complex."** A complex process then differs from a "complicated" process, a large system consisting of very many components, subsystems, degrees of freedom, and so on. A complicated system — such as an ideal gas — needn't be complex, in the sense used here. The ideal gas has no structure. Its microscopic dynamics are accounted for by randomness.

### The Balance Principle

A balance between order and randomness can be reached and used to define a "best" model for a given data set. The balance is given by:
- **Minimizing the model's size** (Occam's dictum: causes should not be multiplied beyond necessity)
- **Minimizing the amount of apparent randomness** (a basic tenet of science: obtain the best prediction of nature)

Neither component can be minimized alone. Typically, the sum of the model size and the error is minimized [19-23].

### The Problem of Innovation

This does not really solve the problem of quantifying structure. In fact, it simply elevates it to a higher level of abstraction. Measuring structure as the length of the description of the "best" model assumes one has chosen a language in which to describe models. The catch is that this representation choice builds in its own biases.

**The problem of "innovation":** How can an observer ever break out of inadequate model classes and discover appropriate ones? How can incorrect assumptions be changed? How is anything new ever discovered, if it must always be expressed in the current language?

---

## 5. A Computational View of Nature

Contemporary physics does not have the tools to address the problems of innovation, the discovery of patterns, or even the practice of modeling itself, since there are no physical principles that define and dictate how to measure natural structure. Physics does have the tools for detecting and measuring:
- Complete order (equilibria, fixed point or periodic behavior)
- Ideal randomness (via temperature, thermodynamic entropy, Shannon entropy rate, Kolmogorov complexity)

What is still needed is a definition of structure and a way to detect and to measure it.

One recent approach is to adapt and extend ideas from the **theory of discrete computation**, which has developed measures of information-processing structure, to inferring complexity in dynamical systems [24]. Computation theory defines the notion of a "machine" — a device for encoding the structures in discrete processes.

Given a discrete series of measurements from a process, a machine can be constructed that is the best description or predictor of this discrete time series. The structure of this machine can be said to be the best approximation to the original process's information-processing structure. Once we have reconstructed the machine, we can say that we understand the structure of the process.

---

## 6. Computational Mechanics: Beyond Statistics, Toward Structure

The goal is to provide both a qualitative and a quantitative analysis of natural information-processing architectures. The machine reconstruction approach to emergence attempts to address each component in turn:

1. **Modeling**: Driven by the need for an encapsulation of environmental experience
2. **Computation**: Driven by the need to process sensory information and produce actions
3. **Innovation**: Driven by limited observational, computational, and control resources

Key extensions needed beyond traditional computation theory:
- Inclusion of probability
- Inductive inference
- Spatial extent
- Continuous-state processes

---

## 7. Agenda

The phrase "calculi of emergence" in the title emphasizes the tools required to address the problems which intrinsic emergence raises. The tools are:
1. **Dynamical systems theory** — with its emphasis on the role of time and on the geometric structures underlying the increase in complexity during a system's time evolution
2. **Computation theory** — the notions of mechanism and structure
3. **Inductive inference** — as a statistical framework in which to detect and innovate new representations

---

# Part II: Mechanism and Computation

Probably the most highly developed appreciation of hierarchical structure is found in the theory of discrete computation, which includes automata theory and the theory of formal languages [31-33]. The main objects of attention in discrete computation are **strings** (or words) $\omega$ consisting of symbols $s$ from a finite alphabet:

$$\omega = s_0 s_1 s_2 \ldots s_{L-1}, \quad s_i \in \mathcal{A} = \{0, 1, \ldots, k-1\}$$

Sets of words are called **formal languages**. One of the main questions in computation theory is how difficult it is to "recognize" a language — that is, to classify any given string as to whether or not it is a member of the set.

---

## 1. Road Maps to Innovation

[Figure 2: The discrete computation hierarchy — see original PDF]

The hierarchy is a partial ordering of descriptive capability. The least powerful models, at the hierarchy's bottom, are those with finite memory — the **finite automata (DFA/NFA)**. At the top are the **universal Turing machines (UTM)** which have infinite random-access tape memories. In between are:
- Context-sensitive languages (recognized by machines with stack memory)
- Languages recognized by machines with linear-bounded memory access

### Two Notions of Computation

1. **"Useful" computation**: The input is the device's initial configuration; performing the computation corresponds to the temporal sequence of state changes; the result is read off in the final state. This involves a semantics of utility.

2. **"Intrinsic" computation**: Focuses on how structures in a device's state space support and constrain information processing. It addresses how computational elements are embedded in a process. It does not ask if the information produced is useful — it divorces the semantics of utility from computation.

---

## 2. Complexity ≠ Randomness

The complexity $C(x)$ of an object $x$ is taken to be the size of its minimal representation $M_{\min}(x)$ when expressed in a chosen vocabulary $\mathcal{V}$:

$$C(x) = |M_{\min}(x)|_{\mathcal{V}}$$

### 2.1 Deterministic Complexity

The **Kolmogorov-Chaitin complexity** $K(x)$ of an object $x$ is the number of bits in the smallest program that outputs $x$ when run on a universal deterministic Turing machine (UTM) [45-47].

If $s^L$ is a string of $L$ discrete symbols produced by an information source with Shannon entropy rate $h_\mu$, then the growth rate of the Kolmogorov-Chaitin complexity is:

$$\frac{K(s^L)}{L} \xrightarrow{L \to \infty} h_\mu$$

For chaotic dynamical systems with continuous state variables:

$$K(s^L) \xrightarrow{L \to \infty, \epsilon \to 0} h_\mu L$$

where the continuous variables are coarse-grained at resolution $\epsilon$.

**Conclusion:** $K(x)$ is a measure of randomness of the object $x$ and, by implication, of randomness in the process which produced it [50].

### 2.2 Statistical Complexity

The **statistical complexity** $C_\mu(x)$ discounts the computational effort the UTM expends in simulating random bits in $x$.

**Key properties:**
- An ideal random object has $C_\mu(x) = 0$
- Simple periodic processes have $C_\mu(x) = 0$
- The statistical complexity is low for both (simple) periodic and ideal random processes

The relationship between the complexities:

$$K(s^L) \approx C_\mu(s^L) + h_\mu L$$

**Interpretation:** $C_\mu$ is the minimum amount of historical information required to make optimal forecasts of bits in $x$ at the error rate $h_\mu$. It is a measure of structure above and beyond that describable as ideal randomness.

### 2.3 Complexity Metrics

[Figure 3: The Bernoulli-Turing Machine (BTM) — see original PDF]

The **Bernoulli-Turing machine (BTM)** is a deterministic Turing machine augmented by contact to an information source — a heat bath. It defines the most general model of discrete stochastic sequential computation.

[Figure 4: Deterministic vs. Statistical Complexity — see original PDF]

- **(a) Deterministic complexity** is a monotonically increasing function of the degree of ideal randomness in a process
- **(b) Statistical complexity** is zero at both extremes and maximized in the middle — "complex" processes are combinations of ordered and stochastic computational elements

---

## 3. ε-Machine Reconstruction

How can an agent detect structure — in particular, computation — in its measurements of the environment?

### Causal States

The goal for the agent is to detect the "hidden" states $\mathcal{S} = \{S_0, S_1, \ldots, S_{|\mathcal{S}|-1}\}$ in its sensory data stream that can help it predict the environment. The states so detected will be called **"causal" states**.

**Definition:** A causal state is the set of subsequences that render the future conditionally independent of the past. The agent identifies a state at different times in a data stream as being in identical conditions of knowledge about the future [24].

[Figure 5: Morph-equivalence induces conditionally-independent states — see original PDF]

Consider two parts of a data stream $s = \ldots s_{-2} s_{-1} s_0 s_1 s_2 \ldots$:
- Forward sequence: $\vec{s}_t = s_t s_{t+1} s_{t+2} \ldots$
- Reverse sequence: $\overleftarrow{s}_t = \ldots s_{t-3} s_{t-2} s_{t-1} s_t$

**Equivalence relation:** $t \sim t'$ if and only if $\Pr(\vec{s} | \overleftarrow{s}_t) = \Pr(\vec{s} | \overleftarrow{s}_{t'})$

The pair $M = (\mathcal{S}, T)$ is referred to as an **ε-machine**, where:
- $\mathcal{S}$ is the set of causal states
- $T : \mathcal{S} \to \mathcal{S}$ is the state transition function

The procedure that begins with a data stream and estimates the number of states and their transition structure and probabilities is referred to as **ε-machine reconstruction** [24].

### What ε-Machines Represent

1. By definition, the machines give the minimal information dependency between morphs — they represent the **causal structure** of events
2. ε-machine reconstruction produces **minimal models** up to the given prediction error level
3. **Time** is the natural ordering captured by ε-machines

---

## 4. Measuring Predictability and Structure

### Shannon Entropy Rate

The **entropy rate** $h_\mu$ measures the rate at which the environment appears to produce information:

$$h_\mu = \lim_{L \to \infty} \frac{H[\Pr(s^L)]}{L}$$

where $H$ is the average of the self-information $-\log_2 \Pr(s^L)$ over $\Pr(s^L)$.

Using the agent's current set $\mathcal{S}$ of inferred causal states:

$$h_\mu = H(\Pr(s|S))$$

### Topological Complexity

The **topological complexity** $C_0$ is given by the minimal number of causal states:

$$C_0 = \log_2 |\mathcal{S}|$$

### Statistical Complexity

The transition probability matrix $\mathbf{T}$ determines the asymptotic causal state probabilities as its left eigenvector:

$$\mathbf{p}_\mathcal{S} \mathbf{T} = \mathbf{p}_\mathcal{S}$$

The **statistical complexity** is:

$$C_\mu = H(\mathbf{p}_\mathcal{S})$$

If the machine is minimal, then $C_\mu$ is the amount of memory (in bits) required for the agent to predict the environment at the given level of accuracy [24].

---

# Part III: Toward a Mathematical Theory of Innovation

## 1. Reconstructing Language Hierarchies

**Innovation** is associated with a change in model class — the computational equivalent of speciation. Innovation is the improvement in an agent's notion of environmental (causal) state.

### Hierarchical ε-Machine Reconstruction

[Table 1: A causal time-series modeling hierarchy — see original PDF]

The procedure:
1. Start at the lowest level by building stochastic finite automata via ε-machine reconstruction
2. At any given level, if the approximations continue increasing in size as more data and resources are used in improving the model's accuracy, then "innovate" a new class when the current representation hits the limits of the agent's computational resources

The innovation step is the evolutionary dynamic that moves from less to more capable model classes by looking for similarities between state-groups within the lower level models. The effective dynamic is one of **increasing abstraction**.

---

## 2. At Each Level in a Hierarchy

At each level in a hierarchy there are common elements:

1. **Symmetries** reflecting the agent's assumptions about the environment's structure
2. **Models** $M$ consisting of states and transitions observed via measurements
3. **Languages** being the ensembles of finitely representable behaviors
4. **Reconstruction**: $M = [s]_{\sim}$ (factoring out a symmetry from a data stream)
5. **Complexity**: $C_\mu(s|\mathcal{M}) = |M_{\min}|$
6. **Predictability** estimated with reference to the distinguishable states

It is crucial that reconstructed models $M$ be **minimal** — so that $M$ contains no more structure than and no additional properties beyond those in the environment.

---

## 3. The ε-Machine Hierarchy

**Definition:** An ε-machine is that:
- Minimal model at the
- Least computationally powerful level yielding a
- Finite description

### Meta-Reconstruction Algorithm

1. At the lowest level, the data stream is its own model: $M_0 = s$. Set $l = 1$.
2. Reconstruct the level $l$ model $M_l$ from the lower level model by factoring out regularities: $M_l = [M_{l-1}]_{\sim}$
3. Test the parsimony of the $l$-level class's descriptive capability by estimating successively more accurate models
4. If the model complexity diverges ($|M_l| \xrightarrow{\epsilon \to 0} \infty$), then set $l \leftarrow l+1$ and go back to step 2
5. If $|M_l| \xrightarrow{\epsilon \to 0} < \infty$, then an ε-machine has been reconstructed. Quit.

---

## 4. The Threshold of Innovation

**When should innovation occur?** A basic premise is that an agent can only call upon finite resources. Innovation should occur as the agent's modeling capacity $\mathcal{A}$ is approached by the complexity of the agent's internal model $|M|$.

The **innovation rate** at level $l$:

$$\gamma_l = \lim_{\epsilon \to 0} \frac{C_l^{(\epsilon/2)} - C_l^{(\epsilon)}}{\log_2 2}$$

This monitors the increase in model size. If $\gamma_l > 0$, the model size at level $l$ diverges and the agent will have to innovate a new model class.

**Consequence:** When confronted with hierarchical processes, finite computational resources fuel the drive toward higher complexity — toward agents with internal models of increasing computational power.

---

## 5. Examples of Hierarchical Learning

### 5.1 The Cost of Chaos

#### Intrinsic Computation in the Period-Doubling Cascade

[Figure 6: Statistical complexity $C_\mu$ versus specific entropy $H(L)/L$ for the period-doubling route to chaos — see original PDF]

The logistic map: $x_{n+1} = f(x_n) = rx(1-x)$

Key results:
- For processes with $H(L)/L < H_c$: $C_\mu = H$ (periodic regime)
- For processes with $H(L)/L > H_c$: More complex relationship (chaotic regime)
- The **latent complexity** of the transition: $\Delta C = C'' - C' \approx 0.7273$ bits

[Figure 7-8: Critical ε-machine at the period-doubling onset of chaos — see original PDF]

At the onset of chaos, the computational structure jumps from finitary level to stack automata. The productions are:
- $A \to BB$
- $B \to BA$

#### Intrinsic Computation in Frequency-Locking Route to Chaos

[Figure 9-10: Quasiperiodic route to chaos — see original PDF]

The circle map: $\theta_{n+1} = \omega + \theta_n + \frac{k}{2\pi} \sin(2\pi\theta_n) \mod 1$

At the golden mean critical winding number, the **Fibonacci machine** emerges with productions:
- $A \to AB$
- $B \to A$

[Table 2: Contents of the Fibonacci machine registers — see original PDF]

### 5.2 The Cost of Indeterminism

[Figure 11-16: Nondeterministic source and its causal representation — see original PDF]

A stochastic nondeterministic finite automaton (hidden Markov model) can lead to an **infinite** causal representation even when the underlying process is simple.

**Result:** The penalty for the "wrong" instrumentation is infinite complexity. This indicates strong selection pressure on the quality of an agent's sensory apparatus.

### 5.3 The Finitary Stochastic Hierarchy

[Figure 17-18: Stochastic computation hierarchy — see original PDF]

The hierarchy for finite-memory stochastic processes:
- Below Measure-Support line: Nonstochastic classes (DFA, NFA, etc.)
- Above Measure-Support line: Stochastic classes (SDFA, SDA variants)

Key insight: DFA ≈ NFA topologically, but SDFA ⊂ SNFA when probabilities are added.

### 5.4 The Costs of Spatial Coherence and Distortion

[Figure 19-20: Elementary cellular automata 18 and 54 — see original PDF]

ε-machine reconstruction applied to CA patterns reveals:
- **Domains**: Dynamically homogeneous regions in space-time
- **Domain walls**: Boundaries between domains
- **Particles**: Propagating space-time structures

[Figure 21: Summary of hierarchical learning examples — see original PDF]

---

# Part IV: Observations and Hypotheses

## 1. Complexity as the Interplay of Order and Chaos

Neither order nor randomness are sufficient in and of themselves for the emergence of complexity. Nor is their naive juxtaposition. As Alfred North Whitehead and many before and after him knew, order and randomness are mere components in an ongoing process.

**Critique of "edge of chaos":** Despite proposals for "computation at the edge of chaos" [71], "adaptation toward the edge of chaos" [72], and "life at the edge of chaos" [73], there is absolutely no general need for high computational capability to be near an "edge of chaos". The infinite-memory counter register functionality embedded in the highly chaotic hidden Markov model of Figure 11 is a clear demonstration of this.

More to the point:
- Stability and order are necessary for **information storage**
- Instability is necessary for the **production of information** and its communication

The trade-off between these requirements is much of what computation theory is about.

---

## 2. Evolutionary Mechanics

**Operational definition of emergence:** A process undergoes emergence if at some time the architecture of information processing has changed in such a way that a distinct and more powerful level of intrinsic computation has appeared that was not present in earlier conditions.

### Why Intrinsic Emergence?

"Emergence" is a groundless concept unless it is defined within the context of processes themselves. Emergence defined without this closure leads to an infinite regress of observers detecting patterns of observers detecting patterns... The regress must be folded into the system — it must be immanent in the dynamics.

### Components of Evolutionary Mechanics

[Figure 22: Schematic diagram of an evolutionary hierarchy — see original PDF]

1. **Modeling**: Driven by the need for encapsulation of environmental experience
2. **Computation**: Driven by the need to process sensory information; delimits inferential, predictive, and semantic capabilities
3. **Innovation**: Driven by limited resources; leads to new model classes that use available resources more efficiently

**The evolutionary dynamic:** Species correspond in the realization space to metastable invariant languages — temporary (hyperbolic) fixed points of the evolutionary dynamic. Each species is dual to some subset of environmental regularities (a niche) whose defining symmetries some subpopulation of agents has been able to discover through innovation.

**Conclusion:** The emergence of natural complexity is a manifestly open-ended process. One force of evolution appears as a movement up the inductive hierarchy through successive innovations. This force is driven at each stage by the limited availability of resources.

> "Some new principle of refreshment is required. The art of progress is to preserve order amid change, and to preserve change amid order. Life refuses to be embalmed alive."
>
> — A. N. Whitehead, *Process and Reality* [1]

---

## Key Concepts Summary

| Term | Definition |
|------|------------|
| **ε-machine** | Minimal model at the least computationally powerful level yielding a finite description |
| **Causal state** | Equivalence class of histories with identical conditional distributions over futures |
| **Statistical complexity** $C_\mu$ | Entropy of the causal state distribution; measures memory required for optimal prediction |
| **Entropy rate** $h_\mu$ | Rate of information production; measures irreducible randomness |
| **Innovation** | Transition to a more powerful computational model class when current class yields diverging complexity |
| **Intrinsic emergence** | Emergence where patterns confer functionality within the system itself |
| **Hierarchical ε-machine reconstruction** | Procedure for discovering minimal models by ascending the computational hierarchy |

---

## Acknowledgments

Many thanks are due to Lisa Borland, Don Glaser, Jim Hanson, Blake LeBaron, Dan McShea, Melanie Mitchell, Dan Upper, and Karl Young for helpful discussions and comments on early drafts. This work was partially funded under AFOSR 91-0293 and ONR N00014-92-4024.

---

## References

1. A. N. Whitehead. *Process and Reality*. The Free Press, New York, corrected edition, 1978.
2. C. W. Reynolds. Flocks, herds, and schools: A distributed behavioral model. *Computer Graphics*, 21:25–34, 1987.
3. B. Hölldobler and E. O. Wilson. *The Ants*. Belknap Press of Harvard University Press, 1990.
4. E. F. Fama. Efficient capital markets II. *J. Finance*, 46:1575–1617, 1991.
5. E. Land. The retinex. *Am. Scientist*, 52:247–264, 1964.
6. B. A. Wandell. Color appearance: The effects of illumination and spatial pattern. *Proc. Nat. Acad. Sci.*, 10:2458–2470, 1993.
7. I. Kovacs and B. Julesz. A closed curve is much more than an incomplete one. *Proc. Nat. Acad. Sci.*, 90:7495–7497, 1993.
8. J. P. Crutchfield, N. H. Packard, J. D. Farmer, and R. S. Shaw. Chaos. *Sci. Am.*, 255:46–57, 1986.
9. H. L. Swinney and J. P. Gollub, editors. *Hydrodynamic Instabilities and the Transition to Turbulence*. Springer Verlag, 1981.
10. A. M. Turing. The chemical basis of morphogenesis. *Trans. Roy. Soc.*, Series B, 237:5, 1952.
11. A. T. Winfree. *The Geometry of Biological Time*. Springer-Verlag, 1980.
12. Q. Ouyang and H. L. Swinney. Transition from a uniform state to hexagonal and striped Turing patterns. *Nature*, 352:610–612, 1991.
13. H. E. Stanley. *Introduction to Phase Transitions and Critical Phenomena*. Oxford University Press, 1971.
14. P. Bak and K. Chen. Self-organized criticality. *Physica A*, 163:403–409, 1990.
15. J. J. Binney, N. J. Dowrick, A. J. Fisher, and M. E. J. Newman. *The Theory of Critical Phenomena*. Oxford University Press, 1992.
16. D. W. Thompson. *On Growth and Form*. Cambridge University Press, 1917.
17. H. Meinhardt. *Models of Biological Pattern Formation*. Academic Press, 1982.
18. S. Forrest. Emergent computation. *Physica D*, 42:1–11, 1990.
19. J. G. Kemeny. The use of simplicity in induction. *Phil. Rev.*, 62:391, 1953.
20. C. S. Wallace and D. M. Boulton. An information measure for classification. *Comput. J.*, 11:185, 1968.
21. J. Rissanen. Modeling by shortest data description. *Automatica*, 14:462, 1978.
22. J. P. Crutchfield and B. S. McNamara. Equations of motion from a data series. *Complex Systems*, 1:417–452, 1987.
23. J. Rissanen. *Stochastic Complexity in Statistical Inquiry*. World Scientific, 1989.
24. J. P. Crutchfield and K. Young. Inferring statistical complexity. *Phys. Rev. Let.*, 63:105–108, 1989.
25. S. Wolfram. Computation theory of cellular automata. *Comm. Math. Phys.*, 96:15, 1984.
26. L. Blum, M. Shub, and S. Smale. On a theory of computation over the real numbers. *Bull. AMS*, 21:1, 1989.
27. M. G. Nordahl. Formal languages and finite cellular automata. *Complex Systems*, 3:63, 1989.
28. J. E. Hanson and J. P. Crutchfield. The attractor-basin portrait of a cellular automaton. *J. Stat. Phys.*, 66:1415–1462, 1992.
29. J. P. Crutchfield. Unreconstructible at any radius. *Phys. Lett. A*, 171:52–60, 1992.
30. C. Moore. Real-valued, continuous-time computers. Technical Report 93-04-018, Santa Fe Institute, 1993.
31. J. E. Hopcroft and J. D. Ullman. *Introduction to Automata Theory, Languages, and Computation*. Addison-Wesley, 1979.
32. H. R. Lewis and C. H. Papadimitriou. *Elements of the Theory of Computation*. Prentice-Hall, 1981.
33. J. G. Brookshear. *Theory of computation*. Benjamin/Cummings, 1989.
34. J. P. Crutchfield. Semantics and thermodynamics. In *Nonlinear Modeling and Forecasting*, pages 317–359. Addison-Wesley, 1992.
35-44. [Additional references on automata theory and formal languages]
45. G. Chaitin. On the length of programs for computing finite binary sequences. *J. ACM*, 13:145, 1966.
46. A. N. Kolmogorov. Three approaches to the concept of the amount of information. *Prob. Info. Trans.*, 1:1, 1965.
47. R. J. Solomonoff. A formal theory of inductive control. *Info. Control*, 7:224, 1964.
48. C. E. Shannon and W. Weaver. *The Mathematical Theory of Communication*. University of Illinois Press, 1962.
49. A. A. Brudno. Entropy and the complexity of the trajectories of a dynamical system. *Trans. Moscow Math. Soc.*, 44:127, 1983.
50. J. Ford. How random is a coin toss? *Physics Today*, April 1983.
51. C. H. Bennett. Dissipation, information, computational complexity, and the definition of organization. In *Emerging Syntheses in the Sciences*. Addison-Wesley, 1988.
52. J. P. Crutchfield and N. H. Packard. Symbolic dynamics of noisy chaos. *Physica*, 7D:201–223, 1983.
53. R. Shaw. *The Dripping Faucet as a Model Chaotic System*. Aerial Press, 1984.
54. P. Grassberger. Toward a quantitative theory of self-generated complexity. *Intl. J. Theo. Phys.*, 25:907, 1986.
55. D. Angluin and C. H. Smith. Inductive inference: Theory and methods. *Comp. Surveys*, 15:237, 1983.
56. J. P. Crutchfield and K. Young. Computation at the onset of chaos. In *Entropy, Complexity, and the Physics of Information*, pages 223–269. Addison-Wesley, 1990.
57. J. P. Crutchfield. Knowledge and meaning... chaos and complexity. In *Modeling Complex Phenomena*, pages 66–101. Springer-Verlag, 1992.
58. J. P. Crutchfield. Reconstructing language hierarchies. In *Information Dynamics*, pages 45–60. Plenum, 1991.
59. J. P. Crutchfield and D. R. Upper. In preparation, 1994.
60. J. P. Crutchfield and J. E. Hanson. Turbulent pattern bases for cellular automata. *Physica D*, 69:279–301, 1993.
61. M. J. Feigenbaum. Universal behavior in nonlinear systems. *Physica*, 7D:16, 1983.
62. L. P. Kadanoff, M. J. Feigenbaum, and S. J. Shenker. Quasiperiodicity in dissipative systems. *Physica*, 5D:370, 1982.
63. J. P. Crutchfield. Observing complexity and the complexity of observation. In *Inside versus Outside*, pages 235–272. Springer-Verlag, 1994.
64. D. Blackwell and L. Koopmans. On the identifiability problem for functions of Markov chains. *Ann. Math. Statist.*, 28:1011, 1957.
65. H. Ito, S.-I. Amari, and K. Kobayashi. Identifiability of hidden Markov information sources. *IEEE Info. Th.*, 38:324, 1992.
66. J. P. Crutchfield and J. E. Hanson. Attractor vicinity decay for a cellular automaton. *CHAOS*, 3(2):215–224, 1993.
67. J. E. Hanson. *Computational Mechanics of Cellular Automata*. PhD thesis, University of California, Berkeley, 1993.
68. N. Boccara, J. Nasser, and M. Roger. Particle-like structures in spatio-temporal patterns. *Phys. Rev. A*, 44:866–875, 1991.
69. B. Russell. *A History of Western Philosophy*. Simon and Schuster, 1945.
70. T. S. Kuhn. *The Structure of Scientific Revolutions*. University of Chicago Press, 1962.
71. C. G. Langton. Computation at the edge of chaos. In *Emergent Computation*. North-Holland, 1990.
72. N. H. Packard. Adaptation toward the edge of chaos. In *Dynamic Patterns in Complex Systems*, pages 293–301. World Scientific, 1988.
73. S. A. Kauffman. *Origins of Order*. Oxford University Press, 1993.
74. M. Mitchell, P. Hraber, and J. P. Crutchfield. Revisiting the edge of chaos. *Complex Systems*, 7:89–130, 1993.
75. J. Maynard-Smith. *Evolutionary Genetics*. Oxford University Press, 1989.
76. J. Monod. *Chance and Necessity*. Vintage Books, 1971.
77. S. J. Gould. *Wonderful Life*. Norton, 1989.
78. C. H. Waddington. *The Strategy of the Genes*. Allen and Unwin, 1957.
79. B. Goodwin. Evolution and the generative order. In *Theoretical Biology*, pages 89–100. Johns Hopkins University Press, 1992.
80. W. Fontana and L. Buss. What would be conserved if the tape were played twice? *Proc. Nat. Acad. Sci.*, 91:757–761, 1994.
81. W. Fontana and L. Buss. "The Arrival of the Fittest". *Bull. Math. Bio.*, 56:1–64, 1994.
82. B. Goodwin and P. Sanders, editors. *Theoretical Biology*. Johns Hopkins University Press, 1992.
83. L. J. Fogel, A. J. Owens, and M. J. Walsh. *Artificial Intelligence through Simulated Evolution*. Wiley, 1966.
84. J. H. Holland. *Adaptation in Natural and Artificial Systems*. MIT Press, 1992.
