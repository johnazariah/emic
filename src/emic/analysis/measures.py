"""Analysis measures for epsilon-machines."""

from __future__ import annotations

import math
from collections.abc import Hashable
from typing import TYPE_CHECKING, TypeVar

if TYPE_CHECKING:
    from emic.types import EpsilonMachine

A = TypeVar("A", bound=Hashable)


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


def excess_entropy(machine: EpsilonMachine[A]) -> float:
    """
    Compute the excess entropy E = I(Past; Future).

    Uses block entropy convergence:

        E = lim_{L→∞} [ H(X₁, ..., X_L) - L · hμ ]

    For a unifilar machine, block entropies H(X₁...X_L) are computed
    exactly by propagating the state distribution through the transition
    structure. The difference H(X₁...X_L) - L·hμ converges to E as L
    grows.

    Note:
        E ≤ Cμ always. The gap χ = Cμ - E is the crypticity.

    Args:
        machine: The epsilon-machine

    Returns:
        Excess entropy in bits

    Examples:
        >>> from emic.sources.synthetic.biased_coin import BiasedCoinSource
        >>> machine = BiasedCoinSource(p=0.5).true_machine
        >>> abs(excess_entropy(machine)) < 1e-10
        True
    """
    h_mu = entropy_rate(machine)

    # Trivial case: single state (IID process)
    if len(machine.states) <= 1:
        return 0.0

    # Build emission/transition structure for the unifilar machine.
    # For each (state, symbol): probability of emitting symbol, and target state.
    state_ids = sorted(s.id for s in machine.states)
    state_idx = {sid: i for i, sid in enumerate(state_ids)}
    n_states = len(state_ids)
    alphabet = list(machine.alphabet)
    symbol_idx = {sym: i for i, sym in enumerate(alphabet)}

    # trans[i] = list of (symbol, probability, target_index)
    trans: list[list[tuple[int, float, int]]] = [[] for _ in range(n_states)]
    for state in machine.states:
        i = state_idx[state.id]
        for t in state.transitions:
            j = state_idx[t.target]
            trans[i].append((symbol_idx[t.symbol], t.probability, j))

    # Start from stationary distribution
    pi = machine.stationary_distribution
    state_dist = [pi.probs.get(sid, 0.0) for sid in state_ids]

    # Compute block entropies using mixed-state propagation.
    # At each step L, we track a set of "mixed states": each is a
    # (probability, state_distribution) pair representing one branch
    # of the observation tree. We accumulate H(X₁...X_L) incrementally.
    #
    # H(X₁...X_L) = H(X₁...X_{L-1}) + H(X_L | X₁...X_{L-1})
    #
    # H(X_L | X₁...X_{L-1}) is computed by averaging the emission entropy
    # over all branches weighted by their probability.

    # A branch is (weight, state_vector) where state_vector[i] = P(state=i | branch)
    branches: list[tuple[float, list[float]]] = [(1.0, list(state_dist))]

    block_entropy = 0.0
    max_L = 50  # Convergence typically within 10-20 steps
    convergence_tol = 1e-12
    prev_excess = float("inf")

    for step in range(max_L):
        # For each branch, compute emission distribution and split
        new_branches: list[tuple[float, list[float]]] = []
        conditional_entropy = 0.0  # H(X_{L+1} | X₁...X_L)

        for weight, sv in branches:
            if weight < 1e-15:
                continue

            # Compute P(symbol | this branch) and new state dist for each symbol
            symbol_probs = [0.0] * len(alphabet)
            # next_sv[sym_idx][state_idx] = un-normalized prob of being in state
            next_sv: list[list[float]] = [[0.0] * n_states for _ in range(len(alphabet))]

            for i in range(n_states):
                if sv[i] < 1e-15:
                    continue
                for sym_idx, prob, j in trans[i]:
                    contribution = sv[i] * prob
                    symbol_probs[sym_idx] += contribution
                    next_sv[sym_idx][j] += contribution

            # Accumulate conditional entropy for this branch
            for sym_idx in range(len(alphabet)):
                p_sym = symbol_probs[sym_idx]
                if p_sym < 1e-15:
                    continue
                conditional_entropy -= weight * p_sym * math.log2(p_sym)

                # Normalize the next state distribution
                normalized = [x / p_sym for x in next_sv[sym_idx]]
                new_branches.append((weight * p_sym, normalized))

        block_entropy += conditional_entropy
        excess = block_entropy - (step + 1) * h_mu

        # Check convergence
        if abs(excess - prev_excess) < convergence_tol:
            return max(0.0, excess)

        prev_excess = excess

        # Merge branches with identical (or very similar) state distributions
        # to prevent exponential blowup
        branches = _merge_branches(new_branches)

    return max(0.0, prev_excess)


def _merge_branches(
    branches: list[tuple[float, list[float]]],
) -> list[tuple[float, list[float]]]:
    """Merge branches with identical state distributions."""
    if not branches:
        return branches

    # Round state vectors for comparison (merge if very close)
    merged: dict[tuple[float, ...], tuple[float, list[float]]] = {}
    precision = 10  # decimal places for rounding

    for weight, sv in branches:
        if weight < 1e-15:
            continue
        key = tuple(round(x, precision) for x in sv)
        if key in merged:
            old_weight, old_sv = merged[key]
            merged[key] = (old_weight + weight, old_sv)
        else:
            merged[key] = (weight, sv)

    return list(merged.values())


def crypticity(machine: EpsilonMachine[A]) -> float:
    """
    Compute the crypticity χ = Cμ - E.

    Crypticity measures how much of the stored information (Cμ) is
    "hidden" — not directly accessible as past-future mutual information.

    χ ≥ 0 always, and χ = 0 only for special processes.

    Args:
        machine: The epsilon-machine

    Returns:
        Crypticity in bits

    Examples:
        >>> from emic.sources.synthetic.golden_mean import GoldenMeanSource
        >>> machine = GoldenMeanSource(p=0.5).true_machine
        >>> crypticity(machine) > 0.4
        True
    """
    return statistical_complexity(machine) - excess_entropy(machine)
