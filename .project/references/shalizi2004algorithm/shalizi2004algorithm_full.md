#

**Source:** shalizi2004algorithm
**Author:**
**Pages:** 8

---

## Full Text

                                            Blind Construction of Optimal Nonlinear Recursive Predictors for
                                                                   Discrete Sequences


                                                           Cosma Rohilla Shalizi                             Kristina Lisa Shalizi
                                                   Center for the Study of Complex Systems                   Statistics Department
                                                            University of Michigan                           University of Michigan
arXiv:cs/0406011v1 [cs.LG] 6 Jun 2004


                                                             Ann Arbor, MI 48109                             Ann Arbor, MI 48109
                                                             cshalizi@umich.edu                              kshalizi@umich.edu

                                                               Abstract                           [2]. The source code and documentation for an imple-
                                                                                                  mentation of CSSR are at http://bactra.org/CSSR/.
                                             We present a new method for nonlinear predic-
                                             tion of discrete random sequences under minimal
                                             structural assumptions. We give a mathematical
                                                                                                  2    Optimal Nonlinear Predictors
                                             construction for optimal predictors of such pro-
                                             cesses, in the form of hidden Markov models. We      Consider a sequence of random variables Xt drawn
                                             then describe an algorithm, CSSR (Causal-State       from a discrete alphabet A. A predictive statistic is
                                             Splitting Reconstruction), which approximates        a function η on the past measurements X−∞         t
                                                                                                                                                        . We
                                             the ideal predictor from data. We discuss the re-
                                             liability of CSSR, its data requirements, and its
                                                                                                  want to predict the process, so we want the statis-
                                                                                                                                         t
                                             performance in simulations. Finally, we compare      tic to summarize the information X−∞        contains about
                                                                                                     ∞
                                             our approach to existing methods using variable-     Xt+1 . That is, we wish to maximize the mutual in-
                                             length Markov models and cross-validated hid-                                                 t
                                                                                                  formation between the statistic η(X−∞        ) and the fu-
                                             den Markov models, and show theoretically and                 ∞
                                                                                                  ture Xt+1 , i.e., in the standard notation, maximize
                                             experimentally that our method delivers results             t       ∞                                t       ∞
                                                                                                  I[η(X−∞    ); Xt+1 ], which can be at most I[X−∞    ; Xt+1 ].
                                             superior to the former and at least comparable
                                             to the latter.                                       A sufficient statistic is one which reaches this level.
                                                                                                  This implies η is sufficient if and only if η(x− ) = η(y − )
                                                                                                                        t                         t
                                                                                                  implies P(Xt+1 ∞
                                                                                                                    |X−∞    = x− ) = P(Xt+1 ∞
                                                                                                                                               |X−∞     = y−)
                                        1    Introduction                                         [3]. Decision theory shows that optimal prediction re-
                                                                                                  quires only knowledge of a sufficient statistic [4]. It
                                        The prediction of discrete sequential data is an impor-   is desirable to compress a sufficient statistic, so as to
                                        tant problem in many fields, including bioinformatics,    minimize the information needed for optimal predic-
                                        neuroscience (spike trains), and nonlinear dynamics       tion. One sufficient statistic η1 is smaller than an-
                                        (symbolic dynamics). Existing prediction methods,         other η2 if η1 can be calculated from η2 . A minimal
                                        with the exception of variable-length Markov model        sufficient statistic is one which can be calculated from
                                        (VLMM) methods, make strong assumptions about             any other sufficient statistic. Minimal sufficient statis-
                                        the nature of the data-generating process. In this pa-    tics thus are the most compact summary of the data
                                        per, we present an algorithm for the blind construc-      which retains all the predictively-relevant information.
                                        tion of asymptotically optimal nonlinear predictors of    We now construct one, following [5] and [6].
                                        discrete sequences. These predictors take the form of     Say that two histories x− and y − , are equivalent when
                                        minimal sufficient statistics, naturally arranged into        ∞
                                                                                                  P(Xt+1    t
                                                                                                         |X−∞    = x− ) = P(Xt+1∞       t
                                                                                                                                     |X−∞   = y − ). The
                                        a hidden Markov model (HMM). We thus secure the                                  −     −
                                                                                                  equivalence class of x is [x ]. Define the function
                                        many desirable features of HMMs, and hidden-state         which maps histories to their equivalence classes:
                                        models more generally, without having to make a pri-
                                        ori assumptions about the architecture of the system.          ǫ(x− ) ≡ [x− ]
                                        Furthermore, our method is more widely applicable                         t                     t
                                        than those based on VLMMs. We also compare our            = y − : P(Xt+1
                                                                                                             ∞
                                                                                                                 |X−∞ = y − ) = P(Xt+1
                                                                                                                                   ∞
                                                                                                                                       |X−∞ = x− )
                                        approach to the use of cross-validation to select an      The possible values of ǫ, i.e., the equivalence classes,
                                        HMM architecture, and find our results are at least       are known as the “causal states” of the process; each
                                        comparable in terms of accuracy and parsimony, and        corresponds to a distinct distribution for the future.
                                        superior in terms of speed. For reasons of space, we      (We comment on the name “causal state” below.) The
                                                                                                                                 t
                                        omit proofs here. These can be found in [1, ch. 5] and    state at time t is St = ǫ(X−∞      ). Clearly, ǫ(x− ) is
a sufficient statistic. It is also minimal, since if η is     show that the current set of states is not sufficient.
sufficient, then η(x− ) = η(y − ) implies ǫ(x− ) = ǫ(y − ).
                                                              Suppose we are given a sequence x̄ of length N from a
One can further show [6] that ǫ is the unique minimal
                                                              finite alphabet A of size k. We wish to derive from this
sufficient statistic, meaning that any other must be
                                                              an estimate ǫ̂ of the the minimal sufficient statistic ǫ.
isomorphic to it.
                                                              We will do this by finding a set of states Σ, each mem-
The causal states have some important properties [6].         ber of which will be a set of strings, or finite-length
(1) {St } is a Markov process. (2) The causal states          histories. The function ǫ̂ will then map a history x−
are recursively calculable; there is a function T such        to whichever state contains a suffix of x− (taking “suf-
that St+1 = T (St , Xt+1 ). (3) One can represent the         fix” in the usual string-manipulation sense). Although
observed process X as a random function of the causal         each state can contain multiple suffixes, one can check
state process, i.e., there is naturally a hidden-Markov-      [2] that the mapping ǫ̂ will never be ambiguous. (This
model representation. (The familiar correspondence            contrasts with the variable-length Markov models de-
between HMMs and state machines lets us re-phrase             scribed in Sec. 5.1 below, where each state contains
the second property as: the causal states form a deter-       only a single suffix.)
ministic machine.) We will refer to causal state models
                                                              The null hypothesis is that the process is Markovian
or causal state machines.
                                                              on the basis of the states in Σ; that is,
The construction of the causal states is essentially the
                                                                       t−1
same as that of the “measure-theoretic prediction pro-          P(Xt |Xt−L = axt−1                      t−1
                                                                               t−L+1 ) = P(Xt |Ŝ = ǫ̂(xt−L+1 )) (1)
cess” introduced by Frank Knight [7], though that is
framed directly in terms of the conditional distribu-         for all a ∈ A. That is, adding an additional piece of
tions. Both can be regarded as applications of Wes-           history does not change the conditional distribution
ley Salmon’s concept of a “statistical relevance basis”       for the next observation. We can check this with a
[8] to time series. Causal states are also closely re-        standard statistical test, such as χ2 or Kolmogorov-
lated to the “predictive state representations” (PSRs)        Smirnov (which we used in our experiments below).
of controlled dynamical systems due to Littman, Sut-          If we reject this hypothesis, we fall back on a re-
ton and Singh [9], though PSRs are not generally min-         stricted alternative hypothesis, which is that we have
imal. (There is currently no discovery procedure for          the right set of conditional distributions, but have
PSRs, though there are ways to learn the parameters           matched them with the wrong histories. That is,
of a given PSR [10].) It is not clear that the “causal
                                                                            t−1
states” really are causal in the strong sense of e.g. [11],          P(Xt |Xt−L = axt−1                   ∗
                                                                                    t−L+1 ) = P(Xt |Ŝ = s )             (2)
but this needs investigation. Meanwhile, they need a
name, and “causal states” is less awkward than the            for some s∗ ∈ Σ, but s∗ 6= ǫ̂(xt−1
                                                                                               t−L+1 ). If this hypothe-
others.                                                       sis passes a statistical test, again with size α, then s∗
Our algorithm for inferring the causal states from data       is the state to which we assign the history1 . Only if
builds on the following observation [6, pp. 842–843].         the restricted alternative is itself rejected do we create
                                                   t
Say that η is next-step sufficient if I[Xt+1 ; η(X−∞  )] =    a new state, with the suffix axt−1t−L+1 .
           t
I[Xt+1 ; X−∞ ]. A next-step sufficient statistic contains     The algorithm itself has three phases; pseudo-code is
all the information needed for optimal one-step-ahead         given in Figure 1. Phase I initializes Σ to a single state,
prediction, but not necessarily for longer predictions.       which contains only the null suffix ∅. (That is, ∅ is a
If η is next-step sufficient, and it is recursively calcu-    suffix of any string.) The length of the longest suffix
lable, then η is sufficient for the whole of the future.      in Σ is L; this starts at 0. Phase II iteratively tests
Since ǫ satisfies these hypotheses, the minimal suffi-        the successive versions of the null hypothesis, Eq. 1,
cient statistic can be found by searching among those         and L increases by one each iteration, until we reach
which are next-step sufficient and recursive.                 some maximum length Lmax . At the end of II, ǫ̂ is
                                                              (approximately) next-step sufficient. Phase III makes
3    Causal-State Splitting                                   ǫ̂ recursively calculable, by splitting the states until
     Reconstruction                                           they have deterministic transitions. The last phase is
                                                              not as straightforward as it may seem.
We now describe an algorithm, Causal-State Splitting             1
                                                                  If more than one such state s∗ exists, we chose the
Reconstruction (CSSR), that estimates an HMM with                            b t |Ŝ = s∗ ) differs least, in total variation
                                                              one for which P(X
the properties described in the last section from se-                         b t |X t−1 = axt−1 ), which is plausible
                                                              distance, from P(X      t−L        t−L+1
quence data. CSSR starts by “assuming” the process is         and convenient. However, which state we chose is irrelevant
an independent, identically-distributed sequence, with        in the limit N → ∞, so long as the difference between the
one causal state, and adds states when statistical tests      distributions is not statistically significant.
There are standard algorithms [12] to take a non-
deterministic finite automaton (NDFA) and produce a
deterministic finite automaton (DFA), which is equiv-          Algorithm CSSR(A,x̄, Lmax , α)
alent in the sense of generating the same language.            I. Initialization: L ← 0, Σ ← {{∅}}
However, these algorithms do not ensure that each              II. Sufficiency:
state of the DFA, considered as an equivalence class               while L < Lmax
of strings, is a subset of a state of the NDFA. In                         for each s ∈ Σ
the present context, applying one of these algorithms                                     b t |Ŝ = s)
                                                                               estimate P(X
would result in states which mixed histories with sig-                         for each x ∈ s
nificantly different conditional distributions for the                             for each a ∈ A
next symbol — we would get a statistic which was re-                                   estimate p ← P(X   b t |X t−1 = ax)
                                                                                                                  t−L
cursive but not next-step sufficient. To preserve proba-                               Test(Σ, p, ax, s, α)
bilistic information while making the transitions deter-                   L←L+1
ministic, we proceed as follows [2]. We want there to be       III. Recursion:
a transition function T (s, b) such that ǫ̂(x− b) = T (s, b)        Remove transient states from Σ
for any x− ∈ s. Thus, for each state-symbol pair s, b,              recursive ← False
we check whether ǫ̂(x− b) is the same for all x− ∈ s.               until recursive
If we find a state-symbol pair where this does not                         recursive ← True
hold, we split that state into states where it does                        for each s ∈ Σ
hold. We then start checking the state-symbol pairs                            for each b ∈ A
all over again, since some other transitions may have                              x0 ← first x ∈ s
been altered. This procedure always terminates, leav-                              T (s, b) ← ǫ̂(x0 b)
ing us with a set of states with deterministic transi-                             for each x ∈ s, x 6= x0
tions. To do this smoothly, we must first remove any                                    if ǫ̂(xb) 6= T (s, b)
transient states which the second phase may have cre-                                   then create new state s′ ∈ Σ
ated. These transients are never true causal states                                            T (s′ , b) ← ǫ̂(xb)
[13], but are sometimes useful in filtering applications,                                      for each y ∈ s such that
in which case they can be straightforwardly restored                                                       ǫ̂(yb) = ǫ̂(xb)
from the true, recurrent states [13].                                                               Move(y, s, s′ )
b t |X t−1 = x) may be estimated in several ways; we
P(X                                                                                            recursive ← False
         t−L
have used simple maximum likelihood. P(X b t |Ŝ = s),
                                                               Test(Σ, p, ax, s, α)
in turn, must be estimated, and we used the weighted
                                                                   if null hypothesis (Eq. 1) passes a test of size α
average of the estimated distributions of the histories
                                                                   then s ← ax ∪ s
in s. When L = 0 and the only state contains just the
             b t |Ŝ = s) = P(X
                            b t ), the unconditional               else if restricted alternative hypothesis (Eq. 2)
null string, P(X
                                                                            passes a test of size α for s∗ ∈ Σ, s∗ 6= s
probability distribution.
                                                                   then Move(ax, s, s∗ )
                                                                   else create new state s′ ∈ Σ
3.1   Time Complexity                                                   Move(ax, s, s′ )

Phase I computes the relative frequency of all words           Move(x, s1 , s2 )
in the data stream, up to length Lmax + 1. There are               s1 ← s1 \ x
several ways this can be done using just a single pass                           b t |Ŝ = s1 )
                                                                   re-estimate P(X
through the data. In our implementation, as we scan                s2 ← s2 ∪ x
the data, we construct a parse tree which counts the                             b t |Ŝ = s2 )
                                                                   re-estimate P(X
occurrences of all strings whose length does not exceed
Lmax + 1. Thereafter we need only refer to the parse
tree, not the data. This procedure is therefore O(N ),         Figure 1:    Pseudo-code for the algorithm CSSR. Argu-
and this is the only sub-procedure whose time depends          ments: A: discrete alphabet for the stochastic process; x̄:
on N .                                                         sequence of length N drawn from A; Lmax , maximum his-
                                                               tory length considered when estimating causal states; α,
Phase II checks, for each suffix ax, whether it belongs        size of the hypothesis tests, i.e., probability of falsely re-
to the same state as its parent x. Using a hash ta-            jecting the hypothesis being tested. Newly created states
ble, we can do this, along with assigning ax to the            are always empty initially.
appropriate state, creating the latter if need be, in
constant time. Since there are at most u(k, Lmax) ≡
                                                                               t+τ
(k Lmax +1 − 1)/(k − 1) suffixes, the time for phase II is            ∞
                                                                   P(Xt+τ +1 |X−∞ = x ).
                                                                                     −

O(u(k, Lmax )) = O(k Lmax ).
                                                               2. The process has only finitely many causal states.
Phase III itself has three parts: getting the transi-
                                                               3. Every state contains at least one suffix of finite
tion structure, removing transient states, and refin-
                                                                  length. That is, there is some Λ such that every
ing the states until they have recursive transitions.
                                                                  state contains a suffix of length Λ or less. This
The time to find the transition structure is at most
                                                                  does not mean that Λ symbols of history always
ku(k, Lmax ). Removing transients can be done by find-
                                                                  fix the state, just that it is possible to synchronize
ing the strongly-connected components of the state-
                                                                  [13] to every state after seeing no more than Λ
transition graph, and then finding the recurrent part
                                                                  symbols.
of the connected-components graph. Both these op-
erations take a time proportional to the number of
                                                              Under these assumptions, the reconstructed set of
nodes plus the number of edges in the state-transition
                                                              causal states “converges in probability” on the true
graph. The number of nodes in the latter is at most
                                                              causal states, in the sense that
u(k, Lmax ), since there must be at least one suffix
per node, and there are at most k edges per node.                  P(∃x− : ǫ(x− ) 6= ǫ̂(x− )) → 0
Hence transient-removal is O(u(k, Lmax )(k + 1)) =
                                                              as N → ∞ [2, p. 16]. We establish this by show-
O(k Lmax +1 + k Lmax ) = O(k Lmax +1 ). As for refining
                                                              ing that the probability of assigning a history to the
the states, the time needed to make one refining pass
                                                              wrong equivalence class goes to zero as N → ∞. More
is ku(k, Lmax), and the maximum number of passes
                                                              exactly, for a pair of histories x− , y − , define the events
needed is u(k, Lmax ), since, in the worst case, we will
have to make every suffix its own state, and do so             E(x− , y − ) ≡     (ǫ̂(x− ) = ǫ̂(y − )) ∧ (ǫ(x− ) 6= ǫ(y − )),
one suffix at a time. So the maximum time for refine-          F (x− , y − ) ≡    (ǫ̂(x− ) 6= ǫ̂(y − )) ∧ (ǫ(x− ) = ǫ(y − )) .
ment is O(ku2 (k, Lmax )) = O(k 2Lmax +1 ), and the max-
imum time for all of phase III is O(k Lmax +1 +k Lmax+1 +     Then [2, pp. 15–16]
k 2Lmax +1 ) = O(k 2Lmax +1 ). Note that if removing tran-
sients consumes the maximal amount of time, then re-               ∀x− , y − , P(E(x− , y − ) ∪ F (x− , y − )) → 0 .
finement cannot and vice versa.                               To establish this fact in its turn, we use large devia-
Adding up, and dropping lower-order terms, the to-            tion theory for Markov chains to show that the empir-
tal time complexity for CSSR is O(k 2Lmax +1 ) + O(N ).       ical conditional distribution for each history converges
Observe that this is linear in the data size N . The high     on its true value exponentially quickly [2, pp. 12–13],
exponent in k is reached only in extreme cases, when          and consequently the probability that any of our es-
every string spawns its own state, almost all of which        timated conditional distributions differs significantly
are transient, etc. In practice, we have found CSSR to        from its true value goes to zero exponentially in N
be much faster than this worst-case result suggests2 .        [2, pp. 13–15]. The test size α does not affect this
                                                              convergence, becoming irrelevant in the limit of large
                                                              N . (With finite N , of course, α influences our risk of
4     Convergence and Performance                             making states simply on the basis of sampling fluctu-
                                                              ations.) Under some further assumptions, P(ǫ̂ 6= ǫ)
We have established the convergence of CSSR on                actually goes to zero exponentially in N , and then, by
the correct set of states, subject to suitable condi-         the Borel-Cantelli Lemma, one has the wrong struc-
tions. The proofs, which use large deviations theory          ture only finitely often before converging on the true
on Markov chains, are too long to give here, so we            causal states.
simply state the assumptions and the conclusions [2].
                                                              If the states are correct, then another large-deviation
We make the following hypotheses.                             argument [2, sec. 4.3] gives us a handle on the expected
                                                              prediction error. Since the forecasts made by our pre-
    1. The process is conditionally stationary. That          dictors are distributional, error should be measured as
                                    ∞
       is, for all values of τ , P(Xt+1   t
                                        |X−∞ = x− ) =         a divergence between the predicted distribution and
                                                              the true one. Using the total variation metric3 as our
    2
      Average-case time complexity will depend on the sta-    divergence measure, error goes down as N −1/2 . This
tistical properties of the data source. For instance, the     is illustrated in Figure 5.
number of strings of length Lmax is here bounded by              3
u(k, Lmax ) ≈ kLmax . But if Lmax is reasonably large, and         The total variation or L1 distance between two mea-
the source satisfies the asymptotic equipartition property    sures
                                                              P     P and Q over a discrete space A is d(P, Q) ≡
[14, sec. 15.7], only ≈ 2hLmax strings are produced with        a∈A |P (a) − Q(a)|. Scheffe’s identity [15] asserts that
positive probability, where h ≤ log k is the source entropy   d(P, Q) = 2 supA⊆A |P (A) − Q(A)|, and consequently 0 ≤
rate.                                                         d(P, Q) ≤ 2.
                                                A | 0.5
                                                                                                  AAAB


                        B | 1.0
   2                                                1
                        B | 0.5
                                                                                                     A | 0.1875


                                                                                                   BA

Figure 2: The Even Process. Transition labels show the
symbol emitted, and the probability of making the transi-
tion.                                                                  B | 0.4375     A | 0.250                           A | 0.5625          B | 0.8125


Of the three assumptions in our convergence proof, the          B | 0.8125      BAB                               A | 0.750            BAA


only one which affects the parameters of the algorithm
is the third, that there is an integer Λ such that each
of the true causal states contains at least one suffix                                              A | 0.9375                B | 0.4375     A | 0.5625


of length Λ or less. Λ is thus a characteristic of the
underlying process, not CSSR. If Lmax < Λ, not only
does the proof of convergence fail, there is no way to                                B | 0.750                   BAAB                         AAA         A | 0.1875

obtain the true states. For periodic processes Λ is
equal to the period; there are no general results for
other kinds of processes.                                                                                B | 0.250

Rather than guessing Λ, one might use the largest
feasible Lmax , but this is limited by the quantity of                                  BB         B | 0.0625
data [17]. Let L(N ) be the the maximum L we can
use when we have N data-points. If the observed
process has the weak Bernoulli property (which ran-         Figure 3: A seven-state process, used in [16] to study
dom functions of irreducible Markov chains do), and         human sequence prediction. Here each state is defined by
an entropy rate of h, then a sufficient condition for       a single suffix, as indicated. All transition probabilities are
the convergence of sequence probability estimates is        multiples of 1/16.
that L(N ) ≤ log N/(h + ε), for some positive ε. If
L(N ) ≥ log N/h, probability estimates over length L
                                                            rect distributions. Figure 5 also shows the asymptotic
words do not converge. We must know h to use this
                                                            scaling of the error with N . Curves average over 30
result, but log k ≥ h, so using log k in those formulas
                                                            independent trials at each N ; α is fixed to 10−3 . Re-
gives conservative estimates. For a given process and
                                                            sults for the seven-state process of Figure 3 are given
data-set, it is of course possible that L(N ) < Λ, in
                                                            in Section 5.2.
which case we simply haven’t enough data to recon-
struct the true states.
We have tested CSSR on a variety of real and sim-
                                                            5        Comparison with Previous Methods
ulated data sources, and here report two simulated
examples, both binary-valued: the “even process,” il-       5.1         Variable-Length Markov Models
lustrated in Figure 2, and a seven-state process used
                                                            The “context” algorithm of Rissanen [18] and its de-
in experimental studies of human sequence prediction
                                                            scendants [19, 20, 21, 22] construct “variable-length
[16], illustrated in figure 3. (The results of applying
                                                            Markov models” (VLMMs) from sequence data. They
CSSR to neuronal spike trains will be reported else-
                                                            find a set of contexts such that, given the context, the
where.)
                                                            past of the sequence and its next symbol are condi-
For the even process, the system can start in either        tionally independent. Contexts are taken to be suffixes
state 1 or state 2. When in state 1 it is equally likely    of the history, and the algorithms work by examining
to emit an A, staying in 1, or emit a B, moving to          increasingly long histories, creating new contexts by
2. In 2 it always emits a B and moves to 1. This is         splitting existing ones into longer suffixes when thresh-
an HMM, but it is not equivalent to any finite-order        olds of error are exceeded [23]. (This means that con-
Markov chain (see below). Figures 4 and 5 illustrate        texts can be arranged in a tree, so these are also called
the ability of CSSR to get the correct number of causal     “context tree” or “probabilistic suffix tree” [23] algo-
states, the correct transition structure, and the cor-      rithms.)
                                 Average Number of States Inferred                                                                                  Prediction Error versus History Length
         26                                                                       26
                  N = 10^6                                                                                                  10                                                                       N = 10^6
         24       N = 10^5                                                        24                                                                                                                 N = 10^5
                  N = 10^4                                                                                                                                                                           N = 10^4
                  N = 10^3                                                                                                                                                                           N = 10^3
         22       N = 10^2                                                        22                                                                                                                 N = 10^2
         20                                                                       20
                                                                                                                                1
         18                                                                       18


                                                                                       Variational Error (log scale)
         16                                                                       16

         14                                                                       14
States


                                                                                                                            0.1
         12                                                                       12

         10                                                                       10

         8                                                                        8

         6                                                                        6                                     0.01

         4                                                                        4

         2                                                                        2

         0                                                                        0                                    0.001
              1         2    3   4         5          6         7    8   9   10                                                     1   2   3         4          5           6           7       8          9   10
                                          History Length                                                                                                                 L

                                                                                                                                                    Scaled Error versus History Length
                                                                                                                       20
                                                                                                                                                                                                     N = 10^6
Figure 4: Number of states inferred versus Lmax and N                                                                  18
                                                                                                                                                                                                     N = 10^5
                                                                                                                                                                                                     N = 10^4
for the even process. The true number of causal states is                                                                                                                                            N = 10^3
                                                                                                                                                                                                     N = 10^2
2.                                                                                                                     16

                                                                                                                       14


                                                                                       Rescaled Variational Error
                                                                                                                       12
Causal state reconstruction has an important advan-
                                                                                                                       10
tage over VLMM methods. Each state in a VLMM is
                                                                                                                        8
represented by a single suffix, and consists of all and
only the histories ending in that suffix. For many pro-                                                                 6


cesses, the causal states contain multiple suffixes. In                                                                 4

these cases, multiple “contexts” are needed to repre-                                                                   2

sent a single causal state, so VLMMs are generally                                                                      0
                                                                                                                            3           4       5            6               7               8          9       10
more complicated than the HMMs we build. The                                                                                                                         L

causal state model is the same as the minimal VLMM
if and only if every causal state contains a single suffix.                            Figure 5: Prediction error as a function of Lmax and N
This is the case for the process in Fig. 3, where CSSR                                 for the even process. Error is the total-variation distance
and VLMM methods will give the same results.                                           between the actual distribution over words of length 10,
                                                                                       and that predicted by the inferred states. Top panel: error
                                                                                                                                                √
Recall the even process of the last section. Any history                               (log scale) as a function of Lmax . Bottom: error times N
ending in A, or in an A followed by an even number                                     (linear scale). Here 3 ≤ Lmax ≤ 10, since if Lmax < 3 CSSR
of B’s, belongs to state 1. Any history terminated by                                  cannot find the correct states. With this α, CSSR never
an A followed by an odd number of B’s, belongs to 2.                                   gets the states right for N = 102 , and only sporadically for
                                                                                       N = 103 , so those lines are not on the scaling curve.
Clearly 1 and 2 both contain infinitely many suffixes,
and so correspond to an infinite number of contexts.
VLMMs are simply incapable of capturing this struc-                                    VLMMs cannot handle the even process, they cannot
ture. If we let Lmax grow, a VLMM algorithm will in-                                   handle any strictly sofic process, even though those are
crease the number of contexts it finds without bound,                                  just regular languages. Causal states cannot provide
but cannot achieve the same combination of predictive                                  a finite representation of every stochastic regular lan-
power and model simplicity as causal state reconstruc-                                 guage [13], but the class they capture strictly includes
tion (as illustrated by Figures 4 and 5). Note, too, that                              those captured by VLMMs.
the causal states for the even process have finite rep-
resentations, even though they contain infinitely many
                                                                                       5.2                                          Cross-Validation
suffixes.
The even process is one of the strictly sofic processes                                A standard heuristic for finding the right HMM ar-
[24, 25], which can be described by finite state models,                               chitecture is cross-validation [26]. One picks multiple
but are not Markov chains of any finite order4 . Just as                               candidate architectures, training each one using the
                                                                                       expectation-maximization (EM) algorithm, and then
     More exactly, each history x− has a follower set of
         4                                                                             compares their performance on fresh test data, select-
futures x+ which can succeed it. A process is sofic if it has                          ing the one with the smallest out-of-sample error.
only a finite number of distinct follower sets, and strictly
sofic if it is sofic and has an infinite number of irreducible                         To compare the performance of CSSR against this
forbidden words.                                                                       baseline, we started with fully-connected HMMs with
 N     dCV           dCSSR         ŝCV        ŝCSSR         N      dCV           dCSSR         ŝCV        ŝCSSR
 102   1.27 ± 0.23   1.10 ± 0.23   6.6 ± 1.5   1.6 ± 1.0      102    1.41 ± 0.23   0.70 ± 0.12   4.5 ± 2.1   5.1 ± 1.5
 103   1.25 ± 0.41   0.19 ± 0.23   5.6 ± 1.7   2.2 ± 0.1      103    1.40 ± 0.17   0.21 ± 0.06   5.8 ± 2.7   6.6 ± 0.8
 104   1.15 ± 0.02   0.02 ± 0.02   2.0 ± 0     2.0 ± 0        104    1.40 ± 0.11   0.06 ± 0.01   2.3 ± 0.7   7.2 ± 0.6

Table 1:       Comparison of the performance of HMM          Table 2: Comparison of the performance of HMM cross-
cross-validation to CSSR on the even process. dCV ,          validation to CSSR on the seven-state process. Variables
total-variation distance between cross-validated HMM and     are as in 1.
the even process; dCSSR , distance between reconstructed
causal state model and the even process; ŝCV , number of
states in cross-validated HMM; ŝCSSR , number of states     6      Conclusion
in reconstructed model. In all cases the numbers given are
the means over multiple independent trials, plus or minus
                                                             We have described an algorithm, CSSR, for the unsu-
one standard deviation. Recall that 0 ≤ d ≤ 2, and that
the minimal number of states needed is 2.                    pervised construction of optimal nonlinear predictors
                                                             of discrete sequences. The predictors take the form of
                                                             minimal sufficient statistics, arranged naturally into
                                                             a hidden Markov model. CSSR’s time complexity is
M states, M = 1 to 10. We trained these, using               linear in the data size. It reliably infers the statistical
the EM algorithm, on N data-points from the even             structure of processes with finitely many causal states.
process. Our test data consisted of another N data-          CSSR’s predictive performance is at least comparable
points from an independent realization, and we se-           to cross-validated expectation-maximization, but it is
lected HMMs based on the log-likelihood they assigned        constructive and faster; and the class of processes it
to the test data. Following common practice, the ini-        can represent is strictly larger than those of competing
tial HMM parameters fed to the EM algorithm were             constructive methods, such as variable-length Markov
those for fully-connected models, i.e., every state could    models.
transition to every other state, and every state could
emit every symbol. We then calculated, for each cross-       Two directions for future work suggest themselves. (1)
validated HMM, the total variation distance between          CSSR does not require prior knowledge about system
the distributions it and the even process generated over     dynamics, but by the same token cannot exploit such
sequences of length 10. (Because cross-validation is         knowledge when it exists. One way around this would
so computationally intensive, we have only compared          be to initialize the algorithm with a non-trivial parti-
up to length N = 104 .) Table 1 compares this error          tion of histories, reflecting a guess about which pat-
measure for the cross-validated HMMs and for the re-         terns are dynamically important, and let CSSR revise
constructed causal state models. It also indicates the       that partition the way it does now. It would be in-
number of states selected by cross-validation, which is      teresting to know when CSSR could correct an erro-
consistently higher than the number needed by CSSR.          neous initial partition. (2) HMMs are models of dy-
Table 2 gives the results of a completely parallel pro-      namical systems without inputs. Partially-observable
cedure applied to the seven-state process.                   Markov decision processes (POMDPs) model systems
                                                             with inputs, i.e., controlled dynamical systems. The
CSSR, like the VLMM methods, is a constructive ap-           causal state theory we have used generalizes naturally
proach. Cross-validation is not constructive but se-         to this setting [1, ch. 7], where it is especially closely
lective. In our case, starting with fully-connected          connected to PSRs. Suffix-tree methods can induce
models (which, again, is a standard heuristic), cross-       POMDPs from data [23, 27, 28], and we believe CSSR
validated expectation-maximization never selected a          can be adapted to reconstruct POMDPs. This would
model whose structure corresponded to the minimal            provide a discovery procedure for PSRs.
sufficient statistic of the data-generating process. In
both cases, the generalization of HMMs with more
states worsened as the data-length grew, so cross-           Acknowledgments
validation increasingly favored small HMMs which,
while bad predictors, at least did not over-fit. Had         For support, we thank the Santa Fe Institute (under
                                                             grants from Intel, the NSF and the MacArthur Foun-
models with the correct structure been in the initial        dation, and DARPA cooperative agreement F30602-00-2-
population of candidates, they doubtless would have          0583), the NSF Research Experience for Undergraduates
done quite well, and the gap in predictive performance       Program (KLS), and the James S. McDonnell Foundation
between CSSR and cross-validation would be much              (CRS). Thanks to D. J. Albers, S. S. Baveja, P.-M. Binder,
smaller. Even when we have such prior architectural          J. P. Crutchfield, D. P. Feldman, R. Haslinger, M. Jones,
                                                             C. Moore, S. Page, A. J. Palmer, A. Ray, D. E. Smith, D.
knowledge, CSSR will typically be faster than cross-         Varn and anonymous referees for suggestions, R. Haslinger
validated EM, which involves performing nonlinear op-        for reading the MS., J. Lindsey and S. Iacus for R help,
timization on multiple model structures.                     E. van Nimwegen for providing a preprint of [29] and sug-
gesting that something similar might infer causal states, K.     [15] L. Devroye and G. Lugosi. Combinatorial Methods in
Kedi for moral support in programming and writing, and                Density Estimation. Springer-Verlag, Berlin, 2001.
G. Richardson for initiating our collaboration.
                                                                 [16] J. Feldman and J. F. Hanna. The structure of re-
                                                                      sponses to a sequence of binary events. Journal of
References                                                            Mathematical Psychology, 3:371–387, 1966.

 [1] C. R. Shalizi. Causal Architecture, Complexity and          [17] K. Marton and P. C. Shields. Entropy and the con-
     Self-Organization in Time Series and Cellular Au-                sistent estimation of joint distributions. The Annals
     tomata. PhD thesis, University of Wisconsin-Madison,             of Probability, 23:960–977, 1994. See also Correction,
     2001. http://bactra.org/thesis/.                                 Annals of Probability, 24 (1996): 541–545.

 [2] C. R. Shalizi, K. L. Shalizi, and J. P. Crutchfield.        [18] J. Rissanen. A universal data compression system.
     An algorithm for pattern discovery in time series.               IEEE Transactions on Information Theory, 29:656–
     Technical Report 02-10-060, Santa Fe Institute, 2002.            664, 1983.
     arxiv.org/abs/cs.LG/0210025.
                                                                 [19] P. Bühlmann and A. J. Wyner. Variable length
 [3] S. Kullback. Information Theory and Statistics. Dover            Markov chains. The Annals of Statistics, 27:480–513,
     Books, New York, 2nd edition, 1968.                              1999.

 [4] D. Blackwell and M. A. Girshick. Theory of Games            [20] F. Willems, Y. Shtarkov, and T. Tjalkens. The
     and Statistical Decisions. Wiley, New York, 1954.                context-tree weighting method: Basic properties.
                                                                      IEEE Transactions on Information Theory, 41:653–
 [5] J. P. Crutchfield and K. Young. Inferring statisti-              664, 1995.
     cal complexity. Physical Review Letters, 63:105–108,
     1989.                                                       [21] P. Tino and G. Dorffner. Predicting the future of
                                                                      discrete sequences from fractal representations of the
 [6] C. R. Shalizi and J. P. Crutchfield. Computational               past. Machine Learning, 45:187–217, 2001.
     mechanics: Pattern and prediction, structure and sim-
                                                                 [22] M. B. Kennel and A. I. Mees. Context-tree modeling
     plicity. Journal of Statistical Physics, 104:817–879,
                                                                      of observed symbolic dynamics. Physical Review E,
     2001. arxiv.org/abs/cond-mat/9907176.
                                                                      66:056209, 2002.
 [7] F. B. Knight. A predictive view of continuous time
                                                                 [23] D. Ron, Y. Singer, and N. Tishby. The power of am-
     processes. The Annals of Probability, 3:573–596, 1975.
                                                                      nesia: Learning probabilistic automata with variable
 [8] W. C. Salmon. Scientific Explanation and the Causal              memory length. Machine Learning, 25:117–149, 1996.
     Structure of the World. Princeton University Press,         [24] B. Weiss. Subshifts of finite type and sofic systems.
     Princeton, 1984.                                                 Monatshefte für Mathematik, 77:462–474, 1973.
 [9] M. L. Littman, R. S. Sutton, and S. Singh. Predictive       [25] R. Badii and A. Politi. Complexity: Hierarchical
     representations of state. In T. G. Dietterich, S. Becker,        Structures and Scaling in Physics. Cambridge Uni-
     and Z. Ghahramani, editors, Advances in Neural In-               versity Press, Cambridge, 1997.
     formation Processing Systems 14, pages 1555–1561,
     Cambridge, Massachusetts, 2002. MIT Press.                  [26] T. Hastie, R. Tibshirani, and J. Friedman. The Ele-
                                                                      ments of Statistical Learning: Data Mining, Inference,
[10] S. Singh, M. L. Littman, N. K. Jong, D. Pardoe, and              and Prediction. Springer-Verlag, New York, 2001.
     P. Stone. Learning predictive state representations.
     In T. Fawcett and N. Mishra, editors, Proceedings of        [27] R. A. McCallum. Instance-based utile distinctions for
     the Twentieth International Conference on Machine                reinforcement learning with hidden state. In A. Priedi-
     Learning (ICML-2003), pages 712–719. AAAI Press,                 tis and S. J. Russell, editors, Proceedings of the Twelth
     2003.                                                            International Machine Learning Conference (ICML
                                                                      1995), pages 387–395, San Francisco, 1995. Morgan
[11] J. Pearl. Causality: Models, Reasoning, and Infer-               Kauffman.
     ence. Cambridge University Press, Cambridge, Eng-
     land, 2000.                                                 [28] H. Jaeger. Observable operator models for discrete
                                                                      stochastic time series. Neural Computation, 12:1371–
[12] H. R. Lewis and C. H. Papadimitriou. Elements of the             1398, 2000.
     Theory of Computation. Prentice-Hall, Upper Saddle
     River, New Jersey, second edition, 1998.                    [29] H. J. Bussemaker, H. Li, and E. D. Siggia. Building a
                                                                      dictionary for genomes: Identification of presumptive
[13] D. R. Upper.           Theory and Algorithms                     regulatory sites by statistical analysis. Proceedings
     for  Hidden    Markov   Models  and    General-                  of the National Academy of Sciences, 97:10096–10100,
     ized Hidden Markov Models.          PhD the-                     2000.
     sis, University of California, Berkeley, 1997.
     http://www.santafe.edu/projects/CompMech/
     papers/TAHMMGHMM.html.

[14] T. M. Cover and J. A. Thomas. Elements of Informa-
     tion Theory. Wiley, New York, 1991.
