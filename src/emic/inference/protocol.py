"""Protocol for inference algorithms."""

from __future__ import annotations

from collections.abc import Hashable, Iterable
from typing import TYPE_CHECKING, Protocol, TypeVar

if TYPE_CHECKING:
    from emic.inference.result import InferenceResult

A = TypeVar("A", bound=Hashable)


class InferenceAlgorithm(Protocol[A]):
    """
    Protocol for epsilon-machine inference algorithms.

    Any algorithm that can infer an epsilon-machine from a sequence
    of symbols satisfies this protocol.

    Examples:
        >>> class MyAlgorithm:
        ...     def infer(self, sequence, alphabet=None):
        ...         ...  # Return InferenceResult
    """

    def infer(
        self,
        sequence: Iterable[A],
        alphabet: frozenset[A] | None = None,
    ) -> InferenceResult[A]:
        """
        Infer an epsilon-machine from the given sequence.

        Args:
            sequence: The observed symbols
            alphabet: Known alphabet (inferred from sequence if None)

        Returns:
            InferenceResult containing the machine and diagnostics
        """
        ...
