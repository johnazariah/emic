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
        assert abs(dist[0] - 0.5) < 1e-10
        assert abs(dist[1] - 0.5) < 1e-10

    def test_empty_distribution(self) -> None:
        """Empty stats has count 0."""
        stats = HistoryStats(history=())
        assert stats.count == 0


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
