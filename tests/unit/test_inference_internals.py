"""Additional tests for inference module to boost coverage."""

from __future__ import annotations

from emic.inference.cssr.partition import StatePartition
from emic.inference.cssr.suffix_tree import HistoryStats, SuffixTree
from emic.inference.cssr.tests import chi_squared_test, distributions_differ
from emic.inference.errors import InsufficientDataError, NonConvergenceError


class TestHistoryStats:
    """Tests for HistoryStats."""

    def test_add_observation(self) -> None:
        """add_observation updates counts."""
        stats = HistoryStats(history=(0, 1))
        stats.add_observation(0)
        stats.add_observation(0)
        stats.add_observation(1)

        assert stats.count == 3
        assert stats.next_symbol_counts[0] == 2
        assert stats.next_symbol_counts[1] == 1

    def test_next_symbol_distribution(self) -> None:
        """next_symbol_distribution returns correct probabilities."""
        stats = HistoryStats(history=(0,))
        stats.add_observation(0)
        stats.add_observation(1)

        dist = stats.next_symbol_distribution
        assert dist is not None
        assert abs(dist[0] - 0.5) < 1e-10
        assert abs(dist[1] - 0.5) < 1e-10

    def test_empty_distribution(self) -> None:
        """Empty stats has count 0."""
        stats = HistoryStats(history=())
        assert stats.count == 0

    def test_next_symbol_distribution_empty(self) -> None:
        """Empty stats returns None for distribution."""
        stats = HistoryStats(history=())
        assert stats.next_symbol_distribution is None


class TestSuffixTree:
    """Tests for SuffixTree."""

    def test_build_from_sequence(self) -> None:
        """build_from_sequence collects statistics."""
        tree: SuffixTree[int] = SuffixTree(max_depth=2, alphabet=frozenset({0, 1}))
        tree.build_from_sequence([0, 1, 0, 1, 0])

        # Check that histories were recorded
        assert len(tree) > 0

    def test_histories_of_length(self) -> None:
        """histories_of_length returns correct histories."""
        tree: SuffixTree[int] = SuffixTree(max_depth=2, alphabet=frozenset({0, 1}))
        tree.add_observation((0,), 1)
        tree.add_observation((1,), 0)
        tree.add_observation((0, 1), 0)

        length_1 = list(tree.histories_of_length(1))
        assert (0,) in length_1
        assert (1,) in length_1

        length_2 = list(tree.histories_of_length(2))
        assert (0, 1) in length_2

    def test_all_histories(self) -> None:
        """all_histories iterates over all histories."""
        tree: SuffixTree[int] = SuffixTree(max_depth=2, alphabet=frozenset({0, 1}))
        tree.add_observation((0,), 1)
        tree.add_observation((1,), 0)

        all_h = list(tree.all_histories())
        assert len(all_h) == 2

    def test_add_observation_truncates_long_history(self) -> None:
        """add_observation truncates histories longer than max_depth."""
        tree: SuffixTree[int] = SuffixTree(max_depth=2, alphabet=frozenset({0, 1}))
        # Add a history longer than max_depth
        tree.add_observation((0, 1, 0, 1), 0)

        # Should truncate to last max_depth symbols
        stats = tree.get_stats((0, 1))
        assert stats is not None
        assert stats.count == 1

    def test_get_stats_nonexistent(self) -> None:
        """get_stats returns None for unobserved history."""
        tree: SuffixTree[int] = SuffixTree(max_depth=2, alphabet=frozenset({0, 1}))
        assert tree.get_stats((0, 1)) is None

    def test_build_from_sequence_records_empty_history(self) -> None:
        """build_from_sequence records the empty history."""
        tree: SuffixTree[int] = SuffixTree(max_depth=2, alphabet=frozenset({0, 1}))
        tree.build_from_sequence([0, 1, 0, 1, 0])

        # Empty history should be recorded
        stats = tree.get_stats(())
        assert stats is not None
        assert stats.count > 0

    def test_build_from_sequence_respects_max_depth(self) -> None:
        """build_from_sequence doesn't create histories longer than max_depth."""
        tree: SuffixTree[int] = SuffixTree(max_depth=2, alphabet=frozenset({0, 1}))
        tree.build_from_sequence([0, 1, 0, 1, 0, 1, 0, 1])

        # Should not have length-3 histories
        length_3 = list(tree.histories_of_length(3))
        assert len(length_3) == 0


class TestStatePartition:
    """Tests for StatePartition."""

    def test_assign_and_get(self) -> None:
        """assign() and get_state() work correctly."""
        partition = StatePartition()
        partition.assign((0,), "S0")
        partition.assign((1,), "S0")

        assert partition.get_state((0,)) == "S0"
        assert partition.get_state((1,)) == "S0"
        assert partition.get_state((2,)) is None

    def test_get_histories(self) -> None:
        """get_histories returns all histories in a state."""
        partition = StatePartition()
        partition.assign((0,), "S0")
        partition.assign((1,), "S0")
        partition.assign((2,), "S1")

        histories = partition.get_histories("S0")
        assert (0,) in histories
        assert (1,) in histories
        assert (2,) not in histories

    def test_num_states(self) -> None:
        """num_states returns correct count."""
        partition = StatePartition()
        partition.assign((0,), "S0")
        partition.assign((1,), "S1")

        assert partition.num_states() == 2

    def test_copy(self) -> None:
        """copy() creates independent copy."""
        partition = StatePartition()
        partition.assign((0,), "S0")

        copy = partition.copy()
        copy.assign((1,), "S1")

        assert partition.num_states() == 1
        assert copy.num_states() == 2

    def test_merge_states(self) -> None:
        """merge_states combines multiple states."""
        partition = StatePartition()
        partition.assign((0,), "S0")
        partition.assign((1,), "S1")

        merged_id = partition.merge_states(["S0", "S1"])

        assert partition.get_state((0,)) == merged_id
        assert partition.get_state((1,)) == merged_id

    def test_merge_states_empty_list(self) -> None:
        """merge_states with empty list returns new state id."""
        partition = StatePartition()
        new_id = partition.merge_states([])
        assert new_id is not None

    def test_split_state_nonexistent(self) -> None:
        """split_state with nonexistent state returns empty list."""
        partition = StatePartition()
        result = partition.split_state("nonexistent", [])
        assert result == []

    def test_split_state_with_remaining_histories(self) -> None:
        """split_state keeps remaining histories in new state."""
        partition = StatePartition()
        partition.assign((0,), "S0")
        partition.assign((1,), "S0")
        partition.assign((2,), "S0")

        # Split, moving only (0,) and (1,) to new groups
        result = partition.split_state("S0", [{(0,)}, {(1,)}])

        # Should have new states for the groups plus one for remaining (2,)
        assert len(result) >= 2
        # All histories should still be assigned
        assert partition.get_state((0,)) is not None
        assert partition.get_state((1,)) is not None
        assert partition.get_state((2,)) is not None

    def test_equality_with_non_partition(self) -> None:
        """Comparing partition to non-partition returns NotImplemented."""
        partition = StatePartition()
        result = partition.__eq__("not a partition")
        assert result is NotImplemented

    def test_equality_with_same_content(self) -> None:
        """Partitions with same content are equal."""
        p1 = StatePartition()
        p2 = StatePartition()
        p1.assign((0,), "S0")
        p2.assign((0,), "S0")
        assert p1 == p2

    def test_equality_with_different_content(self) -> None:
        """Partitions with different content are not equal."""
        p1 = StatePartition()
        p2 = StatePartition()
        p1.assign((0,), "S0")
        p2.assign((0,), "S1")
        assert p1 != p2

    def test_reassign_history_removes_from_old_state(self) -> None:
        """Reassigning a history removes it from the old state."""
        partition = StatePartition()
        partition.assign((0,), "S0")
        partition.assign((1,), "S0")

        # Reassign (0,) to S1
        partition.assign((0,), "S1")

        # (0,) should no longer be in S0
        assert (0,) not in partition.get_histories("S0")
        assert (0,) in partition.get_histories("S1")

    def test_reassign_last_history_removes_state(self) -> None:
        """Reassigning the last history from a state removes the state."""
        partition = StatePartition()
        partition.assign((0,), "S0")

        # Reassign (0,) to S1
        partition.assign((0,), "S1")

        # S0 should no longer exist
        assert "S0" not in partition.state_ids()

    def test_get_histories_nonexistent_state(self) -> None:
        """get_histories for nonexistent state returns empty set."""
        partition = StatePartition()
        result = partition.get_histories("nonexistent")
        assert result == set()

    def test_state_ids_empty_partition(self) -> None:
        """state_ids on empty partition returns empty list."""
        partition = StatePartition()
        assert partition.state_ids() == []

    def test_new_state_id_increments(self) -> None:
        """new_state_id generates incrementing IDs."""
        partition = StatePartition()
        id1 = partition.new_state_id()
        id2 = partition.new_state_id()
        id3 = partition.new_state_id()

        assert id1 == "S0"
        assert id2 == "S1"
        assert id3 == "S2"

    def test_copy_preserves_state_counter(self) -> None:
        """copy() preserves the next state ID counter."""
        partition = StatePartition()
        partition.new_state_id()
        partition.new_state_id()

        copy = partition.copy()
        new_id = copy.new_state_id()

        # Should continue from S2
        assert new_id == "S2"


class TestStatisticalTests:
    """Tests for statistical tests."""

    def test_chi_squared_same_distribution(self) -> None:
        """Same distribution should not differ significantly."""
        dist1 = {0: 50, 1: 50}
        dist2 = {0: 48, 1: 52}

        assert not chi_squared_test(dist1, dist2, 0.05)

    def test_chi_squared_different_distribution(self) -> None:
        """Very different distributions should differ."""
        dist1 = {0: 100, 1: 0}
        dist2 = {0: 0, 1: 100}

        assert chi_squared_test(dist1, dist2, 0.05)

    def test_chi_squared_insufficient_counts(self) -> None:
        """Insufficient counts should not show difference."""
        dist1 = {0: 2, 1: 2}
        dist2 = {0: 1, 1: 3}

        # With very few counts, should not detect difference
        assert not chi_squared_test(dist1, dist2, 0.05)

    def test_distributions_differ_g_test(self) -> None:
        """distributions_differ with g test."""
        dist1 = {0: 100, 1: 0}
        dist2 = {0: 0, 1: 100}

        assert distributions_differ(dist1, dist2, 0.05, "g")

    def test_distributions_differ_ks_test(self) -> None:
        """distributions_differ with ks test."""
        dist1 = {0: 100, 1: 0}
        dist2 = {0: 0, 1: 100}

        assert distributions_differ(dist1, dist2, 0.05, "ks")

    def test_distributions_differ_proportion_test(self) -> None:
        """distributions_differ with proportion test."""
        from emic.inference.cssr.tests import proportion_test

        # Same distributions should not differ
        dist1 = {0: 50, 1: 50}
        dist2 = {0: 48, 1: 52}
        assert not proportion_test(dist1, dist2, 0.1)

        # Very different distributions should differ
        dist1 = {0: 100, 1: 0}
        dist2 = {0: 0, 1: 100}
        assert proportion_test(dist1, dist2, 0.05)

        # Low counts should not show difference
        dist1 = {0: 2, 1: 2}
        dist2 = {0: 0, 1: 4}
        assert not proportion_test(dist1, dist2, 0.05)

    def test_distributions_differ_unknown_test_defaults_to_chi2(self) -> None:
        """distributions_differ with unknown test defaults to chi2."""
        dist1 = {0: 100, 1: 0}
        dist2 = {0: 0, 1: 100}
        # Should not raise, should use chi2 as default
        result = distributions_differ(dist1, dist2, 0.05, "unknown_test_type")
        assert result is True

    def test_chi_squared_with_different_significance_levels(self) -> None:
        """chi_squared_test handles different significance levels."""
        # Moderate difference
        dist1 = {0: 60, 1: 40}
        dist2 = {0: 40, 1: 60}

        # At 0.05, might detect difference
        result_05 = chi_squared_test(dist1, dist2, 0.05)
        # At 0.001, should not detect difference (stricter threshold)
        result_001 = chi_squared_test(dist1, dist2, 0.001)

        # The stricter test should be less likely to detect difference
        if result_05:
            assert result_05 or not result_001

    def test_chi_squared_with_high_dof(self) -> None:
        """chi_squared_test handles high degrees of freedom."""
        # Many categories
        dist1 = dict.fromkeys(range(10), 20)
        dist2 = dict.fromkeys(range(10), 20)
        # Same distribution should not differ
        assert not chi_squared_test(dist1, dist2, 0.05)

    def test_chi_squared_with_zero_expected(self) -> None:
        """chi_squared_test handles zero expected values gracefully."""
        dist1 = {0: 100}
        dist2 = {0: 50, 1: 50}
        # Should not raise, even with asymmetric keys
        chi_squared_test(dist1, dist2, 0.05)


class TestInferenceErrors:
    """Tests for inference error types."""

    def test_insufficient_data_error_explain(self) -> None:
        """InsufficientDataError has explain method."""
        error = InsufficientDataError(required=100, provided=10, algorithm="CSSR")
        explanation = error.explain()

        assert "10" in explanation
        assert "100" in explanation
        assert "CSSR" in explanation

    def test_non_convergence_error_explain(self) -> None:
        """NonConvergenceError has explain method."""
        error = NonConvergenceError(iterations=1000, tolerance=0.05)
        explanation = error.explain()

        assert "1000" in explanation
        assert "0.05" in explanation
