# Strong and Weak Optimizations in Classical and Quantum Models of Stochastic Processes

**Source:** loomis2019strong
**Author:** James P. Crutchfield
**Pages:** 14

---

## Full Text

                                                                                                                                                            arXiv:1809.XXXX


                                                                                       Strong and Weak Optimizations
                                                                                      in Classical and Quantum Models
                                                                                           of Stochastic Processes
                                                                                     Samuel Loomis∗ and James P. Crutchfield†
                                                                                Complexity Sciences Center and Physics Department,
                                                                      University of California at Davis, One Shields Avenue, Davis, CA 95616
                                                                                               (Dated: August 28, 2018)
                                                             Among the predictive hidden Markov models that describe a given stochastic process, the -machine
                                                          is strongly minimal in that it minimizes every Rényi-based memory measure. Quantum models
                                                          can be smaller still. In contrast with the -machine’s unique role in the classical setting, however,
                                                          among the class of processes described by pure-state hidden quantum Markov models, there are
                                                          those for which there does not exist any strongly minimal model. Quantum memory optimization
arXiv:1808.08639v1 [quant-ph] 26 Aug 2018


                                                          then depends on which memory measure best matches a given problem circumstance.

                                                          PACS numbers: 05.45.-a 89.75.Kd 89.70.+c 05.45.Tp


                                                               I.   INTRODUCTION                                  processes; often the advantage is unbounded [10–13]. For
                                                                                                                  quantum models, the minimal memory rate Cq has been
                                            When studying classical stochastic processes, we often                determined in cases such as the Ising model [11] and the
                                            seek models and representations of the underlying system              Perturbed Coin Process [14], where the q-machine attains
                                            that allow us to simulate and predict future dynamics.                the minimum rate. And so, though a given q-machine’s Cq
                                            If the process is memoryful, then models that generate                can be readily calculated [15], in many cases the absolute
                                            it or predict its future actions must also have memory.               minimum Cq is not known.
                                            Memory, however, comes at some resource cost; both                    Properly accounting for memory requires an appropriate
                                            in a practical sense—consider, for instance, the substan-             formalism for resources themselves. The field of resource
                                            tial resources required to generate predictions of weather            theory has recently emerged in quantum information the-
                                            and climate [1, 2]—and in a theoretical sense—seen in                 ory as a toolkit for addressing resource consumption in
                                            analyzing thermodynamic systems such as information                   the contexts of entanglement, thermodynamics, and nu-
                                            engines [3]. It is therefore beneficial to seek out a process’        merous other quantum and classical resources [16]. Its
                                            minimally resource-intensive implementations.                         fundamental challenge is to determine when one system,
                                            Predicting and simulating classical processes, and mon-               or resource, can be converted to another using a prede-
                                            itoring the memory required, led to a generalization of               termined set of free operations.
                                            statistical mechanics called computational mechanics [4–              Resource theory is closely allied with two other areas
                                            7]. To date computational mechanics focused on dis-                   of mathematics, namely majorization and lattice theory.
                                            crete stochastic processes. These are probability measures            Figure 1 depicts their relationships.
                                            P (. . . x−1 x0 x1 . . . ) over strings of symbols taking values in   On the one hand, majorization is a preorder relation %
                                            a finite alphabet A. The minimal information processing               on positive vectors (typically probability distributions)
                                            required to predict the sequence is represented by a type             computed by evaluating a set of inequalities [17]. If the
                                            of hidden Markov model called the -machine. The sta-                 majorization relations hold between two vectors, then
                                            tistical complexity Cµ —the memory rate for -machines                one can be converted to the other using a certain class
                                            to simultaneously generate many copies of a process—is                of operations. Majorization is used in some resource
                                            a key quantity and a proposed invariant for measuring                 theories to numerically test for convertibility between two
                                            the process’ structural complexity.                                   resources [18–20].
                                            When simulating classical processes, quantum systems                  Lattice theory, on the other hand, concerns partially or-
                                            can be constructed that have smaller memory require-                  dered sets and their suprema and infima, if they exist [21].
                                            ments than the -machine [8, 9]. The q-machine is a                   Functions that quantify the practical uses of a resource
                                            particular implementation of quantum simulation that                  are monotonic with respect to the partial orders induced
                                            has shown advantage in memory rate over a wide range of               by convertibility and majorization. Optimization of prac-
                                                                                                                  tical measures of memory is then related to the problem
                                                                                                                  of finding the extrema of the lattice. Majorization and
                                            ∗ sloomis@ucdavis.edu                                                 resource convertibility are both relations that generate
                                                                                                                  lattice-like structures on the set of systems.
                                            † chaos@ucdavis.edu
                                                                                                                                2

                                                                T on a vector p = (pi ) selects two indices i, j ∈ {1, . . . , n},
                          Resource                              such that pi > pj , and transforms the components in the
                           Theory                               following way:
    Majorization                              Conversion
      Proves                                   Induces                                 (T p)i = pi − 
    Conversion                                 Lattice
                                                                                       (T p)j = pj +  ,

                                                                where 0 <  < pi − pj , while leaving all other components
                                                                equal; (T p)k = pk for k 6= i, j.
         Majorization                      Lattice
                                                                Intuitively, these operations reduce concentration, since
         Inequalities                    Optimization
                                                                they act to equalize the disparity between two components,
                                                                in such a way as to not create greater disparity in the
                        Majorization
                                                                opposite direction. This is the principle of transfers.
                         Induces
                          Lattice                               Suppose now that we have two vectors p = (pi ) and
                                                                q = (qi ) and that there exists a sequence of transfer
                                                                operations T1 , . . . , Tm such that Tm ◦ · · · ◦ T1 p = q. We
FIG. 1. Triumvirate of resource theory, majorization, and       will say that p majorizes q; denoted p % q. The relation
lattice theory.                                                 % defines a preorder on the set of distributions, as it is
                                                                reflexive and transitive but not necessarily antisymmetric.
                                                                There are, in fact, a number of equivalent criteria for
Here, we examine the memory costs of classical and quan-
                                                                majorization. We list three relevant to our development
tum models of stochastic processes via majorization. Us-
                                                                in the following composite theorem.
ing lattice-theoretic intuition, we then define the concept
of strong optimization, which occurs when a particular          Theorem 1 (Majorization Criteria). Given two vectors
model simultaneously optimizes all measures of mem-             p = (pi ) and q = (qi ) with the same total sum, let their
ory via its extremal position in the lattice. We show           orderings be given by the permuted vectors p↓ = (p↓i ) and
that among classical predictive models, the -machine           q↓ = (qi↓ ) such that p↓1 > p↓2 > · · · > p↓n and the same for
is strongly minimal. Following this, we show that the           q↓ . Then the following statements are equivalent:
-machine is strongly maximal to a subset of quantum
models but that no strongly minimal quantum model                  1. Hardy-Littlewood-Pólya: For every 1 ≤ k ≤ n,
exists in some circumstances. These results constitute ini-
                                                                                       k       k
tial steps to a resource theory of memoryful information
                                                                                         p↓i ≥   qi↓ ;
                                                                                       X       X
processing.                                                                            i=1        i=1


                                                                   2. Principle of transfers: p can be transformed to q
   II.   MAJORIZATION AND OPTIMIZATION
                                                                      via a sequence of transfer operations;
                                                                   3. Schur-Horn: There exists a unitary matrix  U =
The majorization of positive vectors provides a qualitative                                               
                                                                                                                2
                                                                      (Uij ) such that q = Dp, where D = |Uij | , a
description of how concentrated the quantity of a vector
is over its components. For ease of comparison, consider              uni-stochastic matrix.
vectors p = (pi ), i ∈ {1, . . . , n}, whose components all
                                                                The Hardly-Littlewood-Pólya criterion provides a visual
sum to some constant value, which we take to be unity:
                                                                representation of majorization in the form of the Lorenz
                        n                                       curve. For a distribution p = (pi ), the Lorenz curve is
                              pi = 1 ,                          simply the function βp (k) = i=1 p↓i . See Fig. 2. We can
                        X                                                                    Pk
                        i=1                                     see that p % q so long as the area under βq is completely
                                                                contained in the area under βp .
and are nonnegative: pi ≥ 0. For our purposes, we
interpret these vectors as probability distributions.           The Lorenz curve can be understood via a social analogy,
                                                                by examining rhetoric of the form “The top x% of the
Our introduction to majorization here follows Ref. [17].
                                                                population owns y% of the wealth”. Let y be a function
The historical definition of majorization is also the most
                                                                of x in this statement, and we have the Lorenz curve of a
intuitive, starting with the concept of a transfer operation.
                                                                wealth distribution. (Majorization, in fact, has its origins
Definition 1 (Transfer operation). A transfer operation         in the study of income inequality.)
                                                                                                                                                                                            3


   1                                                             1

                                                                                             2.2
                                                                 4/5
 3/4


                                                                          Renyi entropy Hα
                                                                                             2.0


                                                                                             1.8                                                                       Min-entropy
                                                                                                                                                                       H∞
                                                                 2/5

                                                                                             1.6


                                                                                                          Topological                           Shannon
                                                                                             1.4          entropy H0                            entropy H
   0                                                             0

       0        1          2         3         4         5                                         0.00      0.25       0.50   0.75     1.00        1.25        1.50       1.75      2.00
                                                                                                                                            α
FIG. 2. p and q are comparable and the first majorizes the
second: p % q. (Here we chose p = (3/4, 1/8, 1/8, 0, 0) and              FIG. 4. Rényi entropies of the two incomparable distributions
q = (2/5, 1/5, 1/5, 1/10, 1/10). Tick marks indicate kinks in the        p and q from Fig. 3.
Lorenz curve.)

                                                                         the Rényi entropies:
   1                                                                 1

                                                                                                                       1
                                                                                                                                                   n
                                                                                                                                                                !
                                                                                                             Hα (p) =     log2
                                                                                                                                                   X
                                                                                                                                                           pα          .
                                                                                                                      1−α                          i=1
                                                                                                                                                            i


                                                                         In particular, the three limits
 3/5


                                                                                                                                      n
                                                                                    H(p) = lim Hα (p) = −                                   pi log2 pi ,
                                                                                                                                      X
                                                                                                          α→1
                                                                                                                                      i=1
                                                                             H0 (p) = lim Hα (p) = log2 |{1 ≤ i ≤ n : pi > 0}| , and
                                                                                                          α→0
                                                                         H∞ (p) = lim Hα (p) = − log2 max pi ,
   0                                                                 0

       0         1         2             3         4         5                                            α→∞                                   1≤i≤n


                                                                         —Shannon entropy, topological entropy, and min-entropy,
FIG. 3. p and q are incomparable. (Here we chose p =
(3/5, 1/10, 1/10, 1/10, 1/10) and q = (1/3, 1/3, 1/3, 0, 0).)            respectively—describe important practical features of a
                                                                         distribution. In order, they describe the asymptotic rate
                                                                         at which the outcomes can be accurately conveyed, the
If neither p nor q majorizes the other, they are incompa-                single-shot resource requirements for the same task, and
rable. (See Fig. 3.)                                                     the probability of error in guessing the outcome if no
As noted, majorization is a preorder, since there may                    information is conveyed at all (or, alternatively, the single-
exist distinct p and q such that p % q and q % p. This                   shot rate at which randomness can be extracted from the
defines an equivalence relation ∼ between distributions.                 distribution) [22, 23]. As such, they play a significant role
Every preorder can be converted into a partial order by                  in communication and memory storage.
considering equivalence classes [p]∼ .                                   The example of two incomparable distributions p and q
If majorization, in fact, captures important physical prop-              can be analyzed in terms of the Rényi entropies if we plot
erties of the distributions, we should expect that these                 Hα (p) and Hα (q) as a function of α, as in Fig. 4.
properties may be quantified. The class of monotones that                The central question we explore in the following is ap-
quantify the preorder of majorization are called Schur-                  plying majorization to determine when it is possible to
convex and Schur-concave functions.                                      simultaneously optimize all entropy monotones or, alter-
                                                                         natively, to determine if each monotone has a unique
Definition 2 (Schur-convex (-concave) functions). A                      solution. This leads to defining strong maxima and strong
function f : Rn → R is called Schur-convex (-concave) if                 minima.
p % q implies f (p) ≥ f (q) (f (p) ≤ f (q)).
                                                                         Definition 3 (Strong maximum (minimum)). Let S be
An important class of Schur-concave functions consists of                a set of probability distributions. If a distribution p ∈ S
                                                                                                                             4

satisfies p - q (p % q), for all q ∈ S, then p is a strong            III.   STRONG MINIMALITY OF THE
maximum ( minimum) of the set S.                                                  -MACHINE

The extrema names derive from the fact that the strong
maximum maximizes the Rényi entropies and the strong           The general task we set ourselves is simulating classical
minimum minimizes them. One can extend the definitions         processes.
to the case where p 6∈ S, but is the least-upper-bound         Definition 4 (Bi-infinite process). A bi-infinite process
such that any other p0 satisfying p0 - q must obey p0 -        over an alphabet A is a probability measure P(←     →x ) over
p. This case would be called a strong supremum (or in                                             ←
                                                                                                  →     ←
                                                                                                        −  →
                                                                                                           −
                                                               the set of all bi-infinite strings x = x t x t ∈ A , where
                                                                                                                   ∞
the other direction a strong infimum). However, these          the past ←
                                                                        − = ...x                            →
                                                                                                            −
                                                                        x t          −1+t xt and the future x t = xt xt+1 . . .
constructions may not be unique as % is a preorder and         are constructed by concatenating elements of A.
not a partial order. However, if we sort by equivalence
class, then the strongly maximal (minimal) class is unique     Though defined over bi-infinite strings, the measure gives
if it exists.                                                  probabilities for seeing finite-length words w = x1 . . . x` ,
In lattice-theoretic terms, the strong maximum is essen-       defined as P(w) = P ({←    →
                                                                                          x =←  − w→
                                                                                                x   −
                                                                                                  t x t+` : t ∈ N}). This
tially the lattice-theoretic notion of a meet and the strong   can be taken as an alternate definition of the process
minimum is a join [21].                                        measure.
One example of strong minimization is found in quantum         Here, we focus on finite predictive models.
mechanics. Let ρ be a state and X be a maximal diago-
nalizing measurement. For a given measurement Y , let          Definition 5 (Finite predictive model). A finite predic-
ρ|Y be the corresponding probability distribution that         tive model is a triplet M = (R, A, {T(x) : x ∈ A}) of
comes from measuring ρ with Y . Then ρ|X % ρ|Y for all         hidden states R, an output alphabet   A, and nonnega-
                                                                                                 (x)
maximal projective measurements Y . (This follows from                                   (x)
                                                                                               
                                                               tive transition matrices T = Tρρ0 with x ∈ A and
the unitary matrices that transform from the basis of X        ρ, ρ0 ∈ R, satisfying the properties:
to that of Y , and the Schur-Horn lemma.)
Another, recent example is found in Ref. [24], where the          1. Irreducibility: T =             (x)
                                                                                             P
                                                                                                x∈A T      is stochastic and
set B (p) of all distributions -close to p under the total         irreducible.
variation distance δ is considered:                                                  (x)
                                                                  2. Unifilarity: Tρρ0 = P (x|ρ) δρ0 ,f (ρ,x) for some condi-
               B (p) = {q : δ(p, q) ≤ } .                          tional probability P (x|ρ) and deterministic function
                                                                     f.
This set has a strong minimum, called the steepest dis-
tribution p , and a strong maximum, called the flattest       A finite predictive model is a type of hidden Markov model
distribution p .                                              [25], whose dynamic is to transition between states at
                                                               each timestep while emitting a symbol with probabilities
When a strong minimum or maximum does not exist, we
                                                               determined by the transition matrices T(x) . Unifilarity
refer to the individual extrema of the various monotones
                                                               ensures that, given the model state σ ∈ R and symbol
as weak extrema.
                                                               x ∈ A, the next state σ 0 ∈ R is unique.
We close with a technical note on how to compare dis-
tributions over different numbers of events. There are         Given a finite predictive model M, the state transition
generally two standards for such comparisons that depend       matrix T has a single left-eigenstate π of eigenvalue 1,
on application. In the resource theory of informational        by the Perron-Frobenius theorem, satisfying π > T = π > .
nonequilibrium [20], one compares distributions over dif-      We call this state distribution the stationary state. Us-
ferent numbers of events by “squashing” their Lorenz           ing it, we define the process PM generated by M as
curves so that the x-axis ranges from 0 to 1. Under            PM (w) = π > T(x1 ) · · · T(x` ) 1, where w = x1 . . . x` and
this comparison, the distribution p3 = (1, 0, 0) has more      1 is the vector with all 1’s for its components. PM de-
informational nonequilibrium than p2 = (1, 0). In the          scribes a stationary process. If we let δρ represent the
following, however, we adopt the standard of simply ex-        state-distribution that assigns the state ρ ∈ R probability
tending the smaller distribution by adding events of zero      1, then PM,ρ (w) = δρ> T(x1 ) · · · T(x` ) 1 is the probability
probability. In this, p3 and p2 are considered equiva-         of seeing word w after starting in state ρ.
lent. This choice is driven by our interest in the Rényi       Given a model with stationary distribution π, we de-
entropic costs and not in the overall nonequilibrium. (The     fine the model’s Rényi memory as Hα (M) = Hα (π).
latter is more naturally measured by Rényi negentropies        This includes the topological memory H0 (M), the sta-
H̄α (p) = log n−Hα (p), where n is the number of events.)      tistical memory H (M) = H1 (M), and the min-memory
                                                                                                                                    5


                   0:p         A        1:1 − p                                                      D
             (a)
                             1:1 − p                                                       1 : 1/2       1:1
           0:p       B                  C         1:1 − p
                              0:p
    (b)                                                                                              C
                              1:1 − p                                                1 : 1/2                   0 : 1/2
            0:p          D                  E       0:p
                                                                                                 0 : 1/2
                              1:1 − p
     (c)
                                                                                       A                        B
                                                                                                 0 : 1/2
FIG. 5. (a) -Machine for a coin flipped with bias p. (b)
                                                                              (a)
Alternate representation with p to be in state B and 1 − p to
be in state C. (c) Alternate representation with biases p to
                                                                                 1 : 1/2             D
stay in current state and 1 − p to switch states.                                                                   1:1

H∞ (M). Given a process P, we define the Rényi complex-                                              1 : 1/2
                             (α)
ity as the minimal memory Cµ = minM Hα (M) over all
                                                                                E                                         F
models that generate P [4]. These include the topological                                            0 : 1/2
               (0)                                    (1)
complexity Cµ , the statistical complexity Cµ = Cµ ,
                          (∞)
and the min-complexity Cµ .                                                1 : 1/2                                        0 : 1/2
                                                                                                 0 : 1/2
Among the class of finite predictive models, a particularly
distinguished member is the -machine [4]:                                            A                          B
                                                                                                 0 : 1/2
Definition 6 (Generator -machine). A generator                      (b)
-machine is a finite predictive model M = (S, A, {T(x) :
x ∈ A}) such that for each pair of distinct states ρ, ρ0 ∈ S,   FIG. 6. (a) -Machine for Even-Odd Process. (b) Refinement
                                                                of the Even-Odd Process -machine, where the -machine’s
there exists a word w such that PM,ρ (w) 6= PM,ρ0 (w).          state C has been split into states E and F .

In other words, a generator -machine must be irreducible,
unifilar, and its states must be probabilistically distinct,    strings of an even number of 0s. We see in (a) the process’
so that no pair of distinct states predict the same future.     -machine. In (b), we see an alternative finite predictive
An important result of computational mechanics is that          model, and notice that its states E and F predict the
the generator -machine is unique with respect to the pro-      same futures, and so are not probabilistically distinct.
cess it generates [26]. This is a combined consequence of       We notice that they both play the role of state C in the
the equivalence of the generator definition with another,       -machine, in terms of the futures they predict.
called the history -machine, which is provably unique          We can compare these examples using Lorenz curves of
[6]. That is, given an -machine M, there is no other           the state distributions, as shown in Fig. 7. Here, recall,
-machine that generates PM . A further important re-           we adopted the convention of comparing two distributions
sult is that the -machine minimizes both the statistical       over a different number of states by extending the smaller
                                                  (0)
complexity Cµ and the topological complexity Cµ .               system to include zero-probability states. We notice that
To fix intuitions, consider now several examples of models      the -machine state distribution always majorizes the
and their processes. First, consider the Biased Coin            state distribution of the alternative machines.
Process, a memoryless process in which, at each time            The key to formalizing this observation is the following
step, a coin is flipped with probability p of generating a 1    lemma.
and probability 1 − p of generating a 0. Figure 5 displays
three models for it. Model (a) is the process’ -machine,       Lemma 1 (State Merging). Let M = (R, A, {T(x) : x ∈
and models (b) and (c) are each 2-state alternative finite      A}) be a finite predictive model that is not an -machine.
predictive models. Notice that in both models (b) and           Then the machine created by merging its probabilistically
(c), the two states generate equivalent futures.                equivalent states is the -machine of the process PM gen-
                                                                erated by M.
Continuing, Fig. 6 displays two alternative models of
the Even-Odd Process. This process produces sequences           Proof. Let ∼ be the equivalence relation ρ ∼ ρ0 if
formed by concatenating strings of an odd number of 1s to       PM,ρ (w) = PM,ρ0 (w) for all w. Let S consist of the
                                                                                                                                6

                             (a)                                     machine MS = (S, A, {T e (x) : x ∈ A}) is the -machine
 1                                                               1
                                                                     of the process PM generated by M.

                                                                     The state-merging procedure here is an adaptation of
                                                                     the Hopcroft algorithm for minimization of deterministic
                                                                 p
                                                                     (nonprobabilistic) finite automata, which is itself an im-
                                                                     plementation of the Nerode equivalence relation, [27]. It
                                                                     has been applied previously to analyze synchronization
                                                                     in -machines [28].
                                                                     Using Lemma 1, we can prove the main result of this
                                                                     section:
 0                                                               0
                                                                     Theorem 2 (Strong Minimality of -Machine). Let
         0                    1                          2
                                                                     MS = (S, A, {T e (x) : x ∈ A}) be the -machine of process
                             (b)                                     P and MR = (R, A, {T(x) : x ∈ A}) be any other fi-
                                                                     nite generating machine. Let the stationary distributions
                                                                     be πS = (πS,σ ) and πR = (πR,ρ ), respectively. Then
     1                                                       1

 6/7                                                                 πS % πR .

                                                                     Proof. By Lemma 1, the states of the -machine MS are
                                                             4/7     formed by merging equivalence classes σ = [ρ] on the finite
                                                                     predictive model MR . Since the machines are otherwise
                                                                     equivalent, the stationary probability πS,σ is simply the
                                                                     sum of the stationary probabilities for each ρ ⊆ σ, given
                                                                     by πR,ρ . That is:

                                                                                         πS,σ =
                                                                                                  X
     0                                                       0
                                                                                                         πR,ρ .
             0   1       2         3        4        5
                                                                                                  ρ∈Rσ


FIG. 7. (a) Lorenz curves for Fig. 5(a)’s -machine and Fig.         One can then construct πR from πS by a series of transfer
5(b)’s alternative predictor of the Biased Coin Process. (b)         operations in which probability is shifted out of the state
Same comparison for the Even-Odd Process -machine Fig.              σ into new states ρ. Since the two states are related by a
6(a) and alternative predictor Fig. 6(b).
                                                                     series of transfer operations, πS % πR .

                                                                     It immediately follows from this that not only does the
set of equivalence classes [ρ]∼ generated by this rela-
                                                                     -machine minimize the statistical complexity Cµ and the
tion. For a given class σ ∈ S, consider the transi-                                           (0)
                                                                     topological complexity Cµ , but it also minimizes every
tion probabilities associated with each ρ ∈ σ. For each                                        (α)
x ∈ A such that P (x|ρ) > 0, there is a outcome state                other Rényi complexity Cµ as well.
ρx = f (x, ρ). Comparing with another state in the                   The uniqueness of the -machine is extremely important
same class ρ0 ∈ σ, we have the set of outcome states                 in formulating this result. This property of -machines
ρ0x = f (x, ρ0 ). For the future predictions of both states ρ        follows from the understanding of predictive models as par-
and ρ0 to be equivalent, they must also be equivalent after          titions of the past and of the -machines as corresponding
seeing the symbol x. That is, PM,ρ (w) = PM,ρ0 (w) for               to the coarsest graining of these predictive partitions [6].
all w also implies PM,ρ (xw) = PM,ρ0 (xw) for all w. But             Other paradigms for modeling will not necessarily have
PM,ρ (xw) = PM,ρx (w), and so we have ρx ∼ ρ0x for all               this underlying structure and so may not have strongly
x ∈ A.                                                               minimal solutions. In the following, we see this is, in fact,
                                                                     the case for pure-state quantum machines.
The upshot of these considerations is that we can define a
consistent and unifilar transition dynamic {T  e (x) : x ∈ A}
                                  (x)      (x)
on S given by the matrices Teσσ0 = Teρρ0 for any ρ ∈
                                                                          IV.   STRONG QUANTUM ADVANTAGE
σ and ρ0 ∈ σ 0 . It inherits unifilarity from the original
model M as well as irreducibility. It has probabilistically
distinct states because we have already merged all of the            A pure-state quantum model can be generalized from
probabilistically equivalent states. Therefore, the resulting        the classical case by replacing the classical states σ with
                                                                                                                                7

quantum-mechanical pure states |ησ i and the symbol-               statistical memory S (M) = S1 (M), and the min-memory
labeled transition matrices T(x) with symbol-labeled               S∞ (M), which represent physical limitations on memory
Kraus operators K (x) .                                            storage for the generator.

Definition 7 (Pure-state quantum model). A pure-state              To properly compare pure-state quantum models and clas-
quantum model is a quintuplet M = (H, A, S, Σ = {|ησ i :           sical predictive models, we define the classical equivalent
σ ∈ S}, {K (x) : x ∈ A}) of a Hilbert space H, an output           model of a pure-state quantum model.
alphabet A, pure states |ησ i corresponding to some set of
state labels S, and nonnegative Kraus operators K (x) with         Definition 8 (Classical equivalent model). Let M =
x ∈ A satisfying the properties:                                   (H, A, S, Σ = {|ησ i : σ ∈ S}, {K (x) : x ∈ A}) be a pure-
                                                                   state quantum model, with probabilities and deterministic
   1. Completeness:     The Kraus operators satisfy                function P(x|σ) = hησ | K (x)† K (x) |ησ i and σ 7→ f (σ, x),
            (x)† (x)
                     =                                             respectively. Its classical equivalent MCl. is the classi-
      P
        x K     K      I.
                                                                   cal finite predictive model with state set S, alphabet A
   2. Unifilarity: K (x) |ησ i ∝ ηf (σ,x) for some deter-
                                                                   and symbol-based transition matrices T(x) generated by
      ministic function f (σ, x).
                                                                   the state-to-symbol probabilities P(x|σ) and deterministic
This is a particular kind of hidden quantum Markov model           function f (σ, x).
[29] in which we assume the dynamics can be described by
the evolution of pure states. This is practically analogous        We now prove that a finite classical predictive model
to the assumption of unifilarity in the classical predictive       strongly maximizes all pure-state quantum models of
setting.                                                           which it is the classical equivalent.
It is not necessarily the case that the states {|ησ i} form
an orthonormal basis; rather, nonorthonormality is the             Theorem 3 (Strong quantum advantage). Let M =
intended advantage [8, 9]. Overlap between the states al-          (H, A, S, Σ = {|ησ i : σ ∈ S}, {K (x) : x ∈ A}) be a pure-
lows for a smaller von Neumann entropy for the stationary          state quantum model with stationary state ρπ , and let
state of the process. We formalize this shortly.                   MCl. be the classical equivalent model with stationary
                                                                   state π = (πσ ) (with σ = 1, . . . , n). Let d = dim H and
It is assumed that the Kraus operators have a unique
                                                                   n = |S|. (We have n ≥ d: if not, then we can take a
stationary state ρπ . One way to compute it is to note that
                                                                   smaller Hilbert space that spans the states.) Let λ = (λi )
taking P(x|σ) = hησ | K (x)† K (x) |ησ i and the function σ 7→
                                                                   be an n-dimensional vector where the first d components
f (σ, x) determines a finite predictive model as defined
                                                                   are the eigenvalues of ρπ and the remaining elements are
above. The model’s stationary state π = (πσ ) is related
                                                                   0. Then λ % π.
to the stationary state of the quantum model via:
                                                                   Proof. We know that:
                  ρπ =
                        X
                             πσ |ησ i hησ | .
                                                                                          ρπ =
                           σ
                                                                                                 X
                                                                                                        πσ |ησ i hησ |
The process generated by a pure-state quantum model                                              σ∈S

has the word distribution, for words w = x1 . . . x` :                                       =
                                                                                                 X
                                                                                                        |φσ i hφσ | ,
                                                                                                 σ∈S
    P(w) = Tr K (x` ) · · · K (x1 ) ρπ K (x1 )† · · · K (xL )† .
              h                                               i
                                                                                 √
                                                                   where |φσ i = πσ |ησ i. However, we can also write ρπ in
                                                                   the eigenbasis:
The eigenvalues {λi } of the stationary state ρπ form a
distribution λ = (λi ). The Rényi entropies of these                                              d
distributions form the von Neumann-Rényi entropies of                                     ρπ =
                                                                                                  X
                                                                                                        λi |ii hi|
the states:                                                                                       i=1
                                                                                                  d
                                                                                              =
                                                                                                  X
                     Sα (ρπ ) = Hα (λ) .                                                                |ψi i hψi | ,
                                                                                                  i=1

We noted previously that for a given state these are                               √
                                                                   where |ψi i =       λi |ii. Then the two sets of vectors can be
strongly minimal over the entropies of all projective,
                                                                   related via:
maximal measurements on the state. Given a model M
with stationary state ρπ , we may simply write Sα (M) =                                             d
Sα (ρπ ) as the Rényi memory of the model. Important                                      |φσ i =
                                                                                                    X
                                                                                                          Uσi |ψi i ,
limits, as before, are the topological memory S0 (M), the                                           i=1
                                                                                                                            8

where Uσi is a n × d matrix comprised of d rows of or-                                      1/2
thonormal n-dimensional vectors [30]. Now, we have:

                     πσ = hφσ |φσ i
                            d                                                                  B
                        =         |Uσi |2 λi .                                     1/4                   1/4
                            X

                            i=1

                                                                                         1/4       1/4
Note that Uσi is not square, but since we have taken λi = 0
for i > d, we can simply extend Uσi into a square unitary          1/2
                                                                               C                               D      1/2
                                                                                         1/4       1/4
matrix by filling out the bottom n − d rows with more
orthonormal vectors. This leaves the equation unchanged.
We can then write:                                                                 1/4                   1/4

                            n                                                                  A
                     πσ =         |Uσi |2 λi .
                            X

                            i=1

Then by Theorem 1, λ % π.                                                                  1/2

Corollary 1. Sα (M) ≤ Hα (MCl. ) for all α ≥ 0.
                                                               FIG. 8. The 4-state MBW Process as a Markov chain (which
Proof. Sα (ρπ ) ≤ Hα (π) for all α ≥ 0 follows from the        is the -machine).
definitions of the von Neumann-Rényi entropies and the
Schur-concavity of Hα . 
Many alternative pure-state quantum models may de-
scribe the same process. The “first mark”, so to speak, for          V.    WEAK QUANTUM MINIMALITY
quantum models is the q-machine [9, 15], which directly
embeds the dynamics of the -machine into a quantum
system while already leveraging the memory advantage
due to state overlap.                                          An open problem is to determine the minimal quantum
                                                               pure-state representation of a given classical process. This
Definition 9 (q-Machine). Given an -machine                   problem is solved in some specific instances such as the
                                  (x)
{S, A, {T(x) : x ∈ A}}, where Tσσ0 = P(x|σ)δσ0 ,f (σ,x)        Ising model [11] and the Perturbed Coin Process [14]. In
for some deterministic function f (σ, x), construct the        these cases it is known to be the q-machine. We denote
corresponding q-machine in the following way:                  the smallest value of the Rényi entropy of the station-
                                                                               (α)
   1. The states |ησ i are built to satisfy the recursive      ary state as Cq = minM Sα (M), called the quantum
      relation:                                                Rényi complexities, including the limits, the quantum
                                                                                         (0)
                                                               topological complexity Cq , the quantum min-complexity
                                                                 (∞)                                                    (1)
   hησ |ησ0 i =      P(x|σ)P(x|σ 0 ) ηf (σ,x) |ηf (σ0 ,x) .    Cq , and the quantum statistical complexity Cq = Cq .
                Xp

               x∈A                                             If a strongly minimal quantum pure-state model exists,
                                                               these complexities are all attained by the same pure-state
   2. H is the space spanned by the states |ησ i.              model. One of our primary results in this section is that
   3. The Kraus operators K (x) are determined by the          for some processes, this does not occur.
      relations:

              K (x) |ησ i = P(x|σ) ηf (σ,x) .
                           p                                   We start by examining two examples. The first, the MBW
                                                               Process introduced in Ref. [29], demonstrates a machine
                                                               whose q-machine is not minimal in the von Neumann
One can check that this satisfies the completeness relations
                                                               complexity. Consider the process generated by the 4-state
and has the correct probability dynamics for the process
                                                               MBW machine shown in Fig. 8.
generated by the -machine.
That the q-machine offers statistical memory advantage
with respect to the -machine was previously shown in [31]     This process’ HMM is simply a Markov chain, and its rep-
and with respect to topological memory in [14]. Theorem        resentation in Fig. 8 is its -machine. Denote this classical
3 and Corollary 1 imply these as well as advantage with        representation by M4 . If we take {|Ai , |Bi , |Ci , |Di} as
respect to other Rényi measures of memory.                     an orthonormal basis of a Hilbert space, we can construct
                                                                                                                          9


 0.971                                                     1     0.971                                                    1
     9                                                               9


 0.72                                                            0.72
     9                                                                  9


        0                                                  0            0                                                 0

            0           1           2        3         4                    0       1           2         3           4


FIG. 9. Lorenz curves for the 4-state MBW -machine M4          FIG. 10. Lorenz curves for the 4-state MBW q-machine Q4
and the associated q-machine Q4 .                               and a dimensionally smaller model D4 .


the q-machine with the states:                                  majorize the q-machine, but it does have a lower statistical
                                                                memory: S(D4 ) = 1.0 and S(Q4 ) ≈ 1.2 bit. (On the
                         1     1                                other hand, the q-machine has a smaller min-memory,
                |ηA i = √ |Ai + (|Ci + |Di) ,
                          2    2                                with S∞ (D4 ) = 1.0 and S∞ (Q4 ) ≈ 0.46.)
                         1     1
                |ηB i = √ |Bi + (|Ci + |Di) ,                   Now consider something in the opposite direction. Con-
                          2    2
                                                                sider the 3-state MBW model, denoted M3 and displayed
                         1     1
                |ηC i = √ |Ci + (|Ai + |Bi) , and               in Fig. 11. This is a generalization of the previous ex-
                          2    2
                                                                ample to three states instead of four. We will compute
                         1     1                                the corresponding q-machine Q3 and show that there also
                |ηD i = √ |Di + (|Ai + |Bi) .
                          2    2                                exists a dimensionally smaller representation D3 . In this
Since it is a Markov chain, we can write the                    case, however, D3 is not smaller in its statistical memory.
                                            p Kraus opera-
tors as Kx = |ηx i hx |, where hx |ηx0 i ∝ P(x|x0 ). This     The q-machine Q3 of this Markov chain is given by the
is a special case of the construction used in Ref. [13]. For    states:
q-machines of Markov chains, then, the dual basis is just
                                                                                  2        1
                                                                                r
hx | = hx|. We denote the q-machine model of the 4-state               |ηA i =     |Ai + √ (|Bi + |Ci) ,
MBW Process as Q4 .                                                               3         6
                                                                                  2        1
                                                                                r
Let’s examine the majorization between Q4 and the                       |ηB i =     |Bi + √ (|Ai + |Ci) , and
Markov model via the Lorenz curves of λ, the eigen-                               3         6
values of ρπ , and the stationary state of the Markov chain.                      2        1
                                                                                r
                                                                        |ηC i =     |Ci + √ (|Ai + |Bi) ,
See Fig. 9.                                                                       3         6
It turns out that there is a smaller quantum model em-
                                                                and Kraus operators defined similarly to before. We can
bedded in two dimensions, with states:
                                                                examine the majorization between the q-machine and the
                                                                Markov model by plotting the Lorenz curves of λ, the
                      0
                    |ηA i = |0i ,
                                                                eigenvalues of ρπ , and the stationary state of the Markov
                      0
                    |ηB i = |1i ,                               chain, shown in Fig. 12.
                              1
                      0
                    |ηC i = √ (|0i + |1i) , and                 The lower-dimensional model D3 is given by the states:
                               2
                              1                                                 |ηA i = |0i ,
                      0
                    |ηD i = √ (|0i − |1i) .
                               2                                                                √
                                                                                         1        3
                                                                               |ηB i = |0i +        |1i , and
In this case, h0x | = √12 hηx0 | derives the q-machine. This                            2      √2
gives the proper transition probabilities for the 4-state                                1        3
                                                                               |ηC i = |0i −        |1i ,
MBW model. This dimensionally smaller model we denote                                    2       2
D4 . Figure 10 compares the Lorenz curve of its stationary                    q
                                                                                 2
eigenvalues λ0 to those of Q4 . One sees that it does not       with h0x | =    3 hηx |. This gives the proper transition
                                                                                     0
                                                                                                                                        10

                               2/3
                                                                 1                                                                      1

                                                              0.889


                               C
                   1/6                 1/6


                             1/6 1/6
                               1/6
                   A                       B
                                                                 0                                                                      0
                               1/6
                                                                      0              1                           2                  3
             2/3                               2/3

                                                             FIG. 13. Lorenz curves for the 3-state MBW q-machine, Q3
FIG. 11. 3-state MBW Process as a Markov chain (which is     and a dimensionally smaller model D3 .
the process’ -machine).


    1                                                    1

 0.889


                                                                                    clas
                                                                                         sica
                                                                                              l   pred
                                                                                                       i   ctor
                                                                                                                s

                                                                                                             


    0                                                    0

         0               1             2             3                                                                            els
                                                                                                                                od
                                                                                                                               m
                                                                                                                           m
                                                                                                                         tu
FIG. 12. Lorenz curves for the 3-state MBW -machine M3                                                                an
and the associated q-machine Q3 .                                                                                    qu


probabilities for the 3-state MBW model. Figure 13           FIG. 14. Proposed majorization saddle structure of model-
compares the Lorenz curve of its stationary eigenvalues      space: The -machine (labeled ) is located at a saddle-point
λ0 to that of Q3 . We see that it does not majorize Q3 .     with respect to majorization, where classical deviations (state-
And, this time, this is directly manifested by the fact      splitting) move up the lattice and quantum deviations (utiliz-
that the smaller-dimension model has a larger entropy:       ing state overlap) move down the lattice.
S(D3 ) = 1.0 and S(Q3 ) ≈ 0.61 bit.
After seeing the -machine’s strong minimality with re-
spect to other classical models and its strong maximality    Appendix A proves exactly this—thus, demonstrating
with respect to quantum models, it is certainly tempting     a counterexample to the strong minimality of quantum
to conjecture that a strongly minimal quantum model ex-      models.
ists. However, the examples we just explored cast serious
doubt. None of the examples covered above are strong
minima. One way to prove that no strong minimum exists       Counterexample (Weak Minimality of D3 ). The quan-
for, say, the 3-state MBW process requires showing that      tum model D3 weakly minimizes topological complexity
there does not exist any other quantum model in 2 dimen-     for all quantum generators of the 3-state MBW Process;
sions that generates the process. This would imply that      consequently, the 3-state MBW Process has no strongly
no other model can majorize D3 . And, since this model       minimal model.
is not strongly minimal, no strongly minimal solution can
exist.
                                                                                                                            11

          VI.    CONCLUDING REMARKS                              considering machines that generate a single realization.
                                                                 This is in contrast to Cµ which, being strongly minimized,
                                                                 must be attainable in the single-shot regime along with
Majorizing states provides a means to compare a process’                          (0)       (∞)
                                                                 measures like Cµ and Cµ .
alternative models in both the classical and quantum
regimes. Majorization implies the simultaneous minimiza-         In this way, the quantum realm again appears ambiguous.
tion of a large host of functions. As a result we showed         Ambiguity in structural complexity has been previously
that:                                                            observed in the sense that there exist pairs of processes,
                                                                 A and B, such that Cµ (A) > Cµ (B) but Cq (A) < Cq (B)
   1. The -machine majorizes all classical predictive mod-      [33]. The classical and quantum paradigms for modeling
      els of the same process, and so simultaneously min-        can disagree on simplicity—there is no universal Ockham’s
                                                                 Razor. How this result relates to strong versus weak
      imizes many different measures of memory cost.
                                                                 optimization deserves further investigation.
   2. The q-machine, and indeed any quantum realization          The methods and results here should also be extended to
      of the -machine, always majorizes the -machine,          analyze classical generative models which, in many ways,
      and so simultaneously improves on all the measures         bear resemblances in their functionality to the quantum
      of memory cost.                                            models [34–36]. These drop the requirement of unifilarity,
   3. For at least one process, there does not exist any         similar to how the quantum models relax the notion of
      quantum pure-state model that majorizes all quan-          orthogonality. Important questions to pursue in this vein
      tum pure-state models of that process. Thus, while         are whether generative models are strongly maximized by
      an -machine may be improved upon by different             the -machine and whether they have their own strong
      possible quantum models, there is not a unique one         minimum or, like the quantum models, only weak minima
      quantum model that is unambiguously the “best”             in different contexts.
      choice.                                                    To close, we only explored finite-state, discrete-time pro-
                                                                 cesses. Processes with infinite memory [37] and continuous
Imagining the -machine as an invariant “saddle-point” in        generation [38, 39] are also common in nature. Applying
the majorization structure of model-space, Fig. 14 depicts       our results to understand these requires further mathe-
the implied geometry. That is, we see that despite its non-      matical development.
minimality among all models, the -machine still occupies
a topologically important position in model-space—one
that is invariant to one’s choice of memory measure. How-                       ACKNOWLEDGMENTS
ever, no similar model plays the topologically minimal
role for quantum pure-state models.                              The authors thank Fabio Anza, John Mahoney, Cina
The quantum statistical complexity Cq has been offered           Aghamohammadi, and Ryan James for helpful discus-
up as an alternative quantum measure of structural               sions. As a faculty member, JPC thanks the Santa Fe
complexity—a rival of the statistical complexity Cµ [32].        Institute and the Telluride Science Research Center for
One implication of our results here is that the nature           their hospitality during visits. This material is based
of this quantum minimum Cq is fundamentally different            upon work supported by, or in part by, John Templeton
than that of Cµ . This observation should help further           Foundation grant 52095, Foundational Questions Institute
explorations into techniques required to compute Cq and          grant FQXi-RFP-1609, the U.S. Army Research Labora-
the physical circumstances in which it is most relevant.         tory and the U. S. Army Research Office under contract
That the physical meaning of Cq involves generating an           W911NF-13-1-0390 and grant W911NF-18-1-0028, and
asymptotically large number of realizations of a process         via Intel Corporation support of CSC as an Intel Parallel
may imply that it cannot be accurately computed by only          Computing Center.


 [1] E. N. Lorenz. Deterministic nonperiodic flow. J. Atmos.          ratchets. New J. Physics, 18:023049, 2016.
     Sci., 20:130, 1963.                                          [4] J. P. Crutchfield and K. Young. Inferring statistical
 [2] E. N. Lorenz. The problem of deducing the climate from           complexity. Phys. Rev. Let., 63:105–108, 1989.
     the governing equations. Tellus, XVI:1, 1964.                [5] J. P. Crutchfield. The calculi of emergence: Computation,
 [3] A. B. Boyd, D. Mandal, and J. P. Crutchfield. Identifying        dynamics, and induction. Physica D, 75:11–54, 1994.
     functional thermodynamics in autonomous Maxwellian
                                                                                                                              12

 [6] C. R. Shalizi and J. P. Crutchfield. Computational me-            A: Math. Theor., 51(305301), 2018.
     chanics: Pattern and prediction, structure and simplicity.   [25] D. R. Upper. Theory and Algorithms for Hidden Markov
     J. Stat. Phys., 104:817–879, 2001.                                Models and Generalized Hidden Markov Models. PhD
 [7] J. P. Crutchfield. Between order and chaos. Nature                thesis, University of California, Berkeley, 1997. Published
     Physics, 8:17–24, 2012.                                           by University Microfilms Intl, Ann Arbor, Michigan.
 [8] M. Gu, K. Wiesner, E. Rieper, and V. Vedral. Quantum         [26] N. F. Travers and J. P. Crutchfield. Equivalence of
     mechanics can reduce the complexity of classical models.          history and generator -machines. arxiv.org:1111.4500
     Nature Comm., 3(762), 2012.                                       [math.PR].
 [9] J. R. Mahoney, C. Aghamohammadi, and J. P. Crutchfield.      [27] J. Hopcroft. An n log n algorithm for minimizing states in
     Occam’s quantum strop: Synchronizing and compress-                a finite automaton. In A. Paz Z. Kohavi, editor, Theory
     ing classical cryptic processes via a quantum channel.            of Machines and Computations, pages 189–196, New York,
     Scientific Reports, 6:20495, 2016.                                1971. Academic Press.
[10] C. Aghamohammadi, J. R. Mahoney, and J. P. Crutchfield.      [28] N. F. Travers and J. P. Crutchfield. Exact synchronization
     Extreme quantum advantage when simulating classical               for finite-state sources. J. Stat. Physics, 145:1181–1201,
     systems with long-range interaction. Scientific Reports,          2011.
     7(6735), 2017.                                               [29] A. Monras, A. Beige, and K. Wiesner. Hidden quantum
[11] W. Y. Suen, J. Thompson, A. J. P. Garner, V. Vedral, and          Markov models and non-adaptive read-out of many-body
     M. Gu. The classical-quantum divergence of complexity             states. Appl. Math. Comput. Sci., 3:93, 2011.
     in modelling spin chains. Quantum, 1:25, 2017.               [30] L. P. Hughston, R. Jozsa, and W. K. Wootters. A com-
[12] A. J. P. Garner, Q. Liu, J. Thompson, V. Vedral, and              plete classification of quantum ensembles having a given
     M. Gu. Provably unbounded memory advantage in                     density matrix. Phys. Lett. A, 183:12–18, 1993.
     stochastic simulation using quantum mechanics. New           [31] J. R. Mahoney, C. Aghamohammadi, and J. P. Crutchfield.
     J. Physics, 19:103009, 2017.                                      Occam’s quantum strop: Synchronizing and compress-
[13] C. Aghamohammadi, S. P. Loomis, J. R. Mahoney, and                ing classical cryptic processes via a quantum channel.
     J. P. Crutchfield. Extreme quantum memory advantage               Scientific Reports, 6(20495), 2016.
     for rare-event sampling. Phys. Rev. X, 8:011025, 2018.       [32] R. Tan, D. R. Terno, J. Thompson, V. Vedral, and M. Gu.
[14] J. Thompson, A. J. P. Garner, J. R. Mahoney, J. P.                Towards quantifying complexity with quantum mechanics.
     Crutchfield, V. Vedral, and M. Gu. Causal asymmetry in            Eur. J. Phys. Plus, 129:191, 2014.
     a quantum world. Phys. Rev. X, 8:031013, 2018.               [33] C. Aghamohammadi, J. R. Mahoney, and J. P. Crutchfield.
[15] P. M. Riechers, J. R. Mahoney, C. Aghamohammadi, and              The ambiguity of simplicity in quantum and classical
     J. P. Crutchfield. Minimized state-complexity of quantum-         simulation. Phys. Lett. A, 381(14):1223–1227, 2017.
     encoded cryptic processes. Phys. Rev. A, 93(5):052317,       [34] W. Löhr and N. Ay. Non-sufficient memories that are
     2016.                                                             sufficient for prediction. In J. Zhou, editor, Complex Sci-
[16] B. Coecke, T. Fritz, and R. W. Spekkens. A mathematical           ences 2009, volume 4 of Lecture Notes of the Institute for
     theory of resources. Info. Comput., 250:59–86, 2016.              Computer Sciences, Social Informatics and Telecommuni-
[17] A. W. Marshall, I. Olkin, and B. C. Arnold. Inequalities:         cations Engineering, pages 265–276. Springer, New York,
     Theory of Majorization and Its Applications. Springer,            2009.
     New York, NY, 3 edition, 2011.                               [35] W. Löhr and N. Ay. On the generative nature of prediction.
[18] M. A. Nielsen. Conditions for a class of entanglement             Adv. Complex Sys., 12(02):169–194, 2009.
     transformations. Phys. Rev. Lett., 83(436), 1999.            [36] J. B. Ruebeck, R. G. James, J. R. Mahoney, and J. P.
[19] M. Horodecki and J. Oppenheim. Fundamental limitations            Crutchfield. Prediction and generation of binary markov
     for quantum and nanoscale thermodynamics. Nature                  processes: Can a finite-state fox catch a markov mouse?
     Comm., 4(2059), 2013.                                             Chaos, 28(013109), 2018.
[20] G. Gour, M. P. Müller, V. Narasimhachar, R. W.               [37] J. P. Crutchfield and S. Marzen. Signatures of infinity:
     Spekkens, and N. Y. Halpern. The resource theory of               Nonergodicity and resource scaling in prediction, com-
     informational nonequilibrium in thermodynamics. Phys.             plexity and learning. Phys. Rev. E, 91(050106), 2015.
     Rep., 583:1–58, 2015.                                        [38] J. P. Crutchfield and S. Marzen. Structure and random-
[21] G. Grätzer. Lattice Theory: Foundation. Springer, Basel,          ness of continuous-time, discrete-event processes. J. Stat.
     2010.                                                             Phys., 169(2):303–315, 2017.
[22] R. Renner and S. Wolf. Smooth Rényi entropy and ap-          [39] T. J. Elliot, A. J. P. Garner, and M. Gu. Quantum
     plications. In IEEE Information Theory Society, editor,           self-assembly of causal architecture for memory-efficient
     2004 IEEE Intl. Symp. Info. Th.: Proceedings, page 232,           tracking of complex temporal and symbolic dynamics.
     Piscataway, N.J., 2004. IEEE.                                     arxiv.org:1803.05426.
[23] M. Tomamichel. A Framework for Non-Asymptotic Quan-
     tum Information Theory. PhD thesis, ETH Zurich, Zurich,
     2012.
[24] M. Horodecki, J. Oppenheim, and C. Sparaciari. Extremal
     distributions under approximate majorization. J. Phys.
                                                                                                                           13

  Appendix A: Appendix: Weak Minimality of D3                     These gauge fixings allow us to write:

                                                                                  |ηA i = |0i ,
Here, we prove that D3 is the unique 2D representation
of the 3-state MBW process. We show this by considering                           |ηB i = αB |0i + βB |1i , and
the entire class of 2D models and applying the complete-                          |ηC i = αC |0i + eiθ βC |1i ,
ness constraint.
                                                                  for αB , αC ≥ 0, βB =             2 and β =
                                                                                               1 − αB                   2 and
                                                                                                                   1 − αC
                                                                                           p                      p
We note that a pure-state quantum model of the 3-state                                                     C
                                                                  a phase θ.
MBW process must have three states |ηA i, |ηB i, and |ηC i,
along with three dual states hA |, hB |, and hC | such that:   That these states are embedded in a 2D Hilbert space
                                                                  means there must exist some linear consistency conditions.
                                            2                     For some triple of numbers c = (cA , cB , cC ) we can write:
                                        r
                 hA |ηA i = e   iφAA
                                              ,
                                            3
                                    1                                           cA |ηA i + cB |ηB i + cC |ηC i = 0 .
                 hA |ηB i = eiφAB √ , and
                                     6
                                                                  Up to a constant, we use our parameters to choose:
                               iφAC 1
                 hA |ηC i = e     √ ,
                                     6                                                 
                                                                                             βC
                                                                                                                  
                                                                                                          iθ βC
                                                                      (cA , cB , cC ) = e αB
                                                                                         iθ
                                                                                                − αC , −e       ,1 .
                                                                                             βB              βB

                                                                  Consistency requires that this relationship between vec-
                                   1                              tors is preserved by the Kraus operator dynamic. Consider
                hB |ηA i = eiφBA
                                  √ ,
                                    6                             the matrix A = (Axy ) = (hx |ηy i). The vector c must
                                     2                            be a null vector of A; i.e.       y Axy cy = 0. This first
                                  r                                                              P
                hB |ηB i = eiφBB      , and                      requires that Axy be degenerate. One way to enforce this
                                     3
                                   1                              to check that the characteristic polynomial det(A − λI3 )
                hB |ηC i = eiφBC √ ,                             has an overall factor of λ. For simplicity, we compute the
                                    6                                                             √
                                                                  characteristic polynomial of A 6:
and:                                                                    √
                                                                   det( 6A − λI3 ) =
                                      1
                   hC |ηA i = eiφCA √ ,                                    3
                                       6                            (2 − λ) +
                                iφCB 1                                ei(φAB +φBC +φCA ) + ei(φBA +φCB +φAC ) −
                                                                                                            
                   hC |ηB i = e     √ ,
                                       6
                                                                    (2 − λ) ei(φAB +φBA ) + ei(φAC +φCA ) + ei(φBC +φCB ) .
                                                                                                                        
                                        2
                                     r
                   hC |ηC i = eiφCC      .
                                        3
                                                                  To have an overall factor of λ, we need:
We list the available geometric symmetries that leave the
final stationary state unchanged:                                  0 = 8 + ei(φAB +φBC +φCA ) + ei(φBA +φCB +φAC )
                                                                                                                  


                                                                       − 2 ei(φAB +φBA ) + ei(φAC +φCA ) + ei(φBC +φCB ) .
                                                                                                                       
   1. Phase transformation on each state, |ηx i 7→
      eiφx |ηx i;
                                                                  Typically, there will be several ways to choose phases to
   2. Phase transformation on each dual state, |x i 7→           cancel out vectors, but in this case since the sum of the
      eiφx |x i; and                                             magnitudes of the complex terms is 8, the only way to
   3. Unitary transformation |ηx i 7→ U |ηx i and hx | 7→        cancel is at the extreme point where φAB = −φBA = φ1 ,
      hx | U † .                                                 φBC = −φCB = φ2 , and φCA = −φAC = φ3 and:

From these symmetries we can fix gauge in the following                                φ1 + φ2 + φ3 = π .
ways:
                                                                  To recapitulate the results so far, A has the form:
   1. Set h0|ηx i to be real and positive for all x.
                                                                                   2         eiφ1 −ei(φ1 +φ2 )
                                                                                                              
                                                                           1 
   2. Set φAA = φBB = φCC = 0.                                         A= √     e−iφ1         2      eiφ2       .
                                                                            6 −e−i(φ1 +φ2 ) e−iφ2     2
   3. Set h0|ηA i = 0 and set h1|ηB i to be real and positive.
                                                                                                                           14

We now need to enforce that       y Axy cy = 0. We have the      be used with the contractions with |ηB i to get:
                                P

three equations:
                                                                                     1  2 1 iφ1
                                                                                      r           
                                                                           hA |1i =         e −α ,
            2cA + eiφ1 cB − ei(φ1 +φ2 ) cC = 0 ,                                     β  3 2
               2cB + e−iφ1 cA + eiφ2 cC = 0 , and                                   1 2       1
                                                                                      r              
                                                                          hB |1i =       1 − αe−iφ1 , and
        2cC + e−iφ2 cB − e−i(φ1 +φ2 ) cA = 0 .                                      β 3       2
                                                                                     1   2 −iφ2
                                                                                       r
                                                                          hC |1i =             − αeiφ3 .
                                                                                                       
It can be checked that these are solved by                                          2β 3
                                                                                           e

                   cA = ei(φ1 +φ2 ) cC and                       It is quickly checked that these coefficients are consistent
                   cB = −eiφ2 cC .                               with the action on on |ηC i by making liberal use of e−iφ3 =
                                                                 α(1 − eiθ ).
Taking our formulation of the c vector, we immediately           Recall that with the correct dual states, the Kraus opera-
have βB = βC = β (implying αB = αC = α), φ2 = θ,                 tors take the form:
and:
                                                                                    KA = |ηA i hA | ,
                e−iφ3 = α(1 − eiθ )                                                 KB = |ηB i hB | , and
                       = −2iα sin(θ)eiθ/2                                           KC = |ηC i hC | .
                       = α sin(θ)ei(θ−π)/2 .
                                                                 Completeness requires:
This means:
                                                                           |A i hA | + |B i hB | + |C i hC | = I .
                       1
                              
                               θ
                   α=    csc       and
                       2       2                                 Define the vectors ux = hx |0i and vx = hx |1i. One
                       −θ + sgn(θ)π                              can check that the above relationship implies x u∗x ux =
                                                                                                                P
                  φ3 =              ,
                                                                    x vx vx = 1 and    x ux vx = 0. However, for our model,
                                                                 P ∗                         ∗
                             2
                                                                                    P

                                                                 it is straightforward (though a bit tedious) to check that:
where we take −π ≤ θ ≤ π and sgn(θ) is the sign of θ.
                                                                                            2 1 1
                                                                                 u∗x ux =    + + = 1 and
                                                                           X

                                                                             x
                                                                                            3 6 6
                                                                                             1
                                                                                 vx∗ vx =       1 + α2 − α cos φ1 .
                                                                            X                                    
                                                                                            β 2
Note, however, that for − π3 < θ < π3 , we have | csc(θ)| > 1,               x

so these values are unphysical. Thus, we see that all            Using the definitions of α, β, and φ1 , the second equation
parameters in our possible states |ηx i, as well as all the      can be simplified to:
possible transition phases, are dependent on the single
parameter θ. To construct the dual basis, we start with                                             2 + csc2 θ2
                                                                                         vx∗ vx =
                                                                                   X
the new forms of the states:                                                                                      .
                                                                                     x
                                                                                                    4 − csc2 θ2

                |ηA i = |0i ,
                                                                 This is unity only when csc2 θ2 = 1, which requires that
                |ηB i = α |0i + β |1i , and                      θ = π. This is, indeed, the model D3 that we have already
                |ηC i = α |0i + eiθ β |1i .                      seen.
                                                                 This establishes that the only two-dimensional pure-state
We note directly that we must have:                              quantum model which reproduces the 3-state MBW pro-
                                                                 cess is the one with a nonminimal statistical memory
                             2
                          r
                hA |0i =      ,                                 S(ρπ ). This means there cannot exist a quantum rep-
                             3                                   resentation of the 3-state MBW process that majorizes
                           1                                     all other representations of the same. For, if it existed,
                hB |0i = √ e−iφ1 , and
                            6                                    it must be a two-dimensional model and also minimize
                           1 iφ3                                 S(ρπ ).
                hC |0i = √ e    ,
                            6

from how the dual states contract with |ηA i. These can
