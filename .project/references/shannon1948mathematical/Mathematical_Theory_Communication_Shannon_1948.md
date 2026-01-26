# A Mathematical Theory of Communication

**Author:** Claude E. Shannon
**Affiliation:** Bell Telephone Laboratories
**Source:** The Bell System Technical Journal, Vol. 27, pp. 379–423, 623–656, July, October, 1948
**Date:** 1948

---

## Abstract

This landmark paper establishes the mathematical foundations of information theory. Shannon introduces the concept of entropy as a measure of information, defines the capacity of a communication channel, and proves fundamental theorems about the limits of reliable communication in the presence of noise.

---

## 1. Introduction

The fundamental problem of communication is that of reproducing at one point either exactly or approximately a message selected at another point. The semantic aspects of communication are irrelevant to the engineering problem. The significant aspect is that the actual message is one selected from a set of possible messages.

### The Logarithmic Measure

If the number of messages in the set is finite, then the most natural measure of information is the logarithmic function. The choice of a logarithmic base corresponds to the choice of a unit for measuring information:

- **Base 2**: Binary digits, or **bits** (term suggested by J. W. Tukey)
- **Base 10**: Decimal digits
- **Base e**: Natural units

A device with two stable positions can store one bit of information. $N$ such devices can store $N$ bits, since the total number of possible states is $2^N$ and $\log_2 2^N = N$.

Conversion between bases:
$$\log_2 M = \log_{10} M / \log_{10} 2 = 3.32 \log_{10} M$$

---

## 2. The Communication System

A general communication system consists of five parts:

1. **Information source** — produces a message or sequence of messages
2. **Transmitter** — operates on the message to produce a signal suitable for transmission
3. **Channel** — the medium used to transmit the signal
4. **Receiver** — reconstructs the message from the signal
5. **Destination** — the person or thing for whom the message is intended

[Figure 1: Schematic diagram of a general communication system — see original PDF]

### Types of Messages

- **(a)** Sequence of letters (telegraph/teletype)
- **(b)** Single function of time $f(t)$ (radio/telephony)
- **(c)** Function of time and space $f(x, y, t)$ (television)
- **(d)** Multiple functions of time (3D sound, multiplex)
- **(e)** Multiple functions of multiple variables (color television)

---

## 3. The Discrete Noiseless Channel

### Entropy of an Information Source

For a discrete source emitting symbols with probabilities $p_1, p_2, \ldots, p_n$, the entropy is:

$$H = -\sum_{i=1}^{n} p_i \log p_i$$

This measures the average information per symbol, or equivalently, the average uncertainty about the next symbol.

### Properties of Entropy

1. $H = 0$ if and only if all probabilities but one are zero
2. $H$ is maximum when all probabilities are equal: $H = \log n$
3. $H$ is a continuous function of the probabilities

### The Fundamental Theorem for Noiseless Channels

Let a source have entropy $H$ bits per symbol and a channel have capacity $C$ bits per second. Then it is possible to encode the source so that $C/H - \epsilon$ symbols per second are transmitted, where $\epsilon$ is arbitrarily small. It is not possible to transmit at a rate greater than $C/H$.

---

## 4. The Discrete Channel with Noise

### Channel Capacity

The capacity of a noisy channel is defined as:

$$C = \max_{p(x)} I(X; Y)$$

where $I(X; Y) = H(X) - H(X|Y) = H(Y) - H(Y|X)$ is the mutual information between input and output.

### The Fundamental Theorem (Noisy Channel Coding Theorem)

Let a discrete channel have capacity $C$ and a discrete source have entropy $H$. If $H \leq C$, there exists a coding system such that the output of the source can be transmitted over the channel with an arbitrarily small frequency of errors. If $H > C$, reliable transmission is impossible.

---

## 5. Continuous Information

### Entropy of a Continuous Distribution

For a continuous distribution with density $p(x)$:

$$H = -\int p(x) \log p(x) \, dx$$

### Band-Limited Functions

A function containing no frequencies higher than $W$ cycles per second is completely determined by its values at a series of points spaced $1/(2W)$ seconds apart.

### Capacity of a Band-Limited Channel

For a channel of bandwidth $W$ Hz with signal power $S$ and noise power $N$:

$$C = W \log_2\left(1 + \frac{S}{N}\right) \text{ bits/second}$$

This is the **Shannon-Hartley theorem**.

---

## Key Concepts

| Concept | Definition |
|---------|------------|
| **Entropy** $H$ | Average information per symbol: $H = -\sum p_i \log p_i$ |
| **Channel capacity** $C$ | Maximum rate of reliable information transmission |
| **Mutual information** $I(X;Y)$ | Information that $Y$ provides about $X$ |
| **Bit** | Unit of information; entropy of a fair coin flip |
| **Redundancy** | $1 - H/H_{\max}$; exploitable for error correction |

---

## Historical Significance

This paper founded the field of information theory and introduced concepts that are fundamental to:

- Digital communication systems
- Data compression (source coding)
- Error correction (channel coding)
- Cryptography
- Statistical inference
- Computational complexity

The definition of entropy has deep connections to thermodynamic entropy and has influenced fields from physics to biology to economics.

---

## References

1. Nyquist, H., "Certain Factors Affecting Telegraph Speed," Bell System Technical Journal, April 1924
2. Hartley, R. V. L., "Transmission of Information," Bell System Technical Journal, July 1928

---

*Extracted from: shannon1948mathematical.pdf*
