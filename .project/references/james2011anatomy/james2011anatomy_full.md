#

**Source:** james2011anatomy
**Author:**
**Pages:** 15

---

## Full Text

                                                                                                                          Santa Fe Institute Working Paper 11-05-XXX
                                                                                                                                 arxiv.org:1105.XXXX [physics.gen-ph]
                                                                                    Anatomy of a Bit:
                                                                         Information in a Time Series Observation
                                                           Ryan G. James,1, 2, ∗ Christopher J. Ellison,1, 2, † and James P. Crutchfield1, 2, 3, ‡
                                                                                        1
                                                                                        Complexity Sciences Center
                                                                                           2
                                                                                             Physics Department
                                                                                     University of California at Davis,
                                                                                   One Shields Avenue, Davis, CA 95616
                                                                                            3
                                                                                              Santa Fe Institute
                                                                                1399 Hyde Park Road, Santa Fe, NM 87501
                                                                                         (Dated: October 24, 2018)
                                                         Appealing to several multivariate information measures—some familiar, some new here—we ana-
                                                      lyze the information embedded in discrete-valued stochastic time series. We dissect the uncertainty
                                                      of a single observation to demonstrate how the measures’ asymptotic behavior sheds structural and
arXiv:1105.2988v1 [cs.IT] 16 May 2011


                                                      semantic light on the generating process’s internal information dynamics. The measures scale with
                                                      the length of time window, which captures both intensive (rates of growth) and subextensive com-
                                                      ponents. We provide interpretations for the components, developing explicit relationships between
                                                      them. We also identify the informational component shared between the past and the future that
                                                      is not contained in a single observation. The existence of this component directly motivates the
                                                      notion of a process’s effective (internal) states and indicates why one must build models.
                                                      Keywords: entropy, total correlation, multivariate mutual information, binding information, en-
                                                      tropy rate, predictive information rate

                                                      PACS numbers: 02.50.-r 89.70.+c 05.45.Tp 02.50.Ey 02.50.Ga


                                                                                                         compressed. In fact, a single observation tells us the os-
                                          A single measurement, when considered in the                   cillation’s phase. And, with this single bit of information,
                                        context of the past and the future, contains a                   we have learned everything—the full bit that the time se-
                                        wealth of information, including distinct kinds of               ries contains. Most systems fall somewhere between these
                                        information. Can the present measurement be                      two extremes. Here, we develop an analysis of the infor-
                                        predicted from the past? From the future? Or,                    mation contained in a single measurement that applies
                                        only from them together? Or not at all? Is some                  across this spectrum.
                                        of the measurement due to randomness? Does                          Starting from the most basic considerations, we decon-
                                        that randomness have consequences for the fu-                    struct what a measurement is, using this to directly step
                                        ture or it is simply lost? We answer all of these                through and preview the main results. With that fram-
                                        questions and more, giving a complete dissection                 ing laid out, we reset, introducing and reviewing the rele-
                                        of a measured bit of information.                                vant tools available from multivariate information theory
                                                                                                         including several that have been recently proposed. At
                                                                                                         that point, we give a synthesis employing information
                                                          I.    INTRODUCTION                             measures and the graphical equivalent of the informa-
                                                                                                         tion diagram. The result is a systematic delineation of
                                           In a time series of observations, what can we learn           the kinds of information that the distribution of single
                                        from just a single observation? If the series is a se-           measurements can contain and their required contexts
                                        quence of coin flips, a single observation tells us noth-        of interpretation. We conclude by indicating what is
                                        ing of the past nor of the future. It gives a single bit         missing in previous answers to the measurement question
                                        of information about the present—one bit out of the in-          above, identifying what they do and do not contribute,
                                        finite amount the time series contains. However, if the          and why alternative state-centric analyses are ultimately
                                        time series is periodic—say, alternating 0s and 1s—then          more comprehensive.
                                        with a single measurement in hand, the entire observa-
                                        tion series need not be stored; it can be substantially
                                                                                                                   II.   A MEASUREMENT: A SYNOPSIS

                                        ∗ rgjames@ucdavis.edu                                              For our purposes an instrument is simply an interface
                                        † cellison@cse.ucdavis.edu                                       between an observer and the system to which it attends.
                                        ‡ chaos@cse.ucdavis.edu
                                                                                                         All the observer sees is the instrument’s output—here, we
                                                                                                                              2

take this to be one of k discrete values. And, from a series      bits for n observations.            Here, the function H[P ]
of these outputs, the observer’s goal is to infer and to          is Shannon’s entropy of the distribution P                  =
understand as much about the system as possible—how               (n1 /n, n2 /n, . . . , nk /n). As a shorthand, when discussing
predictable it is, what are the active degrees of freedom,        the information in a random variable X that is dis-
what resources are implicated in generating its behavior,         tributed according to P , we also write H[X]. Thus, to the
and the like.                                                     extent that H[X] ≤ log2 k, as the series length n grows
   The first step in reaching the goal is that the observer       the observer can effectively compress the original series
must store at least one measurement. How many decimal             of observations and so use less storage than n log2 k.
digits must its storage device have? To specify which one            The relationship between the raw measurement
of k instrument outputs occurred the device must use              (log2 k) and the average-case view (H[X]), that we just
log10 k decimal digits. If the device stores binary values,       laid out explicitly, is illustrated in the contrast between
then it must provide log2 k bits of storage. This is the          Figs. 1(a) and 1(b). The difference R1 = log2 k − H[X]
maximum for a one-time measurement. If we perform                 is the amount of redundant information in the raw mea-
a series of n measurements, then the observer’s storage           surements. As such, the magnitude of R1 indicates how
device must have a capacity of n log2 k bits.                     much they can be compressed.
   Imagine, however, that over this series of measure-               Information storage can be reduced further, since us-
ments it happens that output 1 occurs n1 times, 2 occurs          ing H[X] as the amount of information in a measurement
n2 times, and so on, with k occurring nk times. It turns          implicitly assumed the instrument’s outputs were statis-
out that the storage device can have much less capac-             tically independent. And this, as it turns out, leads to
ity; using less, sometimes substantially less, than n log2 k      H[X] being an overestimate as to the amount of infor-
bits.                                                             mation in X. For general information sources, there are
   To see this, recall that the number M of possible se-          correlations and restrictions between successive measure-
quences of n measurements with n1 , n2 , . . . , nk counts is     ments that violate this independence assumption and,
given by the multinomial coefficient:                             helpfully, we can use these to further compress sequences
                                                                of measurements—X1 , X2 , . . . , X` . Concretely, informa-
                                     n                            tion theory tells us that the irreducible information per
                   M=
                           n1 n2 · · · nk                         observation is given by the Shannon entropy rate:
                               n!
                      =                  .                                                       H(`)
                         n1 ! · · · nk !                                               hµ = lim       ,                     (1)
                                                                                             `→∞  `
So, to specify which sequence occurred we need no more
                                                                  where H(`) = − {x` } Pr(x` ) log2 Pr(x` ) is the block en-
                                                                                     P
than:
                                                                  tropy—the Shannon entropy of the length-` word distri-
              k log2 n + log2 M + log2 n + · · ·                  bution Pr(x` ).
                                                                     The improved view of the information in a measure-
The first term is the maximum number of bits to store the         ment is given in Fig. 1(c). Specifically, since hµ ≤ H[X],
count ni of each of the k output values. The second term          we can compress even more; indeed, by an amount
is the number of bits needed to specify the particular            R∞ = log2 k − hµ .
observed sequence within the class of sequences that have            These comments are no more than a review of basic
counts n1 , n2 , . . . , nk . The third term is the number b of   information theory [1] that used a little algebra. They
bits to specify the number of bits in n itself. Finally, the      do, however, set the stage for a parallel, but more de-
ellipsis indicates that we have to specify the number of          tailed, analysis of the information in an observation. In
bits to specify b (log2 log2 n) and so on, until there is less    focusing on a single measurement, the following comple-
than one bit.                                                     ments recent, more sophisticated analyses of information
   We can make sense of this and so develop a help-               sources that focused on a process’s hidden states [2, and
ful comparison to the original storage estimate of                references therein]. In the sense that the latter is a state-
√log2 k bits,n if we apply Stirling’s approximation: n! ≈
n                                                                 centric informational analysis of a process, the following
  2πn (n/e) . For a sufficiently long measurement series,         takes the complementary measurement-centric view.
a little algebra gives:                                              Partly as preview and partly to orient ourselves on the
                                                                  path to be followed, we illustrate the main results in a
                          k
                          X ni             ni                     pictorial fashion similar to that just given; see Fig. 2
          log2 M ≈ −n               log2
                          i=1
                                n          n                      which further dissects the information in X.
                                                                     As a first cut, the information H[X] provided by each
                   = nH[n1 /n, n2 /n, . . . , nk /n] .
                                                                                                                       3

                                                             hµ and ρµ . It partitions H[X] into a piece wµ that is
                                                             structural and a piece rµ that, as mentioned above, is
                            R1                               ephemeral. (See Fig. 2(d).)
                                         R∞                     With the basic informational components contained in
                                                             a single measurement laid out, we now derive them from
             log2 k                                          first principles. The next step is to address information in
                                                             collections of random variables, helpful in a broad array
                            H[X]                             of problems. We then specialize to time series; viz., one-
                                         hµ                  dimensional chains of random variables.


              (a)           (b)          (c)

FIG. 1. Dissecting information in a single measurement X              III.   INFORMATION MEASURES
being one of k values.

                                                                Shannon’s information theory [1] is a widely used
                                   bµ                        mathematical framework with many advantages in the
                      ρµ                                     study of complex, nonlinear systems. Most importantly,
                                   qµ             wµ         it provides a unified quantitative way to analyze systems
                                                             with broadly dissimilar physical substrates. It further
                                                             makes no assumptions as to the types of correlation be-
     H[X]                          bµ
                                                             tween variables, picking up multi-way nonlinear interac-
                                                             tions just as easily as simple pairwise linear correlations.
                      hµ                                        The workhorse of information theory is the Shannon
                                   rµ             rµ         entropy of a random variable, just introduced. The en-
                                                             tropy measures what would commonly be considered the
                                                             amount of information learned, on average, from ob-
       (a)            (b)          (c)            (d)        serving a sample from that random variable. The en-
                                                             tropy H[X] of a random variable X taking on values
                                                             x ∈ A = {1, . . . , k} with distribution Pr(X = x) has the
         FIG. 2. Systematic dissection of H[X].
                                                             following functional form:
                                                                                       X
observation (Fig. 2(a)) can be broken into two pieces:                    H[X] = −         Pr(x) log2 Pr(x) .         (2)
                                                                                     x∈A
one part is information ρµ that could be anticipated
from prior observations and the other hµ —the random         The entropy is defined in the same manner over joint
component—is that which could not be anticipated. (See       random variables—say, X and Y —where the above dis-
Fig. 2(b).) Each of these pieces can be further decom-       tribution is replaced by the joint probability Pr(X, Y ).
posed into two parts. The random component hµ breaks            When considering more than a single random variable,
into two kinds of randomness: a part bµ relevant for         it is quite reasonable to ask how much uncertainty re-
predicting the future, while the remaining part rµ is        mains in one variable given knowledge of the other. The
ephemeral, existing only for the moment.                     average entropy in one variable X given the outcome of
   The redundant portion ρµ of H[X] in turn splits into      another variable Y is the conditional entropy:
two pieces. The first part—also bµ when the process is
stationary—is shared between the past and the current                        H[X|Y ] = H[X, Y ] − H[Y ] .            (3)
observation, but its relevance stops there. The second
piece qµ is anticipated by the past, is present currently,   That is, it is the entropy of the joint random variable
and also plays a role in future behavior. Notably, this      (X, Y ) with the marginal entropy H[Y ] of Y subtracted
informational piece can be negative. (See Fig. 2(c).)        from it.
   We can further combine all elements of H[X] that             The fundamental measure of correlation between ran-
participate in structure—whether it be past, future, or      dom variables is the mutual information. As stated be-
both—into a single element wµ . This decomposition           fore, it can be adapted to measure all kinds of interaction
of H[X] provides a very different decomposition than         between two variables. It can be written in several forms,
                                                                                                                                4

including:                                                       ment is denoted Ā = ΩN \A. Finally, we use a shorthand
                                                                 to refer to the set of random variables corresponding to
        I[X; Y ] =H[X] + H[Y ] − H[X, Y ]                 (4)    index set A:
                 =H[X, Y ] − H[X|Y ] − H[Y |X] .          (5)
                                                                                       XA ≡ {Xi : i ∈ A} .                    (8)
Two variables are generally considered independent if
their mutual information is zero.                                   There are at least three extensions of the two-variable
   Like the entropy, the mutual information can also             mutual information, each based on a different interpre-
be conditioned on another variable, say Z, resulting in          tation of what its original definition intended. The
the conditional mutual information. Its definition is a          first is the multivariate mutual information or co-
straightforward modification of Eq. (4):                         information [3]: I[X0 ; X1 ; . . . ; XN −1 ]. Denoted I[X0:N ],
                                                                 it is the amount of mutual information to which all vari-
    I[X; Y |Z] = H[X|Z] + H[Y |Z] − H[X, Y |Z] .          (6)    ables contribute:
                                                                                                                            
   For example, consider two random variables X and Y                             X                         Y            |v|
                                                                     I[X0:N ] = −    Pr(x0:N ) log2            Pr(xA )−1 
that take the values 0 or 1 independently and uniformly,
                                                                                                             A∈P (N )
and a third Z = X XOR Y , the exclusive-or of the two.                          X
There is a total of two bits of information among the                        =−  (−1)|A| H[XA ]                               (9)
three variables: H[X, Y, Z] = 2 bits. Furthermore, the                          A∈P (N )
variables X and Y share a single bit of information with
                                                                                               X
                                                                             = H[X0:N ] −          I[XA |XĀ ] ,             (10)
Z, their parity. Thus, I[X, Y ; Z] = 1 bit. Interestingly,                                   A∈P (N )
although X and Y are independent, I[X; Y ] = 0, they                                         0<|A|<N

are not conditionally independent: I[X; Y |Z] = 1.
                                                                 where, e.g., I[X{1,3,4} |X{0,2} ] = I[X1 ; X3 ; X4 |X0 , X2 ]. It
                                                                 can be verified that Eq. (9) is a generalization of Eq. (4),
                                                                 adding and subtracting all possible entropies according
      IV.    MULTIVARIATE INFORMATION
                   MEASURES                                      to the number of random variables they include. The
                                                                 co-information has several interesting properties. First,
                                                                 it can be negative, though a consistent interpretation of
  We now turn to a difficult problem: How does one
                                                                 what this means is still lacking in the literature. Second,
quantify interactions among an arbitrary set of variables?
                                                                 this measure vanishes if any two variables in the set are
As just noted, the mutual information provides a very
                                                                 completely independent. (That is, they are independent
general, widely applicable method of measuring depen-
                                                                 and also conditionally independent with respect to all
dence between two, possibly composite, random vari-
                                                                 subsets of the other variables.) This is true regardless of
ables. The challenge comes in the fact that there exist
                                                                 interdependencies among the other variables.
several distinct methods for measuring dependence be-
                                                                    In the second interpretation, the mutual information
tween more than two random variables.
                                                                 is seen as the relative entropy between a joint distribu-
  Consider a finite set A and random variables Xi taking
                                                                 tion and the product of its marginals. Specifically, the
on values xi ∈ A for all i ∈ Z. The vector of N random
                                                                 starting point is:
variables X0:N = {X0 , X1 , . . . , XN −1 } takes on values in
AN . A straightforward generalization of Eq. (2) yields                                  X                    Pr(x, y)
the joint entropy:                                                        I[X; Y ] =         Pr(x, y) log2               ,   (11)
                                                                                                             Pr(x) Pr(y)
                      X
       H[X0:N ] = −        Pr(x0:N ) log2 Pr(x0:N ) ,      (7)   which is simply a rewriting of Eq. (4). When generalized
                      {x0:N }                                    from this form, we obtain the total correlation [4]:
which measures the total amount of information con-                             X                 
                                                                                                        Pr(x0:N )
                                                                                                                          
tained in the joint distribution. From here onward,                 T [X0:N ] =    Pr(x0:N ) log2
                                                                                                    Pr(x0 ) . . . Pr(xN )
we suppress notating the set {x0:N } of realizations over                       X
which the sums are taken.                                                     =    H[XA ] − H[X0:N ] .                     (12)
                                                                               A∈P (N )
  In generalizing the mutual information to arbitrary                            |A|=1
sets of variables, we make use of power sets. We let
ΩN = {0, 1, . . . , N − 1} denote the universal                  The total correlation is sometimes referred to as the
                                              set over the
variable indices and define P (N ) = P ΩN as the power           “multi-information”, though we refrain from using this
set over ΩN . Then, for any set A ∈ P (N ), its comple-          ambiguous term. It differs from the prior measure in
                                                                                                                           5

many fundamental ways. To begin with, it is nonnega-                        X:0             X0              X1:
tive. It also differs in that if X0 is independent of the
others, then T [X0:N ] = T [X1:N ]. Finally, it captures           ···   X−3 X−2 X−1        X0    X1     X2    X3    ···
only the difference between individual variables and the
entire set. The role of two-way and higher interactions         FIG. 3. A process’s time series: Time indices less than zero
                                                                refer to the past X:0 ; index 0 to the present X0 ; and times
is ignored as it leaves out the relative entropies between
                                                                after 0 to the future X1: .
the entire set and more-than-two-variable marginals. In-
deed, this is a common problem. The total correlation
and the next measure miss or, at best, conflate (n > 2)-           W [X0:N ] is close to the binding information, except
way interactions.                                               that it uses the sum of marginals not the joint entropy.
   The last extension stems from the view that mutual in-       As such, it seems to more consistently capture the role
formation is the joint entropy minus all (single-variable)      of single variables within a set than B[X0:N ], which com-
unshared information—that is, we start from Eq. (5).            pares the set’s joint entropy to individual residual uncer-
When interpreted this way, the generalization is called         tainties.
the binding information [5]:                                       Third and finally, there is a measure which, for lack of
                                     X                          a better name, we call the enigmatic information:
         B[X0:N ] = H[X0:N ] −           H[XA |XĀ ] .   (13)
                                   A∈P (N )
                                    |A|=1
                                                                             Q[X0:N ] = T [X0:N ] − B[X0:N ] .          (18)

Like the total correlation, the binding information is          Like the multivariate mutual information—which it
nonnegative and independent random variables do not             equals when N = 3—it can be negative. Its operational
change its value. Note that B[X0:N ] is a first approxima-      meaning will become clear on further discussion.
tion to the multivariate information of Eq. (9) when the
sets A are restricted to singleton sets.
   We next define three additional multivariate informa-                           V.   TIME SERIES
tion measures that have not been studied previously, but
appear following a similar strategy. First, we have the            We now adapt the general multivariate measures to an-
amount of information in individual variables that is not       alyze discrete-valued, discrete-time series generated by a
shared in any way. This is the residual entropy:                stationary process. That is, rather than analyzing sets
                                                                of random variables, we specialize to a one-dimensional
             R[X0:N ] = H[X0:N ] − B[X0:N ]                     chain of them. In this setting, the measures are most ap-
                                                                propriately applied to successively longer blocks of con-
                        X
                      =    H[XA |XĀ ] .                 (14)
                        A∈P (N )                                secutive observations. This allows us to study the asymp-
                          |A|=1
                                                                totic block-length behavior of each, mimicking the ap-
                                                                proach of Ref. [2, 6]. For the class of processes known
In a sense, it is an anti-mutual information: It measures
                                                                as finitary (defined shortly), each of these measures tend
the total amount of randomness localized to an individual
                                                                to a linear asymptote characterized by a subextensive
variable and so not correlated to that in its peers.
                                                                component and an extensive component controlled by an
  Second, we can sum the total correlation and the bind-
                                                                asymptotic growth rate.
ing information. Then we have the local exogenous infor-
                                                                   Let’s first state more precisely and introduce the nota-
mation:
                                                                tion for the class of processes that are the object of study.
         W [X0:N ] = B[X0:N ] + T [X0:N ]                (15)   We consider a bi-infinite chain . . . X−1 X0 X1 . . . of ran-
                     X                                          dom variables. Each Xt , t ∈ Z, takes on a finite set of
                   =    (H[XA ] − H[XA |XĀ ])           (16)   values xt ∈ A. We denote contiguous subsets of the time
                   A∈P (N )                                     series with XA:B where the left index is inclusive and the
                       |A|=1
                       X                                        right is exclusive. By leaving one of the indices off the
                   =       I[XA ; XĀ ] .                (17)   subset is partially infinite in that direction. We divide
                   A∈P (N )
                       |A|=1
                                                                this bi-infinite chain into three segments. First we single
                                                                out the present X0 . All the symbols prior to the present
It is the amount of information in each variable that           are the past X:0 . The symbols following the present are
comes from its peers. It is a “very mutual” information,        the future X1: . Figure 3 illustrates the setting.
one that discounts for the randomness produced locally—            Our focus is on the `-blocks Xt:t+`                     =
that randomness inherent in each variable individually.         Xt Xt+1 · · · Xt+`−1 . The associated process is spec-
                                                                                                                                           6

ified by the set of length-` word distributions:
{Pr(Xt:t+` ) : t ∈ Z, ` ∈ N}. We consider only sta-                                             H(`)
tionary processes for which Pr(Xt:t+` ) = Pr(X0:` ).                                            T (`)


                                                              Information [bits]
And so, we drop the absolute-time index t. More pre-
cisely, the word probabilities derive from an underlying
time-shift invariant, ergodic measure µ on the space of                             E

bi-infinite sequences.
   In the following, an information measure F applied to                            0
to the process’s length-` words is denoted F[X0:` ] or, as
a shorthand, F(`).                                                                 −E
                                                                                        0   1             2        3        4      5   6
                                                                                                        Block length ` [symbols]

    A.   Block Entropy versus Total Correlation               FIG. 4. Block entropy H(`) and block total correlation T (`)
                                                              illustrating their behaviors for the NRPS Process.
   We begin with the long-studied block entropy informa-
tion measure H(`) [7, 8]. (For a review and background
to the following see Ref. [6].) The block entropy curve       That is, ρµ = lim`→∞ T (`)/`. Finally, T (`) is monotone
defines two primary features. First, its growth rate limits   increasing, but concave up. All of this is derived directly
to the entropy rate hµ . Second, its subextensive compo-      from Eqs. (20) and (21), by using well known properties
nent is the excess entropy E:                                 of the block entropy.
                                                                 The block entropy and block total correlation are plot-
                    E = I[X:0 ; X0: ] ,               (19)    ted in Fig. 4. Both measures are 0 at ` = 0 and from
                                                              there approach their asymptotic behavior, denoted by
which expresses the totality of information shared be-        the dashed lines. Though their asymptotic slopes appear
tween the past and future.                                    to be the same, they in fact differ. Numerical data for
   The entropy rate and excess entropy, and the way in        the asymptotic values can be found in Tables I and II
which they are approached with increasing block length,       under the heading NRPS (defined later).
are commonly used quantifiers for complexity in many             There is a persistent confusion in the neuroscience,
fields. They are complementary in the sense that, for         complex systems, and information theory literatures con-
finitary processes, the block entropy for sufficiently long   cerning the relationship between block entropy and block
blocks takes the form:                                        total correlation. This can be alleviated by explicitly
                                                              demonstrating a partial symmetry between the two in
                    H(`) ∼ E + `hµ .                  (20)    the time series setting and by highlighting a weakness of
                                                              the total correlation.
Recall that H(0) = 0 and that H(`) is monotone increas-
                                                                 We begin by showing how, for stationary processes,
ing and concave down. The finitary processes, mentioned
                                                              the block entropy and the block total correlation contain
above, are those with finite E.
                                                              much the same information. From Eqs. (7) and (12) we
  Next, we turn to a less well studied measure for
                                                              immediately see that:
time series—the block total correlation T (`). Adapting
Eq. (12) to a stationary process gives its definition:                                           H(`) + T (`) = `H(1) .                (23)
                 T (`) = `H[X0 ] − H(`) .             (21)    Furthermore, by substituting Eqs. (20) and (22) in
                                                              Eq. (23) we note that the righthand side has no subex-
Note that T (0) = 0 and T (1) = 0. Effectively, it com-
                                                              tensive component. This gives further proof that the
pares a process’s block entropy to the case of indepen-
                                                              subextensive components of Eqs. (20) and (22) must be
dent, identically distributed random variables. In many
                                                              equal and opposite, as claimed. Moreover, by equating
ways, the block total correlation is the reverse side of an
                                                              individual `-terms we find:
information-theoretic coin for which the block entropy is
the obverse. For finitary processes, its growth rate limits                                             hµ + ρµ = H(1) .               (24)
to a constant ρµ and its subextensive part is a constant
that turns out to be −E:                                      And, this is the decomposition given in Fig. 2(b): the
                                                              lefthand side provides two pieces comprising the single-
                   T (`) ∼ −E + `ρµ .                 (22)    observation entropy H(1).
                                                                                                                        7

   Continuing, either information measure can be used to      information, and residual entropy constitute a refinement
obtain the excess entropy. In addition, since the block en-   of the single-measurement decomposition provided by the
tropy provides hµ as well as intrinsically containing H(1),   block entropy and the total correlation [5, 11]. To begin,
ρµ can be directly obtained from the block entropy func-      their block equivalents are, respectively:
tion by taking H(1) − hµ , yielding ρµ . The same is not
true, however, for the total correlation. Though ρµ can                          B(`) = H(`) − R(`)                  (30)
be computed, one cannot obtain hµ from T (`) alone—                              Q(`) = T (`) − B(`)                 (31)
H(1) is required, but not available from T (`), since it is                     W (`) = B(`) + T (`) ,               (32)
subtracted out.
   There are further parallels between the two quantities     where R(`) does not have an analogously simple form.
that can be drawn. First, following Ref. [6], we define       Their asymptotic behaviors are, respectively:
discrete derivatives of the block measures at length `:
                                                                                  R(`) ∼ ER + `rµ                    (33)
                      h` = H(`) − H(` − 1)            (25)
                                                                                 B(`) ∼ EB + `bµ                     (34)
                      ρ` = T (`) − T (` − 1) .        (26)
                                                                                  Q(`) ∼ EQ + `qµ                    (35)
These approach hµ and ρµ , respectively. From them we                            W (`) ∼ EW + `wµ .                  (36)
can determine the subextensive components by discrete
integration, while subtracting out the asymptotic behav-      Their associated rates break the prior two components
ior. We find that:                                            (hµ and ρµ ) into finer pieces. Substituting their defini-
                                                              tions into Eqs. (7) and (21) we have:
                             ∞
                             X
                      E=           (h` − hµ )         (27)                H(`) = B(`) + R(`)                         (37)
                             `=1
                                                                                = (EB + ER ) + `(bµ + rµ )           (38)
and also that                                                             T (`) = B(`) + Q(`)                        (39)
                             ∞                                                  = (EB + EQ ) + `(bµ + qµ ) .         (40)
                             X
                      E=−          (ρ` − ρµ ) .       (28)
                             `=1
                                                              The rates in Eqs. (38) and (40) corresponding to hµ
                                                              and ρµ , respectively, give the decomposition laid out in
Second, these sums are equal term by term.                    Fig. 2(c) above. Two of these components (bµ and rµ )
  The first sum, however, indirectly brings us back to        were defined in Ref. [5] and the third (qµ ) is a direct ex-
Eq. (24). Since h1 = H(1), we have:                           tension. We defer interpreting them to Sec. VI B which
                                ∞
                                                              provides greater understanding by appealing to the se-
                                                              mantics afforded by the process information diagram de-
                                X
                     E = ρµ +         (h` − hµ ) .    (29)
                                `=2
                                                              veloped there.
                                                                The local exogenous information, rather than refining
   Finally, it has been said that the total correlation       the decomposition provided by the block entropy and the
(“multi-information”) is the first term in E [9, 10]. This    total correlation, provides a different decomposition:
has perhaps given the impression that the total corre-
lation is only useful as a crude approximation. Equa-                      W (`) =B(`) + T (`)                       (41)
tion (29) shows that it is actually the total correlation                        =(EB − E) + `(bµ + ρµ ) .           (42)
rate ρµ that is E’s first term. As we just showed, the
total correlation is more useful than being a first term      So, wµ = hµ + ρµ , as mentioned in Fig. 2(d).
in an expansion. Its utility is ultimately limited, though,      Similar to Eq. (23), we can take the local exogenous
since its properties are redundant with that of the block     information together with the residual entropy and find:
entropy which, in addition, gives the process’s entropy
rate hµ .                                                                      R(`) + W (`) = `H(1) .                (43)

                                                              This implies that ER = −EW and that rµ and wµ are
                B.    A Finer Decomposition
                                                              yet another partitioning of H[X], as shown earlier in
                                                              Fig. 2(d).
                                                                Figure 5 illustrates these four block measures for a
  We now show how, in the time series setting, the bind-
                                                              generic process. Each of the four measures reaches
ing information, local exogenous information, enigmatic
                                                                                                                                                8

                                                                                       dent. Finite-state processes with positive hµ are stochas-
                                          R(`)                                         tic, however. So, observations become (conditionally)
                                          B(`)                                         decoupled exponentially fast. Thus, for arbitrarily long
Information [bits]


                                          Q(`)                                         blocks, the first and the last observations tend toward
                                          W (`)                                        independence exponentially and so I(`) limits to 0.
                                                                                          The second proposition regards the growth rate iµ .

                          ER                                                           Proposition 2. For all finite-state processes:
                          EB
                                                                                                                iµ = 0 .                     (47)
                     EQ , EW
                               0      2         4        6        8        10   12
                                              Block length ` [symbols]
                                                                                          The intuition behind this follows from the first propo-
                     FIG. 5. Block equivalents of the residual entropy R(`), bind-     sition. If hµ > 0, then it is clear that since I(`) tends
                     ing information B(`), enigmatic information Q(`), and local       toward 0, then the slope must also tend toward 0. What
                     exogenous information W (`) for a generic process (same as        remains are those processes that are finite state but
                     previous figure).
                                                                                       for which hµ = 0. These are the periodic processes.
                                                                                       For them, iµ also vanishes since, although I(`) may be
                     asymptotic linear behavior at a length of ` = 9 symbols.          nonzero, there is a finite amount of information contained
                     Once there, we see that they each possess a slope that we         in a bi-infinite periodic sequence. Once all this informa-
                     just showed to be a decomposition of the slopes from the          tion has been accounted for at a particular block length,
                     measures in Fig. 4. Furthermore, each has a subextensive          then for all blocks larger than this there is no additional
                     component that is found as the y-intercept of the linear          information to gain. And so, iµ decays to 0.
                     asymptote. These subextensive parts provide a decom-                 The final result concerns the subextensive component
                     position of the excess entropy, discussed further below in        I.
                     Sec. VI B 3.
                                                                                       Proposition 3. For all finite-state processes with
                                                                                       hµ > 0:
                               C.   Multivariate Mutual Information
                                                                                                                 I=0.                        (48)
                       Lastly, we come to the block equivalent of the multi-
                     variate mutual information I[X0:N ]:
                                                       X                                  This follows directly from the previous two proposi-
                                    I(`) = H(`) −          I[XA |XĀ ] .        (44)   tions.
                                                      A∈P (`)                             Thus, the block multivariate mutual information is
                                                      0<|A|<`
                                                                                       qualitatively different from the other block measures. It
                     Superficially, it scales similarly to the other measures:         appears to be most interesting for infinitary processes
                                                                                       with infinite excess entropy.
                                             I(`) ∼ I + `iµ ,                   (45)      Figure 6 demonstrates the general behavior of I(`),
                                                                                       illustrating the three propositions. The dashed line high-
                     with an asymptotic growth rate iµ and a constant subex-           lights the asymptotic behavior of I(`): both I and iµ
                     tensive component I. Yet, it has differing implications           vanish. We further see that I(`) is not restricted to pos-
                     regarding what it captures in the process. This is drawn          itive values. It oscillates about 0 until length ` = 11
                     out by the following propositions, whose proofs appear            where it finally vanishes.
                     elsewhere.
                        The first concerns the subextensive part of I(`).
                                                                                                VI.   INFORMATION DIAGRAMS
                     Proposition 1. For all finite-state processes:
                                                                                          Information diagrams [12] provide a graphical and in-
                                    hµ > 0        ⇒     lim I(`) = 0 .          (46)   tuitive way to interpret the information-theoretic rela-
                                                        `→∞
                                                                                       tionships among variables. In construction and concept,
                                                                                       they are very similar to Venn diagrams. The key dif-
                       The intuition behind this is fairly straightforward. For        ference is that the measure used is a Shannon entropy
                     I(`) to be nonzero, no two observations can be indepen-           rather than a set size. Additionally, an overlap is not
                                                                                                                                              9

                                                                                                              X        Y
                                                                       I(`)

                                                                                                       W                     Z
  Information [bits]


                                                                                                      (a)Joint entropy, Eq. (7)


                       I


                           0      2      4        6        8      10          12
                                       Block length ` [symbols]
                                                                                             (b)Multivariate         (c)Total correlation,
FIG. 6. Block multivariate mutual information I(`) for the                                  mutual information,            Eq. (12)
                                                                                                 Eq. (9)
same example process as before.


set intersection but rather a mutual information. The
irreducible intersections are, in fact, elementary atoms
of a sigma-algebra over the random-variable event space.
An atom’s size reflects the magnitude of one or another                                    (d)Binding information,   (e)Residual entropy,
Shannon information measure—marginal, joint, or con-                                              Eq. (13)                 Eq. (14)
ditional entropy or mutual information.


                           A.   Four-Variable Information Diagrams

   Using information diagrams we can deepen our un-
                                                                                             (f)Local exogenous          (g)Enigmatic
derstanding of the multivariate informations defined                                        information, Eq. (17)    information, Eq. (18)
in Sec. IV. Fig. 7 illustrates them for four random
variables—X, Y , Z, W . There, an atom’s shade of gray                             FIG. 7. Four-variable information diagrams for the multivari-
denotes how much weight it carries in the overall value                            ate information measures of Sec. IV. Darker shades of gray
of its measure. Consider for example the total corre-                              denote heavier weighting in the corresponding informational
lation I-diagram in Fig. 7(c). From the definition of                              sum. For example, the atoms to which all four variables con-
                                                                                   tribute are added thrice to the total correlation and so the
the total correlation, Eq. (12), we see that each vari-
                                                                                   central atom’s weight I[W ; X; Y ; Z] = 3.
able provides one count to each of its atoms and then a
count is removed from each atom. Thus, the atom as-
sociated with four-way intersection W ∩ X ∩ Y ∩ Z con-
tained in each of the four variables carries a total weight                        be easily seen. The multivariate mutual information,
I[W ; X; Y ; Z] = 4 − 1 = 3. Those atoms contained in                              Fig. 7(b), stands out in that it is isolated to a single
three variables carry a weight of 2, those shared among                            atom, that contained in all variables. This makes it
only two variables a weight of 1, and information solely                           clear why the independence of any two of the variables
contained in one variable is not counted at all.                                   leads to a zero value for this measure. The total cor-
   Utilizing the I-diagrams in Fig. 7, we can easily visu-                         relation, Fig. 7(c), contains all atoms contained in at
alize and intuit how these various information measures                            least two variables and gives higher weight to those con-
relate to each other and the distributions they represent.                         tained in more variables. The local exogenous informa-
In Fig. 7(a), we find the joint entropy. Since it represents                       tion, Fig. 7(f), is similar. It counts the same atoms as the
all information contained in the distribution with no bias                         total correlation does, but it gives them higher weight.
to any sort of interaction, we see that it counts each                             Lastly, the binding information, Fig. 7(d), also counts
and every atom once. The residual entropy, Fig. 7(e),                              the same atoms, but only weights each of them once re-
is equally easy to interpret: it counts each atom which is                         gardless of how many variables they participate in.
not shared by two or more variables.                                                  The lone enigmatic information, Fig. 7(g), counts only
   The distinctions in the menagerie of measures attempt-                          those variables that participate in at least three variables
ing to capture interactions among N variables can also                             and, similar to the total correlation, it counts those that
                                                                                                                            10

participate in more variables more heavily.                                                 H[X0 ]

                                                                                               rµ
                                                                            H[X:0 ]                           H[X1: ]
          B.   Process Information Diagrams
                                                                                      bµ               bµ
   Following Ref. [13] we adapt the multivariate I-                                            qµ
diagrams just laid out to tracking information in finitary
stationary processes. In particular, we develop process
I-diagrams to explain the information in a single observa-                                     σµ
tion, as described before in Fig. 2. The resulting process
I-diagram is displayed in Fig. 8. As we will see, exploring
the diagram gives a greater, semantic understanding of          FIG. 8. I-diagram anatomy of H[X0 ] in the full context of
                                                                time: The past X:0 partitions H[X0 ] into two pieces: hµ and
the relationships among the process variables and, as we
                                                                ρµ . The future X0: then partitions those further into rµ , two
will emphasize, of the internal structure of the process        bµ s, and qµ . This leaves a component σµ , shared by the past
itself.                                                         and the future, that is not in the present X0 .
   For all measures, except the multivariate mutual in-
formation, the extensive rate corresponds to one or more
atoms in the decomposition of H[X0 ]. To begin, we al-          terpreted an indicator of complex behavior since, for a
low H[X0 ] to be split in two by the past. This exposes         fixed bµ , larger hµ values imply less temporal structure
two pieces: hµ , the part exterior to the past, and ρµ , the    in the time series.
part interior. This partitioning has been well studied in          Due to stationarity, the mutual information
information theory due to how it naturally arises as one        I[X0 ; X1: |X:0 ] between the present X0 and the fu-
observes a sequence. This decomposition is displayed in         ture X1: conditioned on the past X:0 is the same as the
Fig. 9(a).                                                      mutual information I[X0 ; X:0 |X1: ] between X0 and the
   Taking a step back and including the future in the           past X:0 conditioned on the future X1: . Moreover, both
diagram, we obtain a more detailed understanding of             are bµ . This lends a symmetry to the process I-diagram
how information is transmitted in a process. The past           that does not exist for nonstationary processes. Thus,
and the future together divide H[X0 ] into four parts; see      bµ atoms in Fig. 8 are the same size.
Fig. 9(b). We will discuss each part shortly. First, how-          There are two atoms remaining in the process I-
ever, we draw out a different decomposition—that into           diagram that have not been discussed in literature. Both
rµ and wµ as seen in Fig. 9(c). From this diagram it is         merit attention. The first is qµ —the information shared
easy to see the semantic meaning behind the decompo-            by the past, the present, and the future. Notably, its
sition: rµ being divorced from any temporal structure,          value can be negative and we discuss this further below in
while wµ is steeped in it.                                      Sec. VI B 1. The other piece, denoted σµ , is a component
   We finally turn to the partitioning shown in Fig. 9(b).      of information shared between the past and the future
The process I-diagram makes it rather transparent in            that does not exist in the present observation. This piece
which sense rµ is an amount of ephemeral information:           is vital evidence that attempting to understand a pro-
its atom lies outside both the past and future sets and         cess without using a model for its generating mechanism
so it exists only in the present moment, having no reper-       is ultimately incomplete. We discuss this point further
cussions for the future and being no consequence of the         in Sec. VI B 2 below.
past. It is the amount of information in the present ob-
servation neither communicated to the future nor from
the past. Ref. [5] referred to this as the residual entropy                           1.   Negativity of qµ
rate, as it is the amount of uncertainty that remains in
the present even after accounting for every other variable         The sign of qµ holds valuable information. To see
in the time series.                                             what this is we apply the partial information decompo-
   Ref. [5] also proposed to use bµ as a measure of struc-      sition [14] to further analyze wµ = I[X0 ; X:0 , X1: ]—that
tural complexity [5], and we tend to agree. The argument        portion of the present shared with the past and future.
for this is intuitive: bµ is an amount of information that is   By decomposing wµ into four pieces—three of which are
present now, is not explained by the past, but has reper-       unique—we gain greater insight into the value of qµ and
cussions in the future. That is, it is the portion of the       also draw out potential asymmetries between the past
entropy rate hµ that has consequences. In some contexts         and the future.
one may prefer to employ the ratio bµ /hµ when bµ is in-           The partial information lattice provides us with a
                                                                                                                          11

                                                                                        I[X0 ; X:0 , X1: ]
                                          rµ
                       hµ                                                                    bµ − ι
                                   bµ            bµ
            ρµ                            qµ
                                                                                    ι        ρµ − ι          ι

                 (a)                     (b)
                                                                                    I[X0 ; X:0 ]   I[X0 ; X1: ]

                             rµ
                                                                FIG. 10.       Partial information decomposition of wµ =
                                                                I[X0 ; X:0 , X1: ]. The multivariate mutual information qµ is
                            wµ                                  given by the redundancy Π{X:0 }{X1: } minus the synergy
                                                                Π{X:0 ,X1: } . wµ = ρµ + bµ is the sum of all atoms in this
                                                                diagram.

                             (c)
                                                                qµ means and into the structure of wµ and the process
FIG. 9. The three decompositions of H[X] from Fig. 2. The       as a whole.
dissecting lines are identical to those in Fig. 8.


                                                                          2.   Consequence of σµ : Why we model
method to isolate (i) the contributions Π{X:0 }{X1: } to
wµ that both the past and the future provide redun-                Notably, the final piece of the process I-diagram is not
dantly, (ii) parts Π{X:0 } and Π{X1: } that are uniquely        part of H[X0 ]—not a component of the information in
provided by the past and the future, respectively, and          a single observation. This is σµ , which represents infor-
(iii) a part Π{X:0 ,X1: } that is synergistically provided by   mation that is transmitted from the past to the future,
both the past and the future. Note that, due to station-        but does not go through the currently observed symbol
arity, Π{X:0 } = Π{X1: } . We refer to this as the uniquity     X0 . This is readily understood and leads to an important
and denote it ι.                                                conclusion.
   Using Ref. [14] we see that qµ is equal to the redun-           If one believes that the process under study is gen-
dancy minus the synergy of the past and the future,             erated according to the laws of physics, then the pro-
when determining the present. Thus, if qµ > 0, the past         cess’s internal physical configuration must store all the
and future predominantly contribute information to the          information from the past that is relevant for generat-
present. When qµ < 0, however, considering the past and         ing future behavior. Only when the observed process is
the future separately in determining the present misses         order-1 Markov is it sufficient to keep track of just the
essential correlations. The latter can be teased out if the     current observable. For the plethora of processes that are
past and future are considered together.                        not order-1 or that are non-Markovian altogether, we are
   The process I-diagram (Fig. 8) showed that the mu-           faced with the fact that information relevant for future
tual information between the present and either the past        behavior must be stored somehow. And, this fact is re-
or the future is ρµ . One might suspect from this that          flected in the existence of σµ . When σµ > 0, a complete
the past and the future provide the same information            description of the process requires accounting for this in-
to the present, but this would be incorrect. Though             ternal configurational or, simply, state information. This
they provide the same quantity of information to the            is why we build models and cannot rely on only collecting
present, what that information conveys can differ. This         observation sequences.
is evidence of a process’s structural irreversibility; cf.         The amount of information shared between X:0 and
Refs. [13, 15]. In this light, the redundancy Π{X:0 }{X1: }     X1: , but ignoring X0 , was previously discussed in
between the past and future when considering the present        Ref. [16]. We now see that the meaning of this informa-
is ρµ − ι. Furthermore, the synergy Π{X:0 ,X1: } provided       tion quantity—there denoted I1 —is easily gleaned from
by the past and the future is equal to bµ − ι.                  its components: I1 = qµ + σµ .
   Taking this all together, we find what we already knew:         Furthermore, in Refs. [5], [11], and [16], efficient com-
that qµ = ρµ − bµ , The journey to this conclusion, how-        putation of bµ and I1 were not provided and the brute
ever, provided us with deeper insight into what negative        force estimates are inaccurate and very compute inten-
                                                                                                                       12

sive. Fortunately, by a direct extension of the meth-          mensional processes, differ in two dimensions. We believe
ods developed in Ref. [15] on bidirectional machines,          the semantic differences shown here are evidence that
we can easily compute both rµ = H[X0 |S0+ , S1− ] and          the degeneracy of alternate E-decompositions breaks in
I1 = I[S0+ , S1− ]. This is done by constructing joint prob-   higher dimensions.
abilities of forward-time and reverse-time causal states—
{S + } and {S − }, respectively—at different time indices
employing the dynamic of the bidirectional machine.                              VII.   EXAMPLES
This gives closed-form, exact methods of calculating
these two measures, provided one constructs the process’s         We now make the preceding concrete by calculating
forward and reverse -machines. bµ follows directly in this    these quantities for three different processes, selected to
case since it is the difference of hµ and rµ ; the former is   illustrate a variety of informational properties. Figure 11
also directly calculated from the -machine.                   gives each process via it’s -machine [18]: the Even Pro-
                                                               cess, the Golden Mean Process, and the Noisy Random
                                                               Phase-Slip (NRPS) Process. A process’s -machine con-
                 3.    Decompositions of E
                                                               sists of its causal states—a partitioning of infinite pasts
                                                               into sets that give rise to the same predictions about fu-
   Using the process I-diagram and the tools provided
                                                               ture behavior. The state transitions are labeled p|s where
above, three unique decompositions of the excess entropy,
                                                               s is the observed symbol and p is the conditional proba-
Eq. (19), can be given. Each provides a different inter-
                                                               bility of observing that symbol given the state the process
pretation of how information is transmitted from the past
                                                               is in. The -machine representation for a process is its
to the future.
                                                               minimal unifilar presentation.
   The first is provided by Eqs. (37)-(40). The subexten-
                                                                  Table I begins by showing the single-observation en-
sive parts of the block entropy and total correlation there
                                                               tropy H[1] followed by hµ and ρµ . Note that the Even
determine the excess entropy decomposition. We have:
                                                               and the Golden Mean Processes cannot be differentiated
                                                               using these measures alone. The table then follows with
                  E =EB + ER                           (49)
                                                               the finer decomposition. We now see that the processes
                      = − EB − EQ                      (50)    can be differentiated. We can understand fairly easily
                        1                                      that the Even Process, being infinite-order Markovian,
                      = (ER − EQ )                     (51)
                        2                                      and consisting of blocks of 1s of even length separated by
                          1                                    one or more 0s, exhibits more structure than the Golden
                      = − (EW + EQ ) .                 (52)
                          2                                    Mean Process. (This is rather intuitive if one recalls that
We leave the meaning behind these decompositions as an         the Golden Mean Process has only a single restriction: it
open problem, but do note that they are distinct from          cannot generate sequences with consecutive 0s.) We see
those discussed next.                                          that, for the Even Process, rµ is 0. This can be under-
  The second and third decompositions both derive di-          stood by considering a bi-infinite sample from the Even
rectly from the process I-diagram of Fig. 8. Without           Process with a single gap in it. The structure of this pro-
further work, one can easily see that the excess entropy       cess is such that we can always and immediately identify
breaks into three pieces, all previously discussed:            what that missing symbol must be.
                                                                  These two processes are further differentiated by qµ ,
                      E = bµ + qµ + σµ .               (53)    where it is negative for the Even Process and positive for
                                                               the Golden Mean Process. On the one hand, this implies
   And, finally, one can perform the partial information       that there is a larger amount of synergy than redundancy
decomposition on the mutual information I[X:0 ; X0 , X1: ].    in the Even Process. Indeed, it is often the case, when
The result gives an improved understanding of (i) how          appealing only to the past or the future, that one cannot
much information is uniquely shared with the either the        determine the value of X0 , but when taken together the
immediate or the more distant future and (ii) how much         possibilities are limited to a single symbol. On the other
is redundantly or synergistically with both.                   hand, since qµ is positive for the Golden Mean Process we
   The decompositions provided by the atoms of the pro-        can determine that its behavior is dominated by redun-
cess I-diagram and those provided by the subextensive          dant contributions. That wµ is larger for the Even Pro-
rates of block-information curves are conceptually quite       cess than the Golden Mean Process is consonant with the
different. It has been shown [17] that the subextensive        impression that the former is, overall, more structured.
part of the block entropy and the mutual information be-          The next value in the table is σµ , the amount of state
tween the past and the future, though equal for one di-        information not contained in the current observable. This
                                                                                                                               13

                      1                             1
                                                                                                   Even Golden Mean NRPS
                      2 |0                          2 |1                 H[1]                   0.91830      0.91830 0.97987
                                                                         hµ                     0.66667      0.66667 0.50000
                                                                         ρµ                     0.25163      0.25163 0.47987
                                                                         rµ                     0.00000      0.45915 0.16667
                      A                             A                    bµ                     0.66667      0.20752 0.33333
                                                                         qµ                    -0.41504      0.04411 0.14654
                             1                             1             wµ                     0.91830      0.45915 0.81320
               1|1           2 |1          1|1             2 |0          σµ                     0.66667      0.00000 1.09407
                                                                         Π{X:0 }{X1: }          0.25163      0.25163 0.45550
                                                                         ι : Π{X:0 } , Π{X1: } 0.00000       0.00000 0.02437
                       B                            B                    Π{X:0 ,X1: }           0.66667      0.20752 0.30896
              (a)Even Process              (b)Golden Mean             TABLE I. Information measure analysis of three processes.
                                               Process

                                    1                                                        Even Golden Mean NRPS
                                    2 |0
                                                                            E             0.91830      0.25163 1.57393
                                                                            bµ            0.66667      0.20752 0.33333
                                                                            qµ           -0.41504      0.04411 0.14654
                     1
                     2 |1
                                    A                1|0                    σµ            0.66667      0.00000 1.09407
                                                                            ER            4.48470      0.41504 1.55445
                                                                            EB           -3.56640     -0.16341 0.01948
                                                                            EQ            2.64810     -0.08822 -1.59342
                 B                                         E                EW           -4.48470     -0.41504 -1.55445
                                             1
                                             2 |0                           Π{X0 }{X1: } 0.25163       0.04411 0.47987
                                                                            Π{X0 }        0.00000      0.20752 0.00000
              1|0                                           1               Π{X1: }       0.00000      0.00000 0.76073
                                                            2 |1
                                                                            Π{X0 ,X1: } 0.66667        0.00000 0.33333
                        C                        D
                                                                      TABLE II. Alternative decompositions of excess entropy E
                                    1|1                               for the three prototype processes.
              (c)Noisy Random Phase-Slip Process


FIG. 11. -Machine presentations for the three example pro-           decompositions into ER + EB and −EB − EQ vary from
cesses.                                                               one another significantly. The Even Process has much
                                                                      larger values for these pieces than the total E, whereas
                                                                      the NRPS process has two values nearly equal to E and
vanishes for the Golden Mean Process, as it is order-1                one very small. The Golden Mean Process falls some-
Markovian. The Even Process, however, has a significant               where between these two.
amount of information stored that is not observable in                   The final excess entropy breakdown is provided by
the present.                                                          the partial information decomposition of I[X:0 ; X0 , X1: ].
   Last in the table is a partial information decomposition           Here, we again see differing properties among the three
of I[X0 ; X:0 , X1: ]. qµ is given by Π{X:0 }{X1: } −Π{X:0 ,X1: } .   processes. The Even Process consists only of redundancy
Of note here is that the NRPS process’s nonzero uniquity              Π{X:0 }{X1: } and synergy Π{X:0 ,X1: } . The Golden Mean
ι = 0.02437. For the Even and Golden Mean Processes                   Process contains no synergy, a small amount of redun-
it vanishes. That is, in the NRPS Process information is              dancy, and most of its information sharing is with the
uniquely communicated to the present from the past and                present uniquely. The NRPS Process possesses both syn-
an equivalent in magnitude, but different, information is             ergy and redundancy, but also a significant amount of
communicated to the future. Thus, the NRPS Process                    information shared solely with the more distant future.
illustrates a subtle asymmetry in statistical structure.                 And, finally, Fig. 12 plots how hµ partitions into rµ and
   Table II then provides an alternate breakdown of E for             bµ for the Golden Mean family of processes. This family
each prototype process. We use this here to only high-                consists of all processes with -machine structure given
light how much the processes differ in character from one             in Fig. 11(b), but where the outgoing transition proba-
another. The consequences of the first decomposition of               bilities from state A are parametrized. We can easily see
excess entropy—E = bµ + qµ + σµ —follow directly from                 that for small self-loop transition probabilities, the ma-
the previous table’s discussion. The second and third                 jority of hµ is consumed by bµ . This should be intuitive
                                                                                                                                                   14

                             0.7                                                          constructing a state-based model, is ultimately limited.
                                                                                             Next, we discussed how the different methods and mea-
Entropy rate [bits/symbol]

                             0.6
                                                                                          sures relate to one of the most widely used complexity
                             0.5                                                          measures—the past-future mutual information or excess
                             0.4
                                                                     rµ                   entropy. In particular, we showed how they yield four
                                                                                          distinct decompositions and, in some cases, give useful
                             0.3
                                                                                          interpretations of what these decompositions mean oper-
                             0.2                                                          ationally.
                             0.1
                                                    bµ                                       Then, we calculated all the measures for three different
                                                                                          prototype processes, each highlighting particular features
                             0.0                                                          of the information-theoretic decompositions. We gave in-
                                0.0           0.2        0.4       0.6        0.8   1.0
                                                    Self loop probability p               terpretations of negative mutual informations, as seen in
                                                                                          qµ . The interpretations were consistent, understandable,
FIG. 12. The breakdown of hµ for the Golden Mean Process.                                 and insightful. There was nothing untoward about neg-
The self-loop probability was varied from 0 to 1, adjusting the                           ative informations.
other edge’s probability accordingly.
                                                                                             By adapting it to the time series setting, we high-
                                                                                          lighted a key weakness of the total correlation (or multi-
since, when the self-loop probability is small, the process                               information). This undoubtedly explains the lack of in-
is nearly periodic and rµ should be nearly zero. On the                                   terest in using it in the time series setting, though the
other end of the spectrum, when the self-loop probabil-                                   weakness still holds when it is used to analyze any group
ity is large, hµ is mostly consumed by rµ . This is again                                 of random variables. The weakness has led to persis-
intuitive since observations from that process are domi-                                  tent over-interpretations of what it describes. It also may
nated by 1s and the occasional 0—which provides all the                                   have eclipsed the importance of its more complete analog,
entropy for hµ —has no effect on structure.                                               such as the block entropy, in the settings of networked
                                                                                          random variables.
                                                                                             In closing, we take a longer view. There is an expo-
                                      VIII.    CONCLUDING REMARKS                         nential number of possible atoms for N -way information
                                                                                          measures. In addition, there is a similarly large number
   We began by outlining a conceptual decomposition of                                    possible partial information decompositions for N vari-
a single observation in a time series: a single observation                               ables. This diversity presents the possibility of a large
contains a hierarchy of informational components. We                                      number of independent efforts to define and uniquely mo-
then made the decomposition concrete using a variety                                      tivate why one or the other information measure is the
of multivariate information measures. Adapting them                                       best. Indeed, many of these yet-to-be-explored measures
to time series, we showed that their asymptotic growth                                    may be useful. In this light, there is a bright future for
rates are identified with the hierarchical decomposition.                                 developing information measures adapted to a wide range
To unify the various competing views, we provided the                                     of nonlinear, complex systems. And, helpfully, a unifying
measurement-centric process I-diagram, demonstrating                                      framework appears to be emerging.
that it concisely reveals the semantic meaning behind
each component in the hierarchy.
   Once the measurement-centric process I-diagram was                                                    ACKNOWLEDGMENTS
available, we isolated two components, analyzing in de-
tail their meaning. We utilized the partial information                                      We thank John Mahoney, Nick Travers, and Jörg Re-
lattice [14] to refine our understanding of when the past                                 ichardt for many helpful discussions and feedback. This
and the future redundantly and synergistically inform the                                 work was partially supported by the Defense Advanced
present. This allowed us to explain a subtle statistical                                  Research Projects Agency (DARPA) Physical Intelli-
asymmetry—the directionality in the difference between                                    gence Subcontract No. 9060-000709. The views, opin-
ρµ and Π{X:0 }{X1: } .                                                                    ions, and findings contained in this article are those of
   The other atom we singled out in the process I-diagram                                 the authors and should not be interpreted as representing
was σµ . It is the most compelling evidence that ana-                                     the official views or policies, either expressed or implied,
lyzing a process from its measurements alone, without                                     of the DARPA or the Department of Defense.
                                                                                                                           15


[1] Thomas M. Cover and Joy A. Thomas. Elements of In-          [10] Ionas Erb and Nihat Ay. Multi-Information in the
    formation Theory. Wiley-Interscience, New York, second           Thermodynamic Limit. Journal of Statistical Physics,
    edition, 2006.                                                   115(3/4):949–976, May 2004.
[2] James P. Crutchfield, Christopher J. Ellison, Ryan G.       [11] Samer A. Abdallah and Mark D. Plumbley. Predictive
    James, and John R. Mahoney. Synchronization and                  Information, Multi-Information, and Binding Informa-
    Control in Intrinsic and Designed Computation: An                tion. Technical Report C4DM-TR10-10, Centre for Dig-
    Information-Theoretic Analysis of Competing Models of            ital Music, Queen Mary University of London, 2010.
    Stochastic Computation. Chaos: An Interdisciplinary         [12] Raymond W. Yeung. A New Outlook on Shannon’s In-
    Journal of Nonlinear Science, 20(3):037105, July 2010.           formation Measures. IEEE Transactions on Information
[3] Anthony J. Bell. The co-information lattice. In S. Amari,        Theory, 37(3):466–474, 1991.
    A. Cichocki, S. Makino, and N. Murata, editors, Proceed-    [13] James P. Crutchfield, Christopher J. Ellison, and John R.
    ings of the Fifth International Workshop on Independent          Mahoney. Times Barbed Arrow: Irreversibility, Cryptic-
    Component Analysis and Blind Signal Separation, vol-             ity, and Stored Information. Physical Review Letters,
    ume ICA 2003, New York, 2003. Springer.                          103(9):094101, 2009.
[4] Satosi Watanabe. Information Theoretical Analysis of        [14] Paul L. Williams and Randall D. Beer.               Non-
    Multivariate Correlation. IBM Journal of Research and            negative Decomposition of Multivariate Information.
    Development, 4(1):66–82, January 1960.                           arXiv:1004.2515, April 2010.
[5] Samer A. Abdallah and Mark D. Plumbley. A Measure of        [15] Christopher J. Ellison, John R. Mahoney, and James P.
    Statistical Complexity Based on Predictive Information.          Crutchfield. Prediction, Retrodiction, and The Amount
    arXiv:1012.1890v1, 2010.                                         of Information Stored in the Present. Journal of Statis-
[6] James P. Crutchfield and David P. Feldman. Regular-              tical Physics, 136(6):1005–1034, 2009.
    ities Unseen, Randomness Observed: Levels of Entropy        [16] Robin C. Ball, Marina Diakonova, and Robert S.
    Convergence. Chaos, 13(1):25–54, 2003.                           MacKay. Quantifying Emergence in Terms of Persis-
[7] James P. Crutchfield and N. H. Packard. Symbolic Dy-             tent Mutual Information. Advances in Complex Systems,
    namics of Noisy Chaos. Physica, 7D:201–223, 1983.                13(3):327–338, 2010.
[8] Karl-Erik Eriksson and Kristian Lindgren. Structural        [17] David P. Feldman and James P. Crutchfield. Struc-
    Information in Self-Organizing Systems. Physica Scripta,         tural Information in Two-Dimensional Patterns: Entropy
    35(3):388–397, March 1987.                                       Convergence and Excess Entropy. Physical Review E,
[9] Nihat Ay, Eckehard Olbrich, Nils Bertschinger, and Ju-           67(5):051103, 2003.
    rgen Jost. A Unifying Framework for Complexity Mea-         [18] Cosma Rohilla Shalizi and James P. Crutchfield. Com-
    sures of Finite Systems. Proceedings of ECCS, 2006.              putational Mechanics: Pattern and Prediction, Structure
                                                                     and Simplicity. Journal of Statistical Physics, 104:817–
                                                                     879, 2001.
