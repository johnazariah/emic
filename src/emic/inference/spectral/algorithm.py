"""Spectral Learning algorithm implementation.

This implements the spectral learning algorithm for HMMs from:

    Hsu, D., Kakade, S.M., & Zhang, T. (2012).
    "A Spectral Algorithm for Learning Hidden Markov Models"
    Journal of Computer and System Sciences, 78(5), 1460-1480.

The algorithm uses SVD of Hankel matrices to learn observable operator
representations in polynomial time with statistical consistency guarantees.
"""

from __future__ import annotations

from collections.abc import Hashable, Iterable
from dataclasses import dataclass
from typing import TYPE_CHECKING, Generic, TypeVar

import numpy as np

from emic.inference.errors import InsufficientDataError
from emic.inference.result import InferenceResult
from emic.types import CausalState, EpsilonMachine, EpsilonMachineBuilder

if TYPE_CHECKING:
    from numpy.typing import NDArray

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

        # Check minimum data requirement
        min_required = self.config.min_count * (2 * self.config.max_history + 1) * 2
        if n < min_required:
            raise InsufficientDataError(
                required=min_required,
                provided=n,
                algorithm="Spectral",
            )

        if alphabet is None:
            alphabet = frozenset(symbols)

        alphabet_list = sorted(alphabet, key=str)

        # Build Hankel matrices
        H, H_x, histories, _ = self._build_hankel_matrices(symbols, alphabet_list)

        # Early exit for degenerate cases
        if H.size == 0 or H.shape[0] == 0 or H.shape[1] == 0:
            machine = self._build_trivial_machine(symbols, alphabet)
            return InferenceResult(
                machine=machine,
                sequence_length=n,
                max_history_used=self.config.max_history,
                num_histories_considered=0,
                converged=True,
                iterations=1,
            )

        # Perform SVD and determine rank
        U, S, Vt, rank = self._compute_svd(H)

        # Extract observable operators
        operators = self._extract_operators(H, H_x, U, S, Vt, rank, alphabet_list)

        # Convert to epsilon-machine
        machine = self._build_machine_from_operators(operators, alphabet_list, symbols)

        return InferenceResult(
            machine=machine,
            sequence_length=n,
            max_history_used=self.config.max_history,
            num_histories_considered=len(histories),
            converged=True,
            iterations=rank,
        )

    def _build_hankel_matrices(
        self,
        symbols: list[A],
        alphabet: list[A],
    ) -> tuple[
        NDArray[np.float64],
        dict[A, NDArray[np.float64]],
        list[tuple[A, ...]],
        list[tuple[A, ...]],
    ]:
        """
        Build the Hankel matrix and symbol-conditioned Hankel matrices.

        The Hankel matrix H[i,j] = P(future_j | history_i)
        The conditioned matrix H_x[i,j] = P(x followed by rest of future_j | history_i)

        Returns:
            H: The main Hankel matrix
            H_x: Dict mapping each symbol to its conditioned Hankel matrix
            histories: List of history tuples (row labels)
            futures: List of future tuples (column labels)
        """
        L = self.config.max_history
        n = len(symbols)

        # Count occurrences of (history, future) pairs
        pair_counts: dict[tuple[tuple[A, ...], tuple[A, ...]], int] = {}
        history_counts: dict[tuple[A, ...], int] = {}

        # Count (history, symbol, remaining_future) for conditioned matrices
        # H_x[h, f] = count of seeing h followed by x followed by f[1:]
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
        min_count = self.config.min_count
        valid_pairs = {k: v for k, v in pair_counts.items() if v >= min_count}

        if not valid_pairs:
            empty_h: NDArray[np.float64] = np.zeros((0, 0), dtype=np.float64)
            return (
                empty_h,
                {s: np.zeros((0, 0), dtype=np.float64) for s in alphabet},
                [],
                [],
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
            return (
                empty_h2,
                {s: np.zeros((0, 0), dtype=np.float64) for s in alphabet},
                [],
                [],
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

        return H, H_x, histories, futures

    def _compute_svd(
        self,
        H: NDArray[np.float64],
    ) -> tuple[
        NDArray[np.float64],
        NDArray[np.float64],
        NDArray[np.float64],
        int,
    ]:
        """
        Compute SVD of Hankel matrix and determine effective rank.

        Uses singular value threshold to determine rank, or uses
        explicitly specified rank from config.

        Returns:
            U: Left singular vectors (m x k)
            S: Singular values (k,)
            Vt: Right singular vectors (k x n)
            rank: Effective rank
        """
        # Full SVD
        U_full, S_full, Vt_full = np.linalg.svd(H, full_matrices=False)

        # Determine rank
        if self.config.rank is not None:
            # Use specified rank
            rank = min(self.config.rank, len(S_full))
        else:
            # Use threshold-based rank selection
            if len(S_full) == 0 or S_full[0] < 1e-10:
                rank = 1
            else:
                threshold = S_full[0] * self.config.rank_threshold
                rank = int(np.sum(S_full > threshold))
                rank = max(1, rank)  # At least rank 1

        # Truncate to rank k
        U = U_full[:, :rank]
        S = S_full[:rank]
        Vt = Vt_full[:rank, :]

        return U, S, Vt, rank

    def _extract_operators(
        self,
        _H: NDArray[np.float64],
        H_x: dict[A, NDArray[np.float64]],
        U: NDArray[np.float64],
        S: NDArray[np.float64],
        Vt: NDArray[np.float64],
        _rank: int,
        alphabet: list[A],
    ) -> dict[A, NDArray[np.float64]]:
        """
        Extract observable operators A_x for each symbol x.

        Following Hsu et al., the observable operator for symbol x is:
            A_x = U^T H_x V S^{-1}

        where U, S, V come from SVD of H.

        Returns:
            Dict mapping each symbol to its kxk observable operator matrix.
        """
        # Compute pseudoinverse components with regularization
        reg = self.config.regularization
        S_inv = np.diag(1.0 / (S + reg))

        # V S^{-1} (n_cols x k matrix)
        V = Vt.T  # (n_cols x k)
        V_Sinv = V @ S_inv  # (n_cols x k)

        operators: dict[A, NDArray[np.float64]] = {}
        for symbol in alphabet:
            Hx = H_x[symbol]
            # A_x = U^T H_x V S^{-1}  -> (k x m) @ (m x n) @ (n x k) = (k x k)
            A_x = U.T @ Hx @ V_Sinv
            operators[symbol] = A_x

        return operators

    def _build_machine_from_operators(
        self,
        operators: dict[A, NDArray[np.float64]],
        alphabet: list[A],
        symbols: list[A],
    ) -> EpsilonMachine[A]:
        """
        Build epsilon-machine from observable operators.

        Strategy:
        1. Use eigenvectors of sum of operators to identify state basis
        2. Compute stationary distribution for initial state
        3. Extract transition probabilities from operator structure
        """
        if not operators or not alphabet:
            return self._build_trivial_machine(symbols, frozenset(alphabet))

        # Stack all operators
        ops_list = [operators[s] for s in alphabet]
        k = ops_list[0].shape[0]

        if k == 0:
            return self._build_trivial_machine(symbols, frozenset(alphabet))

        # Sum of operators (related to transition matrix)
        T: NDArray[np.float64] = np.sum(np.stack(ops_list), axis=0)

        # Find stationary distribution via left eigenvector
        try:
            eigenvalues, eigenvectors = np.linalg.eig(T.T)
            # Find eigenvector for eigenvalue ≈ 1
            idx = np.argmin(np.abs(eigenvalues - 1.0))
            pi = np.real(eigenvectors[:, idx])
            pi = np.abs(pi)
            pi = pi / (np.sum(pi) + 1e-10)
        except np.linalg.LinAlgError:
            pi = np.ones(k) / k

        # Build transition matrix by analyzing operators
        # For each state i, compute P(x, j | i) from operators
        builder: EpsilonMachineBuilder[A] = EpsilonMachineBuilder()

        # Compute emission and transition probabilities
        for i in range(k):
            state_i = f"S{i}"
            emissions: dict[A, float] = {}
            transitions: dict[A, int] = {}

            for symbol in alphabet:
                A_x = operators[symbol]
                # Row i of A_x gives transition weights from state i
                row = A_x[i, :]

                # Emission probability proportional to sum of row
                emissions[symbol] = max(0.0, float(np.sum(np.abs(row))))

                # Most likely next state is argmax of row
                if np.any(np.abs(row) > 1e-10):
                    transitions[symbol] = int(np.argmax(np.abs(row)))
                else:
                    transitions[symbol] = i  # Self-loop if no clear transition

            # Normalize emissions
            total_emission = sum(emissions.values())
            if total_emission < 1e-10:
                # Uniform if no emissions
                for symbol in alphabet:
                    emissions[symbol] = 1.0 / len(alphabet)
                total_emission = 1.0

            # Add transitions
            for symbol in alphabet:
                prob = emissions[symbol] / total_emission
                if prob > 1e-10:
                    target = f"S{transitions[symbol]}"
                    builder.add_transition(state_i, symbol, target, prob)

        # Determine start state (highest stationary probability)
        start_idx = int(np.argmax(pi))
        builder.with_start_state(f"S{start_idx}")

        machine = builder.build()

        # Post-process: merge near-identical states
        machine = self._merge_similar_states(machine, alphabet)

        return machine

    def _merge_similar_states(
        self,
        machine: EpsilonMachine[A],
        alphabet: list[A],
    ) -> EpsilonMachine[A]:
        """
        Merge states with nearly identical emission/transition distributions.

        This reduces over-splitting by combining states that behave identically.
        Uses iterative refinement to handle target remapping.
        """
        current = machine
        max_iterations = 10

        for _ in range(max_iterations):
            merged = self._merge_pass(current, alphabet)
            if len(merged.states) == len(current.states):
                break  # No more merging possible
            current = merged

        return current

    def _merge_pass(
        self,
        machine: EpsilonMachine[A],
        alphabet: list[A],
    ) -> EpsilonMachine[A]:
        """Single pass of state merging."""
        states = list(machine.states)
        n_states = len(states)

        if n_states <= 1:
            return machine

        # Build lookup from state_id to CausalState
        state_lookup: dict[str, CausalState[A]] = {s.id: s for s in states}

        # Compute emission distribution for each state (ignoring targets initially)
        def emission_signature(state_id: str) -> tuple[float, ...]:
            """Get emission probability vector for a state."""
            state = state_lookup.get(state_id)
            if state is None:
                return ()

            emissions: list[float] = []
            trans_by_symbol: dict[A, float] = {}
            for t in state.transitions:
                trans_by_symbol[t.symbol] = trans_by_symbol.get(t.symbol, 0.0) + t.probability

            for symbol in sorted(alphabet, key=str):
                emissions.append(trans_by_symbol.get(symbol, 0.0))
            return tuple(emissions)

        def emissions_similar(em1: tuple[float, ...], em2: tuple[float, ...]) -> bool:
            """Check if two emission signatures are similar within threshold."""
            if len(em1) != len(em2):
                return False
            diff = sum(abs(e1 - e2) for e1, e2 in zip(em1, em2, strict=True))
            # Lenient threshold - 25% total variation for noisy spectral estimates
            return diff < 0.25

        # Group states by similar emission distributions (ignoring targets)
        state_ids = [s.id for s in states]
        state_groups: dict[int, list[str]] = {}
        state_to_group: dict[str, int] = {}
        group_id = 0

        for state_id in state_ids:
            sig = emission_signature(state_id)
            found_group = False

            for gid, group_states in state_groups.items():
                rep_sig = emission_signature(group_states[0])
                if emissions_similar(sig, rep_sig):
                    state_groups[gid].append(state_id)
                    state_to_group[state_id] = gid
                    found_group = True
                    break

            if not found_group:
                state_groups[group_id] = [state_id]
                state_to_group[state_id] = group_id
                group_id += 1

        # If no merging possible, return original
        if len(state_groups) == n_states:
            return machine

        # Build merged machine
        builder: EpsilonMachineBuilder[A] = EpsilonMachineBuilder()

        # Map groups to new state names
        group_rep: dict[int, str] = {gid: f"S{gid}" for gid in state_groups}

        # For each group, compute average emission probabilities and transition targets
        for gid, group_states in state_groups.items():
            new_state = group_rep[gid]

            # Average emissions across all states in group
            emission_totals: dict[A, float] = dict.fromkeys(alphabet, 0.0)
            target_votes: dict[A, dict[int, int]] = {s: {} for s in alphabet}

            for sid in group_states:
                state = state_lookup.get(sid)
                if state is None:
                    continue
                for t in state.transitions:
                    emission_totals[t.symbol] += t.probability
                    target_group = state_to_group.get(t.target, 0)
                    target_votes[t.symbol][target_group] = (
                        target_votes[t.symbol].get(target_group, 0) + 1
                    )

            n_group = len(group_states)
            for symbol in alphabet:
                avg_prob = emission_totals[symbol] / n_group if n_group > 0 else 0.0
                if avg_prob > 1e-6:
                    # Most common target group for this symbol
                    if target_votes[symbol]:
                        best_target_group = max(target_votes[symbol].items(), key=lambda x: x[1])[0]
                    else:
                        best_target_group = gid
                    target_state = group_rep.get(best_target_group, new_state)
                    builder.add_transition(new_state, symbol, target_state, avg_prob)

        # Set start state
        if machine.start_state:
            start_group = state_to_group.get(machine.start_state, 0)
            builder.with_start_state(group_rep.get(start_group, "S0"))
        else:
            builder.with_start_state("S0")

        return builder.build()

    def _build_trivial_machine(
        self,
        symbols: list[A],
        alphabet: frozenset[A],
    ) -> EpsilonMachine[A]:
        """Build a single-state machine when spectral decomposition fails."""
        builder: EpsilonMachineBuilder[A] = EpsilonMachineBuilder()

        # Count symbol frequencies
        counts: dict[A, int] = {}
        for s in symbols:
            counts[s] = counts.get(s, 0) + 1

        total = len(symbols) if symbols else 1

        # Add self-loop transitions with empirical probabilities
        for symbol in alphabet:
            prob = counts.get(symbol, 0) / total
            if prob > 0:
                builder.add_transition("S0", symbol, "S0", prob)

        # If no transitions added, use uniform
        if not counts:
            for symbol in alphabet:
                builder.add_transition("S0", symbol, "S0", 1.0 / len(alphabet))

        builder.with_start_state("S0")
        return builder.build()

    def __rrshift__(self, source: Iterable[A]) -> InferenceResult[A]:
        """Support: sequence >> Spectral(config)."""
        alphabet = getattr(source, "alphabet", None)
        return self.infer(source, alphabet=alphabet)
