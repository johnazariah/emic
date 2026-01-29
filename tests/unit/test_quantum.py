"""Tests for quantum complexity measures.

Golden tests validating C_q against known values from the literature.
"""

from __future__ import annotations

from typing import ClassVar

import numpy as np
import pytest

from emic.analysis.quantum import (
    decoherence_trajectory,
    dephasing_channel,
    quantum_advantage,
    quantum_complexity,
    quantum_density_matrix,
    quantum_signal_states,
    signal_state_overlap,
)
from emic.types import EpsilonMachine, EpsilonMachineBuilder

# =============================================================================
# Test Fixtures: Simple Machines
# =============================================================================


@pytest.fixture
def fair_coin() -> EpsilonMachine[int]:
    """Single-state IID process: P(0) = P(1) = 0.5."""
    return (
        EpsilonMachineBuilder[int]()
        .add_transition("S", 0, "S", 0.5)
        .add_transition("S", 1, "S", 0.5)
        .with_start_state("S")
        .with_stationary_distribution({"S": 1.0})
        .build()
    )


@pytest.fixture
def biased_coin() -> EpsilonMachine[int]:
    """Single-state IID process: P(1) = 0.3."""
    return (
        EpsilonMachineBuilder[int]()
        .add_transition("S", 0, "S", 0.7)
        .add_transition("S", 1, "S", 0.3)
        .with_start_state("S")
        .with_stationary_distribution({"S": 1.0})
        .build()
    )


def make_perturbed_coin(p: float) -> EpsilonMachine[int]:
    """Perturbed coin with flip probability p."""
    return (
        EpsilonMachineBuilder[int]()
        .add_transition("S0", 0, "S0", 1 - p)
        .add_transition("S0", 1, "S1", p)
        .add_transition("S1", 0, "S0", p)
        .add_transition("S1", 1, "S1", 1 - p)
        .with_start_state("S0")
        .with_stationary_distribution({"S0": 0.5, "S1": 0.5})
        .build()
    )


@pytest.fixture
def perturbed_coin_03() -> EpsilonMachine[int]:
    """Perturbed coin with p = 0.3."""
    return make_perturbed_coin(0.3)


@pytest.fixture
def golden_mean() -> EpsilonMachine[int]:
    """Golden mean process: no consecutive 1s."""
    return (
        EpsilonMachineBuilder[int]()
        .add_transition("S0", 0, "S0", 0.5)
        .add_transition("S0", 1, "S1", 0.5)
        .add_transition("S1", 0, "S0", 1.0)
        .with_start_state("S0")
        .with_stationary_distribution({"S0": 2 / 3, "S1": 1 / 3})
        .build()
    )


# =============================================================================
# Tests: IID Processes (No Quantum Advantage)
# =============================================================================


class TestIIDProcesses:
    """IID processes have C_q = C_mu = 0."""

    def test_fair_coin_signal_states(self, fair_coin: EpsilonMachine[int]) -> None:
        """Fair coin has one signal state."""
        signal_states, state_ids, symbols = quantum_signal_states(fair_coin)

        assert len(signal_states) == 1
        assert len(state_ids) == 1
        assert len(symbols) == 2

        # Signal state should be normalized
        psi = signal_states[0]
        assert np.isclose(np.vdot(psi, psi), 1.0)

    def test_fair_coin_density_matrix(self, fair_coin: EpsilonMachine[int]) -> None:
        """Fair coin density matrix is rank-1 pure state."""
        rho = quantum_density_matrix(fair_coin)

        # Should be 2x2 (2 symbols, 1 state)
        assert rho.shape == (2, 2)

        # Trace should be 1
        assert np.isclose(np.trace(rho), 1.0)

        # Pure state: rho^2 = rho
        rho_sq = rho @ rho
        assert np.allclose(rho, rho_sq)

    def test_fair_coin_quantum_complexity(self, fair_coin: EpsilonMachine[int]) -> None:
        """Fair coin has C_q = 0 (pure state)."""
        c_q = quantum_complexity(fair_coin)
        assert np.isclose(c_q, 0.0, atol=1e-10)

    def test_fair_coin_quantum_advantage(self, fair_coin: EpsilonMachine[int]) -> None:
        """Fair coin has no quantum advantage."""
        delta = quantum_advantage(fair_coin)
        assert np.isclose(delta, 0.0, atol=1e-10)

    def test_biased_coin_quantum_complexity(self, biased_coin: EpsilonMachine[int]) -> None:
        """Biased coin also has C_q = 0."""
        c_q = quantum_complexity(biased_coin)
        assert np.isclose(c_q, 0.0, atol=1e-10)


# =============================================================================
# Tests: Perturbed Coin (Primary Validation)
# =============================================================================


class TestPerturbedCoin:
    """Perturbed coin is the canonical process with quantum advantage."""

    # Expected values from analytic formula: lambda_pm = 0.5 ± sqrt(p(1-p))
    EXPECTED_CQ: ClassVar[dict[float, float]] = {
        0.05: 0.858,
        0.10: 0.722,
        0.15: 0.592,
        0.20: 0.469,
        0.25: 0.355,
        0.30: 0.250,
        0.35: 0.158,
        0.40: 0.081,
        0.45: 0.025,
    }

    def test_perturbed_coin_signal_states(self, perturbed_coin_03: EpsilonMachine[int]) -> None:
        """Perturbed coin has two overlapping signal states."""
        signal_states, state_ids, symbols = quantum_signal_states(perturbed_coin_03)

        assert len(signal_states) == 2
        assert len(state_ids) == 2
        assert len(symbols) == 2

        # Both should be normalized
        for psi in signal_states:
            assert np.isclose(np.vdot(psi, psi), 1.0)

    def test_perturbed_coin_overlap(self, perturbed_coin_03: EpsilonMachine[int]) -> None:
        """Signal states should have non-zero overlap."""
        overlap = signal_state_overlap(perturbed_coin_03)

        # Diagonal should be 1
        assert np.isclose(overlap[0, 0], 1.0)
        assert np.isclose(overlap[1, 1], 1.0)

        # Off-diagonal should be 2*sqrt(p*(1-p)) = 2*sqrt(0.21) ≈ 0.917
        expected_overlap = 2 * np.sqrt(0.3 * 0.7)
        assert np.isclose(overlap[0, 1], expected_overlap, atol=0.001)
        assert np.isclose(overlap[1, 0], expected_overlap, atol=0.001)

    def test_perturbed_coin_density_matrix(self, perturbed_coin_03: EpsilonMachine[int]) -> None:
        """Density matrix should be mixed state with off-diagonals."""
        rho = quantum_density_matrix(perturbed_coin_03)

        # Trace should be 1
        assert np.isclose(np.trace(rho), 1.0)

        # Should have non-zero off-diagonals (mixed state)
        # The density matrix lives in a 2D subspace
        eigenvalues = np.linalg.eigvalsh(rho)
        nonzero_eigs = eigenvalues[eigenvalues > 1e-10]

        # Should have 2 non-zero eigenvalues for p=0.3
        assert len(nonzero_eigs) == 2

    def test_perturbed_coin_c_mu_is_one(self, perturbed_coin_03: EpsilonMachine[int]) -> None:
        """Perturbed coin always has C_mu = 1 bit."""
        from emic.analysis import statistical_complexity

        c_mu = statistical_complexity(perturbed_coin_03)
        assert np.isclose(c_mu, 1.0, atol=0.001)

    @pytest.mark.parametrize("p,expected_cq", list(EXPECTED_CQ.items()))
    def test_perturbed_coin_cq_values(self, p: float, expected_cq: float) -> None:
        """C_q should match analytic values."""
        machine = make_perturbed_coin(p)
        c_q = quantum_complexity(machine)

        # Allow 0.01 bit tolerance
        assert np.isclose(c_q, expected_cq, atol=0.01), f"p={p}: expected {expected_cq}, got {c_q}"

    def test_perturbed_coin_quantum_advantage(self, perturbed_coin_03: EpsilonMachine[int]) -> None:
        """Perturbed coin with p=0.3 has ~0.75 bit advantage."""
        delta = quantum_advantage(perturbed_coin_03)

        # C_mu = 1, C_q ≈ 0.25, so advantage ≈ 0.75
        assert np.isclose(delta, 0.75, atol=0.01)

    def test_hierarchy_e_leq_cq_leq_cmu(self, perturbed_coin_03: EpsilonMachine[int]) -> None:
        """Verify E <= C_q <= C_mu."""
        from emic.analysis import excess_entropy, statistical_complexity

        e = excess_entropy(perturbed_coin_03)
        c_q = quantum_complexity(perturbed_coin_03)
        c_mu = statistical_complexity(perturbed_coin_03)

        assert e <= c_q + 1e-10, f"E={e} > C_q={c_q}"
        assert c_q <= c_mu + 1e-10, f"C_q={c_q} > C_mu={c_mu}"


# =============================================================================
# Tests: Golden Mean Process
# =============================================================================


class TestGoldenMean:
    """Golden mean process tests."""

    def test_golden_mean_c_mu(self, golden_mean: EpsilonMachine[int]) -> None:
        """Golden mean has C_mu = H(2/3, 1/3) ≈ 0.918 bits."""
        from emic.analysis import statistical_complexity

        c_mu = statistical_complexity(golden_mean)

        # H(2/3, 1/3) = -2/3*log2(2/3) - 1/3*log2(1/3)
        expected = -(2 / 3) * np.log2(2 / 3) - (1 / 3) * np.log2(1 / 3)
        assert np.isclose(c_mu, expected, atol=0.001)

    def test_golden_mean_has_quantum_advantage(self, golden_mean: EpsilonMachine[int]) -> None:
        """Golden mean should have quantum advantage."""
        c_q = quantum_complexity(golden_mean)
        delta = quantum_advantage(golden_mean)

        # C_q should be less than C_mu
        assert delta > 0, "Golden mean should have quantum advantage"
        assert c_q < 0.918, f"C_q={c_q} should be less than C_mu=0.918"


# =============================================================================
# Tests: Decoherence Trajectory
# =============================================================================


class TestDecoherenceTrajectory:
    """Tests for decoherence trajectory computation."""

    def test_dephasing_channel_gamma_zero(self, perturbed_coin_03: EpsilonMachine[int]) -> None:
        """gamma=0 should leave density matrix unchanged."""
        rho = quantum_density_matrix(perturbed_coin_03)
        rho_dephased = dephasing_channel(rho, 0.0)

        assert np.allclose(rho, rho_dephased)

    def test_dephasing_channel_gamma_one(self, perturbed_coin_03: EpsilonMachine[int]) -> None:
        """gamma=1 should give diagonal matrix."""
        rho = quantum_density_matrix(perturbed_coin_03)
        rho_dephased = dephasing_channel(rho, 1.0)

        # Should be diagonal
        off_diag = rho_dephased - np.diag(np.diag(rho_dephased))
        assert np.allclose(off_diag, 0.0)

    def test_trajectory_endpoints(self, perturbed_coin_03: EpsilonMachine[int]) -> None:
        """Trajectory endpoints should match C_q and C_mu."""
        from emic.analysis import statistical_complexity

        trajectory = decoherence_trajectory(perturbed_coin_03)

        # First point: gamma=0, should equal C_q
        gamma_0, c_q_0 = trajectory[0]
        assert gamma_0 == 0.0
        assert np.isclose(c_q_0, quantum_complexity(perturbed_coin_03), atol=1e-10)

        # Last point: gamma=1, should equal C_mu
        gamma_1, c_q_1 = trajectory[-1]
        assert gamma_1 == 1.0
        # Note: C_q(1) = H(diag(rho)), which equals C_mu for perturbed coin
        c_mu = statistical_complexity(perturbed_coin_03)
        assert np.isclose(c_q_1, c_mu, atol=0.01)

    def test_trajectory_monotonic(self, perturbed_coin_03: EpsilonMachine[int]) -> None:
        """C_q(gamma) should be monotonically non-decreasing."""
        trajectory = decoherence_trajectory(perturbed_coin_03)

        values = [c_q for _, c_q in trajectory]
        for i in range(len(values) - 1):
            assert values[i] <= values[i + 1] + 1e-10, (
                f"Not monotonic: C_q({trajectory[i][0]})={values[i]} > "
                f"C_q({trajectory[i + 1][0]})={values[i + 1]}"
            )

    def test_trajectory_expected_values(self, perturbed_coin_03: EpsilonMachine[int]) -> None:
        """Trajectory should match expected values from validation plan."""
        expected = {
            0.0: 0.250,
            0.2: 0.567,
            0.4: 0.769,
            0.6: 0.901,
            0.8: 0.976,
            1.0: 1.000,
        }

        trajectory = decoherence_trajectory(perturbed_coin_03, gamma_values=list(expected.keys()))

        for gamma, c_q in trajectory:
            expected_cq = expected[gamma]
            assert np.isclose(
                c_q, expected_cq, atol=0.01
            ), f"gamma={gamma}: expected {expected_cq}, got {c_q}"


# =============================================================================
# Tests: Edge Cases
# =============================================================================


class TestEdgeCases:
    """Edge cases and numerical stability."""

    def test_perturbed_coin_p_near_half(self) -> None:
        """Near p=0.5, C_q should approach 0."""
        machine = make_perturbed_coin(0.49)
        c_q = quantum_complexity(machine)

        # Should be very small
        assert c_q < 0.01, f"C_q={c_q} should be near 0 for p=0.49"

    def test_perturbed_coin_p_near_zero(self) -> None:
        """Near p=0, C_q should approach C_mu=1."""
        machine = make_perturbed_coin(0.01)
        c_q = quantum_complexity(machine)

        # Should be close to 1
        assert c_q > 0.95, f"C_q={c_q} should be near 1 for p=0.01"

    def test_dephasing_channel_invalid_gamma(self, perturbed_coin_03: EpsilonMachine[int]) -> None:
        """Dephasing with invalid gamma should raise."""
        rho = quantum_density_matrix(perturbed_coin_03)

        with pytest.raises(ValueError, match="gamma must be in"):
            dephasing_channel(rho, -0.1)

        with pytest.raises(ValueError, match="gamma must be in"):
            dephasing_channel(rho, 1.5)
