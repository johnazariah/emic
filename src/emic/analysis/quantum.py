"""Quantum complexity measures for epsilon-machines.

This module implements quantum computational mechanics measures,
computing the quantum statistical complexity C_q and related quantities.

The key insight (Gu et al. 2012): Classical ε-machines must distinguish
causal states orthogonally, but quantum models can encode states
non-orthogonally, requiring less memory when transitions merge paths.

Key references:
- Gu et al. (2012) "Quantum mechanics can reduce complexity of classical models"
- Thompson et al. (2018) "Causal Asymmetry in a Quantum World"
"""

from __future__ import annotations

from collections.abc import Hashable
from typing import TYPE_CHECKING, TypeVar

import numpy as np

if TYPE_CHECKING:
    from numpy.typing import NDArray

    from emic.types import EpsilonMachine

A = TypeVar("A", bound=Hashable)


def quantum_signal_states(
    machine: EpsilonMachine[A],
) -> tuple[list[NDArray[np.complex128]], list[str], list[A]]:
    """
    Construct quantum signal states for each causal state.

    For causal state S_j, the signal state is:
        |s_j> = sum_{k,x} sqrt(T^(x)_{jk}) |x> ⊗ |k>

    where T^(x)_{jk} is the probability of emitting x and transitioning
    from state j to state k.

    Args:
        machine: The epsilon-machine

    Returns:
        Tuple of (signal_states, state_ids, symbols) where:
        - signal_states[j] is the signal state vector for state j
        - state_ids[j] is the state ID for index j
        - symbols[x] is the symbol for index x
    """
    states = list(machine.states)
    state_ids = [s.id for s in states]
    state_to_idx = {s.id: i for i, s in enumerate(states)}
    symbols = list(machine.alphabet)
    symbol_to_idx = {x: i for i, x in enumerate(symbols)}

    n_states = len(states)
    n_symbols = len(symbols)
    dim = n_states * n_symbols  # Hilbert space dimension

    signal_states: list[NDArray[np.complex128]] = []

    for state in states:
        # Construct |s_j>
        psi = np.zeros(dim, dtype=np.complex128)

        for trans in state.transitions:
            x_idx = symbol_to_idx[trans.symbol]
            k_idx = state_to_idx[trans.target]
            # Index in tensor product: |x> ⊗ |k>
            idx = x_idx * n_states + k_idx
            psi[idx] = np.sqrt(trans.probability)

        signal_states.append(psi)

    return signal_states, state_ids, symbols


def quantum_density_matrix(machine: EpsilonMachine[A]) -> NDArray[np.complex128]:
    """
    Construct the average density matrix for the q-machine.

    The density matrix is:
        rho = sum_j pi_j |s_j><s_j|

    where pi_j is the stationary probability of state j.

    Args:
        machine: The epsilon-machine

    Returns:
        The density matrix as a complex numpy array
    """
    signal_states, state_ids, _ = quantum_signal_states(machine)
    pi = machine.stationary_distribution

    dim = len(signal_states[0])
    rho = np.zeros((dim, dim), dtype=np.complex128)

    for psi, sid in zip(signal_states, state_ids, strict=True):
        prob = pi.probs.get(sid, 0.0)
        rho += prob * np.outer(psi, np.conj(psi))

    return rho


def _von_neumann_entropy(rho: NDArray[np.complex128], tol: float = 1e-12) -> float:
    """
    Compute von Neumann entropy S(rho) = -Tr(rho log2 rho).

    Args:
        rho: Density matrix (Hermitian, positive semi-definite)
        tol: Tolerance for treating eigenvalues as zero

    Returns:
        Von Neumann entropy in bits
    """
    # Compute eigenvalues (real for Hermitian matrix)
    eigenvalues = np.linalg.eigvalsh(rho)

    # Filter out small/negative eigenvalues (numerical noise)
    eigenvalues = eigenvalues[eigenvalues > tol]

    if len(eigenvalues) == 0:
        return 0.0

    # S = -sum(lambda * log2(lambda))
    return float(-np.sum(eigenvalues * np.log2(eigenvalues)))


def quantum_complexity(machine: EpsilonMachine[A]) -> float:
    """
    Compute the quantum statistical complexity C_q.

    C_q = S(rho) = -Tr(rho log2 rho)

    where rho is the average density matrix of the q-machine.

    The key inequality holds:
        E <= C_q <= C_mu

    where E is excess entropy and C_mu is classical statistical complexity.

    Args:
        machine: The epsilon-machine

    Returns:
        Quantum statistical complexity in bits

    Examples:
        >>> from emic.sources.synthetic.perturbed_coin import PerturbedCoinSource
        >>> machine = PerturbedCoinSource(p=0.3).true_machine
        >>> c_q = quantum_complexity(machine)
        >>> 0 < c_q < 1  # Should be between 0 and C_mu=1
        True
    """
    rho = quantum_density_matrix(machine)
    return _von_neumann_entropy(rho)


def quantum_advantage(machine: EpsilonMachine[A]) -> float:
    """
    Compute the quantum memory advantage Delta_q = C_mu - C_q.

    This measures how many bits of memory are saved by using a quantum
    model instead of a classical epsilon-machine.

    Args:
        machine: The epsilon-machine

    Returns:
        Quantum advantage in bits (>= 0)

    Examples:
        >>> from emic.sources.synthetic.perturbed_coin import PerturbedCoinSource
        >>> machine = PerturbedCoinSource(p=0.3).true_machine
        >>> delta = quantum_advantage(machine)
        >>> delta > 0  # Perturbed coin has quantum advantage
        True
    """
    from emic.analysis import statistical_complexity

    c_mu = statistical_complexity(machine)
    c_q = quantum_complexity(machine)
    return max(0.0, c_mu - c_q)


def signal_state_overlap(machine: EpsilonMachine[A]) -> NDArray[np.float64]:
    """
    Compute the overlap matrix <s_j|s_k> between signal states.

    The overlap is:
        <s_j|s_k> = sum_{l,x} sqrt(T^(x)_{jl} T^(x)_{kl})

    Non-zero off-diagonal elements indicate irreversibility (paths merge),
    which enables quantum advantage.

    Args:
        machine: The epsilon-machine

    Returns:
        Overlap matrix (n_states x n_states), real and symmetric
    """
    signal_states, _, _ = quantum_signal_states(machine)
    n = len(signal_states)

    overlap = np.zeros((n, n), dtype=np.float64)
    for j in range(n):
        for k in range(n):
            overlap[j, k] = np.real(np.vdot(signal_states[j], signal_states[k]))

    return overlap


def dephasing_channel(rho: NDArray[np.complex128], gamma: float) -> NDArray[np.complex128]:
    """
    Apply dephasing channel with strength gamma.

    D_gamma(rho) = (1-gamma)*rho + gamma*diag(rho)

    Args:
        rho: Input density matrix
        gamma: Dephasing strength in [0, 1]
            - gamma=0: no decoherence (identity)
            - gamma=1: complete dephasing (fully classical)

    Returns:
        Decohered density matrix
    """
    if not 0 <= gamma <= 1:
        msg = f"gamma must be in [0, 1], got {gamma}"
        raise ValueError(msg)

    diagonal = np.diag(np.diag(rho))
    return (1 - gamma) * rho + gamma * diagonal


def decoherence_trajectory(
    machine: EpsilonMachine[A],
    gamma_values: list[float] | None = None,
) -> list[tuple[float, float]]:
    """
    Compute C_q(gamma) along a decoherence trajectory.

    As gamma increases from 0 to 1, C_q interpolates from the quantum
    value to the classical value:
        C_q(0) = C_q (pure quantum)
        C_q(1) = C_mu (fully classical, approximately)

    Args:
        machine: The epsilon-machine
        gamma_values: List of gamma values to sample. Default: 11 points
                      from 0 to 1.

    Returns:
        List of (gamma, C_q(gamma)) pairs
    """
    if gamma_values is None:
        gamma_values = [i / 10 for i in range(11)]

    rho = quantum_density_matrix(machine)

    results: list[tuple[float, float]] = []
    for gamma in gamma_values:
        rho_decohered = dephasing_channel(rho, gamma)
        c_q_gamma = _von_neumann_entropy(rho_decohered)
        results.append((gamma, c_q_gamma))

    return results
