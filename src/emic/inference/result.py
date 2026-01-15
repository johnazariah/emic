"""Inference result container."""

from __future__ import annotations

from collections.abc import Callable, Hashable
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Generic, TypeVar

if TYPE_CHECKING:
    from emic.types import EpsilonMachine

A = TypeVar("A", bound=Hashable)
T = TypeVar("T")


@dataclass(frozen=True)
class InferenceResult(Generic[A]):
    """
    The result of epsilon-machine inference.

    Contains the inferred machine plus diagnostics and quality metrics.

    Attributes:
        machine: The inferred epsilon-machine
        sequence_length: Number of symbols in the input sequence
        max_history_used: Maximum history length considered
        num_histories_considered: Total number of histories analyzed
        converged: Whether the algorithm converged
        iterations: Number of iterations (if applicable)
        warnings: Any warnings generated during inference
    """

    machine: EpsilonMachine[A]

    # Diagnostics
    sequence_length: int
    max_history_used: int
    num_histories_considered: int

    # Convergence info
    converged: bool = True
    iterations: int | None = None

    # Warnings
    warnings: tuple[str, ...] = field(default_factory=tuple)

    def summary(self) -> str:
        """Return a human-readable summary."""
        return (
            f"Inferred ε-machine:\n"
            f"  States: {len(self.machine.states)}\n"
            f"  Alphabet size: {len(self.machine.alphabet)}\n"
            f"  Sequence length: {self.sequence_length}\n"
            f"  Max history: {self.max_history_used}\n"
            f"  Converged: {self.converged}\n"
        )

    def __rshift__(self, func: Callable[[EpsilonMachine[A]], T]) -> T:
        """
        Pipeline operator for chaining analysis.

        Allows: result >> analyze
        """
        return func(self.machine)
