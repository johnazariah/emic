#

**Source:** hsu2012spectral
**Author:**
**Pages:** 30

---

## Full Text

                                             A Spectral Algorithm for Learning Hidden Markov Models
                                                             Daniel Hsu1,2 , Sham M. Kakade2 , and Tong Zhang1
                                                                   1
                                                                    Rutgers University, Piscataway, NJ 08854
                                                            2
                                                                University of Pennsylvania, Philadelphia, PA 19104
arXiv:0811.4413v6 [cs.LG] 6 Jul 2012


                                                                                      Abstract
                                                Hidden Markov Models (HMMs) are one of the most fundamental and widely used statistical
                                            tools for modeling discrete time series. In general, learning HMMs from data is computationally
                                            hard (under cryptographic assumptions), and practitioners typically resort to search heuristics
                                            which suffer from the usual local optima issues. We prove that under a natural separation
                                            condition (bounds on the smallest singular value of the HMM parameters), there is an efficient
                                            and provably correct algorithm for learning HMMs. The sample complexity of the algorithm
                                            does not explicitly depend on the number of distinct (discrete) observations—it implicitly de-
                                            pends on this quantity through spectral properties of the underlying HMM. This makes the
                                            algorithm particularly applicable to settings with a large number of observations, such as those
                                            in natural language processing where the space of observation is sometimes the words in a lan-
                                            guage. The algorithm is also simple, employing only a singular value decomposition and matrix
                                            multiplications.


                                       1    Introduction
                                       Hidden Markov Models (HMMs) (Baum and Eagon, 1967; Rabiner, 1989) are the workhorse sta-
                                       tistical model for discrete time series, with widely diverse applications including automatic speech
                                       recognition, natural language processing (NLP), and genomic sequence modeling. In this model, a
                                       discrete hidden state evolves according to some Markovian dynamics, and observations at a partic-
                                       ular time depend only on the hidden state at that time. The learning problem is to estimate the
                                       model only with observation samples from the underlying distribution. Thus far, the predominant
                                       learning algorithms have been local search heuristics, such as the Baum-Welch / EM algorithm
                                       (Baum et al., 1970; Dempster et al., 1977).
                                           It is not surprising that practical algorithms have resorted to heuristics, as the general learning
                                       problem has been shown to be hard under cryptographic assumptions (Terwijn, 2002). Fortunately,
                                       the hardness results are for HMMs that seem divorced from those that we are likely to encounter
                                       in practical applications.
                                           The situation is in many ways analogous to learning mixture distributions with samples from
                                       the underlying distribution. There, the general problem is also believed to be hard. However,
                                       much recent progress has been made when certain separation assumptions are made with respect
                                       to the component mixture distributions (e.g. (Dasgupta, 1999; Dasgupta and Schulman, 2007;
                                       Vempala and Wang, 2002; Chaudhuri and Rao, 2008; Brubaker and Vempala, 2008)). Roughly
                                       speaking, these separation assumptions imply that with high probability, given a point sampled


                                                                                           1
from the distribution, one can determine the mixture component that generated the point. In fact,
there is a prevalent sentiment that we are often only interested in clustering when such a separation
condition holds. Much of the theoretical work here has focused on how small this separation can
be and still permit an efficient algorithm to recover the model.
    We present a simple and efficient algorithm for learning HMMs under a certain natural sepa-
ration condition. We provide two results for learning. The first is that we can approximate the
joint distribution over observation sequences of length t (here, the quality of approximation is mea-
sured by total variation distance). As t increases, the approximation quality degrades polynomially.
Our second result is on approximating the conditional distribution over a future observation, condi-
tioned on some history of observations. We show that this error is asymptotically bounded—i.e. for
any t, conditioned on the observations prior to time t, the error in predicting the t-th outcome is
controlled. Our algorithm can be thought of as ‘improperly’ learning an HMM in that we do not
explicitly recover the transition and observation models. However, our model does maintain a hid-
den state representation which is closely (in fact, linearly) related to the HMM’s, and can be used
for interpreting the hidden state.
    The separation condition we require is a spectral condition on both the observation matrix and
the transition matrix. Roughly speaking, we require that the observation distributions arising from
distinct hidden states be distinct (which we formalize by singular value conditions on the observation
matrix). This requirement can be thought of as being weaker than the separation condition for
clustering in that the observation distributions can overlap quite a bit—given one observation,
we do not necessarily have the information to determine which hidden state it was generated
from (unlike in the clustering literature). We also have a spectral condition on the correlation
between adjacent observations. We believe both of these conditions to be quite reasonable in many
practical applications. Furthermore, given our analysis, extensions to our algorithm which relax
these assumptions should be possible.
    The algorithm we present has both polynomial sample and computational complexity. Compu-
tationally, the algorithm is quite simple—at its core is a singular value decomposition (SVD) of a
correlation matrix between past and future observations. This SVD can be viewed as a Canonical
Correlation Analysis (CCA) (Hotelling, 1935) between past and future observations. The sam-
ple complexity results we present do not explicitly depend on the number of distinct observations;
rather, they implicitly depend on this number through spectral properties of the HMM. This makes
the algorithm particularly applicable to settings with a large number of observations, such as those
in NLP where the space of observations is sometimes the words in a language.

1.1   Related Work
There are two ideas closely related to this work. The first comes from the subspace identification
literature in control theory (Ljung, 1987; Overschee and Moor, 1996; Katayama, 2005). The second
idea is that, rather than explicitly modeling the hidden states, we can represent the probabilities of
sequences of observations as products of matrix observation operators, an idea which dates back to
the literature on multiplicity automata (Schützenberger, 1961; Carlyle and Paz, 1971; Fliess, 1974).
    The subspace identification methods, used in control theory, use spectral approaches to discover
the relationship between hidden states and the observations. In this literature, the relationship is
discovered for linear dynamical systems such as Kalman filters. The basic idea is that the rela-
tionship between observations and hidden states can often be discovered by spectral/SVD methods
correlating the past and future observations (in particular, such methods often do a CCA between

                                                  2
the past and future observations). However, algorithms presented in the literature cannot be di-
rectly used to learn HMMs because they assume additive noise models with noise distributions
independent of the underlying states, and such models are not suitable for HMMs (an exception
is (Andersson et al., 2003)). In our setting, we use this idea of performing a CCA between past
and future observations to uncover information about the observation process (this is done through
an SVD on a correlation matrix between past and future observations). The state-independent
additive noise condition is avoided through the second idea.
    The second idea is that we can represent the probability of sequences as products of matrix op-
erators, as in the literature on multiplicity automata (Schützenberger, 1961; Carlyle and Paz, 1971;
Fliess, 1974) (see (Even-Dar et al., 2005) for discussion of this relationship). This idea was re-used
in both the Observable Operator Model of Jaeger (2000) and the Predictive State Representations
of Littman et al. (2001), both of which are closely related and both of which can model HMMs. In
fact, the former work by Jaeger (2000) provides a non-iterative algorithm for learning HMMs, with
an asymptotic analysis. However, this algorithm assumed knowing a set of ‘characteristic events’,
which is a rather strong assumption that effectively reveals some relationship between the hidden
states and observations. In our algorithm, this problem is avoided through the first idea.
    Some of the techniques in the work in (Even-Dar et al., 2007) for tracking belief states in an
HMM are used here. As discussed earlier, we provide a result showing how the model’s conditional
distributions over observations (conditioned on a history) do not asymptotically diverge. This
result was proven in (Even-Dar et al., 2007) when an approximate model is already known. Roughly
speaking, the reason this error does not diverge is that the previous observations are always revealing
information about the next observation; so with some appropriate contraction property, we would
not expect our errors to diverge. Our work borrows from this contraction analysis.
    Among recent efforts in various communities (Andersson et al., 2003; Vanluyten et al., 2007;
Zhao and Jaeger, 2007; Cybenko and Crespi, 2008), the only previous efficient algorithm shown to
PAC-learn HMMs in a setting similar to ours is due to Mossel and Roch (2006). Their algorithm
for HMMs is a specialization of a more general method for learning phylogenetic trees from leaf
observations. While both this algorithm and ours rely on the same rank condition and compute
similar statistics, they differ in two significant regards. First, (Mossel and Roch, 2006) were not
concerned with large observation spaces, and thus their algorithm assumes the state and observation
spaces to have the same dimension. In addition, (Mossel and Roch, 2006) take the more ambitious
approach of learning the observation and transition matrices explicitly, which unfortunately results
in a less sample-efficient algorithm that injects noise to artificially spread apart the eigenspectrum
of a probability matrix. Our algorithm avoids recovering the observation and transition matrix
explicitly1 , and instead uses subspace identification to learn an alternative representation.


2       Preliminaries
2.1     Hidden Markov Models
The HMM defines a probability distribution over sequences of hidden states (ht ) and observations
(xt ). We write the set of hidden states as [m] = {1, . . . , m} and set of observations as [n] =
    1
    In Appendix C, we discuss the key step in (Mossel and Roch, 2006), and also show how to use their technique
in conjunction with our algorithm to recover the HMM observation and transition matrices. Our algorithm does not
rely on this extra step—we believe it to be generally unstable—but it can be taken if desired.


                                                       3
{1, . . . , n}, where m ≤ n.
    Let T ∈ Rm×m be the state transition probability matrix with Tij = Pr[ht+1 = i|ht = j],
O ∈ Rn×m be the observation probability matrix with Oij = Pr[xt = i|ht = j], and ~π ∈ Rm
be the initial state distribution with ~πi = Pr[h1 = i]. The conditional independence properties
that an HMM satisfies are: 1) conditioned on the previous hidden state, the current hidden state
is sampled independently of all other events in the history; and 2) conditioned on the current
hidden state, the current observation is sampled independently from all other events in the history.
These conditional independence properties of the HMM imply that T and O fully characterize the
probability distribution of any sequence of states and observations.
    A useful way of computing the probability of sequences is in terms of ‘observation operators’,
an idea which dates back to the literature on multiplicity automata (see (Schützenberger, 1961;
Carlyle and Paz, 1971; Fliess, 1974)). The following lemma is straightforward to verify (see (Jaeger,
2000; Even-Dar et al., 2007)).

Lemma 1. For x = 1, . . . , n, define

                                        Ax = T diag(Ox,1 , . . . , Ox,m ).

For any t:
                                     Pr[x1 , . . . , xt ] = ~1⊤
                                                              m Axt . . . Ax1 ~
                                                                              π.

    Our algorithm learns a representation that is based on this observable operator view of HMMs.

2.2    Notation
As already used in Lemma 1, the vector ~1m is the all-ones vector in Rm . We denote by x1:t the
sequence (x1 , . . . , xt ), and by xt:1 its reverse (xt , . . . , x1 ). When we use a sequence as a subscript, we
mean the product of quantities indexed by the sequence elements. So for example, the probability
calculation in Lemma 1 can be written ~1⊤          m Axt:1 ~ π . We will use ~ht to denote a probability vector
(a distribution over hidden states), with the arrow distinguishing it from the random hidden state
variable ht . Additional notation used in the theorem statements and proofs is listed in Table 1.

2.3    Assumptions
We assume the HMM obeys the following condition.

Condition 1 (HMM Rank Condition). ~π > 0 element-wise, and O and T are rank m.

    The rank condition rules out the problematic case in which some state i has an output distri-
bution equal to a convex combination (mixture) of some other states’ output distributions. Such
a case could cause a learner to confuse state i with a mixture of these other states. As mentioned
before, the general task of learning HMMs (even the specific goal of simply accurately modeling
the distribution probabilities (Terwijn, 2002)) is hard under cryptographic assumptions; the rank
condition is a natural way to exclude the malicious instances created by the hardness reduction.
    The rank condition on O can be relaxed through a simple modification of our algorithm that
looks at multiple observation symbols simultaneously to form the probability estimation tables. For
example, if two hidden states have identical observation probability in O but different transition
probabilities in T , then they may be differentiated by using two consecutive observations. Although

                                                         4
our analysis can be applied in this case with minimal modifications, for clarity, we only state our
results for an algorithm that estimates probability tables with rows and columns corresponding to
single observations.

2.4   Learning Model
Our learning model is similar to those of (Kearns et al., 1994; Mossel and Roch, 2006) for PAC-
learning discrete probability distributions. We assume we can sample observation sequences from
an HMM. In particular, we assume each sequence is generated starting from the same initial state
distribution (e.g. the stationary distribution of the Markov chain specified by T ). This setting is
valid for practical applications including speech recognition, natural language processing, and DNA
sequence modeling, where multiple independent sequences are available.
    For simplicity, this paper only analyzes an algorithm that uses the initial few observations of each
sequence, and ignores the rest. We do this to avoid using concentration bounds with complicated
mixing conditions for Markov chains in our sample complexity calculation, as these conditions are
not essential to the main ideas we present. In practice, however, one should use the full sequences
to form the probability estimation tables required by our algorithm. In such scenarios, a single
long sequence is sufficient for learning, and the effective sample size can be simply discounted by
the mixing rate of the underlying Markov chain.
    Our goal is to derive accurate estimators for the cumulative (joint) distribution Pr[x1:t ] and
the conditional distribution Pr[xt |x1:t−1 ] for any sequence length t. For the conditional distribu-
tion, we obtain an approximation that does not depend on t, while for the joint distribution, the
approximation quality degrades gracefully with t.


3     Observable Representations of Hidden Markov Models
A typical strategy for learning HMMs is to estimate the observation and transition probabilities for
each hidden state (say, by maximizing the likelihood of a sample). However, since the hidden states
are not directly observed by the learner, one often resorts to heuristics (e.g. EM) that alternate
between imputing the hidden states and selecting parameters O    b and Tb that maximize the likelihood
of the sample and current state estimates. Such heuristics can suffer from local optima issues and
require careful initialization (e.g. an accurate guess of the hidden states) to avoid failure.
    However, under Condition 1, HMMs admit an efficiently learnable parameterization that de-
pends only on observable quantities. Because such quantities can be estimated from data, learning
this representation avoids any guesswork about the hidden states and thus allows for algorithms
with strong guarantees of success.
    This parameterization is natural in the context of Observable Operator Models (Jaeger, 2000),
but here we emphasize its connection to subspace identification.

3.1   Definition
Our HMM representation is defined in terms of the following vector and matrix quantities:

                              [P1 ]i = Pr[x1 = i]
                           [P2,1 ]ij   = Pr[x2 = i, x1 = j]
                         [P3,x,1 ]ij   = Pr[x3 = i, x2 = x, x1 = j]   ∀x ∈ [n],

                                                    5
where P1 ∈ Rn is a vector, and P2,1 ∈ Rn×n and the P3,x,1 ∈ Rn×n are matrices. These are the
marginal probabilities of observation singletons, pairs, and triples.
   The representation further depends on a matrix U ∈ Rn×m that obeys the following condition.

Condition 2 (Invertibility Condition). U ⊤ O is invertible.

    In other words, U defines an m-dimensional subspace that preserves the state dynamics—this
will become evident in the next few lemmas.
    A natural choice for U is given by the ‘thin’ SVD of P2,1 , as the next lemma exhibits.

Lemma 2. Assume ~π > 0 and that O and T have column rank m. Then rank(P2,1 ) = m. Moreover,
if U is the matrix of left singular vectors of P2,1 corresponding to non-zero singular values, then
range(U ) = range(O), so U ∈ Rn×m obeys Condition 2.

Proof. Using the conditional independence properties of the HMM, entries of the matrix P2,1 can
be factored as
                                        m X
                                        X m
                          [P2,1 ]ij =             Pr[x2 = i, x1 = j, h2 = k, h1 = ℓ]
                                        k=1 ℓ=1
                                        Xm X m
                                  =               Oik Tkℓ ~πℓ [O ⊤ ]ℓj
                                        k=1 ℓ=1

so P2,1 = OT diag(~π )O ⊤ and thus range(P2,1 ) ⊆ range(O). The assumptions on O, T , and ~π imply
that T diag(~π )O⊤ has linearly independent rows and that P2,1 has m non-zero singular values.
Therefore
                                     O = P2,1 (T diag(~π )O ⊤ )+
(where X + denotes the Moore-Penrose pseudo-inverse of a matrix X (Stewart and Sun, 1990)),
which in turn implies range(O) ⊆ range(P2,1 ). Thus rank(P2,1 ) = rank(O) = m, and also
range(U ) = range(P2,1 ) = range(O).

    Our algorithm is motivated by Lemma 2 in that we compute the SVD of an empirical estimate
of P2,1 to discover a U that satisfies Condition 2. We also note that this choice for U can be thought
of as a surrogate for the observation matrix O (see Remark 5).
    Now given such a matrix U , we can finally define the observable representation:
                               ~b1 = U ⊤ P1
                                            +
                             ~b∞ =      ⊤
                                      P2,1 U    P1
                                                       +
                              Bx =    U ⊤ P3,x,1 U ⊤ P2,1                ∀x ∈ [n] .

3.2    Basic Properties
The following lemma shows that the observable representation, parameterized by {~b∞ , ~b1 , B1 , . . . , Bn },
is sufficient to compute the probabilities of any sequence of observations.

Lemma 3 (Observable HMM Representation). Assume the HMM obeys Condition 1 and that
U ∈ Rn×m obeys Condition 2. Then:

                                                          6
  1. ~b1 = (U ⊤ O)~π .

  2. ~b⊤   ~ ⊤ ⊤ −1
       ∞ = 1m (U O) .

  3. Bx = (U ⊤ O)Ax (U ⊤ O)−1 ∀x ∈ [n].

  4. Pr[x1:t ] = ~b⊤      ~
                   ∞ Bxt:1 b1 ∀t ∈ N, x1 , . . . , xt ∈ [n].

    In addition to joint probabilities, we can compute conditional probabilities using the observable
representation. We do so through (normalized) conditional ‘internal states’ that depend on a history
of observations. We should emphasize that these states are not in fact probability distributions over
hidden states (though the following lemma shows that they are linearly related). As per Lemma 3,
the initial state is
                                            ~b1 = (U ⊤ O)~π .

Generally, for any t ≥ 1, given observations x1:t−1 with Pr[x1:t−1 ] > 0, we define the internal state
as:
                                                              ~
                                 ~bt = ~bt (x1:t−1 ) = Bxt−1:1 b1 .
                                                      ~b⊤ Bx    ~b1
                                                                 ∞       t−1:1


 The case t = 1 is consistent with the general definition of ~bt because the denominator is ~b⊤ ~
                                                                                              ∞ b1 =
~1⊤   ⊤   −1   ⊤
  m (U O) (U O)~
                        ~ ⊤
                   π = 1m~π = 1. The following result shows how these internal states can be used
 to compute conditional probabilities Pr[xt = i|x1:t−1 ].

Lemma 4 (Conditional Internal States). Assume the conditions in Lemma 3. Then, for any time
t:

  1. (Recursive update of states) If Pr[x1:t ] > 0, then

                                                  ~bt+1 =     Bxt~bt
                                                                       ,
                                                            ~b⊤ Bx ~bt
                                                               ∞     t


  2. (Relation to hidden states)
                                             ~bt = (U ⊤ O) ~ht (x1:t−1 )

     where [~ht (x1:t−1 )]i = Pr[ht = i|x1:t−1 ] is the conditional probability of the hidden state at
     time t given the observations x1:t−1 ,

  3. (Conditional observation probabilities)

                                            Pr[xt |x1:t−1 ] = ~b⊤    ~
                                                                ∞ Bxt bt .


Remark 5. If U is the matrix of left singular vectors of P2,1 corresponding to non-zero singular
values, then U acts much like the observation probability matrix O in the following sense:

               Given a conditional state ~bt ,                 Given a conditional hidden state ~ht ,
                Pr[xt = i|x1:t−1 ] = [U~bt ]i .                     Pr[xt = i|x1:t−1 ] = [O~ht ]i .

To see this, note that U U ⊤ is the projection operator to range(U ). Since range(U ) = range(O)
(Lemma 2), we have U U ⊤ O = O, so U~bt = U (U ⊤ O)~ht = O~ht .

                                                       7
3.3   Proofs
Proof of Lemma 3. The first claim is immediate from the fact P1 = O~π . For the second claim, we
write P1 in the following unusual (but easily verified) form:
                              P1⊤ = ~1⊤        π )O⊤
                                      m T diag(~
                                  = ~1⊤    ⊤   −1   ⊤
                                                          π )O ⊤
                                      m (U O) (U O)T diag(~
                                     = ~1⊤   ⊤  −1 ⊤
                                         m (U O) U P2,1 .

The matrix U ⊤ P2,1 has linearly independent rows (by the assumptions on ~π , O, T , and the condition
on U ), so
           ~b⊤ = P ⊤ (U ⊤ P2,1 )+ = ~1⊤ (U ⊤ O)−1 (U ⊤ P2,1 ) (U ⊤ P2,1 )+ = ~1⊤ (U ⊤ O)−1 .
            ∞        1                   m                                           m

To prove the third claim, we first express P3,x,1 in terms of Ax :
                            P3,x,1 = OAx T diag(~π )O⊤
                                     = OAx (U ⊤ O)−1 (U ⊤ O)T diag(~π )O ⊤
                                     = OAx (U ⊤ O)−1 U ⊤ P2,1 .
Again, using the fact that U ⊤ P2,1 has full row rank,
                                                        +
                       Bx =        U ⊤ P3,x,1     U ⊤ P2,1
                                                                       +
                            = (U ⊤ O)Ax (U ⊤ O)−1 U ⊤ P2,1       U ⊤ P2,1
                             = (U ⊤ O)Ax (U ⊤ O)−1 .
The probability calculation in the fourth claim is now readily seen as a telescoping product that
reduces to the product in Lemma 1.
Proof of Lemma 4. The first claim is a simple induction. The second and third claims are also
proved by induction as follows. The base case is clear from Lemma 3 since ~h1 = ~π and ~b1 = (U ⊤ O)~π ,
and also ~b⊤    ~     ~⊤
           ∞ Bx1 b1 = 1m Ax1 ~
                             π = Pr[x1 ]. For the inductive step,

                          ~bt+1 =       Bxt~bt
                                      ~b⊤ Bx ~bt
                                       ∞     t

                                      Bxt (U ⊤ O)~ht
                                 =                          (inductive hypothesis)
                                      Pr[xt |x1:t−1 ]
                                      (U ⊤ O)Ax ~ht
                                              t
                                 =                   (Lemma 3)
                                   Pr[xt |x1:t−1 ]
                                           Pr[ht+1 = ·, xt |x1:t−1 ]
                                 = (U ⊤ O)
                                                  Pr[xt |x1:t−1 ]
                                           Pr[ht+1 = ·|x1:t ] Pr[xt |x1:t−1 ]
                                 = (U ⊤ O)
                                                      Pr[xt |x1:t−1 ]
                                      ⊤    ~
                                 = (U O) ht+1 (x1:t )
and
                           ~b⊤ Bx ~bt+1 = ~1⊤ Ax ~ht+1 = Pr[xt+1 |x1:t ]
                             ∞   t+1        m   t+1

(again, using Lemma 3).

                                                        8
      Algorithm LearnHMM(m, N ):
      Inputs: m - number of states, N - sample size
      Returns: HMM model parameterized by {bb1 , bb∞ , B
                                                       bx ∀x ∈ [n]}

        1. Independently sample N observation triples (x1 , x2 , x3 ) from the HMM to form
           empirical estimates Pb1 , Pb2,1 , Pb3,x,1 ∀x ∈ [n] of P1 , P2,1 , P3,x,1 ∀x ∈ [n].

        2. Compute the SVD of Pb2,1 , and let Ub be the matrix of left singular vectors corre-
           sponding to the m largest singular values.

        3. Compute model parameters:

            (a) b    b ⊤ Pb1 ,
                b1 = U
            (b) b
                b∞ = (Pb⊤ U
                          2,1
                             b )+ P1 ,
                bx = U
            (c) B    b ⊤ Pb3,x,1 (U
                                  b ⊤ Pb2,1 )+ ∀x ∈ [n].


                                   Figure 1: HMM learning algorithm.

4     Spectral Learning of Hidden Markov Models
4.1    Algorithm
The representation in the previous section suggests the algorithm detailed in Figure 1, which simply
uses random samples to estimate the model parameters. Note that in practice, knowing m is not
essential because the method presented here tolerates models that are not exactly HMMs, and the
parameter m may be tuned using cross-validation. As we discussed earlier, the requirement for
independent samples is only for the convenience of our sample complexity analysis.
    The model returned by LearnHMM(m, N ) can be used as follows:

    • To predict the probability of a sequence:
                                         c 1 , . . . , xt ] = bb⊤ B
                                         Pr[x                     b        b b
                                                                ∞ xt . . . Bx1 b1 .


    • Given an observation xt , the ‘internal state’ update is:

                                                               Bbxtb
                                                                   bt
                                                  bbt+1 =               .
                                                             bb⊤ B
                                                                 bx bbt
                                                               ∞    t


    • To predict the conditional probability of xt given x1:t−1 :
                                                            b⊤ b b
                                           c t |x1:t−1 ] = Pb∞ Bxt bt .
                                           Pr[x
                                                               b⊤ b b
                                                             x b∞ Bx bt

    Aside from the random sampling, the running time of the learning algorithm is dominated
by the SVD computation of an n × n matrix. The time required for computing joint probability
calculations is O(tm2 ) for length t sequences—same as if one used the ordinary HMM parameters (O

                                                         9
and T ). For conditional probabilities, we require some extra work (proportional to n) to compute
the normalization factor. However, our analysis shows that this normalization factor is always close
to 1 (see Lemma 13), so it can be safely omitted in many applications.
    Note that the algorithm does not explicitly ensure that the predicted probabilities lie in the
range [0, 1]. This is a dreaded problem that has been faced by other methods for learning and using
general operator models Jaeger (2000), and a number of heuristic for coping with the problem have
been proposed and may be applicable here (see Jaeger et al. (2006) for some recent developments).
We briefly mention that in the case of joint probability prediction, clipping the predictions to the
interval [0, 1] can only increase the L1 accuracy, and that the KL accuracy guarantee explicitly
requires the predicted probabilities to be non-zero.

4.2     Main Results
We now present our main results. The first result is a guarantee on the accuracy of our joint prob-
ability estimates for observation sequences. The second result concerns the accuracy of conditional
probability estimates — a much more delicate quantity to bound due to conditioning on unlikely
events. We also remark that if the probability distribution is only approximately modeled as an
HMM, then our results degrade gracefully based on this approximation quality.

4.2.1     Joint Probability Accuracy
Let σm (M ) denote the mth largest singular value of a matrix M . Our sample complexity bound
will depend polynomially on 1/σm (P2,1 ) and 1/σm (O).
    Also, define                                                         
                                  X                                      
                      ǫ(k) = min         Pr[x2 = j] : S ⊆ [n], |S| = n − k ,               (1)
                                                                         
                                            j∈S

and let
                                          n0 (ε) = min{k : ǫ(k) ≤ ε}.
In other words, n0 (ε) is the minimum number of observations that account for about 1 − ǫ of the
total probability mass. Clearly n0 (ε) ≤ n, but it can often be much smaller in real applications. For
example, in many practical applications, the frequencies of observation symbols observe a power law
(called Zipf’s law) of the form f (k) ∝ 1/k s , where f (k) is the frequency of the k-th most frequently
observed symbol. If s > 1, then ǫ(k) = O(k1−s ), and n0 (ε) = O(ε1/(1−s) ) becomes independent
of the number of observations n. This means that for such problems, our analysis below leads to
a sample complexity bound for the cumulative distribution Pr[x1:t ] that can be independent of n.
This is useful in domains with large n such as natural language processing.
Theorem 6. There exists a constant C > 0 such that the following holds. Pick any 0 < ǫ, η < 1
                                             √
and t ≥ 1, and let ε0 = σm (O)σm (P2,1 )ǫ/(4t m). Assume the HMM obeys Condition 1, and
                                                                        
                            t2             m              m · n0 (ε0 )          1
                   N ≥C· 2 ·             2        4
                                                    +        2         2
                                                                           · log .
                           ǫ     σm (O) σm (P2,1 )    σm (O) σm (P2,1 )         η
With probability at least 1 − η, the model returned by the algorithm LearnHMM(m, N ) satisfies
                               X
                                                             c 1 , . . . , xt ]| ≤ ǫ.
                                    | Pr[x1 , . . . , xt ] − Pr[x
                             x1 ,...,xt


                                                      10
    The main challenge in proving Theorem 6 is understanding how the estimation errors accumulate
in the algorithm’s probability calculation. This would have been less problematic if we had estimates
of the usual HMM parameters T and O; the fully observable representation forces us to deal with
more cumbersome matrix and vector products.

4.2.2   Conditional Probability Accuracy
                                                                                    c t |x1 , . . . , xt−1 ].
In this section, we analyze the accuracy of our conditional probability predictions Pr[x
Intuitively, we might hope that these predictive distributions do not become arbitrarily bad over
time, (as t → ∞). The reason is that while estimation errors propagate into long-term probabil-
ity predictions (as evident in Theorem 6), the history of observations constantly provides feedback
about the underlying hidden state, and this information is incorporated using Bayes’ rule (implicitly
via our internal state updates).
    This intuition was confirmed by Even-Dar et al. (2007), who showed that if one has an approx-
imate model of T and O for the HMM, then under certain conditions, the conditional prediction
does not diverge. This condition is the positivity of the ‘value of observation’ γ, defined as

                                           γ =      inf        kO~v k1 .
                                                 ~v :k~
                                                      vk1 =1

                        √
Note that γ ≥ σm (O)/ n, so it is guaranteed to be positive by Condition 1. However, γ can be
much larger than what this crude lower bound suggests.
    To interpret this quantity γ, consider any two distributions over hidden states ~h, b    h ∈ Rm .
Then kO(h − h)k1 ≥ γkh − hk1 . Regarding h as the true hidden state distribution and b
          ~    b           ~     b                 ~                                              h as
the estimated hidden state distribution, this inequality gives a lower bound on the error of the
estimated observation distributions under O. In other words, the observation process, on average,
reveal errors in our hidden state estimation. The work of (Even-Dar et al., 2007) uses this as a
contraction property to show how prediction errors (due to using an approximate model) do not
diverge. In our setting, this is more difficult as we do not explicitly estimate O nor do we explicitly
maintain distributions over hidden states.
    We also need the following assumption, which we discuss further following the theorem state-
ment.

Condition 3 (Stochasticity Condition). For all observations x and all states i and j, [Ax ]ij ≥ α >
0.

Theorem 7. There exists a constant C > 0 such that the following holds. Pick any 0 < ǫ, η < 1,
                                 √
and let ε0 = σm (O)σm (P2,1 )ǫ/(4 m). Assume the HMM obeys Conditions 1 and 3, and
                                                                                 
                    m      (log(2/α))4             m            1    m · n0 (ε0 )          1
     N ≥ C·         2 2
                        +      4 2  4
                                         ·       2          4
                                                              + 2·      2         2
                                                                                      · log .
                   ǫ α        ǫ α γ        σm (O) σm (P2,1 )   ǫ σm (O) σm (P2,1 )         η

With probability at least 1 − η, then the model returned by LearnHMM(m, N ) satisfies, for any
time t,
                                                                             "                     #
                                          c t |x1 , . . . , xt−1 ]) = Ex         Pr[x t |x 1:t−1 ]
         KL(Pr[xt |x1 , . . . , xt−1 ] || Pr[x                                ln                     ≤ ǫ.
                                                                         1:t
                                                                                 c t |x1:t−1 ]
                                                                                 Pr[x


                                                     11
    To justify our choice of error measure, note that the problem of bounding the errors of condi-
tional probabilities is complicated by the issue of that, over the long run, we may have to condition
on a very low probability event. Thus we need to control the relative accuracy of our predictions.
This makes the KL-divergence a natural choice for the error measure. Unfortunately, because our
HMM conditions are more naturally interpreted in terms of spectral and normed quantities, we
end up switching back and forth between KL and L1 errors via Pinsker-style inequalities (as in
(Even-Dar et al., 2007)). It is not clear to us if a significantly better guarantee could be obtained
with a pure L1 error analysis (nor is it clear how to do such an analysis).
    The analysis in (Even-Dar et al., 2007) (which assumed that approximations to T and O were
provided) dealt with this problem of dividing by zero (during a Bayes’ rule update) by explicitly
modifying the approximate model so that it never assigns the probability of any event to be zero
(since if this event occurred, then the conditional probability is no longer defined). In our setting,
Condition 3 ensures that true model never assigns the probability of any event to be zero. We can
relax this condition somewhat (so that we need not quantify over all observations), though we do
not discuss this here.
    We should also remark that while our sample complexity bound is significantly larger than in
Theorem 6, we are also bounding the more stringent KL-error measure on conditional distributions.

4.2.3    Learning Distributions ǫ-close to HMMs
Our L1 error guarantee for predicting joint probabilities still holds if the sample used to estimate
Pb1 , Pb2,1 , Pb3,x,1 come from a probability distribution Pr[·] that is merely close to an HMM. Specif-
ically, all we need is that there exists some tmax ≥ 3 and some m state HMM with distribution
PrHMM [·] such that:

  1. PrHMM satisfies Condition 1 (HMM Rank Condition),
                       P
  2. For all t ≤ tmax , x1:t | Pr[x1:t ] − PrHMM [x1:t ]| ≤ ǫHMM (t),

  3. ǫHMM (2) ≪ 21 σm (P2,1
                        HMM ).


The resulting error of our learned model Pr c is
                 X                                       X
                                   c 1:t ]| ≤ ǫHMM (t) +
                     | Pr[x1:t ] − Pr[x                                     c 1:t ]|
                                                           |PrHMM [x1:t ] − Pr[x
                 x1:t                                      x1:t

for all t ≤ tmax . The second term is now bounded as in Theorem 6, with spectral parameters
corresponding to PrHMM .

4.3     Subsequent Work
Following the initial publication of this work, Siddiqi, Boots, and Gordon have proposed various ex-
tensions to the LearnHMM algorithm and its analysis Siddiqi et al. (2010). First, they show that
the model parameterization used by our algorithm in fact captures the class of HMMs with rank m
transition matrices, which is more general than the class of HMMs with m hidden states. Second,
they propose extensions for using longer sequences in the parameter estimation, and also for han-
dling real-valued observations. These extensions prove to be useful in both synthetic experiments
and an application to tracking with video data.

                                                   12
    A recent work of Song, Boots, Siddiqi, Gordon, and Smola provides a kernelization of our
model parameterization in the context of Hilbert space embeddings of (conditional) probability
distributions, and extends various aspects of the LearnHMM algorithm and analysis to this set-
ting Song et al. (2010). This extension is also shown to be advantageous in a number of applications.


5     Proofs
Throughout this section, we assume the HMM obeys Condition 1. Table 1 summarizes the notation
that will be used throughout the analysis in this section.

                 m, n                    Number of states and observations
                 n0 (ε)                  Number of significant observations
                 O, T , Ax               HMM parameters
                 P1 , P2,1 , P3,x,1      Marginal probabilities
                 Pb1 , Pb2,1 , Pb3,x,1   Empirical marginal probabilities
                 ǫ1 , ǫ2,1 , ǫ3,x,1      Sampling errors [Section 5.1]
                 Ub                      Matrix of m left singular vectors of Pb2,1
                eb∞ , B  ex , e
                              b1         True observable parameters using U       b [Section 5.1]
                bb∞ , B  bx , b
                              b1         Estimated observable parameters using U        b
                 δ∞ , ∆x , δ1            Parameter
                                         P            errors [Section 5.1]
                 ∆                          x ∆x [Section 5.1]
                 σm (M )                 m-th largest singular value of matrix M
                ~bt , bbt                True and estimated states [Section 5.3]
                ~ht , b ht , gbt                         b ⊤ O)−1b
                                          b ⊤ O)−1~bt , (U
                                         (U                       bt , b
                                                                       ht /(~1⊤ b
                                                                              m ht ) [Section 5.3]
                 Abx                      b O) B
                                         (U ⊤   −1 bx (Ub O) [Section 5.3]
                                                          ⊤

                 γ, α                    inf{kOvk1 : kvk1 = 1}, min{[Ax ]i,j }

                                         Table 1: Summary of notation.


5.1   Estimation Errors
Define the following sampling error quantities:

                                               ǫ1 = kPb1 − P1 k2
                                             ǫ2,1 = kPb2,1 − P2,1 k2
                                           ǫ3,x,1 = kPb3,x,1 − P3,x,1 k2

The following lemma bounds these errors with high probability as a function of the number of
observation samples used to form the estimates.

Lemma 8. If the algorithm independently samples N observation triples from the HMM, then with


                                                          13
probability at least 1 − η:
                                    r            r
                                        1   3        1
                          ǫ1 ≤            ln +
                                        N η          N
                                    r            r
                                        1   3        1
                        ǫ2,1 ≤            ln +
                                        N η          N
                                    r        r
                                     1   3      1
                 max ǫ3,x,1     ≤      ln +
                  x                  N η       N
                                        s         r          ! r        r
                  X                       k   3     k            1   3    1
                       ǫ3,x,1   ≤ min       ln +      + 2ǫ(k) +    ln +
                   x
                                   k      N η       N            N η      N

where ǫ(k) is defined in (1).

Proof. See Appendix A.

    The rest of the analysis estimates how the sampling errors affect the accuracies of the model
parameters (which in turn affect the prediction quality). We need some results from matrix per-
turbation theory, which are given in Appendix B.
    Let U ∈ Rn×m be matrix of left singular vectors of P2,1 . The first lemma implies that if Pb2,1 is
                                                                                                        b)
sufficiently close to P2,1 , i.e. ǫ2,1 is small enough, then the difference between projecting to range(U
and to range(U ) is small. In particular, U      b O will be invertible and be nearly as well-conditioned
                                                  ⊤
      ⊤
as U O.

Lemma 9. Suppose ǫ2,1 ≤ ε · σm (P2,1 ) for some ε < 1/2. Let ε0 = ǫ22,1 /((1 − ε)σm (P2,1 ))2 . Then:

  1. ε0 < 1,
         b ⊤ Pb2,1 ) ≥ (1 − ε)σm (P2,1 ),
  2. σm (U
         b ⊤ P2,1 ) ≥ √1 − ε0 σm (P2,1 ),
  3. σm (U
         b ⊤ O) ≥ √1 − ε0 σm (O).
  4. σm (U

Proof. The assumptions imply ε0 < 1. Since σm (Ub ⊤ Pb2,1 ) = σm (Pb2,1 ), the second claim is immediate
from Corollary 22.             n×m  be the matrix of left singular vectors of P2,1 . For any x ∈ Rm ,
                  q Let U ∈ R           √
kUb ⊤ U xk2 = kxk2 1 − kUb ⊤ U k2 ≥ kxk2 1 − ε0 by Corollary 22 and the fact ε0 < 1. The remaining
                                ⊥   2
claims follow.

   Now we will argue that the estimated parameters bb∞ , Bbx , bb1 are close to the following true
                                                   b is used for U :
parameters from the observable representation when U
               eb∞ = (P ⊤ U  b +           b ⊤ −⊤~1m ,
                         2,1 ) P1 = (U O)

                Bex = (Ub ⊤ P3,x,1 )(U
                                     b ⊤ P2,1 )+ = (U
                                                    b ⊤ O)Ax (U
                                                              b ⊤ O)−1    for x = 1, . . . , n,
                 eb1 = U
                       b ⊤ P1 .

By Lemma 3, as long as Ub ⊤ O is invertible, these parameters eb∞ , B
                                                                    ex , eb1 constitute a valid observable
representation for the HMM.

                                                         14
   Define the following errors of the estimated parameters:

            δ∞ =  b ⊤ O)⊤ (bb∞ − eb∞ )
                 (U                       = (U  b ⊤ O)⊤b
                                                       b∞ − ~1m     ,
                                       ∞                          ∞
                                      
                  b ⊤ O)−1 B
            ∆x = (U           bx − Bex (Ub ⊤ O)    = (U  b ⊤ O)−1 B
                                                                  bx (U
                                                                      b ⊤ O) − Ax ,
                                                1                                 1
                 X
             ∆ =   ∆x
                      x

             δ1 =      b ⊤ O)−1 (bb1 − eb1 )
                      (U                           =    b ⊤ O)−1bb1 − ~π
                                                       (U                      .
                                               1                           1

We can relate these to the sampling errors as follows.

Lemma 10. Assume ǫ2,1 ≤ σm (P2,1 )/3. Then:
                                                    
                               ǫ2,1            ǫ1
             δ∞ ≤ 4 ·                  +               ,
                           σm (P2,1 )2 3σm (P2,1 )
                              √                                              
                       8        m                        ǫ2,1          ǫ3,x,1
             ∆x ≤ √ ·               · Pr[x2 = x] ·                 +            ,
                        3 σm (O)                     σm (P2,1 )2 3σm (P2,1 )
                              √                      P            
                       8        m           ǫ2,1          x ǫ3,x,1
              ∆ ≤ √ ·               ·               +                ,
                        3 σm (O)         σm (P2,1 )2 3σm (P2,1 )
                              √
                       2        m
              δ1 ≤ √ ·              · ǫ1 .
                        3   σ m (O)

                                              b ⊤ O is invertible (Lemma 9).
Proof. The assumption on ǫ2,1 guarantees that U
   We bound δ∞ = k(O U )(bb∞ − eb∞ )k∞ by kO⊤ k∞ kU (bb∞ − eb∞ )k∞ ≤ kbb∞ − eb∞ k2 . Then:
                      ⊤


           kbb∞ − e
                  b∞ k2 = k(Pb2,1
                              ⊤ b +b          ⊤ b +
                                  U ) P1 − (P2,1 U ) P1 k2
                        ≤ k((Pb2,1 U
                                ⊤  b ) − (P2,1 U
                                      +     ⊤  b )+ )Pb1 k2 + k(P2,1
                                                                 ⊤ b + b
                                                                     U ) (P1 − P1 )k2
                          ≤ k((Pb2,1
                                  ⊤ b +      ⊤ b +
                                     U ) − (P2,1 U ) )k2 kPb1 k1 + k(P2,1
                                                                       ⊤ b +
                                                                          U ) k2 kPb1 − P1 k2
                                 √
                            1+ 5                    ǫ2,1                      ǫ1
                          ≤           ·                                +              ,
                                2       min{σm (Pb2,1 ), σm (P2,1
                                                              ⊤ U b )}2 σm (P ⊤ U  b
                                                                               2,1 )

where the last inequality follows from Lemma 23. The bound now follows from Lemma 9.
    Next for ∆x , we bound each term k(U     b ⊤ O)−1 (B bx − B    b ⊤ O)k1 by √mk(U
                                                              ex )(U                   b ⊤ O)−1 (B
                                                                                                 bx −
ex )U             √
    b ⊤ k2 kOk1 ≤ mk(U  b ⊤ O)−1 k2 kB
                                     bx − B
                                          ex k2 kU              √
                                                 b ⊤ k2 kOk1 = mkB    bx − B
                                                                           ex k2 /σm (U
                                                                                      b ⊤ O). To deal
B


                                                       15
      bx − B
with kB    ex k2 , we use the decomposition

                         bx − B
                         B    ex         =   b ⊤ P3,x,1 )(U
                                            (U             b ⊤ P2,1 )+ − (U
                                                                          b ⊤ Pb3,x,1 )(Ub ⊤ Pb2,1 )+
                                    2                                                                  2
                                                                                        
                                         ≤ (Ub P3,x,1 ) (U
                                               ⊤              b P2,1 ) − (U
                                                                ⊤      +    b Pb2,1 )
                                                                               ⊤       +
                                                                                             2
                                                                     
                                           + U b ⊤
                                                      P3,x,1 − Pb3,x,1 (Ub P2,1 )
                                                                          ⊤        +
                                                                                       2
                                                             √
                                                        1+ 5                      ǫ2,1
                                         ≤ kP3,x,1 k2 ·           ·
                                                            2                b
                                                                    min{σm (P2,1 ), σm (U  b ⊤ P2,1 )}2
                                                 ǫ3,x,1
                                           +
                                             σm (Ub ⊤ P2,1 )
                                                                √
                                                          1+ 5                       ǫ2,1
                                         ≤ Pr[x2 = x] ·             ·
                                                               2      min{σm (Pb2,1 ), σm (U  b ⊤ P2,1 )}2
                                                 ǫ3,x,1
                                           +                 ,
                                             σm (Ub ⊤ P2,1 )

where
qP the second P        inequality uses Lemma 23, and the final inequality uses the fact kP3,x,1 k2 ≤
                 2
    i,j [P3,x,1 ]i,j ≤   i,j [P3,x,1 ]i,j = Pr[x2 = x]. Applying Lemma 9 gives the stated bound on ∆x
and also ∆.
                                   √                b ⊤ k2 kPb1 − P1 k2 ≤ √mǫ1 /σm (U
                                           b ⊤ O)−1 U                               b ⊤ O). Again, the stated
   Finally, we bound δ1 by mk(U
bound follows from Lemma 9.

5.2    Proof of Theorem 6
We need to quantify how estimation errors propagate in the probability calculation. Because the
joint probability of a length t sequence is computed by multiplying together t matrices, there is
a danger of magnifying the estimation errors exponentially. Fortunately, this is not the case: the
following lemma shows that these errors accumulate roughly additively.
Lemma 11. Assume Ub ⊤ O is invertible. For any time t:
           X                                   
                 b ⊤
               (U O)   −1 b      b      e   e
                            Bxt:1 b1 − Bxt:1 b1   ≤ (1 + ∆)t δ1 + (1 + ∆)t − 1.
                                                                      1
                         x1:t

Proof. By induction on t. The base case, that k(U       b ⊤ O)−1 (bb1 − eb1 )k1 ≤ (1+ ∆)0 δ1 + (1+ ∆)0 − 1 = δ1
is true by definition. For the inductive step, define unnormalized states bbt = bbt (x1:t−1 ) = B      bx      b
                                                                                                          t−1:1 b1

and ebt = ebt (x1:t−1 ) = B
                          ex      e
                             t−1:1 b1 . Fix t > 1, and assume

                       X                            
                             (Ub ⊤ O)−1 bbt − e   bt   ≤ (1 + ∆)t−1 δ1 + (1 + ∆)t−1 − 1.
                                                             1
                           x1:t−1

Then, we can decompose the sum over x1:t as
         X
                        bx bb1 − B
              b ⊤ O)−1 (B
            k(U                  ex e
                          t:1      t:1 b1 )k1
           x1:t
                  X                                                                    
           =                b ⊤ O)−1
                           (U             B      ext ebt + B
                                           bxt − B                ext b
                                                            bxt − B               ext b
                                                                       bt − ebt + B   bt − ebt                   ,
                                                                                                             1
                  x1:t


                                                                 16
which, by the triangle inequality, is bounded above by
                 X X                             
                            b ⊤ O)−1 B
                           (U            bxt − B    b ⊤ O)
                                               ext (U                            b ⊤ O)−1ebt
                                                                                (U                               (2)
                                                                           1                             1
                     xt x1:t−1
                         X X                                                                         
                    +                     b ⊤ O)−1 B
                                         (U         bxt − B    b ⊤ O)
                                                          ext (U                     b ⊤ O)−1 bbt − ebt
                                                                                    (U                           (3)
                                                                                1                            1
                          xt x1:t−1
                         X X                                                    
                    +                     b ⊤ O)−1 B
                                         (U        et (U      b ⊤ O)−1 bbt − ebt
                                                       b ⊤ O)(U                                .                 (4)
                                                                                           1
                          xt x1:t−1


 We deal with each double sum individually. For the sums in (2), we use the fact that k(U b ⊤ O)−1ebt k1 =
 Pr[x1:t−1 ], which, when summed over x1:t−1 , is 1. Thus the entire double sum is bounded by ∆ by
 definition. For (3), we use the inductive hypothesis to bound the inner sum over k(U  b ⊤ O)(bbt − ebt )k1 ;
 the outer sum scales this bound by ∆ (again, by definition). Thus the double sum is bounded
 by ∆((1 + ∆)t−1 δ1 + (1 + ∆)t−1 − 1). Finally, for sums in (4), we first replace (U b ⊤ O)−1 B et (U
                                                                                                    b ⊤ O)
 with Axt . Since Axt has all non-negative entries, we have that kAxt ~v k1 ≤ ~1m Axt |~v |Pfor any vec-
                                                                                 ⊤

 tor ~v ∈ Rm , where |~v | denotes element-wise absolute value of ~v . Now the fact ~1⊤m     xt Axt |~v| =
~1⊤
  m T |~
             ~ ⊤
       v | = 1m |~v | = k~v k1 and the inductive hypothesis imply the double sum in (4) is bounded by
 (1+ ∆)t−1 δ1 + (1+ ∆)t−1 − 1. Combining these bounds for (2), (3), and (4) completes the induction.


   All that remains is to bound the effect of errors in bb∞ . Theorem 6 will follow from the following
lemma combined with the sampling error bounds of Lemma 8.

Lemma 12. Assume ǫ2,1 ≤ σm (P2,1 )/3. Then for any t,
            X                                                                     
                               c 1:t ] ≤ δ∞ + (1 + δ∞ ) (1 + ∆)t δ1 + (1 + ∆)t − 1 .
                   Pr[x1:t ] − Pr[x
            x1:t


Proof. By Lemma 9 and the condition on ǫ2,1 , we have σm (Ub ⊤ O) > 0 so U
                                                                         b ⊤ O is invertible.
   Now we can decompose the L1 error as follows:
                X                             X
                    c 1:t ] − Pr[x1:t ] =
                    Pr[x                          bb⊤ B
                                                      bx bb1 − ~b⊤ Bx ~b1
                                                                     ∞    t:1          ∞           t:1
                        x1:t                                  x1:t
                               X
                          =            bb⊤ B
                                           b b       e⊤ e e
                                         ∞ xt:1 b1 − b∞ Bxt:1 b1
                               x1:t
                               X
                          ≤            (bb∞ − eb∞ )⊤ (U
                                                      b ⊤ O)(U        ex eb1
                                                             b ⊤ O)−1 B
                                                                        t:1                                      (5)
                               x1:t
                                   X
                               +             (bb∞ − eb∞ )⊤ (U
                                                            b ⊤ O)(U         bx bb1 − B
                                                                   b ⊤ O)−1 (B
                                                                               t:1
                                                                                      ex e
                                                                                        t:1 b1 )                 (6)
                                      x1:t
                                   X
                               +             eb⊤ (U
                                                  b ⊤ O)(U         bx b
                                                         b ⊤ O)−1 (B          e e
                                               ∞                     t:1 b1 − Bxt:1 b1 ) .                       (7)
                                      x1:t


                                                               17
The first sum (5) is
                          X
                                    (bb∞ − eb∞ )⊤ (U
                                                   b ⊤ O)(U        ex eb1
                                                          b ⊤ O)−1 B
                                                                     t:1
                            x1:t
                                     X
                              ≤               b ⊤ O)⊤ (bb∞ − eb∞ )
                                             (U                             (U        ex eb1
                                                                             b ⊤ O)−1 B
                                                                                        t:1
                                                                        ∞                      1
                                     x1:t
                                     X                           X
                              ≤             δ∞ kAxt:1 ~π k1 =           δ∞ Pr[x1:t ] = δ∞
                                     x1:t                        x1:t

where the first inequality is Hölder’s, and the second uses the bounds in Lemma 10.
   The second sum (6) employs Hölder’s and Lemma 11:

                       (bb∞ − eb∞ )⊤ (U
                                      b ⊤ O)(U         bx bb1 − B
                                             b ⊤ O)−1 (B
                                                         t:1
                                                                ex eb1 )
                                                                  t:1


                        ≤           b ⊤ O)⊤ (bb∞ − e
                                   (U              b∞ )          (U         bx b
                                                                  b ⊤ O)−1 (B          e e
                                                                              t:1 b1 − Bxt:1 b1 )
                                                            ∞                                       1
                        ≤ δ∞ ((1 + ∆)t δ1 + (1 + ∆)t − 1).

   Finally, the third sum (7) uses Lemma 11:
                                     X
                                            eb⊤ (U
                                                 b ⊤ O)(U         bx b
                                                        b ⊤ O)−1 (B          e e
                                              ∞                     t:1 b1 − Bxt:1 b1 )
                                     x1:t
                                              X
                                       =                           bx bb1 − B
                                                         b ⊤ O)−1 (B
                                                     1⊤ (U                  ex e
                                                                     t:1      t:1 b1 )
                                              x1:t
                                              X
                                       ≤                        bx bb1 − B
                                                      b ⊤ O)−1 (B
                                                     (U                  ex eb1 )
                                                                  t:1      t:1
                                                                                      1
                                              x1:t
                                       ≤ (1 + ∆)t δ1 + (1 + ∆)t − 1.

Combining these gives the desired bound.

Proof of Theorem 6. By Lemma 8, the specified number of samples N (with a suitable constant
C), together with the setting of ε in n0 (ε), guarantees the following sampling error bounds:
                                                                √                   √       
                 ǫ1 ≤ min 0.05 · (3/8) · σm (P2,1 ) · ǫ, 0.05 · ( 3/2) · σm (O) · (1/ m) · ǫ
              ǫ2,1 ≤ min 0.05 · (1/8) · σm (P2,1 )2 · (ǫ/5),
                                   √                                   √        
                           0.01 · ( 3/8) · σm (O) · σm (P2,1 )2 · (1/(t m)) · ǫ
          X                   √                                  √
            ǫ3,x,1 ≤ 0.39 · (3 3/8) · σm (O) · σm (P2,1 ) · (1/(t m)) · ǫ.
           x

These, in turn, imply the following parameter error bounds, via Lemma 10: δ∞ ≤ 0.05ǫ, δ1 ≤ 0.05ǫ,
and ∆ ≤ 0.4ǫ/t. Finally, Lemma 12 and the fact (1 + a/t)t ≤ 1 + 2a for a ≤ 1/2, imply the desired
L1 error bound of ǫ.


                                                                18
5.3   Proof of Theorem 7
In this subsection, we assume the HMM obeys Condition 3 (in addition to Condition 1).
    We introduce the following notation. Let the unnormalized estimated conditional hidden state
distributions be
                                        b
                                        ht = (Ub ⊤ O)−1bbt ,

and its normalized version,
                                              gt = b
                                              b    ht /(~1⊤ b
                                                          m ht ).

Also, let
                                         A     b ⊤ O)−1 B
                                         bx = (U        bx (U
                                                            b ⊤ O).

This notation lets us succinctly compare the updates made by our estimated model to the updates
of the true model. Our algorithm never explicitly computes these hidden state distributions gbt
(as it would require knowledge of the unobserved O). However, under certain conditions (namely
Conditions 1 and 3 and some estimation accuracy requirements), these distributions are well-defined
and thus we use them for sake of analysis.
    The following lemma shows that if the estimated parameters are accurate, then the state updates
behave much like the true hidden state updates.

                                     ~ ∈ Rm and any observation x,
Lemma 13. For any probability vector w

            X
                 bb⊤ (U
                      b ⊤ O)A
                            bx w
                               ~ −1      ≤ δ∞ + δ∞ ∆ + ∆       and
                   ∞
            x
                            bx w]
                           [A  ~i                     [Ax w]
                                                          ~ i − ∆x
                                         ≥                                for all i = 1, . . . , m
                      bb⊤ (U
                           b ⊤ O)Abx w
                                     ~       ~1⊤
                                               m Ax w
                                                    ~ + δ∞ + δ∞ ∆x + ∆x
                       ∞

                                  ~ ∈ Rm ,
Moreover, for any non-zero vector w

                                             ~1⊤  b ~
                                               m Ax w         1
                                                         ≤        .
                                         bb⊤ (Ub     b
                                                 ⊤ O)A
                                                      xw
                                                       ~   1 − δ∞
                                           ∞

                                                              bx to that of the true operator Ax .
Proof. We need to relate the effect of the estimated operator A
First assume w
             ~ is a probability vector. Then:

                bb⊤ (U
                     b ⊤ O)A
                           bx w
                              ~ − ~1⊤
                  ∞                 m Ax w
                                         ~

                 =    (bb∞ − eb∞ )⊤ (U
                                     b ⊤ O)Ax w
                                              ~

                      + (bb∞ − eb∞ )⊤ (U
                                       b ⊤ O)(A        ~ + eb∞ (U
                                              bx − Ax )w        b ⊤ O)(A
                                                                       bx − Ax )w
                                                                                ~

                 ≤ k(bb∞ − eb∞ )⊤ (U
                                   b ⊤ O)k∞ kAx wk
                                                ~ 1
                         b     e    ⊤ b⊤
                    + k(b∞ − b∞ ) (U O)k∞ k(A    bx − Ax )k1 kwk      bx − Ax )k1 kwk
                                                              ~ 1 + k(A            ~ 1.

Therefore we have
                                X
                                      bb⊤ (U
                                           b ⊤ O)A
                                                 bx w
                                                    ~ − 1 ≤ δ∞ + δ∞ ∆ + ∆
                                        ∞
                                  x


                                                      19
and
                           bb⊤ (U
                                b ⊤ O)A
                                      bx w
                                         ~ ≤ ~1⊤
                             ∞                 m Ax w
                                                    ~ + δ∞ + δ∞ ∆x + ∆x .
Combining these inequalities with
                                bx w]
                               [A  ~ i = [Ax w]      bx − Ax )w]
                                             ~ i + [(A        ~i
                                       ≥ [Ax w]       b
                                             ~ i − k(Ax − Ax )wk
                                                              ~ 1
                                          ≥ [Ax w]      bx − Ax )k1 kwk
                                                ~ i − k(A            ~ 1
                                          ≥ [Ax w]
                                                ~ i − ∆x

gives the first claim.
                                 ~ is a probability vector, and assume ~1⊤
    Now drop the assumption that w                                         b ~ 6= 0 without loss
                                                                         m Ax w
of generality. Then:

                       ~1⊤  b ~
                         m Ax w
                                                        ~1⊤ b ~
                                                          m Ax w
                                      =
                   bb⊤ (Ub ⊤ O)A
                               bx w
                                  ~        ~1⊤ b ~ + (bb∞ − e       b ⊤ O)A
                                                             b∞ )⊤ (U     bx w
                     ∞                       m Ax w                          ~
                                                              bx wk
                                                             kA  ~ 1
                                      ≤
                                            bx wk
                                           kA          b ⊤ O)⊤ (bb∞ − eb∞ )k∞ kA
                                               ~ 1 − k(U                       bx wk
                                                                                  ~ 1

which is at most 1/(1 − δ∞ ) as claimed.

   A consequence of Lemma 13 is that if the estimated parameters are sufficiently accurate, then
the state updates never allow predictions of very small hidden state probabilities.

Corollary 14. Assume δ∞ ≤ 1/2, maxx ∆x ≤ α/3, δ1 ≤ α/8, and maxx δ∞ + δ∞ ∆x + ∆x ≤ 1/3.
Then [b
      gt ]i ≥ α/2 for all t and i.

Proof. For t = 1, we use Lemma 10 to get k~h1 − b              h1 k1 ≤ δ1 ≤ 1/2, so Lemma 17 implies that
 ~
kh1 − b
      g1 k1 ≤ 4δ1 . Then [b        ~         ~
                          g1 ]i ≥ [h1 ]i − |[h1 ]i − [b
                                                      g1 ]i | ≥ α − 4δ1 ≥ α/2 (using Condition 3) as needed.
For t > 1, Lemma 13 implies

                    bx gbt−1 ]i
                   [A                          [Ax b
                                                   gt−1 ]i − ∆x       α − α/3   α
                                    ≥                               ≥         ≥
                   b ⊤ O)A
              ~b⊤ (U       bx bgt−1   ~1⊤
                                        m Ax b
                                             gt−1 + δ∞ + δ∞ ∆x + ∆x   1 + 1/3   2
                ∞

using Condition 3 in the second-to-last step.

    Lemma 13 and Corollary 14 can now be used to prove the contraction property of the KL-
divergence between the true hidden states and the estimated hidden states. The analysis shares
ideas from Even-Dar et al. (2007), though the added difficulty is due to the fact that the state
maintained by our algorithm is not a probability distribution.

Lemma 15. Let ε0 = maxx 2∆x /α + (δ∞ + δ∞ ∆x + ∆x )/α + 2δ∞ . Assume δ∞ ≤ 1/2, maxx ∆x ≤
                                                   gt ∈ Rm is a probability vector, then
α/3, and maxx δ∞ + δ∞ ∆x + ∆x ≤ 1/3. For all t, if b

                                                              γ2
                     KL(~ht+1 ||b
                                gt+1 ) ≤ KL(~ht ||b
                                                  gt ) −             2 KL(~ht ||b
                                                                                 gt )2 + ε0 .
                                                           2 ln α2


                                                    20
Proof. The LHS, written as an expectation over x1:t , is
                                                  "m                          #
                                                   X                [~ht+1 ]i
                        KL(~ht+1 ||b
                                   gt+1 ) = Ex1:t      [~ht+1 ]i ln             .
                                                                    [bgt+1 ]i
                                                                 i=1

We can bound ln(1/[b
                   gt+1 ]i ) as
                                                                           !
                       1               bb⊤ (U
                                            b ⊤ O)A   bxt gbt
               ln              = ln      ∞
                                                              · ~1⊤ b
                                             bxt gbt ]i           m ht+1
                    [b
                     gt+1 ]i                [A
                                                                                              !
                                    ~1⊤     gt [Axt gbt ]i b
                                      m Axt b                b⊤ (Ub ⊤ O)Abxt b
                                                                             gt ~ ⊤ b
                               = ln            ·            · ∞                · 1m ht+1
                                     [Axt b      bxt gbt ]i
                                          gt ]i [A              ~1m Axt gbt
                                                                  ⊤

                                       ~1⊤
                                         m Axt b
                                               gt       [Axt gbt ]i
                               ≤ ln                ·
                                        [Axt b
                                             gt ]i   [Axt gbt ]i − ∆xt
                                                                                   !
                                       ~1⊤
                                         m Axt gbt + δ∞ + δ∞ ∆xt + ∆xt
                                    ·                                  · (1 + 2δ∞ )
                                                    ~1⊤
                                                      m Axt b
                                                            gt
                                                  !
                                      ~1⊤
                                        m Axt b
                                              gt        2∆xt     δ∞ + δ∞ ∆xt + ∆xt
                               ≤ ln                  +         +                    + 2δ∞
                                       [Axt b
                                            gt ]i         α              α
                                                  !
                                      ~1⊤
                                        m Axt b
                                              gt
                               ≤ ln                  + ε0
                                       [Axt b
                                            gt ]i

where the first inequality follows from Lemma 13, and the second uses ln(1 + a) ≤ a. Therefore,
                                           "m                                       !#
                                            X                         ~1⊤ A x  gb t
                 KL(~ht+1 ||b
                            gt+1 ) ≤ Ex1:t    [~ht+1 ]i ln [~ht+1 ]i · m t             + ε0 . (8)
                                                                       [Axt gbt ]i
                                                   i=1

The expectation in (8) is the KL-divergence between Pr[ht |x1:t−1 ] and the distribution over ht+1
                               c t |x1:t−1 ] (using Bayes’ rule) with Pr[ht+1 |ht ] and Pr[xt |ht ]. Call
that is arrived at by updating Pr[h
                         f t+1 |x1:t ]. The chain rule for KL-divergence states
this second distribution Pr[h
                                 f t+1 |x1:t ]) + KL(Pr[ht |ht+1 , x1:t ]||Pr[h
             KL(Pr[ht+1 |x1:t ]||Pr[h                                      f t |ht+1 , x1:t ])
                                    f t |x1:t ]) + KL(Pr[ht+1 |ht , x1:t ]||Pr[h
              = KL(Pr[ht |x1:t ]||Pr[h                                      f t+1 |ht , x1:t ]).

Thus, using the non-negativity of KL-divergence, we have
                                  f t+1 |x1:t ])
              KL(Pr[ht+1 |x1:t ]||Pr[h
                                     f t |x1:t ]) + KL(Pr[ht+1 |ht , x1:t ]||Pr[h
               ≤ KL(Pr[ht |x1:t ]||Pr[h                                      f t+1 |ht , x1:t ])
                                    f t |x1:t ])
                = KL(Pr[ht |x1:t ]||Pr[h
                                              f t+1 |ht , x1:t ] = Pr[h
where the equality follows from the fact that Pr[h                 f t+1 |ht ] = Pr[ht+1 |ht ] =
Pr[ht+1 |ht , x1:t ]. Furthermore,
                                                                           Pr[xt |ht = i]
              Pr[ht = i|x1:t ] = Pr[ht = i|x1:t−1 ] · Pm
                                                                j=1 Pr[xt |ht = j] · Pr[ht = j|x1:t−1 ]


                                                           21
and
              f t = i|x1:t ] = Pr[h
                               c t = i|x1:t−1 ] · P                   Pr[xt |ht = i]
              Pr[h                                                                               ,
                                                    m                           c t = j|x1:t−1 ]
                                                               Pr[xt |ht = j] · Pr[h
                                                         j=1
so
                               f t |x1:t ])
             KL(Pr[ht |x1:t ]||Pr[h
                       "m                                             #
                         X                         Pr[ht = i|x1:t−1 ]
              = Ex1:t          Pr[ht = i|x1:t ] ln
                                                   c t = i|x1:t−1 ]
                                                   Pr[h
                         i=1
                           "m                         Pm                                        #
                              X                         j=1 Pr[xt |ht = j] · Pr[ht = j|x1:t−1 ]
                 − Ex1:t          Pr[ht = i|x1:t ] ln Pm                                          .
                                                                             c t = j|x1:t−1 ]
                                                            Pr[xt |ht = j] · Pr[h
                              i=1                       j=1

The first expectation is
                   "m                                          #
                    X                       Pr[ht = i|x1:t−1 ]
             Ex1:t      Pr[ht = i|x1:t ] ln
                                            c t = i|x1:t−1 ]
                                            Pr[h
                    i=1
                           "                     m
                                                                                           #
                            X                   X                       Pr[ht = i|x1:t−1 ]
               = Ex1:t−1        Pr[xt |x1:t−1 ]     Pr[ht = i|x1:t ] ln
                                                                        c t = i|x1:t−1 ]
                                                                        Pr[h
                             xt                 i=1
                           "     m
                                                                                               #
                            XX                                              Pr[ht = i|x1:t−1 ]
               = Ex1:t−1            Pr[xt |ht = i] · Pr[ht = i|x1:t−1 ] ln
                                                                            c t = i|x1:t−1 ]
                                                                           Pr[h
                             xt i=1
                           "     m
                                                                                   #
                            XX                                  Pr[ht = i|x1:t−1 ]
               = Ex1:t−1            Pr[xt , ht = i|x1:t−1 ] ln
                                                                c t = i|x1:t−1 ]
                                                                Pr[h
                               xt i=1

                = KL(~ht ||b
                           gt ),
and the second expectation is
                   "m                       Pm                                       #
                    X                        j=1 Pr[xt |ht = j] · Pr[ht = j|x1:t−1 ]
             Ex1:t      Pr[ht = i|x1:t ] ln Pm
                                                                   c
                    i=1                      j=1 Pr[xt |ht = j] · Pr[ht = j|x1:t−1 ]
                           "                       Pm                                         #
                            X                       j=1 Pr[x t |ht = j] · Pr[ht = j|x 1:t−1 ]
               = Ex1:t−1        Pr[xt |x1:t−1 ] ln Pm
                                                                          c t = j|x1:t−1 ]
                                                        Pr[xt |ht = j] · Pr[h
                                xt                     j=1

                 = KL(O~ht ||Ob
                              gt ).
Substituting these back into (8), we have
                         KL(~ht+1 ||b
                                    gt+1 ) ≤ KL(~ht ||b
                                                      gt ) − KL(O~ht ||Ob
                                                                        gt ) + ε0 .
It remains to bound KL(O~ht ||Ob gt ) from above. We use Pinsker’s inequality (Cover and Thomas,
1991), which states that for any distributions p~ and ~q,
                                                           1
                                         KL(~
                                            p||~q) ≥          p − ~qk21 ,
                                                             k~
                                                           2
together with the definition of γ, to deduce
                                    1                         γ2
                             gt ) ≥ Ex1:t−1 kO~ht − Ob
                  KL(O~ht ||Ob                       gt k21 ≥    Ex   k~ht − b
                                                                             gt k21 .
                                    2                         2 1:t−1

                                                      22
Finally, by Jensen’s inequality and Lemma 18 (the latter applies because of Corollary 14), we have
that                                                                                    !2
                                                                       1
                 Ex1:t−1 k~ht − b
                                gt k21 ≥ (Ex1:t−1 k~ht − gbt k1 )2 ≥       KL(~ht ||b
                                                                                    gt )
                                                                     ln α2
which gives the required bound.

   Finally, the recurrence from Lemma 15 easily gives the following lemma, which in turn combines
with the sampling error bounds of Lemma 8 to give Theorem 7.
                                                                                      √
Lemma 16. Let ε0 = maxx 2∆x /α + (δ∞ + δ∞ ∆x + ∆x )/α + 2δ∞ and ε1 = maxx (δ∞ + mδ∞ ∆x +
√
  m∆x )/α. Assume δ∞ ≤ 1/2, maxx ∆x ≤ α/3, maxx δ∞ + δ∞ ∆x + ∆x ≤ 1/3, δ1 ≤ ln(2/α)/(8γ 2 ),
ε0 ≤ ln(2/α)2 /(4γ 2 ), and ε1 ≤ 1/2. Then for all t,
                                                  s           
                                                           2 2
                                                      2 ln α ε0
              KL(~ht ||bgt ) ≤ max 4δ1 log(2/α),                and
                                                          γ2
                                     c t |x1:t−1 ]) ≤ KL(~ht ||b
               KL(Pr[xt |x1:t−1 ] || Pr[x                      gt ) + δ∞ + δ∞ ∆ + ∆ + 2ε1 .

Proof. To prove the bound on KL(~ht ||b        gt ), we proceed by induction on t. For the base case,
Lemmas 18 (with Corollary 14) and 17 imply KL(~h1 ||b             g1 ) ≤ k~h1 − b   g1 k1 ln(2/α) ≤ 4δ1 ln(2/α)
as required. The inductive step follows easily from Lemma p              15 and simple calculus: assuming
c2 ≤ p1/(4c1 ), z − c1 z 2 + c2 is non-decreasing
                                              p        in z for all z ≤     c2 /c1 , so z ′ ≤ z − c1 z 2 + c2 and
                                         ′
z ≤ c2 /c1 together imply that z ≤ c2 /c1 . The inductive step uses the the above fact with
z = KL(~ht ||b
             gt ), z ′ = KL(~ht+1 ||b
                                    gt+1 ), c1 = γ 2 /(2(ln(2/α))2 ), and c2 = max(ε0 , c1 (4δ1 log(2/α))2 ).
   Now we prove the bound on KL(Pr[xt |x1:t−1 ]||Pr[x       c t |x1:t−1 ]). First, let Pr[x
                                                                                          c t , ht |x1:t−1 ] denote
our predicted conditional probability of both the hidden state and observation, i.e. the product of
the following two quantities:
                                                                              b⊤ b ⊤ b
             c t = i|x1:t−1 ] = [b
             Pr[h                gt ]i      and     c t |ht = i, x1:t−1 ] = P[b∞ (U O)Axt ]i .
                                                    Pr[x
                                                                                b⊤ b ⊤ b bt
                                                                              x b∞ (U O)Ax g

Now we can apply the chain rule for KL-divergence
                                c t |x1:t−1 ])
            KL(Pr[xt |x1:t−1 ]||Pr[x
                                      c t |x1:t−1 ]) + KL(Pr[xt |ht , x1:t−1 ]||Pr[x
             ≤ KL(Pr[ht |x1:t−1 ]||Pr[h                                               c t |ht , x1:t−1 ])
                                         "m                                 P                       !#
                                          XX                                       bb⊤ (U
                                                                                        b ⊤ O)Ab b
                                                                                                 g
                                                                                                x t
             = KL(~ht ||b gt ) + Ex1:t−1         [~ht ]i Oxt ,i ln Oxt ,i · x ∞
                                                                              b  ⊤    b ⊤
                                                                             [b∞ (U O)Axt ]i b
                                          i=1 xt
                                         "m                                               !#
                                          XX                               Ox   ,i
             ≤ KL(~ht ||b gt ) + Ex1:t−1         [~ht ]i Oxt ,i ln            t

                                          i=1 xt                   [bb⊤   b⊤ b
                                                                      ∞ (U O)Axt ]i
                   + ln(1 + δ∞ + δ∞ ∆ + ∆)

where the last inequality uses Lemma 13. It will suffice to show that
                                                 Oxt ,i
                                                           ≤ 1 + 2ε1 .
                                          [bb⊤  b⊤ b
                                             ∞ (U O)Axt ]i


                                                         23
Note that Oxt ,i = [eb⊤  b⊤
                      ∞ (U O)Axt ]i > α by Condition 3. Furthermore, for any i,

                   |[bb⊤  b⊤ b                     b⊤ b ⊤ b          e⊤ b ⊤
                       ∞ (U O)Axt ]i − Oxt ,i | ≤ kb∞ (U O)Axt − b∞ (U O)Axt k∞
                                                ≤ k(bb∞ − eb∞ )(U
                                                                b ⊤ O)k∞ kAx k∞               t

                                                      + k(bb∞ − eb∞ )(U
                                                                      b ⊤ O)k∞ kAbxt − Axt k∞
                                                      + keb∞ (U
                                                              b O)k∞ kA
                                                                ⊤         bxt − Axt k∞
                                                            √              √
                                                    ≤ δ∞ + mδ∞ ∆xt + m∆xt .

Therefore
                                Oxt ,i                             O
                                                ≤                √ xt ,i    √
                           b⊤  b
                          [b∞ (U ⊤ O)A bxt ]i        Oxt ,i − (δ∞ +mδ∞ ∆xt + m∆xt )
                                                                    1
                                                ≤             √          √
                                                     1 − (δ∞ + mδ∞ ∆xt + m∆xt )/α
                                                       1
                                                ≤           ≤ 1 + 2ε1
                                                     1 − ε1
as needed.

Proof of Theorem 7. The proof is mostly the same as that of Theorem 6 with t = 1, except that
Lemma 16 introduces additional error terms. Specifically, we require

                        ln(2/α)4           m                                       m                   m
            N ≥C·         4 2  4
                                 ·                             and    N ≥C·               ·
                         ǫ α γ     σm (O) σm (P2,1 )4
                                         2                                        ǫ2 α2       σm   (O)2 σ   m (P2,1 )
                                                                                                                     4


so that the terms                                         s                   !
                                                              2 ln(2/α)2 ε0
                                max 4δ1 log(2/α),                                 and ε1 ,
                                                                   γ2
respectively, are O(ǫ). The specified number of samples N also suffices to imply the preconditions
of Lemma 16. The remaining terms are bounded as in the proof of Theorem 6.

Lemma 17. If k~a − ~bk1 ≤ c ≤ 1/2 and ~b is a probability vector, then k~a/(~1⊤~a) − ~bk1 ≤ 4c.

Proof. First, it is easy to check that 1 − c ≤ ~1⊤~a ≤ 1 + c. Let I = {i : ~ai /(~1⊤~a) > ~bi }. Then for
i ∈ I, |~ai /(~1⊤~a) − ~bi | = ~ai /(~1⊤~a) − ~bi ≤ ~ai /(1 − c) − ~bi ≤ (1 + 2c)~ai − ~bi ≤ |~ai − ~bi | + 2c~ai . Similarly,
for i ∈/ I, |~bi −~ai /(~1⊤~a)| = ~bi −~ai /(~1⊤~a) ≤ ~bi −~ai /(1 + c) ≤ ~bi − (1 − c)~ai ≤ |~bi −~ai | + c~ai . Therefore
k~a/(~1⊤~a) − ~bk1 ≤ k~a − ~bk1 + 2c(~1⊤~a) ≤ c + 2c(1 + c) ≤ 4c.

Lemma 18. Let ~a and ~b be probability vectors. If there exists some c < 1/2 such that ~bi > c for
all i, then KL(~a||~b) ≤ k~a − ~bk1 log(1/c).

Proof. See (Even-Dar et al., 2007), Lemma 3.10.


                                                              24
Acknowledgments
The authors would like to thank John Langford and Ruslan Salakhutdinov for earlier discussions on
using bottleneck methods to learn nonlinear dynamic systems; the linearization of the bottleneck
idea was the basis of this paper. We also thank Yishay Mansour for pointing out hardness results
for learning HMMs. Finally, we thank Geoff Gordon, Byron Boots, and Sajid Siddiqi for alerting
us of an error in a previous version of this paper. This work was completed while DH was an intern
at TTI-C in 2008. TZ was partially supported by the following grants: AFOSR-10097389, NSF
DMS-1007527, and NSF IIS-1016061.


References
S. Andersson, T. Ryden, and R. Johansson. Linear optimal prediction and innovations repre-
  sentations of hidden markov models. Stochastic Processes and their Applications, 108:131–149,
  2003.

Leonard E. Baum and J. A. Eagon. An inequality with applications to statistical estimation for
  probabilistic functions of Markov processes and to a model for ecology. Bull. Amer. Math. Soc.,
  73(3):360–363, 1967.

Leonard E. Baum, Ted Petrie, George Soules, and Norman Weiss. A maximization technique occur-
  ring in the statistical analysis of probabilistic functions of Markov chains. Annals of Mathematical
  Statistics, 41(1):164–171, 1970.

S. Charles Brubaker and Santosh Vempala. Isotropic PCA and affine-invariant clustering. In FOCS,
   2008.

J.W Carlyle and A. Paz. Realization by stochastic finite automaton. J. Comput. Syst. Sci., 5:
  26–40, 1971.

Kamalika Chaudhuri and Satish Rao. Learning mixtures of product distributions using correlations
 and independence. In COLT, 2008.

T. M. Cover and J. A. Thomas. Elements of Information Theory. Wiley, 1991.

G. Cybenko and V. Crespi. Learning hidden markov models using non-negative matrix factorization.
  Technical report, 2008. arXiv:0809.4086.

Sanjoy Dasgupta. Learning mixutres of Gaussians. In FOCS, 1999.

Sanjoy Dasgupta and Leonard Schulman. A probabilistic analysis of EM for mixtures of separated,
  spherical Gaussians. JMLR, 8(Feb):203–226, 2007.

A. P. Dempster, N. M. Laird, and D. B. Rubin. Maximum likelihood from incomplete data via the
  EM algorithm. Journal of the Royal Statistical Society, Series B, 39(1):1–38, 1977.

Eyal Even-Dar, Sham M. Kakade, and Yishay Mansour. Planning in POMDPs using multiplicity
  automata. In UAI, 2005.


                                                 25
Eyal Even-Dar, Sham M. Kakade, and Yishay Mansour. The value of observation for monitoring
  dynamic systems. In IJCAI, 2007.

M. Fliess. Matrices deHankel. J. Math. Pures Appl., 53:197–222, 1974.

H. Hotelling. The most predictable criterion. Journal of Educational Psychology, 1935.

H. Jaeger, M. Zhao, K. Kretzschmar, T. Oberstein, D. Popovici, and A. Kolling. Learning ob-
  servable operator models via the es algorithm. In S. Haykin, J. Principe, T. Sejnowski, and
  J. McWhirter, editors, New Directions in Statistical Signal Processing: from Systems to Brain,
  pages 417–464. MIT Press, 2006.

Herbert Jaeger. Observable operator models for discrete stochastic time series. Neural Comput.,
  12(6), 2000.

T. Katayama. Subspace Methods for System Identification. Springer, 2005.

M. Kearns, Y. Mansour, D. Ron, R. Rubinfeld, R. Schapire, and L. Sellie. On the learnability of
 discrete distributions. In STOC, pages 273–282, 1994.

Michael Littman, Richard Sutton, and Satinder Singh. Predictive representations of state. In
 Advances in Neural Information Processing Systems 14 (NIPS), pages 1555–1561, 2001.

L. Ljung. System Identification: Theory for the User. NJ: Prentice-Hall Englewood Cliffs, 1987.

C. McDiarmid. On the method of bounded differences. In Surveys in Combinatorics, pages 148–188.
  Cambridge University Press, 1989.

E. Mossel and S. Roch. Learning nonsingular phylogenies and hidden Markov models. Annals of
  Applied Probability, 16(2):583–614, 2006.

P. V. Overschee and B. De Moor. Subspace Identification of Linear Systems. Kluwer Academic
  Publishers, 1996.

Lawrence R. Rabiner. A tutorial on hidden Markov models and selected applications in speech
  recognition. Proceedings of the IEEE, 77(2):257–286, 1989.

M.P. Schützenberger. On the definition of a family of automata. Inf. Control, 4:245–270, 1961.

S. M. Siddiqi, B. Boots, and G. J. Gordon. Reduced-rank hidden markov models. In Proceedings
  of the 13th International Conference on Artificial Intelligence and Statistics, 2010.

Le Song, Byron Boots, Sajid M. Siddiqi, Geoffrey J. Gordon, and Alex Smola. Hilbert space
  embeddings of hidden markov models. In Proceedings of the 27th International Conference on
  Machine Learning, 2010.

G. W. Stewart and Ji-Guang Sun. Matrix Perturbation Theory. Academic Press, 1990.

Sebastiaan Terwijn. On the learnability of hidden Markov models. In International Colloquium on
  Grammatical Inference, 2002.


                                               26
B. Vanluyten, J. Willems, and B. De Moor. A new approach for the identification of hidden markov
  models. In Conference on Decision and Control, 2007.

Santosh Vempala and Grant Wang. A spectral algorithm for learning mixtures of distributions. In
  FOCS, 2002.

MingJie Zhao and Herbert Jaeger. The error controlling algorithm for learning OOMs. Technical
 Report 6, International University Bremen, 2007.


A     Sample Complexity Bound
We will assume independent samples to avoid mixing estimation. Otherwise, one can discount the
number of samples by one minus the second eigenvalue of the hidden state transition matrix T .
    We are bounding the Frobenius norm of the matrix errors. For simplicity, we unroll the matrices
into vectors, and use vector notations.
    Let z be a discrete random variable that takes values in {1, . . . , d}. We are interested in
estimating the vector ~  q = [Pr(z = j)]dj=1 from N i.i.d. copies zi of z (i = 1, . . . , N ). Let ~
                                                                                                   qi be
the P
    vector of zeros expect the zi -th component being one. Then the empirical estimate of ~          q is
qb = N i=1 ~
           q i /N . We are interested in bounding the quantity

                                                           q − ~qk22 .
                                                          kb

   The following concentration bound is a simple application of the McDiarmid’s inequality (McDiarmid,
1989).

Proposition 19. We have ∀ǫ > 0:
                                            √            2
                           Pr kbq − ~qk2 ≥ 1/ N + ǫ ≤ e−N ǫ .
                    P                          P
Proof. Consider qb = N     qi /N , and let√pb = N
                       i=1 ~                     i=1 p
                                                     ~i /N , where p~i = ~qi except for i = k. Then we
have kb
      q − ~qk2 − kb
                  p−~
                    q k2 ≤ kb q − pbk2 ≤ 2/N . By McDiarmid’s inequality, we have
                                                                                    2
                                       Pr (kb             q − ~qk2 + ǫ) ≤ e−N ǫ .
                                            q − q~k2 ≥ E kb

Note that
                                                              2
                                                                   1/2
                N
                X                             N
                                              X
            E         qi − N ~
                      ~      q       ≤ E           ~qi − N ~q 
                i=1              2            i=1              2
                                       !1/2                                       !1/2       q
                  N
                  X                                 N
                                                    X  h                      i
            =                  q k22
                          qi − ~
                        Ek~                   =       E 1 − 2~qi⊤ ~q + k~qk22            =       N (1 − k~qk22 ).
                  i=1                               i=1

This leads to the desired bound.


                                                              27
    Using this bound, we obtain with probability 1 − 3η:
                                 p               p
                          ǫ1 ≤     ln(1/η)/N + 1/N ,
                                 p               p
                        ǫ2,1 ≤     ln(1/η)/N + 1/N ,
                                 s
                                   X            p           p
                  max ǫ3,x,1 ≤         ǫ23,x,1 ≤ ln(1/η)/N + 1/N ,
                       x
                                                 x
                                                                  !1/2
                      X                  √  X                                  p                     p
                            ǫ3,x,1     ≤  n   ǫ23,x,1                      ≤       n ln(1/η)/N +         n/N .
                       x                               x

    If the observation dimensionality n is large and sample size N is small, then the third inequality
can be improved by considering a more detailed estimate.
                                                    P       Given any k, let ǫ(k) be sum of elements
in the smallest n − k probabilities Pr[x2 = x] = i,j [P3,x,1 ]ij (Equation 1). Let Sk be the set of
these n − k such x. By Proposition 19, we obtain:
                                                                                                          2
                           X                               XX
                                   kPb3,x,1 − P3,x,1 k2F +   ([Pb3,x,1 ]ij − [P3,x,1 ]ij )
                           x∈S
                            / k                                  x∈Sk i,j
                               p                      p          2
                           ≤        ln(1/η)/N +             1/N        .

Moreover, by the definition of Sk , we have
            X                          XX
                kPb3,x,1 − P3,x,1 kF ≤      |[Pb3,x,1 ]ij − [P3,x,1 ]ij |
              x∈Sk                               x∈Sk i,j
                                                 XX                                             
                                             ≤                  max 0, [Pb3,x,1 ]ij − [P3,x,1 ]ij + ǫ(k)
                                                 x∈Sk i,j
                                                           XX                                          
                                                      +                min 0, [Pb3,x,1 ]ij − [P3,x,1 ]ij + ǫ(k)
                                                           x∈Sk i,j

                                                     XX
                                             ≤         ([Pb3,x,1 ]ij − [P3,x,1 ]ij ) + 2ǫ(k).
                                                     x∈Sk i,j

Therefore
            X                       p                        p                p                 p              
                 ǫ3,x,1 ≤ min            k ln(1/η)/N +            k/N +            ln(1/η)/N +       1/N + 2ǫ(k) .
                               k
             x
             P
This means       x ǫ3,x,1 may be small even if n is large, but the number of frequently occurring symbols
are small.


B     Matrix Perturbation Theory
The following perturbation bounds can be found in (Stewart and Sun, 1990).
Lemma 20 (Theorem 4.11, p. 204 in (Stewart and Sun, 1990)). Let A ∈ Rm×n with m ≥ n, and
    e = A + E. If the singular values of A and A
let A                                            e are (σ1 ≥ . . . ≥ σn ) and (e            en ),
                                                                               σ1 ≥ . . . ≥ σ
respectively, then
                               |e
                                σi − σi | ≤ kEk2 i = 1, . . . , n.

                                                                  28
Lemma 21 (Theorem 4.4, p. 262 in (Stewart and Sun, 1990)). Let A ∈ Rm×n , with m ≥ n, with
the singular value decomposition (U1 , U2 , U3 , Σ1 , Σ2 , V1 , V2 ):
                               ⊤                                     
                                U1                              Σ1 0
                               U2⊤  A V1 V2 =  0 Σ2  .
                                U3⊤                                0  0

    e = A + E, with analogous SVD (U
Let A                                       e1 , U
                                                 e2 , U
                                                      e3 , Σ
                                                           e 1, Σ
                                                                e 2 , Ve1 Ve2 ). Let Φ be the matrix of canonical
angles between range(U1 ) and range(U  e1 ), and Θ be the matrix of canonical angles between range(V1 )
           e
and range(V1 ). If there exists δ, α > 0 such that min σ(Σ       e 1 ) ≥ α + δ and max σ(Σ2 ) ≤ α, then

                                                                     kEk2
                                    max{k sin Φk2 , k sin Θk2 } ≤         .
                                                                      δ
Corollary 22. Let A ∈ Rm×n , with m ≥ n, have rank n, and let U ∈ Rm×n be the matrix of n
left singular vectors corresponding to the non-zero singular values σ1 ≥ . . . ≥ σn > 0 of A. Let
Ae = A + E. Let U  e ∈ Rm×n be the matrix of n left singular vectors corresponding to the largest n
singular values σe1 ≥ . . . ≥ σ     e and let U
                              en of A,        e⊥ ∈ Rm×(m−n) be the remaining left singular vectors.
Assume kEk2 ≤ ǫσn for some ǫ < 1. Then:

       en ≥ (1 − ǫ)σn ,
    1. σ
        e ⊤ U k2 ≤ kEk2 /e
    2. kU                σn .
          ⊥

Proof. The first claim follows from Lemma 20, and the second follows from Lemma 21 because the
                   e ⊤ U are the sines of the canonical angles between range(U ) and range(U
singular values of U                                                                       e ).
                     ⊥

Lemma 23 (Theorem 3.8, p. 143 in (Stewart and Sun, 1990)). Let A ∈ Rm×n , with m ≥ n, and
    e = A + E. Then
let A
                                      √
                     e+    +       1+ 5                    e+ k22 }kEk2 .
                    kA − A k2 ≤           · max{kA+ k22 , kA
                                     2

C      Recovering the Observation and Transition Matrices
We sketch how to use the technique of (Mossel and Roch, 2006) to recover the observation and
transition matrices explicitly. This is an extra step that can be used in conjunction with our
algorithm.
    Define the n × n matrix [P3,1 ]i,j = Pr[x3 = i, x1 = j].
                                                         P Let Ox = diag(Ox,1 , . . . , Ox,m ), so Ax =
T Ox . Since P3,x,1 = OAx T diag(~π )O⊤ , we have P3,1 = x P3,x,1 = OT T diag(~π )O ⊤ . Therefore

                       U ⊤ P3,x,1 = U ⊤ OT Ox T diag(~π )O⊤
                                   = (U ⊤ OT )Ox (U ⊤ OT )−1 (U ⊤ OT )T diag(~π )O ⊤
                                   = (U ⊤ OT )Ox (U ⊤ OT )−1 (U ⊤ P3,1 ).

The matrix U ⊤ P3,1 has full row rank, so (U ⊤ P3,1 )(U ⊤ P3,1 )+ = I, and thus

                           (U ⊤ P3,x,1 )(U ⊤ P3,1 )+ = (U ⊤ OT ) Ox (U ⊤ OT )−1 .


                                                       29
Since Ox is diagonal, the eigenvalues of (U ⊤ P3,x,1 )(U ⊤ P3,1 )+ are exactly the observation probabil-
ities Or,1 , . . . , Or,m .
    Define i.i.d. random variables gx ∼ N (0, 1) for each x. It is shown in (Mossel and Roch, 2006)
that the eigenvalues of
                                                                            !
                       X                                             X
                            gx (U ⊤ P3,x,1 )(U ⊤ P3,1 )+ = (U ⊤ OT )   gx Ox (U ⊤ OT )−1 .
                  x                                            x

will be separated with high probability (though the separation is roughly on the same order as the
failure probability; this is the main source of instability with this method). Therefore an eigen-
decomposition will recover the columns of (U ⊤ OT ) up to a diagonal scaling matrix S, i.e. U ⊤ OT S.
Then for each x, we can diagonalize (U ⊤ P3,x,1 )(U ⊤ P3,1 )+ :

                       (U ⊤ OT S)−1 (U ⊤ P3,x,1 )(U ⊤ P3,1 )+ (U ⊤ OT S) = Ox .

Now we can form O from the diagonals of Ox . Since O has full column rank, O+ O = Im , so it is
now easy to also recover ~π and T from P1 and P2,1 :

                                       O + P1 = O + O~π = ~π

and
              O+ P2,1 (O+ )⊤ diag(~π )−1 = O+ (OT diag(~π )O ⊤ )(O+ )⊤ diag(~π )−1 = T.
    Note that because (Mossel and Roch, 2006) do not allow more observations than states, they
do not need to work in a lower dimensional subspace such as range(U ). Thus, they perform an
eigen-decomposition of the matrix
                                                           !
                          X                         X
                                        −1
                             gx P3,x,1 P3,1 = (OT )   gx Ox (OT )−1 ,
                             x                          x

and then use the eigenvectors to form the matrix OT . Thus they rely on the stability of the
eigenvectors, which depends heavily on the spacing of the eigenvalues. Consequently, the resulting
sample complexity of the algorithm is polynomial in 1/η (as opposed to log(1/η)) where η is the
allowed probability of failure.


                                                  30
