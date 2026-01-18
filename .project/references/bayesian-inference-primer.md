# Bayesian Inference Primer

*A ground-up introduction to the probability theory underlying Bayesian Structural Inference (BSI) for epsilon-machine learning.*

---

## Table of Contents

1. [What Is Probability?](#chapter-1-what-is-probability)
2. [Probability Distributions](#chapter-2-probability-distributions)
3. [Multiple Trials](#chapter-3-multiple-trials)
4. [The Binomial Distribution](#chapter-4-the-binomial-distribution)
5. [The Multinomial Distribution](#chapter-5-more-than-two-outcomes--the-multinomial)
6. [Unknown Probabilities](#chapter-6-the-big-question--unknown-probabilities)
7. [Bayes' Theorem](#chapter-7-bayes-theorem--the-update-rule)
8. [A Concrete Example](#chapter-8-a-concrete-example)
9. [The Beta Distribution](#chapter-9-the-beta-distribution)
10. [Conjugate Priors](#chapter-10-conjugate-priors--the-magic-trick)
11. [From Beta to Dirichlet](#chapter-11-from-beta-to-dirichlet)
12. [Application to BSI](#chapter-12-why-this-matters-for-bsi)
13. [What Is Sampling?](#chapter-13-what-is-sampling)
14. [Monte Carlo Methods](#chapter-14-monte-carlo-methods)
15. [MCMC](#chapter-15-markov-chain-monte-carlo-mcmc)
16. [Gibbs Sampling](#chapter-16-gibbs-sampling--a-specific-mcmc-method)
17. [Applying to BSI](#chapter-17-applying-to-bsi)
18. [Model Selection](#chapter-18-model-selection--choosing-the-number-of-states)

---

## Chapter 1: What Is Probability?

### The Basics

A **probability** is a number between 0 and 1 that measures how likely something is to happen.

- 0 = impossible
- 1 = certain
- 0.5 = equally likely to happen or not

**Example**: Flip a fair coin.
- P(heads) = 0.5
- P(tails) = 0.5

These must add up to 1 (something has to happen):

$$P(\text{heads}) + P(\text{tails}) = 0.5 + 0.5 = 1$$

---

## Chapter 2: Probability Distributions

### A Distribution Over Outcomes

A **probability distribution** assigns a probability to each possible outcome.

**Example 1: Fair coin**

| Outcome | Probability |
|---------|-------------|
| Heads | 0.5 |
| Tails | 0.5 |

**Example 2: Biased coin** (lands heads 70% of the time)

| Outcome | Probability |
|---------|-------------|
| Heads | 0.7 |
| Tails | 0.3 |

**Example 3: Six-sided die**

| Outcome | Probability |
|---------|-------------|
| 1 | 1/6 |
| 2 | 1/6 |
| 3 | 1/6 |
| 4 | 1/6 |
| 5 | 1/6 |
| 6 | 1/6 |

**Key rule**: All probabilities must sum to 1.

---

## Chapter 3: Multiple Trials

### Independent Events

If I flip a coin twice, and the flips don't affect each other, they're **independent**.

For independent events, we **multiply** probabilities:

$$P(\text{heads, then heads}) = P(\text{heads}) \times P(\text{heads}) = 0.5 \times 0.5 = 0.25$$

**Example**: Flip a fair coin 3 times. What's the probability of HHH?

$$P(HHH) = 0.5 \times 0.5 \times 0.5 = 0.5^3 = 0.125$$

### Counting Outcomes

If I flip a coin 3 times, how many ways can I get exactly 2 heads?

Let's list them: HHT, HTH, THH — that's 3 ways.

In general, the number of ways to choose $k$ successes from $n$ trials is the **binomial coefficient**:

$$\binom{n}{k} = \frac{n!}{k!(n-k)!}$$

where $n! = n \times (n-1) \times (n-2) \times \cdots \times 2 \times 1$ ("n factorial")

**Example**:

$$\binom{3}{2} = \frac{3!}{2! \cdot 1!} = \frac{6}{2 \cdot 1} = 3 \checkmark$$

---

## Chapter 4: The Binomial Distribution

### Counting Heads in Many Flips

If I flip a biased coin (probability $p$ of heads) $n$ times, what's the probability of getting exactly $k$ heads?

$$P(k \text{ heads}) = \binom{n}{k} p^k (1-p)^{n-k}$$

Let's unpack this:
- $\binom{n}{k}$ = number of ways to arrange $k$ heads in $n$ flips
- $p^k$ = probability of those $k$ heads occurring
- $(1-p)^{n-k}$ = probability of the remaining $n-k$ tails

**Example**: Flip a fair coin ($p = 0.5$) 4 times. P(exactly 2 heads)?

$$P(2) = \binom{4}{2} (0.5)^2 (0.5)^2 = 6 \times 0.25 \times 0.25 = 0.375$$

---

## Chapter 5: More Than Two Outcomes — The Multinomial

### Generalizing Beyond Coins

A coin has 2 outcomes. What about a die with 6? Or an alphabet with 3 symbols {A, B, C}?

The **multinomial distribution** handles this.

Suppose we have $K$ outcomes with probabilities $(\theta_1, \theta_2, \ldots, \theta_K)$ where $\sum_{k=1}^{K} \theta_k = 1$.

After $n$ trials, the probability of seeing counts $(c_1, c_2, \ldots, c_K)$ is:

$$P(c_1, \ldots, c_K) = \frac{n!}{c_1! c_2! \cdots c_K!} \theta_1^{c_1} \theta_2^{c_2} \cdots \theta_K^{c_K}$$

The term $\frac{n!}{c_1! c_2! \cdots c_K!}$ is the **multinomial coefficient** — it counts how many ways to arrange the outcomes.

**Example**: Roll a fair die 6 times. P(each number appears exactly once)?

All $\theta_k = 1/6$, all $c_k = 1$:

$$P = \frac{6!}{1!1!1!1!1!1!} \left(\frac{1}{6}\right)^6 = 720 \times \frac{1}{46656} = \frac{720}{46656} \approx 0.015$$

---

## Chapter 6: The Big Question — Unknown Probabilities

### Here's Where It Gets Interesting

So far, we've assumed we **know** the probabilities (like $p = 0.5$ for a fair coin).

But what if we **don't know** the coin's bias?

We flip it 10 times and see 7 heads, 3 tails. What is $p$?

### Two Schools of Thought

**Frequentist approach**:
- "The best estimate is $\hat{p} = 7/10 = 0.7$"
- Uses maximum likelihood estimation
- Gives a point estimate

**Bayesian approach**:
- "Let's describe our *uncertainty* about $p$ with a probability distribution"
- Before seeing data: we have a **prior** belief about $p$
- After seeing data: we update to a **posterior** belief about $p$
- Gives a full distribution, not just a point

---

## Chapter 7: Bayes' Theorem — The Update Rule

### The Most Important Formula

$$P(A \mid B) = \frac{P(B \mid A) \cdot P(A)}{P(B)}$$

In words: The probability of A given B equals the probability of B given A, times the prior probability of A, divided by the probability of B.

### The Notation

- $P(A \mid B)$ reads as "the probability of A given B" or "the probability of A conditional on B"
- The vertical bar means "given" or "assuming"

### Applied to Learning Parameters

Let $\theta$ be the unknown coin bias. We observe data $D$ (e.g., 7 heads in 10 flips).

$$P(\theta \mid D) = \frac{P(D \mid \theta) \cdot P(\theta)}{P(D)}$$

| Term | Name | Meaning |
|------|------|---------|
| $P(\theta \mid D)$ | **Posterior** | What we believe about $\theta$ after seeing data |
| $P(D \mid \theta)$ | **Likelihood** | How likely is the data if $\theta$ is the true value |
| $P(\theta)$ | **Prior** | What we believed about $\theta$ before seeing data |
| $P(D)$ | **Evidence** | Total probability of the data (normalizing constant) |

### The Intuition

- **Prior**: Your initial belief (maybe you think the coin is probably fair)
- **Likelihood**: How well does this hypothesis explain what you observed?
- **Posterior**: Your updated belief after seeing evidence

Strong evidence can overcome weak priors. Weak evidence barely moves strong priors.

---

## Chapter 8: A Concrete Example

### Learning a Coin's Bias

**Setup**:
- Unknown bias $\theta$ (between 0 and 1)
- Prior belief: the coin is probably fair, but we're not certain
- Data: we flip 10 times, see 7 heads

**Step 1: Choose a prior**

We need a probability distribution over $\theta \in [0, 1]$.

The simplest choice: **uniform prior** — all values equally likely.

$$P(\theta) = 1 \quad \text{for } \theta \in [0, 1]$$

This says "before seeing any data, I think any bias is equally plausible."

**Step 2: Write the likelihood**

Given $\theta$, the probability of 7 heads in 10 flips:

$$P(D \mid \theta) = \binom{10}{7} \theta^7 (1-\theta)^3$$

**Step 3: Apply Bayes' theorem**

$$P(\theta \mid D) \propto P(D \mid \theta) \cdot P(\theta) = \theta^7 (1-\theta)^3 \cdot 1$$

The $\propto$ means "proportional to" — we're ignoring constants that don't depend on $\theta$.

**Step 4: Recognize the shape**

The function $\theta^7 (1-\theta)^3$ has a special name — it's a **Beta distribution**!

---

## Chapter 9: The Beta Distribution

### A Distribution Over Probabilities

The **Beta distribution** is a probability distribution over values between 0 and 1. Perfect for representing uncertainty about a probability!

It has two parameters, $\alpha$ and $\beta$:

$$P(\theta \mid \alpha, \beta) = \frac{\Gamma(\alpha + \beta)}{\Gamma(\alpha)\Gamma(\beta)} \theta^{\alpha - 1} (1 - \theta)^{\beta - 1}$$

The gamma function $\Gamma$ is a generalization of factorial: $\Gamma(n) = (n-1)!$ for positive integers.

For our purposes, just remember:

$$\text{Beta}(\alpha, \beta) \propto \theta^{\alpha - 1} (1 - \theta)^{\beta - 1}$$

### Visualizing Different Betas

| $\alpha$ | $\beta$ | Shape | Interpretation |
|----------|---------|-------|----------------|
| 1 | 1 | Flat (uniform) | No preference, all values equally likely |
| 2 | 2 | Gentle hill centered at 0.5 | Slight preference for fairness |
| 5 | 5 | Peaked at 0.5 | Confident it's close to fair |
| 10 | 2 | Peaked near 1 | Confident it's biased toward heads |
| 2 | 10 | Peaked near 0 | Confident it's biased toward tails |
| 0.5 | 0.5 | U-shaped | Thinks it's probably extreme (near 0 or 1) |

### Key Properties

**Mean** (expected value):
$$E[\theta] = \frac{\alpha}{\alpha + \beta}$$

**Mode** (most likely value, for $\alpha, \beta > 1$):
$$\text{mode} = \frac{\alpha - 1}{\alpha + \beta - 2}$$

**Intuition**: Think of $\alpha$ as "imaginary heads seen" and $\beta$ as "imaginary tails seen."

- $\text{Beta}(1, 1)$: Seen 1 head, 1 tail → no information
- $\text{Beta}(10, 10)$: Seen 10 of each → fairly confident it's fair
- $\text{Beta}(100, 1)$: Seen 100 heads, 1 tail → very confident heads is likely

---

## Chapter 10: Conjugate Priors — The Magic Trick

### What "Conjugate" Means

A prior is **conjugate** to a likelihood if the posterior has the **same functional form** as the prior.

**For the coin problem**:
- Prior: $\theta \sim \text{Beta}(\alpha, \beta)$
- Likelihood: Binomial (coin flips)
- Posterior: $\theta \mid \text{data} \sim \text{Beta}(\alpha + \text{heads}, \beta + \text{tails})$

### Proof (Simple Version)

Prior: $P(\theta) \propto \theta^{\alpha - 1} (1-\theta)^{\beta - 1}$

Likelihood: $P(D \mid \theta) \propto \theta^h (1-\theta)^t$ where $h$ = heads, $t$ = tails

Posterior:
$$P(\theta \mid D) \propto P(D \mid \theta) \cdot P(\theta) \propto \theta^h (1-\theta)^t \cdot \theta^{\alpha-1}(1-\theta)^{\beta-1}$$

$$= \theta^{(\alpha + h) - 1} (1-\theta)^{(\beta + t) - 1}$$

This is $\text{Beta}(\alpha + h, \beta + t)$! ∎

### This Is Magical Because...

We don't need to do any calculus or numerical integration!

**The update rule is just**:

$$\boxed{\text{New pseudocounts} = \text{Old pseudocounts} + \text{Observed counts}}$$

**Example**:
- Prior: $\text{Beta}(1, 1)$ — uniform, like having seen 1 head and 1 tail imaginary
- Observe: 7 heads, 3 tails
- Posterior: $\text{Beta}(1+7, 1+3) = \text{Beta}(8, 4)$

The posterior mean is $8/(8+4) = 0.67$ — close to the observed $7/10 = 0.7$, but pulled slightly toward 0.5 by the prior.

---

## Chapter 11: From Beta to Dirichlet

### More Than Two Outcomes

Beta handles coins (2 outcomes). What about dice or alphabets with $K$ outcomes?

The **Dirichlet distribution** is the generalization of Beta to $K$ categories.

### Definition

$$(\theta_1, \theta_2, \ldots, \theta_K) \sim \text{Dirichlet}(\alpha_1, \alpha_2, \ldots, \alpha_K)$$

where each $\theta_k \geq 0$ and $\sum_{k=1}^{K} \theta_k = 1$.

The probability density is:

$$P(\theta_1, \ldots, \theta_K) = \frac{\Gamma(\sum_k \alpha_k)}{\prod_k \Gamma(\alpha_k)} \prod_{k=1}^{K} \theta_k^{\alpha_k - 1}$$

### The Conjugacy Still Works!

- Prior: $\text{Dirichlet}(\alpha_1, \ldots, \alpha_K)$
- Observe counts: $(c_1, \ldots, c_K)$ from a multinomial
- Posterior: $\text{Dirichlet}(\alpha_1 + c_1, \ldots, \alpha_K + c_K)$

**The update rule is identical**: Add observed counts to pseudocounts.

**Example**: Three symbols {A, B, C}
- Prior: $\text{Dirichlet}(1, 1, 1)$ — uniform over the simplex
- Observe: 5 A's, 3 B's, 2 C's
- Posterior: $\text{Dirichlet}(6, 4, 3)$

Posterior mean for P(A): $6/(6+4+3) = 6/13 \approx 0.46$

### Symmetric Dirichlet

Often we use the same $\alpha$ for all categories: $\text{Dirichlet}(\alpha, \alpha, \ldots, \alpha)$.

| $\alpha$ | Effect |
|----------|--------|
| $\alpha = 1$ | Uniform prior over all distributions |
| $\alpha < 1$ | Prefers sparse distributions (one category dominates) |
| $\alpha > 1$ | Prefers smooth distributions (probabilities spread out) |

---

## Chapter 12: Why This Matters for BSI

### Back to Epsilon-Machines

Each **causal state** in an epsilon-machine has an emission distribution — the probability of emitting each symbol when in that state.

We **don't know** these distributions; we have to learn them from data.

**BSI uses the Dirichlet-Multinomial framework:**

1. Put a Dirichlet prior on each state's emission distribution
2. Observe which symbols follow which histories
3. Conjugacy gives us the posterior automatically — just add counts!

### The Dirichlet-Multinomial Distribution

There's one more concept: what if we want the probability of the counts **without specifying $\theta$**?

We integrate out $\theta$:

$$P(\text{counts} \mid \alpha) = \int P(\text{counts} \mid \theta) P(\theta \mid \alpha) \, d\theta$$

This integral has a closed form! The result is the **Dirichlet-Multinomial** (or Pólya) distribution:

$$P(c_1, \ldots, c_K \mid \alpha_1, \ldots, \alpha_K) = \frac{n!}{\prod_k c_k!} \cdot \frac{\Gamma(\alpha_0)}{\Gamma(\alpha_0 + n)} \cdot \prod_{k=1}^{K} \frac{\Gamma(\alpha_k + c_k)}{\Gamma(\alpha_k)}$$

where $\alpha_0 = \sum_k \alpha_k$ and $n = \sum_k c_k$.

### The Key Insight for BSI

When we ask "should history $h$ belong to state $s$?", we compute:

> "If we add $h$'s counts to state $s$'s counts, how well does the combined distribution explain $h$'s emissions?"

This is exactly the Dirichlet-multinomial calculation — and it has a closed form!

---

## Chapter 13: What Is Sampling?

### When Exact Answers Are Hard

Sometimes we can't compute probabilities exactly. The formula might be too complex, or involve intractable integrals.

**Solution**: Draw **random samples** from the distribution and use them to estimate quantities.

### Analogy: Estimating an Average

Suppose you want to know the average height of students at a university.

**Hard way**: Measure every single student (expensive, time-consuming)

**Easy way**: Randomly sample 100 students, compute their average

With enough samples, the sample average approximates the true average. This is the **Law of Large Numbers**.

### For Probability Distributions

If we can sample from a distribution $P(x)$, we can estimate:

- **Mean**: Average of samples → $E[X]$
- **Variance**: Spread of samples → $\text{Var}(X)$
- **Probabilities**: Fraction of samples in a region → $P(X \in \text{region})$
- **Any function**: Average of $f(\text{sample})$ → $E[f(X)]$

---

## Chapter 14: Monte Carlo Methods

### Using Randomness to Compute

**Monte Carlo methods** use random sampling to estimate quantities that might be hard to compute analytically.

Named after the Monte Carlo casino — it's all about randomness!

### Classic Example: Estimating π

1. Draw a 1×1 square with a quarter-circle inside (radius 1)
2. Randomly drop points uniformly in the square
3. Count what fraction land inside the quarter-circle
4. That fraction ≈ (area of quarter-circle) / (area of square) = $\pi/4$

So: $\pi \approx 4 \times \text{(fraction inside)}$

With 10,000 points, you get a good estimate of $\pi \approx 3.14...$

### For Probability Distributions

**Goal**: Estimate $E[f(X)]$ where $X \sim P(x)$

**Method**:
1. Draw samples $x_1, x_2, \ldots, x_N$ from $P$
2. Compute $\frac{1}{N} \sum_{i=1}^{N} f(x_i)$

As $N \to \infty$, this converges to $E[f(X)]$.

---

## Chapter 15: Markov Chain Monte Carlo (MCMC)

### The Problem

What if we **can't directly sample** from our distribution $P(x)$?

This happens when:
- The distribution is complex (high-dimensional, intricate dependencies)
- It's defined over a huge discrete space
- We only know $P(x)$ up to a normalizing constant: $P(x) \propto f(x)$

### The Brilliant Solution: Random Walks

**Key idea**: Design a random walk that, over time, visits states proportionally to their probability.

Even if we can't sample directly, we might be able to:
1. Start somewhere
2. Propose a move to a nearby state
3. Accept or reject based on probability ratios
4. Repeat

### Markov Chain Basics

A **Markov chain** is a sequence of random states where each state depends only on the previous one, not the full history.

$$P(X_{t+1} \mid X_1, X_2, \ldots, X_t) = P(X_{t+1} \mid X_t)$$

The chain is defined by **transition probabilities**: $P(\text{next state} \mid \text{current state})$.

### The MCMC Guarantee

If we design the transition probabilities correctly, the chain has a **stationary distribution** equal to our target $P(x)$.

After running the chain long enough (**burn-in**), the states we visit are samples from $P(x)$!

---

## Chapter 16: Gibbs Sampling — A Specific MCMC Method

### The Setup

Suppose we have multiple variables $(x_1, x_2, \ldots, x_n)$ with a complex joint distribution $P(x_1, x_2, \ldots, x_n)$.

Sampling from the joint is hard. But sampling from each **conditional** might be easy:

- $P(x_1 \mid x_2, x_3, \ldots, x_n)$ — sample $x_1$ given all others fixed
- $P(x_2 \mid x_1, x_3, \ldots, x_n)$ — sample $x_2$ given all others fixed
- etc.

### The Gibbs Sampler Algorithm

```
Initialize: Pick starting values (x₁, x₂, ..., xₙ)

Repeat many times:
    Sample x₁ from P(x₁ | x₂, x₃, ..., xₙ)
    Sample x₂ from P(x₂ | x₁, x₃, ..., xₙ)  # Note: using NEW x₁
    Sample x₃ from P(x₃ | x₁, x₂, x₄, ..., xₙ)
    ...
    Sample xₙ from P(xₙ | x₁, x₂, ..., xₙ₋₁)

    → Record (x₁, x₂, ..., xₙ) as a sample
```

### Why It Works

**Theorem** (Geman & Geman, 1984): Under mild conditions, the sequence of samples converges to the true joint distribution $P(x_1, \ldots, x_n)$.

Intuitively: Each variable adjusts itself to be consistent with the others. Over time, everything settles into a state that reflects the joint distribution.

### Practical Considerations

- **Burn-in**: Discard early samples (chain hasn't converged yet)
- **Thinning**: Keep every $k$-th sample (reduces correlation between samples)
- **Multiple chains**: Run several chains from different starts to check convergence

---

## Chapter 17: Applying to BSI

### The Variables

In BSI, the variables are **state assignments** for each history:

- $z_{(0)}$ = which state does history "(0)" belong to?
- $z_{(1)}$ = which state does history "(1)" belong to?
- $z_{(0,0)}$ = which state does history "(0,0)" belong to?
- ... and so on for all observed histories

Each $z_h$ takes values in $\{1, 2, \ldots, k\}$ where $k$ is the number of states.

### The Joint Distribution

We want the posterior:

$$P(\text{all assignments} \mid \text{all observed data})$$

This is a complex distribution over a discrete space with $k^{|\text{histories}|}$ possibilities — far too many to enumerate!

### The Gibbs Update

For each history $h$:

1. **Fix** all other histories' current assignments
2. **For each possible state** $s \in \{1, \ldots, k\}$, compute:
   - Aggregate the counts from all histories currently assigned to $s$ (excluding $h$)
   - Add $h$'s counts to get combined counts
   - Use Dirichlet-multinomial to compute: "How likely is $h$'s data under this combined model?"
3. **Sample** a new assignment proportional to these likelihoods

### The Conditional Probability

$$P(z_h = s \mid \text{all other assignments}, \text{data}) \propto \underbrace{P(\text{counts}_h \mid \text{counts in state } s)}_{\text{Dirichlet-multinomial}} \times \underbrace{P(z_h = s)}_{\text{prior}}$$

The Dirichlet-multinomial term uses the formula from Chapter 12.

The prior term often simply counts how many histories are already in state $s$ (a "rich get richer" dynamic).

---

## Chapter 18: Model Selection — Choosing the Number of States

### The Problem

We've described how to sample assignments for a **fixed** number of states $k$.

But what's the right $k$?
- Too few states → **underfitting** (can't capture the true structure)
- Too many states → **overfitting** (fitting noise, spurious states)

### The Bayesian Answer

Compare the **evidence** (marginal likelihood) for different values of $k$:

$$P(k \mid \text{data}) \propto P(\text{data} \mid k) \times P(k)$$

The term $P(\text{data} \mid k)$ is called the **marginal likelihood** or **model evidence**:

$$P(\text{data} \mid k) = \int P(\text{data} \mid \theta, k) P(\theta \mid k) \, d\theta$$

This integrates over all possible parameters — it asks "how likely is the data under this model structure, averaging over all parameter values?"

### Why Evidence Works for Model Selection

- Complex models can fit data better (higher likelihood at the best $\theta$)
- But complex models spread their probability over more parameter values
- This "Occam's razor" effect automatically penalizes unnecessary complexity

### The BIC Approximation

Computing evidence exactly is often intractable. The **Bayesian Information Criterion** provides an approximation:

$$\text{BIC} = -2 \ln(\hat{L}) + p \ln(n)$$

where:
- $\hat{L}$ = maximum likelihood (best fit)
- $p$ = number of free parameters
- $n$ = number of data points

Equivalently, in terms of log-evidence:

$$\ln P(\text{data} \mid k) \approx \ln(\hat{L}) - \frac{p}{2} \ln(n)$$

**Interpretation**:
- First term: How well does the best-fit model explain data? (favors complex models)
- Second term: Penalty for complexity (favors simple models)

**Lower BIC = better model** (or equivalently, higher log-evidence)

### For Epsilon-Machines

For a $k$-state machine over alphabet of size $|\Sigma|$:
- Each state has $|\Sigma| - 1$ free emission probabilities (they must sum to 1)
- Roughly: $p \approx k \times |\Sigma|$ parameters

---

## Summary: Connecting the Concepts

| Chapter | Concept | Role in BSI |
|---------|---------|-------------|
| 1-4 | Basic probability, binomial | Foundation for counting |
| 5 | Multinomial | Models symbol emissions from states |
| 6-7 | Bayesian inference, Bayes' theorem | Framework for learning |
| 8-9 | Beta distribution | Prior/posterior for 2-outcome case |
| 10 | Conjugacy | Enables closed-form updates |
| 11 | Dirichlet distribution | Prior/posterior for K-outcome case |
| 12 | Dirichlet-multinomial | Likelihood with parameters integrated out |
| 13-14 | Sampling, Monte Carlo | Approximating complex distributions |
| 15-16 | MCMC, Gibbs sampling | Sampling from posterior over assignments |
| 17 | BSI application | Putting it all together |
| 18 | Model selection, BIC | Choosing number of states |

---

## What BSI Does — In Plain English

1. **Try different numbers of states** (1, 2, 3, ... up to some maximum)

2. **For each number of states $k$**:
   - Start with random assignments of histories to states
   - Repeat many times (Gibbs sampling):
     - Pick a history
     - Ask: "Given everyone else's assignments, which state best explains this history's data?"
     - Reassign it by sampling from this conditional distribution
   - After burn-in, the assignments represent samples from the posterior

3. **Compare models**: Use BIC to estimate which $k$ best explains the data without overfitting

4. **Return**: The epsilon-machine from the best $k$, using the best assignments found

---

## Further Reading

- **Gelman et al.** - *Bayesian Data Analysis* (the standard textbook)
- **Murphy** - *Machine Learning: A Probabilistic Perspective* (comprehensive)
- **Bishop** - *Pattern Recognition and Machine Learning* (good on graphical models)
- **Strelioff & Crutchfield (2014)** - "Bayesian Structural Inference for Hidden Processes" (the original BSI paper)

---

*Document created: 2026-01-18*
*For the emic project: https://github.com/johnazariah/emic*
