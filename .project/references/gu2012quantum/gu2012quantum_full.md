#

**Source:** gu2012quantum
**Author:**
**Pages:** 6

---

## Full Text

                                            Occam’s Quantum Razor: How Quantum Mechanics can reduce the complexity of
                                                                        classical models

                                                                   Mile Gu,1 Karoline Wiesner,2 Elisabeth Rieper,1 and Vlatko Vedral3, 4
                                                          1
                                                              Center for Quantum Technology, National University of Singapore, Republic of Singapore
                                                                            2
                                                                              School of Mathematics, Centre for Complexity Sciences,
                                                                            University of Bristol, Bristol BS8 1TW, United Kingdom
                                                                                3
                                                                                  Atomic and Laser Physics, Clarendon Laboratory,
                                                                       University of Oxford, Parks Road, Oxford OX13PU, United Kingdom
                                                                 4
                                                                   Department of Physics, National University of Singapore, Republic of Singapore
                                                                                             (Dated: October 24, 2018)
                                                          Mathematical models are an essential component of quantitative science. They generate predic-
                                                       tions about the future, based on information available in the present. In the spirit of Occam’s razor,
                                                       simpler is better; should two models make identical predictions, the one that requires less input
arXiv:1102.1994v5 [quant-ph] 2 Apr 2012


                                                       is preferred. Yet, for almost all stochastic processes, even the provably optimal classical models
                                                       waste information. The amount of input information they demand exceeds the amount of predictive
                                                       information they output. We systematically construct quantum models that break this classical
                                                       bound, and show that the system of minimal entropy that simulates such processes must necessarily
                                                       feature quantum dynamics. This indicates that many observed phenomena could be significantly
                                                       simpler than classically possible should quantum effects be involved.

                                                       PACS numbers: 02.50.-r, 89.70.-a, 03.67.-a, 02.50.Ey, 03.67.Ac


                                                               INTRODUCTION                                   dom and flipped. The obvious model that simulates this
                                                                                                              system keeps track of both switches, and thus requires an
                                                                                                              input of entropy 2. Yet, the output is simply a sequence
                                             Occam’s razor, the principle that ‘plurality is not to be
                                                                                                              of alternating 0s and 1s, and can thus be modeled know-
                                          posited without necessity’, is an important heuristic that
                                                                                                              ing only the value of the previous emission. Occam’s
                                          guides the development of theoretical models in quanti-
                                                                                                              razor stipulates that this alternative is more efficient and
                                          tative science. In the words of Isaac Newton,“We are to
                                                                                                              thus superior; it demands only an input of entropy 1 (i.e.,
                                          admit no more causes of natural things than such as are
                                                                                                              a single bit), when the original model required two. This
                                          both true and sufficient to explain their appearances.”
                                                                                                              motivates a direct interpretation of Occam’s razor; the
                                          Take for example application of Newton’s laws on an ap-
                                                                                                              optimal model of a particular behavior is the one whose
                                          ple in free fall. The future trajectory of the apple is
                                                                                                              input is of minimal entropy. Indeed, this interpretation
                                          entirely determined by a second order differential equa-
                                                                                                              has been already adopted as a principle of computational
                                          tion, that requires only its current location and velocity
                                                                                                              mechanics [1, 2].
                                          as input. We can certainly construct alternative models
                                          that predict identical behavior, that demand the apple                 Efficient mathematical models carry operational conse-
                                          color, or its entire past trajectory as input. Such theo-           quence. The practical application of a model necessitates
                                          ries, however, are dismissed by Occam’s razor, since they           its physical realization within a corresponding simulator
                                          demand input information that is either unnecessary or              (Fig. 1). Therefore, should a model demand an input
                                          redundant.                                                          of entropy C, its physical realization must contain the
                                            Generally, a mathematical model of a system of inter-             capacity to store that information. The construction of
                                          est is an algorithmic abstraction of its observable output.         simpler mathematical models for a given process allows
                                          Envision that the given system is encased within a black            potential construction of simulators with reduced infor-
                                          box, such that we observe only its output. Within a                 mation storage requirements. Thus we can directly infer
                                          second box resides a computer that executes a model of              the minimal complexity of an observed process once we
                                          this system with appropriate input. For the model to                know its simplest model. If a process exhibits observed
                                          be accurate, we expect these boxes to be operationally              statistics that require an input of entropy C to model,
                                          indistinguishable; their output is statistically equivalent,        then whatever the underlying mechanics of the observed
                                          such that no external observer can differentiate which              process, we require a system of entropy C to simulate its
                                          box contains the original system.                                   future statistics.
                                            There are numerous distinct models for any given sys-                These observations motivate maximally efficient mod-
                                          tem. Consider a system of interest consisting of two bi-            els; models that generate desired statistical behavior,
                                          nary switches. At each time-step, the system emits a 0              while requiring minimal input information. In this ar-
                                          or 1 depending on whether the state of the two switches             ticle, we show that even when such behavior aligns with
                                          coincides, and one of the two switches is chosen at ran-            simple stochastic processes, such models are almost al-
                                                                                                                             2


FIG. 1: The Relationship between models and simulators. A mathematical model is defined by a stochastic function
f that maps relevant data from the present,‘x’, to desired output statistics that coincides with the process it seeks to model.
To implement this model, we must realize it within some physical simulator. To do this, we (a) encode ’x’ within a suitable
physical system, (b) evolve the system according to a physical implementation of f and (c) retrieve the predictions of model by
appropriate measurement. On the other hand, given a simulator with entropy C that outputs statistically identical predictions,
we can always construct a corresponding mathematical model that takes the initial state of this system as input. Thus the
input entropy of a model and the initial entropy of its corresponding simulator coincide (this is also a lower bound on the
amount of information the simulator must store). In this article, we regard both models and simulators as algorithms that
map input states to desired output statistics, with implicit understanding that the two terms are interchangeable. The former
emphasizes the mathematical nature of these algorithms, while the latter their physical realization.


ways quantum. For any given stochastic process, we out-          tems [3]). On the other hand, there appears no obvious
line its provably simplest classical model, We show that         reason a model should require anything more. We say
                                                                                                               ←− →−
unless improvement over this optimal classical model vi-         that the resulting model, where C = E = I( X : X ), is
olates the second law of thermodynamics, our construc-           ideal. It turns out that for many systems such models do
tion and a superior quantum model and its corresponding          not exist.
simulator can always be constructed.                                Consider a dynamical system observed at discrete
                                                                 times t ∈ Z, with possible discrete outcomes xt ∈ Σ
                                                                 dictated by random variables Xt . Such a system can
                        RESULTS                                  be modeled by a stochastic process[4], where each re-
                                                                 alization is specified by a sequence of past outcomes
                                                                 ←− = . . . x x x , and exhibits a particular future
                                                                  x
   Framework and tools. We can characterize the ob-                          −3 −2 −1
                                                                 →
                                                                 −                                       →
                                                                                                         −       ←
                                                                                                                 −
servable behavior of any dynamical process by a joint             x = x0 x1 x2 . . . with probability P ( X = →
                                                                                                              −
                                                                                                              x |X = ← −).
                                                                                                                       x
                             ←− →−          ←−       →
                                                     −                         ←
                                                                               − →   −
probability distribution P ( X , X ), where X and X are          Here, E = I( X : X ), referred to as excess entropy[5, 6],
random variables that govern the system’s observed be-           is a quantity of relevance in diverse disciplines ranging
havior respectively, in the past and the future. Each            from spin systems [7] to measures of brain complexity[8].
particular realization of the process has a particular past      How can we construct the simplest simulator of such be-
←−, with probability P (←
 x
                          −
                          X =←  −). Should there exists a
                                x                                havior, preferably with input entropy of no more than
model for this behavior with an input of entropy C, then         E?
we may compress ←  − within a system S of entropy C, such
                   x                                                The brute force approach is to create an algorithm that
                                                                                   →
                                                                                   − ←−
that systematic actions on S generates random variables          samples from P ( X | X = ← −) given complete knowledge
                                                                                            x
                          →
                          − ← −
whose statistics obey P ( X | X = ←−).
                                   x                             of x . Such a construction accepts ←
                                                                    ←−                                 − directly as input,
                                                                                                       x
                                                                                                                 ←
                                                                                                                 −
   We seek the maximally efficient model, such that C is         resulting in the required entropy of C = H( X ), where
                                                       ←−           ←−
minimized. Since the past contains exactly E = I( X :            H( X ) denotes the Shannon entropy of the complete past.
→
−
X ) (the mutual information between past and future)             This is wasteful. Consider the output statistics resulting
                                                                                                               ←
                                                                                                               − →−
about the future, the model must require an input of             from a sequence of coin flips, such that P ( X , X ) is the
entropy at least E (this remains true for quantum sys-           uniform distribution over all binary strings. E equals
                                                                                                                                 3

0 and yet C is infinite. It should not require infinite             with entropy no greater than Cq .
memory to mimic a single coin, better approaches exist.                The key intuition for our construction lies in identify-
   Simplest classical models. -machines are the prov-              ing the cause of irreversibility within classical -machines,
ably optimal classical solution[9, 10]. They rest on the ra-        and addressing it within quantum dynamics. An -
tionale that to exhibit desired future statistics, a system         machine distinguishes two different causal states pro-
needs not distinguish differing pasts, ←   − and ←
                                           x       −0 , if their
                                                   x                vided they have differing future statistics, but makes no
future statistics coincide. This motivates the equivalence          distinction based on how much these futures differ. Con-
relation, ∼, on the set of all past output histories, such          sider two causal states, Sj or Sk , that both have potential
that ← −∼←
       x    −0 iff P (→
            x
                      − ←−) = P (→
                      X| x
                                   − ←
                                   X| x −0 ). To sample from        to emit output r at the next time-step and transition to
    →
    − ←−) for a particular ←−, a -machine need not store           some coinciding causal state Sl . Should this occur, some
P (X | x                    x
←x , only which equivalence class, (←
 −                                     −) ≡ {←
                                       x       −0 : ←
                                               x    −∼←
                                                    x       −0 },
                                                            x       of the information required to completely distinguish Sj
←−
 x belongs to. Each equivalence classes is referred to as           and Sk has been irreversibly lost. We say that Sj and
a causal state.                                                     Sk share non-distinct futures. In fact, this is both nec-
                                   ←− → −                           essary and sufficient condition for Cµ > E (See methods
   For any stochastic process P ( X , X ) with emission al-
phabet Σ, we may deduce its causal states {Si }N                    for proof).
                                                      i=1 that
form the state space of its corresponding -machine. At                The irreversibility condition. Given a stochastic
                                                                                  ←− →−
each time step t, the machine operates according to a               process P ( X , X ) with excess entropy E and statistical
                                   (r)
set of transition probabilities Tj,k ; the probability that         complexity Cµ . Let its corresponding -machine have
                                                                                                (r)
the machine will output xt = r ∈ Σ, and transition to               transition probabilities Tj,k . Then Cµ > E iff there exists
Sk given that it is in state Sj . The resulting -machine,          a non-zero probability that two different causal states, Sj
when initially set to state (←  −), generates a sequence
                                 x                                  and Sk will both make a transition to a coinciding causal
→
−                                                →
                                                 − ← −
 x according to probability distribution P ( X | X = ←        −)
                                                              x     state Sl upon emission of a coinciding output r ∈ Σ,
                                                                           (r)    (r)
as it iterates through these transitions. The resulting             i.e., Tj,l , Tk,l 6= 0. We refer to this as the irreversibility
-machine thus has internal entropy                                 condition.
                             X                                         This condition highlights the fundamental limitation of
             C = H(S) = −        pj log pj ≡ Cµ              (1)    any classical model. In order to generate desired statis-
                               j∈S                                  tics, any classical model must record each binary prop-
                                                                                            →
                                                                                            −               →
                                                                                                            −
                                                                    erty A such that P ( X |A = 0) 6= P ( X |A = 1), regardless
where S is the random variable that governs Sj = (←   −)
                                                       x            of how much these distributions overlap. In contrast,
                                  ←
                                  −
and pj is the probability that ( x ) = Sj .                        quantum models are free of such restriction. A quan-
   The provable optimality of -machines among all clas-            tum system can store causal states as quantum states
sical models motivates Cµ as an intrinsic property of               that are not mutually orthogonal. The resulting quan-
a given stochastic process, rather than just a property             tum -machine differentiates causal states sufficiently to
of -machines. Referred to in literature as the statisti-           generate correct statistical behavior. Essentially, they
cal complexity [10, 11], its interpretation as the mini-            save memory by ‘partially discarding’ A, and yet retain
mal amount of information storage required to simulate              enough information to recover statistical differences be-
such a given process has been applied to quantify self-                         →
                                                                                −                  →
                                                                                                   −
                                                                    tween P ( X |A = 0) and P ( X |A = 1).
organization [12], the onset of chaos [9] and complexity
                                                                       Improved quantum models Given an -machine
of protein configuration space [13]. Such interpretations,                                                                     (r)
however, implicitly assume that classical models are opti-          with causal states Sj and transition probabilities Tj,k ,
mal. Should a quantum simulator be capable of exhibit-              we define quantum causal states
ing the same output statistics with reduced entropy, this                                     N Xq
                                                                                                         (r)
                                                                                              X
fundamental interpretation of Cµ may require review.                                |Sj i =             Tjk |ri|ki,            (2)
   Classical models are not ideal. There is cer-                                              k=1 r∈Σ
tainly room for improvement. For many stochastic pro-
cesses, Cµ is strictly greater than E [11]; the -machine           where |ri and |ki form orthogonal bases on Hilbert spaces
that models such processes is fundamentally irreversible.           of size |Σ| and |S| respectively. A quantum -machine
Even if the entire future output of such an -machine was           accepts a quantum state |Sj i as input in place of Sj .
observed, we would still remain uncertain which causal              Thus, such a system has an internal entropy of
state the machine was initialized in. Some of that infor-                                 Cq = −Trρ log ρ,                     (3)
mation has been erased, and thus, in principle, need never                      P
be stored. In this paper we show that for all such pro-             where ρ = j pj |Sj ihSj |. Cq is clearly strictly less than
cesses, quantum processing helps; for any -machine such            Cµ provided not all |Sj i are mutually orthogonal [14].
that Cµ > E, there exists a quantum system, a quantum                 This is guaranteed whenever Cµ > E. The irre-
-machine with entropy Cq , such that Cµ > Cq ≥ E.                  versibility condition implies that there exists two causal
Therefore, the corresponding model demands an input                 states, Sj and Sk , which will both make a transition to
                                                                                                                                 4

a coinciding causal state Sl upon emission of a coincid-           ENTROPY
                           (r)     (r)
ing output r ∈ Σ, i.e., Tj,l , Tk,l 6= 0. Consequently
           q
              r T r > 0 iff T (r) , T (r) 6= 0, and thus |S i
hSj |Sk i ≥ Tj,l k,l         j,l     k,l                   j

is not orthogonal with respect to hSj |.
   A quantum -machine initialized in state |Sj i can syn-
thesis black-box behavior which is statistically identical
to a classical -machine initialized in state Sj . A simple
method is to (i) measure |Sj i in the basis |ri|ki, resulting
in measurement values r, k. (ii) Set r as output x0 and
prepare the quantum state |Sk i. Repetition of this pro-
cess generates a sequence of outputs x1 , x2 , . . . according
to the same probability distribution as the original -
                         →
                         − −
machine and hence P ( X |←  x ). (We note that while the
simplicity of the above method makes it easy to under-           FIG. 2: Complexity of the Perturbed Coin Simulation.
stand and amiable to experimental realization, there’s           While the excess entropy of the perturbed coin approaches
room for improvement. The decoding process prepares              zero as p → 0.5 (red line), generating such statistics classically
                                                                 generally requires an entropy of Cµ = 1 (green line). Encod-
Sk based of the value of k, and thus still requires Cµ bits
                                                                 ing the past within a quantum system leads to significant im-
of memory. However, there exist more sophisticated pro-          provement (purple p line). (Here, Cq = −λ+ log λ+ −λ− log λ− ,
tocols without such limitation, such that the entropy of         where λ± = 0.5 ± p(1 − p).) Note, however, that even the
the quantum -machine remains at Cq at all times. One            quantum protocol still requires an input entropy greater than
is detailed in methods). These observations lead to the          the excess entropy.
central result of our paper.
                                                        ←
                                                        − →−
   Theorem: Consider any stochastic process P ( X , X )
with excess entropy E, whose optimal classical model has         p [15]). Thus only E/Cµ = 1 − Hs (p) of the information
input entropy Cµ > E. Then we may construct a quan-              stored is useful, which tends to 0 as p → 0.5.
tum system that generates identical statistics, with input          Quantum -machines offer dramatic improvement.
                                                                                                                √          We
entropy Cq < Cµ . In addition, the entropy of this system        encode the quantum causal √    states  |S0 i =    1 −  p|0i +
                                                                 √                   √
never exceeds Cq while generating these statistics.                 p|1i or |S1 i = p|0i + 1 − p|1i within a qubit, which
                                                                 results in entropy Cq = −Trρ ln ρ, where ρ = 21 (|S0 ihS0 |+
   There always exists quantum models of greater effi-
                                                                 |S1 ihS1 |). The non-orthogonality of |S0 i and |S1 i ensures
ciency than the optimal classical model, unless the opti-
                                                                 that this will always be less than Cµ [16]. As p → 0.5, a
mal classical model is already ideal.
                                                                 quantum -machines tends to require negligible amount
   A concrete example of simulating perturbed                    of memory to generate the same statistics compared to
coins. We briefly highlight these ideas with a con-              its classical counterpart (Fig. 2).
crete example of a perturbed coin. Consider a process               This improvement is readily apparent when we model a
   ←− → −
P ( X , X ) realized by a box that contains a single coin.       lattice of K independent perturbed coins, which output a
At each time step, the box is perturbed such that the                              K
                                                                 number x ∈ Z2 that represents state of the lattice after
coin flips with probability 0 < p < 1, and the state of the      each perturbation. Any classical model must necessar-
coin is then observed. This results in a stochastic process,     ily differentiate between 2K equally likely causal states,
where each xt ∈ {0, 1}, governed by random variable Xt ,         and thus require an input of entropy K. A quantum -
represents the result of the observation at time t.              machine reduces this to KCq . For p > 0.2, Cq < 0.5, the
   For any p 6= 0.5, this system has two causal states,          initial condition of two perturbed coins may be encoded
corresponding to the two possible states of the coin; the        within a system of entropy 1. For p > 0.4, Cq < 0.1; a
set of pasts ending in 0, and the set of pasts ending in 1.      system of coinciding entropy can simulate 10 such coins.
We call these S0 and S1 . The perturbed coin is its own          This indicates that quantum systems can potentially sim-
best classical model, requiring exactly a system of en-          ulate N such coins upon receipt of K  N qubits, pro-
tropy Cµ = 1, namely the coin itself, to generate correct        vided appropriate compression (through lossless encod-
future statistics.                                               ings [17]) of the relevant past.
   As p → 0.5, the future statistics of S0 and S1 be-
come increasingly similar. The stronger the perturba-
tion, the less it matters what state the coin was in                                     DISCUSSION
prior to perturbation. This is reflected by the obser-
vation that E → 0 (in fact E = 1 − Hs (p) [7], where                In this article, we have demonstrated that any stochas-
Hs (p) = −p log p − (1 − p) log(1 − p) is the Shannon en-        tic process with no reversible classical model can be fur-
tropy of a biased coin that outputs head with probability        ther simplified by quantum processing. Such stochas-
                                                                                                                                   5

tic processes are almost ubiquitous. Even the statistics          by ΩE . Similarly, we say an ordered pair (Sk ∈ S, r ∈ Σ) is
                                                                                                         (r)
of perturbed coins can be simulated by a quantum sys-             a valid reception configuration iff Tj,k 6= 0 for some Sj ∈ S,
tem of reduced entropy. In addition, the quantum recon-           and denote the set of all valid reception configurations by ΩR .
struction can be remarkably simple. Quantum operations               We define the transition function f : ΩE → ΩR . Such
on a single qubit, for example, allows construction of a          that f (Sj , r) = (Sk , r) if the -machine set to state Sj will
                                                                  transition to state Sk upon emission of r. We also introduce
quantum epsilon machine that simulates such perturbed
                                                                  the shorthand Xba to denote the the list of random variables
coins. This allows potential for experimental validation          Xa , Xa+1 , . . . , Xb .
with present day technology.                                         We first prove the following observations.
   This result has significant implications. Stochastic pro-
cesses play an ubiquitous role in the modeling of dynam-             1. f is one-to-one iff there exist no distinct causal states,
                                                                                                 (r)  (r)
ical systems that permeate quantitative science, from cli-              Sj and Sk , such that Tj,l , Tk,l 6= 0 for some Sl .
mate fluctuations to chemical reaction processes. Classi-               Proof: Suppose f is one-to-one, then f (Sj , r) =
cally, the statistical complexity Cµ is employed as a mea-              f (Sk , r) iff Sj = Sk . Thus, there does not exist two dis-
                                                                                                                        (r)    (r)
sure of how much structure a given process exhibits. The                tinct causal states, Sj and Sk such that Tj,l , Tk,l 6= 0
rationale is that the optimal simulator of such a process               for some Sl . Conversely, if f is not one-to-one, so that
                                                                        f (Sj , r) = f (Sk , r) for some Sj 6= Sk . Let Sl be the
requires at least this much memory. The fact that this                                                               (r)    (r)
                                                                        state such that f (Sj , r) = (Sl , r), then Tj,l , Tk,l 6= 0.
memory can be reduced quantum mechanically implies
the counterintuitive conclusion that quantizing such sim-            2. H(St−1 |Xt St ) = 0 iff f is one-to-one.
ulators can reduce their complexity beyond this classical               Proof: Suppose f is one-to-one. Then for each
bound, even if the process they’re simulating is purely                 (Sj , r) ∈ ΩR , there exists a unique (Sk , r) such that
classical. Many organisms and devices operate based on                  f (Sk , r) = (Sj , r). Thus, given St = Sj and Xt = r, we
the ability to predict and thus react to the environment                may uniquely deduce Sk . Therefore H(St−1 |Xt St ) =
                                                                        0.     Conversely, should H(St−1 |Xt St ) = 0, then
around them. The possibility of exploiting quantum dy-                  H(St−1 Xt |Xt St ) = 0, and thus f is one-to-one.
namics to make identical predictions with less memory
implies that such systems need not be as complex as one              3. H(St−1 |Xt St ) = 0 implies H(St−1 |Xt0 ) = H(St |Xt0 ).
originally thought.                                                     Proof: Note that (i) H(St−1 |Xt0 St ) = H(St |Xt0 St−1 )+
                                                                        H(Xt0 St−1 ) − H(Xt0 St ) and (ii) that, since the output
   This leads to the open question, is it always possible
                                                                        of f is unique for a given (r, S) ∈ ΩE , H(St |Xt St−1 ) =
to find an ideal simulator? Certainly, Fig. 2 shows that                0. (ii) implies that H(St |Xt0 St−1 ) = 0 since un-
our construction, while superior to any classical alterna-              certainty can only decrease with additional knowl-
tive, is still not wholly reversible. While this irreversibil-          edge and is bounded below by 0.              Substituting
ity may indicate that more efficient quantum models ex-                 this into (i) results in the relation H(St−1 |Xt St ) =
ist, it is also possible that ideal models remain forbidden             H(Xt0 St−1 ) − H(Xt0 St ).Thus H(St−1 |Xt St ) = 0 im-
within quantum theory. Both cases are interesting. The                  plies H(St−1 |Xt0 ) = H(St |Xt0 ).
former would indicate that the notion of stochastic pro-             4. H(St−1 |Xt0 ) = H(St |Xt0 ) implies Cµ = E.
cesses ‘hiding’ information from the present [11] is merely             Proof: The result follows then from two known prop-
a construct of inefficient classical probabilistic models,              erties of -machines, (i) limt→∞ H(St |Xt0 ) = 0 and
while the latter hints at a source of temporal asymmetry                (ii) Cµ − E = H(S−1 |X∞      0 ) [10]. Now assume that
within the framework of quantum mechanics; that it is                   H(St−1 |Xt0 ) = H(St |Xt0 ), recursive substitutions im-
                                                                        ply that H(S−1 |Xt0 ) = H(St |Xt0 ). In the limit where
fundamentally impossible to simulate certain observable
                                                                        t → ∞, the above equality implies Cµ − E = 0.
statistics reversibly.
                                                                     5. Cµ = E implies H(St−1 |Xt St ) = 0.
                                                                        Proof: Since (i) Cµ = E = H(S−1 |X∞                  0 )  ≤
                        METHODS:                                        H(S−1 |X∞0 S0 ),     and      (ii)   H(St−1 |Xt St )      =
                                                                        H(S−1 |X0 S0 ), it suffices to show that H(S−1 |X∞ 0 S0 ) =
                                                                        H(S−1 |X0 S0 ).
   Proof of Theorem 1. Let the aforementioned -machine
have causal states S = {Si }N1 and emission alphabet Σ. Con-
                                                                        Now H(S−1 |X∞                    ∞                ∞
                                                                                        0 S0 ) = H(X0 S−1 S0 ) − H(X0 S0 ) =
                                                                             ∞                                        ∞
sider an instance of the -machine at a particular time-step            H(X1 |S−1 X0 S0 ) + H(X0 S−1 S0 ) − H(X1 |X0 S0 ) −
t. Let St and Xt be the random variables that respectively              H(X0 S0 ).      But, by the Markov property of
governs its causal state and observed output at time t, such            causal states, H(X∞                             ∞
                                                                                                1 |S−1 X0 S0 ) = H(X1 |X0 S0 ),
                                                                                        ∞
that the transition probabilities that define the -machine can         thus H(S−1 |X0 S0 ) = H(X0 S−1 S0 ) − H(X0 S0 ) =
be expressed as                                                         H(S−1 |X0 S0 ), as required.
             (r)
           Tj,k = P (St = Sk , Xt = r|St−1 = Sj ).         (4)       Combining (1), (2), (3) and (4), we see that there exists a
                                                                  non-zero probability that two distinct causal states, Sj and
                                                                                   (r)  (r)
We say an ordered pair (Sj ∈ S, r ∈ Σ) is a valid emission        Sk such that Tj,l , Tk,l 6= 0 for some Sl only if Cµ 6= E.
                   (r)                                            Meanwhile (1), (2), and (5) imply that there exists no two
configuration iff Tj,k 6= 0 for some Sk ∈ S. That is, it is
                                                                                                                (r)   (r)
possible for an -machine in state Sj to emit r and transit to    distinct causal states, Sj and Sk such that Tj,l , Tk,l 6= 0 for
some Sk . Denote the set of all valid emission configurations     some Sl only if Cµ = E. Theorem 1 follows.
                                                                                                                                      6

                                                                       can thus execute correctly even if all outputs remained un-
                                                                       measured, and thus are truly ignorant of which causal state
                                                                       they’re in!). Thus, the physical application of the above proto-
                                                                       col generates correct predication statistics without requiring
                                                                       more than memory Cq .
                                                                          Acknowledgments— M.G. would like to thank C. Weed-
                                                                       brook, H. Wiseman, M. Hayashi, W. Son and K. Modi
                                                                       for helpful discussions. M.G. and E.R. are supported by
                                                                       the National Research Foundation and Ministry of Educa-
                                                                       tion, in Singapore. K.W. is funded through EPSRC grant
                                                                       EP/E501214/1. V.V. would like to thank EPSRC, QIP IRC,
FIG. 3: Quantum circuit representation of the refined predic-          Royal Society and the Wolfson Foundation, National Research
tion protocol.                                                         Foundation (Singapore) and the Ministry of Education (Sin-
                                                                       gapore) for financial support.

   Constant Entropy Prediction Protocol. Recall that
in the simple prediction protocol, the preparation of the next
quantum causal state was based on the result of a measure-
ment in basis |ki. Thus, although we can encode the initial             [1] J. P. and Crutchfield, Physica D: Nonlinear Phenomena
conditions of a stochastic process within a system of entropy               75, 11 (1994).
Cq , the decoding process requires an interim system of entropy         [2] A. Ray, Signal Processing 84, 1115 (2004).
Cµ . While this protocol establishes that quantum models                [3] A. S. Holevo, in Proceedings of the Second Japan–
require less knowledge of the past, quantum systems imple-                  USSR Symposium on Probability Theory, edited by
menting this specific prediction protocol still need Cµ bits of             G. Maruyama and J. V. Prokhorov (Springer-Verlag,
memory at some stage during their evolution.                                Berlin, 1973), pp. 104–119, lecture Notes in Mathemat-
   This limitation is unnecessary. In this section, we present              ics, vol. 330.
a more sophisticated protocol whose implementation has en-              [4] J. L. Doob, Stochastic Processes (Wiley, New York,
tropy Cq at all points of operation. Consider aq   quantum -               1953).
                                                      (r)               [5] J. P. Crutchfield and D. P. Feldman, Chaos: An Inter-
machine initialized in state |Sj i = n
                                      P      P
                                         k=1   r∈Σ   Tjk |ri|ki.
                                                                            disciplinary Journal of Nonlinear Science 13, 25 (2003).
We refer the subsystem spanned by |ri as R1 , and the sub-              [6] P. Grassberger, International Journal of Theoretical
system spanned by |ki as K. To generate correct predictive                  Physics 25, 907 (1986).
statistics, we                                                          [7] J. P. Crutchfield and D. P. Feldman, Phys. Rev. E 55,
                                                                            R1239 (1997).
   1. Apply a general quantum operation on  q K that maps
                                               (r)                      [8] G. Tononi, O. Sporns, and G. M. Edelman, Proceedings
      any given |Sj i to |Sj0 i = n
                                 P     P
                                   k=1  r∈Σ   Tjk |ri|Sk i on               of the National Academy of Science 91, 5033 (1994).
      R1 × R2 × K, where R2 is a second Hilbert space of                [9] J. P. Crutchfield and K. Young, Phys. Rev. Lett. 63, 105
      dimension |Σ|. Note that this operation always exists,                (1989).
      since it is defined by Krauss operators Bk = |Sk ihk|            [10] C. Rohilla Shalizi and J. P. Crutchfield, Journal of Statis-
      that satisfy k Bk† Bk = 1.
                   P
                                                                            tical Physics 104, 817 (2001), arXiv:cond-mat/9907176.
   2. Output R1 . Measurement of R1 in the |ri basis leads             [11] J. P. Crutchfield, C. J. Ellison, and J. R. Mahoney, Phys.
      to a classical output r whose statistics coincide with                Rev. Lett. 103, 094101 (2009).
      that of its classical counterpart, x1 .                          [12] C. R. Shalizi, K. L. Shalizi, and R. Haslinger, Phys. Rev.
                                                                            Lett. 93, 118701 (2004).
   3. The remaining subsystem R2 × K is retained as the                [13] T. K. Chun-Biu Li, Haw Yang, Proceedings of the Na-
      initial condition of the quantum -machine at the next                tional Academy of Sciences 105, 536 (2008).
      timestep.                                                        [14] M. A. Nielsen and I. L. Chuang, Quantum computation
   See Fig. 3 for a circuit representation of the protocol. Step            and quantum information (Cambridge University Press,
(1) does not increase system entropy since entropy is con-                  Cambridge, 2000).
served under addition of pure ancilla, while hSj0 |Sk0 i ≥ hSj |Sk i   [15] C. E. Shannon, Bell Sys. Tech. J. 30, 50 (1951).
                                                                       [16] G. S. G. Benenti, G. Casati, Principles of Quantum In-
                 P out R1 in step (3) leaves the epsilon ma-
for all j, k. Tracing
                                                                            formation and computation II. (World Scientific, 2007).
chine in state      pj |Sj i|Sj i, which has entropy Cq . Finally,
the execution of the protocol does not require knowledge of            [17] K. Bostroem and T. Felbinger, Phys. Rev. A 65, 032313
the measurement result r (In fact, the quantum -machine                    (2002).
