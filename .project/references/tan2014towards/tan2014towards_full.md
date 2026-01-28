#

**Source:** tan2014towards
**Author:**
**Pages:** 10

---

## Full Text

                                                              Towards Quantifying Complexity with Quantum Mechanics

                                                         Ryan Tan,1, 2 Daniel R. Terno,3 Jayne Thompson,2 Vlatko Vedral,4, 2, 5 and Mile Gu1, 2
                                                                       1
                                                                         Center for Quantum Information, Institute for Interdisciplinary
                                                                      Information Sciences, Tsinghua University, 100084 Beijing, China
                                              2
                                                Centre for Quantum Technologies, National University of Singapore, 3 Science Drive 2, 117543 Singapore, Singapore
                                                    3
                                                      Department of Physics and Astronomy, Macquarie University, Sydney, New South Wales 2109, Australia
                                                   4
                                                      Department of Physics, University of Oxford, Clarendon Laboratory, Oxford, OX1 3PU, United Kingdom
                                                   5
                                                     Department of Physics, National University of Singapore, 2 Science Drive 3, 117551 Singapore, Singapore
                                                           While we have intuitive notions of structure and complexity, the formalization of this intuition
                                                        is non-trivial. The statistical complexity is a popular candidate. It is based on the idea that the
                                                        complexity of a process can be quantified by the complexity of its simplest mathematical model - the
                                                        model that requires the least past information for optimal future prediction. Here we review how
                                                        such models, known as -machines can be further simplified through quantum logic, and explore the
arXiv:1404.6255v2 [quant-ph] 23 Sep 2014


                                                        resulting consequences for understanding complexity. In particular, we propose a new measure of
                                                        complexity based on quantum -machines. We apply this to a simple system undergoing constant
                                                        thermalization. The resulting quantum measure of complexity aligns more closely with our intuition
                                                        of how complexity should behave.

                                                        PACS numbers: 03.65.-w, 03.67.-a.


                                              Are there any universal laws governing the evolution          a given process thus introduces a more suitable measure
                                           of complexity? While the second law of thermodynam-              of complexity. Known as the statistical complexity, Cµ ,
                                           ics indicates ever increasing entropy, complexity seems          its clear operational significance and relative ease of eval-
                                           to behave differently. The hot, smooth plasma near the           uation have resulted in its widespread adoption in diverse
                                           Universe’s birth and the final state of thermal equilibrium      contexts
                                           predicted by its heat death both appeal to our intuition         [4–9].
                                           of simplicity. Yet between these extremes, where there              Nevertheless, statistical complexity still displays cer-
                                           are stars, galaxies and life, the universe is complex; and       tain incongruities. Notably, it is not continuous – in-
                                           because of that it is interesting. To answer this question,      finitesimal perturbations in the statistics of a process can
                                           one must first quantify complexity.                              lead to large jumps in its statistical complexity. A physi-
                                              This task is non-trivial. While we have intuitive no-         cal process that asymptotically approaches total random-
                                           tions of what is interesting or complex, they are decep-         ness can have monotonically increasing statistical com-
                                           tively difficult to formalize. The first attempts to quan-       plexity, even if its final steady state has statistical com-
                                           tify complexity came in the form of Kolmogorov com-              plexity zero [6]. This seems to contradict our intuition of
                                           plexity [1]. This measure equates the complexity of a            what complexity should be.
                                           sequence of numbers to the size of the minimal computer             The results discussed so far however, have been lim-
                                           program that generates the sequence. While Kolmogorov            ited to classical logic. Reality is ultimately quantum me-
                                           complexity correctly identifies a constant sequence, con-        chanical. If quantum logic allows us as to build simpler
                                           sisting entirely of 0s, as simple; it is maximized by se-        predictive models - models that use less past information
                                           quences that are completely random. This makes the               - then the quantum analogue of statistical complexity
                                           measure unsatisfying for characterizing complexity, be-          could be a more fitting quantifier of structure. Indeed,
                                           cause it seems to misconstrue randomness with struc-             it has been recently demonstrated that quantum models
                                           ture [2].                                                        can optimally predict the future statistics of a classical
                                              A promising way to avoid this problem came from the           stochastic process while generically storing less informa-
                                           study of computational mechanics, where one is con-              tion about the past than their classical counterparts [10].
                                           cerned in building -machines, the simplest predictive           Systems that are complex to predict classically may be
                                           model of a supplied stochastic process [3]. One reason is        simpler quantum mechanically.
                                           that if a stochastic process is more complex, then repli-           The objective of this article is to explore how quan-
                                           cating its future statistics will require more information       tum logic can improve our understanding of what makes
                                           about its past. A completely random process, for exam-           a process interesting and complex, and ultimately con-
                                           ple, requires no past information to reproduce its future        tribute to discovering how complexity evolves. We re-
                                           statistics; and nor would a process that outputs only zero.      view -machines - the provably simplest classical models;
                                           Meanwhile, a process with less trivial behavior, such as         and how they can be further simplified through quan-
                                           one which alternates between zero and one on successive          tum logic. This motivates us to introduce a new measure
                                           emissions, can only be faithfully replicated by storing its      of complexity, Cq , based on the complexity of quantum
                                           last emission - and is thus more complex. The minimum            -machines.
                                           amount of past information required to optimally predict            We apply these ideas to a toy system featuring mono-
                                                                                                                           2

tonically increasing entropy. First we show that the sys-          To formalize this intuition, envision our system en-
tem’s complexity, when characterized by Cq , aligns more         cased in a black box, that simply outputs the outcome
closely with our intuition of how complexity should be-          xt ∈ Σ at time t ∈ Z. In a second black box, a computer
have. In addition to being zero when the system features         attempts to simulate the process through execution of an
zero or maximal entropy, it is also continuous; an in-           appropriate mathematical model. It takes as input some
finitesimal perturbation in the statistics of the process        S that is a function of past observations, ←
                                                                                                            − and outputs
                                                                                                            x
will cause an infinitesimal change in Cq . Thus, we high-        appropriate future statistics. For this simulation to be
light the relevance of quantum mechanics in studying how         completely faithful the two boxes must be indistinguish-
structure and complexity persist and evolve.                     able. For each instance of the process with past ←−, the
                                                                                                                   x
   The article is structured as follows. Section I will re-                                                  →
                                                                                                             −
                                                                 model must output statistical predictions x , according
view statistical complexity, -machines, and their exten-        to the statistical distribution
sion to quantum -machines. Section II reviews a new                                       →
                                                                                           − ←  − →
measure of complexity based on the complexity of these                                  P ( X | X = x ).              (1)
quantum e-machines [10]. Subsection III B then applies
                                                                 The amount of information such a model requires to track
this measure to a toy system with monotonically increas-
                                                                 is then determined by the minimal amount of space it
ing noise; and highlights how the complexity of quantum
                                                                 needs to store about ← −. Formally this is given by the
                                                                                        x
and classical -machines diverge. Concluding remarks are
                                                                 information entropy of S, the random variable that gov-
presented in Section IV.
                                                                 erns input variable S. We refer to this as the complexity
                                                                 of a given predictive model.
                 I.   PRELIMINARIES
                                                                          B.   Classical Statistical Complexity
   This section provides a background mechanism of in-
ferring the statistical complexity of observed phenom-              The statistical complexity for a process is determined
ena and their quantum extensions. For a more extensive           by the complexity of its simplest model – that correctly
treatment of these topics, see Refs. [4, 10, 11]. Famil-         simulates the process while requiring the least amount of
iarity with quantum information to the level of [12] is          information about ←   −. Thus we must find the best way
                                                                                       x
assumed.                                                         of compressing the past without losing information about
                                                                 the future.
                                                                    An immediate brute-force attempt is to store the en-
  A.    Computational Mechanics, Complexity and                                                               →
                Predictive Models
                                                                 tire past. Such a model takes the input x directly and
                                                                 outputs the future according to (1) and thus stores the
                                                                                                           ←−
                                                                 input with information content C = H( X ), where H de-
   Computational mechanics seeks to study the complex-
                                                                 notes the Shannon entropy. This is clearly not efficient.
ity of systems through the lens of predictive models. The                                                           ←− →
                                                                                                                       −
general approach is to assume that a system’s behavior           For example, for a series of fair coin tosses P ( X , X ) is
can probed at discrete points in time t, with outcomes           uniform over the distribution of binary strings. Thus C
xt ∈ Σ dictated by random variable Xt . Here, Σ defines          is infinite, implying that a simulation using this approach
the set of possible observable outcomes.                         will require an infinite amount of memory. Clearly better
   In the ideal scenario, the system may be probed in-           approaches exist.
definitely. The observable behaviour of such a system is            The simplest classical predictive models are epsilon
                                ↔
a sequence of output values x = · · · x−2 x−1 x0 x1 x2 · · · ,   machines (-machines) [3, 4].         Jointly proposed by
        →                      →                                 Crutchfield and Shalizi, -machines are based on the
where x = · · · x−2 x−1 and x = x0 x1 x2 · · · are the out-      reasoning that two different pasts need only be distin-
put sequences of the past and future respectively. This          guished if they have differing future statistics. This
results in a stochastic process, defined by the joint prob-      motivates an equivalence relation on the set of pasts,
                         ←
                         − → −          ←−      →
                                                −
ability distribution P ( X , X ). Here, X and X are the                                                          →       →0
                               →      →                          ∼, such that for any two distinct pasts, x and x ,
random variables governing x and x . Each realization            →      → 0           →
                                                                                      − ← −     →        →
                                                                                                         − ← −    → 0
                                       →                         x ∼ x ⇐⇒ P ( X | X = x ) = P ( X | X = x ). Each
of the system has a particular past x with probability
   ←− →                                       →                  equivalence class is referred to as a causal state Si gov-
P ( X = x ) and exhibits a particular future x with prob-        erned by a random variable S. Let S = {Si }i=1,2,··· ,N
           →
           −     →← − →
ability P ( X = x | X = x ).                                     denote the set of all causal states where N represents the
   Computational mechanics aims to infer the complex-            total number of causal states. An -machine does not
ity of the system through these statistics. It asks, if we       store ← −, but only stores the equivalence class to which
                                                                         x
are to build a mathematical model of the process with            ←−
                                                                  x belongs. More formally:
statistically indistinguishable behavior what is the min-
imal amount of information it needs to keep about past           Definition I.1 (-machines) Given a stochastic pro-
                                                                         ←− → −
observations? The more memory required the greater its           cess P ( X , X ), we can define its -machine as follows:
complexity.                                                      The -machine of the process is the ordered pair {, T},
                                                                                                                              3
                                                     →
where  is the causal state function such that ( x ) = Si ,    where |ri belongs to a Hilbert space of dimension |Σ|
                  (r)                                           and |ki to a space of dimension |S|. The quantum causal
Si ∈ S, T = {Tj,k |r ∈ Σ, Sj , Sk ∈ S} is a collection
                                       (r)                      states, |Si i, are in general not orthogonal; nevertheless
of transition probabilities, with Tj,k = P (St = Sk , Xt =      we can construct a systematic method to sample from
r|St−1 = Sj ).                                                     →
                                                                   − ← −
                                                                P (X |X = ←    −), when given the appropriate quantum
                                                                               x
                                                →               causal state |Si = (←   −)i.
                                                                                         x
  After initiating an -machine in state ( x ), there exists      To see this, consider a machine that takes |Si = (←     −)i
                                                                                                                            x
standard algorithms to systematically generate desired          directly as its input. It can generate the the correct out-
future statistics. At each time-step t, an -machine in         put statistics at each time step, by measuring |Sj i in the
causal state Sj will emit output r ∈ Σ and transit to           |ri basis. Each specific outcome r occurs with probability
                                    (r)
causal state Sk , with probability Tj,k .                         (r)
                                                                Tj,k , and collapses the system to |ki. The machine sets
  Since there are no simpler classical models, Crutchfield      the output x0 equal to “r”, and the quantum -machine
and Shalizi defined the statistical complexity of a given       then applies a quantum operation that maps |ki to state
process to be synonymous with the internal entropy of           |Sk i. Iterating this protocol will give a series of output
the -machine, i.e.,                                            values x0 x1 x2 · · · with the correct statistical distribution.
                                 N
                                                                This can be formalized as:
                                 X
              Cµ = H(S) = −             pi log2 pi       (2)    Definition I.2 The quantum -machine of a process
                                                                   ←− → −
                                 i=1                            P ( X , X ), is the ordered pair {q , Sq } where Sq =
                                 →                              {|Si i}i=1,2,...,N is the set of quantum causal states, and
where pi = P (S = Si = ( x )) is the probability that                                           →
←−∈S.                                                           q is a function such that q ( x ) = |Si i.
 x     i
   Statistical complexity does not equate randomness              The complexity of the resulting model is again deter-
with structure. For a completely random process the con-        mined by the entropy of its input that is given by the
ditional future for all pasts is the same. Thus only one        von Neumann entropy
causal state is needed to specify the process and Cµ = 0.                             Cq = − Tr ρ log ρ                     (4)
This implies that completely random processes have no                       P
inherent structure. On the other hand, a process that           where ρ = i pi |Si ihSi | and pi is the probability of ini-
emits a constant bit-string also features zero complex-         tiating the machine in state |Si i. Since the |Si i are
ity as any probability distribution of a constant variable      generally non-orthogonal, Cq is often strictly less than
has zero entropy. In between these extremes, statistical        Cµ . Quantum -machines thus can have complexity be-
complexity can be expected to peak.                             low what is possible using any classical predictive model.
   Other properties of statistical complexity are more             The advantage of quantum -machines over their classi-
puzzling. Using a simple example of a general two-state         cal counterparts rests in the observation that future pre-
process depicted in Fig. 1, for q0 = q1 = 0.5 + δ, where        dictions do not require complete knowledge of the causal
δ > 0 is arbitrarily small, the output is very close to being   state the process started in. Indeed in the case of classical
completely random. Nevertheless, the conditional futures        -machines two instances of a process can start in differ-
                                                                                                                  r        r
of the two causal states differ, and Cµ = 1. However, at        ent causal states, Si and Sj , where both Ti,k       and Tj,k
                                                                                                     r   r
δ = 0, Cµ is 0. Such discontinuity appears surprising for       are non-zero. With probability Ti,k    Tj,k  both -machines
a measure of structure.                                         will transition to some coinciding causal state Sk upon
                                                                the same emission r. If this happens, all future statistics
                                                                will be identical and no amount of future observations
                C.   Quantum is Simpler                         can ever fully identify whether the system started in Si
                                                                or Sj . Thus some of the information used to distinguish
                                                                between Si and Sj is wasted.
   All the above results assume our mathematical model
                                                                   Quantum mechanics allows the freedom to store dif-
processes classical information. Can a quantum exten-
                                                                ferent causal states as non-orthogonal quantum states,
sion of statistical complexity have different qualitative
                                                                without employing classical randomness. Quantum -
behavior?
                                                                machines exploit this – they utilize quantum causal states
   Quantum logic allows the input information to be en-         that distinguish past causal states only to a degree suf-
coded into a quantum mechanical system. The advantage           ficient for generating correct statistical behaviour. For
here is that this gives extra freedom to encode informa-        example, for a process with two classical causal states
tion in quantum superpositions. This lends a quantum            S0 and S1 , the emission alphabet Σ = {0, 1} and transi-
refinement to the standard -machine. In quantum -                                 r
                                                                tion probabilities Tj,k = δkr Tjk (where δkr is the Kronecker
machines each causal state is associated with a quantum
                                                                delta) we have quantum causal states
causal state:                                                                        q              q
                                                                                         (0)            (1)
                         |S|                                                 |S0 i = T0,0 |00i + T0,1 |11i                (5)
                         X   Xq       (r)
               |Sj i =               Tj,k |ri|ki,        (3)                         q
                                                                                         (0)
                                                                                                    q
                                                                                                        (1)
                         k=1 r
                                                                             |S1 i = T1,0 |00i + T1,1 |11i                (6)
                                                                                                                                 4

                                                          q0    |   r=1


                        1 − q0   |   r=0         S0                             S1      1 − q1     |   r=1


                                                          q1    |   r=0

FIG. 1: The causal state diagram for a two-causal state process. The causal states, S0 and S1 , are represented by a pair of
circles. Arrows denote possible transitions. An arrow pointing from Sj to Sk , j, k ∈ {0, 1}, is labeled by the probability that
                                                                                                    r
the epsilon machine will transition from causal state Sj to causal state Sk upon emitting xt = r: Tj,k , we also explicitly specify
                                                                                    0
the matching value of r. For example, the above process has P (S0 , Xt = 0|S1 ) = T1,0 = q1 with accompanying emission r = 0.


Since we are dealing effectively with a two-dimensional             ity, such an assignment would be rash. The question of
space we label |00i as |0i
                         f and |11i as |1i.
                                         f If S1 and S2             whether quantum -machines are the simplest quantum
have non-zero probability of transitioning to the same              models remains open. In this article we refer to Cq as the
                                 (k)       (k)
causal state, Sk , then clearly T0,k and T1,k are non-zero.         quantum -machine complexity to avoid confusion, and
                                                                    leave questions of whether even simpler quantum models
Therefore hS1 | S2 i > 0, and hence Cq ≤ Cµ . Quan-
                                                                    exist for future work.
tum -machines are simpler then their simplest classical
alternatives, and this difference becomes ever more pro-
nounced as the future statistics of their associated causal
states becomes more similar.                                               B.    The Classical-Quantum Divergence


  II.   COMPLEXITY WITH QUANTUM LOGIC
                                                                       To illustrate the divergence in the complexity of classi-
                                                                    cal and quantum -machines, we outline a simple process
                                                                    involving a box containing a single coin. At each time-
        A.   Quantum -machines and Complexity                      step t the box is perturbed and the state of the coin is
                                                                    measured. This results in a binary output that is either
   How does the advent of quantum logic affect our orig-            heads (xt = 0) or tails (xt = 1), governed by random
inal motivation of studying -machines? The statistical             variable Xt . The probability distribution over an infinite
complexity was proposed as a measure of structure in line           sequence of such measurements then defines a stochastic
with the ideal that the more memory required to model                           ←− →−
                                                                    process P ( X , X ).
a process the greater its complexity. The above obser-                 We assume that the act of perturbation may flip the
vations indicate that if we adopt such ideals we must               state of the coin. The coin may be biased, such that
necessarily accept that what we perceive to be complex              perturbing a coin in state k will cause it to flip with
depends on what information theory we use.                          probability 0 < qk < 1, k ∈ {0, 1}. Note that the special
   If we are limited to classical logic then the simplest way       case of an unbiased coin was analyzed in [10], where it
to model a process is through classical -machines result-          was referred to as the perturbed coin.
ing in a perceived complexity of Cµ . Thus, Crutchfield
                                                                       The resulting process is clearly Markovian; all infor-
defined Cµ as the statistical complexity – and motivated                            →
                                                                                    −
it as an intrinsic measure of structure and complexity of           mation about X is contained in X−1 . For q0 , q1 6= 0.5,
                                 ←− →−                              we have two causal states. One equivalence class con-
a given stochastic process P ( X , X ).
                                                                    taining all pasts ending in “0”, signifying the last state
   However, if we admit quantum information and quan-
                                                                    was heads, and the other containing pasts ending in “1”.
tum logic a stochastic process is likely to look simpler. If
                                                                    These causal states are denoted as S0 and S1 . The tran-
we are to model the process using a quantum -machine,
                                                                    sition probabilities for the corresponding -machine are
then the perceived complexity of the system, Cq , is often                            (r)
strictly less than Cµ . To a creature that employs quan-            then given by Tjk = δkr Tjk , where Tjk are elements of
tum -machines reality would appear simpler. Could Cq               the matrix
provide an alternative quantifier of complexity?                                                             
   This article explores the behavior of Cq . In studying                                       1 − q0   q1
                                                                                      T =                       .              (7)
how it evolves for a simple process we show how our no-                                           q0   1 − q1
tions of structure and complexity can diverge in the pres-
ence of quantum logic. We outline a scenario in which               Together these objects define the classical -machine of
the behavior of Cq aligns much more closely with our                the process (Fig 1).
expectations of how complexity behaves.                               The statistical complexity of the process is then de-
   We note, however, that while it is tempting to im-               termined by H(S) = −p0 log2 p0 − p1 log2 p1 , where
mediately name Cq as the quantum statistical complex-               pi = P ((←−) ∈ S ) for i ∈ {0, 1}. To find these, let
                                                                               x       i
                                                                                                                                        5

                                                                              perturbation in the observed statistics leads to a large
                                                                              change in its perceived structure and complexity? The
                                                                              use of quantum -machines seems to resolve this conun-
                                                                              drum; and thus presents a promising refinement of their
                                                                              classical predecessors.


                                                                              III. THE THERMALIZING QUBIT CLOUD - A
                                                                               SYSTEM OF EVER INCREASING ENTROPY

                                                                                 Can quantum -machines be used to formalize our in-
                                                                              tuition of how complexity should evolve? We shed light
                                                                              on this by studying how complexity evolves in a sim-
FIG. 2: A plot of both the classical statistical complexity
Cµ (red, dashed) and Cq (blue, solid) for the perturbed coin,                 ple system featuring monotonically inreasing entropy - a
against the probability of flipping q = q1 = q2 . At q = 0.5                  cloud of qubits undergoing gradual thermalization. Such
the coin is completely fair and the output is random, mak-                    an environment adheres to the second law of thermody-
ing it unnecessary to store any information about the past to                 namics; mimicking our ideal that all systems graduate
optimally predict the future. This plot illustrates the discon-               towards a state of total disorder.
tinuity in Cµ which jumps directly from 1 to 0 at q=0.5. In                      Our intuition tells us that at either end of the scale
contrast Cq is a continuous function of q.                                    complexity should be minimal. The system should evolve
                                                                              from something simple, to something more complex, and
                                                                              back. Should Cq be a true quantifier of complexity, we
p = (p0 , p1 ); then p satisfies p = T p, with solution                       would expect it to exhibit similar behavior.
                             1
                                                                               Consider an environmental bath containing a large
                                    q1
                     p=                   .                           (8)     number of (N >> 1) qubits, with a global thermaliza-
                         q1 + q0 q0
                                                                              tion parameter λ. When λ = 0, the system is pure,
Thus p0 = q0q+q
             1
                  and p1 = q0q+q
                              0
                                   . The perturbed coin its                   and all qubits are in the state ρ(0) = |0ih0|. When
                1                1
own simplest model, with statistical complexity                               λ = 1, all qubits are maximally random with ρ(1) = I/2.
                                                                              With gradual thermalization, the system, monotonically
                                                                          evolves from order to disorder, such that each qubit
          q0                 q0              q1                q1             evolves according to
Cµ = −         log                      −         log                     .
       q0 + q1            q0 + q1         q0 + q1           q0 + q1
                                                              (9)                                                       λ
                                                                                             ρe (λ) = (1 − λ)|0ih0| +     I.         (10)
√  By  comparison   the quantum     causal  states  √ are |S i
                                                            0 =                                                         2
                √                      √
   1 − q0 |0i + q0 |1i and |S1 i = q1 |0i + 1 − q1 |1i.
Thus the complexity of the quantum -machine is Cq =                          The whole system can be described as ρ⊗N  e (λ). Clearly
− Tr ρ log ρ, with ρ = p0 |S0 ihS0 | + p1 |S1 ihS1 |.                         this system exhibits monotonically increasing entropy,
   The complexity of classical -machines and their quan-                     evolving smoothly from the minimum value of 0 to the
tum counterpart are plotted in Fig 2 for the special case                     maximum value of N .
where the coin is unbiased, i.e., q0 = q1 = q. The clas-                         To characterize how complexity evolves in this system,
sical measure of complexity is clearly discontinuous: for                     we introduce an observer; an entity that probes this ther-
q 6= 0.5, the two causal states are equiprobable and thus                     malizing qubit cloud at particular values of λ. For this
Cµ = 1 [6]. Yet at q = 0.5, the process becomes com-                          toy model we construct a scheme in which the observer’s
pletely random and thus the future is statistical identical                   measurement device consists of a single probe qubit. This
for all pasts; there is only one causal state and Cµ = 0.                     probe is engineered to interact with qubits within the
An infinitesimal perturbation in q around 0.5 leads to a                      cloud (specifics below), during which the observer mon-
sudden change in statistical complexity.                                      itors the probe at discrete time intervals to retrieve a
   The complexity of the quantum -machine, in contrast,                      sequence of binary outcomes · · · x−2 x−1 x0 x1 · · · . From
remains continuous. As q approaches 0.5, the process be-                      these statistics the observe constructs a stochastic pro-
                                                                                      ←− → −
comes progressively more random; the overlap between                          cess P ( X , X ), which is then used to quantify the com-
the future statistics of the two causal states increase,                      plexity of the environment.
thereby increasing the advantage of storing them in non-                         The specifics of our measurement scheme are outlined
orthogonal states. In the limit q → 0.5, hS0 | S1 i → 1 and                   in Fig. 3. At each time-step t, the observer scatters his
Cq smoothly converges to 0.                                                   probe qubit ρobs with a randomly selected qubit in the
   Thus, what appears in -machines as a striking discon-                     cloud; he then chooses one of the two output qubits with
tinuity in complexity vanishes when these machines are                        probability 0 < g < 1 and measures it in the compu-
quantized. Conceptually, discontinuities in complexity                        tational basis to generate output xt . Repetition of this
appear difficult to explain. Why would an infinitesimal                       process then results in a bit-string whose distribution is
                                                                                                                                     6

                                                                          A.     Statistical Complexity of the Qubit Cloud
ρe (λ)
                                  ..                                      The first step in determining how complexity evolves
                                   .
                                                                       in our thermalizing qubit cloud is to construct its associ-
ρe (λ)                                  •      ×
                                                                       ated -machine. To do this, we need to characterize the
ρe (λ)      •      ×                                                   set of causal states S and associated transition probabil-
                                                                       ities. The first observation we make is that the process
 ρobs              ×                           ×               ···     is Markovian. At each time step the equivalent quantum
           eiX̂κ                       eiX̂κ
                                                                       circuit is initialized in input state: |kihk| ⊗ ρe (λ), where
                                                                       the last measurement outcome xt−1 = k ∈ {0, 1} com-
                pSWAP                       pSWAP
                                                                       pletely determines the observer’s input state |ki. This
                                                                                               →
                                                                                               −
 FIG. 3: Circuit representation of how the observer’s qubit            input determines X , for more detail see the Appendix.
                                                                                                                      →
                                                                                                                      −
 evolves through interactions with the qubit cloud. At each            Hence all information about the future X , is contained
 time step, t, a new ancillary environmental qubit ρe (λ) inter-       in X−1 .
 acts with the observer’s probe ρobs . The interaction is mod-            This Markovian property implies that the process has
 eled by a controlled unitary operation, |0ie h0|e ⊗ 1 + |1ie h1|e ⊗   at most two causal states: S0 = {0, 10, 00, 110, · · · },
 Xκ where ⊗ is the direct product and Xκ = exp (iX̂κ) is               the set of pasts ending with “0”, and S1 =
 a function of the Pauli X operator, X̂, and an interaction            {1, 01, 11, 011, · · · }, the set of pasts ending with “1”. In-
 strength parameter 0 ≤ κ ≤ π2 . For the maximally entangling          deed, provided the process is not completely random
 case κ = π2 this interaction reduces to a controlled NOT gate.        or completely uniform (i.e. 0 < λ < 1), we must
 The pSWAP (probabilistic SWAP) defines a the execution of             record something about the past to predict the future,
 a SWAP gate, Us : |φi|ψi → |ψi|φi with probability g; and                     →
                                                                               −                    →
                                                                                                    −
 models the observer’s uncertainty of which qubit represents           i.e. P ( X |S = S0 ) 6= P ( X |S = S1 ). Thus the two causal
 the probe after interaction. The symmetric case of g = 0.5            states S0 and S1 are distinct.
                                                                                                                          (r)
 corresponds to the case where the observe completely loses               To evaluate the transition probabilities Tjk , we first
 track of which output qubit is which. At the end of the sub-                        (r)
 routine the observer measures his qubit in the Z basis and
                                                                       note that Tjk = δkr Tjk : if the system transits to Sk at
 outputs the answer as xt . He then repeats the exercise with          time t it will always emit xt = k. Thus the thermalizing
                                                                                                            ←
                                                                                                            − → −
 a new ancillary environmental qubit.                                  qubit cloud generates a process P ( X , X ) that is statis-
                                                                       tically identical to the perturbed coin (see Fig. 1) with
                                                                       Tjk described by the transition matrix
                                                 ←− → −                                                      
 governed by an associated stochastic process P ( X , X ).                                      1 − q0   q1
                                                                                          T =                   ,            (11)
 We make two simplifying assumptions about the system.                                            q0   1 − q1
                                                                       where q0 and q1 are λ-dependent. We evaluate these in
    1. The timescale in which these measurements are                   the Appendix A to find
       made is infinitesimal compared to the timescale in                                λ           λ
       which λ evolves.                                                        q0 (λ) = g   + (1 − g) sin2 (κ),                  (12a)
                                                                                          2          2            
                                                                                               λ                 λ
                                                                               q1 (λ) = (1 − g) sin2 (κ) + g 1 −     .           (12b)
    2. The number of qubits in the cloud, N , is sufficiently                                  2                 2
       large that the probe quit never interacts with the              The statistical complexity of the process is then defined
       same qubit twice.                                               by the complexity of this model; i.e., the entropy of the
                                                                       random variable S over causal states. Let pi = P (S = Si )
                                                                       be the probability an -machine is in state Si , then from
 These assumptions ensure that that at each value of λ
                                                                       Eq. (8);
 we will probe the environment many times (collect many
 measurement outcomes) allowing the bit string we gen-                                    q1 (λ)                         q0 (λ)
 erate to be modeled by a stationary stochastic process.                  p0 (λ) =                   ,   p1 (λ) =                   ,
                                                                                     q0 (λ) + q1 (λ)                q0 (λ) + q1 (λ)
 These assumptions apply, for example, in studying sys-                                                                            (13)
 tems on the macroscopic scale.                                        and the statistical complexity is thus
   Under these assumptions it is easy to see that the en-                             X
                         ←− → −                                           Cµ (λ) = −      pi (λ) log2 pi (λ), 0 < λ < 1.          (14)
 tropic properties of P ( X , X ) follow the entropic prop-
                                            ←
                                            − →−                                            i
 erties of the qubit cloud. At λ = 0, P ( X , X ) takes on                                                   ←
                                                                                                             − → −
 unit probability for a sequence of 0’s, and thus has zero             for the special case where λ = 1, P ( X , X ) becomes com-
 entropy. Meanwhile, its entropy is maximal at λ = 1.                  pletely random and there is only a single causal state
 Thus, the toy model provides a first order testing ground             encompassing all possible pasts. Therefore the complex-
 for our proposed measure of complexity.                               ity of the system reduces to 0, i.e., Cµ (1) = 0.
                                                                                                                             7

                                                                  minimal for λ = 0, 1. Eq. (12) implies that when λ = 0,
                                                                  q0 (0) = 0 and q1 (0) > 0; thus the -machine resides
                                                                  in state S0 with unit probability. The process is triv-
                                                                  ial (the output is a uniform string of 0s), resulting in
                                                                  Cµ = Cq = 0. On the other end, q0 = q1 when λ = 1,
                                                                           →
                                                                           −                 →
                                                                                             −
                                                                  thus P ( X |S = S0 ) = P ( X |S = S1 ). This indicates that
                                                                  the two causal states have statistically identical futures;
                                                                  and therefore collapse into a single causal state that en-
                                                                  compasses all pasts. Again Cµ = Cq = 0. Thus, both
                                                                  complexity measures agree with our intuition that a sys-
                                                                  tem at either 0 or maximal entropy process is completely
                                                                  trivial.
                                                                     The behavior of Cq and Cµ , however, diverges for inter-
                                                                  mediate values of λ. Fig. 4 displays the generic behavior
                                                                  of both Cµ and Cq . Cµ is a monotonically increasing
                                                                  function for all λ 6= 1. In fact, λ = 1 is a point of discon-
                                                                  tinuity; where Cµ drops sharply to 0. It indicates that the
                                                                  process is ‘maximally complex’ an infinitesimal distance
FIG. 4: Overview of Cq and Cµ for the thermalizing qubit          away from being completely random. If we put this in the
cloud, as a function of the thermalization parrameter, 0 <        context of a physical system where complete randomness
λ < 1. As λ increases more noise is introduced and the envi-      is an idealized limit, it seems to suggest that complex-
ronmental qubits, ρe (λ), becomes more mixed. (a) Plot of Cµ      ity shares almost identical behavior with entropy. These
vs. λ for various swap probabilities, g = 0.25 (brown, dotted),   results contrast quite sharply with our perceived concep-
g = 0.5 (red, solid) and g = 0.75 (blue, dashed). Qualitatively   tion of complexity, and intuition that complexity should
Cµ is a monotonically increasing function of λ. (b) Plot of Cq
                                                                  be complementary to randomness [9, 11]. The behavior
vs. λ for values of g = 0.25 (black, dotted), g = 0.5 (purple,
solid) and g = 0.75 (orange, dashed). Cq dies down as λ → 1       of Cq , on the other hand, appears in line with what we ex-
and the corresponding stochastic process becomes more ran-        pect. The quantum -machine complexity rises and falls
dom. (c) Plot of g = 0.5 case for both Cµ (brown, dotted)         continuously, taking on a peak value at λ ≈ 0.2. There is
and Cq (red, solid) to illustrate the comparative behaviour.      no sudden jumps, and the complexity of the qubit cloud
                                                                  near complete thermalization is indeed very close to 0.
                                                                     Fig. 4 (c) compares Cq and Cµ directly for the spe-
   B.   Quantum -machines and their Complexity                   cial case where g = 12 and κ = π/2. This corresponds
                                                                  to the limiting scenario where the probe interacts with
  The quantum -machine can be determined by directly             the qubit cloud through the idealized CNOT gate and
quantizing the causal states; resulting in two quantum            the observer measures one of the two outputs at random.
causal states                                                     It is clear that the quantum -machine is able to model
                                                                  the resulting process using far less memory; and this ad-
                              f + √q0 |1i,
                     p
              |S0 i = 1 − q0 |0i       f          (15a)           vantage grows with λ. These results are not isolated to
                     √ f p                                        specific parameter choices. Fig. 5 displays the behavior
              |S1 i = q1 |0i + 1 − q1 |1i.
                                       f          (15b)           of Cq for various values of κ and g. In general, Cq is a
The complexity of the quantum -machine is given by the           continuous function of λ and gradually diminishes as λ
von Neumann entropy of the density operator                       approaches either 0 or 1, while peaking somewhere in the
                                                                  middle.
               ρ = p0 |S0 ihS0 | + p1 |S1 ihS1 |,         (16)       These results can be understood qualitatively. As the
                                                                  process becomes more random there are two contribut-
where pi is the probability of finding the quantum -             ing sources to the complexity. The first is positive: noise
machine in the state |Si i. This probability satisfies Eq.        gives the system the energy to transition from causal
(13).                                                             state S0 to S1 . This applies an equalizing pressure to the
                                                                  population level of two causal states S0 , and S1 . Thus,
                                                                  more memory is require to distinguish the two possibil-
               C.    Complexity Dynamics                          ities. The second a negative contribution. As noise in-
                                                                  creases; the future statistics of S0 and S1 become less
  We now have all the tools necessary to analyze how              distinct, and thus distinguishing between the two is less
complexity evolves within the qubit cloud–both through            meaningful. The evolution of complexity within the sys-
the lens of conventional -machines and their quantum             tem rests on the balance of these two contributions.
mechanical counterpart.                                              The classical statistical complexity, however, accounts
  Firstly, observe that the complexity of the system, re-         only for the former contribution. It is based entirely on
gardless of which measure we use (Cµ or Cq ), is indeed           the entropy of distinguishing causal states S0 and S1 .
                                                                                                                          8


FIG. 5: Evolution of Cq with thermalization parameter λ for various values of interaction strength κ and swap probability g.
In (a), (b), (c), g is varied for various fixed values of κ. In (d), (e), (f), κ is varied for various fixed values of g.


Within our toy model as λ increases p0 → p1 . Thus the          then falling as the system approached total randomness.
statistical complexity undergoes monotonic gain. The               When we envision the dynamics of complexity the lat-
progressive convergence in the conditional future of these      ter quantity seems more reasonable. If we are to estimate
two causal states remains ignored until λ = 1. Cq , on the      the probability distribution of a given stochastic process
other hand, continually accounts for the latter contribu-          ←− → −
                                                                P ( X , X ) through observations, there will always be a
tion. As the conditional futures of S0 and S1 converge,         statistical margin of error. Thus, it is unsatisfactory for
so do the quantum causal states |S0 i and |S1 i. Thus the       a quantity that describes the process complexity to jump
amount of memory required to model the process evolves          to a fixed value (here 1) for an infinitesimal perturbations
continuously reflecting our ideal that complexity rests on      away from total randomness. The continuity in the com-
the balance between order and disorder.                         plexity of quantum -machines is thus a welcome trait.
                                                                   This article only skims the surface of how quantum the-
                                                                ory may combine with computational mechanics. Many
                  IV.    DISCUSSION                             open questions remain. On the one hand, the model that
                                                                we have presented here is but a toy with very specific
   In this article we explored a quantifier of complexity       assumptions on how the qubit cloud was probed. Could
by extending the framework of -machines into the quan-         similar techniques be applied to more complex systems
tum mechanical regime. In computational mechanics the           that have been studied within the framework of compu-
information content of -machines presents a popular ap-        tational mechanics? We note that previous studies of
proach to quantifying the structure of a given stochastic       statistical complexity in the Ising lattice demonstrated
process, the rationale being that they are its simplest         similar behavior [6]. The complexity rose monotonically
models. The advent of quantum -machines, however,              with temperature and only dropped to 0 via a sudden
demonstrated that simpler models do exist. This moti-           discontinuous jump at infinite temperature. Could quan-
vated us to ask “how complex would a stochastic process         tizing -machines remove this discontinuity?
look to a quantum -machine?”                                      On the other hand there is currently no proof that
   Our results demonstrated a marked divergence in the          quantum -machines are the provably simplest quantum
complexity of -machines and their quantum mechanical           models. If this turns out false, would the true mini-
counterparts. In a process at various different stages of       mal amount of memory, CQ required to simulate a given
thermalization λ we found that the statistical complexity       stochastic process share the qualitative features of Cq ?
increased monotonically with λ. Only at infinite temper-        Certainly, using bounding arguments (As 0 ≤ CQ ≤ Cq ;
ature did it drop discontinuously to zero. The quantum          we can see that CQ has to be continuous at the point of
-machine complexity, on the other hand, behaved as a           maximal randomness in the qubit cloud.
smooth function of λ first rising for low values of entropy,       The ultimate goal would be to present an operationally
                                                                                                                             9

meaningful, yet nevertheless computable, quantifier of               Acknowledgements.— The authors acknowledges help-
complexity. This would substantiate our intuition that             ful discussions with Karoline Weisner, Alex Monras
complexity lies at the border between order and chaos -            and Borivoje Dakić. This work is supported in part
and thus pave the path for developing universal laws that          by the National Basic Research Program of China
govern complexity. This article presents one clue in the           Grant 2011CBA00300, 2011CBA00302, the National
big puzzle - our notions of what is complex is affected            Natural Science Foundation of China Grant 61033001,
by what sort of information we use; and quantum infor-             61361136003, the Singapore Ministry of Education and
mation could be a valuable tool in understanding what              the Academic Research Fund Tier 3 MOE2012-T3-1-009
around us is ultimately complex.                                   “Random numbers from quantum processes”.


 [1] A. N. Kolmogorov, Theoretical Computer Science 207,           where US is the standard unitary SWAP operation de-
     387 (1998).                                                   fined by US |φiobs |ψie = |ψiobs |φie , and g parametrises
 [2] J. Ladyman, J. Lambert, and K. Wiesner, European              the probability of swapping.
     Journal for Philosophy of Science 3, 33 (2013).                  The assumption that the bath is extremely large, such
 [3] J. P. Crutchfield and K. Young, Physical Review Letters       that the observer’s qubit never interacts with the same
     63, 105 (1989).
                                                                   environmental qubit twice, implies that the system is ini-
 [4] C. R. Shalizi and J. P. Crutchfield, Journal of statistical
     physics 104, 817 (2001).                                      tialized in a product state ρobs ⊗ρe (λ). At each time step,
 [5] C.-B. Li, H. Yang, and T. Komatsuzaki, Proceedings of         t, the observers qubit is initialized in the quantum state
     the National Academy of Sciences 105, 536 (2008).             corresponding to the last measurement outcome xt−1 ,
 [6] J. P. Crutchfield and D. P. Feldman, [arXiv:9702191]          while the environmental qubit is given by (10).
     (1997).                                                          Explicitly, if the outcome of the last measurement is
 [7] K. Wiesner, M. Gu, E. Rieper, and V. Vedral, Proceed-         xt−1 = k (for k ∈ {0, 1}), then the observer’s qubit is ini-
     ings of the Royal Society A: Mathematical, Physical and       tialized in state |ki and the combined two-qubit system,
     Engineering Science 468, 4058 (2012).                         ρobs,e , is initialized as
 [8] W. G. Rory Cerbus, [arXiv:1403.5356] (2014).
 [9] J. P. Crutchfield, Nature Physics 8, 17 (2012).
                                                                                                                    
                                                                                                                  λ
[10] M. Gu, K. Wiesner, E. Rieper, and V. Vedral, Nature                ρobs ⊗ ρe (λ) = |kihk| ⊗ (1 − λ)|0ih0| + 1         (19)
                                                                                                                  2
     communications 3, 762 (2012).
[11] J. P. Crutchfield, Physica D: Nonlinear Phenomena 75,                                    λ             λ
                                                                                        = (1 − )|k0ihk0| + |k1ihk1|.       (20)
     11 (1994).                                                                               2             2
[12] M. A. Nielsen and I. L. Chuang, Quantum computation
     and quantum information (Cambridge university press,             If xt−1 = 0 then after going through the CXκ interac-
     2010).                                                        tion and the probabilistic SWAP operation we take the
                                                                   partial trace over the environmental qubit to recover the
                                                                   state of observer’s qubit directly before measurement:
                          Appendix                                                                             
                                                                                                      λ    λ
                                                                       ρ0obs = Tre (ρ0e,obs ) =    1−     + cos2 κ |0ih0| +
 A. Evaluation of Perturbation Parameters for the                                                     2    2
                                                                                                
             thermalizing qubit cloud                                      λ             λ
                                                                         g + (1 − g) sin2 κ |1ih1| + i sin κ cos κ(|1ih0| − |0ih1|).
                                                                           2             2
  In this Appendix we give a more in depth treatment of                                                                        (21)
the thermalizing qubit cloud . The circuit representation
of this model can be broken down into two stages: a                Correspondingly, if xt−1 = 1 then
two-qubit interaction between the observer’s qubit and
the environmental qubit, followed by a probabilistic swap              ρ0obs = Tre (ρ0obs ⊗ ρ0e )
defined in the caption of Fig. 3. Formally during the first
                                                                                                             
                                                                                          λ             λ
stage the two-qubit unitary is given by                                      = g 1−           + (1 − g) sin2 κ |0ih0| +
                                                                                          2             2
           CXκ = 1 ⊗ |0ie h0|e + Xκ ⊗ |1ie h1|e ,
                                                                                                            
                                                           (17)                   λ                   λ
                                                                                g + (1 − g) 1 − sin2 κ |1ih1| +
where Xκ = exp (iX̂κ) is defined in terms of the Pauli                            2                   2
X operator, and ⊗ denotes the direct product.                                  (1 − g)i sin κ cos κ(|0ih1| − |1ih0|).   (22)
   The probabilistic SWAP operation acts on the com-
bined system consisting of the environmental qubit and             The terms before |0ih0| and |1ih1| give the probabilities
the observer’s qubit, which we denote by ρobs,e . We de-           of measuring |0i and |1i and hence the statistics of the
fine this transformation through                                   next output. The Markovian nature of the -machine
                                                                   is clearly demonstrated by the fact that the probability
    ρobs,e → ρ0obs,e = gUS ρobs,e U†S + (1 − g)ρobs,e      (18)    xt = 0 (or 1) depends only on the value of xt−1 , the last
                                                                                                                             10

measurement outcome. This establishes the set of causal               quantum causal states are subsequently reduced to
states as S0 = {0, 10, 00, 110, · · · }, the set of pasts ending
with “0”, and S1 = {1, 01, 11, 011, · · · }, the set of pasts
ending with “1”. From these results we can also find the
transition probabilities for the corresponding stochastic
process.                                                                                r            r
                                                                                              λf       λf
                                                                                |S0 i =   1 − |0i +      |1i,              (24)
                                                                                              2        2
    B. The Special Case of Maximally Interacting                                        r
                      Probes                                                                    λ            λf
                                                                                |S1 i =   g(1 − ) + (1 − g) |0i  +
                                                                                                2             2
                                                                                        r
  It is instructive to first outline special case where where                               λ                  λ f
                                                                                          g( ) + (1 − g)(1 − )]|1i.        (25)
κ = π/2. Using the value of κ = π/2 in Eq. (21) and                                         2                  2
(22) we can simplify the transition probabilities to:

                                       λ
 P (St = S0 |St−1 = S0 ) = 1 −           ,                    (23a)
                                       2
                                 λ                                    The resulting state of the quantum -machine is:
 P (St = S1 |St−1 = S0 ) =         ,                          (23b)
                                 2
                                 λ             λ
 P (St = S0 |St−1 = S1 ) = g 1 −     + (1 − g) , (23c)
                                 2             2
                                              
                            λ                λ
 P (St = S1 |St−1 = S1 ) = g + (1 − g) 1 −       . (23d)
                            2                2                                       ρ = p0 |S0 ihS0 | + p1 |S1 ihS1 |.     (26)
                                                                      Substituting q0 = λ2 and q1 = g(1 − λ2 ) + (1 − g) λ2 into
The -machine of the process is presented in Fig. 6. The              Eq. (8) directly yields
                                 λ
                                 2
                                   |r = 1


                  S0   g λ2 + (1 − g)(1 − λ2 ) | r = 1   S1
                                                                                            −2g(λ − 1) + λ
 1 − λ2 | r = 0                                                                        p0 =                 ,             (27a)
                                                                                             2(g + λ − gλ)
                       g(1 − λ2 ) + (1 − g) λ2 | r = 0                                            λ
                                                                                       p1 =               .               (27b)
                                                                                            2(g + λ − gλ)
FIG. 6: Causal state diagram for the thermalizing qubit cloud
with interaction strength set by κ = π2 . The two causal states
are denoted S0 and S1 and an arrow from Sj to Sk repre-
sents the corresponding transition, with label denoting the
                        r
transition probability Tjk and corresponding emission r.
