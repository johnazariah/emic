"""Analysis measures for epsilon-machines."""

from __future__ import annotations

import math
from collections.abc import Hashable
from typing import TYPE_CHECKING, TypeVar

import numpy as np

if TYPE_CHECKING:
    from numpy.typing import NDArray

    from emic.types import EpsilonMachine

A = TypeVar("A", bound=Hashable)

# Tolerance for convergence checks
_CONVERGENCE_TOL = 1e-10
_MAX_BLOCK_LENGTH = 1000


def state_count(machine: EpsilonMachine[A]) -> int:
    """
    Number of causal states.

    A simple but fundamental measure of structural complexity.

    Args:
        machine: The epsilon-machine

    Returns:
        Number of states
    """
    return len(machine.states)


def transition_count(machine: EpsilonMachine[A]) -> int:
    """
    Total number of transitions.

    Args:
        machine: The epsilon-machine

    Returns:
        Total number of transitions
    """
    return sum(len(s.transitions) for s in machine.states)


def topological_complexity(machine: EpsilonMachine[A]) -> float:
    """
    Topological complexity: log₂(number of states).

    An upper bound on statistical complexity.

    Args:
        machine: The epsilon-machine

    Returns:
        Topological complexity in bits
    """
    n = len(machine.states)
    return math.log2(n) if n > 0 else 0.0


def statistical_complexity(machine: EpsilonMachine[A]) -> float:
    """
    Compute the statistical complexity Cμ.

    Cμ = H(S) = -Σᵢ πᵢ log₂(πᵢ)

    where πᵢ is the stationary probability of state i.

    Args:
        machine: The epsilon-machine

    Returns:
        Statistical complexity in bits

    Examples:
        >>> from emic.sources.synthetic.golden_mean import GoldenMeanSource
        >>> machine = GoldenMeanSource(p=0.5).true_machine
        >>> 0.9 < statistical_complexity(machine) < 0.95
        True
    """
    stationary = machine.stationary_distribution
    return stationary.entropy()


def entropy_rate(machine: EpsilonMachine[A]) -> float:
    """
    Compute the entropy rate hμ.

    hμ = H(X | S) = Σᵢ πᵢ H(X | S = sᵢ)

    where H(X | S = sᵢ) is the entropy of the emission distribution
    from state sᵢ.

    Args:
        machine: The epsilon-machine

    Returns:
        Entropy rate in bits per symbol

    Examples:
        >>> from emic.sources.synthetic.biased_coin import BiasedCoinSource
        >>> machine = BiasedCoinSource(p=0.5).true_machine
        >>> abs(entropy_rate(machine) - 1.0) < 0.01
        True
    """
    stationary = machine.stationary_distribution
    h = 0.0

    for state in machine.states:
        pi = stationary.probs.get(state.id, 0.0)
        if pi <= 0:
            continue

        # Emission distribution from this state
        emission_probs: dict[A, float] = {}
        for t in state.transitions:
            emission_probs[t.symbol] = emission_probs.get(t.symbol, 0.0) + t.probability

        # Compute entropy of emission distribution
        state_entropy = 0.0
        for prob in emission_probs.values():
            if prob > 0:
                state_entropy -= prob * math.log2(prob)

        h += pi * state_entropy

    return h


def block_entropy(machine: EpsilonMachine[A], length: int) -> float:
    """
    Compute block entropy H(X_0, X_1, ..., X_{L-1}).

    For an ε-machine, the block entropy can be computed by:
    1. Start with stationary distribution over states
    2. For each possible L-block, compute its probability
    3. Return entropy of the block distribution

    For efficiency with large L, we use matrix methods.

    Args:
        machine: The epsilon-machine
        length: Block length L

    Returns:
        Block entropy H(X_0^{L-1}) in bits
    """
    if length <= 0:
        return 0.0

    states = list(machine.states)
    state_ids = [s.id for s in states]
    state_to_idx = {s.id: i for i, s in enumerate(states)}
    symbols = list(machine.alphabet)
    n_states = len(states)
    n_symbols = len(symbols)
    symbol_to_idx = {x: i for i, x in enumerate(symbols)}

    # Build per-symbol transition matrices T^(x)
    # T_x[j, k] = P(emit x and go to k | in state j)
    T_matrices: dict[A, NDArray[np.float64]] = {x: np.zeros((n_states, n_states)) for x in symbols}

    for j, state in enumerate(states):
        for trans in state.transitions:
            k = state_to_idx[trans.target]
            T_matrices[trans.symbol][j, k] += trans.probability

    # Initial state distribution (stationary)
    pi = np.array([machine.stationary_distribution.probs.get(sid, 0.0) for sid in state_ids])

    # For length 1: H(X_0) = H(emission from stationary)
    if length == 1:
        # Marginal emission distribution
        emission_probs = np.zeros(n_symbols)
        for x, T_x in T_matrices.items():
            x_idx = symbol_to_idx[x]
            emission_probs[x_idx] = pi @ T_x.sum(axis=1)
        return _shannon_entropy(emission_probs)

    # For length L > 1: enumerate all L-blocks (exponential, but exact)
    # For large L, use approximation via block entropy growth formula
    if n_symbols**length > 100000:
        # Use asymptotic formula: H(L) ≈ E + L * h_μ
        # We compute E iteratively from shorter blocks
        return _block_entropy_large(machine, length)

    # Enumerate all L-blocks
    block_probs: dict[tuple[A, ...], float] = {}

    def enumerate_blocks(
        current_block: tuple[A, ...], state_dist: NDArray[np.float64], depth: int
    ) -> None:
        """Recursively enumerate all L-blocks and accumulate probabilities."""
        if depth == length:
            prob = state_dist.sum()
            if prob > 1e-15:
                block_probs[current_block] = block_probs.get(current_block, 0.0) + prob
            return

        for x in symbols:
            T_x = T_matrices[x]
            next_dist = state_dist @ T_x
            if next_dist.sum() > 1e-15:
                enumerate_blocks((*current_block, x), next_dist, depth + 1)

    enumerate_blocks((), pi, 0)

    probs = np.array(list(block_probs.values()))
    return _shannon_entropy(probs)


def _block_entropy_large(machine: EpsilonMachine[A], length: int) -> float:
    """Approximate block entropy for large L using asymptotic formula."""
    # Compute E from shorter blocks, then H(L) ≈ E + L * h_μ
    e = excess_entropy(machine)
    h = entropy_rate(machine)
    return e + length * h


def _shannon_entropy(probs: NDArray[np.float64]) -> float:
    """Compute Shannon entropy of a probability vector."""
    probs = probs[probs > 1e-15]
    if len(probs) == 0:
        return 0.0
    return float(-np.sum(probs * np.log2(probs)))


def excess_entropy(machine: EpsilonMachine[A]) -> float:
    """
    Compute the excess entropy E = I(Past; Future).

    The excess entropy measures the mutual information between
    the semi-infinite past and semi-infinite future. It equals
    the subextensive component of block entropy growth:

        H(X_0^{L-1}) → E + L·h_μ  as L → ∞

    Therefore:
        E = lim_{L→∞} [H(X_0^{L-1}) - L·h_μ]

    For finite-state machines, this limit is reached in finite L.

    Equivalently (James et al. 2011):
        E = Sigma_{L=1}^inf (h_L - h_mu)

    where h_L = H(X_L | X_0^{L-1}).

    Args:
        machine: The epsilon-machine

    Returns:
        Excess entropy in bits

    Note:
        For processes with zero crypticity (χ = 0), E = C_μ.
        In general, E ≤ C_μ with strict inequality when χ > 0.

    Examples:
        >>> from emic.sources.synthetic.biased_coin import BiasedCoinSource
        >>> machine = BiasedCoinSource(p=0.5).true_machine
        >>> abs(excess_entropy(machine)) < 1e-10  # IID process
        True
    """
    h_mu = entropy_rate(machine)

    # For single-state machines (IID processes), E = 0
    if len(machine.states) == 1:
        return 0.0

    # Compute E = lim [H(L) - L * h_μ]
    # For ε-machines, convergence happens within O(n) steps
    # where n is the number of states

    # We compute block entropies and look for convergence
    prev_e_estimate = float("inf")
    max_length = min(_MAX_BLOCK_LENGTH, 2 * len(machine.states) + 10)

    for length in range(1, max_length + 1):
        h_l = block_entropy(machine, length)
        e_estimate = h_l - length * h_mu

        # Check convergence
        if abs(e_estimate - prev_e_estimate) < _CONVERGENCE_TOL:
            return max(0.0, e_estimate)  # E ≥ 0 by definition

        prev_e_estimate = e_estimate

    # Return best estimate (may not have fully converged for complex machines)
    return max(0.0, prev_e_estimate)


def crypticity(machine: EpsilonMachine[A]) -> float:
    """
    Compute the crypticity χ = C_μ - E.

    Crypticity measures the "hidden" information in the causal state
    that doesn't contribute to prediction. It represents classical
    waste that quantum models can eliminate.

    Args:
        machine: The epsilon-machine

    Returns:
        Crypticity in bits (always ≥ 0)

    Examples:
        >>> from emic.sources.synthetic.biased_coin import BiasedCoinSource
        >>> machine = BiasedCoinSource(p=0.5).true_machine
        >>> abs(crypticity(machine)) < 1e-10  # IID: no crypticity
        True
    """
    c_mu = statistical_complexity(machine)
    e = excess_entropy(machine)
    return max(0.0, c_mu - e)
