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
    Compute the excess entropy E.

    E = I(Past; Future) = Cμ + Cμ' - I

    For unifilar machines (which epsilon-machines are):
    E = Cμ (statistical complexity equals excess entropy)

    Args:
        machine: The epsilon-machine

    Returns:
        Excess entropy in bits

    Note:
        For general epsilon-machines, E = Cμ since they are unifilar.
    """
    # For unifilar machines, excess entropy equals statistical complexity
    return statistical_complexity(machine)
