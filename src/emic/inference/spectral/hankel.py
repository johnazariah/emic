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

    The Hankel matrix H[i,j] = P(future_j | history_i)
    The conditioned matrix H_x[i,j] = P(x followed by rest of future_j | history_i)

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

    # Count occurrences of (history, future) pairs
    pair_counts: dict[tuple[tuple[A, ...], tuple[A, ...]], int] = {}
    history_counts: dict[tuple[A, ...], int] = {}

    # Count (history, symbol, remaining_future) for conditioned matrices
    symbol_pair_counts: dict[A, dict[tuple[tuple[A, ...], tuple[A, ...]], int]] = {
        s: {} for s in alphabet
    }

    for i in range(L, n - L):
        # Use fixed-length histories and futures for rectangular matrix
        history = tuple(symbols[i - L : i])
        future = tuple(symbols[i : i + L])

        key = (history, future)
        pair_counts[key] = pair_counts.get(key, 0) + 1
        history_counts[history] = history_counts.get(history, 0) + 1

        # For H_x, the first symbol of future determines which matrix
        if len(future) > 0:
            first_symbol = future[0]
            if first_symbol in symbol_pair_counts:
                symbol_pair_counts[first_symbol][key] = (
                    symbol_pair_counts[first_symbol].get(key, 0) + 1
                )

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

    # Build main Hankel matrix (normalized by history counts)
    H = np.zeros((m, n_cols), dtype=np.float64)
    for (h, f), count in valid_pairs.items():
        i, j = history_idx[h], future_idx[f]
        h_count = history_counts.get(h, 1)
        H[i, j] = count / h_count

    # Build symbol-conditioned matrices
    H_x: dict[A, NDArray[np.float64]] = {}
    for symbol in alphabet:
        Hx = np.zeros((m, n_cols), dtype=np.float64)
        for (h, f), count in symbol_pair_counts[symbol].items():
            if h in history_idx and f in future_idx:
                i, j = history_idx[h], future_idx[f]
                h_count = history_counts.get(h, 1)
                Hx[i, j] = count / h_count
        H_x[symbol] = Hx

    return HankelResult(H=H, H_x=H_x, histories=histories, futures=futures)
