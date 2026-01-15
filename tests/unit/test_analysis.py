"""Tests for analysis measures."""

from __future__ import annotations

from emic.analysis import (
    AnalysisSummary,
    analyze,
    entropy_rate,
    excess_entropy,
    state_count,
    statistical_complexity,
    topological_complexity,
    transition_count,
)
from emic.sources.synthetic.biased_coin import BiasedCoinSource
from emic.sources.synthetic.golden_mean import GoldenMeanSource
from emic.sources.synthetic.periodic import PeriodicSource


class TestStructuralMeasures:
    """Tests for structural measures."""

    def test_state_count(self) -> None:
        """state_count returns correct number."""
        machine = GoldenMeanSource(p=0.5).true_machine
        assert state_count(machine) == 2

    def test_transition_count(self) -> None:
        """transition_count returns correct number."""
        machine = GoldenMeanSource(p=0.5).true_machine
        assert transition_count(machine) == 3  # A->A, A->B, B->A

    def test_topological_complexity(self) -> None:
        """topological_complexity is log2(states)."""
        machine = PeriodicSource(pattern=(0, 1, 2, 3)).true_machine
        assert abs(topological_complexity(machine) - 2.0) < 1e-10  # log2(4)


class TestInformationTheoreticMeasures:
    """Tests for information-theoretic measures."""

    def test_statistical_complexity_single_state(self) -> None:
        """Single state has zero statistical complexity."""
        machine = BiasedCoinSource(p=0.5).true_machine
        c_mu = statistical_complexity(machine)
        assert abs(c_mu - 0.0) < 1e-10

    def test_statistical_complexity_golden_mean(self) -> None:
        """Golden Mean has known statistical complexity."""
        machine = GoldenMeanSource(p=0.5).true_machine
        c_mu = statistical_complexity(machine)
        # C_mu = H(2/3, 1/3) ≈ 0.918
        assert 0.9 < c_mu < 0.95

    def test_entropy_rate_fair_coin(self) -> None:
        """Fair coin has maximum entropy rate = 1 bit."""
        machine = BiasedCoinSource(p=0.5).true_machine
        h_mu = entropy_rate(machine)
        assert abs(h_mu - 1.0) < 0.01

    def test_entropy_rate_biased_coin(self) -> None:
        """Biased coin has lower entropy rate."""
        machine = BiasedCoinSource(p=0.9).true_machine
        h_mu = entropy_rate(machine)
        # H(0.9) ≈ 0.47
        assert 0.4 < h_mu < 0.5

    def test_entropy_rate_periodic_is_zero(self) -> None:
        """Periodic (deterministic) process has zero entropy rate."""
        machine = PeriodicSource(pattern=(0, 1)).true_machine
        h_mu = entropy_rate(machine)
        assert abs(h_mu) < 1e-10

    def test_excess_entropy_equals_complexity_for_unifilar(self) -> None:
        """For unifilar machines, E = C_mu."""
        machine = GoldenMeanSource(p=0.5).true_machine
        c_mu = statistical_complexity(machine)
        e = excess_entropy(machine)
        assert abs(c_mu - e) < 1e-10


class TestAnalysisSummary:
    """Tests for analyze() function and AnalysisSummary."""

    def test_analyze_returns_summary(self) -> None:
        """analyze() returns AnalysisSummary."""
        machine = BiasedCoinSource(p=0.5).true_machine
        summary = analyze(machine)
        assert isinstance(summary, AnalysisSummary)

    def test_summary_has_all_fields(self) -> None:
        """Summary contains all expected fields."""
        machine = GoldenMeanSource(p=0.5).true_machine
        summary = analyze(machine)

        assert summary.num_states == 2
        assert summary.num_transitions == 3
        assert summary.alphabet_size == 2
        assert summary.statistical_complexity > 0
        assert summary.entropy_rate > 0
        assert abs(summary.crypticity) < 1e-10  # Unifilar => chi = 0

    def test_summary_to_dict(self) -> None:
        """to_dict() returns correct dictionary."""
        machine = BiasedCoinSource(p=0.5).true_machine
        summary = analyze(machine)
        d = summary.to_dict()

        assert "C_mu" in d
        assert "h_mu" in d
        assert "num_states" in d

    def test_summary_str(self) -> None:
        """String representation is informative."""
        machine = GoldenMeanSource(p=0.5).true_machine
        summary = analyze(machine)
        s = str(summary)

        assert "States:" in s
        assert "Entropy Rate" in s
        assert "Statistical Complexity" in s
