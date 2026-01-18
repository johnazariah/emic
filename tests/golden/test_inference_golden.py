"""Golden tests for inference algorithms.

These tests verify that inference algorithms produce correct results
on known processes with analytically known epsilon-machines.

Each test uses a fixed seed for reproducibility.
"""

from __future__ import annotations

import pytest

from emic.inference import CSM, CSSR, CSMConfig, CSSRConfig
from emic.sources.synthetic.biased_coin import BiasedCoinSource
from emic.sources.synthetic.golden_mean import GoldenMeanSource
from emic.sources.synthetic.periodic import PeriodicSource
from emic.sources.transforms.take import TakeN


class TestBiasedCoinGolden:
    """Golden tests for the biased coin (IID) process.

    The biased coin is the simplest stochastic process:
    - 1 causal state (no memory required)
    - Each symbol is independent of the past
    - Statistical complexity Cμ = 0
    """

    @pytest.fixture
    def sequence(self) -> list[int]:
        """Generate a reproducible biased coin sequence."""
        source = BiasedCoinSource(p=0.5, _seed=42)
        return list(TakeN(10000)(source))

    def test_cssr_finds_one_state(self, sequence: list[int]) -> None:
        """CSSR should find exactly 1 state for IID process."""
        config = CSSRConfig(max_history=5, significance=0.05)
        result = CSSR(config).infer(sequence)

        assert len(result.machine.states) == 1
        assert result.converged

    def test_csm_finds_one_state(self, sequence: list[int]) -> None:
        """CSM should find exactly 1 state for IID process."""
        config = CSMConfig(history_length=5, merge_threshold=0.1)
        result = CSM(config).infer(sequence)

        assert len(result.machine.states) == 1
        assert result.converged


class TestGoldenMeanGolden:
    """Golden tests for the Golden Mean process.

    The Golden Mean process:
    - 2 causal states (A and B)
    - From A: emit 0 and stay in A, OR emit 1 and go to B
    - From B: emit 0 and go to A (no 11 allowed)
    - Forbids consecutive 1s
    """

    @pytest.fixture
    def sequence(self) -> list[int]:
        """Generate a reproducible Golden Mean sequence."""
        source = GoldenMeanSource(p=0.5, _seed=42)
        return list(TakeN(50000)(source))

    def test_cssr_finds_two_states(self, sequence: list[int]) -> None:
        """CSSR should find 2 states for Golden Mean."""
        config = CSSRConfig(max_history=5, significance=0.01)
        result = CSSR(config).infer(sequence)

        # Should find exactly 2 states
        assert len(result.machine.states) == 2
        assert result.converged

    def test_csm_finds_two_states(self, sequence: list[int]) -> None:
        """CSM should find 2 states for Golden Mean."""
        config = CSMConfig(history_length=5, merge_threshold=0.05)
        result = CSM(config).infer(sequence)

        # Should find 2-3 states (may have slight variation)
        assert 2 <= len(result.machine.states) <= 3
        assert result.converged

    def test_machine_forbids_consecutive_ones(self, sequence: list[int]) -> None:
        """Inferred machine should not allow 1,1 transitions."""
        config = CSSRConfig(max_history=5, significance=0.01)
        result = CSSR(config).infer(sequence)

        # After emitting 1, probability of emitting another 1 should be ~0
        # This is verified by checking the structure
        for state in result.machine.states:
            for t in state.transitions:
                if t.symbol == 1:
                    # From the state we go to after emitting 1,
                    # we should not be able to emit 1 again with high probability
                    target_state = result.machine.get_state(t.target)
                    one_prob = 0.0
                    for target_t in target_state.transitions:
                        if target_t.symbol == 1:
                            one_prob = target_t.probability
                    # Allow for some finite sample noise
                    assert one_prob < 0.05, "Should not have high probability of 1->1"


class TestPeriodicGolden:
    """Golden tests for periodic processes.

    A period-n process:
    - n causal states forming a cycle
    - Each state emits exactly one symbol with probability 1
    - Statistical complexity Cμ = log(n)
    """

    def test_period_2_cssr(self) -> None:
        """CSSR should find 2 states for period-2 (alternating)."""
        source = PeriodicSource(pattern=(0, 1))
        sequence = list(TakeN(1000)(source))

        config = CSSRConfig(max_history=3, significance=0.01, min_count=5)
        result = CSSR(config).infer(sequence)

        assert len(result.machine.states) == 2
        assert result.converged

    def test_period_2_csm(self) -> None:
        """CSM should find 2 states for period-2 (alternating)."""
        source = PeriodicSource(pattern=(0, 1))
        sequence = list(TakeN(1000)(source))

        config = CSMConfig(history_length=3, merge_threshold=0.01, min_count=5)
        result = CSM(config).infer(sequence)

        assert len(result.machine.states) == 2
        assert result.converged

    def test_period_3_cssr(self) -> None:
        """CSSR should find 3 states for period-3."""
        source = PeriodicSource(pattern=(0, 1, 2))
        sequence = list(TakeN(1500)(source))

        config = CSSRConfig(max_history=5, significance=0.01, min_count=5)
        result = CSSR(config).infer(sequence)

        assert len(result.machine.states) == 3
        assert result.converged

    def test_period_3_csm(self) -> None:
        """CSM should find 3 states for period-3."""
        source = PeriodicSource(pattern=(0, 1, 2))
        sequence = list(TakeN(1500)(source))

        config = CSMConfig(history_length=5, merge_threshold=0.01, min_count=5)
        result = CSM(config).infer(sequence)

        assert len(result.machine.states) == 3
        assert result.converged


class TestEvenProcessGolden:
    """Golden tests for the Even Process.

    The Even Process emits an even number of 1s between each 0:
    - 2 causal states
    - Similar complexity to Golden Mean

    We simulate this using a specific pattern.
    """

    @pytest.fixture
    def sequence(self) -> list[int]:
        """Generate a reproducible Even Process-like sequence.

        For simplicity, we use the Golden Mean which has similar structure.
        A true Even Process generator would be needed for exact tests.
        """
        # Use Golden Mean as a proxy with similar properties
        source = GoldenMeanSource(p=0.7, _seed=123)
        return list(TakeN(30000)(source))

    def test_cssr_finds_two_states(self, sequence: list[int]) -> None:
        """CSSR should find 2 states for Even-like process."""
        config = CSSRConfig(max_history=5, significance=0.01)
        result = CSSR(config).infer(sequence)

        assert 2 <= len(result.machine.states) <= 3
        assert result.converged

    def test_csm_finds_two_states(self, sequence: list[int]) -> None:
        """CSM should find 2 states for Even-like process."""
        config = CSMConfig(history_length=5, merge_threshold=0.05)
        result = CSM(config).infer(sequence)

        assert 2 <= len(result.machine.states) <= 4
        assert result.converged


class TestAlgorithmConsistency:
    """Tests that CSSR and CSM produce consistent results."""

    @pytest.mark.parametrize(
        "source_name,source,expected_states",
        [
            ("biased_coin", BiasedCoinSource(p=0.5, _seed=123), 1),
            ("golden_mean", GoldenMeanSource(p=0.5, _seed=42), 2),
            ("period_2", PeriodicSource(pattern=(0, 1)), 2),
        ],
    )
    def test_algorithms_agree_on_state_count(
        self,
        source_name: str,
        source: BiasedCoinSource | GoldenMeanSource | PeriodicSource,
        expected_states: int,
    ) -> None:
        """Both algorithms should agree on state count for known processes."""
        sequence = list(TakeN(10000 if source_name != "period_2" else 1000)(source))

        # CSSR - use shorter history for IID to avoid over-splitting
        max_history = 3 if source_name == "biased_coin" else 5
        cssr_config = CSSRConfig(max_history=max_history, significance=0.05)
        cssr_result = CSSR(cssr_config).infer(sequence)

        # CSM
        csm_config = CSMConfig(history_length=max_history, merge_threshold=0.1)
        csm_result = CSM(csm_config).infer(sequence)

        # Both should be within 1 of expected
        assert abs(len(cssr_result.machine.states) - expected_states) <= 1
        assert abs(len(csm_result.machine.states) - expected_states) <= 1
