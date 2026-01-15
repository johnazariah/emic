"""Pipeline utilities and helpers."""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

if TYPE_CHECKING:
    from collections.abc import Callable

T = TypeVar("T")


def tap(func: Callable[[T], object]) -> Callable[[T], T]:
    """Create a tap function for pipeline debugging.

    A tap function applies a side effect (like printing) to the
    value flowing through the pipeline, then returns the value unchanged.
    Useful for debugging intermediate pipeline stages.

    Args:
        func: A function to apply to the value. Return value is ignored.

    Returns:
        A function that applies func and returns its input unchanged.

    Example:
        >>> from emic.sources import GoldenMeanSource
        >>> from emic.sources.transforms import TakeN
        >>> from emic.pipeline import tap
        >>> result = (
        ...     GoldenMeanSource(p=0.5, _seed=42)
        ...     >> tap(lambda s: print(f"Source alphabet: {s.alphabet}"))
        ...     >> TakeN(100)
        ...     >> tap(lambda d: print(f"Took {len(d)} symbols"))
        ... )  # doctest: +SKIP
    """

    def _tap(value: T) -> T:
        func(value)
        return value

    return _tap


def identity(value: T) -> T:
    """Identity function - returns input unchanged.

    Useful as a placeholder in pipeline construction.

    Args:
        value: Any value.

    Returns:
        The same value unchanged.

    Example:
        >>> from emic.pipeline import identity
        >>> identity(42)
        42
    """
    return value


class Pipeline:
    """A composable pipeline builder.

    An alternative to the `>>` operator for programmatic pipeline construction.

    Example:
        >>> from emic.pipeline import Pipeline
        >>> from emic.sources import GoldenMeanSource
        >>> from emic.sources.transforms import TakeN
        >>> from emic.inference import CSSR, CSSRConfig
        >>> pipeline = (
        ...     Pipeline()
        ...     .then(lambda: GoldenMeanSource(p=0.5, _seed=42))
        ...     .then(TakeN(100))
        ... )  # doctest: +SKIP
    """

    def __init__(self) -> None:
        """Create an empty pipeline."""
        self._stages: list[Callable[..., object]] = []

    def then(self, func: Callable[..., object]) -> Pipeline:
        """Add a stage to the pipeline.

        Args:
            func: The function to add.

        Returns:
            Self for chaining.
        """
        self._stages.append(func)
        return self

    def run(self, initial: object = None) -> object:
        """Execute the pipeline.

        Args:
            initial: The initial value (or None to call first stage with no args).

        Returns:
            The final result of the pipeline.
        """
        if not self._stages:
            return initial

        # First stage may be a nullary function (source creator)
        result = self._stages[0]() if initial is None else self._stages[0](initial)

        for stage in self._stages[1:]:
            result = stage(result)

        return result
