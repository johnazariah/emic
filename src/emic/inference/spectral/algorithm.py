"""Spectral Learning algorithm implementation.

This implements the spectral learning algorithm for HMMs from:

    Hsu, D., Kakade, S.M., & Zhang, T. (2012).
    "A Spectral Algorithm for Learning Hidden Markov Models"
    Journal of Computer and System Sciences, 78(5), 1460-1480.

The algorithm uses SVD of Hankel matrices to learn observable operator
representations in polynomial time with statistical consistency guarantees.

Architecture:
    This module provides the main Spectral class that orchestrates the
    inference pipeline. The actual computation is delegated to:
    - hankel.py: Hankel matrix construction
    - operators.py: SVD and operator extraction
    - extraction.py: Operator-to-machine conversion
"""

from __future__ import annotations

from collections.abc import Hashable, Iterable
from dataclasses import dataclass
from typing import TYPE_CHECKING, Generic, TypeVar

from emic.inference.errors import InsufficientDataError
from emic.inference.result import InferenceResult
from emic.inference.spectral.extraction import (
    build_machine_from_operators,
    build_trivial_machine,
)
from emic.inference.spectral.hankel import build_hankel_matrices
from emic.inference.spectral.operators import compute_svd, extract_operators

if TYPE_CHECKING:
    from emic.inference.spectral.config import SpectralConfig

A = TypeVar("A", bound=Hashable)


@dataclass
class Spectral(Generic[A]):
    """
    Spectral Learning algorithm for epsilon-machine inference.

    Uses SVD of Hankel matrices to learn observable operator representations,
    then extracts the epsilon-machine from the learned model.

    This is a polynomial-time algorithm that is statistically consistent
    (converges to the true model with enough data).

    Reference:
        Hsu, D., Kakade, S.M., & Zhang, T. (2012).
        "Spectral Algorithm for Learning Hidden Markov Models"

    Examples:
        >>> from emic.sources.synthetic.golden_mean import GoldenMeanSource
        >>> from emic.sources.transforms.take import TakeN
        >>> from emic.inference.spectral import Spectral, SpectralConfig
        >>>
        >>> source = GoldenMeanSource(p=0.5, _seed=42)
        >>> sequence = list(TakeN(10000)(source))
        >>>
        >>> spectral = Spectral(SpectralConfig(max_history=5))
        >>> result = spectral.infer(sequence)
        >>> len(result.machine.states) >= 2  # Should find ~2 states
        True
    """

    config: SpectralConfig

    def infer(
        self,
        sequence: Iterable[A],
        alphabet: frozenset[A] | None = None,
    ) -> InferenceResult[A]:
        """
        Infer epsilon-machine from sequence using spectral methods.

        Args:
            sequence: The observed sequence of symbols.
            alphabet: The set of possible symbols (inferred if not provided).

        Returns:
            InferenceResult containing the inferred machine and diagnostics.

        Raises:
            InsufficientDataError: If sequence is too short for inference.
        """
        symbols = list(sequence)
        n = len(symbols)

        if alphabet is None:
            alphabet = frozenset(symbols)

        alphabet_list = sorted(alphabet, key=str)

        # Get effective parameters (may be adaptive)
        max_history, min_count = self.config.get_effective_params(
            n_samples=n, alphabet_size=len(alphabet_list)
        )

        # Check minimum data requirement
        min_required = min_count * (2 * max_history + 1) * 2
        if n < min_required:
            raise InsufficientDataError(
                required=min_required,
                provided=n,
                algorithm="Spectral",
            )

        # Step 1: Build Hankel matrices
        hankel = build_hankel_matrices(
            symbols=symbols,
            alphabet=alphabet_list,
            max_history=max_history,
            min_count=min_count,
        )

        # Early exit for degenerate cases
        if hankel.is_empty:
            machine = build_trivial_machine(symbols, alphabet)
            return InferenceResult(
                machine=machine,
                sequence_length=n,
                max_history_used=max_history,
                num_histories_considered=0,
                converged=True,
                iterations=1,
            )

        # Step 2: Perform SVD and determine rank
        svd = compute_svd(
            hankel.H,
            rank=self.config.rank,
            rank_threshold=self.config.rank_threshold,
        )

        # Step 3: Extract observable operators
        op_result = extract_operators(
            H_x=hankel.H_x,
            svd=svd,
            alphabet=alphabet_list,
            regularization=self.config.regularization,
        )

        # Step 4: Convert to epsilon-machine
        machine = build_machine_from_operators(
            operators=op_result.operators,
            alphabet=alphabet_list,
            symbols=symbols,
        )

        return InferenceResult(
            machine=machine,
            sequence_length=n,
            max_history_used=max_history,
            num_histories_considered=len(hankel.histories),
            converged=True,
            iterations=op_result.rank,
        )

    def __rrshift__(self, source: Iterable[A]) -> InferenceResult[A]:
        """Support: sequence >> Spectral(config)."""
        alphabet = getattr(source, "alphabet", None)
        return self.infer(source, alphabet=alphabet)
