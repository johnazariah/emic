"""Noise transforms for testing algorithm robustness."""

from __future__ import annotations

import random
from collections.abc import Hashable, Iterator
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Generic, TypeVar

if TYPE_CHECKING:
    from emic.sources.protocol import SequenceSource

A = TypeVar("A", bound=Hashable)


@dataclass(frozen=True)
class BitFlipNoise(Generic[A]):
    """
    Apply bit-flip (binary symmetric channel) noise to a source.

    Each symbol is independently replaced with a random symbol from the
    alphabet with probability `flip_prob`. This models observation noise
    where the true underlying symbol is corrupted before being observed.

    Parameters:
        flip_prob: Probability of flipping each symbol (0 to 0.5)
        seed: Random seed for reproducibility

    Examples:
        >>> from emic.sources import GoldenMeanSource
        >>> from emic.sources.transforms import BitFlipNoise, TakeN
        >>> source = GoldenMeanSource(p=0.5, _seed=42)
        >>> # Add 5% observation noise
        >>> noisy = BitFlipNoise[int](flip_prob=0.05, seed=123)(source)
        >>> data = TakeN[int](1000)(noisy)

    Note:
        For binary alphabets, flip_prob=0.5 produces random noise
        independent of the input. For larger alphabets, flipped symbols
        are drawn uniformly at random from the alphabet.
    """

    flip_prob: float
    seed: int | None = None

    def __post_init__(self) -> None:
        """Validate flip probability."""
        if not 0 <= self.flip_prob <= 0.5:
            raise ValueError(f"flip_prob must be in [0, 0.5], got {self.flip_prob}")

    def __call__(self, source: SequenceSource[A]) -> _NoisySource[A]:
        """
        Apply the noise transform to a source.

        Args:
            source: The source to add noise to.

        Returns:
            A new source with observation noise applied.
        """
        return _NoisySource(source, self.flip_prob, self.seed)


@dataclass
class _NoisySource(Generic[A]):
    """Internal wrapper that adds noise to a source."""

    _source: SequenceSource[A]
    _flip_prob: float
    _seed: int | None = None
    _rng: random.Random = field(init=False, repr=False)
    _alphabet_list: list[A] = field(init=False, repr=False)

    def __post_init__(self) -> None:
        """Initialize RNG and cache alphabet."""
        self._rng = random.Random(self._seed)
        # Cache alphabet as list for random selection
        self._alphabet_list = list(self._source.alphabet)

    @property
    def alphabet(self) -> frozenset[A]:
        """The alphabet of the underlying source."""
        return self._source.alphabet

    def __iter__(self) -> Iterator[A]:
        """Iterate with noise applied to each symbol."""
        for symbol in self._source:
            if self._rng.random() < self._flip_prob:
                # Flip to a random symbol from alphabet
                yield self._rng.choice(self._alphabet_list)
            else:
                yield symbol

    def __rshift__(self, transform: object) -> object:
        """Pipeline operator for composing with transforms."""
        if callable(transform):
            return transform(self)
        return NotImplemented
