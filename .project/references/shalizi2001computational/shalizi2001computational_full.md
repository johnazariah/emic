# arXiv:cond-mat/9907176v2  [cond-mat.stat-mech]  19 Jun 2000

**Source:** shalizi2001computational
**Author:** Unknown
**Pages:** 29

---

## Full Text

                                                                                                 Computational Mechanics:
                                                                                       Pattern and Prediction, Structure and Simplicity

                                                                                                 Cosma Rohilla Shalizi∗ and James P. Crutchfield
                                                                                           Santa Fe Institute, 1399 Hyde Park Road, Santa Fe, NM 87501
arXiv:cond-mat/9907176v2 [cond-mat.stat-mech] 19 Jun 2000


                                                                                                  Electronic addresses: {shalizi,chaos}@santafe.edu
                                                                                                                 (November 26, 2024)


                                                                                                                                           Capturing a Pattern Defined . . . . . .      8
                                                                Computational mechanics, an approach to structural com-                E   The Lessons of History . . . . . . . . .     8
                                                            plexity, defines a process’s causal states and gives a pro-                    Old Country Lemma . . . . . . . . . .        8
                                                            cedure for finding them. We show that the causal-state
                                                                                                                                       F   Minimality and Prediction . . . . . . .      8
                                                            representation—an ǫ-machine—is the minimal one consistent
                                                                                                                                           Complexity of State Classes . . . . . .      8
                                                            with accurate prediction. We establish several results on ǫ-
                                                            machine optimality and uniqueness and on how ǫ-machines
                                                                                                                                 IV    Computational Mechanics                          9
                                                            compare to alternative representations. Further results relate
                                                                                                                                       A Causal States . . . . . . . . . . . . . .      9
                                                            measures of randomness and structural complexity obtained
                                                                                                                                          Causal States of a Process Defined . . .      9
                                                            from ǫ-machines to those from ergodic and information theo-
                                                            ries.                                                                         1 Morphs . . . . . . . . . . . . . . . .     10
                                                                                                                                             Independence of Past and Future
                                                                     Santa Fe Institute Working Paper 99-07-044                              Conditional on a Causal State . . .       10
                                                                    Keywords: complexity, computation, entropy,                           2 Homogeneity . . . . . . . . . . . . .      10
                                                                     information, pattern, statistical mechanics.                            Strict Homogeneity . . . . . . . . .      10
                                                                      Running Head: Computational Mechanics                                  Weak Homogeneity . . . . . . . . .        10
                                                                                                                                             Strict Homogeneity of Causal States       10
                                                                                                                                       B Causal State-to-State Transitions . . .       11
                                                            02.50.Wp, 05.45, 05.65+b, 89.70.+c                                            Causal Transitions . . . . . . . . . . . .   11
                                                                                                                                          Transition Probabilities . . . . . . . . .   11
                                                                                                                                       C ǫ-Machines . . . . . . . . . . . . . . . .    11
                                                                                     Contents                                             An ǫ-Machine Defined . . . . . . . . . .     11
                                                                                                                                          ǫ-Machines Are Monoids . . . . . . . .       11
                                                            I       Introduction                                        2                 ǫ-Machines Are Deterministic . . . . .       11
                                                                                                                                          Causal States Are Independent . . . . .      12
                                                            II      Patterns                                            3                 ǫ-Machine Reconstruction . . . . . . . .     13
                                                                    A Algebraic Patterns . . . . . . . . . . . .        3
                                                                    B Turing Mechanics: Patterns and Effec-                      V     Optimalities and Uniqueness                     13
                                                                        tive Procedures . . . . . . . . . . . . .       4                 Causal States Are Maximally Prescient        13
                                                                    C Patterns with Error . . . . . . . . . . .         5                 Causal States Are Sufficient Statistics .    13
                                                                    D Randomness: The Anti-Pattern? . . . .             5                 Prescient Rivals Defined . . . . . . . .     14
                                                                    E Causation . . . . . . . . . . . . . . . .         5                 Refinement Lemma . . . . . . . . . . .       14
                                                                    F Synopsis of Pattern . . . . . . . . . . .         5                 Causal States Are Minimal . . . . . . .      15
                                                                                                                                          Statistical Complexity of a Process . .      15
                                                            III     Paddling around Occam’s Pool                        6                 Causal States Are Unique . . . . . . . .     15
                                                                    A Hidden Processes . . . . . . . . . . . .          6                 ǫ-Machines Are Minimally Stochastic .        15
                                                                       Processes Defined . . . . . . . . . . . .        6
                                                                       Stationarity . . . . . . . . . . . . . . .       6        VI    Bounds                                          16
                                                                    B The Pool . . . . . . . . . . . . . . . . .        6                 Excess Entropy . . . . . . . . . . . . .     16
                                                                    C A Little Information Theory . . . . . .           7                 The Bounds of Excess . . . . . . . . . .     16
                                                                       1 Entropy Defined . . . . . . . . . . .          7                 Conditioning Does Not Affect Entropy
                                                                       2 Joint and Conditional Entropies . .            7                 Rate . . . . . . . . . . . . . . . . . . .   17
                                                                       3 Mutual Information . . . . . . . . .           7                 Control Theorem . . . . . . . . . . . .      17
                                                                    D Patterns in Ensembles . . . . . . . . . .         7
                                                                                                                                 VII   Concluding Remarks                              18
                                                                                                                                       A Discussion . . . . . . . . . . . . . . . .    18
                                                                                                                                       B Limitations of the Current Results . . .      18
                                                                                                                                       C Conclusions and Directions for Future
                                                             Permanent address: Physics Department, University of
                                                                ∗
                                                                                                                                          Work . . . . . . . . . . . . . . . . . . .   19
                                                            Wisconsin, Madison, WI 53706


                                                                                                                             1
APPENDIXES                                              20           Computational mechanics [5] is an approach that lets
                                                                  us directly address the issues of pattern, structure, and
A      Information-Theoretic Formulæ                    20        organization. While keeping concepts and mathemati-
                                                                  cal tools already familiar from statistical mechanics, it
B      The Equivalence Relation that Induces                      is distinct from the latter and complementary to it. In
       Causal States                         20                   essence, from either empirical data or from a probabilistic
                                                                  description of behavior, it shows how to infer a model of
C      Time Reversal                                    21        the hidden process that generated the observed behav-
                                                                  ior. This representation—the ǫ-machine—captures the
D      ǫ-Machines are Monoids                           21
                                                                  patterns and regularities in the observations in a way
E      Alternate     Proof    of   the   Refinement               that reflects the causal structure of the process. Use-
       Lemma                                            21        fully, with this model in hand, one can extrapolate be-
                                                                  yond the original observational data to make predictions
F      Finite Entropy for the Semi-Infinite Fu-                   of future behavior. Moreover, in a well defined sense
       ture                                       22              that is the subject of the following, the ǫ-machine is the
           The Finite-Control Theorem . . . . . . 22              unique maximally efficient model of the observed data-
                                                                  generating process.
G      Relations to Other Fields                        22           ǫ-Machines themselves reveal, in a very direct way,
       1 Time Series Modeling . . . . . . . . . .       22        how information is stored in the process, and how that
       2 Decision-Theoretic Problems . . . . . .        22        stored information is transformed by new inputs and by
       3 Stochastic Processes . . . . . . . . . . .     23        the passage of time. This, and not using computers for
       4 Formal Language Theory and Gram-                         simulations and numerical calculations, is what makes
           matical Inference . . . . . . . . . . . .    23        computational mechanics “computational”, in the sense
       5 Computational and Statistical Learn-                     of “computation theoretic”.
           ing Theory . . . . . . . . . . . . . . . .   23           The basic ideas of computational mechanics were intro-
       6 Description-Length Principles and Uni-                   duced a decade ago [6]. Since then they have been used
           versal Coding Theory . . . . . . . . . .     24        to analyze dynamical systems [7,8], cellular automata
       7 Measure Complexity . . . . . . . . . .         24        [9], hidden Markov models [10], evolved spatial compu-
       8 Hierarchical Scaling Complexity . . . .        24        tation [11], stochastic resonance [12], globally coupled
       9 Continuous Dynamical Computing . . .           25        maps [13], and the dripping faucet experiment [14]. De-
                                                                  spite this record of successful application, there has been
References                                              25        some uncertainty about the mathematical foundations of
                                                                  the subject. In particular, while it seemed evident from
Glossary of Notation                                    29        construction that an ǫ-machine captured the patterns in-
                                                                  herent in a process and did so in a minimal way, no ex-
                                                                  plicit proof of this was published. Moreover, there was
                 I. INTRODUCTION                                  no proof that, if the ǫ-machine was optimal in this way,
                                                                  it was the unique optimal representation of a process.
   Organized matter is ubiquitous in the natural world,           These little-needed gaps have now been filled. Subject
but the branch of physics which ought to handle it—               to some (reasonable) restrictions on the statistical char-
statistical mechanics—lacks a coherent, principled way of         acter of a process, we prove that the ǫ-machine is indeed
describing, quantifying, and detecting the many different         the unique optimal causal model. The rigorous proof of
kinds of structure nature exhibits. Statistical mechan-           these results is the main burden of this paper. We gave
ics has good measures of disorder in thermodynamic en-            preliminary versions of the optimality results—but not
tropy and in related quantities, such as the free energies.       the uniqueness theorem, which is new here—in Ref. [15].
When augmented with theories of critical phenomena [1]               The outline of the exposition is as follows. We be-
and pattern formation [2], it also has an extremely suc-          gin by showing how computational mechanics relates to
cessful approach to analyzing patterns formed through             other approaches to pattern, randomness, and causality.
symmetry breaking, both in equilibrium [3] and, more              The upshot of this is to focus our attention on patterns
recently, outside it [4]. Unfortunately, these successes          within a statistical ensemble and their possible represen-
involve many ad hoc procedures—such as guessing rele-             tations. Using ideas from information theory, we state a
vant order parameters, identifying small parameters for           quantitative version of Occam’s Razor for such represen-
perturbation expansion, and choosing appropriate func-            tations. At that point we define causal states [6], equiva-
tion bases for spatial decomposition. It is far from clear        lence classes of behaviors, and the structure of transitions
that the present methods can be extended to handle all            between causal states—the ǫ-machine. We then show
the many kinds of organization encountered in nature,             that the causal states are ideal from the point of view of
especially those produced by biological processes.                Occam’s Razor, being the simplest way of attaining the
                                                                  maximum possible predictive power. Moreover, we show

                                                              2
that the causal states are uniquely optimal. This com-           What makes the Celestial Emporium’s scheme inherently
bination allows us to prove a number of other, related           unsatisfactory, and not just strange, is that it tells us
optimality results about ǫ-machines. We examine the as-          nothing about animals. We want to find patterns in a
sumptions made in deriving these optimality results, and         process that “divide it at the joints, as nature directs,
we note that several of them can be lifted without unduly        not breaking any limbs in half as a bad carver might”
upsetting the theorems. We also establish bounds on a            [18, Sec. 265D].
process’s intrinsic computation as revealed by ǫ-machines           Computational mechanics is not directly concerned
and by quantities in information and ergodic theories.           with pattern formation per se [4]; though we suspect it
Finally, we close by reviewing what has been shown and           will ultimately be useful in that domain. Nor is it con-
what seem like promising directions for further work on          cerned with pattern recognition as a practical matter as
the mathematical foundations of computational mechan-            found in, say, neuropsychology [19], psychophysics [20],
ics.                                                             cognitive ethology [21], computer engineering [22], and
   A series of appendices provide supplemental material          signal and image processing [23,24]. Instead, it is con-
on information theory, equivalence relations and classes,        cerned with the questions of what patterns are and how
ǫ-machines for time-reversed processes, semi-group the-          patterns should be represented. One way to highlight the
ory, and connections and distinctions between computa-           difference is to call this pattern discovery, rather than
tional mechanics and other fields.                               pattern recognition.
   To set the stage for the mathematics to follow and to            The bulk of the intellectual discourse on what patterns
motivate the assumptions used there, we begin now by             are has been philosophical. One distinct subset has been
reviewing prior work on pattern, randomness, and causal-         conducted under the broad rubric of mathematical logic.
ity. We urge the reader interested only in the mathemat-         Within this there are approaches, on the one hand, that
ical development to skip directly to Sec. II F—a synopsis        draw on (highly) abstract algebra and the theory of rela-
of the central assumptions of computational mechanics—           tions; on the other, that approach patterns via the theory
and continue from there.                                         of algorithms and effective procedures.
                                                                    The general idea, in both approaches, is that some ob-
                                                                 ject O has a pattern P—O has a pattern “represented”,
                    II. PATTERNS                                 “described”, “captured”, and so on by P—if and only if
                                                                 we can use P to predict or compress O. Note that the
  To introduce our approach to—and even to argue that            ability to predict implies the ability to compress, but not
some approach is necessary for—discovering and describ-          vice versa; here we stick to prediction. The algebraic and
ing patterns in nature we begin by quoting Jorge Luis            algorithmic strands differ mainly on how P itself should
Borges:                                                          be represented; that is, they differ in how it is expressed
                                                                 in the vocabulary of some formal scheme.
         These ambiguities, redundancies, and de-
                                                                    We should emphasize here that “pattern” in this sense
     ficiencies recall those attributed by Dr. Franz
                                                                 implies a kind of regularity, structure, symmetry, orga-
     Kuhn to a certain Chinese encyclopedia
                                                                 nization, and so on. In contrast, ordinary usage some-
     entitled Celestial Emporium of Benevolent
                                                                 times accepts, for example, speaking about the “pattern”
     Knowledge. On those remote pages it is writ-
                                                                 of pixels in a particular slice of between-channels video
     ten that animals are divided into (a) those
                                                                 “snow”; but we prefer to speak of that as the configura-
     that belong to the Emperor, (b) embalmed
                                                                 tion of pixels.
     ones, (c) those that are trained, (d) suck-
     ling pigs, (e) mermaids, (f) fabulous ones, (g)
     stray dogs, (h) those that are included in this                              A. Algebraic Patterns
     classification, (i) those that tremble as if they
     were mad, (j) innumerable ones, (k) those
     drawn with a very fine camel’s hair brush,                     Although the problem of pattern discovery appears
     (l) others, (m) those that have just broken a               early, in Plato’s Meno [25] for example, perhaps the first
     flower vase, (n) those that resemble flies from             attempt to make the notion of “pattern” mathematically
     a distance.                                                 rigorous was that of Whitehead and Russell in Principia
                                                                 Mathematica. They viewed pattern as a property, not
     —J. L. Borges, “The Analytical Language of                  of sets, but of relations within or between sets, and ac-
     John Wilkins”, in Ref. [16, p. 103]; see also               cordingly they work out an elaborate relation-arithmetic
     discussion in Ref. [17].                                    [26, vol. II, part IV]; cf. [27, ch. 5–6]. This starts by
                                                                 defining the relation-number of a relation between two
  The passage illustrates the profound gulf between pat-         sets as the class of all the relations that are equivalent
terns, and classifications derived from patterns, that are       to it under one-to-one, onto mappings of the two sets.
appropriate to the world and help us to understand it            In this framework relations share a common pattern or
and those patterns which, while perhaps just as legit-           structure if they have the same relation-number. For
imate as prosaic regularities, are not at all informative.

                                                             3
instance, all square lattices have similar structure since         representational scheme. Since we can convert from one
their elements share the same neighborhood relation; as            such device to another—say, from a Post tag system [39]
do all hexagonal lattices. Hexagonal and square lattices,          to a Turing machine—with only a finite description of the
however, exhibit different patterns since they have non-           first system, such constants are easily assimilated when
isomorphic neighborhood relations—i.e., since they have            measuring complexity in this approach.
different relation-numbers. (See also recoding equivalence            In particular, consider the first n symbols On of O and
defined in Ref. [28].) Less work has been done on this             the shortest program Pn that produces them. We ask,
than they—especially Russell [29]—had hoped. This may              What happens to the limit
be due in part to a general lack of familiarity with Volume
                                                                                                |Pn |
II of Ref. [26].                                                                          lim         ,                     (1)
   A more recent attempt at developing an algebraic ap-                                   n→∞    n
proach to patterns builds on semi-group theory and its             where |P| is the length in bits of program P? On the one
Krohn-Rhodes decomposition theorem. Ref. [30] dis-                 hand, if there is a fixed-length program P that generates
cusses a range of applications of this approach to pat-            arbitrarily many digits of O, then this limit vanishes.
terns. Along these lines, Rhodes and Nehaniv have tried            Most of our interesting
                                                                                 √           numbers, rational or irrational—
to apply semi-group complexity theory to biological evo-           such as π, e, 2—are of this sort. These numbers are em-
lution [31]. They suggest that the complexity of a bi-             inently compressible: the program P is the compressed
ological structure can be measured by the number of                description, and so it captures the pattern obeyed by the
subgroups in the decomposition of an automaton that                sequence describing O. If the limit goes to 1, on the other
describes the structure.                                           hand, we have a completely incompressible description
   Yet another algebraic approach has been developed by            and conclude, following Kolmogorov, Chaitin, and oth-
Grenander and co-workers, primarily for pattern recogni-           ers, that O is random [35–38,40,41]. This conclusion is
tion [32]. Essentially, this is a matter of trying to invent       the desired one: the Kolmogorov-Chaitin framework es-
a minimal set of generators and bonds for the pattern              tablishes, formally at least, the randomness of an individ-
in question. Generators can adjoin each other, in a suit-          ual object without appeals to probabilistic descriptions
able n-dimensional space, only if their bonds are compat-          or to ensembles of reproducible events. And it does so by
ible. Each pair of compatible bonds at once specifies a            referring to a deterministic, algorithmic representation—
binary algebraic operation and an observable element of            the UTM.
the configuration built out of the generators. (Our con-              There are many well-known difficulties with applying
struction in App. D, linking an algebraic operation with           Kolmogorov complexity to natural processes. First, as
concatenations of strings, is analogous in a rough way.)           a quantity, it is uncomputable in general, owing to the
Probabilities can be attached to these bonds, leading in a         halting problem [38]. Second, it is maximal for random
natural way to a (Gibbsian) probability distribution over          sequences; this can be construed either as desirable, as
entire configurations. Grenander and his colleagues have           just noted, or as a failure to capture structure, depending
used these methods to characterize, inter alia, several            on one’s aims. Third, it only applies to a single sequence;
biological phenomena [33,34].                                      again this is either good or bad. Fourth, it makes no al-
                                                                   lowance for noise or error, demanding exact reproduction.
                                                                   Finally, limn→∞ |Pn |/n can vanish, although the compu-
    B. Turing Mechanics: Patterns and Effective                    tational resources needed to run the program, such as
                   Procedures                                      time and storage, grow without bound.
                                                                      None of these impediments have kept researchers from
   The other path to patterns follows the traditional ex-          attempting to use Kolmogorov-Chaitin complexity for
ploration of the logical foundations of mathematics, as ar-        practical tasks—such as measuring the complexity of nat-
ticulated by Frege and Hilbert and pioneered by Church,            ural objects (e.g. Ref. [42]), as a basis for theories of
Gödel, Post, Russell, Turing, and Whitehead. A more               inductive inference [43,44], and generally as a means of
recent and relatively more popular approach goes back              capturing patterns [45]. As Rissanen [46, p. 49] says,
to Kolmogorov and Chaitin, who were interested in the              this is akin to “learn[ing] the properties [of a data set] by
exact reproduction of an individual object [35–38]; in par-        writing programs in the hope of finding short ones!”
ticular, their focus was discrete symbol systems, rather              Various of the difficulties just listed have been ad-
than (say) real numbers or other mathematical objects.             dressed by subsequent work. Bennett’s logical depth ac-
The candidates for expressing the pattern P were univer-           counts for time resources [47]. (In fact, it is the time
sal Turing machine (UTM) programs—specifically, the                for the minimal-length program P to produce O.) Kop-
shortest UTM program that can exactly produce the ob-              pel’s sophistication attempts to separate out the “reg-
ject O. This program’s length is called O’s Kolmogorov-            ularity” portion of the program from the random or
Chaitin complexity. Note that any scheme—automaton,                instance-specific input data [48,49]. Ultimately, these ex-
grammar, or what-not—that is Turing equivalent and for             tensions and generalizations remain in the UTM, exact-
which a notion of “length” is well defined will do as a            reproduction setting and so inherit inherent uncom-
                                                                   putability.

                                                               4
                C. Patterns with Error                             ness and, as we have just seen, this is useful for some
                                                                   purposes. As these purposes are not those of analyzing
   Motivated by these theoretical difficulties and practi-         patterns in processes and in real-world data, however,
cal concerns, an obvious next step is to allow our pattern         they are not ours. Randomness simply does not corre-
P some degree of approximation or error, in exchange               spond to a notion of pattern or structure at all and, by
for shorter descriptions. As a result, we lose perfect re-         implication, neither Kolmogorov-Chaitin complexity nor
production of the original configuration from the pattern.         any of its spawn measure pattern.
Given the ubiquity of noise in nature, this is a small price          Nonetheless, some approaches to complexity conflate
to pay. We might also say that sometimes we are willing            “structure” with the opposite of randomness, as conven-
to accept small deviations from a regularity, without re-          tionally understood and measured in physics by thermo-
ally caring what the precise deviation is. As pointed out          dynamic entropy or a related quantity, such as Shannon
in Ref. [17]’s conclusion, this is certainly a prime motiva-       entropy. In effect, structure is defined as “one minus dis-
tion in thermodynamic descriptions, in which we explic-            order”. In contrast, we see pattern—structure, organi-
itly throw away, and have no interest in, vast amounts of          zation, regularity, and so on—as describing a coordinate
microscopic detail in order to find a workable description         “orthogonal” to a process’s degree of randomness. That
of macroscopic observations.                                       is, complexity (in our sense) and randomness each cap-
   Some interesting philosophical work on patterns-with-           ture a useful property necessary to describe how a process
error has been done by Dennett, with reference not just            manipulates information. This complementarity is even
to questions about the nature of patterns and their emer-          codified by the complexity-entropy diagrams introduced
gence but also to psychology [50]. The intuition is that           in Ref. [6]. It should be clear now that when we use the
truly random processes can be modeled very simply—“to              word “complexity” we mean “degrees” of pattern, not
model coin-tossing, toss a coin.” Any prediction scheme            degrees of randomness.
that is more accurate than assuming complete indepen-
dence ipso facto captures a pattern in the data. There
is thus a spectrum of potential pattern-capturers ranging                                E. Causation
from the assumption of pure noise to the exact reproduc-
tion of the data, if that is possible. Dennett notes that             We want our representations of patterns in dynamical
there is generally a trade-off between the simplicity of           processes to be causal—to say how one state of affairs
a predictor and its accuracy, and he plausibly describes           leads to or produces another. Although a key property,
emergent phenomena [51,52] as patterns that allow for              causality enters our development only in an extremely
a large reduction in complexity for only a small reduc-            weak sense, the weakest one can use mathematically,
tion in accuracy. Of course, Dennett was by no means               which is Hume’s [56]: one class of event causes another
the first to consider predictive schemes that tolerate error       if the latter always follows the former; the effect invari-
and noise; we discuss some of the earlier work in App. G.          ably succeeds the cause. As good indeterminists, in the
However, to our knowledge, he was the first to have made           following we replace this invariant-succession notion of
such predictors a central part of an explicit account of           causality with a more probabilistic one, substituting a
what patterns are. It must be noted that this account              homogeneous distribution of successors for the solitary
lacks the mathematical detail of the other approaches we           invariable successor. (A precise statement appears in
have considered so far, and that it relies on the inexact          Sec. IV A’s definition of causal states.) This approach
prediction of a single configuration. In fact, it relies on        results in a purely phenomenological statement of causal-
exact predictors that are “fuzzed up” by noise. The in-            ity, and so it is amenable to experimentation in ways that
troduction of noise, however, brings in probabilities, and         stronger notions of causality—e.g., that of Ref. [57]—are
their natural setting is in ensembles. It is in that setting       not. Ref. [58] independently reaches a concept of causal-
that the ideas we share with Dennett can receive a proper          ity essentially the same ours via philosophical arguments.
quantitative treatment.
                                                                                   F. Synopsis of Pattern
         D. Randomness: The Anti-Pattern?
                                                                     In line with these observations, the ideal, synthesizing
   We should at this point say a bit about the relations           approach to patterns would be at once:
between randomness, complexity, and structure, at least               1. Algebraic, giving us an explicit breakdown or de-
as we use those words. Ignoring some foundational issues,                composition of the pattern into its parts;
randomness is actually rather well understood and well
handled by classical tools introduced by Boltzmann [53];              2. Computational, showing how the process stores and
Fisher, Neyman, and Pearson [54]; Kolmogorov [35]; and                   uses information;
Shannon [55], among others. One tradition in the study
of complexity in fact identifies complexity with random-              3. Calculable, analytically or by systematic approxi-
                                                                         mation;

                                                               5
                                                                           ←
   4. Causal, telling us how instances of the pattern are             and S t are the semi-infinite sequences starting from and
      actually produced; and                                                                           →       ←
                                                                      stopping at t and taking values s and s , respectively.
   5. Naturally stochastic, not merely tolerant of noise                 Intuitively, we can imagine starting with distributions
      but explicitly formulated in terms of ensembles.                for finite-length sequences and extending them gradu-
                                                                      ally in both directions, until the infinite sequence is
This mix is precisely the brew we claim, in all modesty,              reached as a limit. While this can be a useful picture
to have on tap.                                                       to have in mind, defining a process in this way raises
                                                                      some subtle measure-theoretic issues, such as how finite-
                                                                      dimensional distributions limit on an infinite-dimensional
        III. PATTERNS IN ENSEMBLES:                                   one [60, ch. 7]. To avoid these we start with the infinite-
      PADDLING AROUND OCCAM’S POOL                                    dimensional distribution.

                                                                      Definition 2 (Stationarity) A process Si is stationary
  Here a pattern P is something knowledge of which lets               if and only if
us predict, at better than chance rates, if possible, the
future of sequences drawn from an ensemble O: P has                                    →L               →L
to be statistically accurate and confer some leverage or                            P( S t = sL ) = P( S 0 = sL ) ,               (3)
advantage as well. Let’s fix some notation and state the              for all t ∈ Z, L ∈ Z+ , and all sL ∈ AL .
assumptions that will later let us prove the basic results.
                                                                      In other words, a stationary process is one that is
                                                                                                                         →   →
                                                                      time-translation invariant. Consequently, P( S t = s ) =
                   A. Hidden Processes                                   →    →          ←      ←       ←      ←
                                                                      P( S 0 = s ) and P( S t = s ) = P( S 0 = s ), and so we drop
   We restrict ourselves to discrete-valued, discrete-time            the subscripts from now on.
stationary stochastic processes. (See Sec. VII B for dis-
cussion of these assumptions.) Intuitively, such processes
                                                                                              B. The Pool
are sequences of random variables Si , the values of which
are drawn from a countable set A. We let i range over                                                            →
all the integers, and so get a bi-infinite sequence                      Our goal is to predict all or part of S using some func-
                                                                                            ←                                ←
                  ↔
                                                                      tion of some part of S . We begin by taking the set S of
                  S = . . . S−1 S0 S1 . . . .              (2)        all pasts and partitioning it into mutually exclusive and
                                                                      jointly comprehensive subsets. That is, we make a class
In fact, we define a process in terms of the distribution             R of subsets of pasts.1 (See Fig. 1 for a schematic ex-
of such sequences; cf. Ref. [59].                                     ample.) Each ρ ∈ R will be called a state or an effective
                                                                                                         ←
                                                                      state. When the current history s is included in the set
Definition 1 (A Process) Let A be a countable set.                    ρ, we will speak of the process being in state ρ. Thus, we
Let Ω = AZ be the set of bi-infinite sequences composed               define a function from histories to effective states:
from A, Ti : Ω 7→ A be the function that returns the
                                                                                                ←
ith element si of a bi-infinite sequence ω ∈ Ω, and F the                                    η : S 7→ R .                         (4)
field of cylinder sets of Ω. Adding a probability measure P
gives us a probability space (Ω, F , P), with an associated                                            ←     ←
                   ↔                                                  A specific individual history s ∈ S maps to a specific
                                                                                                          ←
random variable S . A process is a sequence of random                 state ρ ∈ R; the random variable S for the past maps to
                   ↔
variables Si = Ti ( S ), i ∈ Z.                                       the random variable R for the effective states. It makes
                                                                      little difference whether we think of η as being a function
Here, and throughout, we follow the convention of using               from a history to a subset of histories or a function from
capital letters to denote random variables and lower-case             a history to the label of that subset. Each interpretation
letters their particular values.                                      is convenient at different times, and we will use both.
   It follows from Def. 1 that there are well defined prob-                                                                 ←
                                                                         Note that we could use any function defined on S to
ability distributions for sequences of every finite length.
     →L                                                               partition that set, by assigning to the same ρ all the his-
                                                                              ←
Let S t be the sequence of St , St+1 , . . . , St+L−1 of L ran-       tories s on which the function takes← the same value. Sim-
                                    →0
dom variables beginning at St . S t ≡ λ, the null sequence.           ilarly, any equivalence relation on S partitions it. (See
          ←L
Likewise, S t denotes the sequence of L random variables
                                                ←L   →L
going up to St , but not including it; S t = S t−L . Both
                                                                       1
→L        ←L                                                →            At several points our constructions require referring to sets
St   and S t take values from sL ∈ AL . Similarly, S t                of sets. To help mark the distinction, we call the set of sets
                                                                      of histories a class.


                                                                  6
                                                                                        X
App. B for more on equivalence relations.) Due to the                       H[X] ≡ −         P(X = x) log2 P(X = x) ,          (5)
way we defined a process’s distribution, each effective                                x∈A
state has a well defined distribution of futures, though
not necessarily a unique one.2 Specifying the effective               taking 0 log 0 = 0. Notice that H[X] is the expectation
state thus amounts to making a prediction about the                   value of − log2 P(X = x) and is measured in bits of infor-
process’s future. All the histories belonging to a given ef-          mation. Caveats of the form “when the sum converges
fective state are treated as equivalent for purposes of pre-          to a finite value” are implicit in all statements about the
dicting the future. (In this way, the framework formally              entropies of infinite countable sets A.
incorporates traditional methods of time-series analysis;                Shannon interpreted H[X] as the uncertainty in X.
see App. G 1.)                                                        (Those leery of any subjective component in notions
                                                                      like “uncertainty” may read “effective variability” in its
                                                                      place.) He showed, for example, that H[X] is the mean
                      ←                                               number of yes-or-no questions needed to pick out the
                      S                                               value of X on repeated trials, if the questions are chosen
                                        R4                            to minimize this average [55].


                R1                                                                2. Joint and Conditional Entropies

                                               R3                       We define the joint entropy H[X, Y ] of two variables
                                                                      X (taking values in A) and Y (taking values in B) in the
                           R2                                         obvious way,

                                                                        H [X, Y ] ≡                                     (6)
   FIG. 1. A schematic picture of a partition of the                         X
    ←                                                                   −           P(X = x, Y = y) log2 P(X = x, Y = y) .
set S of all histories into some class of effective states:
                                                                          (x,y)∈A×B
R = {Ri : i = 1, 2, 3, 4}. Note that the Ri need not form
compact sets; we simply draw them that way for clarity. One
should have in mind Cantor sets or other more pathological
                                                                      We define the conditional entropy H[X|Y ] of one random
structures.                                                           variable X with respect to another Y from their joint
                                                                      entropy:
  We call the collection of all partitions R of the set of                        H[X|Y ] ≡ H[X, Y ] − H[Y ] .                 (7)
          ←
histories S Occam’s pool.
                                                                      This also follows naturally from the definition of con-
                                                                      ditional probability, since P(X = x|Y = y) ≡ P(X =
            C. A Little Information Theory                            x, Y = y)/P(Y = y). H[X|Y ] measures the mean uncer-
                                                                      tainty remaining in X once we know Y .
   Since the bulk of the following development will be con-
sumed with notions and results from information theory
[55], we now review several highlights briefly, for the ben-                             3. Mutual Information
efit of readers unfamiliar with the theory and to fix no-
tation. Appendix A lists a number of useful information-                 The mutual information I[X; Y ] between two variables
theoretic formulæ, which get called upon in our proofs.               is defined to be
Throughout, our notation and style of proof follow those
in Ref. [62].                                                                      I[X; Y ] ≡ H[X] − H[X|Y ] .                 (8)

                                                                      This is the average reduction in uncertainty about X
                     1. Entropy Defined                               produced by fixing Y . It is non-negative, like all entropies
                                                                      here, and symmetric in the two variables.
  Given a random variable X taking values in a count-
able set A, the entropy of X is
                                                                                      D. Patterns in Ensembles

                                                                        It will be convenient to have a way of talking about the
 2
   This is not necessarily true if η is sufficiently patholog-        uncertainty of the future. Intuitively, this would just be
                                                                         →
ical. To paraphrase Ref. [61], readers should assume that             H[ S ], but in general that quantity is infinite and awk-
all our functions are sufficiently tame, measure-theoretically,                                                                 →
that whatever induced distributions we invoke will exist.             ward to manipulate. (The special case in which H[ S ]


                                                                  7
is finite is dealt with in App. F.) Normally, we evade               Proof. By construction (Eq. (4)), for all L,
                          →L
this by considering H[ S ], the uncertainty of the next L                          →L           →L    ←
symbols, treated as a function of L. On occasion, we will                       H[ S |R] = H[ S |η( S )] .                 (13)
refer to the entropy per symbol or entropy rate [55,62]:
                                                                   But
                 →           1 →L
                h[ S ] ≡ lim H[ S ] ,                   (9)                        →L    ←         →L ←
                        L→∞ L                                                   H[ S |η( S )] ≥ H[ S | S ] ,               (14)
and the conditional entropy rate,
                                                                   since the entropy conditioned on a variable is never more
             →            1 →L                                     than the entropy conditioned on a function of the variable
           h[ S |X] ≡ lim H[ S |X] ,                   (10)
                     L→∞ L                                         (Eq. (A14)). QED.
                                                                      Remark 1. That is, conditioning on the whole of the
where X is some random variable and the limits exist.
                                                                   past reduces the uncertainty in the future to as small
For stationary stochastic processes, the limits always ex-
ist [62, Theorem 4.2.1, p. 64].                                    a value as possible. Carrying around the whole semi-
                                                                   infinite past is rather bulky and uncomfortable and is a
   These entropy rates are also always bounded above
by H[S]; which is a special case of Eq. (A3). More-                somewhat dismaying prospect. Put a bit differently: we
           →                                                       want to forget as much of the past as possible and so
over, if h[ S ] = H[S], the process consists of inde-              reduce its burden. It is the contrast between this desire
pendent variables—independent, identically distributed             and the result of Eq. (12) that leads us to call this the
(IID) variables, in fact, since we are only concerned with         Old Country Lemma.
stationary processes here.                                            Remark 2. Lemma 1 establishes the promised upper
Definition 3 (Capturing a Pattern) R captures a                    bound on the strength of patterns: viz., the strength
                                                                                                        →L ←
pattern if and only if there exists an L such that                 of the pattern is at most H[S] − H[ S | S ]/Lpast , where
                                                                                                               →L ←
                     →L                                            Lpast is the least value of L such that H[ S | S ] < LH[S].
                 H[ S |R] < LH[S] .                    (11)

This says that R captures a pattern when it tells us                            F. Minimality and Prediction
something about how the distinguishable parts of a pro-
cess affect each other: R exhibits their dependence. (We             Let’s invoke Occam’s Razor: “It is vain to do with
also speak of η, the function associated with pasts, as            more what can be done with less” [63]. To use the razor,
capturing a pattern, since this is implied by R captur-            we need to fix what is to be “done” and what “more” and
ing a pattern.) Supposing that these parts do not affect           “less” mean. The job we want done is accurate predic-
each other, then we have IID random variables, which                                                                  →L
is as close to the intuitive notion of “patternless” as one        tion, i.e., reducing the conditional entropies H[ S |R] as
is likely to state mathematically. Note that, because of           far as possible, the goal being to attain the bound set by
the independence bound on joint entropies (Eq. (A3)), if           Lemma 1. But we want to do this as simply as possible,
the inequality is satisfied for some L, it is also satisfied       with as few resources as possible. On the road to meeting
for every L′ > L. Thus, we can consider the difference             these two constraints—minimal uncertainty and minimal
           →L                                                      resources—we     will need a measure of the second. Since
H[S] − H[ S |R]/L, for the smallest L for which it is                 ←     ←
                                                                   P( S = s ) is well defined, there is an induced measure
nonzero, as the strength of the pattern captured by R.
                                                                   on the η-states; i.e., P(R = ρ), the probability of being
We will now mark an upper bound (Lemma 1) on the
                                                                   in any particular effective state, is well defined. Accord-
strength of patterns; later we will show how to attain
                                                                   ingly, we define the following measure of resources.
this upper bound (Thm. 1).
                                                                   Definition 4 (Complexity of State Classes) The
                                                                   statistical complexity of a class R of states is
                E. The Lessons of History
                                                                          Cµ (R) ≡ H[R]                                    (15)
  We are now in a position to prove a result about pat-                             X
terns in ensembles that will be useful in connection with                        =−     P(R = ρ) log2 P(R = ρ) ,
our later theorems about causal states.                                                 ρ∈R


Lemma 1 (Old Country Lemma) For all R and for                      when the sum converges to a finite value.
all L ∈ Z+ ,
                                                                   The µ in Cµ reminds us that it is a measure-theoretic
                  →L           →L ←                                property and depends ultimately on the distribution over
                H[ S |R] ≥ H[ S | S ] .                (12)
                                                                   the process’s sequences, which induces a measure over
                                                                   states.


                                                               8
   The statistical complexity of a state class is the average            Alternately and equivalently, we could define an equiv-
uncertainty (in bits) in the process’s current state. This,           alence relation ∼ǫ such that two histories are equivalent if
in turn, is the same as the average amount of memory (in              and only if they have the same conditional distribution of
bits) that the process appears to retain about the past,              futures, and then define causal states as the equivalence
given the chosen state class R. (We will later, in Def. 12,           classes generated by ∼ǫ . (In fact, this was the original
see how to define the statistical complexity of a process             approach [6].) Either way, the divisions of this partition
                                                                        ←
itself.) The goal is to do with as little of this memory              of S are made between regions that leave us in different
as possible. Restated then, we want to minimize statis-               conditions of ignorance about the future.
tical complexity, subject to the constraint of maximally                This last statement suggests another, still equivalent,
accurate prediction.                                                  description of ǫ:
   The idea behind calling the collection of all partitions
   ←
                                                                                  ←′   →L     →L ←            →L     →L ←    ←′
of S Occam’s pool should now be clear: One wants to                     ←
                                                                      ǫ( s ) = { s |P( S
                                                                                                       ←
                                                                                            = s | S = s ) = P( S   = s | S= s ) ,
find the shallowest point in the pool. This we now do.
                                                                              →L       →L     ←′   ←
                                                                              s    ∈S ,       s ∈ S , L ∈ Z+ } .              (17)

         IV. COMPUTATIONAL MECHANICS                                  Using this we can make the original definition, Eq. (16),
                                                                      more intuitive by picturing a sequence of partitions of
                                                                                 ←
         Those who are good at archery learnt from                    the space S of all histories in which each new partition,
      the bow and not from Yi the Archer. Those                       induced using L + 1, is a refinement of the previous one
      who know how to manage boats learnt from                        induced using L. At the coarsest level, the first partition
      the boats and not from Wo.                                      (L = 1) groups together those histories that have the
                                                                      same distribution for the very next observable. These
      —Anonymous in Ref. [64].                                        classes are then subdivided using the distribution of the
                                                                      next two observables, then the next three, four, and so
   The ultimate goal of computational mechanics is to                 on. The limit of this sequence of partitions—the point
discern the patterns intrinsic to a process. That is, as              at which every member of each class has the same dis-
much as possible, the goal is to let the process describe             tribution of futures, of whatever length, as every other
itself, on its own terms, without appealing to a priori                                                           ←
                                                                      member of that class—is the partition of S induced by
assumptions about the process’s structure. Here we sim-
                                                                      ∼ǫ . See App. B for a detailed discussion and review of
ply explore the consistency and well-definedness of these
                                                                      the equivalence relation ∼ǫ .
goals. Of course, practical constraints may keep us from
                                                                         Although they will not be of direct concern in the fol-
doing more than approximating these ideals more or less
                                                                      lowing, due to the time-asymptotic limits taken, there are
grossly. Naturally, such problems, which always turn up
                                                                      transient causal states in addition to those (recurrent)
in implementation, are much easier to address if we start
                                                                      causal states defined above in Eq. (16). Roughly speak-
from secure foundations.
                                                                      ing, the transient causal states describe how a length-
                                                                      ening sequence (a history) of observations allows us to
                      A. Causal States
                                                                      identify the recurrent causal states with increasing pre-
                                                                      cision. See the developments in App. B and in Refs. [10]
                                                                      and [65] for more detail on transient causal states.
Definition 5 (A Process’s Causal States) The                             Causal states are a particular kind of effective state,
causal states of a process are the members of the range               and they have all the properties common to effective
                   ←       ←                      ←
of the function ǫ : S 7→ 2 S —the power set of S :                    states (Sec. III B). In particular, each causal state Si
                                                                      has several structures attached:
     ←      ←′    →    → ←     ←        →   →    ←    ←′
   ǫ( s ) ≡ { s |P( S = s | S = s ) = P( S = s | S = s ) ,
                                                                         1. The index i—the state’s “name”.
                                   → → ←′    ←
                          for all s ∈ S , s ∈ S } ,        (16)
                                                                         2. The set of histories that have brought the process
                                                                                                     ←
that maps from histories to sets of histories. We write                     to Si , which we denote { s ∈ Si }.
the ith causal state as Si and the set of all causal states
as S; the corresponding random variable is denoted S,                    3. A conditional distribution over futures, denoted
                                                                               →                         → ← ←
and its realization σ.                                                      P( S |Si ), and equal to P( S | s ), s ∈ Si . Since
                                                                            we refer to this type of distribution frequently and
  The cardinality of S is unspecified. S can be fi-                         since it is the “shape of the future”, we call it the
nite, countably infinite, a continuum, a Cantor set, or                     state’s morph.
something stranger still. Examples of these are given in
Refs. [5] and [10]; see especially the examples for hidden            Ideally, each of these should be denoted by a different
Markov models given there.                                            symbol, and there should be distinct functions linking
                                                                      each of these structures to their causal state. To keep

                                                                  9
                                                                                                    ←       ←           →   →
the growth of notation under control, however, we shall                  Let us consider P( S = s , S = σ, S = s ).
be strategically vague about these distinctions. Readers
                                                                           ←      ←                 →   →
may variously picture ǫ as mapping histories to (i) simple             P ( S = s , S = σ, S = s )
indices, (ii) subsets of histories, or (iii) ordered triples of                →      →                 ←   ←               ←       ←
indices, subsets, and morphs; or one may even leave ǫ                    = P( S = s |S = σ, S = s )P(S = σ, S = s )                             (21)
uninterpreted, as preferred, without interfering with the                      →      →                 ←   ←               ←       ←       ←   ←
                                                                         = P( S = s |S = σ, S = s )P(S = σ| S = s )P( S = s ) .
development that follows.
                                                                                              ←     ←                           ←
                                                                       Now, P(S = σ| S = s ) = 0, unless σ = ǫ( s ), which case
                                                                                  ←    ←
                      ←                                                P(S = σ| S = s ) = 1. Either way, the first two factors
                      S                S4                              in the last line of Eq. (21) can be written, by Eq. (18),
                                                                                      →     →               ←   ←               ←       ←
                                  S3             S5                           P ( S = s |S = σ, S = s )P(S = σ| S = s )
           S1                                                                             →     →                       ←       ←
                                                                                  = P( S = s |S = σ)P(S = σ| S = s ) ,                          (22)

                                                                       so that, substituting Eq. (22) into Eq. (21),
                                  S2
                                                 S6                           ←     ←               →       →
                                                                        P ( S = s , S = σ, S = s )
                                                                                  →     →                           ←   ←       ←       ←
                                                                          = P( S = s |S = σ)P(S = σ| S = s )P( S = s ) .                        (23)
  FIG. 2. A schematic representation of the partitioning of            QED.
        ←
the set S of all histories into causal states Si ∈ S. Within
                                               ←
each causal state all the individual histories s→have the same
                                                  ←
morph—the same conditional distribution P( S | s ) for future                                       2. Homogeneity
observables.
                                                                         Following Ref. [58], we introduce two new definitions
                          1. Morphs
                                                                       and a lemma which are required later on, especially in
                                                                       the proof of Lemma 7 and the theorems depending on
                                                                       that lemma.
  Each causal state has a unique morph, i.e., no two
causal states have the same conditional distribution of                Definition 6 (Strict Homogeneity) A set X is
futures. This follows directly from Def. 5, and it is not              strictly homogeneous with respect to a certain random
true of effective states in general. Another immediate                 variable Y when the conditional distribution P(Y |X) for
consequence of that definition is that                                 Y is the same for all subsets of X.
         →   →          ←         →    →    ←   ←
       P( S = s |S = ǫ( s )) = P( S = s | S = s ).        (18)
                                                                       Definition 7 (Weak Homogeneity) A set X is
(Again, this is not generally true of effective states.) This          weakly homogeneous with respect to Y if X is not strictly
observation lets us prove a useful lemma about the con-                homogeneous with respect to Y , but X \ X0 (X with X0
                                     ←                   →
ditional independence of the past S and the future S .                 removed) is, where X0 is a subset of X of measure 0.
Lemma 2 The past and the future are independent, con-
ditioning on the causal states.                                        Lemma 3 (Strict Homogeneity of Causal States)
                                                                       A process’s causal states are the largest subsets of his-
  Proof. Recall that two random variables X and Z are                  tories that are all strictly homogeneous with respect to
conditionally independent if and only if there is a third              futures of all lengths.
variable Y such that
                                                                          Proof. We must show that, first, the causal states are
P(X = x, Y = y, Z = z)
                                                                       strictly homogeneous with respect to futures of all lengths
    = P(X = x|Y = y)P(Z = z|Y = y)P(Y = y) . (19)                      and, second, that no larger strictly homogeneous subsets
That is, all of the dependence of Z on X is mediated                   of histories could be made. The first point, the strict ho-
by Y . For convenience below we note that, re-factoring                mogeneity of the causal states, is evident from Eq. (17):
the conditional probabilities, this is equivalent to the re-           By construction, all elements of a causal state have the
quirement that:                                                        same morph, so any part of a causal state will have the
                                                                       same morph as the whole state. The second point like-
P(X = x, Y = y, Z = z)                                                 wise follows from Eq. (17), since the causal state by con-
    = P(Z = z|Y = y)P(Y = y|X = x)P(X = x) . (20)                      struction contains all the histories with a given morph.


                                                                  10
                                                                                                                 ←
Any other set strictly homogeneous with respect to fu-                         Now S = Si if and only if s ∈ Si , and S ′ = Sj if and
tures must be smaller than a causal state, and any set                              ←′                      ←′
                                                                               only s ∈ Sj , where by s we mean the history that is
that includes a causal state as a proper subset cannot be                                                        ←                 ←′    ←
strictly homogeneous. QED.                                                     the immediate successor to s ; for consistency, s = s s.
   Remark. The statistical explanation literature would                        So we can rewrite Eq. (28) as
say that causal states are the “statistical-relevance basis                                                →1
                                                                                                 ←                ←′
for causal explanations”. The elements of such a basis                                     (s) P( s ∈ Si , S = s, s ∈ Sj )
are, precisely, the largest classes of combinations of inde-                             Tij =                                           (29)
                                                                                                       P(S = Si )
pendent variables with homogeneous distributions for the                                                   →1
                                                                                                 ←                ←
dependent variables. See Ref. [58] for further discussion                                      P( s ∈ Si , S = s, s s ∈ Sj )
along these lines.                                                                           =                                           (30)
                                                                                                           P(S = Si )
                                                                                                    ←        ←
                                                                                                 P( s ∈ Si , s s ∈ Sj )
                                                                                             =                                           (31)
           B. Causal State-to-State Transitions                                                      P(S = Si ) .
                                                                                                                          ←   ←     ←′    ←
   The causal state at any given time and the next value                       In the third line we used the fact that S = s and S = s s
                                                                                               →1
of the observed process together determine a new causal                        jointly imply S = s, making that condition redundant.
state; this is proved shortly in Lemma 5. Thus, there is                       QED.
a natural relation of succession among the causal states;                                       (λ)
                                                                                  Notice that Tij = δij ; that is, the transition labeled
recall the discussion of causality in Sec. II E. Moreover,
                                                                               by the null symbol λ is the identity.
given the current causal state, all the possible next values
have well defined conditional probabilities. In fact, by
construction the entire semi-infinite future does. Thus,
                                         (s)                                                             C. ǫ-Machines
there is a well defined probability Tij of the process
generating the value s ∈ A and going to causal state Sj ,
                                                                                  The combination of the function ǫ from histories to
if it is in state Si .                                                                                                                   (s)
                                                                               causal states with the labeled transition probabilities Tij
Definition 8 (Causal Transitions) The labeled transi-                          is called the ǫ-machine of the process [5,6].
                   (s)
tion probability Tij is the probability of making the tran-                    Definition 9 (An ǫ-Machine Defined)
sition from state Si to state Sj while emitting the symbol                     The ǫ-machine of a process is the ordered pair {ǫ, T},
s ∈ A:                                                                         where ǫ is the causal state function and T is set of the
            (s)                         →1                                     transition matrices for the states defined by ǫ.
           Tij ≡ P(S ′ = Sj , S = s|S = Si ) ,                     (24)
                                                                                 Equivalently, we may denote an ǫ-machine by {S, T}.
                                                                                 To satisfy the algebraic requirement outlined in
                                                                               Sec. II F, we make explicit the connection with semi-
where S is the current causal state and S ′ its successor                      group theory.
                                    (s)
on emitting s. We denote the set {Tij : s ∈ A} by T.
                                                                               Proposition 1 (ǫ-Machines Are Monoids) The al-
                                                         (s)
Lemma 4 (Transition Probabilities) Tij                         is given        gebra generated by the ǫ-machine {ǫ, T} is a semi-group
by                                                                             with an identity element, i.e., it is a monoid.
                  (s)         ←          ←
             Tij = P( s s ∈ Sj | s ∈ Si )                          (25)           Proof. See App. D.
                              ←          ←                                        Remark. Due to this, ǫ-machines can be interpreted as
                            P( s ∈ Si , s s ∈ Sj )                             capturing a process’s generalized symmetries. Any sub-
                        =           ←                ,             (26)
                                  P( s ∈ Si )                                  groups of an ǫ-machine’s semi-group are, in fact, symme-
                                                                               tries in the more familiar sense.
       ←
where s s is read as the semi-infinite sequence obtained
                                        ←                                      Lemma 5 (ǫ-Machines Are Deterministic) For each
by concatenating s ∈ A onto the end of s .                                                     (s)                                ←
                                                                               Si and s ∈ A, Tij > 0 only for that Sj for which ǫ( ss) =
                                                                                                     ←                        ←
  Proof.                                                                       Sj if and only if ǫ( s ) = Si , for all pasts s .
            (s)                       →1
        Tij = P(S ′ = Sj , S = s|S = Si )                          (27)           Proof. The lemma is equivalent to asserting that for
                                                                                                 ← ←′    ←       ←      ←′          ←
                                      →1                                       all s ∈ A and s , s ∈ S , if ǫ( s ) = ǫ( s ), then ǫ( ss) =
                    P(S ′ = Sj , S = s, S = Si )                                 ←′      ←
                  =                                                (28)        ǫ( s s). ( ss is just another history and belongs to one or
                            P(S = Si ) .                                       another causal state.)


                                                                          11
  Suppose this were not true. Then there would have to                                              Proof. What we wish to show is that, writing S, S ′ ,
                          →                                                                        ′′
exist at least one future s such that                                                             S for the sequence of causal states at three successive
                                                                                                  times, S and S ′′ are conditionally independent, given S ′ .
         →   →       ←       ←             →        →    ←      ←′
       P( S = s | S = ss) 6= P( S = s | S = s s) ,                                    (32)        We can do this directly:

                             ←             ←′                                                      P ( S = σ, S ′ = σ ′ , S ′′ = σ ′′ )
when nonetheless ǫ( s ) = ǫ( s ). Equivalently, we would
have                                                                                                 = P(S ′′ = σ ′′ |S = σ, S ′ = σ ′ )P(S = σ, S ′ = σ ′ )
                                                                                                                →1
                 ↔       ← →                    ↔      ←′ →                                             = P( S ∈ a|S = σ, S ′ = σ ′ )P(S = σ, S ′ = σ ′ ) ,           (36)
             P( S = ss s )                P( S = s s s )
                 ←        ←
                                     6=         ←       ←′
                                                                  ,                   (33)
              P( S = ss)                   P( S = s s)                                            where a is the subset of all symbols that lead from σ ′ to
                                                                                                  σ ′′ . This is a well defined subset, in virtue of Lemma 5
                         →
where we read s s as the semi-infinite string that be-                                            immediately preceding, which also guarantees the equal-
                     →                                                                            ity of conditional probabilities we have used. Likewise,
gins s and continues s . (Remember, the point at which
we break the stochastic process into a past and a fu-                                                                                      →1
ture is arbitrary.) However, the probabilities in the de-                                                  P(S ′′ = σ ′′ |S ′ = σ ′ ) = P( S ∈ a|S ′ = σ ′ ) .        (37)
                                          →1            ←       ←         ←       ←
nominators are equal to P( S = s| S = s )P( S = s ) and                                           But, by construction,
  →1         ←       ←′          ←        ←′
P( S = s| S = s )P( S = s ), respectively, and by as-                                                      →1                                 →1
               →1             ←       ←′                →1            ←       ←                         P( S ∈ a|S = σ, S ′ = σ ′ ) = P( S ∈ a|S ′ = σ ′ ) ,          (38)
sumption P( S = s| S = s ) = P( S = s| S = s ), since
  ←′       ←
ǫ( s ) = ǫ( s ). Therefore, we would need                                                         and hence
                 ↔       ←    →                 ↔       ←′ →                                            P(S ′′ = σ ′′ |S ′ = σ ′ ) = P(S ′′ = σ ′′ |S = σ, S ′ = σ ′ ) .
             P( S = s s s )               P( S = s s s )
                   ←                 6=            ←     ←′
                                                                  .                   (34)
              P( S = s )
                          ←
                                            P( S = s )                                                                                                                (39)

This is the same, though, as                                                                      So, to resume,

         →     →     ←        ←                →        →     ←       ←′                          P ( S = σ, S ′ = σ ′ , S ′′ = σ ′′ )
     P( S = s s | S = s ) 6= P( S = s s | S = s ) .                                   (35)
                                                                                                    = P(S ′′ = σ ′′ |S ′ = σ ′ )P(S = σ, S ′ = σ ′ )
                                                            →
This is to say that there is a future s s that has different                                        = P(S ′′ = σ ′′ |S ′ = σ ′ )P(S ′ = σ ′ |S = σ)P(S = σ) . (40)
                                                          ←
probabilities depending on whether we conditioned on s
       ←′                                                                                         The last line follows from the definition of conditional
or on s . But this contradicts the assumption that the                                            probability and is equivalent to the more easily inter-
two histories belong to the same causal state. Therefore,                                         preted expression given by
                         →
there is no such future s , and the alternative statement
of the lemma is true. QED.                                                                                            P(S ′′ |S ′ )P(S|S ′ )P(S ′ ) .                 (41)
   Remark 1. In automata theory [66], a set of states and
transitions is said to be deterministic if the current state                                      Thus, applying mathematical induction to Eq. (41),
and the next input—here, the next result from the origi-                                          causal states at different times are independent, condi-
nal stochastic process—together fix the next state. This                                          tioning on the intermediate causal states. QED.
use of the word “deterministic” is often confusing, since                                            Remark 1. This lemma strengthens the claim that the
many stochastic processes (e.g., simple Markov chains)                                            causal states are, in fact, the causally efficacious states:
are deterministic in this sense.                                                                  given knowledge of the present state, what has gone be-
   Remark 2. Starting from a fixed state, a given symbol                                          fore makes no difference. (Again, recall the philosophical
always leads to at most one single state. But there can                                           preliminaries of Sec. II E.)
be several transitions from one state to another, each                                               Remark 2. This result indicates that the causal states,
labeled with a different symbol.                                                                  considered as a process, define a kind of Markov chain.
                                          (s)                         (s)             →1          Thus, causal states can be roughly considered to be a
   Remark 3. Clearly, if Tij > 0, then Tij = P( S =                                               generalization of Markovian states. We say “kind of”
s|S = Si ). In automata theory the “disallowed” transi-                                           since the class of ǫ-machines is substantially richer [5,10]
         (s)
tions (Tij = 0) are sometimes explicitly represented and                                          than what one normally associates with Markov chains
lead to a “reject” state indicating that the particular his-                                      [67,68].
tory does not occur.
                                                                                                  Definition 10 (ǫ-Machine Reconstruction)
Lemma 6 (Causal States Are Independent) The                                                       ǫ-Machine reconstruction is any procedure that given a
                                                                                                             ↔                             ↔
probability distributions over causal states at different                                         process P( S ), or an approximation of P( S ), produces the
times are conditionally independent.                                                              process’s ǫ-machine {S, T}.

                                                                                             12
                                                                       →1
   Given a mathematical description of a process, one can              S ∈ A the next “observable” we get from the original
often calculate analytically its ǫ-machine. (For example,              stochastic process, S ′ the next causal state, R the cur-
see the computational mechanics analysis of spin systems               rent state according to η, and R′ the next η-state. σ will
in Ref. [65].) There is also a wide range of algorithms                stand for a particular value (causal state) of S and ρ a
which reconstruct ǫ-machines from empirical estimates                  particular value of R. When we quantify over alterna-
      ↔
of P( S ). Some, such as those used in Refs. [5–7,69], op-             tives to the causal states, we quantify over R.
erate in “batch” mode, taking the raw data as a whole
and producing the ǫ-machine. Others could operate in-                  Theorem 1 (Causal States are Maximally Pre-
crementally, in “on-line” mode, taking in individual mea-              scient) [15]
surements and re-estimating the set of causal states and                 For all R and all L ∈ Z+ ,
their transition probabilities.
                                                                                           →L            →L
                                                                                         H[ S |R] ≥ H[ S |S] .                    (42)
      V. OPTIMALITIES AND UNIQUENESS

                                                                                                                          →L
  We now show that: causal states are maximally ac-                      Proof.     We have already seen that H[ S |R] ≥
curate predictors of minimal statistical complexity; they                   →L ←
are unique in sharing both properties; and their state-                H[ S | S ] (Lemma 1). But by construction (Def. 5),
to-state transitions are minimally stochastic. In other
                                                                             →L     →L ←      ←        →L     →L        ←
words, they satisfy both of the constraints borrowed from                P( S     = s | S = s ) = P( S      = s |S = ǫ( s )) .    (43)
Occam, and they are the only representations that do
so. The overarching moral here is that causal states                   Since entropies depend only on the probability distri-
and ǫ-machines are the goals in any learning or model-                              →L              →L    ←
                                                                       bution, H[ S |S] = H[ S | S ] for every L.                Thus,
ing scheme. The argument is made by the time-honored                        →L           →L
means of proving optimality theorems. We address, in                   H[ S |R] ≥ H[ S |S], for all L. QED.
our concluding remarks (Sec. VII), the practicalities in-                 Remark. That is to say, causal states are as good at
volved in attaining these goals.                                       predicting the future—are as prescient—as complete his-
                                                                       tories. In this, they satisfy the first requirement borrowed
                                                                       from Occam. Since the causal states are well defined and
                      ←                     R4                         since they can be systematically approximated, we have
                      S                S4                              shown that the upper bound on the strength of patterns
                                                                       (Def. 3 and Lemma 1, Remark) can in fact be reached.
                                      S3         S5                    Intuitively, the causal states achieve this because, unlike
           S1                                                          effective states in general, they do not throw away any
                                                                       information about the future which might be contained
                                                                           ←
                R1                          R3                         in S . Even more colloquially, to paraphrase the defini-
                                 S2                                    tion of information in Ref. [70], the causal states record
                                                 S6                    every difference (about the past) that makes a difference
                        R2                                             (to the future). We can actually make this intuition quite
                                                                       precise, in an easy corollary to the theorem.
  FIG. 3. An alternative class R of states (delineated by
                             ←                                         Corollary 1 (Causal States Are Sufficient Statis-
dashed lines) that partition S overlaid on the causal states S         tics) The causal states S of a process are sufficient statis-
(outlined by solid lines). Here, for example, S2 contains parts        tics for predicting it.
of R1 , R2 , R3 and R4 . The collection of all such alternative
partitions form Occam’s pool. Note again that the Ri need                Proof. It follows from Thm. 1 and Eq. (8) that, for all
not be compact nor simply connected, as drawn.                         L ∈ Z+ ,
  As part of our strategy, though, we also prove sev-                                      →L            →L ←
eral results that are not optimality results; we call these                              I[ S ; S] = I[ S ; S ] ,                 (44)
lemmas to indicate their subordinate status. All of our
                                                                       where I was defined in Eq. (8). Consequently, the causal
theorems, and some of our lemmas, will be established by
                                                                       state is a sufficient statistic—see Refs. [62, p. 37] and [71,
comparing causal states, generated by ǫ, with other rival
                                                                       sec. 2.4–2.5]—for predicting futures of any length. QED.
sets of states, generated by other functions η. In short,
                                                                          All subsequent results concern rival states that are as
none of the rival states—none of the other patterns—can
                                                                       prescient as the causal states. We call these prescient
out-perform the causal states.
                                                                       rivals and denote a class of them R̂.
  It is convenient to fix some additional notation. Let
S be the random variable for the current causal state,

                                                                  13
Definition 11 (Prescient Rivals) Prescient rivals R̂                 improper) subset of some Sj . Otherwise, at least one R̂i
are states that are as predictive as the causal states; viz.,        would have to contain parts of at least two causal states.
for all L ∈ Z+ ,                                                     And so, using this R̂i to predict the future observables
                                                                                                                →
                   →L              →L
                                                                     would lead to more uncertainty about S than using the
                H[ S |R̂] = H[ S |S] .                   (45)        causal states. This is illustrated by Fig. 4, which should
                                                                     be contrasted with Fig. 3.
                                                                        Adding the measure-0 set ρ̂0 of histories to this picture
                                                                     does not change its heuristic content much. Precisely be-
  Remark. Prescient rivals are also sufficient statistics.           cause these histories have zero probability, treating them
                                                                     in an “inappropriate” way makes no discernible difference
Lemma 7 (Refinement Lemma) For all prescient ri-                     to predictions, morphs, and so on. There is a problem
vals R̂ and for each ρ̂ ∈ R̂, there is a σ ∈ S and                   of terminology, however, since there seems to be no stan-
a measure-0 subset ρ̂0 ⊂ ρ̂, possibly empty, such that               dard name for the relationship between the partitions R̂
ρ̂ \ ρ̂0 ⊆ σ, where \ is set subtraction.                            and S. We propose to say that the former is a refinement
                                                                     of the latter almost everywhere or, simply, a refinement
   Proof. We invoke a straightforward extension of                   a.e.
Thm. 2.7.3 of Ref. [62]: If X1 , X2 , . . . , Xn are random
                                                                        Remark 3. One cannot work the proof the other way
variables over the same set A, each with distinct proba-             around to show that the causal states have to be a refine-
bility distributions, Θ a random variable over the integers
                                                                     ment of the equally prescient R̂-states. This is precluded
from 1 to n such that P(Θ = i) = λi , and Z a random                 because applying the theorem borrowed from Ref. [62],
variable over A such that Z = XΘ , then
                                                                     Eq. (46), hinges on being able to reduce uncertainty by
                        Xn                                           specifying from which distribution one chooses. Since
               H[Z] = H[   λi Xi ]                                   the causal states are constructed so as to be strictly ho-
                            i=1                                      mogeneous with respect to futures, this is not the case.
                          n
                          X                                          Lemma 3 and Thm. 1 together protect us.
                      ≥         λi H[Xi ] .              (46)           Remark 4. Because almost all of each prescient rival
                          i=1                                        state is wholly contained within a single causal state,
                                                                     we can construct a function g : R̂ 7→ S, such that, if
In words, the entropy of a mixture of distributions is at              ←                 ←
                                                                     η( s ) = ρ̂, then ǫ( s ) = g(ρ̂) almost always. We can even
least the mean of the entropies of those distributions.
This follows since H is strictly concave, which in turn              say that S = g(R̂) almost always, with the understanding
follows from x log x being strictly convex for x ≥ 0. We             that this means that, for each ρ̂, P(S = σ|R̂ = ρ̂) > 0 if
obtain equality in Eq. (46) if and only if all the λi are            and only if σ = g(ρ̂).
either 0 or 1, i.e., if and only if Z is at least weakly
homogeneous (Def. 7).
   The conditional distribution of futures for each rival                                 ←
                                                                                           S         ∧
state ρ can be written as a weighted mixture of the
                                                                                  ∧                  R 8 S4
morphs of one or more causal states. (Cf. Fig. 3.) Thus,                          R1      ∧        ∧     ∧
                                                                                                                     S5
by Eq. (46), unless every ρ is at least weakly homoge-
                          →L
                                                                                S1        R9       R 7 S3R 6         ∧
neous with respect to S          (for each L), the entropy of                                                        R 10
→L                                                                             ∧                    ∧
S conditioned on R will be higher than the minimum,                            R2           ∧       R 5 S2            ∧
the entropy conditioned on S. So, in the case of the                                        R3
maximally predictive R̂, every ρ̂ ∈ R̂ must be at least                                             ∧                 R 11
                                               →L                                                   R4              S6
weakly homogeneous with respect to all S . But the
causal states are the largest classes that are strictly ho-
                                      →L
mogeneous with respect to all S (Lemma 3). Thus,                        FIG. 4. A prescient rival partition R̂ must be a refine-
the strictly homogeneous part of each ρ̂ ∈ R̂ must be a              ment of the causal-state partition almost everywhere. That
subclass, possibly improper, of some causal state σ ∈ S.             is, almost all of each R̂i must contained within some Sj ; the
QED.                                                                 exceptions, if any, are a set of histories of measure 0. Here
  Remark 1. An alternative proof appears in App. E.                  for instance S2 contains the positive-measure parts of R̂3 ,
  Remark 2. The content of the lemma can be made                     R̂4 , and R̂5 . One of these rival states, say R̂3 , could have
quite intuitive, if we ignore for a moment the measure-0             member-histories in any or all of the other causal states, pro-
                                                                     vided the total measure of such exceptional histories is zero.
set ρ̂0 of histories mentioned in its statement. It then as-
                                                                     Cf. Fig. 3.
serts that any alternative partition R̂ that is as prescient
as the causal states must be a refinement of the causal-
state partition. That is, each R̂i must be a (possibly

                                                                14
Theorem 2 (Causal States Are Minimal) [15] For                         Theorem 3 (Causal States Are Unique) For all pre-
all prescient rivals R̂,                                               scient rivals R̂, if Cµ (R̂) = Cµ (S), then there exists an
                                                                       invertible function between R̂ and S that almost always
                   Cµ (R̂) ≥ Cµ (S) .                     (47)         preserves equivalence of state: R̂ and η are the same
                                                                       as S and ǫ, respectively, except on a set of histories of
                                                                       measure 0.
  Proof. By Lemma 7, Remark 4, there is a function g
                                                                         Proof. From Lemma 7, we know that S = g(R̂) almost
such that S = g(R̂) almost always. But H[f (X)] ≤ H[X]
                                                                       always. We now show that there is a function f such
(Eq. (A11)) and so
                                                                       that R̂ = f (S) almost always, implying that g = f −1
                                                                       and that f is the desired relation between the two sets of
              H[S] = H[g(R̂)] ≤ H[R̂] .                   (48)
                                                                       states. To do this, by Eq. (A12) it is sufficient to show
but Cµ (R̂) = H[R̂] (Def. 4). QED.                                     that H[R̂|S] = 0. Now, it follows from an information-
  Remark 1. We have just established that no rival pat-                theoretic identity (Eq. (A8)) that
tern, which is as good at predicting the observations as
the causal states, is any simpler, in the sense given by                        H[S] − H[S|R̂] = H[R̂] − H[R̂|S] .               (49)
Def. 4, than the causal states. (This is the theorem of
Ref. [6].) Occam therefore tells us that there is no reason            Since, by Lemma 7 H[S|R̂] = 0, both sides of Eq. (49)
not to use the causal states. The next theorem shows                   are equal to H[S]. But, by hypothesis, H[R̂] = H[S].
that causal states are uniquely optimal, and so that Oc-               Thus, H[R̂|S] = 0 and so there exists an f such that
cam’s Razor all but forces us to use them.                             R̂ = f (S) almost always. We have then that f (g(R̂)) =
  Remark 2. Here it becomes important that we are try-                 R̂ and g(f (S)) = S, so g = f −1 . This implies that f
                             →
ing to predict the whole of S and not just some piece,                 preserves equivalence of states almost always: for almost
→L                                                                         ← ←′    ←     ←        ←′                    ←        ←′
                              ←       ←′                               all s , s ∈ S , η( s ) = η( s ) if and only if ǫ( s ) = ǫ( s ).
S . Suppose two histories s and s have the same con-
ditional distribution for futures of lengths up to L, but              QED.
differing ones after that. They would then belong to dif-                 Remark. As in the case of the Refinement Lemma 7, on
ferent causal states. An η-state that merged those two                 which the theorem is based, the measure-0 caveats seem
causal states, however, would have just as much ability                unavoidable. A rival that is as predictive and as simple
           →L                                                          (in the sense of Def. 4) as the causal states, can assign
to predict S as the causal states. More, these R-states                a measure-0 set of histories to different states than the
would be simpler, in the sense that the uncertainty in the             ǫ-machine does, but no more. This makes sense: such
current state would be lower. We conclude that causal                  a measure-0 set makes no difference, since its members
states are optimal, but for the hardest job—that of pre-               are never observed, by definition. By the same token,
dicting futures of all lengths.                                        however, nothing prevents a minimal, prescient rival from
   Remark 3. We have already seen (Thm. 1, Remark 2)                   disagreeing with the ǫ-machine on those histories.
that causal states are sufficient statistics for predicting
futures of all lengths; so are all prescient rivals. A mini-           Theorem 4 (ǫ-Machines Are Minimally Stochas-
mal sufficient statistic is one that is a function of all other        tic) [15] For all prescient rivals R̂,
sufficient statistics [62, p. 38]. Since, in the course of the
proof of Thm. 2, we have shown that there is a function                                 H[R̂′ |R̂] ≥ H[S ′ |S] ,                 (50)
g from any R̂ to S, we have also shown that causal states
are minimal sufficient statistics.                                     where S ′ and R̂′ are the next causal state of the process
   We may now, as promised, define the statistical com-                and the next η-state, respectively.
plexity of a process [5,6].
                                                                                                                              →1
Definition 12 (Statistical Complexity of a Pro-                          Proof. From Lemma 5, S ′ is fixed by S and S              to-
                                                                                                 →1
cess) The statistical complexity “Cµ (O)” of a process O                                    ′
                                                                       gether, thus H[S |S, S ] = 0 by Eq. (A12). Therefore,
is that of its causal states: Cµ (O) ≡ Cµ (S).                         from the chain rule for entropies Eq. (A6),
  Due to the minimality of causal states we see that the                                →1               →1
statistical complexity measures the average amount of                                H[ S |S] = H[S ′ , S |S] .                  (51)
historical memory stored in the process. Without the
                                                                       We have no result like the Determinism Lemma 5
minimality theorem, this interpretation would not be
                                                                       for the rival states R̂, but entropies are always non-
possible, since we could trivially elaborate internal states,                                   →1                          →L
while still generating the same observed process. Cµ for               negative: H[R̂′ |R̂, S ] ≥ 0. Since for all L, H[ S |R̂] =
those states would grow without bound and so be ar-                       →L
                                                                       H[ S |S] by the definition, Def. (11), of prescient rivals,
bitrary and not a characteristic property of the process                  →1           →1
[17].                                                                  H[ S |R̂] = H[ S |S]. Now we apply the chain rule again,

                                                                  15
              →1           →1                  →1
      H[R̂′ , S |R̂] = H[ S |R̂] + H[R̂′ | S , R̂]          (52)        Definition 13 (Excess Entropy) The excess entropy
                           →1
                                                                        E of a process is the mutual information between its semi-
                     ≥ H[ S |R̂]                            (53)        infinite past and its semi-infinite future:
                           →1                                                                       → ←
                     = H[ S |S]                             (54)                             E ≡ I[ S ; S ] .                        (61)
                                →1
                            ′
                     = H[S , S |S]                          (55)
                                          →1
                     = H[S ′ |S] + H[ S |S ′ , S] .         (56)           The excess entropy is a frequently-used measure of the
                                                                        complexity of stochastic processes and appears under a
In going from Eq. (54) to Eq. (55) we have used Eq. (51),               variety of names; e.g., “predictive information”, “stored
and in the last step we have used the chain rule once                   information”, “effective measure complexity”, and so on
more.                                                                   [73–79]. E measures the amount of apparent information
  Using the chain rule one last time, we have                           stored in the observed behavior about the past. As we
              →1                          →1                            now establish, E is not, in general, the amount of mem-
      H[R̂′ , S |R̂] = H[R̂′ |R̂] + H[ S |R̂′ , R̂] .       (57)        ory that the process stores internally about its past; a
                                                                        quantity measured by Cµ .
Putting these expansions, Eqs. (56) and (57), together
we get                                                                  Theorem 5 (The Bounds of Excess) The statistical
                                                                        complexity Cµ bounds the excess entropy E:
                →1                              →1
H[R̂′ |R̂] + H[ S |R̂′ , R̂] ≥ H[S ′ |S] + H[ S |S ′ , S]   (58)                                 E ≤ Cµ ,                            (62)
                                     →1              →1
     H[R̂′ |R̂] − H[S ′ |S] ≥ H[ S |S ′ , S] − H[ S |R̂′ , R̂] .                                                →
                                                                        with equality if and only if H[S| S ] = 0.
From Lemma 7, we know that S = g(R̂), so there is an-                                     → ←           →           →    ←
other function g ′ from ordered pairs of η-states to ordered              Proof. E = I[ S ; S ] = H[ S ] − H[ S | S ] and, by the
                                                                                                            →       ←        →
pairs of causal states: (S ′ , S) = g ′ (R̂′ , R̂). Therefore,          construction of causal states, H[ S | S ] = H[ S |S], so
Eq. (A14) implies
                                                                                           →        →               →
               →1                →1
                                                                                   E = H[ S ] − H[ S |S] = I[ S ; S] .               (63)
            H[ S |S ′ , S] ≥ H[ S |R̂′ , R̂] .              (59)
                                                                        Thus, since the mutual information between two vari-
And so, we have that                                                    ables is never larger than the self-information of either
                                                                        one of them (Eq. (A9)), E ≤ H[S] = Cµ , with equality
         →1               →1                                                                 →
      H[ S |S ′ , S] − H[ S |R̂′ , R̂] ≥ 0                              if and only if H[S| S ] = 0. QED.
                                                                                                                                 →
               H[R̂′ |R̂] − H[S ′ |S] ≥ 0                                 Remark 1.      Note that we have invoked H[ S ], not
                                                                          →L
                           H[R̂′ |R̂] ≥ H[S ′ |S] .         (60)        H[ S ], but only while subtracting off quantities like
                                                                          →    ←
                                                                        H[ S | S ]. We need not worry, therefore, about the exis-
QED.                                                                                                                →L
   Remark. What this theorem says is that there is no                   tence of a finite L → ∞ limit for H[ S ], just that of a
                                                                                                   →L ←                 →L
more uncertainty in transitions between causal states,                  finite L → ∞ limit for I[ S ; S ] and I[ S ; S]. There are
than there is in the transitions between any other kind                 many elementary cases (e.g., the fair coin process) where
of prescient effective states. In other words, the causal               the latter limits exist while the former do not.
states approach as closely to perfect determinism—in the                   Remark 2. At first glance, it is tempting to see E
usual physical, non-computation-theoretic sense—as any                  as the amount of information stored in a process. As
rival that is as good at predicting the future. This sort of            Thm. 5 shows, this temptation should be resisted. E is
internal determinism has long been held to be a desider-                only a lower bound on the true amount of information
atum of scientific models [72].                                         the process stores about its history, namely Cµ . We can,
                                                                        however, say that E measures the apparent information
                                                                        in the process, since it is defined directly in terms of
                       VI. BOUNDS
                                                                        observed sequences and not in terms of hidden, intrinsic
                                                                        states, as Cµ is.
  In this section we develop bounds between measures                       Remark 3. Perhaps another way to describe what E
of structural complexity and entropy derived from ǫ-                    measures is to note that, by its implicit assumption of
machines and those from ergodic and information the-                    block-Markovian structure, it takes sequence-blocks as
ories, which are perhaps more familiar.                                 states. But even for the class of block-Markovian sources,
                                                                        for which such an assumption is appropriate, excess en-
                                                                        tropy and statistical complexity measure different kinds

                                                                   16
of information storage. Refs. [65] and [80] showed that in          This, owing to the time-translation invariance of station-
the case of one-dimensional range-R spin systems, or any            arity, is equivalent to taking account of all the dependen-
other block-Markovian source where block configurations             cies in the entire process, including those between past
                                                                                                                          →
are isomorphic to causal states:                                    and future. But these are what is captured by h[ S |R̂].
                                                                    It is not that conditioning on R fails to reduce our un-
                    Cµ = E + Rhµ ,                     (64)         certainty about the future; it does so, for all finite times,
                                                                    and conditioning on S achieves the maximum possible
for finite R. Only for zero-entropy-rate block-Markovian
                                                                    reduction in uncertainty. Rather, the lemma asserts that
sources will the excess entropy, a quantity estimated di-
                                                                    such conditioning cannot effect the asymptotic rate at
rectly from sequence blocks, equal the statistical com-
                                                                    which such uncertainty grows with time.
plexity, the amount of memory stored in the process.
Examples of such sources include periodic processes, for            Theorem 6 (Control Theorem) Given a class R̂ of
which we have Cµ = E = log2 p, where p is the period.               prescient rivals,
Corollary 2 For all prescient rivals R̂,                                                          →
                                                                                     H[S] − h[ S |R̂] ≤ Cµ ,                         (70)
                        E ≤ H[R̂] .                    (65)         where H[S] is the entropy of a single symbol from the
                                                                    observable stochastic process.

                                                                      Proof. As is well known (Ref. [62, Thm. 4.2.1, p. 64]),
  Proof. This follows directly from Thm. 2, since H[R̂] ≥           for any stationary stochastic process,
Cµ . QED.
                                                                                         →L
Lemma 8 (Conditioning Does Not Affect Entropy                                        H[ S ]             →L−1
                                                                                 lim        = lim H[SL | S   ].                      (71)
Rate) For all prescient rivals R̂,                                              L→∞    L     L→∞

                        →        →                                  Moreover, the limits always exist. Up to this point, we
                    h[ S ] = h[ S |R̂] ,               (66)                         →
                                                                    have defined h[ S ] in the manner of the left-hand side;
                             →                                      recall Eq. (9). It will be convenient in the following to
where the entropy rate h[ S ] and the conditional entropy           use that of the right-hand side.
       →
rate h[ S |R̂] were defined in Eq. (9) and Eq. (10), re-              From the definition of conditional entropy, we have
spectively.
                                                                                  ←L          ←1 ←L−1             ←L−1
                                                                                H[ S ] = H[ S | S         ] + H[ S        ]
  Proof. From Thm. 5 and its Corollary 2, we have
                                                                                              ←L−1 ←1             ←1
                                                                                       = H[ S        | S ] + H[ S ] .              (72)
             →L       →L
     lim H[ S ] − H[ S |R̂] ≤ lim H[R̂] ,         (67)
      L→∞                                  L→∞                      So we can express the entropy of the last observable the
                                                                    process generated before the present as
or,
                                                                          ←1        ←L        ←L−1 ←1
               →L           →L                                       H[ S ] = H[ S ] − H[ S             |S ]                         (73)
           H[ S ] − H[ S |R̂]       H[R̂]
       lim                    ≤ lim       .            (68)                         ←1 ←L−1             ←L−1            ←L−1 ←1
      L→∞          L           L→∞   L                                         = H[ S | S     ] + H[ S         ] − H[ S       |S ]   (74)
                                                                                    ←1 ←L−1            ←L−1 ←1
                            →L        →L                                       = H[ S | S     ] + I[ S         ;S ] .                (75)
Since, by Eq. (A4), H[ S ] − H[ S |R̂] ≥ 0, we have
                    →        →                                      We go from Eq. (73) to Eq. (74) by substituting the first
                h[ S ] − h[ S |R̂] = 0 .               (69)                                       ←L
                                                                    RHS of Eq. (72) for H[ S ].
QED.                                                                 Taking the L → ∞ limit has no effect on the LHS,
   Remark. Forcing the process into a certain state R̂ = ρ̂                                                    
                                                                        ←1               ←1 ←L−1       ←L−1 ←1
is akin to applying a controller, once. But in the infinite-          H[ S ] = lim H[ S | S      ] + I[ S  ; S ] . (76)
                 →L                                                               L→∞
entropy case, H[ S ] →L→∞ ∞, with which we are con-
cerned, the future could contain (or consist of) an infi-           Since the process is stationary, we can move the first
nite sequence of disturbances. In the face of this “grand                                                        →L−1
                                                                    term in the limit forward to H[SL | S               ]. This limit is
disturbance”, the effects of the finite control are simply            →
washed out.                                                         h[ S ], by Eq. (71). Furthermore, because of stationarity,
                                                                       ←1          →1                                                 →
  Another way of viewing this is to reflect on the fact             H[ S ] = H[ S ] = H[S]. Shifting the entropy rate h[ S ]
       →
that h[ S ] accounts for the effects of all the dependencies        to the LHS of Eq. (76) and appealing to time-translation
between all the parts of the entire semi-infinite future.           once again, we have

                                                               17
                   →             ←L−1 ←1
         H[S] − h[ S ] = lim I[ S      ;S ]            (77)         prescient; our second, that they are the simplest way of
                         L→∞                                        representing the pattern of maximum strength; our third
                           ← →1                                     theorem, that they are unique in having this double op-
                       = I[ S ; S ]                    (78)
                                                                    timality. Further results showed that ǫ-machines are the
                            →1         →1 ←
                       = H[ S ] − H[ S | S ]           (79)         least stochastic way of capturing maximum-strength pat-
                            →1         →1
                                                                    terns and emphasized the need to employ the efficacious
                       = H[ S ] − H[ S |S]             (80)         but hidden states of the process, rather than just its gross
                           →1                                       observables, such as sequence blocks.
                       = I[ S ; S]                     (81)            Why are ǫ-machine states causal? First, ǫ-machine ar-
                       ≤ H[S] = Cµ ,                   (82)         chitecture (say, as given by its semi-group algebra) de-
                                                                                                                        →   ←
                                                                    lineates the dependency between the morphs P( S | S ),
where the last inequality comes from Eq. (A9). QED.                 considered as events in which each new symbol deter-
   Remark 1. The Control Theorem is inspired by, and is             mines the succeeding morph. Thus, if state B follows
a version of, Ashby’s law of requisite variety [81, ch. 11].        state A then A is a cause of B and B is an effect of A.
This states that applying a controller can reduce the un-           Second, ǫ-machine minimality guarantees that there are
certainty in the controlled variable by at most the en-             no other events that intervene to render A and B inde-
tropy of the control variable. (This result has recently            pendent [17].
been rediscovered in Ref. [82].) Thinking of the control-              The ǫ-machine is thus a causal representation of all the
ling variable as the causal state, we have here a limitation        patterns in the process. It is maximally predictive and
on the controller’s ability to reduce the entropy rate.             minimally complex. It is at once computational, since it
   Remark 2. This is the only result so far where the               shows how the process stores information (in the causal
difference between the finite-L and the infinite-L cases            states) and transforms that information (in the state-to-
is important. For the analogous result in the finite case,          state transitions), and algebraic (for details on which see
see App. F, Thm. 7.                                                 App. D). It can be analytically calculated from given
   Remark 3. By applying Thm. 2 and Lemma 8, we                     distributions and systematically approached from empir-
                                                           →
could go from the theorem as it stands to H[S] − h[ S               ical data. It satisfies the basic constraints laid out in
|R̂] ≤ H[R̂]. This has a pleasing appearance of symmetry            Sec. II F.
to it, but is actually a weaker limit on the strength of the           These comments suggest that computational mechan-
pattern or, equivalently, on the amount of control that             ics and ǫ-machines are related or may be of interest to
fixing the causal state (or one of its rivals) can exert.           a number of fields. Time series analysis, decision theory,
                                                                    machine learning, and universal coding theory explicitly
                                                                    or implicitly require models of observed processes. The
          VII. CONCLUDING REMARKS                                   theories of stochastic processes, formal languages and
                                                                    computation, and of measures of physical complexity are
                       A. Discussion                                all concerned with representations of processes—concerns
                                                                    which also arise in the design of novel forms of comput-
   Let’s review, informally, what we have shown. We                 ing devices. Very often the motivations of these fields
began with questions about the nature of patterns and               are far removed from computational mechanics. But it
about pattern discovery. Our examination of these issues            is useful, if only by way of contrast, to touch briefly on
lead us to want a way of describing patterns that was at            these areas and highlight one or several connections with
once algebraic, computational, intrinsically probabilistic,         computational mechanics, and we do so in App. G.
and causal. We then defined patterns in ensembles, in a
very general and abstract sense, as equivalence classes of
                                                                            B. Limitations of the Current Results
histories, or sets of hidden states, used for prediction. We
defined the strength of such patterns (by their forecasting
ability or prescience) and their statistical complexity (by           Let’s catalogue the restrictive assumptions we made at
the entropy of the states or the amount of information re-          the beginning and that were used by our development.
tained by the process about its history). We showed that
                                                                       1. We know exact joint probabilities over sequence
there was a limit on how strong such patterns could get
                                                                          blocks of all lengths for a process.
for each particular process, given by the predictive ability
of the entire past. In this way, we narrowed our goal to               2. The observed process takes on discrete values.
finding a predictor of maximum strength and minimum
complexity.                                                            3. The process is discrete in time.
   Optimal prediction led us to the equivalence relation
∼ǫ and the function ǫ and so to representing patterns by               4. The process is a pure time series; e.g., without spa-
causal states and their transitions—the ǫ-machine. Our                    tial extent.
first theorem showed that the causal states are maximally              5. The observed process is stationary.


                                                               18
   6. Prediction can only be based on the process’s past,              we are neither being rash when we say that we have laid
      not on any outside source of information.                        a foundation for those projects, nor that we are being
                                                                       flippant when we say that patterns are what ǫ-machines
The question arises, Can any be relaxed without much                   represent and that we discover them by ǫ-machine recon-
trouble?                                                               struction. We would like to close by marking out two
   One way to lift the first limitation is to develop a statis-        broad avenues for future work.
tical error theory for ǫ-machine inference that indicates,                First, consider the mathematics of ǫ-machines them-
say, how much data is required to attain a given level of              selves. We have just mentioned possible extensions
confidence in an ǫ-machine with a given number of causal               in the form of lifting assumptions made in this de-
states. This program is underway and, given its initial                velopment, but there are many other ways to go. A
progress, we describe several issues in more detail in the             number of measure-theoretic issues relating to the def-
next section.                                                          inition of causal states (omitted here for brevity) de-
   The second limitation probably can be addressed, but                serve careful treatment, along the lines of Ref. [10]. It
with a corresponding increase in mathematical sophis-                  would be helpful to have a good understanding of the
tication. The information-theoretic quantities we have                 measurement-resolution scaling properties of ǫ-machines
used are also defined for continuous random variables. It              for continuous-state processes, and of their relation to
is likely that many of the results carry over to the con-              such ideas in automata theory as the Krohn-Rhodes de-
tinuous setting.                                                       composition [30]. Anyone who manages to absorb Vol-
   The third limitation also looks similarly solvable, since           ume II of Ref. [26] would probably be in a position to
continuous-time stochastic process theory is moderately                answer interesting questions about the structures that
well developed. This may involve sophisticated probabil-               processes preserve, perhaps even to give a purely relation-
ity theory or functional analysis.                                     theoretic account of ǫ-machines. We have alluded in a
   As for the fourth limitation, there already exist tricks            number of places to the trade-off between prescience and
to make spatially extended systems look like time series.              complexity. For a given process there is presumably a
Essentially, one looks at all the paths through space-                 sequence of optimal machines connecting the one-state,
time, treating each one as if it were a time series. While             zero-complexity machine with minimal prescience to the
this works well for data compression [83], it is not yet               ǫ-machine. Each member of the path is the minimal ma-
clear whether it will be entirely satisfactory for captur-             chine for a certain degree of prescience; it would be very
ing structure [84]. More work needs to be done on this                 interesting to know what, if anything, we can say in gen-
subject.                                                               eral about the shape of this “prediction frontier”.
   It is unclear at this time how to relax the assumption of              Second, there is ǫ-machine reconstruction, an activity
stationarity. One can formally extend most of the results              about which we have said next to nothing. As we men-
in this paper to non-stationary processes without much                 tioned above (p. 12), there are already several algorithms
trouble. It is, however, unclear how much substantive                  for reconstructing machines from data, even “on-line”
content these extensions have and, in any case, a system-              ones. It is fairly evident that these algorithms will find
atic classification of non-stationary processes is (at best)           the true machine in the limit of infinite time and infinite
in its infant stages.                                                  data. What is needed is an understanding of the error
   Finally, one might say that the last restriction is a pos-          statistics [85] of different reconstruction procedures of the
itive feature when it comes to thinking about patterns                 kinds of mistakes these procedures make and the proba-
and the intrinsic structure of a process. “Pattern” is a               bilities with which they make them. Ideally, we want to
vague word, of course, but even in ordinary usage it is                find “confidence regions” for the products of reconstruc-
only supposed to involve things inside the process, not                tion. The aim is to calculate (i) the probabilities of differ-
the rest of the universe. Given two copies of a document,              ent degrees of reconstruction error for a given volume of
the contents of one copy can be predicted with an en-                  data, (ii) the amount of data needed to be confident of a
viable degree of accuracy by looking at the other copy.                fixed bound on the error, or (iii) the rates at which differ-
This tells us that they share a common structure, but                  ent reconstruction procedures converge on the ǫ-machine.
says absolutely nothing about what that pattern is, since              So far, an analytical theory has been developed that pre-
it is just as true of well-written and tightly-argued sci-             dicts the average number of estimated causal states as a
entific papers (which presumably are highly organized)                 function of the amount of data used when reconstructing
as it is of monkey-at-keyboard pieces of gibberish (which              certain kinds of processes [86]. Once we possess a more
definitely are not).                                                   complete theory of statistical inference for ǫ-machines,
                                                                       analogous perhaps to what already exists in computa-
                                                                       tional learning theory, we will be in a position to begin
   C. Conclusions and Directions for Future Work                       analyzing, sensibly and rigorously, the multitude of in-
                                                                       triguing patterns and information-processing structures
  Computational mechanics aims to understand the na-                   the natural world presents.
ture of patterns and pattern discovery. We hope that
the foregoing development has convinced the reader that


                                                                  19
                                                                                     ←0
                ACKNOWLEDGMENTS                                     Recall that s = λ, the empty string. We define the
                                                                                     ←
                                                                    relation ∼ǫ over S by
   We thank Dave Albers, Dave Feldman, Jon Fetter,
Rob Haslinger, Wim Hordijk, Amihan Huesmann, Cris                           ←K     ←L                    → ←K                   → ←L
                                                                            si ∼ ǫ sj          ⇔ P( S |si ) = P( S |sj ) ,                    (B2)
Moore, Mitch Porter, Erik van Nimwegen, and Karl
Young for advice on the manuscript; and the participants                                            →
in the 1998 SFI Complex Systems Summer School, the                  for all semi-infinite S = s0 s1 s2 · · ·, where K, L ∈ Z+ .
Madison probability seminar, the Madison Physics De-                Here we show that ∼ǫ is an equivalence relation by
partment’s graduate student mini-colloquium, and the                reviewing the basic properties of relations, equivalence
Ann Arbor Complex Systems seminar for numerous help-                classes, and partitions. (The proof details are straight-
ful comments on earlier versions of these results. This             forward and are not included. See Ref. [87].) We
work was supported at the Santa Fe Institute under                  will drop the length variables K and L and denote by
                                                                    ← ←′ ←′′      ←                                       ←
the Computation, Dynamics, and Inference Program via                 s , s , s ∈ S members of any length in the set S of
ONR grant N00014-95-1-0975, NSF grant PHY-9970158,                  Eq. (B1).
                                                                                                                 ←
and DARPA contract F30602-00-2-0583.                                  First, ∼ǫ is a relation on S since we can represent it
                                                                    as a subset of the Cartesian product
  APPENDIX A: INFORMATION-THEORETIC                                             ←       ←           ← ←′          ← ←′          ←
               FORMULÆ
                                                                                S × S = {( s , s ) : s , s ∈ S } .                            (B3)
                                                                                                                                                  ←
                                                                       Second, the relation ∼ǫ is an equivalence relation on S
  The following formulæ prove useful in the development.
                                                                    since it is
They are relatively intuitive, given our interpretation,
                                                                                           ←        ←             ←       ←
and they can all be proved with little more than straight              1. reflexive: s ∼ǫ s , for all s ∈ S ;
algebra; see Ref. [62, ch. 2]. Below, f is a function.
                                                                                               ←        ←′       ←′       ←
                                                                       2. symmetric: s ∼ǫ s ⇒ s ∼ǫ s ; and
             H[X, Y ] = H[X] + H[Y |X]                  (A1)
                                                                                            ←       ←′           ←′       ←′′       ←   ←′′
             H[X, Y ] ≥ H[X]                            (A2)           3. transitive: s ∼ǫ s and s ∼ǫ s ⇒ s ∼ǫ s .
             H[X, Y ] ≤ H[X] + H[Y ]                    (A3)                       ←       ←                                            ←
                                                                      Third, if s ∈ S , the equivalence class of s is
             H[X|Y ] ≤ H[X]                             (A4)
                                                                                                    ←′       ←   ←′
    H[X|Y ] = H[X] iff Xis independent of Y             (A5)                           ←
                                                                                     [ s ] = { s ∈ S : s ∼ǫ s } .
                                                                                                                          ←
                                                                                                                                              (B4)
         H[X, Y |Z] = H[X|Z] + H[Y |X, Z]               (A6)
                                                                                                                                ←             ←
         H[X, Y |Z] ≥ H[X|Z]                            (A7)        The set of all equivalence classes in S is denoted S /∼ǫ
                                                                                                                      ←
    H[X] − H[X|Y ] = H[Y ] − H[Y |X]                    (A8)        and is called the factor set of S with respect to ∼ǫ . In
             I[X; Y ] ≤ H[X]                            (A9)        Sec. IV A we called the individual equivalence classes
                                                                    causal states Si and denoted the set of causal states
    I[X; Y ] = H[X] iff H[X|Y ] = 0                    (A10)                                                            ←
                                                                    S = {Si : i = 0, 1, . . . , k − 1}. That is, S = S /∼ǫ .
            H[f (X)] ≤ H[X]                            (A11)
                                                                    (We noted in the main development that the cardinality
       H[X|Y ] = 0 iff X = f (Y )                      (A12)        k = |S| of causal states may or may not be finite.)
         H[f (X)|Y ] ≤ H[X|Y ]                         (A13)          Finally, we list several basic properties of the causal-
         H[X|f (Y )] ≥ H[X|Y ]                         (A14)        state equivalence classes.
                                                                          S      ←      ←
Eqs. (A1) and (A6) are called the chain rules for                      1. ←    ←[ s ] = S .
                                                                            s   ∈S
entropies. Strictly speaking, the right hand side of
                                                                            Sk−1            ←
Eq. (A12) should read “for each y, P(X = x|Y = y) > 0                  2.    i=0 Si = S .
for one and only one x”.
                                                                            ←        ←′         ←        ←′
                                                                       3. [ s ] = [ s ] ⇔ s ∼ǫ s .
APPENDIX B: THE EQUIVALENCE RELATION                                         ← ←′          ←
                                                                       4. If s , s ∈ S , either
    THAT INDUCES CAUSAL STATES
                                                                                   ← T ←′
                                                                            (a) [ s ]       [ s ] = ∅ or
   Any relation that is reflexive, symmetric, and transi-                          ←           ←′
tive is an equivalence relation.                                            (b) [ s ] = [ s ] .
                    ←
   Consider the set S of all past sequences, of any length:                                                                             ←
                                                                       5. The causal states S are a partition of S . That is,
   ←      ←L
   S = {s      = sL−1 · · · s−1 : si ∈ A, L ∈ Z+ } .    (B1)                (a) Si 6= ∅ for each i,

                                                               20
              Sk−1         ←
        (b)    i=0 Si = S , and
                                                                     remove probabilities.    Then define the set of matrices
                                                                     U = {T(λ) } {U(s) , s ∈ A}. Finally, define G as the
                                                                                   S
        (c) Si ∩ Sj = ∅ for all i 6= j.
                                                                     set of all matrices generated from the set U by recursive
  We denote the start state with S0 . The start state is             multiplication. That is, an element g of G is
                                 ←
the causal state associated with s = λ. That is, S0 = [λ].
                                                                               g (ab...cd) = U(d) U(c) . . . U(b) U(a) ,          (D1)

                                                                     where a, b, . . . c, d ∈ A. Clearly, G constitutes a semi-
          APPENDIX C: TIME REVERSAL
                                                                     group under matrix multiplication. Moreover, g (a...bc) =
                                                                     0 (the all-zero matrix) if and only if, having emitted the
   The definitions and properties of the causal states ob-           symbols a . . . b in order, we must arrive in a state from
tained by scanning sequences in the opposite direction,              which it is impossible to emit the symbol c. That is, the
                        →
i.e., the causal states S /∼ǫ , follow similarly to those de-        zero-matrix 0 is generated if and only if the concatenation
                                                ←     →              of c onto a . . . b is forbidden. The element ∅ is thus the
rived just above in App. B. In general, S /∼ǫ 6= S /∼ǫ .
That is, past causal states are not necessarily the same             all-zero matrix 0, which clearly satisfies the necessary
as future causal states; past and future morphs can dif-             constraints. This completes the proof of Proposition 1.
fer; unlike entropy rate [15], past and future statistical              We call the matrix representation—Eq. (D1) taken
                                    ←       →                        over all words in Ak —of G the semi-group machine of
complexities need not be equal: Cµ 6=Cµ ; and so on. The             the ǫ-machine {S, T}. See Ref. [89].
presence or lack of this type of time-reversal symmetry, as
reflected in these inequalities, is a fundamental property
of a process.                                                          APPENDIX E: ALTERNATE PROOF OF THE
                                                                              REFINEMENT LEMMA

  APPENDIX D: ǫ-MACHINES ARE MONOIDS                                   The proof of Lemma 7 carries through verbally, but
                                                                     we do not wish to leave loop-holes. Unfortunately, this
   A semi-group is a set of elements closed under an as-             means introducing two new bits of mathematics.
sociative binary operator, but without a guarantee that                First of all, we need the largest classes that are strictly
every, or indeed any, element has an inverse [88]. A                                                                         →L
monoid is a semi-group with an identity element. Thus,               homogeneous (Def. 6) with respect to S for fixed L;
semi-groups and monoids are generalizations of groups.               these are, so to speak, truncations of the causal states.
Just as the algebraic structure of a group is generally              Accordingly, we will talk about S L and σ L , which are
interpreted as a symmetry, we propose to interpret the               analogous to S and σ. We will also need to define the
algebraic structure of a semi-group as a generalized sym-            function φL         L     L
                                                                                σρ ≡ P(S = σ |R = ρ).
metry. The distinction between monoids and other semi-                 Putting these together, for every L we have
groups becomes important here: only semi-groups with                       →L             X       →L
an identity element—i.e., monoids—can contain subsets                    H[ S |R = ρ] = H[  φL         L   L
                                                                                             σρ P( S |S = σ )]                    (E1)
that are groups and so represent conventional symme-                                                     σL
tries.                                                                                              X           →L
   We claim that the transformations that concatenate                                           ≥        φL         L   L
                                                                                                          σρ H[ S |S = σ ] .      (E2)
strings of symbols from A onto other such strings form a                                            σL

semi-group G, the generators of which are the transfor-              Thus,
mations that concatenate the elements of A. The identity
element is to be provided by concatenating the null sym-                 →L                X                       →L
bol λ. The concatenation of string t onto the string s is            H[ S     | R] =            P(R = ρ)H[ S |R = ρ]              (E3)
                                                                                            ρ
forbidden if and only if strings of the form st have proba-
                                                                                                                     →L
bility zero in a process. All such concatenations are to be
                                                                                  X                      X
                                                                              ≥        P(R = ρ)               φL         L   L
                                                                                                               σρ H[ S |S = σ ]   (E4)
realized by a single semi-group element denoted ∅. Since                           ρ                     σL
if P(st) = 0, then P(stu) = P(ust) = 0 for any string                             X                             →L
u, we require that ∅g = g∅ = ∅ for all g ∈ G. Can we                          =           P(R = ρ)φL         L   L
                                                                                                   σρ H[ S |S = σ ]               (E5)
provide a representation of this semi-group?                                      σL ,ρ
   Recall that, from our definition of the labeled tran-                          X                                     →L
                        (λ)
sition probabilities, Tij = δij . Thus, T(λ) is an iden-                      =           P(S L = σ L , R = ρ)H[ S |S L = σ L ] (E6)
tity element. This suggests using the labeled transi-                             σL ,ρ
tion matrices to form a matrix representation of the                              X                            →
                                             (s)                              =        P(S L = σ L )H[ S |S L = σ L ]             (E7)
semi-group. Accordingly, first define Uij by setting                              σL
 (s)                 (s)              (s)
Uij    = 0 when Tij        = 0 and Uij      = 1 otherwise, to                          →L
                                                                              = H[ S |S L ] .                                     (E8)

                                                                21
That is to say,                                                                    1. Time Series Modeling

                   →L         →L
              H[ S |R] ≥ H[ S |S L ] ,                 (E9)            The goal of time series modeling is to predict the fu-
                                                                    ture of a measurement series on the basis of its past.
with equality if and only if every φL
                                    σρ is either 0 or 1.            Broadly speaking, this can be divided into two parts:
             →L           →                                         identify equivalent pasts and then produce a prediction
Thus, if H[ S |R̂] = H[ S |S L ], every ρ̂ is entirely con-         for each class of equivalent pasts. That is, we first pick
tained within some σ L ; except for possible subsets of                              ←
measure 0. But if this is true for every L—which, in                a function η : S 7→ R and then pick another function
                                                                               →
the case of a prescient rival R̂, it is—then every ρ̂ is            p : R 7→ S . Of course, we can choose for the range
at least weakly homogeneous (Def. 7) with respect to                of p futures of some finite length (length 1 is popular)
   →L                                                               or even choose distributions over these. While practical
all S . Thus, by Lemma 3, all its members, except for               applications often demand a single definite prediction—
that same subset of measure 0, belong to the same causal            “You will meet a tall dark stranger”, there are obvious
state. QED.                                                         advantages to predicting a distribution—“You have a .95
                                                                    chance of meeting a tall dark stranger and a .05 chance of
                                                                    meeting a tall familiar albino.” Clearly, the best choice
  APPENDIX F: FINITE ENTROPY FOR THE
                                                                    for p is the actual conditional distribution of futures for
        SEMI-INFINITE FUTURE
                                                                    each ρ ∈ R. Given this, the question becomes what the
                         →                                          best R is; i.e., What is the best η? At least in the case
  While cases where H[ S ] is finite—more exactly, where            of trying to understand the whole of the underlying pro-
             →L
limL→∞ H[ S ] exists and is finite—may be uninterest-               cess, we have shown that the best η is, unambiguously,
ing for information-theorists, they are of great interest to        ǫ. Thus, our discussion has implicitly subsumed that of
physicists, since they correspond, among other things, to           traditional time series modeling.
periodic and limit-cycle behaviors. There are, however,                Computational mechanics—in its focus on letting the
only two substantial differences between what is true               process speak for itself through (possibly impoverished)
of the infinite-entropy processes considered in the main            measurements—follows the spirit that motivated one ap-
body of the development and the finite-entropy case.                proach to experimentally testing dynamical systems the-
   First, we can simply replace statements of the form              ory. Specifically, it follows in spirit the methods of re-
                  →L               →                                constructing “geometry from a time series” introduced
“for all L, H[ S ] . . . ” with H[ S ]. For example, the            by Refs. [90] and [91]. A closer parallel is found, how-
optimal prediction theorem (Thm. 1) for finite-entropy              ever, in later work on estimating minimal equations of
                                   →           →
processes becomes for all R, H[ S |R] ≥ H[ S |S]. The               motion from data series [92].
details of the proofs are, however, entirely analogous.
   Second, we can prove a substantially stronger version
of the control theorem (Thm. 6).                                               2. Decision-Theoretic Problems

Theorem 7 (The Finite-Control Theorem) For all                         The classic focus of decision theory is “rules of induc-
prescient rivals R̂,                                                tive behavior” [93–95]. The problem is to chose functions
                   →      →
                                                                    from observed data to courses of action that possess de-
              H[ S ] − H[ S |R̂] ≤ Cµ .                (F1)         sirable properties. This task has obvious affinities to con-
                                                                    sidering the properties of ǫ and its rivals η. We can go
                                                                    further and say that what we have done is consider a de-
                                                                    cision problem, in which the available actions consist of
  Proof. By a direct application of Eq. (A9) and the                predictions about the future of the process. The calcu-
definition of mutual information Eq. (8), we have that              lation of the optimum rule of behavior in general faces
                  →      →                                          formidable technicalities, such as providing an estimate
              H[ S ] − H[ S |S] ≤ H[S] .               (F2)         of the utility of every different course of action under
                                                                    every different hypothesis about the relevant aspects of
                                                          →
But, by the definition of prescient rivals (Def. 11), H[ S          the world. On the one hand, it is not hard to concoct
         →                                                          time-series tasks where the optimal rule of behavior does
|S] = H[ S |R̂], and, by definition, Cµ = H[S]. Substi-
                                                                    not use ǫ at all. On the other hand, if we simply aim to
tuting equals for equals gives us the theorem. QED.
                                                                    predict the process indefinitely far into the future, then
                                                                    because the causal states are minimal sufficient statistics
APPENDIX G: RELATIONS TO OTHER FIELDS
                                                                    for the distribution of futures (Thm. 2, Remark 4), the
                                                                    optimal rule of behavior will use ǫ.


                                                               22
                3. Stochastic Processes                             amount and kind of memory available to the automata.
                                                                    The lowest level of the hierarchy is that of regular lan-
   Clearly, the computational mechanics approach to pat-            guages, which may be familiar to Unix-using readers as
terns and pattern discovery involves stochastic processes           regular expressions. These correspond to finite-state ma-
in an intimate and inextricable way. Probabilists have,             chines and to hidden Markov models of finite dimension.
of course, long been interested in using information-               In such cases, relatives of our minimality and unique-
theoretic tools to analyze stochastic processes, particu-           ness theorems are well known [66], and the construction
larly their ergodic behavior [59,96–98]. There has also             of causal states is analogous to the “Nerode equivalence
been considerable work in the hidden Markov model and               classing” procedure [66,109]. Our theorems, however, are
optimal prediction literatures on inferring models of pro-          not restricted to this low-memory, non-stochastic setting.
cesses from data or from given distributions [10,99–102].              The problem of learning a language from observational
To the best of our knowledge, however, these two ap-                data has been extensively studied by linguists, and by
proaches have not been previously combined.                         computer scientists interested in natural-language pro-
   Perhaps the closest approach to the spirit of compu-             cessing. Unfortunately, well developed learning tech-
tational mechanics in the stochastic process literature             niques exist only for the two lowest classes in the Chom-
is, surprisingly, the now-classical theory of optimal pre-          sky hierarchy, the regular and the context-free languages.
diction and filtering for stationary processes, developed           (For a good account of these procedures see Ref. [110].)
by Wiener and Kolmogorov [103–106]. The two theories                Adapting and extending this work to the reconstruction
share the use of information-theoretic notions, the uni-            of ǫ-machines should form a useful area of future research,
fication of prediction and structure, and the conviction            a point to which we alluded in the concluding remarks.
that “the statistical mechanics of time series” is a “field
in which conditions are very remote from those of the
statistical mechanics of heat engines and which is thus              5. Computational and Statistical Learning Theory
very well suited to serve as a model of what happens in
the living organism” [106, p. 59]. So far as we have been              The goal of computational learning theory [111,112] is
able to learn, however, no one has ever used this theory            to identify algorithms that quickly, reliably, and simply
to explicitly identify causal states and causal structure,          lead to good representations of a target “concept”. The
leaving these implicit in the mathematical form of the              latter is typically defined to be a binary dichotomy of
prediction and filtering operators. Moreover, the Wiener-           a certain feature or input space. Particular attention is
Kolmogorov framework forces us to sharply separate the              paid to results about “probably approximately correct”
linear and nonlinear aspects of prediction and filtering,           (PAC) procedures [113]: those having a high probabil-
because it has a great deal of trouble calculating non-             ity of finding members of a fixed “representation class”
linear operators [105]. Computational mechanics is com-             (e.g., neural nets, Boolean functions in disjunctive nor-
pletely indifferent to this issue, since it packs all of the        mal form, and deterministic finite automata). The key
process’s structure into the ǫ-machine, which is equally            word here is “fixed”; as in contemporary time-series anal-
calculable in linear or strongly nonlinear situations.              ysis, practitioners of this discipline acknowledge the im-
                                                                    portance of getting the representation class right. (Get-
                                                                    ting it wrong can make easy problems intractable.) In
   4. Formal Language Theory and Grammatical                        practice, however, they simply take the representation
                    Inference                                       class as a given, even assuming that we can always count
                                                                    on it having at least one representation which exactly cap-
   A formal language is a set of symbol strings (“words”            tures the target concept. Although this is in line with im-
or “allowed words”) drawn from a finite alphabet. Ev-               plicit assumptions in most of mathematical statistics, it
ery formal language may be described either by a set of             seems dubious when analyzing learning in the real world
rules (a “grammar”) for creating all and only the allowed           [5,114,115].
words, by an abstract automaton which also generates                   In any case, the preceding development made no such
the allowed words, or by an automaton which accepts                 assumption. One of the goals of computational mechan-
the allowed words and rejects all “forbidden” words. Our            ics is, exactly, discovering the best representation. This
ǫ-machines, stripped of probabilities, correspond to such           is not to say that the results of computational learning
automata—generative in the simple case or classificatory,           theory are not remarkably useful and elegant, nor that
if we add a reject state and move to it when none of the            one should not take every possible advantage of them
allowed symbols are encountered.                                    in implementing ǫ-machine reconstruction. In our view,
   Since Chomsky [107,108], it has been known that for-             though, these theories belong more to statistical infer-
mal languages can be classified into a hierarchy, the               ence, particularly to algorithmic parameter estimation,
higher levels of which have strictly greater expressive             than to foundational questions about the nature of pat-
power. The hierarchy is defined by restricting the form             tern and the dynamics of learning.
of the grammatical rules or, equivalently, by limiting the             Finally, in a sense computational mechanics’ focus on


                                                               23
causal states is a search for a particular kind of structural        entropy of the states used by some optimal predictor.
decomposition for a process. That decomposition is most              The same paper suggested that it could be approximated
directly reflected in the conditional independence of past           (from below) by the excess entropy; there called the ef-
and future that causal states induce. This decomposi-                fective measure complexity, as noted in Sec. VI above.
tion reminds one of the important role that conditional              This is a position closely allied to that of computational
independence plays in contemporary methods for artifi-               mechanics, to Rissanen’s MDL principle, and to the min-
cial intelligence, both for developing systems that rea-             imal embeddings introduced by the “geometry of a time
son in fluctuating environments [116] and the more re-               series” methods [90] just described.
cently developed algorithmic methods of graphical mod-                  In contrast to computational mechanics, however, the
els [117,118].                                                       key notion of “optimal prediction” was left undefined,
                                                                     as were the nature and construction of the states of the
                                                                     optimal predictor. In fact, the predictors used required
   6. Description-Length Principles and Universal                    knowing the process’s underlying equations of motion.
                   Coding Theory                                     Moreover, the statistical complexity Cµ (S) differs from
                                                                     the measure complexities in that it is based on the well
   Rissanen’s minimum description length (MDL) prin-                 defined causal states, whose optimal predictive powers
ciple, most fully described in Ref. [46], is a procedure             are in turn precisely defined. Thus, computational me-
for selecting the most concise generative model out of a             chanics is an operational and constructive formalization
family of models that are all statistically consistent with          of the insights expressed in Ref. [75].
given data. The MDL approach starts from Shannon’s re-
sults on the connection between probability distributions
and codes. Rissanen’s development follows the inductive                        8. Hierarchical Scaling Complexity
framework introduced by Solomonoff [43].
   Suppose we choose a representation that leads to a                   Introduced in Ref. [123, ch. 9], this approach seeks,
class M of models and are given data set X. The MDL                  like computational mechanics, to extend certain tradi-
principle enjoins us to pick the model M ∈ M that mini-              tional ideas of statistical physics. In brief, the method is
mizes the sum of the length of the description of X given            to construct a hierarchy of nth -order Markov models and
M, plus the length of description of M given M. The                  examine the convergence of their predictions with the real
description length of X is taken to be − log P(X|M);                 distribution of observables as n → ∞. The discrepancy
cf. Eq. (5). The description length of M may be regarded             between prediction and reality is, moreover, defined in-
as either given by some coding scheme or, equivalently, by           formation theoretically, in terms of the relative entropy
some distribution over the members of M. (Despite the                or Kullback-Leibler distance [62,71]. (We have not used
similarities to model estimation in a Bayesian framework             this quantity.) The approach implements Weiss’s dis-
[119], Rissanen does not interpret this distribution as a            covery that for finite-state sources there is a structural
Bayesian prior or regard description length as a measure             distinction between block-Markovian sources (subshifts
of evidential support.)                                              of finite type) and sofic systems. Weiss showed that, de-
   The construction of causal states is somewhat simi-               spite their finite memory, sofic systems are the limit of
lar to the states estimated in Rissanen’s context algo-              an infinite series of increasingly larger block-Markovian
rithm [46,120] (and to the “vocabularies” built by uni-              sources [124].
versal coding schemes, such as the popular Lempel-Ziv                   The hierarchical-scaling-complexity approach has sev-
algorithm [121,122]). Despite the similarities, there are            eral advantages, particularly its ability to handle issues
significant differences. For a random source—for which               of scaling in a natural way (see Ref. [123, sec. 9.5]).
there is a single causal state—the context algorithm es-             Nonetheless, it does not attain all the goals set in
timates a number of states that diverges (at least loga-             Sec. II F. Its Markovian predictors are so many black
rithmically) with the length of the data stream, rather              boxes, saying little or nothing about the hidden states
than inferring a single state, as ǫ-machine reconstruction           of the process, their causal connections, or the intrin-
would. Moreover, we avoid any reference to encodings of              sic computation carried on by the process. All of these
rival models or to prior distributions over them; Cµ (R)             properties, as we have shown, are manifest from the ǫ-
is not a description length.                                         machine. We suggest that a productive line of future
                                                                     work would be to investigate the relationship between
                                                                     hierarchical scaling complexity and computational me-
                7. Measure Complexity                                chanics, and to see whether they can be synthesized.
                                                                     Along these lines, hierarchical scaling complexity reminds
  Ref. [75] proposed that the appropriate measure of the             us somewhat of hierarchical ǫ-machine reconstruction de-
complexity of a process was the “minimal average Shan-               scribed in Ref. [5].
non information needed” for optimal prediction. This
true measure complexity was to be taken as the Shannon


                                                                24
         9. Continuous Dynamical Computing                             [11] James P. Crutchfield and Melanie Mitchell. The evolu-
                                                                            tion of emergent computation. Proceedings of the Na-
   Using dynamical systems as computers has become in-                      tional Academy of Sciences, 92:10742–10746, 1995.
creasingly attractive over the last ten years or so among              [12] A. Witt, A. Neiman, and J. Kurths. Characterizing the
                                                                            dynamics of stochastic bistable systems by measures of
physicists, computer scientists, and others exploring the
                                                                            complexity. Physical Review E, 55:5050–5059, 1997.
physical basis of computation [125–128]. These propos-
                                                                       [13] Jordi Delgado and Ricard V. Solé. Collective-induced
als have ranged from highly abstract ideas about how to
                                                                            computation. Physical Review E, 55:2338–2344, 1997.
embed Turing machines in discrete-time nonlinear con-                  [14] W. M. Gonçalves, R. D. Pinto, J. C. Sartorelli, and M. J.
tinuous maps [7,129] to, more recently, schemes for spe-                    de Oliveira. Inferring statistical complexity in the drip-
cialized numerical computation that could in principle                      ping faucet experiment. Physica A, 257:385–389, 1998.
be implemented in current hardware [130]. All of them,                 [15] James P. Crutchfield and Cosma Rohilla Shalizi. Ther-
however, have been synthetic, in the sense that they con-                   modynamic depth of causal states: Objective com-
cern designing dynamical systems that implement a given                     plexity via minimal representations. Physical Review E,
desired computation or family of computations. In con-                      59:275–283, 1999.
trast, one of the central questions of computational me-               [16] Jorge Luis Borges. Other Inquisitions, 1937–1952. Uni-
chanics is exactly the converse: given a dynamical sys-                     versity of Texas Press, Austin, 1964. Trans. Ruth L. C.
tem, how can one detect what it is intrinsically comput-                    Simms.
ing?                                                                   [17] James P. Crutchfield. Semantics and thermodynamics.
   We believe that having a mathematical basis and a                        In Martin Casdagli and Stephen Eubank, editors, Non-
set of tools for answering this question are important to                   linear Modeling and Forecasting, volume 12 of Santa
the synthetic, engineering approach to dynamical com-                       Fe Institute Studies in the Sciences of Complexity,
puting. Using these tools we may be able to discover, for                   pages 317–359, Reading, Massachusetts, 1992. Addison-
example, novel forms of computation embedded in nat-                        Wesley.
ural processes that operate at higher speeds, with less                [18] Plato. Phaedrus.
energy, and with fewer physical degrees of freedom than                [19] A. R. Luria. The Working Brain: An Introduction to
currently possible.                                                         Neuropsychology. Basic Books, New York, 1973.
                                                                       [20] Norma Van Surdam Graham. Visual Pattern Analyzers,
                                                                            volume 16 of Oxford Psychology Series. Oxford Univer-
                                                                            sity Press, Oxford, 1989.
                                                                       [21] Sara J. Shettleworth. Cognition, Evolution and Behav-
                                                                            ior. Oxford University Press, Oxford, 1998.
                                                                       [22] Julius T. Tou and Rafael C. Gonzalez. Pattern Recogni-
                                                                            tion Principles. Addison-Wesley, Reading, Mass, 1974.
  [1] Julia M. Yeomans. Statistical Mechanics of Phase Tran-
                                                                       [23] Stephen P. Banks. Signal Processing, Image Processing,
      sitions. Clarendon Press, Oxford, 1992.
                                                                            and Pattern Recognition. Prentice Hall, New York, 1990.
  [2] Paul Manneville. Dissipative Structures and Weak Tur-
                                                                       [24] Jae S. Lim. Two-Dimensional Signal and Image Pro-
      bulence. Academic Press, Boston, Massachusetts, 1990.
                                                                            cessing. Prentice Hall, New York, 1990.
  [3] P. M. Chaikin and T. C. Lubensky. Principles of Con-
                                                                       [25] Plato. Meno. In Sec. 80D Meno says: “How will you
      densed Matter Physics. Cambridge University Press,
                                                                            look for it, Socrates, when you do not know at all what
      Cambridge, England, 1995.
                                                                            it is? How will you aim to search for something you do
  [4] Mark C. Cross and Pierre Hohenberg. Pattern Forma-
                                                                            not know at all? If you should meet it, how will you
      tion Out of Equilibrium. Reviews of Modern Physics,
                                                                            know that this is the thing that you did not know?”
      65:851–1112, 1993.
                                                                            The same difficulty is raised in Theaetetus, Sec. 197 et
  [5] James P. Crutchfield. The calculi of emergence: Compu-
                                                                            seq.
      tation, dynamics, and induction. Physica D, 75:11–54,
                                                                       [26] Alfred North Whitehead and Bertrand Russell. Prin-
      1994.
                                                                            cipia Mathematica. Cambridge University Press, Cam-
  [6] James P. Crutchfield and Karl Young. Inferring statis-
                                                                            bridge, England, 2nd edition, 1925–27.
      tical complexity. Physical Review Letters, 63:105–108,
                                                                       [27] Bertrand Russell. Introduction to Mathematical Philoso-
      1989.
                                                                            phy. The Muirhead Library of Philosophy. George Allen
  [7] James P. Crutchfield and Karl Young. Computation at
                                                                            and Unwin, London, revised edition, 1920. First edition,
      the onset of chaos. In Zurek [131], pages 223–269.
                                                                            1919. Reprinted New York: Dover Books, 1993.
  [8] Nicolás Perry and P.-M. Binder. Finite statistical com-
                                                                       [28] James P. Crutchfield. Information and its metric. In
      plexity for sofic systems. Physical Review E, 60:459–463,
                                                                            L. Lam and H. C. Morris, editors, Nonlinear Struc-
      1999.
                                                                            tures in Physical Systems—Pattern Formation, Chaos
  [9] James E. Hanson and James P. Crutchfield. Compu-
                                                                            and Waves, page 119, New York, 1990. Springer-Verlag.
      tational mechanics of cellular automata: An example.
                                                                       [29] Bertrand Russell. Human Knowledge: Its Scope and
      Physica D, 103:169–189, 1997.
                                                                            Limits. Simon and Schuster, New York, 1948.
 [10] Daniel R. Upper. Theory and Algorithms for Hidden
                                                                       [30] John Rhodes. Applications of Automata Theory and Al-
      Markov Models and Generalized Hidden Markov Models.
                                                                            gebra via the Mathematical Theory of Complexity to
      PhD thesis, University of California, Berkeley, 1997.


                                                                  25
     Biology, Physics, Psychology, Philosophy, Games, and              [47] Charles H. Bennett. How to define complexity in
     Codes. University of California, Berkeley, California,                 physics, and why. In Zurek [131], pages 137–148.
     1971.                                                             [48] Moshe Koppel. Complexity, depth, and sophistication.
[31] Chrystopher L. Nehaniv and John L. Rhodes. Krohn-                      Complex Systems, 1:1087–1091, 1987.
     Rhodes theory, hierarchies, and evolution. In Boris               [49] Moshe Koppel and Henri Atlan. An almost machine-
     Mirkin, F. R. McMorris, Fred S. Roberts, and Andrey                    independent theory of program-length complexity,
     Rzhetsky, editors, Mathematical Hierarchies and Biol-                  sophistication and induction. Information Sciences,
     ogy: DIMACS workshop, November 13–15, 1996, vol-                       56:23–44, 1991.
     ume 37 of DIMACS Series in Discrete Mathematics and               [50] Daniel C. Dennett. Real patterns. Journal of Philoso-
     Theoretical Computer Science, Providence, Rhode Is-                    phy, 88:27–51, 1991. Reprinted in Dennett (1997).
     land, 1997. American Mathematical Society.                        [51] James P. Crutchfield. Is anything ever new? Consider-
[32] Ulf Grenander. Elements of Pattern Theory. Johns Hop-                  ing emergence. In G. Cowan, D. Pines, and D. Melzner,
     kins Studies in the Mathematical Sciences. Johns Hop-                  editors, Complexity: Metaphors, Models, and Reality,
     kins University Press, Baltimore, Maryland, 1996.                      volume 19 of Santa Fe Institute Studies in the Sciences
[33] Ulf Grenander, Y. Chow, and D. M. Keenan. Hands:                       of Complexity, pages 479–497, Reading, Massachusetts,
     A Pattern Theoretic Study of Biological Shapes, vol-                   1994. Addison-Wesley.
     ume 2 of Research Notes in Neural Computing. Springer-            [52] John H. Holland. Emergence: From Chaos to Order.
     Verlag, New York, 1991.                                                Addison-Wesley, Reading, Massachusetts, 1998.
[34] Ulf Grenander and K. Manbeck. A stochastic shape and              [53] Ludwig Boltzmann. Lectures on Gas Theory. University
     color model for defect detection in potatoes. American                 of California Press, Berkeley, 1964.
     Statistical Association, 2:131–151, 1993.                         [54] Harald Cramér. Mathematical Methods of Statistics.
[35] A. N. Kolmogorov. Three approaches to the quantita-                    Almqvist and Wiksells, Uppsala, 1945. Republished by
     tive definition of information. Problems of Information                Princeton University Press, 1946, as vol. 9 in the Prince-
     Transmission, 1:1–7, 1965.                                             ton Mathematics Series, and as a paperback, in the
[36] Gregory Chaitin. On the length of programs for comput-                 Princeton Landmarks in Mathematics and Physics se-
     ing finite binary sequences. Journal of the Association                ries, 1999.
     for Computing Machinery, 13:547–569, 1966.                        [55] Claude E. Shannon. A mathematical theory of com-
[37] A. N. Kolmogorov. Combinatorial foundations of infor-                  munication. Bell System Technical Journal, 27:379–423,
     mation theory and the calculus of probabilities. Russ.                 1948.
     Math. Surveys, 38:29, 1983.                                       [56] David Hume. A Treatise of Human Nature: Being an
[38] Ming Li and Paul M. B. Vitanyi. An Introduction to                     Attempt to Introduce the Experimental Method of Rea-
     Kolmogorov Complexity and its Applications. Springer-                  soning into Moral Subjects. John Noon, London, 1739.
     Verlag, New York, 1993.                                                Reprint (Oxford: Clarendon Press, 1951) of original edi-
[39] Marvin Minsky. Computation: Finite and Infinite Ma-                    tion, with notes and analytical index.
     chines. Prentice-Hall, Englewood Cliffs, New Jersey,              [57] Mario Bunge. Causality: The Place of the Causal Princ-
     1967.                                                                  ple in Modern Science. Harvard University Press, Cam-
[40] P. Martin-Löf. The definition of random sequences. In-                bridge, Massachusetts, 1959. Reprinted as Causality and
     formation and Control, 9:602–619, 1966.                                Modern Science, NY: Dover Books, 1979.
[41] L. A. Levin. Laws of information conservation (non-               [58] Wesley C. Salmon. Scientific Explanation and the
     growth) and aspects of the foundation of probability                   Causal Structure of the World. Princeton University
     theory. Problemy Peredachi Informatsii, 10:30–35, 1974.                Press, Princeton, 1984.
     Translation: Problems of Information Transmission 10              [59] Patrick Billingsley. Ergodic Theory and Information.
     (1974) 206–210.                                                        Tracts on Probablity and Mathematical Statistics. Wi-
[42] V. G. Gurzadyan. Kolmogorov complexity as a descrip-                   ley, New York, 1965.
     tor of cosmic microwave background maps. Europhysics              [60] Patrick Billingsley. Probability and Measure. Wiley Se-
     Letters, 46:114–117, 1999. Also available as an electronic             ries in Probability and Mathematical Statistics. Wiley,
     preprint, LANL archive, astro-phy/9902123.                             New York, 1979.
[43] Raymond J. Solomonoff. A formal theory of inductive               [61] Bernard F. Schutz. Geometrical Methods of Mathemat-
     inference. Information and Control, 7:1–22 and 224–254,                ical Physics. Cambridge University Press, Cambridge,
     1964.                                                                  England, 1980.
[44] Paul Vitányi and Ming Li. Minimum description length             [62] Thomas M. Cover and Joy A. Thomas. Elements of In-
     induction, Bayesianism, and Kolmogorov complexity.                     formation Theory. Wiley, New York, 1991.
     Electronic pre-print, LANL Archive, cs.LG/9901014,                [63] William of Ockham. Philosophical Writings: A Selec-
     1999.                                                                  tion, Translated, with an Introduction, by Philotheus
[45] Gary William Flake. The Computational Beauty of Na-                    Boehner, O.F.M., Late Professor of Philosophy, The
     ture: Computer Explorations of Fractals, Chaos, Com-                   Franciscan Institute. Bobbs-Merrill, Indianapolis, 1964.
     plex Systems and Adaptation. MIT Press, Cambridge,                     first pub. various European cities, early 1300s.
     Massachusetts, 1998.                                              [64] Anonymous. Kuan Yin Tzu, T’ang Dynasty. Written
[46] Jorma Rissanen. Stochastic Complexity in Statistical In-               in China during the T’ang dynasty. Partial translation
     quiry. World Scientific, Singapore, 1989.                              in Joseph Needham, Science and Civilisation in China,


                                                                  26
     vol. II (Cambridge University Press, 1956), p. 73.                [84] David P. Feldman. Computational Mechanics of Clas-
[65] David P. Feldman and James P. Crutchfield. Dis-                        sical        Spin       Systems.         PhD        thesis,
     covering non-critical organization: Statistical me-                    University of California, Davis, 1998. Available on-line
     chanical, information theoretic, and computational                     at http://hornacek.coa.edu/dave/Thesis/thesis.html.
     views of patterns in simple one-dimensional spin                  [85] Deborah Mayo. Error and the Growth of Experimen-
     systems. Journal of Statistical Physics, submitted,                    tal Knowledge. Science and Its Conceptual Foundations.
     1998. Santa Fe Institute Working Paper 98-04-026,                      University of Chicago Press, Chicago, 1996.
     http://www.santafe.edu/projects/CompMech/ papers/                 [86] James P. Crutchfield and Cristopher Douglas. Imagined
     DNCO.html.                                                             complexity: Learning a random process. in preparation,
[66] John E. Hopcroft and Jeffrey D. Ullman. Introduc-                      1999.
     tion to Automata Theory, Languages, and Computation.              [87] Rudolf Lidl and Gunter Pilz. Applied Abstract Algebra.
     Addison-Wesley, Reading, 1979. 2nd edition of Formal                   Springer, New York, 1984.
     Languages and Their Relation to Automata, 1969.                   [88] E. S. Ljapin. Semigroups, volume 3 of Translations of
[67] John G. Kemeny and J. Laurie Snell. Finite Markov                      Mathematical Monographs. American Mathematical So-
     Chains. Springer-Verlag, New York, 1976.                               ciety, Providence, Rhode Island, 1963.
[68] John G. Kemeny, J. Laurie Snell, and Anthony W.                   [89] Karl Young. The Grammar and Statistical Mechanics
     Knapp. Denumerable Markov Chains. Springer-Verlag,                     of Complex Physical Systems. PhD thesis, University of
     New York, 2nd edition, 1976.                                           California, Santa Cruz, 1991.
[69] James E. Hanson. Computational Mechanics of Cellular              [90] Norman H. Packard, James P. Crutchfield, J. Doyne
     Automata. PhD thesis, University of California, Berke-                 Farmer, and Robert S. Shaw. Geometry from a time
     ley, 1993.                                                             series. Physical Review Letters, 45:712–716, 1980.
[70] Gregory Bateson. Mind and Nature: A Necessary Unity.              [91] Floris Takens. Detecting strange attractors in fluid tur-
     E. P. Dutton, New York, 1979.                                          bulence. In D. A. Rand and L. S. Young, editors, Sym-
[71] Solomon Kullback. Information Theory and Statistics.                   posium on Dynamical Systems and Turbulence, volume
     Dover Books, New York, 2nd edition, 1968. First edition                898 of Lecture Notes in Mathematics, page 366, Berlin,
     New York: Wiley, 1959.                                                 1981. Springer-Verlag.
[72] Claude Bernard. Introduction a l’etude de la medecine             [92] James P. Crutchfield and Bruce S. McNamara. Equa-
     experimentale. J. B. Bailliere, Paris, 1865. Trans. by                 tions of motion from a data series. Complex Systems,
     Henry Copley Green as Introduction to the Study of                     1:417–452, 1987.
     Experimental Medicine, New York: Macmillian, 1927;                [93] Jerzy Neyman. First Course in Probability and Statis-
     reprinted New York: Dover, 1957.                                       tics. Henry Holt, New York, 1950.
[73] James P. Crutchfield and Norman H. Packard. Symbolic              [94] David Blackwell and M. A. Girshick. Theory of Games
     dynamics of noisy chaos. Physica D, 7:201–223, 1983.                   and Statistical Decisions. Wiley, New York, 1954.
[74] Robert Shaw. The Dripping Faucet as a Model Chaotic                    Reprinted New York: Dover Books, 1979.
     System. Aerial Press, Santa Cruz, California, 1984.               [95] R. Duncan Luce and Howard Raiffa. Games and De-
[75] Peter Grassberger. Toward a quantitative theory of self-               cisions: Introduction and Critical Survey. Wiley, New
     generated complexity. International Journal of Theoret-                York, 1957.
     ical Physics, 25:907–938, 1986.                                   [96] I. M. Gel’fand and A. M. Yaglom. Calculation of the
[76] Kristian Lindgren and Mats G. Nordahl. Complex-                        amount of information about a random function con-
     ity measures and cellular automata. Complex Systems,                   tained in another such function. Uspekhi Matematich-
     2:409–440, 1988.                                                       eski Nauk, 12:3–52, 1956. Trans. in American Math-
[77] W. Li. On the relationship between complexity and en-                  ematical Society Translations, 2nd series, 12 (1959):
     tropy for Markov chains and regular languages. Complex                 199–246.
     Systems, 5:381–399, 1991.                                         [97] Peter E. Caines. Linear Stochastic Systems. Wiley, New
[78] Dirk Arnold. Information-theoretic analysis of phase                   York, 1988.
     transitions. Complex Systems, 10:143–155, 1996.                   [98] Robert M. Gray. Entropy and Information Theory.
[79] William Bialek and Naftali Tishby. Predictive infor-                   Springer-Verlag, New York, 1990.
     mation. Electronic pre-print, LANL archive, cond-                 [99] David Blackwell and Lambert Koopmans. On the iden-
     mat/9902341, 1999.                                                     tifiability problem for functions of finite Markov chains.
[80] James P. Crutchfield and David P. Feldman. Statisti-                   Annals of Mathematical Statistics, 28:1011–1015, 1957.
     cal complexity of simple one-dimensional spin systems.           [100] H. Ito, S.-I. Amari, and K. Kobayashi. Identifiability of
     Physical Review E, 55:1239R–1243R, 1997.                               hidden Markov information sources and their minimum
[81] W. Ross Ashby. An Introduction to Cybernetics. Chap-                   degrees of freedom. IEEE Transactions on Information
     man and Hall, London, 1956.                                            Theory, 38:324–333, 1992.
[82] Hugo Touchette and Seth Lloyd. Information-theoretic             [101] H. Jaeger. Observable operator models for discrete
     limits of control. Physical Review Letters, 84:1156–1159,              stochastic time series. Neural Computation, forth-
     1999.                                                                  coming, 1999. ftp://ftp.gmd.de/GMD/ais/ publica-
[83] Abraham Lempel and Jacob Ziv. Compression of two-                      tions/1999/.
     dimensional data. IEEE Transactions in Information               [102] Paul Algoet. Universal schemes for prediction, gam-
     Theory, IT-32:2–8, 1986.                                               bling and portfolio selection. The Annals of Probability,


                                                                 27
      20:901–941, 1992. See also an important Correction, The            [121] Abraham Lempel and Jacob Ziv. On the complexity
      Annals of Probability, 23 (1995): 474–478.                               of finite sequences. IEEE Transactions in Information
[103] A. N. Kolmogorov. Interpolation und extrapolation von                    Theory, IT-22:75–81, 1976.
      stationären zufälligen folgen. Bull. Acad. Sci. U.S.S.R.,        [122] Jacob Ziv and Abraham Lempel. A universal algorithm
      Math., 3:3–14, 1941. In German.                                          for sequential data compression. IEEE Transactions in
[104] Norbert Wiener. Extrapolation, Interpolation, and                        Information Theory, IT-23:337–343, 1977.
      Smoothing of Stationary Time Series: With Engineer-                [123] Remo Badii and Antonio Politi. Complexity: Hierarchi-
      ing Applications. The Technology Press of the Mas-                       cal Structures and Scaling in Physics, volume 6 of Cam-
      sachusetts Institute of Technology, Cambridge, Mas-                      bridge Nonlinear Science Series. Cambridge University
      sachusetts, 1949. “First published during the war as                     Press, Cambridge, 1997.
      a classifed report to Section D2 , National Defense Re-            [124] Benjamin Weiss. Subshifts of finite type and sofic sys-
      search Council”.                                                         tems. Monatshefte für Mathematik, 77:462–474, 1973.
[105] Norbert Wiener. Nonlinear Problems in Random The-                  [125] Cristopher Moore. Recursion theory on the reals and
      ory. The Technology Press of the Massachusetts Insti-                    continuous-time computation. Theoretical Computer
      tute of Technology, Cambridge, Massachusetts, 1958.                      Science, 162:23–44, 1996.
[106] Norbert Wiener. Cybernetics: Or, Control and Com-                  [126] Cristopher Moore. Dynamical recognizers: Real-time
      munication in the Animal and the Machine. MIT Press,                     language recognition by analog computers. Theoretical
      Cambridge, Massachusetts, 2nd edition, 1961. First edi-                  Computer Science, 201:99–136, 1998.
      tion New York: Wiley, 1948.                                        [127] Pekka Orponen. A survey of continuous-time computa-
[107] Noam Chomsky. Three models for the description of lan-                   tion theory. In D.-Z. Du and K.-I Ko, editors, Advances
      guage. IRE Transactions on Information Theory, 2:113,                    in Algorithms, Languages, and Complexity, pages 209–
      1956.                                                                    224. Kluwer Academic, Dordrecht, 1997.
[108] Noam Chomsky. Syntactic Structures, volume 4 of                    [128] Lenore Blum, Michael Shub, and Steven Smale. On a
      Janua linguarum, series minor. Mouton, The Hauge,                        theory of computation and complexity over the real
      1957.                                                                    numbers: NP-completeness, recursive functions and
[109] B. A. Trakhtenbrot and Ya. M. Barzdin. Finite Au-                        universal machines. Bulletin of the American Mathe-
      tomata. North-Holland, Amsterdam, 1973.                                  matical Society, 21:1–46, 1989.
[110] Eugene Charniak. Statistical Language Learning. Lan-               [129] Cristopher Moore. Unpredictability and undecidability
      guage, Speech and Communication. MIT Press, Cam-                         in dynamical systems. Physical Review Letters, 64:2354–
      bridge, Massachusetts, 1993.                                             2357, 1990.
[111] Michael J. Kearns and Umesh V. Vazirani. An Intro-                 [130] Sudeshna Sinha and William L. Ditto. Dynamics based
      duction to Computational Learning Theory. MIT Press,                     computation. Physical Review Letters, 81:2156–2159,
      Cambridge, Massachusetts, 1994.                                          1998.
[112] V. N. Vapnik. The Nature of Statistical Learning The-              [131] Wojciech H. Zurek, editor. Complexity, Entropy, and
      ory. Springer-Verlag, Berlin, 2nd edition, 2000.                         the Physics of Information, volume 8 of Santa Fe In-
[113] Leslie G. Valiant. A theory of the learnable. Commu-                     stitute Studies in the Sciences of Complexity, Reading,
      nications of the Association for Computing Machinery,                    Massachusetts, 1990. Addison-Wesley.
      27:1134–1142, 1984.
[114] Margaret A. Boden. Precis of The Creative Mind:
      Myths and Mechanisms. Behaviorial and Brain Sciences,
      17:519–531, 1994.
[115] Chris Thornton. Truth from Trash: How Learning
      Makes Sense. Complex Adaptive Systems. MIT Press,
      Cambridge, Massachusetts, 2000.
[116] Judea Pearl. Causality: Models, Reasoning, and Infer-
      ence. Cambridge University Press, Cambridge, England,
      2000.
[117] M. I. Jordan, editor. Learning in Graphical Models, vol-
      ume 89 of NATO Science Series D: Behavioral and So-
      cial Sciences, Dordrecht, 1998.
[118] Peter Spirtes, Clark Glymour, and Richard Scheines.
      Causation, Prediction, and Search. Adaptive Compu-
      tation and Machine Learning. MIT Press, Cambridge,
      Massachusetts, 2000.
[119] David V. Lindley. Bayesian Statistics, a Review. Society
      for Industrial and Applied Mathematics, Philadelphia,
      1972.
[120] Jorma Rissanen. Universal coding, information, predic-
      tion, and estimation. IEEE Transactions in Information
      Theory, IT-30:629–636, 1984.


                                                                    28
                                     APPENDIX: GLOSSARY OF NOTATION

In the order of their introduction.

Symbol      Description                                               Where Introduced
  O         Object in which we wish to find a pattern                 Sec. II, p. 3
  P         Pattern in O                                              Sec. II, p. 3
  A         Countable alphabet                                        Sec. III A, p. 6
   ↔
   S        Bi-infinite, stationary, discrete stochastic process on A Def. 1, p. 6
   ↔                                  ↔
   s        Particular realization of S                               Def. 1, p. 6
   →L                                                    ↔
   S        Random variable for the next L values of S                Sec. III A, p. 6
  →L                            →L
   s        Particular value of S                                     Sec. III A, p. 6
   →1                                          ↔
   S        Next observable generated by S                            Sec. III A, p. 6
   ←L          →L
   S        As S , but for the last L values, up to the present       Sec. III A, p. 6
  ←L                            ←L
   s        Particular value of S                                     Sec. III A, p. 6
   →                                       ↔
   S        Semi-infinite future half of S                            Sec. III A, p. 6
   →                            →
   s        Particular value of S                                     Sec. III A, p. 6
   ←                                  ↔
   S        Semi-infinite past half of S                              Sec. III A, p. 6
   ←                            ←
   s        Particular value of S                                     Sec. III A, p. 6
   λ        Null string or null symbol                                Sec. III A, p. 6
   ←                                                ↔
   S        Set of all pasts realized by the process S                Sec. III B, p. 6
                        ←
   R        Partition of S into effective states                      Sec. III B, p. 6
   ρ        Member-class of R; a particular effective state           Sec. III B, p. 6
                            ←
   η     Function from S to R                                         Sec. III B, Eq. (4), p. 6
  R      Current effective (η) state, as a random variable            Sec. III B, p. 6
  R′     Next effective state, as a random variable                   Sec. III B, p. 6
 H[X] Entropy of the random variable X                                Sec. III C 1, p. 7
H[X, Y ] Joint entropy of the random variables X and Y                Sec. III C 2, p. 7
H[X|Y ] Entropy of X conditioned on Y                                 Sec. III C 2, p. 7
I[X; Y ] Mutual information of X and Y                                Sec. III C 3, p. 7
       →                    →
 hµ [ S ]   Entropy rate of S                                         Sec. III D, Eq. (9), p. 8
   →                        →
hµ [ S |X] Entropy rate of S conditioned on X                         Sec. III D, Eq. (10), p. 8
 Cµ (R) Statistical complexity of R                                   Def. 4, p. 8
                                          ↔
   S        Set of the causal states of S                             Def. 5, p. 9
    σ       Particular causal state                                   Def. 5, p. 9
    ǫ       Function from histories to causal states                  Def. 5, p. 9
    S       Current causal state, as a random variable                Def. 5, p. 9
   S′       Next causal state, as a random variable                   Def. 5, p. 9
   ∼ǫ       Relation of causal equivalence between two histories      Sec. IV A, p. 9
    (s)
  Tij       Probability of going from causal state i to j, emitting s Def. 8, p. 11
   R̂       Set of prescient rival states                             Def. 11, p. 14
    ρ̂      Particular prescient rival state                          Def. 11, p. 14
   R̂       Current prescient rival state, as a random variable       Def. 11, p. 14
   R̂′      Next prescient rival state, as a random variable          Def. 11, p. 14
 Cµ (O)     Statistical complexity of the process O                   Def. 12, p. 15
  Cµ        Without an argument, short for Cµ (O)                     Def. 12, p. 15
   E        Excess entropy                                            Def. 13, p. 16


                                                             29
