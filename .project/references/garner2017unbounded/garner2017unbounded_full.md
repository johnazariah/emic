#

**Source:** garner2017unbounded
**Author:**
**Pages:** 12

---

## Full Text

                                                           Provably unbounded memory advantage in stochastic simulation
                                                                            using quantum mechanics.

                                                     Andrew J. P. Garner,1, 2, ∗ Qing Liu,3 Jayne Thompson,1 Vlatko Vedral,4, 1, 5, 2 and Mile Gu3, 6, 1, †
                                                    1
                                                     Centre for Quantum Technologies, National University of Singapore, 3 Science Drive 2, 117543, Singapore
                                                               2
                                                                 Center for Quantum Information, Institute for Interdisciplinary Information Sciences,
                                                                                    Tsinghua University, Beijing, 100084, China
                                                       3
                                                         School of Physical and Mathematical Sciences, Nanyang Technological University, 639673, Singapore
                                             4
                                               Atomic and Laser Physics, University of Oxford, Clarendon Laboratory, Parks Road, Oxford, OX1 3PU, United Kingdom.
                                                          5
                                                            Department of Physics, National University of Singapore, 2 Science Drive 3, Singapore 117542
                                                                    6
                                                                      Complexity Institute, Nanyang Technological University, 639673, Singapore.
                                                                                             (Dated: 15th November 2021)
                                                           Simulating the stochastic evolution of real quantities on a digital computer requires a trade-off
                                                         between the precision to which these quantities are approximated, and the memory required to
                                                         store them. The statistical accuracy of the simulation is thus generally limited by the internal
                                                         memory available to the simulator. Here, using tools from computational mechanics, we show that
                                                         quantum processors with a fixed finite memory can simulate stochastic processes of real variables
                                                         to arbitrarily high precision. This demonstrates a provable, unbounded memory advantage that a
arXiv:1609.04408v2 [quant-ph] 13 Oct 2017


                                                         quantum simulator can exhibit over its best possible classical counterpart.

                                                         PACS numbers: 03.67.-a, 02.50.Ey, 05.20.-y


                                               Many macroscopic processes we wish to simulate in-           the statistics of a n bit classical simulator for arbitrar-
                                            volve the dynamics of real numbers. The dynamical prop-         ily large n using a bounded amount of memory. Thus,
                                            erties we wish to track (e.g. the position of an object)        quantum simulators can side-step the precision-memory
                                            can take on almost any number, seemingly without no-            tradeoff – finite quantum memory can simulate such pro-
                                            ticeable quantization until one goes down to the Planck         cesses to arbitrary fixed precision.
                                            scale. The simulation of such processes necessitates com-          This unbounded divergence has practical and found-
                                            promise between the resources allocated and the preci-          ational consequences.      Practically, it suggests that
                                            sion with which we track such properties. Clever imple-         quantum processors may be increasingly advantageous as
                                            mentations to this problem, such as the floating point          we wish to simulate ever more memory-intensive systems,
                                            format [1], form the heart of modern computing techno-          such as those arising from big data sets. Foundationally,
                                            logy – but all subscribe to the same trade-off: treating a      the minimal memory required to simulate a process is a
                                            quantity with higher precision requires the allocation of       well-established measure of structure, known as statist-
                                            more memory. To perfectly replicate the future statistics       ical complexity [10–21]. Our work suggests that there are
                                            of a continuous variable dynamical system exactly would         certain processes which grow unboundedly in statistical
                                            inevitably require unbounded memory.                            complexity, but yet remain simple to an observer with
                                               The advent of quantum technology, however, opens             quantum capabilities.
                                            new possibilities. Not only has this technology shown
                                            great potential in solving problems many consider clas-            Cyclic random walks. Consider a small bead loc-
                                            sically intractable [2–6], it has demonstrated the capabil-     ated on a circular ring of circumference 1 (as per figure 1).
                                            ity to greatly reduce the amount of information one needs       Its position can always be described by some real num-
                                            to send in certain tasks requiring communication between        ber y ∈ [0, 1). At each discrete time t ∈ Z, the bead’s
                                            distributed parties [7–9]. Could the memory required by         position is stochastically perturbed. This perturbation is
                                            a quantum machine that simulates dynamical processes            described by a real random variable X that is governed
                                            likewise scale much more favourably with precision?
                                               Here, we consider the simulation of a class of stochastic
                                            systems involving the dynamics of parameters that take                                               P(X=x)
                                            on real numbers. Classical simulation of such processes
                                                                                                                                           x
                                            digitally involves ‘coarse-graining’: the parameter at each
                                            point in time is approximated to n bits of precision at                               yt           yt+1=yt+x
                                            some memory cost that scales linearly with n. We con-
                                            struct quantum simulators the exhibit unbounded ad-               Figure 1: Cyclic random walk. At each time step, the
                                            vantage. The quantum simulator can exactly replicate                   system stochastically hops from state y t ∈ [0, 1) to
                                                                                                               y t+1 = frac[y t + x]. As x is chosen according to the real
                                                                                                             random variable X, the current value of the system is itself
                                            ∗ ajpgarner@nus.edu.sg                                            described by a sequence of real random variables {Y t }t∈Z
                                            † gumile@ntu.edu.sg                                                            that satisfy Y t+1 = frac[Y t + X].
                                                                                                                                           2

by a continuous probability density function P (X), such                  Classical simulation costs scale with precision.
that                                                                   We can formally describe simulators using the tools of
                                                                       computational mechanics [11–14]. A simulator of a pro-
                    Y t+1 = frac[Y t + X],                      (1)    cess is a device whose future output behaviour condi-
 where Y t represents the random variable that governs the             tioned on any particular past should be statistically in-
 location of the bead at time t, and frac[y] = y − byc ∈               distinguishable to the process itself. Specifically, let the
 [0, 1) denotes the fractional part of y, such that posi-              state of the simulator at each time be st , such that at the
 tions differing only by whole rotations around the ring               subsequent time-step it can output y t+1 and transition
 are equivalent. We refer to P (X) as the shift function,              to state st+1 . For this device to be a statistically faithful
 and assume the process is stationary, in the sense that               simulator of a process P(Y~, Y~ ), we require that:
 P (X) has no explicit dependence on t, and rotationally                    1. For each specific past y~ at each time t, we can de-
 symmetric such that X has no dependence on the cur-                           terministically configure the device using a function
 rent value of Y t . This same formalism describes a diverse                   f into some state s = f (y),
                                                                                                        ~ such that it will produce
 range of systems undergoing cyclic random walks, such as                                                            ~ = ~y | Y~ = y).
                                                                               future outputs ~y with probability P(Y              ~
 the azimuthal motion of gas molecules diffusing in an an-
 nular tube, or the position of a single electron travelling                2. If a simulator is in state st = f (y)
                                                                                                                  ~ at time t, and
 through an electric circuit with constant resistance.                         outputs y t in the subsequent time-step, its internal
    We capture the dynamics of Y formally using the                            state must then transition to st+1 = f (yy
                                                                                                                        ~ t ).
 framework for describing stochastic processes. In general,
 a stochastic process P is characterized by a bi-infinite se-             The first condition ensures the simulator can be ini-
 quence of random variables {Y t }t , that governs its value           tialized to simulate desired conditional future statistics;
 at each discrete time t ∈ Z. For convenience, we often se-            the second that a correctly initialized simulator continues
 gregate past and future values, such that Y~ = . . . Y −1 Y 0         to exhibit statistically correct statistics at every time-
 and Y ~ = Y 1 Y 2 . . . respectively govern the values in the         step. The memory cost of the simulator corresponds
 past and future with respect to time t = 0. The cyc-                  to the storage requirements of this internal state. This
 lic random walk above is then entirely captured by the                cost is bounded from below by the information entropy
                                                                       of the random variable S := f (Y ). In the asymptotic
 joint probability distribution P(Y~, Y  ~ ) such that for any
                                                                       limit of many independent identically distributed cop-
 instance of the process with past values y,   ~ future values
                                             ~ = ~y | Y~ = y).         ies of the simulator, this bound is tight as the ensemble
~y will be observed with probability P(Y                   ~           of states may be compressed (such as by Shannon’s
    Here, we consider the simulations of the above process             noiseless encoding theorem [22], or Schumacher compres-
 to ever increasing precision. We adopt a natural tech-                sion [23, 24]). Physically a simulator can be viewed as
 nique of discretizing a continuous process, by introducing            a communication channel in time: it represents the ex-
 a family of stochastic processes {Pn } that describe dis-             act object Alice must give to Bob at each time-step that
 crete approximations of this process, where in each the               captures sufficient past information for Bob to replicate
 position of bead is represented to n bits of precision by             the processes conditional future behaviour. f is known
 a n-digit binary number. This is done by limiting y to a              as the encoding function, which describes how the past is
 discrete set of N = 2n equally–spaced values, yj = j/N                encoded within the channel.
 (for j = 0 to N − 1). At each time-step, the probabil-                   This memory cost of the provably-optimal classical
 ity that a bead in discrete location yj transitions to yk ,           simulator – known as the statistical complexity Cµ – is
 is given by the probability pjk that a bead initially at              extensively studied in complexity science [11]. This value
 yj will transition to any value of y whose n bit binary               captures the absolute minimum memory any classical
 representation is yk . That is                                        simulator of a process must store, and thus is a prom-
              pkj = P Y t+1 = y ∈ Ik | Y t = yj
                                                   
                                                               (2)     inent quantifier of a process’s structure and complexity2
                                                                       (e.g. [14–21]). Such an optimal simulator can be expli-
                                1                                      citly constructed, and corresponds to the simulator that
where Ik = {y : |y − yk | < 2N    } represents the interval
on the ring that is ‘rounded to’ yk . This results in a                stores in its internal memory the causal states of the pro-
Markovian stochastic process that emits a symbol from                  cess [11, 12]: defined by an encoding function f such that
the finite alphabet {yk } at each time-step, whose dynam-              f (y)                             ~ | Y~ = y)
                                                                           ~ = f (y~0 ) if and only if P(Y        ~ = P(Y~ | Y~ = y~0 )
ics are governed by the stochastic matrix with elements                (i.e. the conditional futures of y~ and y~0 coincide).
pjk . As n → ∞, the statistics of Pn approach that of P;
at the potential cost of tracking more information1 .
                                                                       2    The statistical complexity is distinct from algorithmic inform-
                                                                           ation (Kolmogorov–Chaitin complexity). Statistical complexity
1 An alternative discretization is to calculate the transition prob-       is, as the name would imply, intrinsically statistical – concerned
  abilities by assuming the initial value of y t is uniformly dis-         with the replication of the statistical behaviour of a process;
  tributed in Ij . This yields asymptotically identical statistics         whereas algorithmic information relates to the compressibility
  as N → ∞, and does not change the results of this article.               of an exact string [25].
                                                                                                                                3

   In our cyclic random walks, each Pn is a first-order               (as all quantum states occur with equiprobability). Thus
Markov process: the statistics of future outcomes depend              the memory required to store these states is given by
only on the most recent value of Y t . When this example              thePvon Neumann entropy given HQ := − Tr (ρ log ρ) =
is discretized, the causal states are thus typically in one-          − k λk log λk , where λk are the eigenvalues of ρ. The
to-one correspondence with the 2n discrete values that                key improvement here is that {|Sj i} are not in general
Y cann take3 . That is, Pn has 2n causal states, labelled             mutually orthogonal, and thus HQ is generally less than
{sj }2j=0−1 , where sj corresponds to the set of pasts ending         Cµ . Nevertheless a quantum circuit (outlined in figure 2
in Y 0 = yj . When the simulator has been running for                 – with details in the Technical Appendix) acting on these
a sufficiently long time, the probability distribution over           quantum states will produce statistically identical out-
the internal memory converges on P(S = si ) = N1 for each             puts to the classical simulator.
i – its steady state, in which all causal states occur with              The von Neumann entropy of a quantum state is equal
equiprobability. Thus, the classical statistical complexity           to the Shannon entropy of the outcome statistics of a
                                                                      projective measurement on that state, minimized over
                            Cµ = n,                            (3)    all choices of projective measurement. This minimization
                                                                      corresponds to a measurement in the basis in which the
scales linearly with the precision.                                   state’s density matrix is diagonal. A classical probability
  Quantum simulators are memory–efficient. It                         distribution maps onto a mixed quantum state, diagonal
has recently been shown that quantum processors have                  in a fixed basis. As such, the stationary state of the clas-
the capability to simulate stochastic processes with less             sical simulator can be assigned a quantum state, whose
memory than is classically possible [26–30]. Here, we                 von Neumann entropy is exactly that distribution’s Shan-
construct an explicit quantum simulator for the cyclic                non entropy. This allows us to compare the entropic cost
random walk. Instead of storing each causal state si                  of the classical and quantum machines’ memories on an
directly, our quantum simulator stores a corresponding                equal footing.
quantum state                                                            Unbounded advantage of quantum memory.
                               N −1
                                                                      We now come to the main claim of our paper: there are
                               X      √                               stochastic processes that can be simulated to infinite pre-
                     |Sj i =              pkj |ki ,            (4)
                                                                      cision using a finite amount of quantum memory.
                               k=0
                                                                         Explicitly, we show that for certain cyclic processes,
where {|ki} forms an orthonormal basis.                               the quantum ensemble state’s eigenvalues {λk }k=0...N −1
                                                                                         PN −1
                                                                      satisfy limN →∞ k=0 −λk log λk = Ω for some finite
                                                                      value Ω. Our result relies on first observing that the
                                                                      eigenvalues λk can be directly related to transition prob-
                                                                      abilities {pjk } via the relation

                                                                                            1 √  √         
                                                                                   λk =       F pj0 F p(N −j)0 ,              (5)
                                                                                            N
                                                                      where F denotes the discrete Fourier transform, F(xj ) =
    Figure 2: Circuit for memory-efficient quantum
                                                                      PN −1             −2πi
                                                                                              
                                                    ~ | y)               j=0 xj exp      N jk . (The proof relies on invoking the
     simulator. The above circuit samples P(Y           ~ when        cyclic symmetry of the process – and hence of the trans-
    supplied with the appropriate quantum state S t that
                                                                      ition probabilities – and is explicitly derived in the Tech-
 encodes the past. At t = 0, an ancillary system, initialized
in state |S0 i, is fed into the simulator. A controlled unitary
                                                                      nical Appendix). The spread pj0 (as a function of j) is an
 is then enacted such that U : |ji |S0 i → |ji |Sj i for each j.      indicator of how quickly a particle diffuses in the random
    The state of the ancillary system and memory are then             walk. Thus, the Fourier-like relation between pj0 and λk
     coherently swapped, and the ancillary system is then             indicates an inverse relationship between the amount of
   emitted as output. Measurement of the ancillary system             diffusion in the cyclic process and the spread of eigenval-
  then correct samples Y  ~ 1 . Iteration of this procedure then      ues. The greater the variance of X, the more quickly a
  generates output behaviour statistical identical to that of         particle diffuses, and the smaller the spread of λk – res-
                       the original process.                          ulting in a reduced quantum memory requirement. We
                                                                      now show that for some natural examples, this reduction
  The stationary state of the quantum simulator
                                          P is then                   is sufficiently large that Hq remains bounded for all n (as
given by the quantum ensemble state ρ = N1 j |Sj ih Sj |              illustrated in figure 3).
                                                                         Example 1: Gaussian noise. A cyclic process rotat-
                                                                      ing at a constant rate subject to Gaussian noise has a
                                                                      shift function
                                                                                  given by a Gaussian distribution Gµ,σ (x) =
3 There are exceptions, such as when P (x) = 1 for x ∈ [0, 1), and                          2

  the system jumps to a completely random point at each time-
                                                                       √1
                                                                      σ 2π
                                                                           exp   − (x−µ)
                                                                                     2σ 2       about mean µ with standard devi-
  step; here there is only one causal state for all N , because the   ation σ. Here, µ characterises the average velocity (in
  current position no longer affects the future outcomes at all.      terms of the variable’s mean displacement per time-step),
                                                                                                                           4


              (a) Quantum memory cost for process with             (b) Quantum memory cost for process with
                                                 x2                                                1
                                                   
                                      1                               uniform white noise P (x) =    when
              Gaussian noise P (x) = √ exp − 2 .                                                  2∆
                                    σ 2π        2σ
                                                                      x ∈ [−∆, ∆] and P (x) = 0 elsewhere.


                  (c) Gaussian noise function σ = 0.01,              (d) Uniform noise function ∆ = 0.01,
            demonstrating unbounded difference in classical      demonstrating unbounded difference in classical
            and quantum memory requirements. The dotted               and quantum memory requirements.
           line shows the analytic upper bound from eq. (6).

  Figure 3: Bounded quantum memory costs for unbounded precision. The memory required to simulate a cyclic
random walk is plotted against the precision N for the Gaussian and top-hat shift functions. In both examples, the quantum
simulator has an unbounded memory advantage – the classical cost scales as log N whilst the quantum cost converges upon a
    constant value. The more rapidly the shift function diffuses X, the lower the limiting quantum memory requirement.


and σ the size of the fluctuations. When µ = 0, this pro-        the precision n = log N increases, the sum
cess corresponds to Gaussian diffusion. For our analysis,               P N2 −1
                                                                 limN →∞ k=−   N λk log λk converges on a finite value,
we take σ  1 and thus ignore fluctuations where the                             2

particle travels more than a complete loop around the            bounded (in bits) by
ring in a single time-step (a value of σ = 0.1 ensures that                         1         √             √
such events are less likely than one part in a million.)                 HQ ≤           − 1 + 4 2πσ log2 2 2πσ            (6)
                                                                                 2 ln 2
   As can be seen in figures 3a and 3c, as the de-               Thus, for any fixed 0 < σ  1, the Gaussian random
sired precision increases, the memory cost of simu-              walk may be simulated to arbitrarily high precision us-
lating this process quickly converges onto a constant            ing a quantum simulator of bounded entropy. Moreover,
determined by the fluctuation strength σ; ultimately,            this also implies an unbounded divergence between the
infinite-precision simulation is possible using only a fi-       classical and the quantum statistical complexity [27, 31]
nite quantum memory. This behaviour may be under-                CQ , which is upper bounded by HQ .
stood analytically by seeing that for large N , the eigen-          Example 2: Uniform white noise. In the second ex-
values associated with the quantum simulator’s internal          ample, we consider a particle that is perturbed by uni-
memory are also given by samples from a Gaussian dis-            formly distributed noise. At each time-step, the particle
                                        N         N
                      1 (k) for k = −
tribution: λk = G0, 4πσ                 2 , . . . 2 − 1, where   can move anywhere in the range of µ±∆ from its current
for convenience we have cyclicly offset the label of the         position with uniform probability, where ∆ < 21 . Again,
eigenvalues’ indices by N (proof in Technical Appendix).         µ characterises the average velocity, and here ∆ the size
This demonstrates that increasing σ tightens the spread          of the fluctuations. The associated shift function is a top-
of eigenvalues, and thus reduces the memory requirement          hat function, that has a uniform value of 2∆1
                                                                                                                in the range
for the quantum simulator.                                       x ∈ [µ − ∆, µ + ∆] and 0 everywhere else.
   In the Technical Appendix, we prove that as
                                                                                                                             5

   The entropy of the quantum simulator, Hq is plotted              nearly-orthogonal quantum states at some memory cost.
for various precision in figures 3b and 3d. We see that             On the other hand, when two points are initially closer
for any fixed ∆ > 0, the quantum memory required by                 than the standard deviation scale, the probability that
our simulator converges to a bounded value. As in the               they could be distinguished by their future behaviour di-
Gaussian scenario, the quantum simulator can replicate              minishes, and they may be represented by increasingly
a classical simulation to any given precision using with            overlapping quantum states. In this regime, a fixed finite
finite entropy. In the Technical Appendix, we prove this            memory can accommodate any desired precision.
analytically. We show that as N → ∞, the entropy re-                   We gain further insight into the origins of quantum
mains finite, and is bounded above by HQ ≤ 1.894     √
                                                       ∆
                                                         +3.067.    advantage by considering the cases where it does not ap-
In particular, for large N , the eigenvalues of the relev-          pear: σ = 0 and ∆ = 0. In both these cases, the shift
ant ensemble state obey λk = 2∆ sinc2 (2k∆) for k =                 function is a Dirac delta distribution. As such, no mat-
− N2 , . . . N2 − 1, where sinc(x) is the normalized sinc func-     ter how high the precision, by observing the future out-
                       1                                            puts, it will always be possible to distinguish whether
tion, sinc(x) := πx      sin(πx). Larger values ∆ will result
in a smaller spread of eigenvalues, and result is smal-             the system came from some site sj or its neighbour sj+1 ;
ler Hq . For any given ∆ > 0 the entropy is finite in               the dynamics of the system are wholly reversible. If sj
the limit N → ∞. This establishes a second natural                  always transitions to sk and sj+1 always to sk+1 , be-
example where the quantum simulator can demonstrate                 ing able to distinguish between these two sites is crucial
an unbounded memory advantage over its best possible                to produce the correct statistical behaviour, even as the
classical counterpart.                                              precision increases. As such, the quantum simulator can-
   The origin of quantum advantage. The source                      not tolerate overlap between the states |sj i and |sj+1 i,
of classical inefficiency can be understood by consider-            and must store them orthogonally (allowing them to be
ing dynamics on causal states. Consider two instances               distinguished). In this scenario, the quantum simulator
of Pn , one where Y 0 = yj , and the other where Y 0 =              cannot demonstrate any advantage in memory cost over
yj+1 . As their conditional future statistics differ [that          its classical analogue.
is, P(X  ~ | Y 0 = yj ) 6= P(X~ | Y 0 = yj+1 )], a classical sim-      Discussion and outlook. In this article, we presen-
ulator must be configured differently for each instance             ted a task in which quantum mechanics has an unboun-
(corresponding to being initialized in one of two different         ded memory advantage over the most memory-efficient
causal states, sj or sj+1 ). Nevertheless, there is finite          classical alternative: the simulation of a classical cyclic
probability that at the next time-step, both instances of           stochastic process. We found that the classical simu-
the process emit the same output (up to precision n).               lator has a memory requirement that scales linearly with
Should this happen, we would not be able to use the cur-            the precision required, while the quantum simulator’s re-
rent state of the machine to determine the causal state             quirement may be bounded by a finite value, even at
it was in at the previous time. That is, there is some              arbitrarily-high fixed precision. This establishes a rare
probability that the distinction between sj and sj+1 will           scenario where the scaling advantage of quantum pro-
never be reflected in the future statistics of the process          cessing can be provably established.
– a phenomenon known as crypticity [28, 32]. As n in-                  This finding leads to a number of natural open ques-
creases, this occurs with greater likelihood (tending to            tions – the first being of generality. Certainly, the ex-
unit probability as n → ∞), and thus proportionally                 amples presented are sufficiently simple that such diver-
more information is wasted. Ultimately, in the limit of             gences are unlikely to be merely a mathematical oddity.
high precision, a vanishingly small proportion of the in-           The unbounded quantum advantage relies on {Pn } hav-
formation stored in the classical memory is pertinent to            ing two properties: (a) the number of causal states
the statistical behaviour of the process’s future.                  grows with n, and (b) the conditional future statistics
   Quantum simulators compensate for this waste by                  P(X ~ | S = si ) between different causal states converges
mapping these causal states to non-orthogonal quantum               sufficient quickly with n. If these conditions can be form-
states. The quantum state (eq. (4)) associated with                 alized, we may be able to establish similar divergences in
neighbouring causal states (|Sj i and |Sj+1 i) also be-             much more general scenarios, such as the simulation of
come increasingly similar with increasing n – resulting             non-Markovian or non-cyclic processes. Beyond von Neu-
in progressively greater savings. Consider the Gaussian             mann entropy, it would be interesting if similar scaling
scenerio, where Hq is bounded by equation (6). For small            can be found for other metrics of memory cost, such as
σ, the memory cost scales as − log2 σ, such that halving            the dimension – namely, whether there is an encoding
the variance of fluctuations at each time-step adds one             that allows for simulation to arbitrary precision using
bit to the memory cost of the quantum simulator. The                a Hilbert space of bounded dimension. Meanwhile the
standard deviation of the shift function has set an effect-         inefficiency of classical simulators have show to directly
ive length scale over which the system must be simulated            results in unavoidable increased heat dissipation [33–35].
classically. The statistical behaviour of future outputs            This hints that quantum processing may allow significant
from two systems that are initially prepared in points              energetic savings for stochastic simulation, especially for
separated by more than one standard deviation are typic-            systems that become increasingly difficult to simulate as
ally distinguishable, and so these points must be stored as         they scale in size.
                                                                                                                                         6

   On a foundational level, the statistical complexity is             as the time-independent cyclic random walks described
often regarded as a fundamental measure of a process’s                in this article), this distribution has no explicit time de-
intrinsic structure – the rationale being that it quantifies          pendence, so we omit the superscript t.
the minimal amount of information about a process’s his-                  A faithful simulator of process P is a machine (or pro-
tory that must be recorded to allow for predictions about             gram) that, having been initialized in accordance with
that process’s future behaviour. The measure has been                 the observation of past y~t , then generates a series of out-
applied to understand structure within diverse complex                puts ~yt according to the distribution P(Y         ~ t = ~y t | Y~t =
settings: from the dynamics of neurons [15] and the stock              t                                             t
                                                                     y~ ). Since storing an infinite string y~ may require an
market [19], to quantifying self-organization [16], among             unbounded amount of memory, one instead configures
other examples [17, 18, 20, 21]. The discovery of more                the internal state of the simulator s (over configuration
efficient quantum models has led to the idea that the                 space S) according to some function s = f (y),          ~ satisfy-
complexity of a system depends on what sort of inform-                        ~ t = ~y t | S = s) = P(Y   ~ t = ~y t | Y~t = y~t ), where
                                                                      ing P(Y
ation we use to observe it [27, 31]. In this context, our
                                                                      S = f (Y~) is the random variable describing the internal
results establish a family of processes that can look ever
                                                                      state of the simulator (formed by applying the function f
more complex classically, but remain simple quantum-
mechanically. It would fascinating to see if divergences              on each variate of Y~). Moreover, once initiated into state
between quantum and classical complexities can be found               st , when the simulator outputs y t in the subsequent time-
in existing studies, such as the examples above. Could                step, its internal state must then transition to the state
it be that these systems appear complex classically –                 st+1 = f (yy~ t ) (where yy ~ t indicates the concatenation of
but look much simpler when viewed through the lens of                 y t to the end of string y). ~
quantum theory?                                                           The memory cost of such a simulator is
                                                                      given
                                                                         P by the information entropy of S, H(S) =
                                                                      − si ∈S P(S = si ) log P(S = si ). The function f that
                ACKNOWLEDGEMENTS                                      minimizes this classically corresponds to identifying the
                                                                      causal state of a particular past [11, 12], defined by the
   We thank James Crutchfield, Thomas Elliott,                        equivalence relationship: y~ ∼ y~0 for pasts y~ and y~0 if
David Garner, Peter Grassberger, Jan-Åke Larsson,                    and only if P(Y   ~ = ~y | X~t = y)~ = P(Y ~ = ~y | X~t = y~0 ) for
and Chengran Yang for helpful comments and discus-                    all possible future values ~y ∈ Y    ~ . The causal states are
sions. We gratefully acknowledge funding from the John                unique for any given process, and so their entropy H(S)
Templeton Foundation Grant 53914 “Occam’s Quantum                     is a property of the process itself known as its statistical
Mechanical Razor: Can Quantum theory admit the                        complexity Cµ , capturing the intuition that a more
Simplest Understanding of Reality?”; the Foundational                 complex process requires more memory to simulate.
Questions Institute; the Ministry of Education in Singa-                  For Markovian processes, such as discussed in this art-
pore, the Academic Research Fund Tier 3 MOE2012-                      icle, the number of causal states required is equal to the
T3-1-009; and the the National Research Foundation of                 number of unique rows in the stochastic matrix describ-
Singapore (Award Nos. NRF–NRFF2016–02 and NRF–                        ing the evolution. When these rows are generated by
CRP14-2014-02).                                                       the discretization of a continuous process into N divi-
                                                                      sions – such as when they are derived from the cyclic
                                                                      walk’s shift function P (X) – the number of states will be
                TECHNICAL APPENDIX                                    equal to N , except for very specific (e.g. pathologically
                                                                      fractal) choices of P (X) and N . Since by symmetry the
   Classical costs from computational mechanics.                      probability of the simulator being in any particular state
We here present some minimal details from the math-                   is equal, the classical memory cost of a simulator hence
ematical framework of computational mechanics [11–14]                 scales with the number of sites as log N , or linearly with
to substantiate the claim that the classical simulator’s              the precision n = log2 N .
minimal memory cost is equal to the precision log N .                     Details of the quantum circuit in figure 2. Let
   In computational mechanics, the evolution of a dy-                 us consider figure 2 in more depth (see also [26]). The
namical property (over domain Y) is characterised by a                circuit consists of one persistent internal memory state,
discrete-time stochastic process P, written as bi-infinite            and an “output tape”—a line of quantum states, which
sequence of random variables {Y t }t∈Z , where each ran-              are fed into the system one at a time. Suppose each
dom variable Y t governs the value y t ∈ Y of the dynam-              state on the output tape is initialized into some arbit-
ical property at time t. The statistical behaviour of a               rary state |φi. For any two quantum states |xi and |yi in
process may be represented in a causal manner by writing              the same Hilbert space, it is always possible to construct
it as the conditional probability distribution P(Y     ~t | Y~t ),
       ~ t     t+1 t+2
                                                                      a unitary transformation V such     P that V |xi = |yi. This
where Y = Y       Y    . . . is the infinite string of random         will be of the form |y ih x| + i |yi0 ih x0i | where |x0i i are
variables occuring after time t, and Y~t = . . . Y t−1 Y t is         states orthogonal to each other and to |xi, and |yi0 i are
the infinite string of random variables occuring before               states orthogonal to each other and to |yi. Thus, in the
(and including) time t. For stationary processes (such                joint Hilbert space HN ⊗ HN of two quantum systems of
                                                                                                                                                   7

dimension N , it is possible to build a “controlled” unit-                     causal state S t then outputted string yi1 . . . yiM , and a
ary operation U containing the elements |j ih j| ⊗ |ψj ih φ|                   new causal state directly set according to this output se-
for every |ψj i in an arbitrary (generally non-orthogonal)                     quence. Measuring the string of output tape subsystems
set of states {ψj }j=0...(N −1) . [Note: the orthogonality of                  thus still ensures that the internal memory state collapses
{|ji} allows us to pairwise use the above construction for                     into the correct causal state S t+M , conditional on the
each |ψj i.]                                                                   string observed.
   For a Markovian process discretized such that the                              In the first mode of operation (as drawn in figure 2),
stochastic matrix with elements pjk describes its evol-                        only one ancillary quantum system is required, as it can
ution, the above prescription supplies the unitary oper-                       be reset and re-used between timesteps (the output tape
ation required for our quantum simulator when we set                           carries away classical information only). In the second
                       PN −1 √
each |ψj i = |Sj i = k=0 pkj |ki, as per eq. (4) (states                       mode, the quantum output explicitly fulfils the role of the
{|ki} and {|ji} are in the same basis).                                        ancillary system, and a fresh ancillary system (provided
   We may now evaluate the action of a single time-step                        by the “blank” output tape set to some fixed choice of
(grey dashed box within figure 2). Here, the joint Hil-                        pure quantum state) is inserted at each time step. In
bert space corresponds to that of the internal memory to-                      both modes, the ancillary system does not need to persist
gether with the output tape. In the figure, we explicitly                      between time steps in order for the simulator to continue
wrote the initial state of the output tape as |φi = |S0 i,                     producing statistically correct outputs. As such, in both
but this is arbitrary; any |φi could be made into |S0 i by                     cases, it is the von Neumann entropy − Tr ρ log ρ of the
acting on it first with a unitary gate containing |S0 ih φ|.                   first subsystem, which remains within the simulator at all
At the start of a time step, the internal memory is in                         times, that we consider to be the internal memory cost.
                          PN −1 √                                                 Derivation of discrete eigenspectrum.                 The
state |S t i = |Sj i =      k=0     pkj |ki. Hence, the joint
state of the memory and output tape is initially |Sj i⊗|φi.                    quantum machine state corresponding to the    P √system   be-
After the controlled unitary is applied,                                       ing in classical state α is given as |Sα i = β pβα |βi.
                                               P the
                                                  √
                                                      memory and
tape will be in the entangled state k pkj |ki ⊗ |Sk i.                         Assuming {pβα }βα is simply connected, theP   quantum ma-
Applying a coherent swap operation (i.e. exchanging the                        chine will reach a stationary state ρ = N1 α |Sα ih Sα |.
labels                                                                         Rather than directly calculating the entropy of ρ, we
P √ of the Hilbert spaces) will take this joint state to
   k   pk j |Sk i ⊗ |ki – the state of the system at the end                   can instead evaluate the entropy of the associated Gram
of the grey box.                                                               matrix g, whose elements gαβ are given by the overlaps
                                                                                1             4
   The tape system is then ejected from the simulator. If                      N hSα |Sβ i. The circular symmetry of the cyclic random
one were to measure this state in the {|ki} basis, one pro-                    walk ensures that the discretized transition probabilities
jects onto state |ki with probability pkj , and hence the                      satisfy pαβ = p(α+k)(β+k) (that is, the transition prob-
output statistics of this measurement match that of the                        abilities depend only on differences between indices). It
process being simulated. Moreover, after measuring, due                        hence follows that the Gram matrix associated with ρ is
to the entanglement, we know that when |ki is measured,                        circulant [36]. Since all rows can be derived by cyclic
the internal memory must be in state |Sk i, which is ex-                       permutation of the top row, we shall drop one index and
actly the quantum state that would have been prepared                          write the top row as gα = g0α . P    The eigenvalues of the
if we had mapping the output statistics onto a classical                       Gram matrix are given by λk = α gα exp − 2πi      N αk for
causal state and then prepared |Sk i directly. Hence, the                      k = 0, . . . , N − 1, which can immediately be recognized
quantum circuit in figure 2 can function as a discretized                      as the discrete Fourier transform (DFT) of {gα }α , which
simulator for a Markovian process.                                             we denote as F(g0α ).                         P √
   However, it is very important to note that there is no                         Moreover, the inner product hS0 |Sj i = α pα0 pαj ,
                                                                                                                 √ √
need whatsoever to measure the output tape |ki for the                         has the form of a convolution p ∗ q, where we have
quantum simulator to continue functioning. If it suits                         rewritten pαj as q0(α−j) such that q is the N -periodic
one’s purpose to store the output states in quantum                            extension of the reflection of p; q0j = p(N −j)0 and q0j =
memory (e.g. to perform further quantum information                            q0(j+N ) . We may then apply the circular convolution
processing on the output data), then the quantum sim-                          theorem to find the eigenvalues of g, and therefore of ρ:
ulator still functions correctly. In this mode of opera-                                              1 √  √         
tion, the measurements can be omitted from figure 2,                                           λk =     F pj0 F p(N −j)0 .                       (8)
and after M steps, the simulator would have produced                                                  N
the entangled state                                                            These eigenvalues can hence be found efficiently by nu-
          X Xq                                                                 merical algorithms, such as the fast-Fourier transform.
   |Φi =       ...       P (Y t = yi1 , . . . Y t+M = yiM |S t )
          i1         iM
                   t+M
               S         (S t , yi1 , . . . yiM ) ⊗ |yi1 i ⊗ . . . |yy+M i     4    This works
                                                                                          P 1by constructing a fictitious purification of ρ, given
                                                                         (7)       |Ψi =     i
                                                                                               √   |Si i ⊗ |ii (where {|ii}i is an orthonormal basis)
                                                                                                 N
                                                                                   such that TrB |Ψ ih Ψ| = ρ and TrA |Ψ ih Ψ| = g. Since the
where S t+M (S t , yi1 , . . . yiM ) is the quantum state that                     von Neumann entropy of pure state |Ψi is 0, it follows from
would have been prepared if the system was originally in                           triangle inequalities that H(ρ) = H(g).
                                                                                                                                      8

   Example: Dirac-delta shift function. Let the shift func-         where we have used the convolution theorem in the final
tion be P (x) = δ(x − x0 ) for some x0 ∈ [0, 1). It                 step. The periodic sampling of g(x) causes the Fourier
can be seen that all pj0 = 0 except for the one at in-              transform to be periodic with period N (a phenomenon
dex j 0 that incorporates the delta peak where pj 0 0 = 1.        known as aliasing), such that λk = λk+N ; the convolution
                                j0                                  with a delta train effectively makes λk a periodic sum of
                                                        
Hence, F(pj0 ) = exp −2πi N        k and F p(N −j)0 =
                                                                    F(gonce (x)). This periodicity allows us the freedom to
          (N −j 0 )
exp(−2πi N k), and so λk = N1 for all k. Thus,                      choose a convenient range of k. In this article, we will
the von Neumann entropy of the simulator’s memory is                typically use − N2 to N2 − 1. If F(gonce (x)) ≈ 0 outside
log N .                                                             the chosen range, then we can approximate
   Example: Uniform shift function. Consider the uni-
                                                                                        λk ≈ [F(gonce (x))] (k).                    (11)
form shift function P (x)  = 1√ for x ∈ [0, 1). Here,
                       √
pj0 = N1 , and so F pj0 = N for k = 0 and 0 for                       Asymptotic limit of eigenvalues. For large N , we
all other k. As such, we find that the eigenvalue λ0 = 1,           can derive an expression for λk in terms of the probability
and all other eigenvalues λ1 = . . . λN −1 = 0, and hence           density function P (x). We substitute pα0 with N1 P ( Nα
                                                                                                                              ),
the entropy of the Gram matrix is zero, for all values              which for Riemann-integrable P (x) is an arbitrarily good
of N .                                                              approximation in the limit of N → ∞. Similarly, we may
   Sampling Fourier transforms. It will be useful                   substitute pαj with N1 P ◦ (− j−α             ◦
                                                                                                   N ), where P (x) denotes
to show an auxiliary relationship between discrete and                                      5
                                                                    the 1-periodic extension of P (x). Taking the limit of the
continuous Fourier transforms. Let g(x) be a func-                  Riemann sum for a product of two functions, we then see
tion over the range x ∈ [0, 1] that is sampled at N
                                                       n                                         N −1
equally spaced points with values given by gn = g( N     )                                       X      √
for n = 0 .P  . . N − 1. We can construct a function                    lim hS0 |Sj i = lim                pα0 pαj
                 N −1      n                                           N →∞               N →∞
gcomb (x) =      n=0 δ x − N g(x), whose Fourier trans-
                                                                                                 α=0
form is                                                                                          N −1r
                                                                                                 X 1       α       j−α
                                                                                        = lim          P ( )P ◦ (−     )
                  Z ∞         N −1                                                        N →∞     N       N        N
                              X       n                                                      α=0
F(gcomb (x)) =           dx       δ x−    g(x) exp (−2πikx)                               Z 1 p
                   −∞         n=0
                                       N                                                =    dx P (x)P ◦ (y − x),      (12)
                  N −1       n                                                            0
                  X                    n 
              =          g      exp −2πi k ,                  (9)   where y =      j
                              N         N                                          N.  Moreover, since P only has support
                  n=0
                                                                    in [0, 1), we can rewrite the integral limits from p −∞
which when evaluated at integer k is exactly the DFT of             to  ∞,  and  conclude   that lim N →∞  hS |S
                                                                                                             0 j  i = [ P (x) ∗
                                                                                                                 N −1
                                                                    p                                     1
                                                                        ◦
                                                                       P (−x)](y) sampled at y = 0, N , . . . N . Thus by
the samples {gn }, which we write as {λk }.
   If g is periodic, it is always possible to offset the posi-      treating gj as samples from a function g(y = Nj ) at dis-
tion of the sample window of g by some integer c without            crete intervals of N1 , we find that gj ≈ N1 g(y = Nj ) for
changing the values of g’s DFT. For the functions we con-           large N , and hence
sider in this article, it is more convenient to start at − N2 ,
since typically g− N , g N → 0 and g0 = 1. Moreover,                                 j      hp         p          i
                      2    2                                                  g(y = ) =        P (x) ∗ P ◦ (−x) (y) .      (13)
once the sample window has been set, the values of g(x)                             N
outside this window can not affect λk , since they do not             As shown                    the eigenvalues {λk} are given
                                                                               in eq. (10), P      ∞
feature in the sum. Thus, instead of considering sampling           by λk = F(gonce (x)) ∗ m=−∞ δ(k − mN ) evaluated
g(x) across a finite window, we can consider an infinite            at integers k = 0, 1, . . . N − 1, where gonce (y) = g(y) over
delta train sampled at the same intervals, but across a             an (arbitrary) single period of g(y) and takes the value
function gonce (x) where gonce (x) = g(x) inside the range          zero elsewhere. Due to the periodic summation, it can
of the sample window (i.e. [− 12 , 12 ) for the window used         be seen also that λk = λk+N , and so we are also free
in this article) and gonce (x) = 0 outside this range. Here         to choose the most convenient range for k, which will
                                      N
                                                                   typically be from − N2 to N2 − 1. If [F(gonce )](k) ≈ 0
                                      2
                                      X           n                when |k| > N2 , then the approximation
  λk = F(gcomb (x)) = F g(x)                δ(x − )
                                           N
                                                  N                                                            N      N
                                     n=− 2
                                                                        λk ≈ [F(gonce )](k)      for k = −       ,...   −1          (14)
                                            ∞
                                                         !                                                     2      2
                                            X    n
                         = F gonce (x)      δ(x − )                 is reasonable. This assumption amounts taking enough
                                       n=−∞
                                                 N
                                                                    samples of g(x) to admit a faithful reconstruction of g(x)
                                             ∞
                                             X
                         = F(gonce (x)) ∗          δ(k − mN ),
                                            m=−∞
                                                             (10)   5 Equivalent to wrapping x to [0, 1) before evaluating P (x).
                                                                                                                                         9

under the Nyquist–Shannon theorem [37]. This holds                           Hence, we see that choosing Gaussian transfer func-
true for the examples we shall now consider, where we                     tion with standard deviation σ  1 corresponds to a
                                                                                                                                     1
will ultimately take large values of N .                                  spectrum of eigenvalues with standard deviation 4πσ           .
   Example 1: Gaussian noise. Suppose the shift                              Upper bound on quantum memory cost. We now
function of the particle is given bya Gaussian distribu-                demonstrateP that the entropy of such a system, given
                                    (x−µ)2                                H     =  −    k λk log2 λk , is finite by bounding it from
                      1
tion Gµ,σ (x) = σ√2π exp − 2σ2              about µ with stand-             Q
                                                                          above. For convenience, we write λ(k) := G0, 4πσ         1 (k) =
ard deviation σ  1 such that we can ignore the prob-                                                    √
                                                                                       2                                          2 2
ability of the particle looping around the ring.p                         A exp −Bk where A = 2 2πσ and B = 8π σ , and
   Derivation of eigenvalues. We can express Gµ,σ (x)                     will perform the calculation in units of nats. Thus, con-
as a Gaussian:                                                            sider c(k) = −λ(k) ln λ(k), explicitly

                                                                                     c(k) = A exp −Bk 2 Bk 2 − ln A .
                                                                                                                            
                                         (x − µ)2                                                                                      (19)
q                                                  
                 − 12       − 14
   Gµ,σ (x) = σ (2π) exp −                    2
                                           4σ                                         dc
                                                                                                                                       
                                                                         By setting dk    = 2ABk exp −Bk 2 −Bk 2 + ln A + 1 =
                          1 √    √ −1                                 2
                                                          
                 1                              − 1          (x −  µ)
            = σ 2 (2π) 4 2( 2σ) (2π) 2 exp − √                            0, we find that c(k) has stationary points at k = 0, ±∞
                                                             2( 2σ)2 and when
                 1    1       1
            = σ 2 2 2 (2π) 4 Gµ,√2σ (x).                        (15)                   r                  s       √       
                                                                                           ln A + 1          ln 2 2πσ + 1
                                                                                k= ±                = ±                         .      (20)
   It can be easily verified that gµ,σ (−x) = g−µ,σ (x).                                      B                   8π 2 σ 2
   We also note that F(gµ,σ (x)) is also Gaussian:
                                                                          When σ < 2e√1 2π ≈ 0.073, these last two solutions dis-
                                                 2 2
                                                      
   F(gµ,σ (x)) = exp (2πiµk) exp −2(πσ) k                                 appear, and since we are in the regime of σ  1, this
               1    1                                                     condition is satisfied. Hence, for small σ, c(k) monoton-
        = (2π) 2        exp (−2πiµk)                                      ically decreases from its maximum value at k = 0 for
                 2πσ                                               !      both positive and negative k. This allows us to apply
                                  1    1 −1                 k2
                         · (2π)− 2 (      ) exp −                2
                                                                          the Maclaurin–Cauchy integral bound (see e.g. [38]),
                                      2πσ                    1
                                                               
                                                         2 2πσ                 Z ∞              ∞                  Z ∞
                            1
               = (2π)− 2 σ −1 exp (−2πiµk) g0, 2πσ
                                                                                               X
                                                        1 (k)   (16)               c(k)dk ≤        c(k) ≤ c(m) +           c(k)dk,     (21)
                                                                               m             k=m                     m
                                                  2
  Likewise, we can express [Gµ,σ (x)] as a Gaussian:
                                                                          which holds for any monotonically decreasing region
                           
                              (x − µ)2
                                                                         [m, ∞) of a function c(k) (here, m = 0).
                       −1
[Gµ,σ (x)]2 = σ −2 (2π) exp −                                                Using known results for definite Gaussian integrals,
                                 σ2
                                                                      !    Z ∞               r          Z ∞                    r
         −1       − 12       − 12     σ         −1       (x − µ)2                −Bx2      1 π                 2 −Bx2        1   π
    =σ        (2π)       2          ( √ )−1 (2π) 2 exp −                       e      dx =         and        x e       dx =       3
                                                                                                                                     ,
                                       2                  2( √σ2 )2         0              2   B          0                  4   B
                                                                                                                                (22)
                  − 12         1
    = σ −1 (2π)          2− 2 Gµ, √σ2 (x).                       (17)     we evaluate
                                                                                   Z ∞                 r                r
                                                                                                     1    π               π
  Taken together (making sure to substitute in the cor-                                 c(k)dk = AB           − A  ln A
                                                                                                     4   B  3             B
rectly modified values of µ and σ), this allows us to                               0
                                                                                                   r                
provide an analytic solution for eq. (14) for Gaussian shift                                     A π 1
functions:                                                                                     =              − ln A
                                                                                                 2 B 2
                                                                                                              
        q           q                                                                        1 1
 λk = F     Gµ,σ (x) F       Gµ,σ (−x)                                                         =       − ln A .                 (23)
                                                                                                 2 2
        q           q               
    =F      gµ,σ (x) F      G−µ,σ (x)                                     Since c(0) = −A ln A, we find from equation (20) that
                                                                                  ∞                   
             1
    = 2σ(2π) 2 F Gµ,√2σ (x) F G−µ,√2σ (x)
                                                                                      X            1
                                                                                            c(k) ≤   − ln A − A ln A,
                       √                                                                           2
             1                                                                        k=m
    = 2σ(2π) 2 (2π)−1 ( 2σ)−2 exp (−2πiµk) exp (2πiµk)                                                      
                                                                                                 1     1
              · [G0, √1        (k)]2                                                            ≤ −       + A ln A.                   (24)
                     2   2πσ                                                                     4     2
             1        1             1    1
    = (2π)− 2 σ −1 ( √    )−1 (2π)− 2 2− 2 G0, 4πσ
                                                1 (k)                     To obtain a bound on HQ , we double the above since
                    2 2πσ
                                                                          c(k) is even, and multiply by ln12 to convert from nats to
    = G0, 4πσ
           1 (k).                                                (18)     bits (equivalently, change the base ln to log2 since ln x
                                                                                                                               ln 2 =
                                                                                                                                  10

                     1
log2 x): HQ ≤ 2 ln     2 − (1 + 2A) log2 A. In terms of the      In the region x > 0, we can expand
shift function’s standard deviation σ, this gives our result
                                                                           sin2 x
                                                                                                      
                               √            √                                            2
                                                                                                   x
                 1                                               c(x) = −2∆ 2      ln sin x − 2 ln √       .                 (30)
                                    
       HQ ≤           − 1 + 4 2πσ log2 2 2πσ.           (25)                 x                       2∆
              2 ln 2
   In the limit of small σ, the leading term of the entropy    The function −y ln y has a maximum value of 1e at y = e,
thus scales with − log2 σ, such that halving the width         and so we can upper bound c(x) by making the substi-
of the standard deviation adds one bit to the maximum          tution of − sin2 x ln sin2 x with 1e . Since sin2 x ∈ [0, 1],
required quantum memory cost.                                                     √                        
                                                               in the region x > 2∆ where 4∆ ln √x2∆ > 0, we can
  Example 2: Uniform white noise. The normalized               likewise upper bound c(x) by making the substitution of
top-hat (rectangular) shift function allowing for jumps of                                              √
                                                               sin2 (x) with 1. Thus, for the region x > 2∆, we have
up to ±∆ around a constant displacement µ is written
                                                               a function f (x) ≥ c(x) given
               (
                  1
                       for µ − ∆ ≤ x ≤ µ + ∆,
      S∆ (x) = 2∆
                                                                                                        
                                                     (26)                             2∆ 1           x
                 0     otherwise.                                              f (x) = 2     + 2 ln √      .                 (31)
                                                                                      x    e          2∆
  Derivation of eigenvalues. Taking the square root of
this function                                                    However, as we plan to ultimately apply the
            √ alters its normalization, but not its shape:
                                                               Maclaurin–Cauchy integral convergence test, it is only
p
  S∆ (x) = 2∆S∆ (x).
  Suppose 0 < ∆ < 12 . In this case, S∆ (x) ∗ S∆ (−x)          convenient to use this upper bound in the region of x
yields the triangle function                                   where f (x) monotonically decreases.
                                                                                                   We identify
                                                                                                              this
                                                                                 df
                                                              region by setting dx = 4∆      √x        1
                                                                                      x3 −2 ln 2∆ + 1 − e                   = 0,
                             x
                      1 − 2∆ for 0 ≤ x ≤ 2∆,                  to              f (x) decreases monotonically when x ≥
                                                               √ find that
                      
                             x
 S∆ (x) ∗ S∆ (−x) = 1 + 2∆       for − 2∆ ≤ x < 0, (27)           2∆ exp e−1
                      
                      0                                                    2e , descending from its maximum value of
                                 otherwise.                    exp 1−e   .
                                                                      e
                                                                  However, once again consider c(x). Since it has the
This function is independent of the constant displace-         form of −y ln y, it follows that in any region, c(x) ≤
ment µ. Indeed, non-zero µ only results in perfectly can-      1           1−e
                                                                                  > 1e , we can then upper bound c(x) in
celling terms e2πikµ and e−2πikµ in the Fourier transform.     e . Since     e             √
   Basic Fourier analysis tells us that S∆ (x) transforms      the region of 0 ≤ x ≤ 2∆ to form the monotonically
into a normalized sinc function (sinc x = sin(πx)/πx),         decreasing function d(x) given
and the triangle function into the square of this:                                                            √
                                                                     exp 1−e                           0 ≤ x ≤ 2∆ exp e−1
                                                                                                                            
F(S∆ (x) ∗ S∆ (−x)) = 2∆sinc2 (2k∆). As this tends to                        e                                            2e
0 for large k, we can approximate the values of λk for         d(x) = 2∆ h 1             i                  √
                                                                                     √x                 x > 2∆ exp e−1
                                                                                                                        
                                                                             + 2 ln                                      ,
large N using eq. (14), to find the eigenspectrum                      x2 e           2∆                             2e
                                                                                                                       (32)
                2                   N        N                 that is guaranteed to satisfy d(x) ≥ c(x) for all x ≥ 0. At
   λk = 2∆sinc (2k∆)       for k = − , . . .   − 1.    (28)
                                    2        2                 this point, it is convenient to express this again in terms
                                                               of k, making the substitution ksplit = π√12∆ exp e−1
                                                                                                                       
   Upper bound on quantum memory cost. Through the                                                                  2e :

careful deployment of mildly intimidating algebra, we can               
                                                                               1−e
                                                                                      
also derive an upper bound on entropy cost of simulating                exp
                                                                                e h                              0 ≤ k ≤ dksplit e
the square shift function.  The outline of the proof is as     d(k) =       1                         √    i
                                                                                          1
                     P
follows. To bound k c(k) where c(k) = −λk ln λk , we
                                                                                         e + 2 ln    π 2∆k      k > dksplit e,
                                                                          2∆π 2 k 2
first construct a monotonically decreasing function d(k)                                                                  (33)
that satisfies c(k) ≤ d(k) at every k, and then show that
P                                                              where dksplit e represents the lowest integer above (or in-
    d(k) is bounded
                P from above. This sum will hence also         cluding) ksplit . This rounding is necessary since ksplit =
upper-bound k c(k). As with the Gaussian example,                √1   exp e−1      is in general not an integer. To upper
                                                               π 2∆          2e
for algebraic convenience, we will use natural logarithms      bound c(k) at all points, we must round        up this split
and only consider the region of positive k. In the final       between the regions of k, since exp 1−e        upper bounds
                                                                                                           e
stage, we will convert from nats to bits, and use the even-    all f (k). (I.e. being slightly too inclusive in the first re-
ness of c(k) to arrive at the full bound.                      gion will result in a slightly higher value of d(k) for the
   Explictly, we write                                         first k satisfying k ≥ ksplit ).
                                                                  Having derived our monotonically decreasing  P∞ function
                         sin2 x        sin2 x
                                             
             c(x) = −2∆ 2 ln 2∆ 2                      (29)    d(k), we are now in a position to show that k=0 d(k) is
                           x              x                                                 Pdksplit e       P∞
                                                               finite for ∆ > 0. Writing k=0           d(k) + k=dksplit e d(k)
where we have made the substitution x = 2πk∆.                  (for an upper bound, it is fine if a term is counted twice!),
                                                                                                                                                       11

we evaluate the two regions separately. Firstly,                                Combining these two terms, we arive at:
 dksplit e                                             
   X                       1          e−1              1−e
                  1+ √
             d(k) ≤            exp               exp
                       π 2∆             2e              e                      ∞
    k=0
                                                                                                                                        
                                                                               X           4                 1−e                     1−e
                     
                       1−e
                             
                                      1
                                                
                                                  1−e
                                                                                  d(k) ≤ √   exp                      + 2 exp                 . (37)
              = exp             + √        exp            (34)                           π 2∆                 2e                      e
                                                                               k=0
                          e       π 2∆             2e
                                  1
                                      exp e−1
                                                
where we have used 2π∆                      2e    + 1      >
   1       e−1
d 2π∆ exp 2e e. Secondly, using the Maclaurin-Cauchy
integral test (see e.g. [38]), we bound                                                                                 P∞
                                                                                Finally, to bound the entropy HQ = − ∞ λk log2 λk ,
        ∞
        X                                   Z ∞                               we must double the above (c(k) is even, and equation (37)
                  d(k) ≤ d(dksplit e) +                     d(k)dk            bounds only the region [0, ∞)), and we convert from nats
    k=dksplit e                                 dksplit e                     to bits (by including a factor of ln12 ):
                                                  Z ∞
                                      1−e
                          ≤ exp                 +            d(k)dk,   (35)
                                       e            ksplit
                                                                                                                                            
where the second line follows by substituting d(dksplit e)                                8                  1−e          4              1−e
                                                                                HQ ≤       √   exp                     +      exp                  .
with the maximum value of d(k), and by failing to round                              π ln 2 2∆                2e         ln 2             e
up the lower bound of the integral (thus including an                                                                                           (38)
                                R dksplit e
extra contribution equal to ksplit          d(k)dk ≥ 0). This
                                                                                By evaluating the constant terms, approximately,
integral may be analytically solved,

   1
       Z ∞
               1 1
                            √        
                     + 2 ln  π   2∆k
2π 2 ∆ ksplit k 2 e
                                                                                                       1.894
       
           −1
                  
                    1             √          ∞                                                HQ ≤ √ + 3.067,                               (39)
     =                + 2 + 2 ln π 2∆k                                                                    ∆
         2π 2 ∆ k e                                    exp( e−1
                                                             2e )
                                                   √1
                                                  π 2∆
                           
          3           1−e
     = √        exp           .                             (36)
       π 2∆            2e                                                     yielding our result.


 [1] IEEE. IEEE Standard for Floating-Point Arith-                                 10.1098/rspa.1998.0164.
     metic.      IEEE Std 754-2008, Aug 2008.            doi:                  [7] W. van Dam. Nonlocality & Communication Complexity.
     10.1109/IEEESTD.2008.4610935.                                                 PhD thesis, University of Oxford, 2000.
 [2] D. Deutsch. Quantum Theory, the Church-Turing Prin-                       [8] R. M. de Wolf. Quantum Computing and Communication
     ciple and the Universal Quantum Computer. Proceed-                            Complexity. PhD thesis, University of Amsterdam, 2001.
     ings of the Royal Society A: Mathematical, Physical and                       URL http://dare.uva.nl/record/1/194123.
     Engineering Sciences, 400(1818):97–117, jul 1985. ISSN                    [9] Gilles Brassard. Quantum Communication Complexity.
     1364-5021. doi:10.1098/rspa.1985.0070.                                        Foundations of Physics, 33(11):1593–1616. ISSN 1572-
 [3] D. Deutsch and R. Jozsa. Rapid Solution of Problems                           9516. doi:10.1023/A:1026009100467.
     by Quantum Computation. Proc. R. Soc. Lond. A., 439                      [10] P. Grassberger Toward a quantitative theory of self-
     (1907):553–558, 1992. ISSN 09628444. URL http://www.                          generated complexity International Journal of Theor-
     jstor.org/stable/52182.                                                       etical Physics, 25:(9):907–938, 1986 ISSN 0020-7748 doi:
 [4] L. K. Grover. A fast quantum mechanical algorithm for                         10.1007/BF00668821
     database search. In Proceedings of the twenty-eighth an-                 [11] J. P. Crutchfield and K. Young. Inferring statistical com-
     nual ACM symposium on Theory of computing, STOC                               plexity. Physical Review Letters, 63:(2):105–108, 1989.
     ’96, pages 212–219, New York, NY, USA, 1996. ACM.                             ISSN 00319007. doi:10.1103/PhysRevLett.63.105.
     ISBN 0-89791-785-5. doi:10.1145/237814.237866.                           [12] C. R. Shalizi and J. P. Crutchfield. Computational mech-
 [5] P. W. Shor. Polynomial-Time Algorithms for Prime Fac-                         anics: Pattern and prediction, structure and simplicity.
     torization and Discrete Logarithms on a Quantum Com-                          Journal of Statistical Physics, 104(3-4):817–879, 2001.
     puter. SIAM J. Comput., 26(5):1484–1509, oct 1997.                            ISSN 00224715. doi:10.1023/A:1010388907793.
     ISSN 0097-5397. doi:10.1137/S0097539795293172.                           [13] J. P. Crutchfield, C. J. Ellison, and J. R. Ma-
 [6] R. Cleve, A. K. Ekert, C. Macchiavello, and M. Mo-                            honey. Time’s barbed arrow: Irreversibility, Crypti-
     sca.     Quantum algorithms revisited.        Proc. R.                        city, and stored information. Physical Review Let-
     Soc. Lond. A., 454(1969):339–354, Jan 1998.         doi:                      ters, 103(9):094101, 2009.        ISSN 00319007.       doi:
                                                                                                                              12

     10.1103/PhysRevLett.103.094101.                                    doi:10.1038/ncomms1761.
[14] J. P. Crutchfield. Between order and chaos. Nature            [27] W. Y. Suen, J. Thompson, A. J. P. Garner, V. Vedral,
     Physics, 8(1):17–24, dec 2011. ISSN 1745-2473. doi:                and M. Gu. The classical-quantum divergence of com-
     10.1038/nphys2190.                                                 plexity in the Ising spin chain. Quantum 1:25, 2017. doi:
[15] R. Haslinger, K. L. Klinkner, and C. R. Shalizi. The               10.22331/q-2017-08-11-25
     computational structure of spike trains. Neural compu-        [28] J. R. Mahoney, C. Aghamohammadi, and J. P. Crutch-
     tation, 22(1):121–57, jan 2010. ISSN 1530-888X. doi:               field. Occam’s Quantum Strop: Synchronizing and
     10.1162/neco.2009.12-07-678.                                       Compressing Classical Cryptic Processes via a Quantum
[16] C. R. Shalizi, K. L. Shalizi, and R. Haslinger. Quantifying        Channel. Scientific reports, 6:20495, Jan 2016. ISSN
     self-organization with optimal predictors. Physical review         2045-2322. doi:10.1038/srep20495.
     letters, 93(11):118701, sep 2004. ISSN 0031-9007. doi:        [29] M. S. Palsson, M. Gu, J. Ho, H. M. Wiseman, and
     10.1103/PhysRevLett.93.118701.                                     G. J. Pryde. Experimentally modeling stochastic pro-
[17] J.G. Marques da Silva, J.C. Sartorelli, W.M. Gonçalves,           cesses with less memory by the use of a quantum pro-
     and R.D. Pinto. A scale law in a dripping faucet. Physics          cessor . Science Advances, 3(2):e1601302, Feb 2017. doi:
     Letters A, 226(5):269–274, feb 1997. ISSN 03759601. doi:           10.1126/sciadv.1601302
     10.1016/S0375-9601(96)00941-3.                                [30] P. M. Riechers, J. R. Mahoney, C. Aghamohammadi,
[18] R. W. Clarke, M. P. Freeman, and N. W. Watkins. Ap-                and J. P. Crutchfield. Minimized state complexity of
     plication of computational mechanics to the analysis of            quantum-encoded cryptic processes. Physical Review
     natural data: An example in geomagnetism. Physical                 A, 93(5):052317, May 2016. ISSN 2469-9926. doi:
     Review E, 67(1):016203, jan 2003. ISSN 1063-651X. doi:             10.1103/PhysRevA.93.052317.
     10.1103/PhysRevE.67.016203.                                   [31] C. Aghamohammadi, J. R. Mahoney, and J. P. Crutch-
[19] J. B. Park, J. W. Lee, J.-S. Yang, H.-H. Jo, and                   field. The ambiguity of simplicity in quantum and clas-
     H.-T. Moon. Complexity analysis of the stock mar-                  sical simulation. Physics Letters A, 381(14):1223–1227,
     ket. Physica A: Statistical Mechanics and its Applica-             April 2017 doi:10.1016/j.physleta.2016.12.036
     tions, 379(1):179–187, jun 2007. ISSN 03784371. doi:          [32] J. R. Mahoney, C. J. Ellison, and J. P. Crutchfield. In-
     10.1016/j.physa.2006.12.042.                                       formation accessibility and cryptic processes. Journal
[20] C.-B. Li, H. Yang, and T. Komatsuzaki. Multiscale                  of Physics A: Mathematical and Theoretical, 42(36):
     complex network of protein conformational fluctuations             362002, sep 2009. ISSN 1751-8113. doi:10.1088/1751-
     in single-molecule time series. Proceedings of the Na-             8113/42/36/362002.
     tional Academy of Sciences of the United States of Amer-      [33] K. Wiesner, M. Gu, E. Rieper, and V. Vedral.
     ica, 105(2):536–41, jan 2008. ISSN 1091-6490. doi:                 Information-theoretic lower bound on energy cost of
     10.1073/pnas.0707378105.                                           stochastic computation. Proceedings of the Royal So-
[21] C. Lu and R. R. Brooks. P2P hierarchical botnet traffic            ciety A: Mathematical, Physical and Engineering Sci-
     detection using hidden Markov models. In Proceedings               ences, 468:4058–4066, 2012. ISSN 1364-5021. doi:
     of the 2012 Workshop on Learning from Authoritative                10.1098/rspa.2012.0173.
     Security Experiment Results - LASER ’12, pages 41–46,         [34] S. Still, D. A. Sivak, A. J. Bell, and G. E. Crooks.
     New York, New York, USA, jul 2012. ACM Press. ISBN                 Thermodynamics of Prediction. Physical Review Let-
     9781450311953. doi:10.1145/2379616.2379622.                        ters, 109(12):120604, Sep 2012. ISSN 0031-9007. doi:
[22] C. E. Shannon. A mathematical theory of commu-                     10.1103/PhysRevLett.109.120604.
     nication. Bell Sys. Tech. Jour., 27(3):379–423,623–           [35] A. J. P. Garner, J. Thompson, V. Vedral, and M. Gu.
     656, Jul 1948. ISSN 00058580. doi:10.1002/j.1538-                  The thermodynamics of complexity and pattern manip-
     7305.1948.tb01338.x.                                               ulation? Physical Review E, 95(4):042140, Apr 2017.
[23] Benjamin Schumacher. Quantum coding. Physical Re-                  doi:10.1103/PhysRevE.95.042140
     view A, 51(4):2738–2747, Apr 1995. ISSN 1050-2947. doi:       [36] Robert M. Gray. Toeplitz and Circulant Matrices: A
     10.1103/PhysRevA.51.2738.                                          Review. Foundations and Trends in Communications
[24] Andreas Winter. Coding Theorems of Quantum Inform-                 and Information Theory, 2(3):155–239, 2005. ISSN 1567-
     ation Theory. PhD thesis, Universit´’at Bielefeld, Apr             2190. doi:10.1561/0100000006.
     1999. URL http://arxiv.org/abs/quant-ph/9907077.              [37] C. E. Shannon. Communication in the Presence of Noise.
[25] J. Ladyman, J. Lambert, and K. Wiesner. What is a                  Proceedings of the IRE, 37(1):10–21, Jan 1949. ISSN
     complex system? European Journal for Philosophy of                 0096-8390. doi:10.1109/JRPROC.1949.232969.
     Science 3 33-67, 2013 doi:10.1007/s13194-012-0056-8           [38] K. Knopp. Theory and applications of infinite series.
[26] M. Gu, K. Wiesner, E. Rieper, and V. Vedral. Quantum               Dover Publications, second english edition, 1990. ISBN
     mechanics can reduce the complexity of classical models.           9780486661650.
     Nature Communications, 3:762, 2012. ISSN 2041-1723.
