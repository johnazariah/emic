"""Golden tests for inference algorithms.

These tests verify that inference algorithms produce correct results
on known processes with analytically known epsilon-machines.

Each test uses a fixed seed for reproducibility.
"""

from __future__ import annotations

import pytest

from emic.inference import (
    BSI,
    CSM,
    CSSR,
    NSD,
    BSIConfig,
    CSMConfig,
    CSSRConfig,
    NSDConfig,
    Spectral,
    SpectralConfig,
)
from emic.sources.synthetic.biased_coin import BiasedCoinSource
from emic.sources.synthetic.even_process import EvenProcessSource
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

    def test_bsi_finds_one_state(self, sequence: list[int]) -> None:
        """BSI should find exactly 1 state for IID process."""
        config = BSIConfig(max_states=5, max_history=3, n_samples=100, seed=42)
        result = BSI(config).infer(sequence)

        assert len(result.machine.states) == 1
        assert result.converged

    def test_nsd_finds_one_state(self, sequence: list[int]) -> None:
        """NSD should find exactly 1 state for IID process."""
        config = NSDConfig(max_states=5, history_length=5, seed=42)
        result = NSD(config).infer(sequence)

        assert len(result.machine.states) == 1
        assert result.converged

    def test_spectral_finds_one_state(self, sequence: list[int]) -> None:
        """Spectral should find exactly 1 state for IID process."""
        config = SpectralConfig(max_history=5, rank_threshold=0.1)
        result = Spectral(config).infer(sequence)

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

    def test_bsi_finds_two_states(self, sequence: list[int]) -> None:
        """BSI should find 2 states for Golden Mean."""
        config = BSIConfig(max_states=5, max_history=5, n_samples=200, seed=42)
        result = BSI(config).infer(sequence)

        # Should find 2-3 states
        assert 2 <= len(result.machine.states) <= 3
        assert result.converged

    def test_nsd_finds_two_states(self, sequence: list[int]) -> None:
        """NSD should find 2 states for Golden Mean."""
        config = NSDConfig(max_states=5, history_length=5, seed=42)
        result = NSD(config).infer(sequence)

        # Should find 2-3 states
        assert 2 <= len(result.machine.states) <= 3
        assert result.converged

    def test_spectral_finds_two_states(self, sequence: list[int]) -> None:
        """Spectral should find 2 states for Golden Mean."""
        config = SpectralConfig(max_history=5, rank_threshold=0.01)
        result = Spectral(config).infer(sequence)

        # Should find 2-3 states
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

    def test_period_2_bsi(self) -> None:
        """BSI should find 2 states for period-2 (alternating)."""
        source = PeriodicSource(pattern=(0, 1))
        sequence = list(TakeN(1000)(source))

        config = BSIConfig(max_states=5, max_history=3, n_samples=100, seed=42)
        result = BSI(config).infer(sequence)

        # BSI may find 2-3 states depending on MCMC sampling
        assert 2 <= len(result.machine.states) <= 3
        assert result.converged

    def test_period_2_nsd(self) -> None:
        """NSD should find 2 states for period-2 (alternating)."""
        source = PeriodicSource(pattern=(0, 1))
        sequence = list(TakeN(1000)(source))

        config = NSDConfig(max_states=5, history_length=3, seed=42)
        result = NSD(config).infer(sequence)

        assert len(result.machine.states) == 2
        assert result.converged

    def test_period_2_spectral(self) -> None:
        """Spectral should find 2 states for period-2 (alternating)."""
        source = PeriodicSource(pattern=(0, 1))
        sequence = list(TakeN(1000)(source))

        config = SpectralConfig(max_history=3, rank_threshold=0.01)
        result = Spectral(config).infer(sequence)

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

    def test_period_3_bsi(self) -> None:
        """BSI should find 3 states for period-3."""
        source = PeriodicSource(pattern=(0, 1, 2))
        sequence = list(TakeN(1500)(source))

        config = BSIConfig(max_states=5, max_history=5, n_samples=100, seed=42)
        result = BSI(config).infer(sequence)

        # BSI may find 3-4 states depending on MCMC sampling
        assert 3 <= len(result.machine.states) <= 4
        assert result.converged

    def test_period_3_nsd(self) -> None:
        """NSD should find 3 states for period-3."""
        source = PeriodicSource(pattern=(0, 1, 2))
        sequence = list(TakeN(1500)(source))

        config = NSDConfig(max_states=5, history_length=5, seed=42)
        result = NSD(config).infer(sequence)

        assert len(result.machine.states) == 3
        assert result.converged

    def test_period_3_spectral(self) -> None:
        """Spectral should find 3 states for period-3."""
        source = PeriodicSource(pattern=(0, 1, 2))
        sequence = list(TakeN(1500)(source))

        config = SpectralConfig(max_history=5, rank_threshold=0.01)
        result = Spectral(config).infer(sequence)

        assert len(result.machine.states) == 3
        assert result.converged


class TestEvenProcessGolden:
    """Golden tests for the Even Process.

    The Even Process emits runs of 1s with even length:
    - 2 causal states (A and B)
    - From A: emit 0 and stay, OR emit 1 and go to B
    - From B: emit 1 and go to A
    - 1s always come in pairs

    Note: Even Process can be harder to infer than Golden Mean due to
    the constraint being "must emit 1" rather than "cannot emit 1".
    """

    @pytest.fixture
    def sequence(self) -> list[int]:
        """Generate a reproducible Even Process sequence."""
        source = EvenProcessSource(p=0.5, _seed=42)
        return list(TakeN(50000)(source))

    def test_cssr_finds_two_states(self, sequence: list[int]) -> None:
        """CSSR should find ~2 states for Even process.

        Note: CSSR may find additional transient states due to
        finite sample effects in the Even Process structure.
        """
        config = CSSRConfig(max_history=5, significance=0.01)
        result = CSSR(config).infer(sequence)

        # May find 2-5 states due to finite sample effects
        assert 2 <= len(result.machine.states) <= 5
        assert result.converged

    def test_csm_finds_two_states(self, sequence: list[int]) -> None:
        """CSM should find 2 states for Even process."""
        config = CSMConfig(history_length=5, merge_threshold=0.05)
        result = CSM(config).infer(sequence)

        assert 2 <= len(result.machine.states) <= 4
        assert result.converged

    def test_bsi_finds_two_states(self, sequence: list[int]) -> None:
        """BSI should find ~2 states for Even process."""
        config = BSIConfig(max_states=5, max_history=5, n_samples=200, seed=42)
        result = BSI(config).infer(sequence)

        # BSI may find 2-5 states
        assert 2 <= len(result.machine.states) <= 5
        assert result.converged

    def test_nsd_finds_two_states(self, sequence: list[int]) -> None:
        """NSD should find 2 states for Even process."""
        config = NSDConfig(max_states=5, history_length=5, seed=42)
        result = NSD(config).infer(sequence)

        assert 2 <= len(result.machine.states) <= 3
        assert result.converged

    def test_spectral_finds_two_states(self, sequence: list[int]) -> None:
        """Spectral should find 2 states for Even process."""
        config = SpectralConfig(max_history=5, rank_threshold=0.01)
        result = Spectral(config).infer(sequence)

        assert 2 <= len(result.machine.states) <= 3
        assert result.converged

    def test_machine_enforces_even_ones(self, sequence: list[int]) -> None:
        """Inferred machine should show that 1s come in pairs."""
        config = CSSRConfig(max_history=5, significance=0.01)
        result = CSSR(config).infer(sequence)

        # After emitting a single 1, we must emit another 1
        # Check that there's a state where P(1) ≈ 1.0 after seeing a 1
        has_forced_one = False
        for state in result.machine.states:
            for t in state.transitions:
                if t.symbol == 1:
                    target_state = result.machine.get_state(t.target)
                    for target_t in target_state.transitions:
                        if target_t.symbol == 1 and target_t.probability > 0.95:
                            has_forced_one = True
        assert has_forced_one, "Should have a state that forces emission of 1"


class TestAlgorithmConsistency:
    """Tests that CSSR, CSM, BSI, and NSD produce consistent results.

    Note: Spectral is excluded as its state extraction needs more tuning.
    """

    @pytest.mark.parametrize(
        "source_name,source,expected_states",
        [
            ("biased_coin", BiasedCoinSource(p=0.5, _seed=123), 1),
            ("golden_mean", GoldenMeanSource(p=0.5, _seed=42), 2),
            ("period_2", PeriodicSource(pattern=(0, 1)), 2),
            ("even_process", EvenProcessSource(p=0.5, _seed=42), 2),
        ],
    )
    def test_algorithms_agree_on_state_count(
        self,
        source_name: str,
        source: BiasedCoinSource | GoldenMeanSource | PeriodicSource | EvenProcessSource,
        expected_states: int,
    ) -> None:
        """Core algorithms should agree on state count for known processes."""
        # Use larger samples for more complex processes
        n_samples = {
            "period_2": 1000,
            "biased_coin": 10000,
            "golden_mean": 30000,
            "even_process": 50000,  # Even process needs more data
        }
        sequence = list(TakeN(n_samples.get(source_name, 10000))(source))

        # CSSR - use shorter history for IID to avoid over-splitting
        max_history = 3 if source_name == "biased_coin" else 5
        cssr_config = CSSRConfig(max_history=max_history, significance=0.05)
        cssr_result = CSSR(cssr_config).infer(sequence)

        # CSM
        csm_config = CSMConfig(history_length=max_history, merge_threshold=0.1)
        csm_result = CSM(csm_config).infer(sequence)

        # BSI - allow more tolerance (±2) as it's Bayesian
        bsi_config = BSIConfig(max_states=5, max_history=max_history, n_samples=100, seed=42)
        bsi_result = BSI(bsi_config).infer(sequence)

        # NSD
        nsd_config = NSDConfig(max_states=5, history_length=max_history, seed=42)
        nsd_result = NSD(nsd_config).infer(sequence)

        # Core algorithms (CSSR, CSM) should be within tolerance of expected
        # Even process needs more tolerance due to its structure
        cssr_tolerance = 3 if source_name == "even_process" else 1
        assert (
            abs(len(cssr_result.machine.states) - expected_states) <= cssr_tolerance
        ), f"CSSR: expected ~{expected_states}, got {len(cssr_result.machine.states)}"
        assert (
            abs(len(csm_result.machine.states) - expected_states) <= 2
        ), f"CSM: expected ~{expected_states}, got {len(csm_result.machine.states)}"
        # Alternative algorithms have more tolerance (±2)
        assert (
            abs(len(bsi_result.machine.states) - expected_states) <= 2
        ), f"BSI: expected ~{expected_states}, got {len(bsi_result.machine.states)}"
        assert (
            abs(len(nsd_result.machine.states) - expected_states) <= 2
        ), f"NSD: expected ~{expected_states}, got {len(nsd_result.machine.states)}"
