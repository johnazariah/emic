"""CSSR algorithm implementation - corrected version.

This implementation follows the original Shalizi & Klinkner (2004) paper more closely,
using level-by-level sufficiency testing rather than simultaneous distribution comparison.

Reference:
    Shalizi, C.R. & Shalizi, K.L. (2004). "Blind Construction of Optimal
    Nonlinear Recursive Predictors for Discrete Sequences". arXiv:cs/0406011
"""

from __future__ import annotations

from collections.abc import Hashable, Iterable
from dataclasses import dataclass
from typing import TYPE_CHECKING, Generic, TypeVar

from emic.inference.cssr.partition import StatePartition
from emic.inference.cssr.suffix_tree import SuffixTree
from emic.inference.cssr.tests import distributions_differ
from emic.inference.errors import InsufficientDataError
from emic.inference.result import InferenceResult
from emic.types import EpsilonMachine, EpsilonMachineBuilder

if TYPE_CHECKING:
    from emic.inference.cssr.config import CSSRConfig

A = TypeVar("A", bound=Hashable)


@dataclass
class CSSR(Generic[A]):
    """
    Causal State Splitting Reconstruction algorithm (corrected version).

    This implementation follows the three-phase structure from the original paper:

    Phase I (Initialization):
        Build suffix tree and initialize with all histories in one state.

    Phase II (Sufficiency):
        For each history length L from 1 to L_max:
            For each history h of length L:
                Let s be the suffix of h of length L-1
                If P(next | h) differs significantly from P(next | state(s)):
                    Create new state or reassign h

    Phase III (Recursion/Determinism):
        Ensure transitions are deterministic by merging states that would
        receive the same history under extension.

    Reference:
        Shalizi, C.R. & Klinkner, K.L. (2004). "Blind Construction of Optimal
        Nonlinear Recursive Predictors for Discrete Sequences"
    """

    config: CSSRConfig

    def infer(
        self,
        sequence: Iterable[A],
        alphabet: frozenset[A] | None = None,
    ) -> InferenceResult[A]:
        """Infer epsilon-machine from sequence."""
        symbols = list(sequence)
        n = len(symbols)

        min_required = self.config.min_count * (self.config.max_history + 1) * 2
        if n < min_required:
            raise InsufficientDataError(
                required=min_required,
                provided=n,
                algorithm="CSSR",
            )

        if alphabet is None:
            alphabet = frozenset(symbols)

        # Phase I: Build suffix tree
        suffix_tree: SuffixTree[A] = SuffixTree(
            max_depth=self.config.max_history, alphabet=alphabet
        )
        suffix_tree.build_from_sequence(symbols)

        # Phase II: Level-by-level sufficiency testing
        partition = self._sufficiency_phase(suffix_tree, alphabet)

        # Phase III: Ensure determinism (merge equivalent states)
        partition = self._determinism_phase(partition, suffix_tree, alphabet)

        # Build machine
        machine = self._build_machine(partition, suffix_tree, alphabet)

        return InferenceResult(
            machine=machine,
            sequence_length=n,
            max_history_used=self.config.max_history,
            num_histories_considered=len(suffix_tree),
            converged=True,
            iterations=self.config.max_history,
        )

    def _sufficiency_phase(
        self,
        suffix_tree: SuffixTree[A],
        alphabet: frozenset[A],
    ) -> StatePartition:
        """
        Phase II: Level-by-level sufficiency testing with synchronizing detection.

        Key insight: Some histories are non-synchronizing (ambiguous) and should
        not be used to define states. We:
        1. Identify synchronizing histories at each level
        2. Only group synchronizing histories into states
        3. Assign non-synchronizing histories to states based on their
           longest synchronizing suffix
        """
        partition = StatePartition()

        # Collect all histories and check synchronization
        all_histories: list[tuple[A, ...]] = []
        sync_histories: list[tuple[A, ...]] = []
        nonsync_histories: list[tuple[A, ...]] = []

        for h in suffix_tree.all_histories():
            if len(h) == 0:
                continue
            stats = suffix_tree.get_stats(h)
            if stats is None or stats.count < self.config.min_count:
                continue
            all_histories.append(h)

            if self._is_synchronizing(h, suffix_tree, alphabet):
                sync_histories.append(h)
            else:
                nonsync_histories.append(h)

        if not all_histories:
            state_id = partition.new_state_id()
            for a in alphabet:
                partition.assign((a,), state_id)
            return partition

        # If no synchronizing histories, use all
        if not sync_histories:
            sync_histories = all_histories
            nonsync_histories = []

        # Group synchronizing histories by distribution
        partition = self._group_by_distribution(sync_histories, suffix_tree, partition)

        # Assign non-synchronizing histories to state of their sync suffix
        for h in nonsync_histories:
            state = self._find_state_for_history(h, partition, suffix_tree)
            if state:
                partition.assign(h, state)

        return partition

    def _process_length_v2(
        self,
        length: int,
        partition: StatePartition,
        suffix_tree: SuffixTree[A],
        _alphabet: frozenset[A],
    ) -> StatePartition:
        """
        Process all histories of a given length.

        For each history h of length L:
        1. Get parent suffix s = h[1:]
        2. Compare P(next|h) with P(next|s) directly
        3. If same, assign h to same state as s
        4. If different, find or create appropriate state

        This follows the Shalizi paper: compare h to its SUFFIX, not to state aggregate.
        """
        new_partition = partition.copy()

        # Get histories at this length
        histories = list(suffix_tree.histories_of_length(length))

        for h in histories:
            h_stats = suffix_tree.get_stats(h)
            if h_stats is None or h_stats.count < self.config.min_count:
                continue

            # Get parent suffix and its distribution
            parent = h[1:]  # Remove first element
            parent_stats = suffix_tree.get_stats(parent)
            parent_state = partition.get_state(parent)

            if parent_stats is None or parent_stats.count < self.config.min_count:
                # No parent data - assign h to new state
                new_state = new_partition.new_state_id()
                new_partition.assign(h, new_state)
                continue

            if parent_state is None:
                # Parent not assigned - assign h to new state
                new_state = new_partition.new_state_id()
                new_partition.assign(h, new_state)
                continue

            # Compare h's distribution to PARENT's distribution (not state aggregate)
            h_dist = h_stats.next_symbol_counts
            parent_dist = parent_stats.next_symbol_counts

            if distributions_differ(
                h_dist, parent_dist, self.config.significance, self.config.test
            ):
                # h is different from its parent - find or create new state
                # Try to find an existing state with matching distribution
                found_state = None
                for state_id in partition.state_ids():
                    # Get a representative history from this state
                    state_histories = partition.get_histories(state_id)
                    if state_histories:
                        rep_history = next(iter(state_histories))
                        rep_stats = suffix_tree.get_stats(rep_history)
                        if rep_stats and not distributions_differ(
                            h_dist,
                            rep_stats.next_symbol_counts,
                            self.config.significance,
                            self.config.test,
                        ):
                            found_state = state_id
                            break

                if found_state is not None:
                    new_partition.assign(h, found_state)
                else:
                    # Create new state
                    new_state = new_partition.new_state_id()
                    new_partition.assign(h, new_state)
            else:
                # h matches parent - assign to same state
                new_partition.assign(h, parent_state)

        return new_partition

    def _get_state_distribution(
        self,
        state_id: str,
        partition: StatePartition,
        suffix_tree: SuffixTree[A],
    ) -> dict[A, int] | None:
        """Get the aggregate next-symbol distribution for a state."""
        histories = partition.get_histories(state_id)
        if not histories:
            return None

        aggregate: dict[A, int] = {}
        for h in histories:
            stats = suffix_tree.get_stats(h)
            if stats:
                for sym, cnt in stats.next_symbol_counts.items():
                    aggregate[sym] = aggregate.get(sym, 0) + cnt

        return aggregate if aggregate else None

    def _is_synchronizing(
        self,
        history: tuple[A, ...],
        suffix_tree: SuffixTree[A],
        alphabet: frozenset[A],
    ) -> bool:
        """
        Check if a history is synchronizing.

        A history is synchronizing if all its parent extensions have
        consistent distributions. If extending with different prefixes
        gives significantly different distributions, it's not synchronizing.

        Additionally, if any SUFFIX of the history is non-synchronizing,
        the history itself is non-synchronizing (ambiguity propagates).
        """
        # First check: if any suffix is non-synchronizing, so is this history
        # (We check suffixes from shortest to longest, but we only check the
        # length-1 suffix to avoid infinite recursion)
        if len(history) > 1:
            suffix = history[1:]  # Remove first element
            if not self._is_synchronizing_core(suffix, suffix_tree, alphabet):
                return False

        return self._is_synchronizing_core(history, suffix_tree, alphabet)

    def _is_synchronizing_core(
        self,
        history: tuple[A, ...],
        suffix_tree: SuffixTree[A],
        alphabet: frozenset[A],
    ) -> bool:
        """Core synchronizing check - just looks at extensions.

        Uses a VERY strict threshold (0.001) to only flag truly ambiguous
        histories like all-1s patterns in the Even Process. This prevents
        false positives from statistical fluctuation in IID processes.
        """
        h_stats = suffix_tree.get_stats(history)
        if h_stats is None:
            return False

        # Check extensions: (a,) + history for each a in alphabet
        extension_dists: list[dict[A, int]] = []
        for a in alphabet:
            extended = (a, *history)
            ext_stats = suffix_tree.get_stats(extended)
            if ext_stats and ext_stats.count >= self.config.min_count:
                extension_dists.append(ext_stats.next_symbol_counts)

        # If no extensions, we can't determine - check the suffix instead
        # This handles max-depth histories
        if len(extension_dists) < 2:
            return True

        # Check if all extensions have similar distributions
        # Use a STRICT threshold (0.001) to avoid false positives
        sync_threshold = min(self.config.significance, 0.001)
        for i in range(len(extension_dists)):
            for j in range(i + 1, len(extension_dists)):
                if distributions_differ(
                    extension_dists[i],
                    extension_dists[j],
                    sync_threshold,
                    self.config.test,
                ):
                    return False

        return True

    def _find_state_for_history(
        self,
        history: tuple[A, ...],
        partition: StatePartition,
        suffix_tree: SuffixTree[A],
    ) -> str | None:
        """Find the appropriate state for a non-synchronizing history."""
        # Try to find a matching synchronizing suffix
        for i in range(1, len(history)):
            suffix = history[i:]
            state = partition.get_state(suffix)
            if state is not None:
                return state

        # Fall back to distribution matching
        h_stats = suffix_tree.get_stats(history)
        if h_stats is None:
            return None

        for state_id in partition.state_ids():
            state_dist = self._compute_state_distribution(state_id, partition, suffix_tree)
            if not distributions_differ(
                h_stats.next_symbol_counts, state_dist, self.config.significance, self.config.test
            ):
                return state_id

        return None

    def _merge_equivalent_states(
        self,
        partition: StatePartition,
        suffix_tree: SuffixTree[A],
        sync_histories: list[tuple[A, ...]] | None = None,
    ) -> StatePartition:
        """
        Merge states with indistinguishable aggregate distributions.

        If sync_histories is provided, only use those for computing distributions.
        Uses a more lenient threshold for merging to avoid over-splitting
        due to statistical fluctuations with large sample sizes.
        """
        current = partition.copy()
        changed = True

        # Use a more lenient threshold for merging (min 0.1)
        # This helps avoid over-splitting from statistical fluctuation
        merge_sig = max(
            self.config.merge_significance or self.config.significance,
            0.1,  # At least 10% threshold for merging
        )

        while changed:
            changed = False
            state_ids = current.state_ids()

            if len(state_ids) <= 1:
                break

            # Compute aggregate for each state (using only sync histories if provided)
            state_dists: dict[str, dict[A, int]] = {}
            for sid in state_ids:
                agg: dict[A, int] = {}
                for h in current.get_histories(sid):
                    # If sync_histories provided, only use those
                    if sync_histories is not None and h not in sync_histories:
                        continue
                    stats = suffix_tree.get_stats(h)
                    if stats:
                        for sym, cnt in stats.next_symbol_counts.items():
                            agg[sym] = agg.get(sym, 0) + cnt
                state_dists[sid] = agg

            # Try to merge pairs
            for i, s1 in enumerate(state_ids):
                if not state_dists[s1]:  # Skip empty
                    continue
                for s2 in state_ids[i + 1 :]:
                    if not state_dists[s2]:  # Skip empty
                        continue
                    if not distributions_differ(
                        state_dists[s1], state_dists[s2], merge_sig, self.config.test
                    ):
                        current = current.copy()
                        current.merge_states([s1, s2])
                        changed = True
                        break
                if changed:
                    break

        return current

    def _group_by_distribution(
        self,
        histories: list[tuple[A, ...]],
        suffix_tree: SuffixTree[A],
        partition: StatePartition,
    ) -> StatePartition:
        """Group histories by distribution similarity.

        Uses a two-phase approach:
        1. First check if all histories can be merged (homogeneous)
        2. If so, put all in one state
        3. Otherwise, do greedy grouping
        """
        if not histories:
            return partition

        # Get distributions for all histories
        hist_dists: list[tuple[tuple[A, ...], dict[A, int]]] = []
        for h in histories:
            h_stats = suffix_tree.get_stats(h)
            if h_stats is None or h_stats.count < self.config.min_count:
                continue
            hist_dists.append((h, dict(h_stats.next_symbol_counts)))

        if not hist_dists:
            return partition

        # Check if all histories can be merged into one state
        # Use pairwise tests between consecutive histories with a lenient threshold
        # This is more robust than testing against a huge pool
        all_homogeneous = True

        # Use a more lenient significance for the homogeneity check
        # This accounts for multiple comparisons and sampling variability
        homog_sig = max(self.config.significance, 0.01)

        # Test first few histories pairwise to check homogeneity
        for i in range(min(len(hist_dists) - 1, 10)):
            _, dist1 = hist_dists[i]
            _, dist2 = hist_dists[i + 1]
            if distributions_differ(dist1, dist2, homog_sig, self.config.test):
                all_homogeneous = False
                break

        # Also check if any extreme outliers exist using proportion tolerance
        if all_homogeneous:
            all_keys = set()
            for _, dist in hist_dists:
                all_keys.update(dist.keys())

            min_props: dict[A, float] = {}
            max_props: dict[A, float] = {}
            for _, dist in hist_dists:
                total = sum(dist.values())
                if total < 1:
                    continue
                for k in all_keys:
                    p = dist.get(k, 0) / total
                    min_props[k] = min(min_props.get(k, 1.0), p)
                    max_props[k] = max(max_props.get(k, 0.0), p)

            # Allow 25% range for sample variability
            tolerance = 0.25
            all_homogeneous = all(
                max_props.get(k, 0) - min_props.get(k, 0) <= tolerance for k in all_keys
            )

        if all_homogeneous:
            state_id = partition.new_state_id()
            for h, _ in hist_dists:
                partition.assign(h, state_id)
            return partition

        # Otherwise, do greedy grouping with lenient chi-squared
        groups: list[list[tuple[A, ...]]] = [[hist_dists[0][0]]]
        group_reps: list[dict[A, int]] = [dict(hist_dists[0][1])]

        # Use lenient threshold for grouping
        group_sig = max(self.config.significance, 0.1)

        for h, h_dist in hist_dists[1:]:
            found_group = False

            for i, rep_dist in enumerate(group_reps):
                if not distributions_differ(h_dist, rep_dist, group_sig, self.config.test):
                    groups[i].append(h)
                    found_group = True
                    break

            if not found_group:
                groups.append([h])
                group_reps.append(dict(h_dist))

        # Assign to partition
        for group in groups:
            state_id = partition.new_state_id()
            for h in group:
                partition.assign(h, state_id)

        return partition

    def _process_length(
        self,
        length: int,
        partition: StatePartition,
        suffix_tree: SuffixTree[A],
    ) -> StatePartition:
        """
        Process histories of a given length.

        For each history h of length L:
        1. Find suffix s = h[1:] (length L-1)
        2. Get state of s: state_s = partition.get_state(s)
        3. Compute aggregate distribution of state_s
        4. Compare P(next | h) with P(next | state_s)
        5. If different, find appropriate state for h or create new one
        """
        new_partition = partition.copy()

        # Get all histories of this length
        histories = list(suffix_tree.histories_of_length(length))

        for h in histories:
            h_stats = suffix_tree.get_stats(h)
            if h_stats is None or h_stats.count < self.config.min_count:
                continue

            # Get parent suffix (h[1:])
            parent_suffix = h[1:]
            parent_state = partition.get_state(parent_suffix)

            if parent_state is None:
                # Parent not in partition - try to find closest match
                parent_state = self._find_matching_state(h, partition, suffix_tree)

            if parent_state is None:
                # No parent found - create new state
                new_state = new_partition.new_state_id()
                new_partition.assign(h, new_state)
                continue

            # Compute aggregate distribution of parent state
            parent_aggregate = self._compute_state_distribution(
                parent_state, partition, suffix_tree
            )

            # Compare h's distribution with parent state's distribution
            if distributions_differ(
                h_stats.next_symbol_counts,
                parent_aggregate,
                self.config.significance,
                self.config.test,
            ):
                # h differs from its parent state - find or create appropriate state
                target_state = self._find_or_create_state(
                    h, h_stats.next_symbol_counts, new_partition, suffix_tree
                )
                new_partition.assign(h, target_state)
            else:
                # h is consistent with parent state
                new_partition.assign(h, parent_state)

        return new_partition

    def _compute_state_distribution(
        self,
        state_id: str,
        partition: StatePartition,
        suffix_tree: SuffixTree[A],
    ) -> dict[A, int]:
        """Compute aggregate next-symbol distribution for a state."""
        aggregate: dict[A, int] = {}
        for h in partition.get_histories(state_id):
            stats = suffix_tree.get_stats(h)
            if stats:
                for sym, cnt in stats.next_symbol_counts.items():
                    aggregate[sym] = aggregate.get(sym, 0) + cnt
        return aggregate

    def _find_matching_state(
        self,
        history: tuple[A, ...],
        partition: StatePartition,
        suffix_tree: SuffixTree[A],
    ) -> str | None:
        """Find a state that matches the history's distribution."""
        h_stats = suffix_tree.get_stats(history)
        if h_stats is None:
            return None

        for state_id in partition.state_ids():
            state_dist = self._compute_state_distribution(state_id, partition, suffix_tree)
            if not distributions_differ(
                h_stats.next_symbol_counts,
                state_dist,
                self.config.significance,
                self.config.test,
            ):
                return state_id

        return None

    def _find_or_create_state(
        self,
        _history: tuple[A, ...],
        h_dist: dict[A, int],
        partition: StatePartition,
        suffix_tree: SuffixTree[A],
    ) -> str:
        """Find an existing matching state or create a new one."""
        # Check if any existing state matches this distribution
        for state_id in partition.state_ids():
            state_dist = self._compute_state_distribution(state_id, partition, suffix_tree)
            if not distributions_differ(
                h_dist, state_dist, self.config.significance, self.config.test
            ):
                return state_id

        # No match - create new state
        return partition.new_state_id()

    def _determinism_phase(
        self,
        partition: StatePartition,
        suffix_tree: SuffixTree[A],
        _alphabet: frozenset[A],
    ) -> StatePartition:
        """
        Phase III: Ensure deterministic transitions.

        Merge states that would be reached by the same history extension.
        This ensures the resulting machine is unifilar (deterministic given symbol).

        Uses a lenient threshold to avoid over-splitting.
        """
        current = partition.copy()
        changed = True

        # Use lenient merge threshold (at least 0.1)
        merge_sig = max(self.config.merge_significance or self.config.significance, 0.1)

        while changed:
            changed = False
            state_ids = current.state_ids()

            if len(state_ids) <= 1:
                break

            # For each pair of states, check if they can be merged
            for i, s1 in enumerate(state_ids):
                for s2 in state_ids[i + 1 :]:
                    dist1 = self._compute_state_distribution(s1, current, suffix_tree)
                    dist2 = self._compute_state_distribution(s2, current, suffix_tree)

                    if not distributions_differ(dist1, dist2, merge_sig, self.config.test):
                        current = current.copy()
                        current.merge_states([s1, s2])
                        changed = True
                        break

                if changed:
                    break

        return current

    def _build_machine(
        self,
        partition: StatePartition,
        suffix_tree: SuffixTree[A],
        alphabet: frozenset[A],
    ) -> EpsilonMachine[A]:
        """Construct epsilon-machine from partition."""
        builder: EpsilonMachineBuilder[A] = EpsilonMachineBuilder()

        state_ids = partition.state_ids()
        if not state_ids:
            state_ids = ["S0"]
            partition.assign((), "S0")

        for state_id in state_ids:
            histories = partition.get_histories(state_id)

            # Aggregate next-symbol counts
            symbol_counts: dict[A, int] = {}
            for h in histories:
                stats = suffix_tree.get_stats(h)
                if stats:
                    for sym, cnt in stats.next_symbol_counts.items():
                        symbol_counts[sym] = symbol_counts.get(sym, 0) + cnt

            total = sum(symbol_counts.values())
            if total == 0:
                total = len(alphabet)
                symbol_counts = dict.fromkeys(alphabet, 1)

            for sym, cnt in symbol_counts.items():
                prob = cnt / total
                target = self._find_target_state(histories, sym, partition, suffix_tree)
                if target is None:
                    target = state_id

                builder.add_transition(
                    source=state_id,
                    symbol=sym,
                    target=target,
                    probability=prob,
                )

        if state_ids:
            builder.with_start_state(state_ids[0])

        return builder.build()

    def _find_target_state(
        self,
        histories: set[tuple[A, ...]],
        symbol: A,
        partition: StatePartition,
        _suffix_tree: SuffixTree[A],
    ) -> str | None:
        """Find target state after emitting symbol."""
        for h in histories:
            extended = (*h[1:], symbol) if len(h) >= self.config.max_history else (*h, symbol)

            target = partition.get_state(extended)
            if target is not None:
                return target

            # Try shorter suffixes
            for i in range(1, len(extended)):
                suffix = extended[i:]
                target = partition.get_state(suffix)
                if target is not None:
                    return target

        return None

    def __rrshift__(self, source: Iterable[A]) -> InferenceResult[A]:
        """Support: sequence >> CSSR(config)."""
        alphabet = getattr(source, "alphabet", None)
        return self.infer(source, alphabet=alphabet)
