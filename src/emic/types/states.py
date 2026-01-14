"""State types for epsilon-machines."""

from __future__ import annotations

from collections.abc import Hashable
from dataclasses import dataclass
from typing import Generic, TypeVar

from emic.types.probability import Distribution, ProbabilityValue

# States are identified by strings
StateId = str

A = TypeVar("A", bound=Hashable)

# Tolerance for probability validation
_PROBABILITY_TOLERANCE = 1e-9


@dataclass(frozen=True)
class Transition(Generic[A]):
    """
    A labeled transition from one state to another.

    Represents: "On symbol `symbol`, go to `target` with probability `probability`"

    Attributes:
        symbol: The emitted symbol for this transition.
        probability: The probability of taking this transition (must be in (0, 1]).
        target: The ID of the target state.

    Examples:
        >>> t = Transition(symbol='a', probability=0.5, target='S1')
        >>> t.symbol
        'a'
        >>> t.probability
        0.5
    """

    symbol: A
    probability: ProbabilityValue
    target: StateId

    def __post_init__(self) -> None:
        """Validate that probability is in valid range."""
        if not (0.0 < self.probability <= 1.0 + _PROBABILITY_TOLERANCE):
            msg = f"Probability must be in (0,1], got {self.probability}"
            raise ValueError(msg)


@dataclass(frozen=True)
class CausalState(Generic[A]):
    """
    A causal state in an epsilon-machine.

    A causal state is an equivalence class of histories that induce
    the same conditional distribution over futures.

    Attributes:
        id: Unique identifier for this state.
        transitions: Set of outgoing transitions from this state.

    Examples:
        >>> t1 = Transition(symbol=0, probability=0.5, target='A')
        >>> t2 = Transition(symbol=1, probability=0.5, target='B')
        >>> state = CausalState(id='A', transitions=frozenset({t1, t2}))
        >>> state.alphabet
        frozenset({0, 1})
    """

    id: StateId
    transitions: frozenset[Transition[A]]

    def __post_init__(self) -> None:
        """Validate transition probabilities for each symbol sum to <= 1."""
        by_symbol: dict[A, float] = {}
        for t in self.transitions:
            by_symbol[t.symbol] = by_symbol.get(t.symbol, 0.0) + t.probability
        for symbol, total in by_symbol.items():
            if total > 1.0 + _PROBABILITY_TOLERANCE:
                msg = f"Transitions for symbol {symbol} sum to {total} > 1"
                raise ValueError(msg)

    @property
    def alphabet(self) -> frozenset[A]:
        """Symbols that have transitions from this state."""
        return frozenset(t.symbol for t in self.transitions)

    def transition_distribution(self, symbol: A) -> Distribution[StateId]:
        """
        Get the distribution over next states given a symbol.

        Args:
            symbol: The input symbol.

        Returns:
            A distribution over target state IDs.

        Raises:
            KeyError: If symbol has no transitions from this state.

        Examples:
            >>> t = Transition(symbol=0, probability=1.0, target='B')
            >>> state = CausalState(id='A', transitions=frozenset({t}))
            >>> dist = state.transition_distribution(0)
            >>> dist['B']
            1.0
        """
        relevant = [t for t in self.transitions if t.symbol == symbol]
        if not relevant:
            msg = f"No transition for symbol {symbol} from state {self.id}"
            raise KeyError(msg)
        return Distribution({t.target: t.probability for t in relevant})

    def emission_distribution(self) -> Distribution[A]:
        """
        Get the distribution over emitted symbols from this state.

        Note: This assumes the machine is "edge-emitting" (symbols on transitions).

        Returns:
            A distribution over symbols that can be emitted from this state.

        Examples:
            >>> t1 = Transition(symbol=0, probability=0.5, target='A')
            >>> t2 = Transition(symbol=1, probability=0.5, target='B')
            >>> state = CausalState(id='A', transitions=frozenset({t1, t2}))
            >>> dist = state.emission_distribution()
            >>> dist[0]
            0.5
        """
        probs: dict[A, float] = {}
        for t in self.transitions:
            probs[t.symbol] = probs.get(t.symbol, 0.0) + t.probability
        return Distribution(probs)

    def next_states(self, symbol: A) -> frozenset[StateId]:
        """
        Get possible next states given a symbol.

        Args:
            symbol: The input symbol.

        Returns:
            Set of state IDs that can be reached with this symbol.

        Examples:
            >>> t = Transition(symbol=0, probability=1.0, target='B')
            >>> state = CausalState(id='A', transitions=frozenset({t}))
            >>> state.next_states(0)
            frozenset({'B'})
        """
        return frozenset(t.target for t in self.transitions if t.symbol == symbol)
