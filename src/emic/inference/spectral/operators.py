"""Observable operator extraction for spectral learning.

This module implements the SVD-based operator extraction step from the
spectral learning algorithm for HMMs (Hsu et al., 2012).

Observable operators A_x capture the state-transition dynamics conditioned
on observing symbol x:
    A_x = U^T H_x V S^{-1}

where U, S, V come from the SVD of the Hankel matrix H.
"""

from __future__ import annotations

from collections.abc import Hashable
from dataclasses import dataclass
from typing import TYPE_CHECKING, Generic, TypeVar

import numpy as np

if TYPE_CHECKING:
    from numpy.typing import NDArray

A = TypeVar("A", bound=Hashable)


@dataclass(frozen=True)
class SVDResult:
    """Result of SVD decomposition with rank selection.

    Attributes:
        U: Left singular vectors (m x k), where k is the selected rank.
        S: Singular values (k,).
        Vt: Right singular vectors (k x n).
        rank: Selected effective rank.
        singular_values_full: All singular values before truncation (for diagnostics).
    """

    U: NDArray[np.float64]
    S: NDArray[np.float64]
    Vt: NDArray[np.float64]
    rank: int
    singular_values_full: NDArray[np.float64]


@dataclass(frozen=True)
class OperatorResult(Generic[A]):
    """Result of observable operator extraction.

    Attributes:
        operators: Dict mapping each symbol to its kxk observable operator matrix.
        rank: The rank (number of hidden states in the learned model).
        svd: The underlying SVD decomposition.
    """

    operators: dict[A, NDArray[np.float64]]
    rank: int
    svd: SVDResult


def compute_svd(
    H: NDArray[np.float64],
    *,
    rank: int | None = None,
    rank_threshold: float = 0.001,
    use_gap_selection: bool = True,
) -> SVDResult:
    """
    Compute SVD of Hankel matrix and determine effective rank.

    Uses gap-based rank selection by default: finds the largest relative
    gap in the singular value spectrum to separate signal from noise.
    Falls back to threshold-based selection if no clear gap exists.

    Args:
        H: Hankel matrix (m x n).
        rank: Fixed rank to use (overrides automatic selection if provided).
        rank_threshold: Threshold for fallback rank selection. Singular values
            below max_sv * threshold are discarded.
        use_gap_selection: If True, use gap-based rank selection (recommended).
            If False, use threshold-based selection only.

    Returns:
        SVDResult containing truncated SVD components and diagnostics.
    """
    # Full SVD
    U_full, S_full, Vt_full = np.linalg.svd(H, full_matrices=False)

    # Determine rank
    if rank is not None:
        # Use specified rank
        effective_rank = min(rank, len(S_full))
    elif len(S_full) == 0 or S_full[0] < 1e-10:
        effective_rank = 1
    elif use_gap_selection and len(S_full) > 1:
        # Gap-based rank selection: find largest relative drop
        effective_rank = _select_rank_by_gap(S_full)
    else:
        # Threshold-based rank selection
        threshold = S_full[0] * rank_threshold
        effective_rank = int(np.sum(S_full > threshold))
        effective_rank = max(1, effective_rank)

    # Truncate to rank k
    U = U_full[:, :effective_rank]
    S = S_full[:effective_rank]
    Vt = Vt_full[:effective_rank, :]

    return SVDResult(
        U=U,
        S=S,
        Vt=Vt,
        rank=effective_rank,
        singular_values_full=S_full,
    )


def _select_rank_by_gap(
    S: NDArray[np.float64],
) -> int:
    """
    Select rank by finding the largest relative gap in singular values.

    The idea is that "signal" singular values are larger and separated
    from "noise" singular values by a gap. We find where this gap is.

    The algorithm combines two criteria:
    1. Gap size: the relative drop from S[i] to S[i+1]
    2. Absolute threshold: S[i+1] should be small relative to S[0]

    This handles both rank-1 processes (first gap is clear) and
    higher-rank processes (later gaps may be larger but earlier
    singular values are still significant).

    Args:
        S: Singular values in descending order.
        min_threshold: Minimum threshold to avoid keeping very small SVs.

    Returns:
        Selected rank (number of singular values to keep).
    """
    n = len(S)
    if n <= 1:
        return 1

    # Use 1% of max as noise floor
    noise_floor = S[0] * 0.01
    n_above_noise = int(np.sum(noise_floor < S))

    if n_above_noise <= 1:
        return 1

    # For small matrices (2-3 SVs), we can't skip the last gap
    # Just count how many SVs are significant
    if n <= 3:
        # If all SVs are similar magnitude (within 10% of max), keep all
        if S[-1] > S[0] * 0.9:
            return n
        # Otherwise count SVs above 10% of max
        return int(np.sum(S[0] * 0.10 < S))

    # Don't consider gaps at the very end (often just numerical noise)
    n_consider = min(n_above_noise, n - 1)
    if n_consider <= 1:
        return 1

    # Compute relative gaps: (S[i] - S[i+1]) / S[i]
    gaps = np.zeros(n_consider)
    for i in range(n_consider):
        if S[i] > 1e-10:
            gaps[i] = (S[i] - S[i + 1]) / S[i]

    # Special handling for distinguishing rank-1 vs rank-2
    # For rank-1 (i.i.d.): σ₂ is small relative to σ₁
    # For rank-2: both σ₁ and σ₂ are substantial
    if len(S) >= 2:
        relative_sv2 = S[1] / S[0]
        # If σ₂ < 40% of σ₁, strongly prefer rank 1
        if relative_sv2 < 0.40:
            return 1
        # If σ₂ > 45% of σ₁ AND there's a big gap after σ₂, use rank 2
        if relative_sv2 > 0.45 and len(gaps) > 1 and gaps[1] > 0.60:
            return 2

    # Find the largest gap, but only consider the first half of the
    # spectrum to avoid spurious gaps in the noise region
    half = max(2, n_consider // 2)
    best_gap_idx = int(np.argmax(gaps[:half]))

    # Occam's razor: if gap[0] is substantial and the best gap is only
    # slightly larger, prefer the simpler model (rank 1)
    if gaps[0] > 0.50 and best_gap_idx > 0:
        gap_improvement = gaps[best_gap_idx] - gaps[0]
        if gap_improvement < 0.10:
            return 1

    # Accept if the gap is significant (>50%)
    if gaps[best_gap_idx] > 0.50:
        return best_gap_idx + 1

    # If no clear gap in first half, check if there's a VERY large gap later
    all_best_idx = int(np.argmax(gaps))
    if gaps[all_best_idx] > 0.80:
        return all_best_idx + 1

    # Fall back: count SVs that are significant relative to max
    # Use 15% as threshold (more conservative than 10%)
    threshold_rank = int(np.sum(S[0] * 0.15 < S))
    return max(1, min(threshold_rank, 5))


def extract_operators(
    H_x: dict[A, NDArray[np.float64]],
    svd: SVDResult,
    alphabet: list[A],
    regularization: float = 1e-6,
) -> OperatorResult[A]:
    """
    Extract observable operators A_x for each symbol x.

    Following Hsu et al., the observable operator for symbol x is:
        A_x = U^T H_x V S^{-1}

    where U, S, V come from SVD of H.

    Args:
        H_x: Dict mapping each symbol to its conditioned Hankel matrix.
        svd: The SVD result from the main Hankel matrix.
        alphabet: List of all symbols.
        regularization: Regularization for numerical stability.

    Returns:
        OperatorResult containing the observable operators.
    """
    U, S, Vt = svd.U, svd.S, svd.Vt

    # Compute pseudoinverse components with regularization
    S_inv = np.diag(1.0 / (S + regularization))

    # V S^{-1} (n_cols x k matrix)
    V = Vt.T  # (n_cols x k)
    V_Sinv = V @ S_inv  # (n_cols x k)

    operators: dict[A, NDArray[np.float64]] = {}
    for symbol in alphabet:
        Hx = H_x[symbol]
        # A_x = U^T H_x V S^{-1}  -> (k x m) @ (m x n) @ (n x k) = (k x k)
        A_x = U.T @ Hx @ V_Sinv
        operators[symbol] = A_x

    return OperatorResult(
        operators=operators,
        rank=svd.rank,
        svd=svd,
    )
