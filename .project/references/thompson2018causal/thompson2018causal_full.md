# thompson2018causal

**Source:** thompson2018causal
**Author:** Unknown
**Pages:** 14

---

## Full Text

                                                                            Causal Asymmetry in a Quantum World

                                                                     Jayne Thompson,1, ∗ Andrew J. P. Garner,1, 2 John R. Mahoney,3
                                                                       James P. Crutchfield,3 Vlatko Vedral,4, 1, 5 and Mile Gu6, 7, 1, †
                                                    1
                                                      Centre for Quantum Technologies, National University of Singapore, 3 Science Drive 2, 117543, Singapore
                                                                             2
                                                                               Institute for Quantum Optics and Quantum Information,
                                                                    Austrian Academy of Sciences, Boltzmanngasse 3, Vienna, A-1090, Austria
                                                                                3
                                                                                  Complexity Sciences Center and Physics Department,
                                                                       University of California at Davis, One Shields Avenue, Davis, CA 956
                                                                                   4
                                                                                     Atomic and Laser Physics, University of Oxford,
                                                                            Clarendon Laboratory, Oxford, OX1 3PU, United Kingdom
                                                          5
                                                            Department of Physics, National University of Singapore, 3 Science Drive 2, Singapore 117543
                                                  6
                                                    School of Physical and Mathematical Sciences, Nanyang Technological University, Singapore 639673, Singapore
                                                               7
                                                                 Complexity Institute, Nanyang Technological University, Singapore 639673, Singapore
arXiv:1712.02368v2 [quant-ph] 21 Jul 2018


                                                            Causal asymmetry is one of the great surprises in predictive modelling: the memory required to
                                                         predict the future differs from the memory required to retrodict the past. There is a privileged
                                                         temporal direction for modelling a stochastic process where memory costs are minimal. Models
                                                         operating in the other direction incur an unavoidable memory overhead. Here we show that this
                                                         overhead can vanish when quantum models are allowed. Quantum models forced to run in the
                                                         less natural temporal direction not only surpass their optimal classical counterparts, but also any
                                                         classical model running in reverse time. This holds even when the memory overhead is unbounded,
                                                         resulting in quantum models with unbounded memory advantage.


                                               How can we observe an asymmetry in the temporal
                                            order of events when physics at the quantum level is
                                                                                                                             Entropy 𝐶 −
                                            time-symmetric? The source of time’s barbed arrow is a
                                                                                                                                                (b) Retrodiction


                                                                                                                                     C
                                            longstanding puzzle in foundational science [1–4]. Causal


                                                                                                                                      -
                                            asymmetry offers a provocative perspective [5]. It asks
                                            how Occam’s razor – the principle of assuming no more
                                            causes of natural things than are both true and sufficient
                                            to explain their appearances – can privilege one particu-
                                            lar temporal direction over another. That is, if we want
                                            to model a process causally – such that the model makes


                                                                                                                                                                   C+
                                                                                                                                           (a) Prediction
                                            statistically correct future predictions based only on in-
                                                                                                                                                               Entropy 𝐶 +
                                            formation from the past – what is the minimum past
                                            information we must store? Are we forced to store more
                                            data if we model events in one particular temporal order
                                            over the other (see Fig. 1)?                                    FIG. 1. A stochastic process can be modeled in either tem-
                                                                                                            poral order. (a) A causal model takes information available
                                               Consider a cannonball in free fall. To model its future
                                                                                                            in the past x~ and and uses it to make statistically accurate
                                            trajectory, we need only its current position and veloc-        predictions about the process’ conditional future behaviour
                                            ity. This remains true even when we view the process in            ~ X~ = x).
                                                                                                            P (X|        ~ (b) A retrocausal model replicates the system’s
                                            reverse-time. This exemplifies causal symmetry. There           behaviour, as seen by an observer who scans the outputs from
                                            is no difference in the amount of information we must           right to left encountering Xt+1 before Xt . Thus it stores rele-
                                            track for prediction versus retrodiction. However this is       vant future information ~x, in order to generate a statistically
                                            not as obvious for more complex processes. Take a glass                                               ~X
                                                                                                            accurate retrodiction of the past P (X|  ~ =~x). Causal asym-
                                            shattering upon impacting the floor. In one temporal di-        metry implies a non-zero gap between the minimum memory
                                            rection, the future distribution of shards depends only on      required by any causal model C + , and its retrocausal coun-
                                            the glass’s current position, velocity and orientation. In      terpart C − .
                                            the opposite, we may need to track relevant information
                                            regarding each glass shard to infer the glass’s prior tra-
                                            jectory. Does this require more or less information? This       a simulator operating in the ‘less natural’ temporal di-
                                            potential divergence is quantified in the theory of compu-      rection is penalized with potentially unbounded memory
                                            tational mechanics [6]. It is not only generally non-zero,      overhead, and is cited as a candidate source of time’s
                                            but can also be unbounded. This phenomenon implies              barbed arrow [5].
                                                                                                              These studies assumed that all models are imple-
                                                                                                            mented using classical physics. Could the observed causal
                                            ∗ thompson.jayne2@gmail.com
                                                                                                            asymmetry have been a consequence of this classicality
                                            † gumile@ntu.edu.sg
                                                                                                            constraint? Here, we first consider a particular stochastic
                                                                                                                               2

process that is causally asymmetric. We determine the             where past and future are interchanged, such that Y~ =
minimal information needed to model the same process in                               ~ = X−1 X−2 . . . and Yt = X−(t+1) . A
                                                                  . . . X1 X0 , while Y
forward versus reverse time using quantum physics, and            causal model for the time-reversed process then corre-
prove these quantities exactly coincide. More generally,          sponds to a retrocausal model for the forward process
we present systematic methods to model any causally               P (X, ~ X).
                                                                           ~    It generates a statistically accurate retrodic-
asymmetric stochastic process quantum mechanically.               tion of the conditional past P (X|    ~X~ = ~x), using only
Critically, the resulting quantum models not only use             information contained in the future ~x. The statistical
less information than any classical counterpart, but also         complexity of this time-reversed process C − (referred to
any classical model of the time-reversed process. Thus,           as the retrodictive statistical complexity for P) quantifies
quantum models can field a memory advantage, that al-             the minimal amount of causal information we must assign
ways exceeds the memory overhead incurred by causal                                  ~ in order of decreasing t. Causal asym-
                                                                                  ~ X)
                                                                  to model P (X,
asymmetry. Our work indicates this overhead can emerge
                                                                  metry captures the divergence ∆C = |C − − C + |. When
when imposing classical causal explanations. These re-
                                                                  ∆C > 0, a particular temporal direction is privileged,
sult remain true even in cases where causal asymmetry
                                                                  such that modelling the process in the other temporal
becomes unbounded.
                                                                  direction incurs a memory overhead of ∆C.
                                                                      Note that the definitions above are entropic measures,
                                                                  and thus take operational meaning at the i.i.d. limit –
                   I.   BACKGROUND                                i.e. modelling N instances of a stochastic process with
                                                                  statistical complexity C + requires N C + bits of past in-
     Framework – Consider a system that emits an out-             formation, in the limit of large N . While this is the most
 put xt governed by some random variable Xt at each               commonly adopted measure in computational mechan-
 discrete point in time t. This behaviour can be described        ics, single shot variants do exist. The topological state
 by a stochastic process P – a joint probability distri-          complexity D+ , is particularly noteworthy [8]. It cap-
 bution P (X, ~ X)
                 ~ that correlates past behaviour, X~ =           tures the minimum number of dimensions (max entropy)
 . . . X−2 X−1 , with future expectations, X  ~ = X0 X1 . . . .   Ξ must have to generate future statistics. A single-shot
 Each instance of the past x~ = . . . x−2 x−1 exhibits a con-     variant of causal asymmetry can thus be defined by the
 ditional future ~x = x0 x1 . . . with probability P (X  ~ =      difference ∆D = |D− − D+ |, between the topological
                                                                  state complexities of P + and P − . Here, we focus on
~x|X~ = x).~
                                                                  statistical complexity for clarity. However many of our
     Suppose that a model for this system can replicate this      results also hold in this single-shot regime. We return to
 future statistical behaviour using only H bits of past in-       this when relevant.
 formation. Then this model can be executed by encoding
                                                                      Classical models – Prior studies of causal asymme-
 the past x~ into a state s(x)~ ∈ S of a physical system Ξ
                                                                  try assumed all models were classical. In this context,
 of entropy H, such that repeated application of a sys-
                                                                  causal asymmetry can be explicitly demonstrated using
 tematic action M on Ξ sequentially generates x0 ,x1 . . .
                                             ~ X~ = x).           ε-machines, the provably optimal classical causal mod-
 governed by the conditional future P (X|             ~ The       els [8, 9]. This involves dividing the set of pasts into
 model is causal if at each instance of time, all the infor-      equivalences classes, such that two pasts, x~ and x~0 lie in
 mation Ξ contains about the future can be obtained from          the same class if-and-only-if they have coinciding future
 the past [7]. Implementing it on a computer then gives us                              ~ X~ = x)          ~ X~ = x~0 ). Instead
                                                                  behaviour, i.e., P (X|         ~ = P (X|
 a statistically faithful simulation of the process’ realiza-
                                                        ~ X),
                                                          ~       of recording the entire past, an ε-machine records only
 tions. The simplest causal model for a process P (X,             which equivalence class x~ lies within – inducing an en-
 is the model that minimizes H.
                                                                  coding function ε : X~ → S from the space of pasts X~
     The statistical complexity C + is defined as the entropy     onto the space of equivalence classes S = {si }, known as
 H of this simplest model – it is the minimal amount              causal states. At each time-step, the machine operates
 of past information needed to make statistically correct         according to a collection of transition probabilities Tijx :
 future predictions [8, 9]. This measure is used to quan-         the probability an ε-machine initially in si , will transi-
 tify structure in diverse settings [10–12], including hidden     tion to sj while emitting output x. The classical statis-
 variable models emulating quantum contextuality [13].            tical complexity thus coincides with the amount of infor-
 C + also fields thermodynamic significance, having been          mation needed to store the current causal state
 linked to the minimal heat dissipation in stochastic sim-
 ulation and the minimal structure a device needs to
                                                                                               X
                                                                                       Cµ+ = −     πi log πi ,                (1)
 fully extract free energy from non-equilibrium environ-                                        i
 ments [14–17].
     Causal asymmetry captures the discrepancy in statis-         where πi is the probability the past lies within si . ε-
 tical complexity when a process is viewed in forward ver-        machines are also optimal with respect to the max en-
 sus reverse time [18]. Consider an observer that encoun-         tropy [19], such that the topological state complexity Dµ
 ters Xt+1 before Xt . Their observations are characterized       of a process is the logarithm of the number of causal
 by the time-reversed stochastic process P − = P − (Y~, Y  ~)     states [8]. Despite their provable optimality, ε-machines
                                                                                                                                      3

               (a) 𝑃ℎ+ 𝑋,
                       ശ 𝑋Ԧ                                                  (b) 𝑃ℎ− 𝑌, 𝑌
                                    1|p                                                                  𝑠2−
                                                                                            1|1                      2|p
                                                                                                    2 | pq
                                          𝑠1+                time reversal
               0 |1- p        𝑠0+                  1|1-q
                                                                              1|1-q           𝑠1−                  𝑠0−     0 |1- p


                                    2|q                                                               0 | q(1-p)


                                                ~ X),
FIG. 2. (a) The ε-machine for the process Ph+ (X, ~ created by a flipping a biased coin and emitting outcome 2 when H → T ,
0 when T → T , and 1 when T /H → H. This process has two causal states s+                 +
                                                                                  1 and s0 , where the latter includes all pasts
                                                         − ~ ~
ending in either 0 or 2. (b) The time-reversed process P (Y , Y ). Here pasts ending in 0, 1 and 2 now all lead to qualitatively
different future behaviour and must be stored in distinct causal states s−    −      −
                                                                         0 , s1 and s2 respectively which occur with respective
               −                      −     +                    −
probabilities π0 = (q − pq)/(p + q), π1 = π1 = p/(p + q) and π2 = pq/(p + q).


still appear to waste memory. The amount of past infor-             This immediately establishes a difference in the number
mation they demand typically exceeds the amount the                 of distinct configurations needed for causal versus retro-
past contains about the future – the mutual information             causal modelling. Indeed, Ph+ fields causal asymmetry
E = I(X,   ~ X).
             ~      Observing an ε-machine’s entire future
is insufficient for deducing its initial state. Some of the                     ∆Cµ = Cµ− − Cµ+ = (1 − π1− )h(γ),                    (2)
information it stores in the present is never reflected in
future statistics and is thus effectively erased during op-         where γ = π2− /(1 − π1− ) and πj− = Ph− (y~ ∈ s−    j ). To
eration. In general, this waste differs between prediction          understand this asymmetry, note that when modelling
and retrodiction, inducing non-zero causal asymmetry.               Ph+ , we need only know if the previous output was 1
    Examples – We illustrate this by examples, starting             (i.e., current state of the coin) to decide whether a 0
with the perturbed coin. Consider a box containing a sin-           should be replaced by a 2. To model Ph− however, one
gle biased coin. At each time-step, the box is perturbed,           cannot simply look into the ‘future’ to see if the system
causing the coin to flip with probability p if it is in heads       will output 1 next. Causal asymmetry thus captures the
(0), and q if it is in tails (1). The coin’s state is then          overhead required to accommodate this restriction.
emitted as output. This describes a stochastic process                 In general, causal asymmetry can be unbounded. In
P0+ . As only the last output is necessary for generat-             Appendix D, we describe the class of n-m flower pro-
ing correct future statistics, P0+ has two causal states,           cesses, where Cµ+ scales as O(log n) while Cµ− scales as
corresponding to the states of the coin. The statistical            O(log m). n and m can be adjusted independently, al-
complexity h(π1+ ) thus represents the entropy of the bi-           lowing construction of processes where ∆Cµ > K for any
                             p
ased coin, where π1+ = p+q       is the probability the coin is     given constant K. Setting m = 2 for example, can yield
in heads and h(x) = −x log x − (1 − x) log(1 − x) is the            a process where Cµ+ can be made arbitrarily high, while
binary entropy. Furthermore P0+ is clearly symmetric                Cµ− ≤ log 3. When this occurs, the memory overhead
under time reversal (i.e., P0+ = P0− ), and thus trivially          incurred for modelling the process in the ‘less natural’
causally symmetric.                                                 direction scales towards infinity.
    Suppose we post-process the output of the perturbed                Quantum Models – A quantum causal model is de-
coin, replacing the first 0 of each consecutive substring           scribed formally by an ordered tuple Q = (f, Ω, M)
of 0s with a 2 (For example, . . . 1000110100 . . . becomes         where Ω is a set of quantum states; f : X~ → Ω de-
. . . 1200112120 . . .). This results in a new stochastic pro-      fines how each past x,                             ~ = |sx~i
                                                                                          ~ is encoded into a state f (x)
cess, Ph+ (X,~ X),
                ~ called the heralding coin P + , which             of a physical system Ξ; and M is a quantum measure-
                                                      h
also has two causal states, s+       1 = {x|x~ −1 = 1} and          ment process. To model P (X,   ~ X),
                                                                                                      ~ repeated applications
s+        ~ −1 6= 1}. In fact, one can model Ph+ (X,      ~ X)
                                                            ~       of M on Ξ must generate correct conditional future be-
  0 = {x|x
by perturbing the same biased coin in a box, and modi-              haviour. That is, application of M on a system Ξ in
fying it to output 2 – instead of 0 – when it transitions           state |sx~i must (i) generate an output x with proba-
from heads to tails (see Fig. 2). Thus the heralding coin           bility P (X0 = x|X~ = x)    ~ and (ii) transition Ξ into a
also has classical statistical complexity Cµ+ = h(π1+ ).            new state f (x~0 ) = |sx~0 i where x~0 = xx,
                                                                                                              ~ such that L-
    Its retrodictive statistical complexity, however, is            repeated applications of M will generate x0 , . . . , xL−1
higher. The time-reversed process Ph− (Y~, Y     ~ ) represents     with correct probability P (X0:L |X~ = x)~ for any desired
an alternative post-processing of the perturbed coin - re-          L ∈ Z+ [20]. The entropy of a model Q is given by
placing the last 0 in each consecutive substring of 0s with         the von Neumann entropy S(ρ) = −Tr(ρ log ρ), where
                                                                             P (X~ = x)|s
                                                                          P
a 2. Now, 0 can be followed by 0 or 2, while 1 can be               ρ=                ~ x~ihsx~|. Thus the quantum statistical
followed by anything, and 2 can only be followed by 1, in-          complexity Cq+ of a process can be computed by mini-
ducing three causal states s−   j = {y|y
                                       ~ −1 = j} (see Fig. 2).      mizing S(ρ) over all valid models [21].
                                                                                                                                4

                                                                                          II.   RESULTS
            ശ 𝑋Ԧ
    (a) 𝑃ℎ+ 𝑋,
       |𝑠𝑖+ ൿ               𝑉𝑝        𝑉𝑞                                We study this question via two complementary ap-
                                                                     proaches. The first is a case study of the heralding coin
                                                                     - the aforementioned process that exhibits causal asym-
        |0ۧ                                                          metry. We pioneer methods to establish its provably op-
                                                  |0ۧ
                                                                     timal quantum causal and retrocausal models, and thus
                                                                     produce a precise picture of how quantum mechanics mit-
     (b) 𝑃ℎ− 𝑌, 𝑌                                                    igates all present causal asymmetry. The second stud-
                                                                     ies quantum modelling of arbitrary processes with causal
        |𝑠𝑖− ൿ                   𝑈𝑞        𝑋                         asymmetry. Here, Cq+ and Cq− cannot be directly evalu-
                           𝑈𝑝                                        ated, but can nevertheless be bounded. In doing so, we
                                                                     show that when forced to model such process in the less
                                                                     natural direction, the quantum advantage always exceeds
                                                    |00ۧ
                                                                     the memory overhead ∆Cµ .
            |00ۧ
                                                                        The Heralding Coin – Let Ph+ denote the heralding
                                                                     coin process. Here we first state the optimal quantum
FIG. 3. Quantum circuits for generating (a) Ph+ (X,      ~ X)
                                                           ~ and     models of Ph+ and Ph− . We then outline how their opti-
(b) Ph− (Y~, Y
             ~ ). Here CU (black circle and line) is the stan-       mality is established, leaving details of the formal proof
dard control gate CU : |wi|ψi → |wiU (w mod 2) |ψi. Mean-            to Appendix B. The optimal causal model Q+ has two
while C̄U (white circle, black line) is defined as C̄U |wi|ψi =      internal states;
|0iU (w+1 mod 2) |ψi. (a) To simulate Ph+ (X,      ~ we initialize
                                                ~ X)                                        p            √
                                                                                     |s+
                                                                                       0i=     1 − p|0i + p|1i,
a qubit in state |s+  i i and an  ancilla   in state |0i. Execut-                           √        p
ing the local unitary Vp |0i → |s+   0 i, followed  by the 2-qubit                   |s+
                                                                                       1i=    q|2i + 1 − q|1i,              (3)
gate CVq , where Vq Vp |0i = |s+1 i, creates a suitable entangled
state – such that a computation basis measurement of the top         with associated encoding function +      ~ = |s+
                                                                                                           q (x)      i i if-and-
                                                                                   +
qubit yields xt , and simultaneously collapses the bottom qubit      only-if x~ ∈ si . Given a qubit in state +  q (x),
                                                                                                                      ~   Fig. 3
into the causal state for the next time step. (b) To simulate        establishes the sequential proccedure that replicates ex-
Ph− (Y~, Y
         ~ ) we prepare state |s− i|0i|0i as input. Execution of
                      √         i √                                                                               ~ X~ = x).
                                                                     pected future behaviour, i.e., samples Ph+ (X|         ~
C̄Up where Up |0i = 1 − p|0i√+ p|1i, followed by CUq where             Meanwhile the optimal quantum retrocausal model Q−
                        √
Uq satisfies Uq |0i = q|0i + 1 − q|1i, and finally CX where
                                                                     has encoding function −   ~ = |s−
                                                                                            q (y)
                                                                                                                               −
                                                                                                      i i if-and-only-if y~ ∈ si ,
X is the Pauli X operator generates a suitable entangled state
– such that measuring the first two qubits yields yt (provided
                                                                     where
we identify measurement outcome 00 → yt = 0, 10 → yt = 1                             |s−
                                                                                       0 i = |0i,
and 01 → yt = 2), and collapses the remaining qubit into the                                 √
                                                                                     |s−
                                                                                                     p
quantum causal state for the next time step. In either circuit,                        1i=     q|0i + 1 − q|1i,
retaining only the state of Ξ (green circle) at each time-step                       |s−
                                                                                       2 i = |1i.                             (4)
is sufficient for generating statistically correct predictions or
retrodictions.                                                       The associated procedure for sequential generation of ~y
                                                                     as governed by Ph− (Y  ~ |Y~ = y)
                                                                                                    ~ is outlined in Fig. 3.
                                                                        To establish optimality, we first invoke the causal state
                                                                     correspondence: for any stochastic process with causal
                                                                     states {si } that occur with probability πi , there exists
                                                                     an optimal model Q = (q , Ω, M), where the elements
   This optimization is highly non-trivial. There exists             of Ω are in 1-1 correspondence with {si } (see Lemma 1
no systematic techniques for constructing optimal quan-              of Appendix A). Since the heralding coin process has
tum models, or proving the optimality of a given candi-              two forward causal states, we can restrict our computa-
date model. To date, Cq+ , has only been evaluated for               tion of Cq+ to quantum models where Ω = {|ψ0+ i, |ψ1+ i}.
the Ising chain [20]. This process, however, is symmet-              Moreover we can show that    p the data processing inequal-
ric under time reversal, implying that ∆Cµ is trivially              ity implies |hψ0+ |ψ1+ i| ≤ p(1 − q) ≡ F (see Lemma 2
zero. Nevertheless recent advances show multiple set-                of Appendix A). The monotonicity between |hψ0+ |ψ1+ i|
tings where quantum models outperform optimal classi-                and the entropy of the resulting model, together with
cal counterparts [22–26]. In fact, for every stochastic pro-         observation that |hs+      +
                                                                                           0 |s1 i| = F , then implies optimality
                                                                          +
cess where the optimal classical models are wasteful (i.e.,          of Q (see Theorem 1 P      of Appendix B). This establishes
Cµ+ > E), it is always possible to design a simpler quan-            Cq+ = S(ρ+ ) for ρ+ = i πi+ |s+        +
                                                                                                       i ihsi |.
                                                                                                       −
tum model [22]. Indeed, sometimes the quantum mem-                      Proving the optimality of Q is more involved. First
ory advantage Cµ+ − Cq+ can be unbounded [27]. Could                 note the causal state correspondence allows us to con-
quantum models mitigate the memory overhead induced                  sider only candidate models Q = (f, Ω, M) where Ω =
by causal asymmetry?                                                 {|ψk− i}k=0...2 has three elements. The data processing
                                                                                                                                           5

  (a)                            (b)                   (c)                        (d)                                (e)


                                               1.4                                             0.6
                                                                                                           0.4
         0.5                                                                                                                         1.5


                                 q


                                                       q


                                                                                 q
 q


                                                                                                                 q
                           0.2                                       0.9                                                   0.9
                                                   1
                                                                       0.7                               0.2
                                              0.5                                                                          0.7

               p                        p                        p                                   p                     p
                                                                                                                                     1.0
  (f )                           (g)                   (h)                         (i)                               (j)


                     0.9                                                                 0.1
                                                             0.1
                                       0.7
                                                                                               0.4                                   0.5
                                                             0.2
 q


                                 q


                                                       q


                                                                                 q


                                                                                                                 q
                     0.7
                                                                       0.4                                 0.6             0.3
               0.5
                                             0.5                                                                               0.2

               p                        p                        p                                   p                     p


FIG. 4. Complexity of the heralding coin plotted against p and q. The figure illustrates E ≤ Cq+ = Cq− ≤ Cµ+ ≤ Cµ− across all
values of the parameter space (0 ≤ p, q ≤ 1). (d) depicts the classical causal asymmetry ∆Cµ , and (f) effectively demonstrates
Cq+ = Cq− and thus ∆Cq = 0.


inequality can then be used to establish the fidelity con-                 see Fig 4 f and g), they each still store some unnecessary
straints |hψj− |ψk− i| ≤ |hs−   |s− i| (see Lemma 2 of Ap-                 information (Cq+ , Cq− > E, see Fig. 4 i).
                        P −j −k −
pendix A). Let σ =         πk |ψk ihψk | with eigenvalues λk ,                Our results persist when considering minimal dimen-
and ρ− = πk− |s−
           P
                       ihs−                     −                          sions, rather than minimal entropy required for causal
                     k    k | with eigenvalues λk . In Lemma
4 of Appendix B, we prove that for all choices of |ψk− i sat-              modelling. Ph+ requires only two causal states, and thus
                                                                           can be modeled using a 2-level system (Dµ+ = log 2).
isfying the fidelity constraint λ−  k majorizes λk . Thus ρ
                                                            −

has minimal entropy among all valid retrocausal quan-                      Ph− , however, has three causal states. Modelling it thus
tum models.                                                                requires a 3-level system (Dµ− = log 3). In contrast,
   Q+ and Q− exhibit different encoding functions (one                     the three quantum causal states of Ph− can be embed-
maps onto two code words, the other onto three), and                       ded within a single qubit, and thus the dynamics of the
invoke seemingly unrelated quantum circuits for gener-                     heralding coin can be modelled using a single qubit in
ating future statistics (see Fig. 3). Nevertheless direct                  either temporal direction. Therefore this vanishing of
computation yields                                                         causal asymmetry also applies in single shot settings.
                                                                              General Processes – We now study quantum mit-
                                         √ 
                                                                           igation of causal asymmetry for general stochastic pro-
                                  
                   +       −         1+ c
                 Cq = Cq = h                  ,           (5)              cesses by bounding Cq+ and Cq− from above. Let Cµmin =
                                        2
                                                                           min(Cµ+ , Cµ− ) represent the minimum amount of infor-
where c = (p2 (1 + 4(1 − q)q) − 2pq + q 2 )/(p + q)2 and h(·)              mation we need to classically model P (X,   ~ X)
                                                                                                                          ~ when al-
is the binary entropy. Thus ∆Cq = 0 for all values of p                    lowed to optimize over temporal direction. Meanwhile let
and q. This establishes our first result:                                  Cqmax = max(Cq+ , Cq− ) be the minimal memory a quan-
                                                                           tum system needs when forced to model the process in
Result 1. There exists stochastic processes that are                       the least favourable temporal direction. In Appendix C,
causally asymmetric (Cµ+ 6= Cµ− ), but exhibit no such                     we establish the following:
asymmetry when modelled quantum mechanically (Cq+ =
                                                                           Result 2. For any stochastic process P,
Cq− ).
                                                                                           max(Cq+ , Cq− ) ≤ min(Cµ+ , Cµ− )         (6)
   This vanishing of causal asymmetry at the quantum
level is not simply the result of saturating the bound                     Equality occurs only if Cµ+ = Cµ− = E, such that P          is
given by E. Fig. 4 shows that E < Cq+ = Cq− < Cµ+ <                        causally symmetric.
Cµ− for almost all values of p and q. While both quantum                     Consider any causally asymmetric process P, such that
causal and retrocausal models reduce memory resources                      modelling it in the less favourable temporal direction in-
beyond classical limits (i.e., Cq+ < Cµ+ and Cq− < Cµ− ,                   curs memory overhead ∆Cµ . Result 2 implies that this
                                                                                                                          6

overhead can be entirely mitigated by quantum models.          density matrix ρ(t) [30–32]. E(t) propagates backwards
There exists a quantum model that is not only provably         through time, representing how our expectations of the
simpler than its optimal classical counterpart, but is also    past change as we scan future measurement outcomes in
simpler than any classical model of the time-reversed pro-     time-reversed order. The original motivation was that
cess P − . In Lemma 7 (see Appendix C), we show that           ρ(t) and E(t) combined yield a more accurate estimate
such models can be systematically constructed, and align       of the measurement statistics at time t than ρ(t) alone,
with the simplest currently known quantum models –             allowing improved smoothing procedures [33–36].
q-machines [28, 29]. As a corollary, causal asymmetry             While this framework and causal asymmetry differ in
guarantees both Cq+ < Cµ+ and Cq− < Cµ− , i.e., non-           motivation and details (e.g. monitoring is done in con-
zero quantum advantage exists when modelling in either         tinuous time, whereas we have so far only considered dis-
causal direction.                                              crete time), there are also notable coinciding concepts.
  A variant of these results also applies to topological       The standard propagation equation for ρ(t) parallels a
state complexity. Suppose the number of causal states          causal model for observed measurement statistics, while
for P and its time-reversal P − differ, such that Dµ+ 6=       its time-reversed counterpart governing E(t) parallels a
Dµ− . Let Dq+ and Dq− respectively be the logarithm of the     corresponding retrocausal model. It would certainly be
minimal dimensions needed to model P and P − quantum           interesting to see if such systems exhibit either classical
mechanically. Appendix C also establishes that                 or quantum causal asymmetry. For example, does the re-
                                                               source cost of tracking E(t) differ from that of ρ(t) under
Result 3. For any stochastic process P,                        some appropriate measure [37]?
                                                                  Answering these questions will likely involve significant
             max(Dq+ , Dq− ) ≤ min(Dµ+ , Dµ− ).         (7)    extensions of current results. Our framework presently
                                                               assumes the process evolves autonomously, and that time
   Given there exists stochastic processes where predic-
                                                               is divided into discrete steps. These restrictions will need
tive and retrodictive topological complexity differ (e.g.
                                                               to be lifted, by combining present results with recent gen-
the heralding coin). This immediately implies the fol-
                                                               eralizations of classical and quantum computational me-
lowing corollary:
                                                               chanics to continuum time [38, 39] and input-dependent
Result 4. The quantum topological complexity Dq can be         regimes [16, 40, 41]. More generally, such developments
strictly less than the classical topological complexity Dµ .   will enable a formal study of causal asymmetry in the
                                                               quantum trajectories formulation of open quantum sys-
   This solves an open question in quantum modelling -         tems.
whether quantum mechanics allows for models that simu-            Arrow of Time in Quantum Measurement –
late stochastic processes using not only reduced memory,       Related to such open systems are recent proposals for
but also reduced dimensions.                                   inferring an arrow of time from continuous measure-
   These results have particular impact when ∆Cµ is ex-        ment [42]. These proposals consider continuously mon-
ceedingly large. Recall that in the case of the n-2 flower     itoring a quantum system initialized in state ρi , result-
process, Cµmin ≤ log 3 while Cµ+ scales as O(log n). Our       ing in a measurement record r(t) with some probability
theorem then implies that Cq± ≤ Cµmin ≤ log 3. Thus we         P [r(t)|ρi ]. Concurrently, the state of the system evolves
immediately identify a class of processes whose optimal        through a quantum trajectory ρ(t), into some final con-
classical models require a memory that scales as O(log n),     figuration ρ(T ) = ρf . The goal is to identify an alter-
and yet can be modelled quantum mechanically using a           native sequence of measurements, such that for at least
single qutrit.                                                 one possible outcome record r0 (t) occurring with non-zero
                                                               probability P [r0 (t)|ρf ], the trajectory rewinds. That is,
                                                               a system initially in state ρf will evolve into ρi , passing
            III.   FUTURE DIRECTIONS                           through all intermediary states in time-reversed order.
                                                               An arrow of time emerges as P [r(t)|ρi ] and P [r0 (t)|ρf ]
  There are a number of potential relations between            generally differ, such that one of the two directions oc-
causal asymmetry and innovations on the arrow of time,         curs with greater probability. An argument via Bayes’
and retrodictive quantum theory. In this section, we sur-      theorem then assigns different probabilistic likelihoods
vey some of these connections, and highlight promising         towards whether ρ(t) occurred in forward or reverse time.
future research directions.                                       This framework provides a complementary perspective
  Retrodictive Quantum Mechanics – Consider the                to our results. It aims to reverse the trajectory of the sys-
evolution of an open quantum system that is moni-              tem’s internal state ρ(t), placing no constraints on the re-
tored continuously in time. Standard quantum trajec-           lation between the measurement statistics governing r(t)
tory theory describes how the system’s internal state          and r0 (t). In contrast, causal asymmetry deals with re-
ρ(t) evolves, encapsulating how our expectations of fu-        versing the observed measurement statistics (as described
ture measurement outcomes update based on past ob-             by some stochastic process P), while placing no restric-
servations. Retrodictive quantum mechanics introduces          tions on the internal dynamics of the causal and retro-
the effect matrix E(t) – a time-reversed analogue of the       causal models (the two models may even field different
                                                                                                                        7

Hilbert space dimensions, such as in the heralding coin        the contexts of prediction and pattern manipulation [14–
example).                                                      17, 44]. For instance, the minimum heat one must dis-
   We also observe some striking parallels. Both works         sipate to generate future predictions based on only past
                                                                                             +
start out with some sequential data, but no knowledge          observations is given by Wdiss   = kB T (Cµ+ − E), where
about whether the sequence occurred in forward or re-          kB is Boltzmann’s constant, T is the environmental tem-
verse time. Both ask the following question: Is there          perature, and the excess entropy E is symmetric with re-
some sort of asymmetry singling out one temporal di-           spect to time-reversal. Therefore, non-zero causal asym-
rection over the other? In the emerging arrow of time          metry implies that flipping the temporal order in which
from quantum measurement, we are given a trajectory            we ascribie predictions incurs an energetic overhead of
ρ(t), and asymmetry arises from the difficulty (in terms       ∆Wdiss = kB T ∆Cµ . In processes where ∆Cµ scales
of success probability) of realizing this trajectory in for-   without bound, this cost may become prohibitive. Could
ward versus reverse time. Meanwhile, in causal asym-           our observation that ∆Cq ≤ Cµmin imply such energetic
metry, we are given the observed measurement statistics,       penalties become strongly mitigated when quantum sim-
and an arrow of time arises from the difference in re-         ulators are taken into account?
source costs needed to realize these statistics causally in       A second direction is to isolate what properties of
forward versus reverse time. It would then be interesting      quantum processing enable it to mitigate causal asymme-
to see if a similar argument via Bayes’ theorem can be         try. In Appendix C, we establish that all deterministic
adapted to causal asymmetry. Supposing more complex            processes are causally symmetric, such that Cµ± = Cq± =
machines are less likely to exist in nature (e.g. due to di-   E (see Lemma 6 of Appendix C). Randomness is there-
mensional or entropic constraints), could we then argue        fore essential for causal asymmetry. Observe also that the
whether a given stochastic process is more likely to occur     provably optimal quantum causal and retrocausal mod-
in one causal direction versus the other?                      els for the heralding coin both operated unitarily – such
                                                               that their dynamics are entirely deterministic (modulo
                                                               measurement of outputs). Indeed, such unitary quantum
                  IV.    DISCUSSION                            models can always be constructed [29], and we conjecture
                                                               that this unitarity implies causal symmetry. However,
   Causal asymmetry captures the memory overhead in-           it remains an open question as to whether the optimal
curred when modelling a stochastic process in one tem-         quantum model is always unitary.
poral order versus the other. This induces a privileged           Insights here will ultimately help answer the big out-
temporal direction when one seeks the simplest causal          standing question of whether the quantum statistical
explanation. Here we demonstrate a process where this          complexity ever displays asymmetry under time-reversal.
overhead is non-zero when using classical models, and          Identifying any process for which such asymmetry per-
yet vanishes when quantum models are allowed. For ar-          sists implies that Occam’s preference for minimal cause
bitrary processes exhibiting causal asymmetry, we prove        can privilege a temporal direction in a fully quantum
that quantum models forced to operate in a given tempo-        world. Proof that no such process exists would be equally
ral order always require less memory than classical coun-      exciting, indicating that causal asymmetry is a conse-
terparts, even when the latter are permitted to operate        quence of enforcing all causal explanations to be classical
in either temporal direction. The former result repre-         in a fundamentally quantum world.
sents a concrete case where causal asymmetry vanishes             Acknowledgements – The authors appreciated the
in the quantum regime. The latter implies that the more        feedback and input received from: Yang Chengran, Suen
causally asymmetric a process, the greater the resource        Whei Yeap, Liu Qing, Alec Boyd, Varun Narasimhachar,
advantage of modelling it quantum mechanically.                Felix Binder, Thomas Elliott, Howard Wiseman, Geoff
   Our results also hold when memory is quantified by          Pryde, Nora Tischler, Farzad Ghafari and Chiara Mar-
max entropy. They thus establish that quantum mechan-          letto. This work was supported by, the National Re-
ics can reduce the dimensionality needed to simulate a         search Foundation of Singapore and in particular NRF
process beyond classical limits. Indeed our results isolate    Awards NRF-NRFF2016-02, NRF-CRP14-2014-02 and
families of processes whose statistical complexity grows       RF2017-NRF- ANR004 VanQuTe, the John Templeton
without bound, but can nevertheless be modelled exactly        Foundation grants 52095 and 54914, Foundational Ques-
by a quantum system of bounded dimension. These fea-           tions Institute grant FQXi-RFP-1609 and Physics of the
tures make such processes ideal for demonstrating the          Observer grant No. FQXi-RFP-1614, the Oxford Mar-
practical benefits of quantum models – allowing us to          tin School, the Singapore Ministration of Education Tier
verify arbitrarily large quantum advantage in single-shot      1 RG190/17 and the U. S. Army Research Laboratory
regimes [19, 43], and avoiding the need to measure von         and the U. S. Army Research Office under contracts
Neumann entropy as in current state of the art experi-         No. W911NF-13-1-0390, No. W911NF-13-1-0340, and
ments [24].                                                    No. W911NF-18-1-0028. Much of the collaborative was
   One compelling open question is the potential thermo-       also made possible by the ‘Interdisciplinary Frontiers of
dynamic consequences of causal asymmetry. In computa-          Quantum and Complexity Science’ workshop held in Jan-
tional mechanics, Cµ+ has thermodynamical relevance in         uary 2017 in Singapore, funded by the John Templeton
                                                                                                                                    8

Foundation, the Centre for Quantum Technologies and                  Ω = {|ψi i} are in one-to-one correspondence with the
the Lee foundation of Singapore.                                     classical causal states. In addition, it can be shown that
                                                                     Ω must satisfy the following constraint:
                                                                     Lemma 2 (Maximum fidelity constraint). Let P (X,           ~ X)
                                                                                                                                   ~
           Appendix A: Technical Definitions
                                                                     be a stochastic process with causal states {si }, and Q =
                                                                     (f, Ω, M) be a valid quantum model satisfying f (x)         ~ =
  We first introduce further technical notation and back-            |ψi i iff x~ ∈ si . Then |hψi |ψj i| ≤ Fij , where Fij =
ground that will be used for subsequent proofs.                      P                    1
                                                                        x [Pi (~
                                                                        ~      x)Pj (~x)] 2 is the fidelity between the future morphs
 Definition 1 (Quantum Causal Model). Consider an                    of si and sj .
 ordered tuple Q = (f, Ω, M) where Ω is a set of quantum                These definitions assume that all elements of Ω are
 states; f : X~ → Ω is an encoding function that maps each           pure. This is because computational mechanics consid-
                   ~ = |sx~i of a physical system Ξ; and M
x~ onto a state f (x)                                                ers only causal models – models whose internal states do
 is a quantum process. Q is a quantum model for P (X,        ~ X)
                                                               ~     not store more information about the future than what
                                 ~
 if-and-only-if for any x~ ∈ X , whenever Ξ is prepared              is available from the past. Specifically, let R be a ran-
        ~ subsequent application of M: (i) generates an
 in f (x)                                                            dom variable governing the state of a model at t = 0.
 output x with probability P (X0 = x|X~ = x)         ~ and (ii)            ~ X)
                                                                     I(R, X|  ~ is then known as the oracular information,
 transitions Ξ into a new state f (x~0 ) = |sx~0 i where x~0 = xx
                                                               ~     and represents the amount of extra information R con-
 [20].                                                                                      ~ that is not contained in the past
                                                                     tains about the future X
                                                                      ~                          ~ X)
                                                                     X. For causal models, I(R, X|   ~ = 0 [45]. In Appendix
   Condition (i) guarantees that if a quantum model is               E, we show that this allows us to assume all elements of
initialized in state f (x)
                         ~ then the model’s future output            Ω are pure without loss of generality.
X0 = x will be statistically indistinguishable from the
output of the process itself. (ii) ensures the internal
memory of the quantum model updates to record the                               Appendix B: Proofs of Optimality
event X0 = x, allowing the model to stay synchronized
with the sequence of outputs it has generated thus far.                Here, we formally prove that the quantum models for
Thus a series of L repeated applications of M acting on              the heralding coin given in Eq. (3) and Eq. (4) are
Ξ, generates output x0:L = x0 . . . xL−1 with probability            optimal.
P (X0:L = x0:L |X~ = x),
                       ~ and simultaneously transitions Ξ
                   ~ 0:L ). In the limit L → ∞, the model
into the state f (xx
produces a sequence of outputs ~x = x0 x1 . . . with prob-                    1.   Optimality of the Causal Model.
            ~ X~ = x).
ability P (X|       ~
   The entropy of a quantum model Q is given by                        Let Ph+ denote the heralding coin process, with corre-
                                                                     sponding ε-machine depicted in Fig. 2(a).
               Cq (Q) = S (ρ) = − Tr (ρ log ρ),            (A1)
                                                   P                 Theorem 1. Consider Q+ = (ε+                +   +
                                                                                                            q , Ω , M ), where
where S(·) is the von Neumann entropy, ρ =                            +        +                        +
                                                     x~ πx~ρx~ for       ~ = |si i if-and-only-if x~ ∈ si , with
                                                                     εq (x)
ρx~ = |sx~ihsx~|, and πx~ = P (X~ = x).
                                    ~                                                      p               √
                                                                                     |s+
                                                                                       0i=    1 − p|0i + p|1i,
Definition 2. Q is an optimal quantum model for a                                          √          p
                                                                                     |s+
                                                                                       1i=   q|2i + 1 − q|1i,             (B1)
           ~ X),
process P (X, ~ if given any other model Q0 , we have
     0
Cq (Q ) ≥ Cq (Q).                                                    Ω+ = {|s+         +
                                                                                0 i, |s1 i}, and M
                                                                                                   +
                                                                                                     described by the quantum
                                                                                                +
                                                                     circuit in Fig. 3(a). Q is an optimal quantum model
   Consider a stationary stochastic process P (X,~ X),
                                                   ~ such            for Ph+ .
that P (X0:L ) = P (Xt:t+L ) for any L ∈ Z+ , t ∈ Z. Let
                                                                     Proof. We prove this by contradiction. Assume there ex-
    ~ X)
P (X,  ~ have causal states S = {si } each occurring with
                                                                     ists some Q = (f, Ω, M) such Cq (Q) < Cq (Q+ ). Lemma
stationary probability πi . Define the conditional distri-           1 implies that we can assume Ω = {|ψ0 i, |ψ1 i} for some
            ~ = P (X|
bution Pi (X)         ~ X~ = x~ ∈ si ) as the future morph           |ψ0 i and |ψ1 i and encoding function f (x)     ~ = |ψi i if-and-
of causal state si . We will make use of the following two           only-if x~ ∈ s+    , without   loss  of  generality. Cq (Q), the
                                                                                      i
results derived in [20].                                             von-Neumann entropy of the ensemble {|ψi i, πi+ }, is a
                                                   ~ X)
                                                     ~               monotonically decreasing function of |hψ0 |ψ1 i| [46]. Thus
Lemma 1 (Causal state correspondence). Let P (X,                                         +                                  + +
be a stochastic process with causal states {si }. There              pq (Q) < Cq (Q ) implies that |hψ0 |ψ1 i| > |hs0 |s1 i| =
                                                                     C
                                                                        p(1 − q). Meanwhile, Lemma 2 implies
exists an optimal model Q = (q , Ω, M) where Ω = {|si i}
        ~ = |si i if-and-only-if x~ ∈ si .
and q (x)                                                                                                     1
                                                                                          X                       p
                                                                          |hψ0 |ψ1 i| ≤     [P0+ (~x)P1+ (~x)] 2 = p(1 − q)       (B2)
 This implies that we can limit our search for optimal                                  ~
                                                                                        x

models Q = (f, Ω, M), to those whose internal states                 This is a contradiction. Thus no such Q exists.
                                                                                                                                          9

      2.   Optimality of the Retrocausal Model.                       state from largest to smallest by λ−     −    −
                                                                                                          0 , λ1 , λ2 . Meanwhile
                                                                                                         ψ1
                                                                      by the above lemma Cq (Q) = S(ρ ) where
  Let Ph− denote the time reversal of the heralding coin
process, with corresponding ε-machine in Fig. 2(b).                            ρψ1 = π0− |0ih0| + π2− |1ih1| + π1− |ψ1 ihψ1 |,

Theorem 2. Define Q− = (ε−                  −   −
                                       q , Ω , M ), where
                                                                      and |ψ1 i is described by Eq. (B4). We label the eigenval-
ε−  ~ = |s−
 q (y)
                                   −
          i i if-and-only-if y~ ∈ si , with
                                                                      ues of ρψ1 from largest to smallest by λψ   1   ψ1   ψ1
                                                                                                                 0 , λ1 , λ2 . To
                                                                                                       −
                                                                      establish that Cq (Q) ≥ Cq (Q ) it is sufficient to show
                   |s−
                     0 i = |0i,
                                                                      λ−  λψ1 , where  denotes majorization [47]. This
                           √                                          is established by proving that (1) λ−           ψ1
                     −                                                                                         0 ≥ λ0     and (2)
                                 p
                   |s1 i = q|0i + 1 − q|1i,                             −     −      ψ1    ψ1
                                                                      λ0 + λ1 ≥ λ0 + λ1 .
                   |s−
                     2 i = |1i,                               (B3)                                          ψ1
                                                                         We begin by establishing λ−  0 ≥ λ0 . By the minimax
Ω− = {|s−                                   −
         i i}, and the measurement process M given in                 principle [48], the largest eigenvalue for ρψ1 is
Fig. 3(b). Q is an optimal quantum model for Ph− .
             −

                                                                                         λψ1
                                                                                          0 =         max hx|ρψ1 |xi,                   (B6)
  Below we break the proof of this theorem down into a                                            |hx|xi|2 =1
series of small steps. Each step is phrased as a lemma.
                                                                      Suppose that this maximum is attained for some |xi =
Lemma 3. Let Q = (f, Ω, M) be a quantum model for                     |x(t, φ, κ, η)i such that
                  ~ = |ψi i iff y~ ∈ s−
Ph− satisfying f (y)                  i . Then, up to a
unitary rotation,
                                                                                                       p
                                                                         |xi = t sin φ eiη |0i + eiκ       1 − t2 |1i + t cos φ|2i,     (B7)
    |ψ0 i = |0i,
                                p                                     where φ ∈ [0, π/2], 0 ≤ t ≤ 1 and η, κ ∈ [0, 2π]. We
    |ψ1 i = r sin θ eiω |0i +       1 − r2 eiα |1i + r cos θ|2i,      can assume the coefficient of |2i is real and positive be-
    |ψ2 i = |1i,                                               (B4)   cause Eq. (B6) remains unchanged when |xi → eiψ |xi.
                                                                      Substituting Eq. (B7) into Eq. (B6) yields
for some θ ∈ [0, π/2],
                  √ 0≤r≤  1, α, ω ∈ [0, 2π], such that
         √              √
r sin θ ≤ q and 1 − r2 ≤ 1 − q.                                       λψ    −        2   −        2   −
                                                                       0 = π0 |hx|0i| + π2 |hx|1i| + π1 rt sin θ sin φe
                                                                        1                                               i(ω−η)

                                             1                                                                        2
Proof. Set Fij− =           −
                               y )Pj− (~y )] 2 . Explicit evalua-
                     P                                                               p       p
                        y [Pi (~
                        ~
                                                   √                       +ei(α−κ) 1 − r2 1 − t2 + rt cos θ cos φ . (B8)
               −       √      −                −
tion yields F01   = q, F02        = 0, F12       = 1 − q. By
the maximum fidelity constraint, |hψi |ψj i| ≤ Fij− . Thus            We defined |x(t, φ, κ, η)i to be the vector that maximizes
hψ0 |ψ2 i = 0. Therefore |ψ0 i = |0i and |ψ2 i = |1i                  Eq. (B8); and thus we have implicitly optimized over κ
up to a unitary rotation. We can then write |ψ1 i in                  and η in Eq. (B8). This optimization will automatically
the form above without loss of generality as the coeffi-              set ei(α−κ) = ei(ω−η) = 1 (since any two complex num-
cient of |2i can be made real and positive by choosing a              bers c1 , c2 ∈ C satisfy |c1 + c2 |2 ≤ (|c1 | + |c2 |)2 ). Using
                                                                      this and trigonometry identities to simplify Eq. (B8),
                           √ element |2i. Meanwhile
suitable definition of basis
                                                       √
                                                             con-
straints on |hψ1 |ψ2 i| ≤ 1 − q and |hψ0 |ψ1 i| ≤ q imply             yields
          √        √            √
r sin θ ≤ q and 1 − r2 ≤ 1 − q.
                                                                           λψ    − 2    2      −      2
                                                                            0 = π0 t sin φ + π2 (1 − t )
                                                                             1


  Our models described in Eq.√ (4) can be obtained by                                                 p     p      2
                        √                       √                               +π1− rt cos (φ − θ) + 1 − r2 1 − t2 (B9)
setting r sin θ eiω = q and 1 − r2 eiα = 1 − q in
Eq. (B4) (i.e. this corresponds to choosing |ψ0 i = |s−
                                                      0 i,                                                                         ψ0
|ψ1 i = |s−
          1 i and  |ψ2 i = |s−
                             2 i). The subsequent lemma                 We now show that there always exists some λ0 1 such
                                                                                    ψ10    ψ1
then establishes that this is the optimal choice.                     that λ−0 ≥ λ0 ≥ λ√   0 . The maximum fidelity constraint
                                                                      implies r sin(θ) ≤ q. Thus there exists some dθ such
Lemma 4. For any quantum model Q = (f, Ω, M) of                                             √
                                                                      that r sin(θ + dθ) = q, (in particular we choose the so-
Ph− satisfying f (y)
                  ~ = |ψi i if-and-only-if y~ ∈ s−
                                                 i .                  lution of this equation where 0 < θ+dθ ≤ π/2). Consider
                       Cq (Q) ≥ Cq (Q− ).                     (B5)              ψ0                       0
                                                                               λ0 1 =     max hx|ρψ1 |xi,
                                                                                        |hx|xi|2 =1
That is, Q− , as described by Eq. (4), is the lowest en-                          0
tropy (optimal) model which satisfies the causal state cor-                    ρψ1 = π0− |0ih0| + π2− |1ih1| + π1− |ψ10 ihψ10 |,
respondence.
                                                                      where
Proof. By definition Cq (Q− ) = S(ρ− ) for ρ− =                                                   p
P     − −      −           −     −       −                            |ψ10 i = r sin (θ + dθ)|0i + 1 − r2 |1i + r cos (θ + dθ)|2i
   i πi |si ihsi |, where πi = Ph (y~ ∈ si ) and the states                    √
  −
                                                                                              p                p
|si i are given in Eq. (4). We label the eigenvalues of this                 = q|0i + sin χ 1 − q|1i + cos χ 1 − q|2i, (B10)
                                                                                                                                         10
                √        √
for sin χ = 1 − r2 / 1 − q.               Furthermore let |x0 i =                         Appendix C: Proof of Result 2
|x(t, β, 0, 0)i be defined as
                                 p                                              Here we prove Result 2. To do this, we require some
     |x0 i = t sin β|0i +         1 − t2 |1i + t cos β|2i             (B11)   preliminary lemmas. The first connects the capacity for
                                                                              quantum models to improve upon their optimal classical
for β = min(π/2, φ + dθ). Then we have                                        counterparts with causal asymmetry.
   ψ0              0                                                          Lemma 5. If the classical and quantum statistical com-
  λ0 1 ≥ hx0 |ρψ1 |x0 i
                                                                              plexity of a process P coincide, such that Cq+ = Cµ+ , then
       = π0− t2 sin2 β + π2− (1 − t2 )                                        P is causally symmetric and Cµ+ = Cµ− = E.
                                              p             p       2
             +π1− rt cos (β − θ − dθ) +           1 − r2     1 − t2            Proof. We first make use of the prior results showing that
        ≥ π0− t2 sin2 φ + π2− (1 − t2 )                                        whenever classical models waste information, more effi-
                                        p            p            2
                                                                               cient quantum models exist [22]. Specifically Cµ+ > E
             +π1− rt cos (φ − θ) +          1 − r2       1 − t2                if-and-only-if Cq+ < Cµ+ . Thus, Cq+ = Cµ+ implies that
                                                                               Cµ+ = E. It is therefore sufficient to show that Cµ+ = E
        = λψ 1
                                                                      (B12)
           0                                                                   implies Cµ− = E.
where we have used the fact that 0 ≤ φ ≤ β ≤ π/2 and                               We prove this by contradiction. Assume Cµ+ = E but
|β − θ − dθ| ≤ |φ − θ| ≤ π/2. Specifically these two                              −
                                                                               Cµ > E. Now Cµ+ = E implies H(S−1 |X)         ~ = 0, where
conditions imply sin β ≥ sin φ and cos (β − θ − dθ) ≥                          S−1 is the random variable governing the causal state at
                               ψ0                                              t = −1 [9]. Thus given ~x we can find a unique si such
cos (φ − θ) ≥ 0. Thus we have λ0 1 ≥ λψ1
                                      0 .
                            ψ0                                                 that P (X~ = x| ~X ~ = ~x) is only non-zero when x~ ∈ si .
   To show λ−
            0 ≥ λ0 , we define |yi to be the state satis-
                   1

       ψ10                                                                     It follows that the sets τi = {~x|Pi (X ~ = ~x) 6= 0} form a
               ψ10
fying λ0 = hy|ρ |yi. In general we can parameterize                            partitioning on the space of all futures (i.e. τi ∩ τj = ∅
                       p                             p                         for i 6= j).
 |yi = weia |0i +           1 − w2 sin ξeib |1i +        1 − w2 cos ξ|2i           Furthermore any two x,                       ~ X~ = x)
                                                                                                          ~ x~0 ∈ si satisfy P (X|      ~ =
                                                                                    ~  ~    0
                                                                               P (X|X = x~ ), by definition of si . Thus Bayes’ theorem
for 0 ≤ w ≤ 1, ξ ∈ [0, π/2], and a, b ∈ [0, 2π]. Using the
                                                                               implies that the τi partition the future into equivalence
same argument as in Eq. (B9), we can show a = b = 0                                                                 ~X~ = ~x) = P (X|~X ~ =
and thus                                                                       classes ~x ∼ ~x0 if-and-only-if P (X|
                                                                                 0
                                                                              ~x ) [49]. Hence {τi } constitute the retrocausal states.
        ψ0
    λ0 1 = π0− w2 + π2− (1 − w2 ) sin2 ξ +      (B13)                          Bayes’ theorem also yields P (X~ = x|    ~X~ = ~x ∈ τi ) 6= 0
                                                                                                                           −
                        p                   √   2                              only when x~ ∈ si . This implies H(S−1        |X~ = x)
                                                                                                                                    ~ = 0,
           π1−
                p
                  1 − q 1 − w2 cos (χ − ξ) + qw                                          −
                                                                               where S−1 governs the retrocausal state at time t = −1.
                          √                                                    Hence Cµ− = E, which is a contradiction.
  Define |y 0 i = w |0i + 1 − w2 |1i. By mirroring the
analysis in Eq. (B12) we find                                                   It follows as a direct corollary of this result that causal
                                                                              asymmetry vanishes for deterministic processes (i.e. pro-
             λ−     0 − 0
              0 ≥ hy |ρ |y i                                                  cesses where H(X| ~ X)~ = 0).
                = π0 w + π2− (1 − w2 )
                   − 2
                                                                                                                    ~ X)
                                                                                                                       ~ has
                                                                              Lemma 6. Any deterministic process P (X,
                               p        √   2
                  +π1−
                        p
                          1 − q 1 − w2 + qw                                   ∆Cµ = 0.

                 ≥ λ0 1
                       ψ0
                                                                      (B14)   Proof. Any deterministic process has E = Cµ+ [9, 50].
                                                                              Since E ≤ Cq+ ≤ Cµ+ it follows that E = Cµ+ = Cq+ and
                                                 ψ1       ψ0                  thus according to the above lemma ∆Cµ = 0.
Together the above results imply λ−
                                  0 ≥ λ0 ≥ λ0 , es-
                                          1

                     −     ψ1
tablishing step (1) λ0 ≥ λ0 .                                                     Our next lemma makes use of q-machines [28], the sim-
                                             ψ1     ψ1
  For step (2) We must show λ−        −
                                0 + λ1 ≥ λ0 + λ1 .                            plest currently known quantum models. Consider a pro-
                           −
However by construction ρ only spans a 2-dimensional                          cess P = P (X, ~ X)
                                                                                               ~ whose classical ε-machine has a collec-
Hilbert space and thus we have λ−     −
                                0 + λ1 = 1. It follows                        tion of causal states S = {si } and transition probabilities
                  ψ1    ψ1
that λ−     −
       0 + λ1 ≥ λ0 + λ1 . Together, these results imply
                                                                                                                           ~ X),
                                                                              Tijx . Let k denote the cryptic order of P (X,  ~ defined
λ  λ and therefore Cq (Q− ) ≤ Cq (Q).
 −      ψ1
                                                                              as the smallest l such that H(Sl |X0:∞ ) = 0 [23, 28, 50].
                                                                              The q-machine of P has internal states |Si i defined by a
  By Lemma 1, Ph− has an optimal quantum model                                recursive relation
which satisfies the causal state correspondence. Mean-
                                                                                           |Si i = |Si (l = k)i, where                (C1)
while by Lemma 4, any Q satisfying the causal state cor-                                              Xq
respondence must have Cq (Q) ≥ Cq (Q− ). It follows that                                   |Si (l)i =        Tijx |xi|Sj (l − 1)i,    (C2)
Q− is an optimal quantum model for Ph− .                                                               xj
                                                                                                                                            11

                                                                        such that C̄q+ = S(ω + ). Then
                                                                                          X
                                                      1|
                                                        1          𝑠1         ω + = lim      πi |Si (l)ihSi (l)|,
                                            𝑛
                                      n +2|𝑝𝑛+2         𝑛                              l→∞
                          n|
                             1                                                                    i
                            𝑛                                                          X          Xp
                                                                  1
                                                            n +2|𝑝𝑛+2              =         πi              Pi (~x)Pi (~x0 )|~xih~x0 |,
                                                        𝑛
                                                  n +1|𝑝𝑛+1
                                                                                         i        ~ x0
                                                                                                  x,~
                                                                                       XX                   Xq
                                                                  1
                                                            n +1|𝑝𝑛+1              =                  Px~     P~x|x~P~x0 |x~|~xih~x0 |,
                                          𝑠0                                             i   x∈s
                                                                                             ~ i            ~ x0
                                                                                                            x,~
                                𝑛/2                                                      X q
                          n +2|𝑝𝑛+2
                                                                                   =        P~x|x~Px~P~x0 |x~0 Px~0 δx,     xih~x0 |. (C3)
                                                                                                                     ~ x~0 |~
                   𝑛/2
             n +1|𝑝𝑛+1                                                                 ~ x0 ,x,
                                                                                       x,~   ~ x~0
                                     1
                                 n/2|𝑛                                  Furthermore the forward q-machine complexity is given
                   𝑠𝑛/2                                                 by C̄q+ = S(ω + ). A similar argument shows that C̄q− is
                                                                        given by C̄q− = S(ω − ), where
                                                                                       X q
                                                                            ω− =           ~ x P~
                                                                                          Px|~  x Px~0 |~
                                                                                                        x0 P~
                                                                                                            x0 δ~
                                                                                                                x,~   ~ x~0 |.
                                                                                                                  x0 |xih                  (C4)
FIG. 5. The n-m flower process, illustrated for the case m =                       ~ x0 ,x,
                                                                                   x,~   ~ x~0
2, and n even. Physically this process can be generated by a
set {d1 , . . . , dn } of m-sided dice where each dice di is biased,    Consider now the pure state
so that it lands on side j ∈ {1, . . . m} with probability pij (and                            Xp
in general the bias on each dice is different, such that pij 6= pkj                  |ψiX,
                                                                                        ~X ~ =      P (x,    ~ ~xi
                                                                                                       ~ ~x)|x,                            (C5)
for i 6= k). We randomly select a dice di , recording the choice                                            x,~
                                                                                                            ~x
xt = i. Afterwards we role the dice, transcribing the outcome
j as xt+1 = j + n.                                                      which represents that quantum superposition, or q-
                                                                        sample [51], over all possible output strings of the
                                                                                              ~ X),
                                                                        stochastic process P (X, ~ with associated density op-
and |Si (0)i = |ii. The associated encoding function                    erator
satisfies f (x) ~ = |Si i whenever x~ ∈ si [23, 28]. Let                          X X X Xp
C̄q = S(ρ) be the q-machine complexity – the amount                       ρX,
                                                                            ~X~ =                   P←
                                                                                                     x 0 P←
                                                                                                     →    →  ~ xihx~0 |h~x0 | (C6)
                                                                                                          x |xi|~
of information      a q-machine stores about the past, where                             ~ i x~0 ∈s0i ~
                                                                                    i,i0 x∈s            x0
                                                                                                      x,~
       P
ρ =       i π i |Si ihSi |. Meanwhile let the max entropy
D̄q = log tr[ρ]0 be the q-machine state complexity – the                We can verify that ω + = TrX~ [ρX~X~ ] and ω − = TrX~ [ρX~X~ ].
minimum dimensionality of any quantum system Ξ ca-                      Thus S(ω − ) = S(ω + ) and therefore C̄q+ = C̄q− . The q-
pable of storing these internal states. Note that since                 machine complexity of the forward and backward pro-
q-machines are valid quantum models, Cq+ ≤ C̄q+ and                     cesses thus coincide.
Cq− ≤ C̄q− . Likewise Dq+ ≤ D̄q+ and Dq− ≤ D̄q− . We now                  Note that the rank of ω + and ω − must also coin-
establish that the q-machine for P and its time-reversal                cide. Thus, an analogous argument establishes that
P − have coinciding Von Neumann entropies and coincid-                  log tr[ρ+ ]0 = log tr[ρ− ]0 , indicating the two models also
ing max entropies.                                                      have the same dimensionality. Therefore D̄q+ = D̄q− .
                                                                           We now prove Result 2. Consider any stochastic pro-
Lemma 7. Let P (X,     ~ X)
                          ~ be a stationary stochastic pro-             cess P. First assume P is causally asymmetric, such that
            − ~ ~
cess and P (Y , Y ) its time reversal with q-machine com-               ∆Cµ 6= 0. Note first that this implies Cµ+ , Cµ− > E (by
plexity C̄q+ and C̄q− , and q-machine state complexity D̄q+             Lemma 5). Meanwhile Lemma 7 implies that C̄q+ = C̄q− .
and D̄q− respectively. Then C̄q+ = C̄q− , and D̄q+ = D̄q−               Thus it is sufficient to show that C̄q+ < Cµ+ and C̄q− <
                                                                        Cµ− , whenever Cµ+ , Cµ− > E.
                                                                           Note that for a general process, C̄q < Cµ , if-and-only-
Proof. We first introduce some compact notation. Let                    if the q-machine has two internal states with non-zero
                                                                        overlap hSi |Sj i > 0 [52]. It is also previously estab-
P (X~ = x, ~X~ = ~x) = P←                    ~
                            x similarly P (X = ~
                            →                      x|X~ = x)
                                                          ~ =
           ~                                           ~                lished that that whenever Cµ > E, we can find some
P~x|x~, P (X = ~x|S−1 = si ) = Pi (~x) as well as P (X = x)~ =          hSi (1)|Sj (1)i > 0 [22], as defined by Eq. (C1). It fol-
Px~ and P (x~ ∈ si ) = πi .                                             lows from the iterative construction that hSi |Sj i > 0,
   Now let |Si+ i denote the internal states of the q-                  and thus C̄q < Cµ . Therefore Cµ+ > E implies C̄q+ < Cµ+
machine for P (X,    ~ X),
                        ~ such that ρ+ = P πi |S + ihS + |,             and Cµ− > E implies C̄q− < Cµ− . Hence, for any causally
                                                 i      i   i
and C̄q+ = S(ρ+ ). From existing work [23, 28], we                      asymmetric P
know thatPliml→∞ hSi (l)|Sj (l)i = hSi (k)|Sj (k)i. Thus let
ω + (l) =             +      +
              i πi |Si (l)ihSi (l)|, and ω
                                           +
                                              = liml→∞ ω + (l)                          max(Cq+ , Cq− ) < min(Cµ+ , Cµ− )                  (C7)
                                                                                                                                      12

Conversely, suppose max(Cq+ , Cq− ) = min(Cµ+ , Cµ− ).               It is trivial to generalize the causal state correspon-
Without loss of generality, we can assume Cµ+ ≤ Cµ− .              dence to mixed state models. Thus we can assume that
This implies either (i) Cq+ = Cµ+ or (ii) Cq− = Cµ+ . In           Q has an encoding function where
the case of (i), direct application of Lemma 5 implies                                      X             (i)  (i)
Cµ+ = Cµ− = E. In the case of (ii) we have Cµ+ ≥ C̄q+ =                        f (x)
                                                                                   ~ = ωi =     qk (si )|ψk ihψk |,     (E2)
C̄q− ≥ Cq− = Cµ+ , which implies Cµ+ = C̄q+ . That is, q-                                        k

machines are not more efficient than ε-machines in mod-
                                                                   if-and-only-if x~ ∈ si . So that the internal states Ω = {ωi }
elling P. This is true if-and-only-if Cq+ = Cµ+ [22, 23].
                                                                   are in 1-1 correspondence with the classical causal states.
Thus Lemma 5 again implies Cµ+ = Cµ− = E. This com-                   Our proof makes use of the requirement that causal
pletes the proof.                                                                                                          ~ X)~ =
                                                                   models store no oracular information, i.e. I(R, X|
                                                                   P                 ~   ~
                                                                      x~ P (x)I(R,
                                                                             ~       X|X = x)   ~ = 0 where R is the ran-
            Appendix D: n-m flower process                         dom variable governing the memory.                 Regrouping
                                                                   the pasts into causal state equivalence classes yields
                                                                   P                 ~
   The family of n-m flower processes demonstrate how                 si ∈S πi I(R, X|x~ ∈ si ) = 0, where πi is the probabil-
                                                                   ity the past belongs to si . Thus I(R, X|    ~ x~ ∈ si ) = 0 for
causal asymmetry can be potential unbounded (see Fig.
5). The process has statistical complexity Cµ+ = 1 +               every si ∈ S.
1                                                                     We have assumed some elements of Ω are mixed. In
2 log[n]. In contrast, the time reversed process will have
at most m + 1 causal states and thus Cµ− ≤ log[m + 1].             particular, suppose we have a specific ωi0 = ω ∈ Ω with
Meanwhile the predictive and retrodictive topological              S(ω) > 0 that occurs with probability πi0 = π. Let x~ be
state complexities satisfy Dµ+ = log[n + 1] and Dµ− ≤              a particular past such that f (x)   ~ = ω, and Ψ = {|ψk i}
log[m + 1]. n and m can be adjusted independently. Set-            be a set of pure states that form an unravelling of ω.
ting m = 2, and allowing n → ∞, yields diverging Cµ+               I.Fe.
                                                                   P        there must exist some qk ∈ [0, 1] such that ω =
but finite Cµ− . Thus ∆Cµ also diverges to infinity. A                k qk |ψk ihψk |. Now let OM be a quantum process that
                                                                   maps ω to a classical random variable X        ~ governed by
similar divergence is witness for topological state com-
plexity.                                                                                           ~  ~
                                                                   probability distribution P (X|X = x).    ~ By definition of a
   Applying Result 2, we see that Cq+ and Cq− are both             quantum model, this process can always be constructed
bounded above by log 3. The same is also true for Dq+              by concatenations of M acting on a physical system Ξ.
and Dq− . Thus, quantum models of this process can fit                Let A represent the state of Ξ and B be the random
within a single qutrit, whether modelling in forward or            variable that governs the resulting output of OM acting
reverse time. In the specific case of the former, Cµ+ and          on Ξ. Zero oracular information implies that A and B
                                                                   must be uncorrelated when conditioned on observing past
Dµ+ diverge to infinity. Thus, we obtain a family of pro-
                                                                   ~ Therefore OM (|ψk ihψk |) = OM (|ψj ihψj |) = OM (ω)
                                                                   x.
cesses whose quantum models field unbounded memory
                                                                   for all |ψk i, |ψj i ∈ Ψ.
advantage - in both the entropic and single-shot sense.
                                                                      Now consider the entropy of Q. By concavity of en-
                                                                   tropy
                                                                                                                           
     Appendix E: Excluding Mixed State Models                            X                   X                      X
                                                                    S        πj ωj  = S       qk π|ψk ihψk | +       πj ωj 
  In this section we consider more general causal models                 j                   k                       ωj 6=ω
Q = (f, Ω, M) which have the freedom to encode pasts                                                                          
                                                                                        X                         X
                          X                                                         ≥       qk S π|ψk ihψk | +            πj ωj 
             f (x)
                ~ = ωx~ =         ~ kx~ihψkx~|,
                              qk (x)|ψ             (E1)                                 k                         ωj 6=ω
                              k                                                                                               
                                                                                                                  X
into mixed quantum states. We show that this does                                   ≥ mink S π|ψk ihψk | +             πj ωj  .
not allow for models which are more optimal than those                                                         ωj 6=ω
which only encode pasts into pure quantum states.                                                                                    (E3)
Theorem 3. Consider a stochastic process P (X,            ~ X),
                                                             ~     Without loss of generality we can assume this minimum
with a causal model Q = (f, Ω, M).       If the internal  states   is obtained for k = 0. Let Ω00 = (Ω \ ω) ∪ {|ψ0 ihψ0 |} be
                                              ~ ix~ihψix~|, then
                                       P
of Q are mixed, such that f (x)   ~ = i qi (x)|ψ                   a set of internal states where ω is replaced with |ψ0 ihψ0 |,
we can always find a causal model Q = (f 0 , Ω0 , M0 ) such
                                         0
                                                                   and define encoding function f 00 such that f 00 (x)
                                                                                                                     ~ = f (x)
                                                                                                                             ~
that f 0 (x)
          ~ = |sx~ihsx~|, and Cq (Q0 ) ≤ Cq (Q).                   except when f (x) ~ = ω, whereby f 00 (x)
                                                                                                           ~ = |ψ0 ihψ0 |. De-
                                                                   fine a new quantum model Q00 = (f 00 , Ω00 , M). Clearly
              ~ X)
Proof. Let P (X, ~ have causal states S = {si }. Sup-              Cq (Q00 ) ≤ Cq (Q).
pose Q = (f, Ω, M) is an optimal causal model for                     If any of the states in Ω00 are still mixed, then by
   ~ X),
P (X, ~ with mixed internal states.                                repeating the above procedure we can replace them
                                                                                                                                13

with pure states, thereby constructing a model Q0 =
(f 0 , Ω0 , M) with pure internal states such that Cq (Q0 ) ≤
Cq (Q)


 [1] Noah Linden, Sandu Popescu, Anthony J Short, and An-                energy cost of stochastic computation,” in Proceedings of
     dreas Winter, “Quantum mechanical evolution towards                 the Royal Society of London A: Mathematical, Physical
     thermal equilibrium,” Physical Review E 79, 061103                  and Engineering Sciences, Vol. 468 (The Royal Society,
     (2009).                                                             2012) pp. 4058–4066.
 [2] Sandu Popescu, Anthony J Short, and Andreas Win-               [16] Adán Cabello, Mile Gu, Otfried Gühne, Jan-Åke Lars-
     ter, “Entanglement and the foundations of statistical me-           son, and Karoline Wiesner, “Thermodynamical cost of
     chanics,” Nature Physics 2, 754 (2006).                             some interpretations of quantum theory,” Physical Re-
 [3] Don N Page and William K Wootters, “Evolution with-                 view A 94, 052127 (2016).
     out evolution: Dynamics described by stationary observ-        [17] Alexander B Boyd, Dibyendu Mandal, Paul M Riech-
     ables,” Physical Review D 27, 2885 (1983).                          ers, and James P Crutchfield, “Transient dissipation and
 [4] Huw Price, Time’s arrow & Archimedes’ point: new di-                structural costs of physical information transduction,”
     rections for the physics of time (Oxford University Press,          Physical Review Letters 118, 220602 (2017).
     USA, 1997).                                                    [18] Note that in computational mechanics literature, causal
 [5] James P Crutchfield, Christopher J Ellison, and John R              asymmetry is often referred to as causal irreversibility
     Mahoney, “Times barbed arrow: Irreversibility, cryptic-             [5]. Here, we choose the term causal asymmetry to avoid
     ity, and stored information,” Physical review letters 103,          confusion with standard notions of irreversibility used in
     094101 (2009).                                                      the physics community.
 [6] James P Crutchfield, “Between order and chaos,” Nature         [19] Robert Konig, Renato Renner, and Christian Schaffner,
     Physics 8, 17–24 (2012).                                            “The operational meaning of min-and max-entropy,”
 [7] Formally, this implies that the conditional mutual infor-           IEEE Transactions on Information theory 55, 4337–4347
     mation I(R, X|    ~ is zero, where R is the random vari-
                    ~ X)                                                 (2009).
                                                         ~ X)
     able governing the state of Ξ. In literature, I(R, X|   ~ is   [20] Whei Yeap Suen, Jayne Thompson, Andrew J. P. Garner,
     named oracular information, as it captures the amount               Vlatko Vedral, and Mile Gu, “The classical-quantum di-
     of information a state of the memory s stores about the             vergence of complexity in the ising spin chain,” Quantum
     future that is not contained in the past [45, 53]. Note that        1, 25 (2017).
     this notion of causal model differs from the recent devel-     [21] Note that while these definitions implicitly assume we
     opments in quantum causal models [54, 55] and founda-               can only encode onto pure states Ω. We show in Appendix
     tion work on causal inference [56].                                 E that even when we allow the encoding function to map
 [8] James P Crutchfield and Karl Young, “Inferring statisti-            directly onto mixed quantum states, it does not help –
     cal complexity,” Physical Review Letters 63, 105 (1989).            there is always a pure state quantum causal model with
 [9] Cosma Rohilla Shalizi and James P Crutchfield, “Com-                entropy S(ρ) = Cq+ (see Theorem 3).
     putational mechanics: Pattern and prediction, structure        [22] Mile Gu, Karoline Wiesner, Elisabeth Rieper, and
     and simplicity,” Journal of statistical physics 104, 817–           Vlatko Vedral, “Quantum mechanics can reduce the com-
     879 (2001).                                                         plexity of classical models,” Nature communications 3,
[10] W.M. Gonalves, R.D. Pinto, J.C. Sartorelli, and M.J.                762 (2012).
     de Oliveira, “Inferring statistical complexity in the drip-    [23] Paul M Riechers, John R Mahoney, Cina Aghamoham-
     ping faucet experiment,” Physica A: Statistical Mechan-             madi, and James P Crutchfield, “Minimized state com-
     ics and its Applications 257, 385 – 389 (1998).                     plexity of quantum-encoded cryptic processes,” Physical
[11] Joongwoo Brian Park, Jeong Won Lee, Jae-Suk Yang,                   Review A 93, 052317 (2016).
     Hang-Hyun Jo, and Hie-Tae Moon, “Complexity analy-             [24] Matthew S Palsson, Mile Gu, Joseph Ho, Howard M
     sis of the stock market,” Physica A: Statistical Mechanics          Wiseman, and Geoff J Pryde, “Experimentally mod-
     and its Applications 379, 179–187 (2007).                           eling stochastic processes with less memory by the use
[12] Peter Tino and Miroslav Koteles, “Extracting finite-state           of a quantum processor,” Science Advances 3, e1601302
     representations from recurrent neural networks trained              (2017).
     on chaotic symbolic sequences,” IEEE Transactions on           [25] Ryan Tan, Daniel R Terno, Jayne Thompson, Vlatko
     Neural Networks 10, 284–302 (1999).                                 Vedral, and Mile Gu, “Towards quantifying complex-
[13] Adán Cabello, Mile Gu, Otfried Gühne, and Zhen-Peng               ity with quantum mechanics,” Eur. Phys. J. Plus 129,
     Xu, “Optimal classical simulation of state-independent              191 (2014).
     quantum contextuality,” Physical Review Letters 120,           [26] Alex Monras and Andreas Winter, “Quantum learning
     130401 (2018).                                                      of classical stochastic processes: The completely positive
[14] Andrew JP Garner, Jayne Thompson, Vlatko Vedral,                    realization problem,” Journal of Mathematical Physics
     and Mile Gu, “Thermodynamics of complexity and                      57, 015219 (2016).
     pattern manipulation,” Physical Review E 95, 042140            [27] Andrew JP Garner, Qing Liu, Jayne Thompson, Vlatko
     (2017).                                                             Vedral, and Mile Gu, “Provably unbounded memory ad-
[15] Karoline Wiesner, Mile Gu, Elisabeth Rieper, and                    vantage in stochastic simulation using quantum mechan-
     Vlatko Vedral, “Information-theoretic lower bound on                ics,” New Journal of Physics 19, 103009 (2017).
                                                                                                                                14

[28] John R Mahoney, Cina Aghamohammadi, and James P                   output processes,” npj Quantum Information 3, 6 (2017).
     Crutchfield, “Occams quantum strop: Synchronizing and        [42] Justin Dressel, Areeya Chantasri, Andrew N Jordan,
     compressing classical cryptic processes via a quantum             and Alexander N Korotkov, “Arrow of time for continu-
     channel,” Scientific reports 6 (2016).                            ous quantum measurement,” Physical review letters 119,
[29] Felix C Binder, Jayne Thompson, and Mile Gu, “A prac-             220507 (2017).
     tical, unitary simulator for non-markovian complex pro-      [43] Oscar CO Dahlsten, “Non-equilibrium statistical me-
     cesses,” arXiv preprint arXiv:1709.02375 (2017).                  chanics inspired by modern information theory,” Entropy
[30] Justin Dressel, “Weak values as interference phenom-              15, 5346–5361 (2013).
     ena,” Physical Review A 91, 032116 (2015).                   [44] Susanne Still, David A Sivak, Anthony J Bell, and
[31] Søren Gammelmark, Brian Julsgaard,             and Klaus          Gavin E Crooks, “Thermodynamics of prediction,” Phys-
     Mølmer, “Past quantum states of a monitored system,”              ical review letters 109, 120604 (2012).
     Physical review letters 111, 160401 (2013).                  [45] James P Crutchfield, Christopher J Ellison, Ryan G
[32] HM Wiseman, “Weak values, quantum trajectories, and               James, and John R Mahoney, “Synchronization and
     the cavity-qed experiment on wave-particle correlation,”          control in intrinsic and designed computation: An
     Physical Review A 65, 032111 (2002).                              information-theoretic analysis of competing models of
[33] Dian Tan, SJ Weber, Irfan Siddiqi, K Mølmer, and                  stochastic computation,” Chaos: An Interdisciplinary
     KW Murch, “Prediction and retrodiction for a continu-             Journal of Nonlinear Science 20, 037105 (2010).
     ously monitored superconducting qubit,” Physical review      [46] Richard Jozsa and Jürgen Schlienz, “Distinguishability
     letters 114, 090403 (2015).                                       of states and von neumann entropy,” Physical Review A
[34] T Rybarczyk, B Peaudecerf, M Penasa, S Gerlich, Brian             62, 012301 (2000).
     Julsgaard, Klaus Mølmer, S Gleyzes, M Brune, JM Rai-         [47] Michael A Nielsen and Guifré Vidal, “Majorization and
     mond, S Haroche, et al., “Forward-backward analysis of            the interconversion of bipartite states.” Quantum Infor-
     the photon-number evolution in a cavity,” Physical Re-            mation & Computation 1, 76–93 (2001).
     view A 91, 062116 (2015).                                    [48] R Courant and D Hilbert, Methods of mathematical
[35] SJ Weber, Areeya Chantasri, Justin Dressel, Andrew N              physics, vol. I (Interscience, 1953).
     Jordan, KW Murch, and Irfan Siddiqi, “Mapping the            [49] To derive this simply write P (X~ = x|      ~ = ~
                                                                                                                  ~X     x ∈ τi ) =
     optimal route between two quantum states,” Nature 511,                   ~ x|X=
                                                                           P (X=~   ~ x)P
                                                                                      ~ (x)~
                                                                                                =
                                                                                                        ~ x0 |X=
                                                                                                     P (X=~   ~ x)P
                                                                                                                  ~ (x)
                                                                                                                      ~
                                                                                                                           .
                                                                       P          ~ x|X=
                                                                                       ~ x)P      P         ~ x0 |X=
                                                                                                                  ~ x)P
     570 (2014).                                                         x∈s
                                                                         ~ i   P (X=~     ~ (x)
                                                                                             ~     x∈s
                                                                                                   ~ i   P (X=~      ~ (x)
                                                                                                                        ~

[36] Philippe Campagne-Ibarcq, Landry Bretheau, Em-               [50] John R Mahoney, Christopher J Ellison, Ryan G James,
     manuel Flurin, Alexia Auffèves, François Mallet, and            and James P Crutchfield, “How hidden are hidden pro-
     Benjamin Huard, “Observing interferences between past             cesses? a primer on crypticity and entropy convergence,”
     and future quantum states in resonance fluorescence,”             Chaos: An Interdisciplinary Journal of Nonlinear Science
     Physical review letters 112, 180402 (2014).                       21, 037112 (2011).
[37] Note that since ρ(t) and E(t) vary over a continuum,         [51] Dorit Aharonov and Amnon Ta-Shma, “Adiabatic quan-
     the memory costs of tracking either is likely to be un-           tum state generation and statistical zero knowledge,” in
     bounded. Thus one may need to modify present ap-                  Proceedings of the thirty-fifth annual ACM symposium on
     proaches. Existing approaches include the use of differ-          Theory of computing (ACM, 2003) pp. 20–29.
     ential entropies [38] and studying scaling as we track the   [52] Michael A Nielsen and Isaac L Chuang, “Quantum com-
     process to greater precision [27].                                putation and quantum information,” (2000).
[38] Sarah Marzen and James P Crutchfield, “Informational         [53] Christopher J Ellison, John R Mahoney, Ryan G James,
     and causal architecture of continuous-time renewal pro-           James P Crutchfield, and Jörg Reichardt, “Informa-
     cesses,” Journal of Statistical Physics 168, 109–127              tion symmetries in irreversible processes,” Chaos: An In-
     (2017).                                                           terdisciplinary Journal of Nonlinear Science 21, 037107
[39] Thomas J Elliott and Mile Gu, “Superior memory                    (2011).
     efficiency of quantum devices for the simulation of          [54] John-Mark A Allen, Jonathan Barrett, Dominic C Hors-
     continuous-time stochastic processes,” npj Quantum In-            man, Ciarán M Lee, and Robert W Spekkens, “Quantum
     formation 4, 18 (2018).                                           common causes and quantum causal models,” Physical
[40] Nix Barnett and James P Crutchfield, “Computational               Review X 7, 031021 (2017).
     mechanics of input–output processes: Structured trans-       [55] Fabio Costa and Sally Shrapnel, “Quantum causal mod-
     formations and the \epsilon -transducer,” Journal of Sta-         elling,” New Journal of Physics 18, 063032 (2016).
     tistical Physics 161, 404–451 (2015).                        [56] Judea Pearl, “Causal inference in statistics:         An
[41] Jayne Thompson, Andrew JP Garner, Vlatko Vedral,                  overview,” Statistics surveys 3, 96–146 (2009).
     and Mile Gu, “Using quantum theory to simplify input–
