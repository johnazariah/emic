"""State partition for CSSR algorithm."""

from __future__ import annotations

from collections.abc import Hashable
from typing import Generic, TypeVar

A = TypeVar("A", bound=Hashable)


class StatePartition(Generic[A]):
    """
    A partition of histories into equivalence classes (causal states).

    Manages the assignment of histories to states and supports
    split and merge operations.
    """

    def __init__(self) -> None:
        self._history_to_state: dict[tuple[A, ...], str] = {}
        self._state_to_histories: dict[str, set[tuple[A, ...]]] = {}
        self._next_state_id = 0

    def new_state_id(self) -> str:
        """Generate a new unique state ID."""
        state_id = f"S{self._next_state_id}"
        self._next_state_id += 1
        return state_id

    def assign(self, history: tuple[A, ...], state_id: str) -> None:
        """Assign a history to a state."""
        # Remove from old state if reassigning
        old_state = self._history_to_state.get(history)
        if old_state is not None:
            self._state_to_histories[old_state].discard(history)
            if not self._state_to_histories[old_state]:
                del self._state_to_histories[old_state]

        # Assign to new state
        self._history_to_state[history] = state_id
        if state_id not in self._state_to_histories:
            self._state_to_histories[state_id] = set()
        self._state_to_histories[state_id].add(history)

    def get_state(self, history: tuple[A, ...]) -> str | None:
        """Get the state ID for a history."""
        return self._history_to_state.get(history)

    def get_histories(self, state_id: str) -> set[tuple[A, ...]]:
        """Get all histories in a state."""
        return self._state_to_histories.get(state_id, set()).copy()

    def state_ids(self) -> list[str]:
        """Get all state IDs."""
        return list(self._state_to_histories.keys())

    def split_state(
        self,
        state_id: str,
        groups: list[set[tuple[A, ...]]],
    ) -> list[str]:
        """
        Split a state into multiple new states.

        Args:
            state_id: The state to split
            groups: List of history sets, each becoming a new state

        Returns:
            List of new state IDs
        """
        if state_id not in self._state_to_histories:
            return []

        new_state_ids: list[str] = []
        for group in groups:
            new_id = self.new_state_id()
            new_state_ids.append(new_id)
            for history in group:
                self.assign(history, new_id)

        # Clean up old state if empty
        if state_id in self._state_to_histories:
            remaining = self._state_to_histories.get(state_id, set())
            if remaining:
                # Histories not in any group stay in a new state
                new_id = self.new_state_id()
                new_state_ids.append(new_id)
                for history in list(remaining):
                    self.assign(history, new_id)

        return new_state_ids

    def merge_states(self, state_ids: list[str]) -> str:
        """
        Merge multiple states into one.

        Returns:
            The ID of the merged state
        """
        if not state_ids:
            return self.new_state_id()

        target_id = state_ids[0]
        for state_id in state_ids[1:]:
            histories = self.get_histories(state_id)
            for history in histories:
                self.assign(history, target_id)

        return target_id

    def num_states(self) -> int:
        """Number of states in the partition."""
        return len(self._state_to_histories)

    def __eq__(self, other: object) -> bool:
        """Check if two partitions are equivalent."""
        if not isinstance(other, StatePartition):
            return NotImplemented
        return self._history_to_state == other._history_to_state

    def copy(self) -> StatePartition[A]:
        """Create a copy of this partition."""
        new_partition: StatePartition[A] = StatePartition()
        new_partition._next_state_id = self._next_state_id
        new_partition._history_to_state = self._history_to_state.copy()
        new_partition._state_to_histories = {
            k: v.copy() for k, v in self._state_to_histories.items()
        }
        return new_partition
