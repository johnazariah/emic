# Computational Mechanics: Pattern and Prediction, Structure and Simplicity

**Authors:** Cosma Rohilla Shalizi and James P. Crutchfield
**Affiliation:** Santa Fe Institute, 1399 Hyde Park Road, Santa Fe, NM 87501
**Email:** {shalizi, chaos}@santafe.edu
**Permanent Address:** Physics Department, University of Wisconsin, Madison, WI 53706
**Source:** arXiv:cond-mat/9907176v2, 19 June 2000
**Report:** Santa Fe Institute Working Paper 99-07-044

---

## Abstract

Computational mechanics, an approach to structural complexity, defines a process's causal states and gives a procedure for finding them. We show that the causal-state representation—an ε-machine—is the minimal one consistent with accurate prediction. We establish several results on ε-machine optimality and uniqueness and on how ε-machines compare to alternative representations. Further results relate measures of randomness and structural complexity obtained from ε-machines to those from ergodic and information theories.

**Keywords:** complexity, computation, entropy, information, pattern, statistical mechanics

**PACS:** 02.50.Wp, 05.45, 05.65+b, 89.70.+c

---

## Contents

- **I. Introduction**
- **II. Patterns**
  - A. Algebraic Patterns
  - B. Turing Mechanics: Patterns and Effective Procedures
  - C. Patterns with Error
  - D. Randomness: The Anti-Pattern?
  - E. Causation
  - F. Synopsis of Pattern
- **III. Paddling around Occam's Pool**
  - A. Hidden Processes
  - B. The Pool
  - C. A Little Information Theory
  - D. Patterns in Ensembles
  - E. The Lessons of History
  - F. Minimality and Prediction
- **IV. Computational Mechanics**
  - A. Causal States
  - B. Causal State-to-State Transitions
  - C. ε-Machines
- **V. Optimalities and Uniqueness**
- **VI. Bounds**
- **VII. Concluding Remarks**
- **Appendices A–G**
- **References**
- **Glossary of Notation**

---

# I. Introduction

Organized matter is ubiquitous in the natural world, but the branch of physics which ought to handle it—statistical mechanics—lacks a coherent, principled way of describing, quantifying, and detecting the many different kinds of structure nature exhibits. Statistical mechanics has good measures of disorder in thermodynamic entropy and in related quantities, such as the free energies. When augmented with theories of critical phenomena and pattern formation, it also has an extremely successful approach to analyzing patterns formed through symmetry breaking, both in equilibrium and, more recently, outside it. Unfortunately, these successes involve many ad hoc procedures—such as guessing relevant order parameters, identifying small parameters for perturbation expansion, and choosing appropriate function bases for spatial decomposition. It is far from clear that the present methods can be extended to handle all the many kinds of organization encountered in nature, especially those produced by biological processes.

**Computational mechanics** is an approach that lets us directly address the issues of pattern, structure, and organization. While keeping concepts and mathematical tools already familiar from statistical mechanics, it is distinct from the latter and complementary to it. In essence, from either empirical data or from a probabilistic description of behavior, it shows how to infer a model of the hidden process that generated the observed behavior. This representation—the **ε-machine**—captures the patterns and regularities in the observations in a way that reflects the causal structure of the process. Usefully, with this model in hand, one can extrapolate beyond the original observational data to make predictions of future behavior. Moreover, in a well defined sense that is the subject of the following, the ε-machine is the unique maximally efficient model of the observed data-generating process.

ε-Machines themselves reveal, in a very direct way, how information is stored in the process, and how that stored information is transformed by new inputs and by the passage of time. This, and not using computers for simulations and numerical calculations, is what makes computational mechanics "computational", in the sense of "computation theoretic".

The basic ideas of computational mechanics were introduced a decade ago [6]. Since then they have been used to analyze dynamical systems [7,8], cellular automata [9], hidden Markov models [10], evolved spatial computation [11], stochastic resonance [12], globally coupled maps [13], and the dripping faucet experiment [14]. Despite this record of successful application, there has been some uncertainty about the mathematical foundations of the subject. In particular, while it seemed evident from construction that an ε-machine captured the patterns inherent in a process and did so in a minimal way, no explicit proof of this was published. Moreover, there was no proof that, if the ε-machine was optimal in this way, it was the unique optimal representation of a process. These little-needed gaps have now been filled.

**Main Results:** Subject to some (reasonable) restrictions on the statistical character of a process, we prove that the ε-machine is indeed the unique optimal causal model.

---

# II. Patterns

To introduce our approach to—and even to argue that some approach is necessary for—discovering and describing patterns in nature we begin by quoting Jorge Luis Borges on the "Celestial Emporium of Benevolent Knowledge":

> "These ambiguities, redundancies, and deficiencies recall those attributed by Dr. Franz Kuhn to a certain Chinese encyclopedia entitled *Celestial Emporium of Benevolent Knowledge*. On those remote pages it is written that animals are divided into (a) those that belong to the Emperor, (b) embalmed ones, (c) those that are trained, (d) suckling pigs, (e) mermaids, (f) fabulous ones, (g) stray dogs, (h) those that are included in this classification, (i) those that tremble as if they were mad, (j) innumerable ones, (k) those drawn with a very fine camel's hair brush, (l) others, (m) those that have just broken a flower vase, (n) those that resemble flies from a distance."

What makes the Celestial Emporium's scheme inherently unsatisfactory, and not just strange, is that it tells us nothing about animals. We want to find patterns in a process that "divide it at the joints, as nature directs, not breaking any limbs in half as a bad carver might" [Plato, *Phaedrus*, Sec. 265D].

Computational mechanics is not directly concerned with pattern formation per se; though we suspect it will ultimately be useful in that domain. Nor is it concerned with pattern recognition as a practical matter. Instead, it is concerned with the questions of **what patterns are** and **how patterns should be represented**. One way to highlight the difference is to call this **pattern discovery**, rather than pattern recognition.

## A. Algebraic Patterns

Perhaps the first attempt to make the notion of "pattern" mathematically rigorous was that of Whitehead and Russell in *Principia Mathematica*. They viewed pattern as a property, not of sets, but of relations within or between sets. In this framework relations share a common pattern or structure if they have the same **relation-number**. For instance, all square lattices have similar structure since their elements share the same neighborhood relation; as do all hexagonal lattices. Hexagonal and square lattices, however, exhibit different patterns since they have non-isomorphic neighborhood relations.

A more recent approach builds on **semi-group theory** and its Krohn-Rhodes decomposition theorem. Rhodes and Nehaniv have tried to apply semi-group complexity theory to biological evolution [31], suggesting that the complexity of a biological structure can be measured by the number of subgroups in the decomposition of an automaton that describes the structure.

## B. Turing Mechanics: Patterns and Effective Procedures

The approach of Kolmogorov and Chaitin focuses on the exact reproduction of an individual object. The candidates for expressing the pattern P are universal Turing machine (UTM) programs—specifically, the shortest UTM program that can exactly produce the object O. This program's length is called O's **Kolmogorov-Chaitin complexity**.

Consider the first $n$ symbols $O_n$ of $O$ and the shortest program $P_n$ that produces them. We ask, What happens to the limit:

$$\lim_{n \to \infty} \frac{|P_n|}{n}$$

where $|P|$ is the length in bits of program $P$?

- If this limit vanishes, $O$ is eminently **compressible**
- If the limit goes to 1, we have a completely **incompressible** description and conclude that $O$ is **random**

There are many well-known difficulties with applying Kolmogorov complexity to natural processes:
1. It is **uncomputable** in general, owing to the halting problem
2. It is **maximal for random sequences**
3. It only applies to a **single sequence**
4. It makes **no allowance for noise or error**
5. Computational resources needed may grow without bound

## C. Patterns with Error

An obvious next step is to allow our pattern $P$ some degree of approximation or error, in exchange for shorter descriptions. Given the ubiquity of noise in nature, this is a small price to pay.

Dennett notes that there is generally a trade-off between the simplicity of a predictor and its accuracy, and he plausibly describes **emergent phenomena** as patterns that allow for a large reduction in complexity for only a small reduction in accuracy.

## D. Randomness: The Anti-Pattern?

Some approaches to complexity conflate "structure" with the opposite of randomness. In contrast, we see pattern—structure, organization, regularity—as describing a coordinate **"orthogonal"** to a process's degree of randomness. That is, complexity (in our sense) and randomness each capture a useful property necessary to describe how a process manipulates information. This complementarity is even codified by the **complexity-entropy diagrams** introduced in [6].

## E. Causation

We want our representations of patterns in dynamical processes to be **causal**—to say how one state of affairs leads to or produces another. Causality enters our development in an extremely weak sense, the weakest one can use mathematically, which is Hume's: one class of event causes another if the latter always follows the former; the effect invariably succeeds the cause. We replace this invariant-succession notion with a more probabilistic one, substituting a homogeneous distribution of successors for the solitary invariable successor.

## F. Synopsis of Pattern

The ideal, synthesizing approach to patterns would be:

1. **Algebraic**, giving us an explicit breakdown or decomposition of the pattern into its parts
2. **Computational**, showing how the process stores and uses information
3. **Calculable**, analytically or by systematic approximation
4. **Causal**, telling us how instances of the pattern are actually produced
5. **Naturally stochastic**, explicitly formulated in terms of ensembles

This mix is precisely the brew we claim, in all modesty, to have on tap.

---

# III. Paddling around Occam's Pool

Here a pattern $P$ is something knowledge of which lets us predict, at better than chance rates, if possible, the future of sequences drawn from an ensemble $O$: $P$ has to be statistically accurate and confer some leverage or advantage as well.

## A. Hidden Processes

We restrict ourselves to **discrete-valued, discrete-time stationary stochastic processes**.

**Definition 1 (A Process):** Let $\mathcal{A}$ be a countable set. Let $\Omega = \mathcal{A}^{\mathbb{Z}}$ be the set of bi-infinite sequences composed from $\mathcal{A}$, $T_i: \Omega \mapsto \mathcal{A}$ be the function that returns the $i$th element $s_i$ of a bi-infinite sequence $\omega \in \Omega$, and $\mathcal{F}$ the field of cylinder sets of $\Omega$. Adding a probability measure $P$ gives us a probability space $(\Omega, \mathcal{F}, P)$, with an associated random variable $\overleftrightarrow{S}$. A process is a sequence of random variables $S_i = T_i(\overleftrightarrow{S})$, $i \in \mathbb{Z}$.

**Definition 2 (Stationarity):** A process $S_i$ is stationary if and only if:

$$P(\overrightarrow{S}_t^L = s^L) = P(\overrightarrow{S}_0^L = s^L)$$

for all $t \in \mathbb{Z}$, $L \in \mathbb{Z}^+$, and all $s^L \in \mathcal{A}^L$.

## B. The Pool

Our goal is to predict all or part of $\overrightarrow{S}$ using some function of some part of $\overleftarrow{S}$. We begin by taking the set $\overleftarrow{\mathcal{S}}$ of all pasts and partitioning it into mutually exclusive and jointly comprehensive subsets. That is, we make a class $R$ of subsets of pasts.

We define a function from histories to effective states:

$$\eta: \overleftarrow{\mathcal{S}} \mapsto R$$

We call the collection of all partitions $R$ of the set of histories $\overleftarrow{\mathcal{S}}$ **Occam's pool**.

## C. A Little Information Theory

### 1. Entropy Defined

Given a random variable $X$ taking values in a countable set $\mathcal{A}$, the **entropy** of $X$ is:

$$H[X] \equiv -\sum_{x \in \mathcal{A}} P(X = x) \log_2 P(X = x)$$

taking $0 \log 0 = 0$. $H[X]$ is measured in bits of information.

### 2. Joint and Conditional Entropies

**Joint entropy:**

$$H[X, Y] \equiv -\sum_{(x,y) \in \mathcal{A} \times \mathcal{B}} P(X = x, Y = y) \log_2 P(X = x, Y = y)$$

**Conditional entropy:**

$$H[X|Y] \equiv H[X, Y] - H[Y]$$

### 3. Mutual Information

$$I[X; Y] \equiv H[X] - H[X|Y]$$

This is the average reduction in uncertainty about $X$ produced by fixing $Y$.

## D. Patterns in Ensembles

**Entropy rate:**

$$h[\overrightarrow{S}] \equiv \lim_{L \to \infty} \frac{1}{L} H[\overrightarrow{S}^L]$$

**Conditional entropy rate:**

$$h[\overrightarrow{S}|X] \equiv \lim_{L \to \infty} \frac{1}{L} H[\overrightarrow{S}^L|X]$$

**Definition 3 (Capturing a Pattern):** $R$ captures a pattern if and only if there exists an $L$ such that:

$$H[\overrightarrow{S}^L|R] < L \cdot H[S]$$

## E. The Lessons of History

**Lemma 1 (Old Country Lemma):** For all $R$ and for all $L \in \mathbb{Z}^+$:

$$H[\overrightarrow{S}^L|R] \geq H[\overrightarrow{S}^L|\overleftarrow{S}]$$

*Remark:* Conditioning on the whole of the past reduces the uncertainty in the future to as small a value as possible. Carrying around the whole semi-infinite past is rather bulky and uncomfortable. We want to forget as much of the past as possible.

## F. Minimality and Prediction

Let's invoke **Occam's Razor**: "It is vain to do with more what can be done with less."

**Definition 4 (Complexity of State Classes):** The statistical complexity of a class $R$ of states is:

$$C_\mu(R) \equiv H[R] = -\sum_{\rho \in R} P(R = \rho) \log_2 P(R = \rho)$$

The statistical complexity of a state class is the average uncertainty (in bits) in the process's current state. This is the same as the average amount of memory (in bits) that the process appears to retain about the past.

**The goal:** Minimize statistical complexity, subject to the constraint of maximally accurate prediction.

---

# IV. Computational Mechanics

> "Those who are good at archery learnt from the bow and not from Yi the Archer. Those who know how to manage boats learnt from the boats and not from Wo."
> — Anonymous, in [64]

The ultimate goal of computational mechanics is to discern the patterns intrinsic to a process. That is, as much as possible, the goal is to let the process describe itself, on its own terms, without appealing to a priori assumptions about the process's structure.

## A. Causal States

**Definition 5 (A Process's Causal States):** The causal states of a process are the members of the range of the function $\epsilon: \overleftarrow{\mathcal{S}} \mapsto 2^{\overleftarrow{\mathcal{S}}}$:

$$\epsilon(\overleftarrow{s}) \equiv \{\overleftarrow{s}' \,|\, P(\overrightarrow{S} = \overrightarrow{s} \,|\, \overleftarrow{S} = \overleftarrow{s}) = P(\overrightarrow{S} = \overrightarrow{s} \,|\, \overleftarrow{S} = \overleftarrow{s}'), \text{ for all } \overrightarrow{s} \in \overrightarrow{\mathcal{S}}, \overleftarrow{s}' \in \overleftarrow{\mathcal{S}}\}$$

We write the $i$th causal state as $S_i$ and the set of all causal states as $\mathcal{S}$; the corresponding random variable is denoted $S$, and its realization $\sigma$.

The cardinality of $\mathcal{S}$ is unspecified. $\mathcal{S}$ can be finite, countably infinite, a continuum, a Cantor set, or something stranger still.

Each causal state $S_i$ has several structures attached:

1. The index $i$—the state's "name"
2. The set of histories that have brought the process to $S_i$, denoted $\{\overleftarrow{s} \in S_i\}$
3. A conditional distribution over futures, denoted $P(\overrightarrow{S}|S_i)$, called the state's **morph**

### 1. Morphs

Each causal state has a unique morph. An immediate consequence of the definition:

$$P(\overrightarrow{S} = \overrightarrow{s} \,|\, S = \epsilon(\overleftarrow{s})) = P(\overrightarrow{S} = \overrightarrow{s} \,|\, \overleftarrow{S} = \overleftarrow{s})$$

**Lemma 2:** The past and the future are independent, conditioning on the causal states.

$$P(\overleftarrow{S} = \overleftarrow{s}, S = \sigma, \overrightarrow{S} = \overrightarrow{s}) = P(\overrightarrow{S} = \overrightarrow{s}|S = \sigma) P(S = \sigma|\overleftarrow{S} = \overleftarrow{s}) P(\overleftarrow{S} = \overleftarrow{s})$$

### 2. Homogeneity

**Definition 6 (Strict Homogeneity):** A set $X$ is strictly homogeneous with respect to a certain random variable $Y$ when the conditional distribution $P(Y|X)$ for $Y$ is the same for all subsets of $X$.

**Definition 7 (Weak Homogeneity):** A set $X$ is weakly homogeneous with respect to $Y$ if $X$ is not strictly homogeneous with respect to $Y$, but $X \setminus X_0$ is, where $X_0$ is a subset of $X$ of measure 0.

**Lemma 3 (Strict Homogeneity of Causal States):** A process's causal states are the largest subsets of histories that are all strictly homogeneous with respect to futures of all lengths.

## B. Causal State-to-State Transitions

**Definition 8 (Causal Transitions):** The labeled transition probability $T_{ij}^{(s)}$ is the probability of making the transition from state $S_i$ to $S_j$ while emitting the symbol $s \in \mathcal{A}$:

$$T_{ij}^{(s)} \equiv P(S' = S_j, \overrightarrow{S}^1 = s \,|\, S = S_i)$$

**Lemma 4 (Transition Probabilities):**

$$T_{ij}^{(s)} = \frac{P(\overleftarrow{s} \in S_i, \overleftarrow{s}s \in S_j)}{P(\overleftarrow{s} \in S_i)}$$

## C. ε-Machines

**Definition 9 (An ε-Machine Defined):** The ε-machine of a process is the ordered pair $\{\epsilon, T\}$, where $\epsilon$ is the causal state function and $T$ is set of the transition matrices for the states defined by $\epsilon$.

Equivalently, we may denote an ε-machine by $\{\mathcal{S}, T\}$.

**Proposition 1 (ε-Machines Are Monoids):** The algebra generated by the ε-machine $\{\epsilon, T\}$ is a semi-group with an identity element, i.e., it is a monoid.

*Remark:* ε-machines can be interpreted as capturing a process's generalized symmetries. Any subgroups of an ε-machine's semi-group are, in fact, symmetries in the more familiar sense.

**Lemma 5 (ε-Machines Are Deterministic):** For each $S_i$ and $s \in \mathcal{A}$, $T_{ij}^{(s)} > 0$ only for that $S_j$ for which $\epsilon(\overleftarrow{s}s) = S_j$ if and only if $\epsilon(\overleftarrow{s}) = S_i$, for all pasts $\overleftarrow{s}$.

*Remark:* In automata theory, a set of states and transitions is said to be deterministic if the current state and the next input together fix the next state.

**Lemma 6 (Causal States Are Independent):** The probability distributions over causal states at different times are conditionally independent.

**Definition 10 (ε-Machine Reconstruction):** ε-Machine reconstruction is any procedure that given a process $P(\overleftrightarrow{S})$, or an approximation of $P(\overleftrightarrow{S})$, produces the process's ε-machine $\{\mathcal{S}, T\}$.

---

# V. Optimalities and Uniqueness

We now show that:
1. Causal states are maximally accurate predictors of minimal statistical complexity
2. They are unique in sharing both properties
3. Their state-to-state transitions are minimally stochastic

**Theorem 1 (Causal States are Maximally Prescient):** For all $R$ and all $L \in \mathbb{Z}^+$:

$$H[\overrightarrow{S}^L|R] \geq H[\overrightarrow{S}^L|S]$$

*Remark:* Causal states are as good at predicting the future—are as prescient—as complete histories. They satisfy the first requirement borrowed from Occam.

**Corollary 1 (Causal States Are Sufficient Statistics):** The causal states $S$ of a process are sufficient statistics for predicting it.

**Definition 11 (Prescient Rivals):** Prescient rivals $\hat{R}$ are states that are as predictive as the causal states; viz., for all $L \in \mathbb{Z}^+$:

$$H[\overrightarrow{S}^L|\hat{R}] = H[\overrightarrow{S}^L|S]$$

**Lemma 7 (Refinement Lemma):** For all prescient rivals $\hat{R}$ and for each $\hat{\rho} \in \hat{R}$, there is a $\sigma \in \mathcal{S}$ and a measure-0 subset $\hat{\rho}_0 \subset \hat{\rho}$, possibly empty, such that $\hat{\rho} \setminus \hat{\rho}_0 \subseteq \sigma$.

*Remark:* Any alternative partition $\hat{R}$ that is as prescient as the causal states must be a refinement of the causal-state partition almost everywhere.

**Theorem 2 (Causal States Are Minimal):** For all prescient rivals $\hat{R}$:

$$C_\mu(\hat{R}) \geq C_\mu(\mathcal{S})$$

*Remark:* No rival pattern, which is as good at predicting the observations as the causal states, is any simpler than the causal states. Occam therefore tells us that there is no reason not to use the causal states.

**Definition 12 (Statistical Complexity of a Process):** The statistical complexity $C_\mu(O)$ of a process $O$ is that of its causal states: $C_\mu(O) \equiv C_\mu(\mathcal{S})$.

**Theorem 3 (Causal States Are Unique):** For all prescient rivals $\hat{R}$, if $C_\mu(\hat{R}) = C_\mu(\mathcal{S})$, then there exists an invertible function between $\hat{R}$ and $\mathcal{S}$ that almost always preserves equivalence of state.

**Theorem 4 (ε-Machines Are Minimally Stochastic):** For all prescient rivals $\hat{R}$:

$$H[\hat{R}'|\hat{R}] \geq H[S'|S]$$

where $S'$ and $\hat{R}'$ are the next causal state and the next η-state, respectively.

*Remark:* There is no more uncertainty in transitions between causal states than there is in the transitions between any other kind of prescient effective states. The causal states approach as closely to perfect determinism as any rival that is as good at predicting the future.

---

# VI. Bounds

**Definition 13 (Excess Entropy):** The excess entropy $E$ of a process is the mutual information between its semi-infinite past and its semi-infinite future:

$$E \equiv I[\overrightarrow{S}; \overleftarrow{S}]$$

**Theorem 5 (The Bounds of Excess):** The statistical complexity $C_\mu$ bounds the excess entropy $E$:

$$E \leq C_\mu$$

with equality if and only if $H[S|\overrightarrow{S}] = 0$.

*Remark:* At first glance, it is tempting to see $E$ as the amount of information stored in a process. $E$ is only a lower bound on the true amount of information the process stores about its history, namely $C_\mu$. We can, however, say that $E$ measures the **apparent information** in the process, since it is defined directly in terms of observed sequences and not in terms of hidden, intrinsic states.

**Corollary 2:** For all prescient rivals $\hat{R}$:

$$E \leq H[\hat{R}]$$

**Lemma 8 (Conditioning Does Not Affect Entropy Rate):** For all prescient rivals $\hat{R}$:

$$h[\overrightarrow{S}] = h[\overrightarrow{S}|\hat{R}]$$

*Remark:* Forcing the process into a certain state $\hat{R} = \hat{\rho}$ is akin to applying a controller, once. But in the infinite-entropy case, the effects of the finite control are simply washed out.

**Theorem 6 (Control Theorem):** Given a class $\hat{R}$ of prescient rivals:

$$H[S] - h[\overrightarrow{S}|\hat{R}] \leq C_\mu$$

where $H[S]$ is the entropy of a single symbol from the observable stochastic process.

*Remark:* The Control Theorem is inspired by, and is a version of, **Ashby's law of requisite variety**.

---

# VII. Concluding Remarks

## A. Discussion

Let's review, informally, what we have shown. We began with questions about the nature of patterns and about pattern discovery. Our examination of these issues led us to want a way of describing patterns that was at once algebraic, computational, intrinsically probabilistic, and causal. We then defined patterns in ensembles, in a very general and abstract sense, as equivalence classes of histories, or sets of hidden states, used for prediction. We defined the strength of such patterns (by their forecasting ability or prescience) and their statistical complexity (by the entropy of the states or the amount of information retained by the process about its history).

Optimal prediction led us to the equivalence relation $\sim_\epsilon$ and the function $\epsilon$ and so to representing patterns by causal states and their transitions—the ε-machine.

**Our first theorem** showed that the causal states are maximally prescient.

**Our second** showed that they are the simplest way of representing the pattern of maximum strength.

**Our third theorem** showed that they are unique in having this double optimality.

**Further results** showed that ε-machines are the least stochastic way of capturing maximum-strength patterns.

### Why are ε-machine states causal?

1. ε-machine architecture delineates the dependency between the morphs $P(\overrightarrow{S}|\overleftarrow{S})$, considered as events in which each new symbol determines the succeeding morph. Thus, if state B follows state A then A is a cause of B and B is an effect of A.

2. ε-machine minimality guarantees that there are no other events that intervene to render A and B independent.

The ε-machine is thus a causal representation of all the patterns in the process. It is maximally predictive and minimally complex. It is at once computational, since it shows how the process stores information (in the causal states) and transforms that information (in the state-to-state transitions), and algebraic.

## B. Limitations of the Current Results

Let's catalogue the restrictive assumptions:

1. We know exact joint probabilities over sequence blocks of all lengths for a process
2. The observed process takes on discrete values
3. The process is discrete in time
4. The process is a pure time series (without spatial extent)
5. The observed process is stationary
6. Prediction can only be based on the process's past, not on any outside source of information

**Possible relaxations:**
- The second limitation (continuous values) probably can be addressed, with a corresponding increase in mathematical sophistication
- The third limitation (continuous time) looks similarly solvable
- For the fourth limitation (spatial extent), tricks exist to make spatially extended systems look like time series
- The assumption of stationarity is unclear how to relax

## C. Conclusions and Directions for Future Work

Computational mechanics aims to understand the nature of patterns and pattern discovery. We hope that the foregoing development has convinced the reader that we are neither being rash when we say that we have laid a foundation for those projects, nor that we are being flippant when we say that patterns are what ε-machines represent and that we discover them by ε-machine reconstruction.

### Two broad avenues for future work:

**1. The mathematics of ε-machines themselves:**
- Measure-theoretic issues relating to the definition of causal states
- Understanding of the measurement-resolution scaling properties for continuous-state processes
- Relation to the Krohn-Rhodes decomposition in automata theory
- The trade-off between prescience and complexity—the "prediction frontier"

**2. ε-Machine reconstruction:**
- Understanding error statistics of different reconstruction procedures
- Finding "confidence regions" for the products of reconstruction
- Calculating:
  - The probabilities of different degrees of reconstruction error for a given volume of data
  - The amount of data needed to be confident of a fixed bound on the error
  - The rates at which different reconstruction procedures converge on the ε-machine

---

# Appendices

## Appendix A: Information-Theoretic Formulæ

The following formulæ prove useful in the development:

| Formula | Description |
|---------|-------------|
| $H[X, Y] = H[X] + H[Y\|X]$ | Chain rule for entropies |
| $H[X, Y] \geq H[X]$ | Joint entropy lower bound |
| $H[X, Y] \leq H[X] + H[Y]$ | Independence bound |
| $H[X\|Y] \leq H[X]$ | Conditioning reduces entropy |
| $H[X\|Y] = H[X]$ iff $X$ is independent of $Y$ | Independence criterion |
| $H[X, Y\|Z] = H[X\|Z] + H[Y\|X, Z]$ | Conditional chain rule |
| $H[X] - H[X\|Y] = H[Y] - H[Y\|X]$ | Symmetry of mutual information |
| $I[X; Y] \leq H[X]$ | Mutual information bound |
| $I[X; Y] = H[X]$ iff $H[X\|Y] = 0$ | Maximum mutual information |
| $H[f(X)] \leq H[X]$ | Functions reduce entropy |
| $H[X\|Y] = 0$ iff $X = f(Y)$ | Deterministic relationship |
| $H[f(X)\|Y] \leq H[X\|Y]$ | Conditional function bound |
| $H[X\|f(Y)] \geq H[X\|Y]$ | Function conditioning |

## Appendix B: The Equivalence Relation that Induces Causal States

Consider the set $\overleftarrow{\mathcal{S}}$ of all past sequences, of any length:

$$\overleftarrow{\mathcal{S}} = \{\overleftarrow{s}^L = s_{L-1} \cdots s_{-1} : s_i \in \mathcal{A}, L \in \mathbb{Z}^+\}$$

We define the relation $\sim_\epsilon$ over $\overleftarrow{\mathcal{S}}$ by:

$$\overleftarrow{s}_i^K \sim_\epsilon \overleftarrow{s}_j^L \Leftrightarrow P(\overrightarrow{S}|\overleftarrow{s}_i^K) = P(\overrightarrow{S}|\overleftarrow{s}_j^L)$$

The relation $\sim_\epsilon$ is an equivalence relation on $\overleftarrow{\mathcal{S}}$ since it is reflexive, symmetric, and transitive. The causal states $\mathcal{S} = \overleftarrow{\mathcal{S}}/\sim_\epsilon$ are the equivalence classes.

## Appendix C: Time Reversal

The causal states obtained by scanning sequences in the opposite direction, $\overrightarrow{\mathcal{S}}/\sim_\epsilon$, follow similarly. In general, $\overleftarrow{\mathcal{S}}/\sim_\epsilon \neq \overrightarrow{\mathcal{S}}/\sim_\epsilon$. That is:
- Past causal states are not necessarily the same as future causal states
- Past and future morphs can differ
- Unlike entropy rate, past and future statistical complexities need not be equal: $\overleftarrow{C}_\mu \neq \overrightarrow{C}_\mu$

The presence or lack of this type of time-reversal symmetry is a fundamental property of a process.

## Appendix D: ε-Machines are Monoids

A **semi-group** is a set of elements closed under an associative binary operator, but without a guarantee that every element has an inverse. A **monoid** is a semi-group with an identity element. We propose to interpret the algebraic structure of a semi-group as a **generalized symmetry**.

The transformations that concatenate strings of symbols from $\mathcal{A}$ onto other such strings form a semi-group $G$, the generators of which are the transformations that concatenate the elements of $\mathcal{A}$. The identity element is provided by concatenating the null symbol $\lambda$.

We call the matrix representation of $G$ the **semi-group machine** of the ε-machine $\{\mathcal{S}, T\}$.

## Appendix F: Finite Entropy for the Semi-Infinite Future

While cases where $H[\overrightarrow{S}]$ is finite may be uninteresting for information-theorists, they are of great interest to physicists, since they correspond to periodic and limit-cycle behaviors.

**Theorem 7 (The Finite-Control Theorem):** For all prescient rivals $\hat{R}$:

$$H[\overrightarrow{S}] - H[\overrightarrow{S}|\hat{R}] \leq C_\mu$$

## Appendix G: Relations to Other Fields

### G.1 Time Series Modeling

The goal of time series modeling is to predict the future of a measurement series on the basis of its past. We have shown that the best $\eta$ is, unambiguously, $\epsilon$.

### G.2 Decision-Theoretic Problems

If we simply aim to predict the process indefinitely far into the future, then because the causal states are minimal sufficient statistics for the distribution of futures, the optimal rule of behavior will use $\epsilon$.

### G.3 Stochastic Processes

Perhaps the closest approach to the spirit of computational mechanics in the stochastic process literature is the classical theory of **optimal prediction and filtering** developed by Wiener and Kolmogorov. The two theories share the use of information-theoretic notions, the unification of prediction and structure, and the conviction that "the statistical mechanics of time series" is relevant to understanding living organisms.

### G.4 Formal Language Theory and Grammatical Inference

For regular languages, relatives of our minimality and uniqueness theorems are well known, and the construction of causal states is analogous to the **"Nerode equivalence classing"** procedure. Our theorems, however, are not restricted to this low-memory, non-stochastic setting.

### G.5 Computational and Statistical Learning Theory

One of the goals of computational mechanics is, exactly, discovering the best representation. In a sense, computational mechanics' focus on causal states is a search for a particular kind of structural decomposition for a process, reflected in the conditional independence of past and future that causal states induce.

### G.6 Description-Length Principles and Universal Coding Theory

The construction of causal states is somewhat similar to the states estimated in Rissanen's **context algorithm**. Despite the similarities, there are significant differences. We avoid any reference to encodings of rival models or to prior distributions over them; $C_\mu(R)$ is not a description length.

### G.7 Measure Complexity

Grassberger proposed that the appropriate measure of the complexity of a process was the "minimal average Shannon information needed" for optimal prediction. This is a position closely allied to that of computational mechanics.

### G.8 Hierarchical Scaling Complexity

This approach seeks to extend certain traditional ideas of statistical physics by constructing a hierarchy of $n$th-order Markov models and examining the convergence of their predictions.

### G.9 Continuous Dynamical Computing

Using dynamical systems as computers has become increasingly attractive. One of the central questions of computational mechanics is exactly the converse: given a dynamical system, how can one detect what it is intrinsically computing?

---

# Key Concepts Summary

| Term | Definition |
|------|------------|
| **ε-machine** | Ordered pair $\{\epsilon, T\}$ where $\epsilon$ is the causal state function and $T$ is the set of transition matrices |
| **Causal state** | Equivalence class of histories with identical conditional distributions over futures |
| **Morph** | The conditional distribution over futures associated with a causal state |
| **Statistical complexity** $C_\mu$ | Entropy of the causal state distribution; measures memory retained about the past |
| **Entropy rate** $h_\mu$ | Rate of information production; measures irreducible randomness |
| **Excess entropy** $E$ | Mutual information between past and future; lower bound on $C_\mu$ |
| **Prescient rival** | Any state partition that is as predictive as the causal states |
| **Occam's pool** | The collection of all possible partitions of histories |

---

## Glossary of Notation

| Symbol | Description |
|--------|-------------|
| $O$ | Object in which we wish to find a pattern |
| $P$ | Pattern in $O$ |
| $\mathcal{A}$ | Countable alphabet |
| $\overleftrightarrow{S}$ | Bi-infinite, stationary, discrete stochastic process on $\mathcal{A}$ |
| $\overrightarrow{S}^L$ | Random variable for the next $L$ values |
| $\overleftarrow{S}^L$ | Random variable for the last $L$ values up to the present |
| $\overrightarrow{S}$ | Semi-infinite future |
| $\overleftarrow{S}$ | Semi-infinite past |
| $\lambda$ | Null string or null symbol |
| $\overleftarrow{\mathcal{S}}$ | Set of all pasts realized by the process |
| $R$ | Partition of $\overleftarrow{\mathcal{S}}$ into effective states |
| $\rho$ | Member-class of $R$; a particular effective state |
| $\eta$ | Function from $\overleftarrow{\mathcal{S}}$ to $R$ |
| $H[X]$ | Entropy of the random variable $X$ |
| $H[X,Y]$ | Joint entropy of $X$ and $Y$ |
| $H[X\|Y]$ | Entropy of $X$ conditioned on $Y$ |
| $I[X;Y]$ | Mutual information of $X$ and $Y$ |
| $h_\mu[\overrightarrow{S}]$ | Entropy rate of $\overrightarrow{S}$ |
| $C_\mu(R)$ | Statistical complexity of $R$ |
| $\mathcal{S}$ | Set of the causal states |
| $\sigma$ | Particular causal state |
| $\epsilon$ | Function from histories to causal states |
| $S$ | Current causal state, as a random variable |
| $\sim_\epsilon$ | Relation of causal equivalence between two histories |
| $T_{ij}^{(s)}$ | Probability of going from causal state $i$ to $j$, emitting $s$ |
| $\hat{R}$ | Set of prescient rival states |
| $C_\mu(O)$ | Statistical complexity of the process $O$ |
| $E$ | Excess entropy |

---

## References

1. J. M. Yeomans. *Statistical Mechanics of Phase Transitions*. Clarendon Press, Oxford, 1992.
2. P. Manneville. *Dissipative Structures and Weak Turbulence*. Academic Press, 1990.
3. P. M. Chaikin and T. C. Lubensky. *Principles of Condensed Matter Physics*. Cambridge, 1995.
4. M. C. Cross and P. Hohenberg. Pattern Formation Out of Equilibrium. *Rev. Mod. Phys.*, 65:851–1112, 1993.
5. J. P. Crutchfield. The calculi of emergence. *Physica D*, 75:11–54, 1994.
6. J. P. Crutchfield and K. Young. Inferring statistical complexity. *Phys. Rev. Lett.*, 63:105–108, 1989.
7. J. P. Crutchfield and K. Young. Computation at the onset of chaos. In Zurek [131], pages 223–269.
8. N. Perry and P.-M. Binder. Finite statistical complexity for sofic systems. *Phys. Rev. E*, 60:459–463, 1999.
9. J. E. Hanson and J. P. Crutchfield. Computational mechanics of cellular automata. *Physica D*, 103:169–189, 1997.
10. D. R. Upper. *Theory and Algorithms for Hidden Markov Models and Generalized Hidden Markov Models*. PhD thesis, UC Berkeley, 1997.
11. J. P. Crutchfield and M. Mitchell. The evolution of emergent computation. *PNAS*, 92:10742–10746, 1995.
12. A. Witt, A. Neiman, and J. Kurths. *Phys. Rev. E*, 55:5050–5059, 1997.
13. J. Delgado and R. V. Solé. *Phys. Rev. E*, 55:2338–2344, 1997.
14. W. M. Gonçalves et al. *Physica A*, 257:385–389, 1998.
15. J. P. Crutchfield and C. R. Shalizi. Thermodynamic depth of causal states. *Phys. Rev. E*, 59:275–283, 1999.
16. J. L. Borges. *Other Inquisitions, 1937–1952*. University of Texas Press, 1964.
17. J. P. Crutchfield. Semantics and thermodynamics. In *Nonlinear Modeling and Forecasting*, pages 317–359, 1992.
[18–131: Additional references available in original document]

---

## Acknowledgments

Thanks to Dave Albers, Dave Feldman, Jon Fetter, Rob Haslinger, Wim Hordijk, Amihan Huesmann, Cris Moore, Mitch Porter, Erik van Nimwegen, and Karl Young for advice on the manuscript. This work was supported at the Santa Fe Institute under the Computation, Dynamics, and Inference Program via ONR grant N00014-95-1-0975, NSF grant PHY-9970158, and DARPA contract F30602-00-2-0583.
