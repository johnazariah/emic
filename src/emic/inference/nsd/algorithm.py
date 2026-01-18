"""Neural State Discovery algorithm."""

from __future__ import annotations

import math
import random
from collections import defaultdict
from collections.abc import Hashable, Iterable
from dataclasses import dataclass
from typing import TYPE_CHECKING, Generic, TypeVar

from emic.inference.errors import InsufficientDataError
from emic.inference.result import InferenceResult
from emic.types import EpsilonMachine, EpsilonMachineBuilder

if TYPE_CHECKING:
    from emic.inference.nsd.config import NSDConfig

A = TypeVar("A", bound=Hashable)


@dataclass
class NSD(Generic[A]):
    """
    Neural State Discovery for epsilon-machine learning.

    NSD learns causal states by embedding histories into a vector space
    and clustering. This implementation uses a simplified approach without
    neural networks: it creates embeddings from next-symbol distributions
    and uses k-means clustering to discover states.

    Reference:
        This is a simplified version inspired by representation learning
        approaches to computational mechanics.

    Examples:
        >>> from emic.sources.synthetic.golden_mean import GoldenMeanSource
        >>> from emic.sources.transforms.take import TakeN
        >>> from emic.inference.nsd import NSD, NSDConfig
        >>>
        >>> source = GoldenMeanSource(p=0.5, _seed=42)
        >>> sequence = list(TakeN(5000)(source))
        >>>
        >>> nsd = NSD(NSDConfig(max_states=5))
        >>> result = nsd.infer(sequence)
        >>> len(result.machine.states) <= 5
        True
    """

    config: NSDConfig

    def infer(
        self,
        sequence: Iterable[A],
        alphabet: frozenset[A] | None = None,
    ) -> InferenceResult[A]:
        """
        Infer an epsilon-machine from the sequence using NSD.

        Args:
            sequence: Input sequence of symbols.
            alphabet: Set of possible symbols. Inferred from data if None.

        Returns:
            InferenceResult containing epsilon-machine and discovery info.

        Raises:
            InsufficientDataError: If sequence is too short.
        """
        symbols = list(sequence)
        n = len(symbols)

        min_required = self.config.history_length * 10
        if n < min_required:
            raise InsufficientDataError(
                required=min_required,
                provided=n,
                algorithm="NSD",
            )

        if alphabet is None:
            alphabet = frozenset(symbols)

        symbols_list = sorted(alphabet)  # type: ignore[type-var]
        n_symbols = len(symbols_list)
        sym_to_idx = {s: i for i, s in enumerate(symbols_list)}

        # Initialize RNG
        rng = random.Random(self.config.seed)

        # Build history embeddings based on predictive distributions
        histories, embeddings = self._build_embeddings(symbols, symbols_list, sym_to_idx, n_symbols)

        if len(histories) == 0:
            # Fallback for very short sequences
            machine = self._build_trivial_machine(alphabet, symbols_list)
            return InferenceResult(
                machine=machine,
                sequence_length=n,
                max_history_used=self.config.history_length,
                num_histories_considered=0,
            )

        # Find optimal number of states using gap statistic heuristic
        best_k = 1
        best_score = float("-inf")

        for k in range(1, min(self.config.max_states + 1, len(histories) + 1)):
            labels, _, inertia = self._kmeans(embeddings, k, rng)
            # Simplified model selection: prefer fewer states unless significantly better
            score = -inertia - 0.5 * k * math.log(len(histories))
            if score > best_score:
                best_score = score
                best_k = k

        # Run final clustering with best k
        labels, _, _ = self._kmeans(embeddings, best_k, rng)

        # Build machine from clustering
        machine = self._build_machine(
            symbols, histories, labels, symbols_list, sym_to_idx, best_k, alphabet
        )

        return InferenceResult(
            machine=machine,
            sequence_length=n,
            max_history_used=self.config.history_length,
            num_histories_considered=len(histories),
        )

    def _build_embeddings(
        self,
        sequence: list[A],
        symbols: list[A],
        sym_to_idx: dict[A, int],
        n_symbols: int,
    ) -> tuple[list[tuple[A, ...]], list[list[float]]]:
        """
        Build embeddings for each history based on predictive distribution.

        The embedding is the next-symbol probability distribution, which
        captures the predictive equivalence that defines causal states.
        """
        # Count next symbols for each history
        history_counts: dict[tuple[A, ...], dict[int, int]] = defaultdict(lambda: defaultdict(int))

        for i in range(self.config.history_length, len(sequence) - 1):
            history = tuple(sequence[i - self.config.history_length : i])
            next_sym = sequence[i]
            history_counts[history][sym_to_idx[next_sym]] += 1

        # Convert to probability distributions (embeddings)
        histories: list[tuple[A, ...]] = []
        embeddings: list[list[float]] = []

        for history, counts in history_counts.items():
            total = sum(counts.values())
            if total < 3:  # Skip rare histories
                continue

            # Create embedding as probability distribution
            embedding = [0.0] * n_symbols
            for sym_idx, count in counts.items():
                embedding[sym_idx] = count / total

            histories.append(history)
            embeddings.append(embedding)

        return histories, embeddings

    def _kmeans(
        self,
        embeddings: list[list[float]],
        k: int,
        rng: random.Random,
    ) -> tuple[list[int], list[list[float]], float]:
        """
        Run k-means clustering on embeddings.

        Returns labels, centroids, and inertia.
        """
        n = len(embeddings)
        dim = len(embeddings[0]) if embeddings else 0

        if n == 0 or k == 0:
            return [], [], 0.0

        # Initialize centroids randomly (k-means++)
        centroids: list[list[float]] = []
        available = list(range(n))

        # First centroid: random
        first_idx = rng.choice(available)
        centroids.append(embeddings[first_idx][:])
        available.remove(first_idx)

        # Remaining centroids: weighted by distance
        for _ in range(1, min(k, n)):
            if not available:
                break

            # Compute distances to nearest centroid
            distances = []
            for idx in available:
                min_dist = min(self._euclidean_distance(embeddings[idx], c) for c in centroids)
                distances.append(min_dist**2)

            # Sample proportional to distance squared
            total = sum(distances)
            if total == 0:
                next_idx = rng.choice(available)
            else:
                r = rng.random() * total
                cumsum = 0.0
                next_idx = available[-1]
                for i, d in enumerate(distances):
                    cumsum += d
                    if r <= cumsum:
                        next_idx = available[i]
                        break

            centroids.append(embeddings[next_idx][:])
            available.remove(next_idx)

        # Pad if needed
        while len(centroids) < k:
            centroids.append([0.0] * dim)

        # Run k-means iterations
        labels = [0] * n

        for iteration in range(self.config.n_iterations):
            # Assignment step
            new_labels = []
            for emb in embeddings:
                distances = [self._euclidean_distance(emb, c) for c in centroids]
                new_labels.append(min(range(k), key=lambda i: distances[i]))

            # Check convergence
            if new_labels == labels and iteration > 0:
                break

            labels = new_labels

            # Update step
            new_centroids: list[list[float]] = [[0.0] * dim for _ in range(k)]
            counts = [0] * k

            for i, label in enumerate(labels):
                counts[label] += 1
                for j in range(dim):
                    new_centroids[label][j] += embeddings[i][j]

            for c in range(k):
                if counts[c] > 0:
                    for j in range(dim):
                        new_centroids[c][j] /= counts[c]
                else:
                    new_centroids[c] = centroids[c]

            centroids = new_centroids

        # Compute inertia
        inertia = sum(
            self._euclidean_distance(embeddings[i], centroids[labels[i]]) ** 2 for i in range(n)
        )

        return labels, centroids, inertia

    def _euclidean_distance(self, a: list[float], b: list[float]) -> float:
        """Compute Euclidean distance between two vectors."""
        return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b, strict=True)))

    def _build_machine(
        self,
        sequence: list[A],
        histories: list[tuple[A, ...]],
        labels: list[int],
        symbols: list[A],
        sym_to_idx: dict[A, int],
        n_states: int,
        alphabet: frozenset[A],
    ) -> EpsilonMachine[A]:
        """Build epsilon-machine from clustered histories."""
        # Map histories to states
        history_to_state = {h: labels[i] for i, h in enumerate(histories)}

        # Count transitions
        trans_counts: dict[tuple[int, A], dict[int, int]] = defaultdict(lambda: defaultdict(int))

        for i in range(self.config.history_length, len(sequence) - 1):
            history = tuple(sequence[i - self.config.history_length : i])
            if history not in history_to_state:
                continue

            current_state = history_to_state[history]
            current_sym = sequence[i]

            # Find next history's state
            next_history = history[1:] + (current_sym,)
            if next_history in history_to_state:
                next_state = history_to_state[next_history]
                trans_counts[(current_state, current_sym)][next_state] += 1

        # Build machine using builder
        builder: EpsilonMachineBuilder[A] = EpsilonMachineBuilder()

        # Compute per-state symbol probabilities
        state_symbol_counts: dict[int, dict[A, int]] = defaultdict(lambda: defaultdict(int))
        for (from_s, sym), to_counts in trans_counts.items():
            state_symbol_counts[from_s][sym] += sum(to_counts.values())

        # Add transitions
        used_states: set[int] = set()
        for (from_s, sym), to_counts in trans_counts.items():
            from_id = f"S{from_s}"
            used_states.add(from_s)

            # Get most likely target
            if to_counts:
                to_s = max(to_counts.items(), key=lambda x: x[1])[0]
                to_id = f"S{to_s}"
                used_states.add(to_s)

                # Compute probability
                total = sum(state_symbol_counts[from_s].values())
                count = state_symbol_counts[from_s][sym]
                prob = count / total if total > 0 else 1.0 / len(symbols)

                builder.add_transition(from_id, sym, to_id, prob)

        # Ensure all states have all symbols
        if not used_states:
            used_states = {0}

        for state in used_states:
            state_id = f"S{state}"
            for sym in symbols:
                if (state, sym) not in trans_counts:
                    builder.add_transition(state_id, sym, state_id, 1.0 / len(symbols))

        # Set start state
        start_id = f"S{min(used_states)}"
        builder.with_start_state(start_id)

        return builder.build()

    def _build_trivial_machine(self, alphabet: frozenset[A], symbols: list[A]) -> EpsilonMachine[A]:
        """Build a trivial single-state machine for edge cases."""
        builder: EpsilonMachineBuilder[A] = EpsilonMachineBuilder()

        prob = 1.0 / len(symbols)
        for sym in symbols:
            builder.add_transition("S0", sym, "S0", prob)

        builder.with_start_state("S0")
        return builder.build()

    def __rrshift__(self, source: Iterable[A]) -> InferenceResult[A]:
        """Support: sequence >> NSD(config)."""
        alphabet = getattr(source, "alphabet", None)
        return self.infer(source, alphabet=alphabet)
