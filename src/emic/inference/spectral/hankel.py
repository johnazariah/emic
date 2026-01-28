"""Hankel matrix construction for spectral learning.

This module implements the Hankel matrix construction step from the
spectral learning algorithm for HMMs (Hsu et al., 2012).

The Hankel matrix H captures the joint probabilities of history-future pairs:
    H[i,j] ≈ P(future_j | history_i)

Symbol-conditioned Hankel matrices H_x capture:
    H_x[i,j] ≈ P(x followed by rest of future_j | history_i)
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
class HankelResult(Generic[A]):
    """Result of Hankel matrix construction.

    Attributes:
        H: Main Hankel matrix (m x n), where m = # histories, n = # futures.
        H_x: Dict mapping each symbol to its conditioned Hankel matrix.
        histories: List of history tuples (row labels).
        futures: List of future tuples (column labels).
    """

    H: NDArray[np.float64]
    H_x: dict[A, NDArray[np.float64]]
    histories: list[tuple[A, ...]]
    futures: list[tuple[A, ...]]

    @property
    def is_empty(self) -> bool:
        """Check if the Hankel matrix is empty/degenerate."""
        return self.H.size == 0 or self.H.shape[0] == 0 or self.H.shape[1] == 0


def build_hankel_matrices(
    symbols: list[A],
    alphabet: list[A],
    max_history: int,
    min_count: int = 5,
) -> HankelResult[A]:
    """
    Build the Hankel matrix and symbol-conditioned Hankel matrices.

    Following Hsu et al. (2012):
        H[h, f] ≈ P(history h followed by future f)
        H_x[h, f] ≈ P(history h followed by symbol x followed by future f)

    The key distinction is that H_x conditions on a SINGLE symbol x between
    the history and future, not on the future starting with x.

    Args:
        symbols: The observed sequence of symbols.
        alphabet: List of all possible symbols.
        max_history: Length of history/future windows.
        min_count: Minimum observations for a (history, future) pair to be included.

    Returns:
        HankelResult containing the matrices and their row/column labels.
    """
    L = max_history
    n = len(symbols)

    # For H: Count (history, future) pairs where history=[i-L:i], future=[i:i+L]
    # For H_x: Count (history, x, future) where history=[i-L:i], x=symbols[i], future=[i+1:i+1+L]

    # Count occurrences of (history, future) pairs for H
    pair_counts: dict[tuple[tuple[A, ...], tuple[A, ...]], int] = {}
    total_pairs = 0

    # Count (history, x, future) for H_x - note future is SHIFTED by 1
    # H_x[h, f] = count of seeing h, then x, then f
    symbol_triple_counts: dict[A, dict[tuple[tuple[A, ...], tuple[A, ...]], int]] = {
        s: {} for s in alphabet
    }

    for i in range(L, n - L):
        # For main Hankel matrix H
        history = tuple(symbols[i - L : i])
        future = tuple(symbols[i : i + L])

        key = (history, future)
        pair_counts[key] = pair_counts.get(key, 0) + 1
        total_pairs += 1

        # For H_x: the symbol at position i is the conditioning symbol
        # The future is symbols[i+1 : i+1+L]
        if i + L < n:  # Make sure we have enough symbols for the shifted future
            x = symbols[i]
            future_shifted = tuple(symbols[i + 1 : i + 1 + L])
            if x in symbol_triple_counts:
                triple_key = (history, future_shifted)
                symbol_triple_counts[x][triple_key] = symbol_triple_counts[x].get(triple_key, 0) + 1

    # Filter by minimum count
    valid_pairs = {k: v for k, v in pair_counts.items() if v >= min_count}

    if not valid_pairs:
        empty_h: NDArray[np.float64] = np.zeros((0, 0), dtype=np.float64)
        return HankelResult(
            H=empty_h,
            H_x={s: np.zeros((0, 0), dtype=np.float64) for s in alphabet},
            histories=[],
            futures=[],
        )

    # Get unique histories and futures that appear in valid pairs
    history_set: set[tuple[A, ...]] = set()
    future_set: set[tuple[A, ...]] = set()
    for h, f in valid_pairs:
        history_set.add(h)
        future_set.add(f)

    histories = sorted(history_set, key=str)
    futures = sorted(future_set, key=str)

    if not histories or not futures:
        empty_h2: NDArray[np.float64] = np.zeros((0, 0), dtype=np.float64)
        return HankelResult(
            H=empty_h2,
            H_x={s: np.zeros((0, 0), dtype=np.float64) for s in alphabet},
            histories=[],
            futures=[],
        )

    m, n_cols = len(histories), len(futures)
    history_idx = {h: i for i, h in enumerate(histories)}
    future_idx = {f: j for j, f in enumerate(futures)}

    # Build main Hankel matrix with JOINT probabilities P(history, future)
    H = np.zeros((m, n_cols), dtype=np.float64)
    for (h, f), count in valid_pairs.items():
        i, j = history_idx[h], future_idx[f]
        H[i, j] = count / total_pairs

    # Build symbol-conditioned matrices with joint probabilities
    # H_x[h, f] = P(h, x, f) = count(h, x, f) / total
    H_x: dict[A, NDArray[np.float64]] = {}
    for symbol in alphabet:
        Hx = np.zeros((m, n_cols), dtype=np.float64)
        for (h, f), count in symbol_triple_counts[symbol].items():
            if h in history_idx and f in future_idx:
                i, j = history_idx[h], future_idx[f]
                Hx[i, j] = count / total_pairs
        H_x[symbol] = Hx

    return HankelResult(H=H, H_x=H_x, histories=histories, futures=futures)
