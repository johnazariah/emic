"""Epsilon-machine types."""

from __future__ import annotations

from collections.abc import Hashable
from dataclasses import dataclass
from typing import TYPE_CHECKING, Generic, TypeVar

from emic.types.probability import Distribution
from emic.types.states import CausalState, StateId, Transition

if TYPE_CHECKING:
    from typing import Self

A = TypeVar("A", bound=Hashable)


@dataclass(frozen=True)
class EpsilonMachine(Generic[A]):
    """
    An epsilon-machine (ε-machine) over alphabet A.

    An ε-machine is the minimal, optimal predictor of a stationary stochastic
    process. It consists of:
    - A finite set of causal states
    - Labeled transitions between states
    - A stationary distribution over states

    Properties:
    - Unifilarity: Each (state, symbol) pair has at most one outgoing transition
    - Minimality: No two states have the same conditional future distribution

    This class represents the result of inference - the discovered structure.

    Attributes:
        alphabet: The set of symbols used by this machine.
        states: The set of causal states.
        start_state: The ID of the initial state.
        stationary_distribution: The steady-state distribution over states.

    Examples:
        >>> from emic.types import EpsilonMachineBuilder
        >>> machine = (
        ...     EpsilonMachineBuilder[int]()
        ...     .add_transition("A", 0, "A", 0.5)
        ...     .add_transition("A", 1, "B", 0.5)
        ...     .add_transition("B", 0, "A", 1.0)
        ...     .with_start_state("A")
        ...     .build()
        ... )
        >>> len(machine)
        2
        >>> machine.is_unifilar()
        True
    """

    alphabet: frozenset[A]
    states: frozenset[CausalState[A]]
    start_state: StateId
    stationary_distribution: Distribution[StateId]

    def __post_init__(self) -> None:
        """Validate machine invariants."""
        # Validate start state exists
        state_ids = frozenset(s.id for s in self.states)
        if self.start_state not in state_ids:
            msg = f"Start state {self.start_state} not in states"
            raise ValueError(msg)

        # Validate stationary distribution is over states
        for state_id in self.stationary_distribution.support:
            if state_id not in state_ids:
                msg = f"Stationary distribution contains unknown state {state_id}"
                raise ValueError(msg)

        # Validate unifilarity
        for state in self.states:
            seen: dict[A, StateId] = {}
            for t in state.transitions:
                if t.symbol in seen and seen[t.symbol] != t.target:
                    msg = (
                        f"State {state.id} violates unifilarity: "
                        f"symbol {t.symbol} goes to both {seen[t.symbol]} and {t.target}"
                    )
                    raise ValueError(msg)
                seen[t.symbol] = t.target

    def __len__(self) -> int:
        """Number of causal states."""
        return len(self.states)

    @property
    def state_ids(self) -> frozenset[StateId]:
        """Set of all state IDs."""
        return frozenset(s.id for s in self.states)

    def get_state(self, state_id: StateId) -> CausalState[A]:
        """
        Get a state by ID.

        Args:
            state_id: The ID of the state to retrieve.

        Returns:
            The CausalState with the given ID.

        Raises:
            KeyError: If state not found.

        Examples:
            >>> from emic.types import EpsilonMachineBuilder
            >>> machine = (
            ...     EpsilonMachineBuilder[int]()
            ...     .add_transition("A", 0, "A", 1.0)
            ...     .with_start_state("A")
            ...     .build()
            ... )
            >>> state = machine.get_state("A")
            >>> state.id
            'A'
        """
        for state in self.states:
            if state.id == state_id:
                return state
        msg = f"State {state_id} not found"
        raise KeyError(msg)

    def transition_matrix(self, symbol: A) -> dict[StateId, Distribution[StateId]]:
        """
        Get the transition matrix for a given symbol.

        Returns a mapping from source state to distribution over target states.
        Only states that have transitions for the given symbol are included.

        Args:
            symbol: The symbol to get transitions for.

        Returns:
            A dict mapping state IDs to distributions over next states.

        Examples:
            >>> from emic.types import EpsilonMachineBuilder
            >>> machine = (
            ...     EpsilonMachineBuilder[int]()
            ...     .add_transition("A", 0, "B", 1.0)
            ...     .add_transition("B", 0, "A", 1.0)
            ...     .with_start_state("A")
            ...     .build()
            ... )
            >>> matrix = machine.transition_matrix(0)
            >>> matrix["A"]["B"]
            1.0
        """
        result: dict[StateId, Distribution[StateId]] = {}
        for state in self.states:
            if symbol in state.alphabet:
                result[state.id] = state.transition_distribution(symbol)
        return result

    def is_unifilar(self) -> bool:
        """
        Check if machine is unifilar (deterministic given state and symbol).

        A machine is unifilar if, for each state, each symbol leads to at most
        one target state. This is a fundamental property of epsilon-machines.

        Returns:
            True if the machine is unifilar, False otherwise.

        Examples:
            >>> from emic.types import EpsilonMachineBuilder
            >>> machine = (
            ...     EpsilonMachineBuilder[int]()
            ...     .add_transition("A", 0, "A", 1.0)
            ...     .with_start_state("A")
            ...     .build()
            ... )
            >>> machine.is_unifilar()
            True
        """
        for state in self.states:
            symbols_seen: set[A] = set()
            for t in state.transitions:
                if t.symbol in symbols_seen:
                    return False
                symbols_seen.add(t.symbol)
        return True

    def is_ergodic(self) -> bool:
        """
        Check if machine is ergodic (single recurrent class).

        Returns:
            True if the machine is ergodic, False otherwise.

        Raises:
            NotImplementedError: This method is not yet implemented.
        """
        # TODO: Implement graph connectivity check
        raise NotImplementedError


class EpsilonMachineBuilder(Generic[A]):
    """
    Mutable builder for constructing EpsilonMachine instances.

    Since EpsilonMachine is immutable, this builder provides an ergonomic
    way to construct machines incrementally.

    Examples:
        >>> machine = (
        ...     EpsilonMachineBuilder[int]()
        ...     .with_alphabet({0, 1})
        ...     .add_state("A")
        ...     .add_state("B")
        ...     .add_transition("A", 0, "A", 0.5)
        ...     .add_transition("A", 1, "B", 0.5)
        ...     .add_transition("B", 0, "A", 1.0)
        ...     .with_start_state("A")
        ...     .build()
        ... )
        >>> len(machine)
        2
    """

    def __init__(self) -> None:
        """Initialize an empty builder."""
        self._alphabet: set[A] = set()
        self._states: dict[StateId, list[Transition[A]]] = {}
        self._start_state: StateId | None = None
        self._stationary: dict[StateId, float] | None = None

    def with_alphabet(self, symbols: set[A]) -> Self:
        """
        Set the alphabet for the machine.

        Args:
            symbols: The set of symbols to use.

        Returns:
            Self for method chaining.
        """
        self._alphabet = symbols
        return self

    def add_state(self, state_id: StateId) -> Self:
        """
        Add a state to the machine.

        Args:
            state_id: The ID of the state to add.

        Returns:
            Self for method chaining.
        """
        if state_id not in self._states:
            self._states[state_id] = []
        return self

    def add_transition(
        self,
        source: StateId,
        symbol: A,
        target: StateId,
        probability: float,
    ) -> Self:
        """
        Add a transition to the machine.

        This will also add the source and target states if they don't exist,
        and add the symbol to the alphabet.

        Args:
            source: The source state ID.
            symbol: The symbol emitted on this transition.
            target: The target state ID.
            probability: The probability of this transition.

        Returns:
            Self for method chaining.
        """
        self.add_state(source)
        self.add_state(target)
        self._alphabet.add(symbol)
        self._states[source].append(Transition(symbol, probability, target))
        return self

    def with_start_state(self, state_id: StateId) -> Self:
        """
        Set the start state for the machine.

        Args:
            state_id: The ID of the start state.

        Returns:
            Self for method chaining.
        """
        self._start_state = state_id
        return self

    def with_stationary_distribution(
        self,
        dist: dict[StateId, float],
    ) -> Self:
        """
        Set the stationary distribution for the machine.

        Args:
            dist: A mapping from state IDs to probabilities.

        Returns:
            Self for method chaining.
        """
        self._stationary = dist
        return self

    def build(self) -> EpsilonMachine[A]:
        """
        Build the EpsilonMachine.

        Returns:
            The constructed EpsilonMachine.

        Raises:
            ValueError: If start state is not set.
        """
        if self._start_state is None:
            msg = "Start state not set"
            raise ValueError(msg)

        states = frozenset(
            CausalState(id=sid, transitions=frozenset(trans)) for sid, trans in self._states.items()
        )

        # Compute stationary distribution if not provided
        if self._stationary is None:
            self._stationary = self._compute_stationary_distribution()

        return EpsilonMachine(
            alphabet=frozenset(self._alphabet),
            states=states,
            start_state=self._start_state,
            stationary_distribution=Distribution(self._stationary),
        )

    def _compute_stationary_distribution(self) -> dict[StateId, float]:
        """
        Compute the stationary distribution by solving π = π P.

        Uses power iteration for simplicity and robustness.
        Pure Python implementation - no numpy dependency.

        For machines with absorbing states or incomplete transitions,
        falls back to uniform distribution.
        """
        state_ids = list(self._states.keys())
        n = len(state_ids)
        if n == 0:
            return {}
        if n == 1:
            return {state_ids[0]: 1.0}

        # Build transition matrix P[i][j] = prob of going from state i to state j
        state_idx = {sid: i for i, sid in enumerate(state_ids)}
        P: list[list[float]] = [[0.0] * n for _ in range(n)]

        for sid, transitions in self._states.items():
            i = state_idx[sid]
            row_sum = 0.0
            for t in transitions:
                if t.target in state_idx:
                    j = state_idx[t.target]
                    P[i][j] += t.probability
                    row_sum += t.probability
            # Check if row sums to ~1 (proper stochastic matrix)
            if abs(row_sum - 1.0) > 0.01:
                # Not a proper stochastic matrix, use uniform
                return dict.fromkeys(state_ids, 1.0 / n)

        # Power iteration to find stationary distribution
        # Start with uniform
        pi = [1.0 / n] * n

        for _ in range(1000):  # Max iterations
            # Compute pi_new = pi @ P (matrix-vector multiplication)
            pi_new = [0.0] * n
            for j in range(n):
                for i in range(n):
                    pi_new[j] += pi[i] * P[i][j]

            # Normalize to handle numerical errors
            total = sum(pi_new)
            if total <= 0:
                # Degenerate case, use uniform
                return {state_ids[i]: 1.0 / n for i in range(n)}
            pi_new = [p / total for p in pi_new]

            # Check convergence
            max_diff = max(abs(pi_new[i] - pi[i]) for i in range(n))
            if max_diff < 1e-10:
                break
            pi = pi_new

        # Final validation
        total = sum(pi)
        if total <= 0:
            return {state_ids[i]: 1.0 / n for i in range(n)}

        return {state_ids[i]: pi[i] for i in range(n)}
