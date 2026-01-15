"""CSSR algorithm implementation."""

from __future__ import annotations

from collections.abc import Hashable, Iterable
from dataclasses import dataclass
from typing import TYPE_CHECKING, Generic, TypeVar

from emic.inference.cssr.partition import StatePartition
from emic.inference.cssr.suffix_tree import SuffixTree
from emic.inference.cssr.tests import distributions_differ
from emic.inference.errors import InsufficientDataError, NonConvergenceError
from emic.inference.result import InferenceResult
from emic.types import EpsilonMachine, EpsilonMachineBuilder, Transition

if TYPE_CHECKING:
    from emic.inference.cssr.config import CSSRConfig

A = TypeVar("A", bound=Hashable)


@dataclass
class CSSR(Generic[A]):
    """
    Causal State Splitting Reconstruction algorithm.

    Infers an epsilon-machine from an observed sequence by:
    1. Building a suffix tree of observed histories
    2. Grouping histories into causal states based on
       statistical indistinguishability of their futures

    Reference:
        Shalizi, C.R. & Crutchfield, J.P. (2001).
        "Computational Mechanics: Pattern and Prediction,
        Structure and Simplicity"

    Examples:
        >>> from emic.sources.synthetic.golden_mean import GoldenMeanSource
        >>> from emic.sources.transforms.take import TakeN
        >>> from emic.inference import CSSR, CSSRConfig
        >>>
        >>> source = GoldenMeanSource(p=0.5, _seed=42)
        >>> sequence = list(TakeN(10000)(source))
        >>>
        >>> cssr = CSSR(CSSRConfig(max_history=5))
        >>> result = cssr.infer(sequence)
        >>> len(result.machine.states)
        2
    """

    config: CSSRConfig

    def infer(
        self,
        sequence: Iterable[A],
        alphabet: frozenset[A] | None = None,
    ) -> InferenceResult[A]:
        """Infer epsilon-machine from sequence."""
        # Convert to list for multiple passes
        symbols = list(sequence)
        n = len(symbols)

        # Check minimum data requirement
        min_required = self.config.min_count * (self.config.max_history + 1) * 2
        if n < min_required:
            raise InsufficientDataError(
                required=min_required,
                provided=n,
                algorithm="CSSR",
            )

        # Infer alphabet if not provided
        if alphabet is None:
            alphabet = frozenset(symbols)

        # Build suffix tree
        suffix_tree: SuffixTree[A] = SuffixTree(
            max_depth=self.config.max_history, alphabet=alphabet
        )
        suffix_tree.build_from_sequence(symbols)

        # Initialize: group histories by next-symbol distribution similarity
        partition = self._initialize_partition(suffix_tree)

        # Iterate: split and merge until convergence
        converged = False
        num_iterations = 0
        for _ in range(self.config.max_iterations):
            num_iterations += 1
            old_partition = partition.copy()

            # Split states where histories have different futures
            partition = self._split_states(partition, suffix_tree)

            # Merge states that are indistinguishable
            partition = self._merge_states(partition, suffix_tree)

            if partition == old_partition:
                converged = True
                break

        if not converged:
            raise NonConvergenceError(
                iterations=self.config.max_iterations,
                tolerance=self.config.significance,
            )

        # Build machine from final partition
        machine = self._build_machine(partition, suffix_tree, alphabet)

        return InferenceResult(
            machine=machine,
            sequence_length=n,
            max_history_used=self.config.max_history,
            num_histories_considered=len(suffix_tree),
            converged=converged,
            iterations=num_iterations,
        )

    def _initialize_partition(self, suffix_tree: SuffixTree[A]) -> StatePartition:
        """
        Initialize partition by grouping similar histories.

        Start with histories of length max_history grouped by
        their next-symbol distribution similarity.
        """
        partition = StatePartition()

        # Collect histories with sufficient counts
        valid_histories: list[tuple[A, ...]] = []
        for history in suffix_tree.all_histories():
            stats = suffix_tree.get_stats(history)
            if stats and stats.count >= self.config.min_count:
                valid_histories.append(history)

        if not valid_histories:
            # No valid histories - create single state with empty history
            partition.assign((), partition.new_state_id())
            return partition

        # Initially put all histories in one state
        initial_state = partition.new_state_id()
        for history in valid_histories:
            partition.assign(history, initial_state)

        return partition

    def _split_states(
        self,
        partition: StatePartition,
        suffix_tree: SuffixTree[A],
    ) -> StatePartition:
        """
        Split states where histories have different next-symbol distributions.

        For each state, check if any history has a significantly different
        distribution from others. If so, split the state.
        """
        new_partition = partition.copy()

        for state_id in partition.state_ids():
            histories = list(partition.get_histories(state_id))
            if len(histories) <= 1:
                continue

            # Find a representative distribution
            representative = histories[0]
            rep_stats = suffix_tree.get_stats(representative)
            if rep_stats is None:
                continue

            # Group histories by whether they differ from representative
            same_group: set[tuple[A, ...]] = {representative}
            diff_group: set[tuple[A, ...]] = set()

            for history in histories[1:]:
                stats = suffix_tree.get_stats(history)
                if stats is None:
                    same_group.add(history)
                    continue

                if distributions_differ(
                    rep_stats.next_symbol_counts,
                    stats.next_symbol_counts,
                    self.config.significance,
                    self.config.test,
                ):
                    diff_group.add(history)
                else:
                    same_group.add(history)

            # If we found differences, split
            if diff_group:
                groups = [same_group, diff_group]
                new_partition.split_state(state_id, groups)

        return new_partition

    def _merge_states(
        self,
        partition: StatePartition,
        suffix_tree: SuffixTree[A],
    ) -> StatePartition:
        """
        Merge states that are statistically indistinguishable.

        Two states should be merged if their aggregate next-symbol
        distributions are not significantly different.
        """
        new_partition = partition.copy()
        state_ids = partition.state_ids()

        if len(state_ids) <= 1:
            return new_partition

        # Compute aggregate distribution for each state
        state_distributions: dict[str, dict[A, int]] = {}
        for state_id in state_ids:
            aggregate: dict[A, int] = {}
            for history in partition.get_histories(state_id):
                stats = suffix_tree.get_stats(history)
                if stats:
                    for symbol, count in stats.next_symbol_counts.items():
                        aggregate[symbol] = aggregate.get(symbol, 0) + count
            state_distributions[state_id] = aggregate

        # Find pairs of states to merge
        merged: set[str] = set()
        for i, s1 in enumerate(state_ids):
            if s1 in merged:
                continue
            for s2 in state_ids[i + 1 :]:
                if s2 in merged:
                    continue

                dist1 = state_distributions.get(s1, {})
                dist2 = state_distributions.get(s2, {})

                if not distributions_differ(
                    dist1, dist2, self.config.significance, self.config.test
                ):
                    # Merge s2 into s1
                    new_partition.merge_states([s1, s2])
                    merged.add(s2)

        return new_partition

    def _build_machine(
        self,
        partition: StatePartition,
        suffix_tree: SuffixTree[A],
        alphabet: frozenset[A],
    ) -> EpsilonMachine[A]:
        """
        Construct the epsilon-machine from the final state partition.

        Each state in the partition becomes a CausalState.
        Transitions are computed from observed symbol frequencies.
        """
        builder: EpsilonMachineBuilder[A] = EpsilonMachineBuilder()

        state_ids = partition.state_ids()
        if not state_ids:
            # Edge case: no states (shouldn't happen)
            state_ids = ["S0"]
            partition.assign((), "S0")

        # Compute transition probabilities for each state
        for state_id in state_ids:
            histories = partition.get_histories(state_id)

            # Aggregate next-symbol counts
            symbol_counts: dict[A, int] = {}
            for history in histories:
                stats = suffix_tree.get_stats(history)
                if stats:
                    for symbol, count in stats.next_symbol_counts.items():
                        symbol_counts[symbol] = symbol_counts.get(symbol, 0) + count

            total = sum(symbol_counts.values())
            if total == 0:
                # No observations - uniform over alphabet
                total = len(alphabet)
                symbol_counts = dict.fromkeys(alphabet, 1)

            # Create transitions
            transitions: list[Transition[A]] = []
            for symbol, count in symbol_counts.items():
                prob = count / total

                # Determine target state by extending history
                # Find which state the extended history belongs to
                target_state = self._find_target_state(histories, symbol, partition, suffix_tree)
                if target_state is None:
                    target_state = state_id  # Self-loop as fallback

                transitions.append(Transition(symbol=symbol, probability=prob, target=target_state))

            # Add state to builder
            for t in transitions:
                builder.add_transition(
                    source=state_id,
                    symbol=t.symbol,
                    target=t.target,
                    probability=t.probability,
                )

        # Set start state (first state or most common)
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
        """
        Find the target state after emitting a symbol.

        Given the current histories and a symbol, find which state
        the extended histories belong to.
        """
        for history in histories:
            # Extend history with symbol
            if len(history) >= self.config.max_history:
                extended = (*history[1:], symbol)
            else:
                extended = (*history, symbol)

            # Find state for extended history
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
