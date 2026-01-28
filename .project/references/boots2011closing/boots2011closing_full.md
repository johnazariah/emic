#

**Source:** boots2011closing
**Author:**
**Pages:** 10

---

## Full Text

                                                           Closing the Learning-Planning Loop with
                                                               Predictive State Representations

                                                          Byron Boots                        Sajid M. Siddiqi                  Geoffrey J. Gordon
                                                 Machine Learning Department                 Robotics Institute            Machine Learning Department
                                                  Carnegie Mellon University             Carnegie Mellon University         Carnegie Mellon University
                                                    Pittsburgh, PA 15213                   Pittsburgh, PA 15213               Pittsburgh, PA 15213
                                                      beb@cs.cmu.edu                      siddiqi@cs.cmu.edu                 ggordon@cs.cmu.edu

                                        ABSTRACT                                                          POMDPs and yield representations that are at least as com-
arXiv:0912.2385v1 [cs.LG] 12 Dec 2009


                                        A central problem in artificial intelligence is that of plan-     pact [24, 5]. In contrast to the latent-variable representa-
                                        ning to maximize future reward under uncertainty in a par-        tions of POMDPs, PSRs and OOMs represent the state of a
                                        tially observable environment. In this paper we propose and       dynamical system by tracking occurrence probabilities of a
                                        demonstrate a novel algorithm which accurately learns a           set of future events (called tests or characteristic events)
                                        model of such an environment directly from sequences of           conditioned on past events (called histories or indicative
                                        action-observation pairs. We then close the loop from ob-         events). Because tests and histories are observable quan-
                                        servations to actions by planning in the learned model and        tities, it has been suggested that learning PSRs and OOMs
                                        recovering a policy which is near-optimal in the original         should be easier than learning POMDPs. A final benefit
                                        environment. Specifically, we present an efficient and sta-       of PSRs and OOMs is that many successful approximate
                                        tistically consistent spectral algorithm for learning the pa-     planning techniques for POMDPs can be used to plan in
                                        rameters of a Predictive State Representation (PSR). We           these observable models with minimal adjustment. Accord-
                                        demonstrate the algorithm by learning a model of a simu-          ingly, PSR and OOM models of dynamical systems have po-
                                        lated high-dimensional, vision-based mobile robot planning        tential to overcome both the “curse of dimensionality” (by
                                        task, and then perform approximate point-based planning           compactly modeling state), and the “curse of history” (by
                                        in the learned PSR. Analysis of our results shows that the        applying approximate planning techniques).
                                        algorithm learns a state space which efficiently captures the        The quality of an optimized policy for a POMDP, PSR, or
                                        essential features of the environment. This representation        OOM depends strongly on the accuracy of the model: inac-
                                        allows accurate prediction with a small number of parame-         curate models typically lead to useless plans. We can specify
                                        ters, and enables successful and efficient planning.              a model manually or learn one from data, but due to the diffi-
                                                                                                          culty of learning, it is far more common to see planning algo-
                                                                                                          rithms applied to manually-specified models. Unfortunately,
                                        1.   INTRODUCTION                                                 it is usually only possible to hand-specify accurate models for
                                           Planning a sequence of actions or a policy to maximize fu-     small systems where there is extensive and goal-relevant do-
                                        ture reward has long been considered a fundamental problem        main knowledge. For example, recent extensions of approx-
                                        for autonomous agents. For many years, Partially Observ-          imate planning techniques for PSRs have only been applied
                                        able Markov Decision Processes (POMDPs) [1, 27, 4] have           to models constructed by hand [11, 8]. For the most part,
                                        been considered the most general framework for single agent       learning models for planning in partially observable environ-
                                        planning. POMDPs model the state of the world as a latent         ments has been hampered by the inaccuracy of learning al-
                                        variable and explicitly reason about uncertainty in both ac-      gorithms. For example, Expectation-Maximization (EM) [2]
                                        tion effects and state observability. Plans in POMDPs are         does not avoid local minima or scale to large state spaces;
                                        expressed as policies, which specify the action to take given     and, although many learning algorithms have been proposed
                                        any possible probability distribution over state. Unfortu-        for PSRs [25, 10, 34, 16, 30, 3] and OOMs [9, 6, 14] that
                                        nately, exact planning algorithms such as value iteration [27]    attempt to take advantage of the observability of the state
                                        are computationally intractable for most realistic POMDP          representation, none have been shown to learn models that
                                        planning problems. There are arguably two primary reasons         are accurate enough for planning. As a result, there have
                                        for this [18]. The first is the “curse of dimensionality”: for    been few successful attempts at learning a model directly
                                        a POMDP with n states, the optimal policy is a function of        from data and then closing the loop by planning in that
                                        an n − 1 dimensional distribution over latent state. The sec-     model.
                                        ond is the “curse of history”: the number of distinct policies       Several researchers have, however, made progress in the
                                        increases exponentially in the planning horizon. We hope to       problem of planning using a learned model. In one in-
                                        mitigate the curse of dimensionality by seeking a dynamical       stance [21], researchers obtained a POMDP heuristically
                                        system model with compact dimensionality, and to mitigate         from the output of a model-free algorithm [15] and demon-
                                        the curse of history by looking for a model that is susceptible   strated planning on a small toy maze. In another instance [20],
                                        to approximate planning.                                          researchers used Markov Chain Monte Carlo (MCMC) in-
                                           Predictive State Representations (PSRs) [13] and the closely   ference both to learn a factored Dynamic Bayesian Network
                                        related Observable Operator Models (OOMs) [9] are gen-            (DBN) representation of a POMDP in a small synthetic net-
                                        eralizations of POMDPs that have attracted interest be-           work administration domain, as well as to perform online
                                        cause they both have greater representational capacity than
planning. Due to the cost of the MCMC sampler used, this              step, O is the set of possible observations, and Q is a set of
approach is still impractical for larger models. In a final ex-       core tests. A set of core tests Q has the property that for any
ample, researchers learned Linear-Linear Exponential Fam-             test τ , there exists some function fτ such that p(τ O |h||τ A ) =
ily PSRs from an agent traversing a simulated environment,            fτ (p(QO |h||QA )) for all histories h. Here, the prediction
and found a policy using a policy gradient technique with             vector
a parameterized function of the learned PSR staten as in-
put [33, 31]. In this case both the learning and the planning               p(QO |h||QA ) = [p(q1O |h||q1A ), ..., p(q|Q|
                                                                                                                      O        A
                                                                                                                          |h||q|Q| )]T   (1)
algorithm were subject to local optima. In addition, the au-          contains the probabilities of success of the tests in Q. The
thors determined that the learned model was too inaccurate            existence of fτ means that knowing the probabilities for the
to support value-function-based planning methods [31].                tests in Q is sufficient for computing the probabilities for all
   The current paper differs from these and other previous            other tests, so the prediction vector is a sufficient statistic
examples of planning in learned models: it both uses a prin-          for the system. The vector m1 is the initial prediction for
cipled and provably statistically consistent model-learning           the outcomes of the tests in Q given some initial distribution
algorithm, and demonstrates positive results on a challeng-           over histories ω. We will allow the initial distribution to be
ing high-dimensional problem with continuous observations.            general; in practice ω might correspond to the steady state
In particular, we propose a novel, consistent spectral algo-          distribution for a heuristic exploration policy, or the distri-
rithm for learning a variant of PSRs called Transformed               bution over histories when we first encounter the system, or
PSRs [19] directly from execution traces. The algorithm               the empty history with probability 1.
is closely related to subspace identification for learning lin-          In order to maintain predictions in the tests in Q we need
ear dynamical systems (LDSs) [26, 29] and spectral algo-              to compute p(QO |ho||a, QA ), the distribution over test out-
rithms for learning Hidden Markov Models (HMMs) [7] and               comes given a new extended history, from the current distri-
reduced-rank Hidden Markov Models [22]. We then demon-                bution p(QO |h||QA ) (here p(QO |ho||a, QA ) is the probability
strate that this algorithm is able to learn compact models            over test outcomes conditioned on history h and observation
of a difficult, realistic dynamical system without any prior          o given the intervention of choosing the immediate next ac-
domain knowledge built into the model or algorithm. Fi-               tion a and the appropriate actions for the test). Let faoq be
nally, we perform point-based approximate value iteration             the function needed to update our prediction of test q ∈ Q
in the learned compact models, and demonstrate that the               given an action a and an observation o. (This function is
greedy policy for the resulting value function works well in          guaranteed to exist since we can set τ = aoq in fτ above.)
the original (not the learned) system. To our knowledge this          Finally, F is the set of functions faoq for all a ∈ A, o ∈ O,
is the first research that combines all of these achievements,        and q ∈ Q.
closing the loop from observations to actions in an unknown              In this work we will restrict ourselves to linear PSRs, a
domain with no human intervention beyond collecting the               subset of PSRs where the functions faoq are required to be
raw transition data.                                                  linear in the prediction vector p(QO |h||QA ), so that
                                                                      faoq (p(QO |h||QA )) = mTaoq p(QO |h||QA ) for some vector
2.   PREDICTIVE STATE REPRESENTATIONS                                 maoq ∈ R|Q| .1 We write Mao to be the matrix with rows
   A predictive state representation (PSR) [13] is a compact          mTaoq . By Bayes’ Rule, the update from history h, after
and complete description of a dynamical system that repre-            taking action a and seeing observation o, is:
sents state as a set of predictions of observable experiments
or tests that one could perform in the system. Specifically, a
                                                                                                        p(o, QO |h||a, QA )
test of length k is an ordered sequence of action-observation                   p(QO |ho||a, QA ) =
pairs τ = a1 o1 . . . ak ok that can be executed and observed                                                p(o|h||a)
at a given time. Likewise, a history is an ordered sequence                                              Mao p(QO |h||QA )
of action-observation pairs h = ah1 oh1 . . . aht oht that has been                                 =                                    (2)
                                                                                                        mT∞ Mao p(QO |h||QA )
executed and observed prior to a given time. The prediction
for a test τ is the probability of the sequence of observations       where m∞ is a normalizing vector. Specifying a PSR in-
o1 , . . . , ok being generated, given that we intervene to take      volves first finding a set of core tests Q, called the discovery
the sequence of actions a1 , . . . , ak . If the observations pro-    problem, and then finding the parameters Mao and m∞ for
duced by the dynamical system match those specified by the            those tests as well as an initial state m1 , called the learn-
test, then the test is said to have succeeded. The key idea           ing problem. The discovery problem is usually solved by
behind a PSR is that, if the expected outcomes of execut-             searching for linearly independent tests by repeatedly per-
ing all possible tests are known, then everything there is to         forming Singular Value Decompositions (SVDs) on collec-
know about the state of a dynamical system is also known.             tions of tests [10, 34]. The learning problem is then solved
   In PSRs, actions in tests are interventions, not observa-          by regression.
tions. Thus it is notationally convenient to separate a test          1
                                                                       Linear PSRs have been shown to be a highly expressive
τ into the observation component τ O and the action com-              class of models [9, 24]: if the set of core tests is minimal,
ponent τ A . In equations that contain probabilities, a single        then the set of PSRs with n = |Q| core tests is provably
vertical bar | indicates conditioning and a double vertical           equivalent to the set of dynamical systems with linear di-
bar || indicates intervening. For example, p(τiO |h||τiA ) is the     mension n. The linear dimension of a dynamical system is
probability of the observations in test τi , conditioned on his-      a measure of its intrinsic complexity; specifically, it is the
tory h, and given that we intervene to execute the actions            rank of the system-dynamics matrix [24] of the dynamical
                                                                      system. Since there exist dynamical systems of finite linear
in τi .                                                               dimension which cannot be modeled by any POMDP (or
   Formally a PSR consists of five elements {A, O, Q, m1 , F }.       HMM) with a finite number of states (see [9] for an exam-
A is the set of actions that can be executed at each time-            ple), POMDPs and HMMs are a proper subset of PSRs [24].
2.1    Transformed PSRs                                            indicative events as promised: it is a set of indicative events
   Transformed PSRs (TPSRs) [19] are a generalization of           which ensures that the rank of PT ,H is equal to the linear
PSRs that maintain a small number of linear combinations           dimension of the system. Finally, m1 , which we have de-
of test probabilities as sufficient statistics of the dynamical    fined as the initial prediction for the outcomes of tests in Q
system. As we will see, transformed PSRs can be thought            given some initial distribution over histories h, is given by
of as linear transformations of regular PSRs. Accordingly,         m1 = Sπ (here we are taking the expectation of the columns
TPSRs include PSRs as a special case since this transfor-          of S according to the correct distribution over histories ω).
mation can be the identity matrix. The main benefit of                We define PT ,ao,H ∈ R|T |×|H| , a set of matrices, one for
TPSRs is that given a set of core tests, the parameter learn-      each action-observation pair, that represent the probabilities
ing problem can be solved and a large step toward solving          of a triple of an indicative event hj , the immediate following
the discovery problem can be achieved in closed form. In           observation O, and a subsequent test τj , given the appropri-
this respect, TPSRs are closely related to the transformed         ate actions:
representations of LDSs and HMMs found by subspace iden-           [PT ,ao,H ]i,j ≡ Pr[τiO , O = o, H ∈ hj ||A = a, τiA ]
tification [29, 26, 7].
   For some dynamical system, let Q be the minimal set of                       = Pr[τiO , O = o|H ∈ hj ||A = a, τiA ] Pr[H ∈ hj ]
core tests with cardinality n = |Q| equal to the dimension-                     = Pr[τiO |H ∈ hj , O = o||A = a, τiA ]
ality of the linear system. Then, let T be a set of core tests
(not necessarily minimal) and let H be a sufficient set of                        Pr[O = o|H ∈ hj ||A = a] Pr[H ∈ hj ]
indicative events. A set of indicative events is a mutually                     = rτTi Pr[QO |H ∈ hj , O = o||A = a, QA ]
exclusive and exhaustive partition of the set of all possible                     Pr[O = o|H ∈ hj ||A = a] Pr[H ∈ hj ]
histories. We will define a sufficient set of indicative events
below. For TPSRs, |T | and |H| may be arbitrarily larger                        = rτTi Mao Pr[QO |H ∈ hj ||QA ] Pr[H ∈ hj ]
than n; in practice we might choose T and H by selecting                        = rτTi Mao shj Pr[H ∈ hj ]
sets that we believe to be large enough and varied enough
to exhibit the types of behavior that we wish to model.                         = rτTi Mao shj πhj
   We define several matrices in terms of T and H. In each          ⇒ PT ,ao,H = RMao Sdiag(π)                                (3c)
of these matrices we assume that histories H are sampled
according to ω; further actions and observations are specified     The matrices PT ,ao,H factor according to R and S (defined
in the individual probability expressions. PH ∈ R|H| is a          above) and the PSR transition matrix Mao ∈ Rn×n . Note
vector containing the probabilities of every h ∈ H.                that R spans the column space of both PT ,H and the matri-
                                                                   ces PT ,ao,H ; we make use of this fact below.
                       [PH ]i ≡ Pr[H ∈ hi ]                           Finally, we will use the fact that m∞ is a normalizing vec-
                                 = ω(H ∈ hi )                      tor to derive the equations below (by repeatedly multiplying
                                                                   by S and S † , and using the facts SS † = I and mT∞ S = 1T ,
                           ≡ π hi
                                                                   since each column of S is a vector of core-test predictions).
                      ⇒ PH = π                              (3a)   Here, k = |H| and 1k denotes the ones-vector of length k:
Here we have defined two notations, PH and π, for the same                                   mT∞ S = 1Tk
vector. Below we will generalize PH , but keep the same
                                                                                          mT∞ SS † = 1Tk S †
meaning for π.
  Next we define PT ,H ∈ R|T |×|H| , a matrix with entries                                    mT∞ = 1Tk S †                   (4a)
that contain the joint probability of every test τi ∈ T (1 ≤
                                                                                             mT∞ S = 1Tk S † S
i ≤ |T |) and every indicative event hj ∈ H (1 ≤ j ≤ |H|)
(assuming we execute test actions τiA ):                                                        1Tk = 1Tk S † S               (4b)

       [PT ,H ]i,j ≡ Pr[τiO , H ∈ hj ||τiA ]                          We now define a TPSR in terms of the matrices PH , PT ,H ,
                                                                   PT ,ao,H and an additional matrix U that obeys the condition
                  = Pr[τiO |H ∈ hj ||τiA ] Pr[H ∈ hj ]             that U T R is invertible. In other words, the columns of U
                  ≡ rτTi Pr[QO |H ∈ hj ||QA ] Pr[H ∈ hj ]          define an n-dimensional subspace that is not orthogonal to
                                                                   the column space of PT ,H . A natural choice for U is given
                  ≡ rτTi shj Pr[H ∈ hj ]                           by the left singular vectors of PT ,H .
                  = rτTi shj π                                        With these definitions, we define the parameters of a TPSR
                                                                   in terms of observable matrices and simplify the expressions
       ⇒ PT ,H = RSdiag(π)                                  (3b)   using Equations 3(a–c), as follows (here, Bao is a similarity
The vector rτi is the linear function that specifies the prob-     transform of the low-dimensional linear transition matrix
ability of the test τi given the probabilities of core tests Q.    Mao and b1 and b∞ are the corresponding linear transforma-
The vector shj contains the probabilities of all core tests Q      tions of the minimal PSR initial state M1 and the normal-
given that the history belongs to the indicative event hj . Be-    izing vector):
cause of our assumptions about the linear dimension of the                              b1 ≡ U T PT ,H 1k
system, the matrix PT ,H factors according to R ∈ R|T |×n
(a matrix with rows rτTi for all 1 ≤ i ≤ |T |) and S ∈ Rn×|H|                              = U T RSdiag(π)1k
(a matrix with columns shj for all 1 ≤ j ≤ |H|). Therefore,                                = U T RSπ
the rank of PT ,H is no more than the linear dimension of
the system. At this point we can define a sufficient set of                                = (U T R)m1                        (5a)
     bT∞ ≡ PH
            T
              (U T PT ,H )†                                             In practice, reset is often not available. In this case we
         = 1Tn S † Sdiag(π)(U T PT ,H )†                              can estimate PbH , PbT ,H , and PbT ,ao,H by dividing a single
                                                                      long sequence of action-observation pairs into subsequences
         = 1Tn S † (U T R)−1 (U T R)Sdiag(π)(U T PT ,H )†             and pretending that each subsequence started with a reset.
         = 1Tn S † (U T R)−1 U T PT ,H (U T PT ,H )†                  We are forced to use an initial distribution over histories,
                                                                      ω, equal to the steady state distribution of the policy which
         = 1Tn S † (U T R)−1                                          generated the data. This approach is called the suffix-history
         = mT∞ (U T R)−1                                      (5b)    algorithm [34]. With this method, the estimated matrices
              T             T        †
                                                                      will be only approximately correct, since interventions that
     Bao ≡ U PT ,ao,H (U PT ,H )                                      we take at one time will affect the distribution over histories
         = U T RMao Sdiag(π)(U T PT ,H )†                             at future times; however, the approximation is often a good
                                                                      one in practice.
         = U T RMao (U T R)−1 (U T R)Sdiag(π)(U T PT ,H )†              Once we have computed PbH , PbT ,H , and PbT ,ao,H , we can
         = (U T R)Mao (U T R)−1 U T PT ,H (U T PT ,H )†               generate Ub by singular value decomposition of PbT ,H . We can

         = (U T R)Mao (U T R)−1                               (5c)    then learn the TPSR parameters by plugging U     b , PbH , PbT ,H ,
                                                                      and PbT ,ao,H into Equation 5. For reference, we summarize
The derivation of Equation 5b makes use of Equations 4a               the above steps here2 :
and 4b. Given these parameters we can calculate the prob-
ability of observations o1:t at any time t given that we inter-          1. Compute empirical estimates PbH , PbT ,H ,PbT ,ao,H .
vened with actions a1:t , from the initial state m1 . Here we
write the product of each Mao (one for each action observa-              2. Use SVD on PbT ,H to compute U   b , the matrix of left
tion pair) Ma1 o1 Ma2 o2 . . . Mat ot as Mao1:t .                           singular vectors corresponding to the n largest singular
                                                                            values.
Pr[o1:t ||a1:t ] = mT∞ Mao1:t m1
                                                                         3. Compute model parameter estimates:
              = mT∞ (U T R)−1 (U T R)Mao1:t (U T R)−1 (U T R)m1
                                                                             (a) b    b T PbH ,
                                                                                 b1 = U
              = bT∞ Bao1:t b1                                  (6)
                                                                                 b∞ = (PbTT,H U
                                                                             (b) b              b )† PbH ,
In addition to the initial TPSR state b1 , we define normal-                                          b T PbT ,H )†
                                                                                       b T PbT ,ao,H (U
ized conditional ‘internal states’ bt . We define the TPSR                   (c) B
                                                                                 bao = U
state at time t + 1 as:                                               As we include more data in our averages, the law of large
                              Bao b1                                  numbers guarantees that our estimates PbH , PbT ,H , and PbT ,ao,H
                       bt+1 ≡ T 1:t                            (7)    converge to the true matrices PH , PT ,H , and PT ,ao,H (de-
                             b∞ Bao1:t b1
                                                                      fined in Equation 3). So by continuity of the formulas in
We can define a recursive state update for t > 1 as follows           steps 3(a–c) above, if our system is truly a TPSR of finite
(using Equation 7 as the base case for t = 1):                        rank, our estimates b  b1 , b
                                                                                                  b∞ , and B
                                                                                                           bao converge to the true
                            Bao1:t b1                                 parameters up to a linear transform. Although parameters
                   bt+1 ≡                                             estimated with finite data can sometimes lead to negative
                          bT∞ Bao1:t b1
                                                                      probability estimates when filtering or predicting, this can
                            Baot Bao1:t−1 b1                          be avoided in practice by thresholding the prediction vectors
                         = T
                          b∞ Baot Bao1:t−1 b1                         by some small positive probability.
                            Bao bt                                       Note that the learning algorithm presented here is distinct
                         = T t                                 (8)    from the TPSR learning algorithm presented in Rosencrantz
                          b∞ Baot bt
                                                                      et al. [19]. The principal difference between the two algo-
   The prediction of tests p(T O |h||T A ) at time t is given by      rithms is that here we estimate the joint probability of a
U bt = U U T Rst = Rst , and the rotation from a TPSR to a            past event, a current observation, and a future event in the
PSR is given by st = (U T R)−1 bt where st is the prediction          matrix PbT ,ao,H whereas in [19], the authors instead estimate
vector for the PSR. Note that in general, the elements of the         the probability of a future event, conditioned on a past event
linear combinations bt cannot be interpreted as probabilities         and a current observation. To compensate, Rosencrantz et
since they may lie outside the range [0, 1].                          al. later multiply this estimate by an approximation of the
                                                                      probability of the current observation, conditioned on the
                                                                      past event, but not until after the SVD is applied. Rosen-
3.    LEARNING TPSRS                                                  crantz et al. also derive the approximate probability of the
  Our learning algorithm works by building empirical esti-            current observation differently: as the result of a regression
mates PbH , PbT ,H , and PbT ,ao,H of the matrices PH , PT ,H , and   instead of directly from empirical counts. Finally, Rosen-
PT ,ao,H defined above. To build these estimates, we repeat-          crantz et al. do not make any attempt to multiply by the
edly sample a history h from the distribution ω, execute a            marginal probability of the past event, although this term
sequence of actions, and record the resulting observations.           2
This data gathering strategy implies that we must be able               The learning strategy employed here may be seen as a gen-
to arrange for the system to be in a state corresponding to           eralization of Hsu et al.’s spectral algorithm for learning
                                                                      HMMs [7] to PSRs. Note that since HMMs and POMDPs
h ∼ ω; for example, if our system has a reset, we can take            are a proper subset of PSRs, we can use the algorithm in
ω to be the distribution resulting from executing a fixed             this paper to learn back both HMMs and POMDPs in PSR
exploration policy for a few steps after reset.                       form.
cancels in the current work so it is possible that, in the                    where δ(O = o) is an indicator function for a particular
absence of estimation errors, both algorithms arrive at the                   observation. The parameters of the TPSR are defined in
same answer.                                                                  terms of a matrix U that obeys the condition that U T ΦT R
   Below we present two extensions to our learning algo-                      is invertible (we can take U to be the left singular values of
rithm that preserve consistency while relaxing the require-                   PT ,H ), and in terms of the matrices PH , PT ,H , and PT ,ao,H .
                                                                                                                      T
ment that we find a discrete set of indicative events and                     We also define a new vector e s.t. ΦH eT = 1k ; this means
tests. These extensions make learning substantially easier                    that the ones vector 1k must be in the row space of ΦH .
                                                                                                       T
for many difficult domains (e.g. for continuous observations)                 Since ΦH is a matrix of features, we can always ensure that
in practice.                                                                  this is the case by requiring one of our features to be a
3.1    Learning TPSRs with Indicative and Char-                               constant. Then, one row of ΦH is 1Tk , and we can set eT =
       acteristic Features                                                    [ 1 0 . . . 0 ]T . Finally we define the generalized TPSR
                                                                              parameters b1 , b∞ , and Bao as follows:
   In data gathered from complex real-world dynamical sys-
tems, it may not be possible to find a reasonably-sized set                    b1 ≡ U T PT ,H eT
of discrete core tests T or indicative events H. When this                                                       T
is the case, we can generalize the TPSR learning algorithm                          = U T ΦT RSdiag(π)ΦH eT
and work with features of tests and histories, which we call                        = U T ΦT RSdiag(π)1k
characteristic features and indicative features respectively.
In particular let T and H be large sets of tests and indica-                        = (U T ΦT R)Sπ
tive events (possibly too large to work with directly) and                          = (U T ΦT R)m1                                           (10a)
let φT and φH be shorter vectors of characteristic and in-
dicative features. The matrices PH , PT ,H , and PT ,ao,H will                bT∞ ≡ PH
                                                                                     T
                                                                                       (U T PT ,H )†
no longer contain probabilities but rather expected values                                            T
                                                                                    = 1Tn diag(π)ΦH (U T PT ,H )†
of features or products of features. For the special case of
                                                                                                             T
features that are indicator functions of tests and histories,                       = 1Tn S † Sdiag(π)ΦH (U T PT ,H )†
we recover the TPSR matrices from Section 2.1 where PH ,                                                                             T
PT ,H , and PT ,ao,H consist of probabilities.                                      = 1Tn S † (U T ΦT R)−1 (U T ΦT R)Sdiag(π)ΦH (U T PT ,H )†
   Here we prove the consistency of our estimation algorithm                        = 1Tn S † (U T ΦT R)−1 U T PT ,H (U T PT ,H )†
using these more general matrices as inputs. In the follow-
ing equations ΦT and ΦH are matrices of characteristic and                          = 1Tn S † (U T ΦT R)−1
indicative features respectively, with first dimension equal                        = mT∞ (U T ΦT R)−1                                       (10b)
to the number of characteristic or indicative features and                               T            T          †
second dimension equal to |T | and |H| respectively.                          Bao ≡ U PT ,ao,H (U PT ,H )
   An entry of ΦH is the expectation of one of the indicative                                                        T
                                                                                    = U T ΦT RMao Sdiag(π)ΦH (U T PT ,H )†
features given the occurrence of one of the indicative events.
                                                                                                                                         T
An entry of ΦT is the weight of one of our tests in calculating                     = U TΦT RMao (U TΦT R)−1(U TΦT R)Sdiag(π)ΦH (U TPT ,H )†
one of our characteristic features. With these features we
                                                                                    = (U T ΦT R)Mao (U T ΦT R)−1 U T PT ,H (U T PT ,H )†
generalize the matrices PH , PT ,H , and PT ,ao,H :
                              X                                                     = (U T ΦT R)Mao (U T ΦT R)−1                             (10c)
        [PH ]i ≡ E(φH
                    i (h)) =      Pr[H ∈ h]ΦH  ih
                                     h∈H                                      Just as in the beginning of Section 3, we can estimate PbH ,
                   H
      ⇒ PH = Φ π                                                     (9a)     PbT ,H , and PbT ,ao,H , and then plug the matrices into Equa-
                                                                              tions 10(a–c). Thus we see that if we work with characteris-
   [PT ,H ]i,j ≡ E(φTi (τ O ) · φH       A
                                 j (h)||τ )
                 XX                                                           tic and indicative features, and if our system is truly a TPSR
               =           Pr[τ O , H ∈ h||τ A ]ΦTiτ ΦH
                                                      jh                      of finite rank, our estimates b b1 , b
                                                                                                                   b∞ , and B
                                                                                                                            bao again converge
                 τ ∈T h∈H                                                     to the true PSR parameters up to a linear transform.
                 XX
             =               rτT sh πh ΦTiτ ΦH
                                             jh        (by Eq. (3b))
                 τ ∈T h∈H
                                                                              3.2     Kernel Density Estimation for Continuous
                 X               X                                                    Observations
             =          rτT ΦTiτ   sh πh ΦH
                                          jh
                                                                                 For continuous observations, we use Kernel Density Esti-
                 τ ∈T           h∈H
                                                                              mation (KDE) [23] to model the observation probability den-
                                           T
   ⇒ PT ,H = ΦT RSdiag(π)ΦH                                          (9b)     sity function (PDF). We use a fraction of the training data
                                                                              points as kernel centers, placing one multivariate Gaussian
[PT ,ao,H ]i,j ≡ E(φTi (τ O ) · φH                  A
                                 j (h) · δ(O = o)||τ A = a)
                 XX                                                           kernel at each point.3 The KDE estimator of the observa-
             =              Pr[τ O, O = o, H ∈ h||A = a, τ A ]ΦTiτ ΦH
                                                                    jh        tion PDF is a convex combination of these kernels; since
                 τ ∈T h∈H                                                     each kernel integrates to 1, this estimator also integrates to
                 XX                                                           1. KDE theory [23] tells us that, with the correct kernel
             =               rτT Mao sh πh ΦTiτ ΦH
                                                 jh      (by Eq. (3c))
                                                                              weights, as the number of kernel centers and the number
                 τ ∈T h∈H
                                     !                           !            of samples go to infinity and the kernel bandwidth goes to
                   X                           X
             =            rτT ΦTiτ       Mao         sh πh ΦH
                                                            jh                3
                                                                                We use a general elliptical covariance matrix, chosen by
                   τ ∈T                        h∈H                            PCA: that is, we use a spherical covariance after projecting
                                               T                              onto the eigenvectors of the covariance matrix of the obser-
 ⇒ PT ,ao,H = ΦT RMao Sdiag(π)ΦH                                       (9c)   vations, and scaling by the square roots of the eigenvalues.
zero (at appropriate rates), the KDE estimator converges to             backup steps on a finite set of heuristically-chosen belief
the observation PDF in L1 norm. The kernel density esti-                points rather than over the entire belief simplex. PBVI ex-
mator is completely determined by the normalized vector of              ploits the fact that the value function is PWLC. A linear
kernel weights; therefore, if we can estimate this vector ac-           lower bound on the value function at one point b can be
curately, our estimate of the observation PDF will converge             used as a lower bound at nearby points; this insight allows
to the observation PDF as well. Hence our goal is to predict            the value function to be approximated with a finite set of
the correct expected value of this normalized kernel vector             hyperplanes (often called α-vectors), one for each point. Al-
given all past observations. In the continuous-observation              though PBVI was designed for POMDPs, the approach has
case, we can still write our latent-state update in the same            been generalized to PSRs [8]. Formally, given some set of
form, using a matrix Bao ; however, rather than learning                points B = {b0 , . . . , bk } in the TPSR state space, we recur-
each of the uncountably-many Bao matrices separately, we                sively compute the value function and linear lower bounds
learn one base operator per kernel center, and use convex               at only these points. The approximation of the value func-
combinations of these base operators to compute observable              tion can be represented by a set Γ = {α0 , . . . , αk } such
operators as needed. For more details on practical aspects              that each αi corresponds to the optimal value function at
of the learning procedure with continuous observations, see             at least one prediction vector bi . To obtain the approximate
Section 5.2.                                                            value function Vt+1 (b) from the previous value function Vt (b)
                                                                        we apply the recursive backup operator on points in B: if
                                                                        Vt (b) = maxα∈Γt αT b, then
4.    PLANNING IN TPSRS                                                                          "                           #
   The primary motivation for modeling a controlled dynam-                                                    X         T
ical system is for reasoning about the effects of taking a se-                Vt+1 (b) = max R(b, a) + γ         max α Bao b        (13)
                                                                                        a∈A                      α∈Γt
                                                                                                           o∈O
quence of actions in the system. The TPSR model can be
augmented for this purpose by specifying a reward function                 In addition to being tractable on much larger-scale plan-
for taking an action a in state b:                                      ning problems than exact value iteration, PBVI comes with
                                                                        theoretical guarantees in the form of error bounds that are
                                                                        low-order polynomials in the degree of approximation, range
                         R(b, a) = ηaT b                         (11)
                                                                        of reward values, and discount factor γ [17, 8]. Perseus [28,
where ηaT ∈ Rn is the linear reward function for taking action          11] is a variant of PBVI that updates the value function over
a. Given this function and a discount factor γ, the planning            a small randomized subset of a large set of reachable belief
problem for TPSRs is to find a policy that                              points at each time step. By only updating a subset of belief
                                       ˆP maximizes
                                              t
                                                          ˜the ex-      points, Perseus can achieve a computational advantage over
pected discounted sum of rewards E         t γ R(bt , at ) . The
optimal policy can be compactly represented using the op-               plain PBVI in some domains. We use Perseus in this paper
timal value function V ∗ , which is defined recursively as:             due to its speed and simplicity of implementation.

                    "
                                 X
                                                             #          5.    EXPERIMENTAL RESULTS
     V ∗ (b) = max R(b, a) + γ         p(o|b, a)V ∗ (bao )       (12)      We have introduced a novel algorithm for learning TPSRs
              a∈A
                                 o∈O                                    directly from data, as well as a kernel-based extension for
                                                                        modeling continuous observations, and discussed how to plan
where bao is the state obtained from b after executing action           in the learned model. First we demonstrate the viability of
a and observing o. When optimized exactly, this value func-             this approach to planning in a challenging non-linear, par-
tion is always piecewise linear and convex (PWLC) in the                tially observable, controlled domain by learning a model di-
state and has finitely many pieces in finite-horizon planning           rectly from sensor inputs and then “closing the loop” by plan-
problems.4 The optimal action is then obtained by taking                ning in the learned model. Second, unlike previous attempts
the arg max instead of the max in Equation 12.                          to learn PSRs, which either lack planning results [19, 32], or
   Exact value iteration in POMDPs or TPSRs optimizes                   which compare policies within the learned system [33], we
the value function over all possible belief or state vectors.           compare our resulting policy to a bound on the best possi-
Computing the exact value function is problematic because               ble solution in the original system and demonstrate that the
the number of sequences of actions that must be consid-                 policy is close to optimal.
ered grows exponentially with the planning horizon, called
the “curse of history.” Approximate point-based planning                5.1    The Autonomous Robot Domain
techniques (see below) attempt only to calculate the best se-
                                                                           The simulated autonomous robot domain consists of a
quence of actions at some finite set of belief points. Unfortu-
                                                                        simple 45 × 45 unit square arena with a central obstacle
nately, in high dimensions, approximate planning techniques
                                                                        and brightly colored walls (Figure 1(A-B)). We modeled the
have difficulty adequately sampling the space of possible be-
                                                                        robot as a sphere of radius 2 units. The robot can move
liefs. This is due to the “curse of dimensionality.” Because
                                                                        around the floor of the arena, and rotate to face in any direc-
TPSRs often admit a compact low-dimensional representa-
                                                                        tion. The robot has a simulated 16 × 16 pixel color camera,
tion, approximate point-based planning techniques can work
                                                                        whose focal plane is located one unit in front of the robot’s
well in these models.
                                                                        center of rotation. The robot’s visual field was 45◦ in both
   Point-Based Value Iteration (PBVI) [17] is an efficient
                                                                        azimuth and elevation, thus providing the robot with an an-
approximation of exact value iteration that performs value
                                                                        gular resolution of ∼ 2.8◦ per pixel. Images on the sensor
4
  This observation follows from that fact that a TPSR is a              matrix at any moment were simulated by a non-linear per-
linear transformation of a PSR, and PSRs like POMDPs                    spective transformation of the projected values arising from
have PWLC value functions [11].                                         the robot’s position and orientation in the environment at
 A.                                  B.                            C. x 10−3                                    D.
                     Outer Walls
                                                                      4
            Inner Walls

                                                                      0


                                                                     −4


                                                                      −8        −4       0       4       8 −3   Learned Representation
                                       Simulated Ebvironment                                             x 10
      Simulated Environment                                                     Learned Subspace                      Mapped to
                                         3-d View (to scale)
                                                                                                                   Geometric Space

Figure 1: Learning the Autonomous Robot Domain. (A) The robot uses visual sensing to traverse a square
domain with multi-colored walls and a central obstacle. Examples of images recorded by the robot occupying
two different positions in the environment are shown on the at the bottom of the figure. (B) A to-scale
3-dimensional view of the environment. (C) The 2nd and 3rd dimension of the learned subspace (the first
dimension primarily contained normalization information). Each point is the embedding of a single history,
displayed with color equal to the average RGB color in the first image in the highest probability test. (D)
The same points in (C) projected onto the environment’s geometric space.


that time. The resulting 768-element pattern of unprocessed               initial segment of one of our trajectories. We choose the
RGB values was the only input to an robot (images were not                kernel covariance using PCA on these sequences of observa-
preprocessed to extract features), and each action produced               tions, just as described for single observations in Section 3.2.
a new set of pixel values. The robot was able to move for-                We then generate our indicative features for a new sequence
ward 1 or 0 units, and simultaneously rotate 15◦ , −15◦ , or              of three observations by evaluating each indicative kernel at
0◦ , resulting in 6 unique actions. In the real world, friction,          the new sequence, and normalizing so that the vector of fea-
uneven surfaces, and other factors confound precisely pre-                tures sums to one. Similarly, we define 2000 characteristic
dictable movements. To simulate this uncertainty, a small                 kernels, each one centered at a sequence of 3 observations
amount of Gaussian noise was added to the translation and                 from the end of one of our sample trajectories, choose a
rotation components of the actions. The robot was allowed                 kernel covariance, and define our characteristic feature vec-
to occupy any real-valued (x, y, θ) pose in the environment,              tor by evaluating each kernel at a new observation sequence
but was not allowed to intersect walls. In case of a collision,           and normalizing. The initial distribution ω is, therefore, the
we interrupted the current motion just before the robot in-               distribution obtained by initializing uniformly and taking 3
tersected an obstacle, simulating an inelastic collision.                 random actions. Finally, we define 500 observation kernels,
                                                                          each one centered at a single observation from the middle of
5.2    Learning a Model                                                   one of our sample trajectories, and replace each observation
   We learn our model from a sample of 10000 short tra-                   by its corresponding vector of normalized kernel weights.
jectories, each containing 7 action-observation pairs. We                    Next, we construct the matrices PbH , PbT ,H , and PbT ,ao,H .
generate each trajectory by starting from a uniformly ran-                As defined above, each element of PbH is the empirical ex-
domly sampled position in the environment and executing                   pectation (over our 8,000 training trajectories) of the cor-
a uniform random sequence of actions. We used the first                   responding element  P of the   indicative feature vector—that
l = 2000 trajectories to generate kernel centers, and the re-             is, element i is w1 w        H          H
                                                                                                t=1 φit , where φit is the ith indicative
maining w = 8000 to estimate the matrices PH , PT ,H , and                feature, evaluated at the current history at time t. Simi-
PT ,ao,H .                                                                larly, each element of PbT ,H is the empirical expectation of
   To define these matrices, we need to specify a set of in-              the product of one indicative P   feature and one characteris-
dicative features, a set of observation kernel centers, and a             tic feature: element i, j is w1 w        T H
                                                                                                              t=1 φit φjt . Once we have
set of characteristic features. We use Gaussian kernels to                constructed PbT ,H , we can compute U   b as the matrix of left
define our indicative and characteristic features, in a similar
                                                                          singular vectors of PbT ,H . One of the advantages of subspace
manner to the Gaussian kernels described above for observa-
                                                                          identification is that the complexity of the model can be
tions; our analysis allows us to use arbitrary indicative and
characteristic features, but we found Gaussian kernels to be              tuned by selecting the number of singular vectors in U    b . To
convenient and effective. Note that the resulting features                learn an exact TPSR, we should pick the first n singular
over tests and histories are just features; unlike the kernel             vectors that correspond to singular values in PbT ,H greater
centers defined over observations, there is no need to let the            than some cutoff that varies with the noise resolution of our
kernel width approach zero, since we are not attempting to                data. However, we may wish to pick a smaller set of sin-
learn accurate PDFs over the histories and tests in H and                 gular vectors; doing so will produce a more compact TPSR
T.                                                                        at the possible loss of prediction quality. We chose n = 5,
   In more detail, we define a set of 2000 indicative kernels,            the smallest TPSR that was able to produce high quality
each one centered at a sequence of 3 observations from the                policies (see Section 5.4 below).
A.                                      B.                                             C.                       D. 600
  x 10
       −3
                                             x 10
                                                 −3                                                                                                     507.8


                                                                                                                Number of Actions
 4                                           4
                                                                                                                                400

 0                                           0

                                                                                                                                200
−4                                        −4
                                                                                                                                        13.9    18.2*
  −8         −4     0         4       8 −3 −8         −4       0          4     8 −3                                                0
                                      x 10                                      x 10                                                Optimal            Random
                                                      Policies Executed in                   Paths Taken in
         Estimated Value Function                                                                                                              Greedy Walk
                                                       Learned Subspace                     Geometric Space
                                                                                                                                               Perseus


Figure 2: Planning in the Learned State Space. (A) The value function computed for each embedded point;
lighter indicates higher value. (B) Policies executed in the learned subspace. The red, green, magenta, and
yellow paths correspond to the policy executed by a robot with starting positions facing the red, green,
magenta, and yellow walls respectively. (C) The paths taken by the robot in geometric space while executing
the policy. Each of the paths corresponds to the path of the same color in (B). The darker circles indicate the
starting and ending position of each path, and the tick-mark in the circles indicates the robot’s orientation.
(D) Mean number of actions in path from 100 randomly sampled start position to the target image (facing
blue wall). The first bar (left) is the mean number of actions in the optimal solution found by A* search in the
robot’s configuration space. The second bar (center) is the mean number of actions taken by executing the
policy computed by Perseus in the learned model (the asterisk indicates that this mean was only computed
over the 78 successful paths). The last bar (right) is the mean number of actions required to find the target
with a random policy. The graph indicates that the policy computed from the learned TPSR is close to
optimal.


   Finally, rather than computing PbT ,ao,H directly, we in-                  the major features of the robot’s visual environment (Figure
stead compute U   b T PbT ,ao,H for each pair a, o: the latter ma-            1(C-D)), and continuous paths in the environment translate
trices are much smaller, and in our experiments, we saved                     into continuous paths in the latent space (Figure 2(B)).
substantially on both memory and runtime by avoiding con-
struction of the larger matrices. To construct U    b T PbT ,ao,H , we        5.4    Planning in the Learned Model
restrict to those training trajectories in which the action at                   To test the quality of the learned model, we set up a nav-
the middle time step (i.e., step 4) is a. Then, each element of               igation problem where the robot was required to plan a set
PbT ,ao,H is the empirical expectation (among the restricted                  of actions in order to reach a goal image (looking directly at
set of trajectories) of the product of one indicative feature,                the blue wall). We specified a large reward (1000) for this
one characteristic feature, and element o of the observation                  observation, a reward of −1 for colliding with a wall, and
kernel vector. So,                                                            0 for every other observation. We next learned a reward
                         wa                                                   function by linear regression from the histories embedded
       b T PbT ,ao,H = 1                   T 1
                          X T T
       U                       b φt )(φH
                              (U       t )     K(ot − o)           (14)       in the learned TPSR state space to the reward specified at
                       wa t=1               Zt                                each image that followed an embedded history. We used the
                                                                              reward function to compute an approximate value function
where K(.) is the kernel function and Zt is the kernel nor-                   using the Perseus algorithm with discount factor γ = .8, a
malization constant computed by summing over the 500 ob-                      prediction horizon of 10 steps, and with the 8000 embedded
servation kernels for each ot . Given the matrices PH , PT ,H ,               histories as the set of belief points. The learned value func-
and PT ,ao,H , we can compute the TPSR parameters using                       tion is displayed in Figure 2(A). Once the approximate value
the equations in Section 3.                                                   function has been learned, and an initial belief specified, the
                                                                              robot greedily chooses the action which maximizes the ex-
5.3         Qualitative Evaluation                                            pected value. The initial beliefs were computed by starting
  Having learned the parameters of the TPSR, the model                        with b1 and then incorporating 3 random action-observation
can be used for prediction, filtering, and planning in the                    pairs. Examples of paths planned in the learned model are
autonomous robot domain. We first evaluated the model                         presented in Figure 2(B); the same paths are shown in geo-
qualitatively by projecting the sets of histories in the train-               metric space (recall that the robot only has access to images;
ing data onto the learned TPSR state space: U     b T PbH . We                the geometric space is never observed by the robot) in Fig-
colored each datapoint according to the average of the red,                   ure 2(C). Note that there are a set of valid target positions in
green, and blue components of the highest probability obser-                  the environment since one can receive an identical close-up
vation following the projected history. The features of the                   image of a blue wall from anywhere along the corresponding
low dimensional embedding clearly capture the topology of                     edge of the environment.
   The reward function encouraged the robot to navigate to       the greater representational power of the PSR as compared
a specific set of points in the environment, therefore the       to POMDPs and partly due to the efficient and statistically
planning problem can be viewed as solving a shortest path        consistent nature of the learning method.
problem. Even though we don’t encode this intuition into
our algorithm, we can use it to quantitatively evaluate the
performance of the policy in the original system. First we
                                                                 7.   REFERENCES
randomly sampled 100 initial histories in the environment         [1] K. J. Aström. Optimal control of Markov decision
and asked the robot to plan a path based on its learned pol-          processes with incomplete state estimation. Journal of
icy. The robot was able to reach the goal in 78 of the trials.        Mathematical Analysis and Applications, 10:174–205,
In 22 trials, the robot got stuck repeatedly taking alternat-         1965.
ing actions whose effects cancelled (for example, alternating     [2] J. Bilmes. A gentle tutorial on the EM algorithm and
between turning −15◦ and 15◦ ).5 When the robot was able              its application to parameter estimation for gaussian
to reach the goal, we compared the number of actions taken            mixture and hidden markov models. Technical Report,
both to the minimal path, calculated by A* search in the              ICSI-TR-97-021, 1997.
robot’s configuration space given the true underlying posi-       [3] M. Bowling, P. McCracken, M. James, J. Neufeld, and
tion, and to a random policy. Note that comparison to the             D. Wilkinson. Learning predictive state
optimal policy is somewhat unfair: in order to recover the            representations using non-blind policies. In Proc.
optimal policy the robot would have to know its true under-           ICML, 2006.
lying position (which is not available to it), our model as-      [4] A. R. Cassandra, L. P. Kaelbling, and M. R. Littman.
sumptions would have to be exact, and the algorithm would             Acting Optimally in Partially Observable Stochastic
need an unlimited amount of training data. The results,               Domains. In Proc. AAAI, 1994.
summarized in Figure 2(D), indicate that the TPSR policy          [5] Eyal Even-Dar and Sham M. Kakade and Yishay
is close to the optimal policy in the original system. We             Mansour. Planning in POMDPs Using Multiplicity
think that this result is remarkable, especially given that           Automata. In UAI, 2005.
previous approaches have encountered significant difficulty       [6] H. Jaeger, M. Zhao, A. Kolling. Efficient Training of
modeling continuous domains [12] and domains with simi-               OOMs. In NIPS, 2005.
larly high levels of complexity [33].                             [7] D. Hsu, S. Kakade, and T. Zhang. A spectral
                                                                      algorithm for learning hidden markov models. In
6.   CONCLUSIONS                                                      COLT, 2009.
                                                                  [8] M. T. Izadi and D. Precup. Point-based Planning for
   We have presented a novel consistent subspace identifi-
                                                                      Predictive State Representations. In Proc. Canadian
cation algorithm that simultaneously solves the discovery
                                                                      AI, 2008.
and learning problems for TPSRs. In addition, we provided
two extensions to the learning algorithm that are useful in       [9] H. Jaeger. Observable operator models for discrete
practice, while maintaining consistency: characteristic and           stochastic time series. Neural Computation,
indicative features only require one to know relevant fea-            12:1371–1398, 2000.
tures of tests and histories, rather than sets of core tests     [10] M. James and S. Singh. Learning and discovery
and histories, while kernel density estimation can be used to         predictive state representations in dynamical systems
find observable operators when observations are real-valued.          with reset. In Proc. ICML, 2004.
We also showed how point-based approximate planning tech-        [11] M. R. James, T. Wessling, and N. A. Vlassis.
niques can be used to solve the planning problem in the               Improving approximate value iteration using memories
learned model. We demonstrated the representational ca-               and predictive state representations. In AAAI, 2006.
pacity of our model and the effectiveness of our learning        [12] N. K. Jong and P. Stone. Towards Employing PSRs in
algorithm by learning a very compact model from simulated             a Continuous Domain. Technical Report
autonomous robot vision data. We closed the loop by suc-              UT-AI-TR-04-309, University of Texas at Austin,
cessfully planning with the learned models, using Perseus to          2004.
approximately compute the value function and optimal pol-        [13] M. Littman, R. Sutton, and S. Singh. Predictive
icy for a navigation task. To our knowledge this is the first         representations of state. In Advances in Neural
instance of learning a model for a simulated robot in a par-          Information Processing Systems (NIPS), 2002.
tially observable environment using a consistent algorithm       [14] M. Zhao and H. Jaeger and M. Thon. A Bound on
and successfully planning in the learned model. We com-               Modeling Error in Observable Operator Models and an
pare the policy generated by our model to a bound on the              Associated Learning Algorithm. Neural Computation.
best possible value, and determine that our policy is close      [15] A. McCallum. Reinforcement Learning with Selective
to optimal.                                                           Perception and Hidden State. PhD Thesis, University
   We believe the spectral PSR learning algorithm presented           of Rochester, 1995.
here, and subspace identification procedures for learning        [16] P. McCracken and M. Bowling. Online discovery and
PSRs in general, can increase the scope of planning under             learning of predictive state representations. In Proc.
uncertainty for autonomous agents in previously intractable           NIPS, 2005.
scenarios. We believe that this improvement is partly due to     [17] J. Pineau, G. Gordon, and S. Thrun. Point-based
5                                                                     value iteration: An anytime algorithm for POMDPs.
  In an actual application, we believe that we could avoid
getting stuck by performing a short lookahead or simply by            In Proc. IJCAI, 2003.
randomizing our policy; for purposes of comparison, how-         [18] J. Pineau, G. Gordon, and S. Thrun. Anytime
ever, we report results for the greedy policy.                        point-based approximations for large POMDPs.
     Journal of Artificial Intelligence Research (JAIR),
     27:335–380, 2006.
[19] M. Rosencrantz, G. J. Gordon, and S. Thrun.
     Learning low dimensional predictive representations.
     In Proc. ICML, 2004.
[20] S. Ross and J. Pineau. Model-Based Bayesian
     Reinforcement Learning in Large Structured Domains.
     In Proc. UAI, 2008.
[21] G. Shani, R. I. Brafman, and S. E. Shimony.
     Model-based online learning of POMDPs. In Proc.
     ECML, 2005.
[22] S. M. Siddiqi, B. Boots, and G. J. Gordon.
     Reduced-Rank Hidden Markov Models.
     http://arxiv.org/abs/0910.0902, 2009.
[23] B. W. Silverman. Density Estimation for Statistics
     and Data Analysis. Chapman & Hall, 1986.
[24] S. Singh, M. James, and M. Rudary. Predictive state
     representations: A new theory for modeling dynamical
     systems. In Proc. UAI, 2004.
[25] S. Singh, M. L. Littman, N. K. Jong, D. Pardoe, and
     P. Stone. Learning predictive state representations. In
     Proc. ICML, 2003.
[26] S. Soatto and A. Chiuso. Dynamic data factorization.
     Technical report, UCLA, 2001.
[27] E. J. Sondik. The Optimal Control of Partially
     Observable Markov Processes. PhD. Thesis, Stanford
     University, 1971.
[28] M. T. J. Spaan and N. Vlassis. Perseus: Randomized
     point-based value iteration for POMDPs. Journal of
     Artificial Intelligence Research, 24:195–220, 2005.
[29] P. Van Overschee and B. De Moor. Subspace
     Identification for Linear Systems: Theory,
     Implementation, Applications. Kluwer, 1996.
[30] E. Wiewiora. Learning predictive representations from
     a history. In Proc. ICML, 2005.
[31] D. Wingate. Exponential Family Predictive
     Representations of State. PhD Thesis, University of
     Michigan, 2008.
[32] D. Wingate and S. Singh. On discovery and learning
     of models with predictive representations of state for
     agents with continuous actions and observations. In
     Proc. AAMAS, 2007.
[33] D. Wingate and S. Singh. Efficiently learning
     linear-linear exponential family predictive
     representations of state. In Proc. ICML, 2008.
[34] B. Wolfe, M. James, and S. Singh. Learning predictive
     state representations in dynamical systems without
     reset. In Proc. ICML, 2005.
