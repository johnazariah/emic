"""Causal State Merging (CSM) algorithm implementation."""

from __future__ import annotations

import math
from collections.abc import Hashable, Iterable
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Generic, TypeVar

from emic.inference.errors import InsufficientDataError
from emic.inference.result import InferenceResult
from emic.types import EpsilonMachine, EpsilonMachineBuilder

if TYPE_CHECKING:
    from emic.inference.csm.config import CSMConfig

A = TypeVar("A", bound=Hashable)


@dataclass
class HistoryStats(Generic[A]):
    """
    Statistics for a single history string.

    Attributes:
        history: The history tuple
        count: Number of times this history was observed
        next_symbol_counts: Count of each following symbol
    """

    history: tuple[A, ...]
    count: int = 0
    next_symbol_counts: dict[A, int] = field(default_factory=lambda: {})

    def add_observation(self, next_symbol: A) -> None:
        """Record an observation of this history followed by next_symbol."""
        self.count += 1
        self.next_symbol_counts[next_symbol] = self.next_symbol_counts.get(next_symbol, 0) + 1

    @property
    def next_symbol_distribution(self) -> dict[A, float]:
        """Probability distribution over the next symbol."""
        total = sum(self.next_symbol_counts.values())
        if total == 0:
            return {}
        return {s: c / total for s, c in self.next_symbol_counts.items()}


@dataclass
class MergeInfo:
    """Information about a merge in the hierarchy."""

    state1: str
    state2: str
    merged_state: str
    distance: float


@dataclass
class CSM(Generic[A]):
    """
    Causal State Merging algorithm.

    Infers an epsilon-machine from an observed sequence by:
    1. Creating a state for each unique history of the specified length
    2. Computing pairwise distances between state predictive distributions
    3. Iteratively merging the closest pair until threshold is exceeded

    This is a bottom-up approach that complements CSSR's top-down splitting.

    Reference:
        This implementation follows the state-merging approach described
        in computational mechanics literature as an alternative to CSSR.

    Examples:
        >>> from emic.sources.synthetic.golden_mean import GoldenMeanSource
        >>> from emic.sources.transforms.take import TakeN
        >>> from emic.inference.csm import CSM, CSMConfig
        >>>
        >>> source = GoldenMeanSource(p=0.5, _seed=42)
        >>> sequence = list(TakeN(10000)(source))
        >>>
        >>> csm = CSM(CSMConfig(history_length=5))
        >>> result = csm.infer(sequence)
        >>> len(result.machine.states)
        2
    """

    config: CSMConfig

    def infer(
        self,
        sequence: Iterable[A],
        alphabet: frozenset[A] | None = None,
    ) -> InferenceResult[A]:
        """
        Infer epsilon-machine from sequence.

        Args:
            sequence: The observed sequence of symbols.
            alphabet: The set of possible symbols (inferred if not provided).

        Returns:
            InferenceResult containing the inferred machine and diagnostics.

        Raises:
            InsufficientDataError: If sequence is too short for inference.
        """
        # Convert to list for multiple passes
        symbols = list(sequence)
        n = len(symbols)

        # Check minimum data requirement
        min_required = self.config.min_count * (self.config.history_length + 1) * 2
        if n < min_required:
            raise InsufficientDataError(
                required=min_required,
                provided=n,
                algorithm="CSM",
            )

        # Infer alphabet if not provided
        if alphabet is None:
            alphabet = frozenset(symbols)

        # Collect history statistics
        history_stats = self._collect_history_stats(symbols)

        # Initialize partition: each valid history is its own state
        partition, state_to_histories = self._initialize_partition(history_stats)

        if not partition:
            # No valid histories, create trivial machine
            return self._build_trivial_result(alphabet, n)

        # Compute initial distances between all state pairs
        distances = self._compute_all_distances(partition, state_to_histories, history_stats)

        # Merge history for hierarchical option
        merge_history: list[MergeInfo] = []

        # Iteratively merge closest pairs
        num_merges = 0
        while len(partition) > 1:
            # Find closest pair
            min_dist = float("inf")
            best_pair: tuple[str, str] | None = None

            for (s1, s2), dist in distances.items():
                if dist < min_dist:
                    min_dist = dist
                    best_pair = (s1, s2)

            if best_pair is None or min_dist > self.config.merge_threshold:
                break

            # Merge the pair
            s1, s2 = best_pair
            new_state = self._merge_states(s1, s2, partition, state_to_histories, history_stats)
            num_merges += 1

            if self.config.hierarchical:
                merge_history.append(MergeInfo(s1, s2, new_state, min_dist))

            # Update distances
            distances = self._update_distances_after_merge(
                s1, s2, new_state, partition, state_to_histories, history_stats, distances
            )

        # Build machine from final partition
        machine = self._build_machine(partition, state_to_histories, history_stats, alphabet)

        return InferenceResult(
            machine=machine,
            sequence_length=n,
            max_history_used=self.config.history_length,
            num_histories_considered=len(history_stats),
            converged=True,
            iterations=num_merges,
        )

    def _collect_history_stats(
        self,
        symbols: list[A],
    ) -> dict[tuple[A, ...], HistoryStats[A]]:
        """Collect statistics for all histories of the configured length."""
        n = len(symbols)
        L = self.config.history_length
        stats: dict[tuple[A, ...], HistoryStats[A]] = {}

        for i in range(L, n):
            history = tuple(symbols[i - L : i])
            next_symbol = symbols[i]

            if history not in stats:
                stats[history] = HistoryStats(history=history)
            stats[history].add_observation(next_symbol)

        return stats

    def _initialize_partition(
        self,
        history_stats: dict[tuple[A, ...], HistoryStats[A]],
    ) -> tuple[dict[str, set[tuple[A, ...]]], dict[str, set[tuple[A, ...]]]]:
        """
        Initialize partition with each valid history as its own state.

        Returns:
            Tuple of (partition dict, state_to_histories dict).
            Both contain the same data but partition is the master copy.
        """
        partition: dict[str, set[tuple[A, ...]]] = {}
        state_counter = 0

        for history, stats in history_stats.items():
            if stats.count >= self.config.min_count:
                state_id = f"S{state_counter}"
                partition[state_id] = {history}
                state_counter += 1

        return partition, partition

    def _compute_all_distances(
        self,
        partition: dict[str, set[tuple[A, ...]]],
        state_to_histories: dict[str, set[tuple[A, ...]]],
        history_stats: dict[tuple[A, ...], HistoryStats[A]],
    ) -> dict[tuple[str, str], float]:
        """Compute pairwise distances between all states."""
        distances: dict[tuple[str, str], float] = {}
        state_ids = list(partition.keys())

        for i, s1 in enumerate(state_ids):
            for s2 in state_ids[i + 1 :]:
                dist = self._compute_state_distance(s1, s2, state_to_histories, history_stats)
                # Store with sorted key for consistent lookup
                key = (s1, s2) if s1 < s2 else (s2, s1)
                distances[key] = dist

        return distances

    def _compute_state_distance(
        self,
        s1: str,
        s2: str,
        state_to_histories: dict[str, set[tuple[A, ...]]],
        history_stats: dict[tuple[A, ...], HistoryStats[A]],
    ) -> float:
        """
        Compute distance between two states' predictive distributions.

        Aggregates the predictive distributions from all histories in each
        state, then computes the distance between the aggregates.
        """
        dist1 = self._aggregate_distribution(s1, state_to_histories, history_stats)
        dist2 = self._aggregate_distribution(s2, state_to_histories, history_stats)

        return self._distribution_distance(dist1, dist2)

    def _aggregate_distribution(
        self,
        state_id: str,
        state_to_histories: dict[str, set[tuple[A, ...]]],
        history_stats: dict[tuple[A, ...], HistoryStats[A]],
    ) -> dict[A, float]:
        """Aggregate next-symbol distribution for a state from all its histories."""
        counts: dict[A, int] = {}

        for history in state_to_histories.get(state_id, set()):
            stats = history_stats.get(history)
            if stats:
                for symbol, count in stats.next_symbol_counts.items():
                    counts[symbol] = counts.get(symbol, 0) + count

        total = sum(counts.values())
        if total == 0:
            return {}

        return {s: c / total for s, c in counts.items()}

    def _distribution_distance(
        self,
        dist1: dict[A, float],
        dist2: dict[A, float],
    ) -> float:
        """
        Compute distance between two probability distributions.

        Uses the configured distance metric.
        """
        if not dist1 or not dist2:
            return float("inf")

        all_keys = set(dist1.keys()) | set(dist2.keys())
        p = [dist1.get(k, 0.0) for k in all_keys]
        q = [dist2.get(k, 0.0) for k in all_keys]

        metric = self.config.distance_metric

        if metric == "kl":
            return self._kl_divergence(p, q)
        if metric == "hellinger":
            return self._hellinger_distance(p, q)
        if metric == "tv":
            return self._total_variation(p, q)
        if metric == "chi2":
            return self._chi_squared_distance(p, q)

        # Default to KL
        return self._kl_divergence(p, q)

    @staticmethod
    def _kl_divergence(p: list[float], q: list[float], epsilon: float = 1e-10) -> float:
        """Compute KL divergence D(P||Q)."""
        # Symmetrized KL divergence
        kl_pq = 0.0
        kl_qp = 0.0

        for pi, qi in zip(p, q, strict=True):
            # Add epsilon for numerical stability
            pi = max(pi, epsilon)
            qi = max(qi, epsilon)
            kl_pq += pi * math.log(pi / qi)
            kl_qp += qi * math.log(qi / pi)

        return (kl_pq + kl_qp) / 2

    @staticmethod
    def _hellinger_distance(p: list[float], q: list[float]) -> float:
        """Compute Hellinger distance."""
        sum_sq = 0.0
        for pi, qi in zip(p, q, strict=True):
            sum_sq += (math.sqrt(pi) - math.sqrt(qi)) ** 2
        return math.sqrt(sum_sq / 2)

    @staticmethod
    def _total_variation(p: list[float], q: list[float]) -> float:
        """Compute total variation distance."""
        return sum(abs(pi - qi) for pi, qi in zip(p, q, strict=True)) / 2

    @staticmethod
    def _chi_squared_distance(p: list[float], q: list[float], epsilon: float = 1e-10) -> float:
        """Compute chi-squared distance."""
        chi2 = 0.0
        for pi, qi in zip(p, q, strict=True):
            mean = (pi + qi) / 2
            if mean > epsilon:
                chi2 += (pi - qi) ** 2 / mean
        return chi2

    def _merge_states(
        self,
        s1: str,
        s2: str,
        partition: dict[str, set[tuple[A, ...]]],
        state_to_histories: dict[str, set[tuple[A, ...]]],
        history_stats: dict[tuple[A, ...], HistoryStats[A]],  # noqa: ARG002
    ) -> str:
        """
        Merge two states into one.

        Modifies partition and state_to_histories in place.
        Returns the ID of the merged state.
        """
        # Use the lexicographically smaller ID for the merged state
        merged_id = s1 if s1 < s2 else s2
        removed_id = s2 if s1 < s2 else s1

        # Merge histories
        merged_histories = partition[merged_id] | partition[removed_id]
        partition[merged_id] = merged_histories
        state_to_histories[merged_id] = merged_histories

        # Remove the absorbed state
        del partition[removed_id]
        state_to_histories.pop(removed_id, None)

        return merged_id

    def _update_distances_after_merge(
        self,
        s1: str,
        s2: str,
        new_state: str,
        partition: dict[str, set[tuple[A, ...]]],
        state_to_histories: dict[str, set[tuple[A, ...]]],
        history_stats: dict[tuple[A, ...], HistoryStats[A]],
        old_distances: dict[tuple[str, str], float],
    ) -> dict[tuple[str, str], float]:
        """Update distance matrix after a merge."""
        removed_id = s2 if new_state == s1 else s1
        new_distances: dict[tuple[str, str], float] = {}

        # Remove entries involving the removed state
        for (state_a, state_b), dist in old_distances.items():
            if removed_id in (state_a, state_b):
                continue
            new_distances[(state_a, state_b)] = dist

        # Recompute distances to the merged state
        for other_state in partition:
            if other_state == new_state:
                continue

            dist = self._compute_state_distance(
                new_state, other_state, state_to_histories, history_stats
            )
            key = (new_state, other_state) if new_state < other_state else (other_state, new_state)
            new_distances[key] = dist

        return new_distances

    def _build_trivial_result(
        self,
        alphabet: frozenset[A],
        sequence_length: int,
    ) -> InferenceResult[A]:
        """Build a trivial single-state result when no valid histories exist."""
        builder: EpsilonMachineBuilder[A] = EpsilonMachineBuilder()

        # Single state with uniform self-loops
        for symbol in alphabet:
            builder.add_transition("S0", symbol, "S0", 1.0 / len(alphabet))

        builder.with_start_state("S0")

        return InferenceResult(
            machine=builder.build(),
            sequence_length=sequence_length,
            max_history_used=self.config.history_length,
            num_histories_considered=0,
            converged=True,
            iterations=0,
        )

    def _build_machine(
        self,
        partition: dict[str, set[tuple[A, ...]]],
        state_to_histories: dict[str, set[tuple[A, ...]]],
        history_stats: dict[tuple[A, ...], HistoryStats[A]],
        alphabet: frozenset[A],
    ) -> EpsilonMachine[A]:
        """
        Construct the epsilon-machine from the final partition.

        Each state in the partition becomes a CausalState.
        Transitions are computed from observed symbol frequencies.
        """
        builder: EpsilonMachineBuilder[A] = EpsilonMachineBuilder()

        state_ids = list(partition.keys())
        if not state_ids:
            # Edge case: no states
            builder.add_transition("S0", next(iter(alphabet)), "S0", 1.0)
            builder.with_start_state("S0")
            return builder.build()

        # Build reverse mapping: history -> state
        history_to_state: dict[tuple[A, ...], str] = {}
        for state_id, histories in state_to_histories.items():
            for history in histories:
                history_to_state[history] = state_id

        # Compute transitions for each state
        for state_id in state_ids:
            histories = partition[state_id]

            # Aggregate next-symbol counts
            symbol_counts: dict[A, int] = {}
            for history in histories:
                stats = history_stats.get(history)
                if stats:
                    for symbol, count in stats.next_symbol_counts.items():
                        symbol_counts[symbol] = symbol_counts.get(symbol, 0) + count

            total = sum(symbol_counts.values())
            if total == 0:
                # No observations - uniform over alphabet
                total = len(alphabet)
                symbol_counts = dict.fromkeys(alphabet, 1)

            # Create transitions
            for symbol, count in symbol_counts.items():
                prob = count / total

                # Determine target state by finding where extended histories go
                target_state = self._find_target_state(
                    histories, symbol, history_to_state, state_id
                )

                builder.add_transition(
                    source=state_id,
                    symbol=symbol,
                    target=target_state,
                    probability=prob,
                )

        # Set start state (first state in sorted order for determinism)
        sorted_states = sorted(state_ids)
        builder.with_start_state(sorted_states[0])

        return builder.build()

    def _find_target_state(
        self,
        histories: set[tuple[A, ...]],
        symbol: A,
        history_to_state: dict[tuple[A, ...], str],
        default_state: str,
    ) -> str:
        """
        Find the target state after emitting a symbol.

        Given the current histories and a symbol, find which state
        the extended histories belong to.
        """
        L = self.config.history_length

        for history in histories:
            # Extend history with symbol and truncate to length L
            extended = (*history[1:], symbol) if len(history) >= L else (*history, symbol)

            # Find state for extended history
            target = history_to_state.get(extended)
            if target is not None:
                return target

            # Try shorter suffixes as fallback
            for i in range(1, len(extended)):
                suffix = extended[i:]
                target = history_to_state.get(suffix)
                if target is not None:
                    return target

        return default_state

    def __rrshift__(self, source: Iterable[A]) -> InferenceResult[A]:
        """Support: sequence >> CSM(config)."""
        alphabet = getattr(source, "alphabet", None)
        return self.infer(source, alphabet=alphabet)
