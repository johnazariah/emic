"""Perturbed Coin Process source.

The Perturbed Coin is a canonical example in quantum computational mechanics,
used extensively in Gu et al. (2012) "Quantum Models of Classical World" to
demonstrate quantum memory advantage.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from emic.sources.base import StochasticSource

if TYPE_CHECKING:
    from collections.abc import Iterator

    from emic.types import EpsilonMachine


@dataclass
class PerturbedCoinSource(StochasticSource[int]):
    """
    The Perturbed Coin Process.

    A coin with persistent bias. The coin tends to repeat its last observation,
    but occasionally "flips" with probability p.

    State machine:
        S0 (last saw 0): emit 0 with prob (1-p), emit 1 with prob p
        S1 (last saw 1): emit 1 with prob (1-p), emit 0 with prob p

    Transitions:
        S0 --0:(1-p)--> S0
        S0 --1:p--> S1
        S1 --1:(1-p)--> S1
        S1 --0:p--> S0

    Parameters:
        p: Probability of flipping (changing state). Default: 0.3
           - p = 0: deterministic (always repeat)
           - p = 0.5: fair coin (IID, no memory)
           - p → 0.5: maximum quantum advantage

    Statistical properties (exact formulas):
        - Stationary: pi_0 = pi_1 = 0.5 (symmetric)
        - Statistical complexity: C_mu = 1 bit (always, for p != 0.5)
        - Entropy rate: h_mu = H_s(p) where H_s is binary entropy
        - Excess entropy: E = 1 - H_s(p)
        - Crypticity: chi = H_s(p)

    Quantum properties:
        - Signal states: |s_0> = sqrt(1-p)|00> + sqrt(p)|11>
                         |s_1> = sqrt(p)|00> + sqrt(1-p)|11>
        - Overlap: <s_0|s_1> = 2*sqrt(p(1-p))
        - Quantum complexity: C_q = H_vn(rho) where rho is the mixed state
        - Quantum advantage: Delta_q = C_mu - C_q

    References:
        - Gu et al. (2012) "Quantum mechanics can reduce the complexity of
          classical models" Nature Communications 3:762
        - Garner et al. (2017) "Provably unbounded memory advantage in
          stochastic simulation using quantum mechanics"

    Examples:
        >>> source = PerturbedCoinSource(p=0.3, _seed=42)
        >>> it = iter(source)
        >>> symbols = [next(it) for _ in range(100)]
        >>> set(symbols) == {0, 1}
        True

        >>> # Symmetric: roughly equal 0s and 1s
        >>> 0.3 < symbols.count(1) / len(symbols) < 0.7
        True
    """

    p: float = 0.3
    _alphabet: frozenset[int] = field(default_factory=lambda: frozenset({0, 1}))

    def __post_init__(self) -> None:
        """Validate parameters and initialize RNG."""
        super().__post_init__()
        if not (0 < self.p < 1):
            msg = f"p must be in (0, 1), got {self.p}"
            raise ValueError(msg)

    def __iter__(self) -> Iterator[int]:
        """
        Generate symbols from the Perturbed Coin process.

        Yields:
            Symbols from {0, 1}.
        """
        # Start in random state based on stationary distribution
        state = 0 if self._rng.random() < 0.5 else 1

        while True:
            if self._rng.random() < self.p:
                # Flip: emit opposite of current state, change state
                yield 1 - state
                state = 1 - state
            else:
                # Stay: emit same as current state, stay in state
                yield state

    def with_seed(self, seed: int) -> PerturbedCoinSource:
        """
        Return a new source with the given seed.

        Args:
            seed: The random seed to use.

        Returns:
            A new PerturbedCoinSource with the given seed.
        """
        return PerturbedCoinSource(p=self.p, _seed=seed)

    @property
    def true_machine(self) -> EpsilonMachine[int]:
        """
        Return the known epsilon-machine for this process.

        The Perturbed Coin has exactly 2 causal states, both equally likely.

        Returns:
            The epsilon-machine that generates this process.
        """
        from emic.types import EpsilonMachineBuilder

        return (
            EpsilonMachineBuilder[int]()
            .add_transition("S0", 0, "S0", 1.0 - self.p)
            .add_transition("S0", 1, "S1", self.p)
            .add_transition("S1", 1, "S1", 1.0 - self.p)
            .add_transition("S1", 0, "S0", self.p)
            .with_start_state("S0")
            .with_stationary_distribution({"S0": 0.5, "S1": 0.5})
            .build()
        )
