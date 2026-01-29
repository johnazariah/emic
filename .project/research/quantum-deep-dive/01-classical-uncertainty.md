# Chapter 1: Classical Uncertainty

*Probability, entropy, and what it means to "know" something*

---

## The Setup

Before we can understand what makes quantum mechanics quantum, we need to be crystal clear about classical uncertainty. This chapter establishes the baseline: how do we represent and measure uncertainty using probability?

This isn't just review—how we represent classical uncertainty will directly reveal what's different about quantum uncertainty.

---

## Probability as a Vector

When we have a random variable $X$ that can take values $\{x_1, x_2, \ldots, x_n\}$, we represent our knowledge as a **probability vector**:

$$\mathbf{p} = \begin{pmatrix} p_1 \\ p_2 \\ \vdots \\ p_n \end{pmatrix}$$

where $p_i = P(X = x_i)$ and $\sum_i p_i = 1$.

**Example**: A weighted die with probabilities:
- Face 1: 0.1
- Face 2: 0.1
- Face 3: 0.1
- Face 4: 0.1
- Face 5: 0.1
- Face 6: 0.5

$$\mathbf{p} = \begin{pmatrix} 0.1 \\ 0.1 \\ 0.1 \\ 0.1 \\ 0.1 \\ 0.5 \end{pmatrix}$$

This is just a list of numbers—nothing mysterious. But notice: we're using a vector to represent uncertainty.

---

## From Vectors to Matrices: A Key Step

Here's a seemingly pointless elaboration that will become crucial.

Instead of a probability *vector*, we can represent the same information as a **diagonal matrix**:

$$P = \begin{pmatrix}
p_1 & 0 & \cdots & 0 \\
0 & p_2 & \cdots & 0 \\
\vdots & & \ddots & \\
0 & 0 & \cdots & p_n
\end{pmatrix}$$

For our weighted die:

$$P = \begin{pmatrix}
0.1 & 0 & 0 & 0 & 0 & 0 \\
0 & 0.1 & 0 & 0 & 0 & 0 \\
0 & 0 & 0.1 & 0 & 0 & 0 \\
0 & 0 & 0 & 0.1 & 0 & 0 \\
0 & 0 & 0 & 0 & 0.1 & 0 \\
0 & 0 & 0 & 0 & 0 & 0.5
\end{pmatrix}$$

Why bother? Because:

> **The diagonal contains all the classical information. Everything else is zero.**

This is not a mathematical nicety—it's the punchline of this whole series. In quantum mechanics, those off-diagonal zeros can become nonzero. When they do, something fundamentally new happens.

But we're getting ahead of ourselves. For now, just remember: **classical = diagonal**.

---

## Entropy: Measuring Uncertainty

How much uncertainty does a probability distribution contain? Shannon's entropy gives the answer:

$$H(\mathbf{p}) = -\sum_{i=1}^n p_i \log_2 p_i$$

The units are **bits**—the same bits your computer uses.

### What Does It Mean?

Entropy tells you the average number of yes/no questions needed to determine the outcome.

- **Maximum entropy**: A fair coin has $H = 1$ bit. One yes/no question suffices.
- **Zero entropy**: A certain outcome ($p_i = 1$ for some $i$) has $H = 0$. No questions needed.
- **In between**: Biased distributions fall somewhere in between.

### Worked Example: The Weighted Die

Let's compute the entropy of our weighted die:

$$H = -\sum_{i=1}^6 p_i \log_2 p_i$$

| Face | $p_i$ | $\log_2 p_i$ | $-p_i \log_2 p_i$ |
|------|-------|--------------|-------------------|
| 1 | 0.1 | -3.322 | 0.332 |
| 2 | 0.1 | -3.322 | 0.332 |
| 3 | 0.1 | -3.322 | 0.332 |
| 4 | 0.1 | -3.322 | 0.332 |
| 5 | 0.1 | -3.322 | 0.332 |
| 6 | 0.5 | -1.000 | 0.500 |

$$H = 5 \times 0.332 + 0.500 = 1.66 + 0.50 = 2.16 \text{ bits}$$

Compare to a fair die: $H_{\text{fair}} = \log_2 6 = 2.58$ bits.

The biased die has less uncertainty because we can partially predict the outcome (it's probably a 6).

---

## Information = Resolved Uncertainty

Here's a subtle but important point: **information is not the same as data**.

- **Data**: The actual symbols you receive (e.g., "6, 3, 6, 6, 1, 6, ...")
- **Information**: How much your uncertainty decreased upon receiving the data

If you already knew the die was loaded to show 6, seeing another 6 gives you almost no information. If you expected a fair die, seeing 6 gives you about 2.58 bits of information.

**Shannon's insight**: Information is the *difference* between prior uncertainty and posterior uncertainty.

This will matter when we discuss measurement in quantum mechanics. Measurement gives you information precisely because it resolves uncertainty—by forcing a definite outcome.

---

## States as Slots: The Classical Picture

Think of each possible outcome as a **slot** in memory:

```
┌─────┬─────┬─────┬─────┬─────┬─────┐
│  1  │  2  │  3  │  4  │  5  │  6  │
├─────┼─────┼─────┼─────┼─────┼─────┤
│ 0.1 │ 0.1 │ 0.1 │ 0.1 │ 0.1 │ 0.5 │
└─────┴─────┴─────┴─────┴─────┴─────┘
```

Each slot holds a probability. The slots are **mutually exclusive**—the die can only be in one state at a time. When we observe the die, it's definitely in one slot or another.

This mutual exclusivity is the classical assumption. In the matrix picture, it's why off-diagonals are zero: there's no "connection" between outcomes.

In Chapter 3, we'll see that quantum mechanics allows slots to have connections—nonzero off-diagonal elements—and this changes everything.

---

## A Preview: Why This Matters

Consider a simple machine that flips between two states, $A$ and $B$:

```
     ┌──────────────────┐
     │                  │
     ▼                  │
   ┌───┐   p=0.7    ┌───┐
   │ A │ ────────▶  │ B │
   └───┘            └───┘
     ▲      p=0.3      │
     │                 │
     └─────────────────┘
```

At equilibrium, suppose we find the machine in each state with probability 50%:

$$\mathbf{p} = \begin{pmatrix} 0.5 \\ 0.5 \end{pmatrix}$$

Classical entropy: $H = -0.5 \log_2(0.5) - 0.5 \log_2(0.5) = 1$ bit.

To track this machine classically, we need 1 bit of memory—one slot for "A" and one for "B".

But what if states $A$ and $B$ lead to similar futures? What if they're almost the same, from a predictive standpoint? Classical mechanics still requires 1 bit—the states are in different slots, so we must distinguish them.

Quantum mechanics will let us store these states in **overlapping** slots, using less than 1 bit. That's the quantum advantage. But to see it, we first need to understand what "overlapping" even means—which requires leaving the classical world behind.

---

## Key Takeaway

> **Classical uncertainty lives on the diagonal.**
>
> A probability distribution is a list of numbers summing to 1. When represented as a matrix, all information sits on the diagonal. The off-diagonal entries are zero—there's no "interference" between outcomes.
>
> This is what we mean by "classical." Quantum mechanics will populate those off-diagonals.

---

## Common Misconceptions

### "Entropy measures disorder"

Not quite. Entropy measures *uncertainty about the outcome*. A fair coin is not "disordered"—it's highly structured, just maximally uncertain. Better: entropy measures how surprised you'll be, on average.

### "More entropy = more complex"

No! Maximum entropy means maximum randomness—no structure at all. The most "complex" systems in a meaningful sense have *intermediate* entropy: enough structure to be predictable, enough randomness to be interesting. This is exactly what computational mechanics studies.

### "Information is stored in bits"

Data is stored in bits. Information is what you *learn*—the uncertainty that gets resolved. If you already knew the answer, receiving it gives you zero information, even though it took bits to transmit.

### "Classical probability is simple"

It's not! Probability theory is subtle and deep. But compared to quantum probability, classical probability has one simplifying feature: outcomes don't interfere with each other. That's the conceptual core of "classical."

---

## Code Example

Here's how to compute entropy in Python:

```python
import numpy as np

def entropy(p: np.ndarray) -> float:
    """Shannon entropy in bits."""
    # Filter out zeros to avoid log(0)
    p = p[p > 0]
    return -np.sum(p * np.log2(p))

# Weighted die example
p_die = np.array([0.1, 0.1, 0.1, 0.1, 0.1, 0.5])
print(f"Weighted die entropy: {entropy(p_die):.3f} bits")  # 2.161 bits

# Fair die comparison
p_fair = np.ones(6) / 6
print(f"Fair die entropy: {entropy(p_fair):.3f} bits")  # 2.585 bits

# Representing as a diagonal matrix (classical density matrix)
P_matrix = np.diag(p_die)
print("Classical 'density matrix':")
print(P_matrix)
# All off-diagonals are zero!
```

Output:
```
Weighted die entropy: 2.161 bits
Fair die entropy: 2.585 bits
Classical 'density matrix':
[[0.1 0.  0.  0.  0.  0. ]
 [0.  0.1 0.  0.  0.  0. ]
 [0.  0.  0.1 0.  0.  0. ]
 [0.  0.  0.  0.1 0.  0. ]
 [0.  0.  0.  0.  0.1 0. ]
 [0.  0.  0.  0.  0.  0.5]]
```

---

## What's Next

In [Chapter 2: The Quantum Twist](02-quantum-twist.md), we'll see what happens when we allow complex amplitudes instead of just real probabilities—and why those off-diagonal zeros can become nonzero.

---

*[← Back to Overview](00-overview.md) | [Next: The Quantum Twist →](02-quantum-twist.md)*
