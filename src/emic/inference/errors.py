"""Inference error types."""

from __future__ import annotations


class InferenceError(Exception):
    """Base class for inference errors."""

    def explain(self) -> str:
        """Return a human-readable explanation."""
        return str(self)


class InsufficientDataError(InferenceError):
    """Raised when sequence is too short for reliable inference."""

    def __init__(
        self,
        required: int,
        provided: int,
        algorithm: str = "unknown",
    ) -> None:
        super().__init__(
            f"Insufficient data for {algorithm}: " f"need {required} symbols, got {provided}"
        )
        self.required = required
        self.provided = provided
        self.algorithm = algorithm

    def explain(self) -> str:
        """Return a human-readable explanation."""
        return (
            f"The sequence you provided has {self.provided} symbols, "
            f"but the {self.algorithm} algorithm needs at least {self.required} "
            f"to produce reliable results. Try:\n"
            f"  • Using a longer sequence\n"
            f"  • Reducing max_history parameter\n"
            f"  • Reducing min_count parameter (less reliable)"
        )


class NonConvergenceError(InferenceError):
    """Raised when algorithm fails to converge."""

    def __init__(self, iterations: int, tolerance: float) -> None:
        super().__init__(f"Algorithm did not converge after {iterations} iterations")
        self.iterations = iterations
        self.tolerance = tolerance

    def explain(self) -> str:
        """Return a human-readable explanation."""
        return (
            f"The algorithm did not stabilize after {self.iterations} iterations. "
            f"This might indicate:\n"
            f"  • The process has complex structure requiring more iterations\n"
            f"  • The significance level ({self.tolerance}) is too sensitive\n"
            f"  • The data contains anomalies\n"
            f"Try increasing max_iterations or significance level."
        )
