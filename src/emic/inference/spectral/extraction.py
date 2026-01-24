"""Epsilon-machine extraction from observable operators.

This module implements the conversion from learned observable operators
to an epsilon-machine (HMM with deterministic transitions on observations).

The extraction problem is non-trivial because observable operators live
in a learned coordinate system that may not correspond directly to the
true hidden states.

Approach:
    1. Compute b∞ (normalizer) and b₁ (initial state) vectors
    2. Use operators to compute P(symbol | state) via b∞
    3. Propagate belief states through the sequence to identify discrete states
    4. Map belief states to discrete states via clustering/quantization

Reference:
    Hsu, D., Kakade, S.M., & Zhang, T. (2012).
    "A Spectral Algorithm for Learning Hidden Markov Models"
    Journal of Computer and System Sciences, 78(5), 1460-1480.
"""

from __future__ import annotations

from collections.abc import Hashable
from typing import TYPE_CHECKING, TypeVar

import numpy as np

from emic.types import CausalState, EpsilonMachine, EpsilonMachineBuilder

if TYPE_CHECKING:
    from numpy.typing import NDArray

A = TypeVar("A", bound=Hashable)


def build_machine_from_operators(
    operators: dict[A, NDArray[np.float64]],
    alphabet: list[A],
    symbols: list[A],
) -> EpsilonMachine[A]:
    """
    Build epsilon-machine from observable operators using belief state clustering.

    This is the core extraction step that converts learned operators
    into a discrete-state machine.

    Approach:
        1. Compute initial belief b₁ and normalizer b∞
        2. Simulate belief state evolution through the sequence
        3. Cluster belief states to identify discrete states
        4. Build transitions from cluster dynamics

    The belief clustering approach is more robust than dimension-based
    extraction because it handles arbitrary coordinate rotations in the
    learned operator space.

    Args:
        operators: Dict mapping each symbol to its kxk observable operator.
        alphabet: List of all symbols.
        symbols: Original sequence (for belief simulation).

    Returns:
        Inferred epsilon-machine.
    """
    if not operators or not alphabet:
        return build_trivial_machine(symbols, frozenset(alphabet))

    ops_list = [operators[s] for s in alphabet]
    k = ops_list[0].shape[0]

    if k == 0:
        return build_trivial_machine(symbols, frozenset(alphabet))

    # Sum of operators gives the total state-to-state dynamics
    T: NDArray[np.float64] = np.sum(np.stack(ops_list), axis=0)

    # Compute b∞ for proper probability normalization
    b_inf = _compute_b_infinity(T, k)

    # Compute initial belief state
    b_init = _compute_initial_belief(T, k)

    # Simulate belief states through the sequence
    beliefs = _simulate_beliefs(operators, symbols, b_init, b_inf)

    if len(beliefs) < 10:
        # Not enough data for clustering - fall back to dimension-based
        return _build_from_dimensions(operators, alphabet, symbols, k, b_inf, T)

    # Cluster the belief states
    clusters, n_clusters = _cluster_beliefs_kmeans(beliefs, k)

    if n_clusters == 0:
        return _build_from_dimensions(operators, alphabet, symbols, k, b_inf, T)

    # Build machine from clusters
    return _build_from_clusters(alphabet, symbols, clusters, n_clusters)


def _simulate_beliefs(
    operators: dict[A, NDArray[np.float64]],
    symbols: list[A],
    b_init: NDArray[np.float64],
    b_inf: NDArray[np.float64],
) -> list[tuple[NDArray[np.float64], A, int]]:
    """
    Simulate belief state evolution through the sequence.

    Returns list of (belief_state, next_symbol, position) tuples.
    """
    k = len(b_init)
    beliefs: list[tuple[NDArray[np.float64], A, int]] = []

    b = b_init.copy()
    for i, sym in enumerate(symbols[:-1]):
        if sym not in operators:
            continue

        A_x = operators[sym]
        # Update belief: b' = A_x @ b / (b_inf @ A_x @ b)
        b_new = A_x @ b
        norm = float(np.dot(b_inf, b_new))
        b_new = b_new / norm if abs(norm) > 1e-10 else np.ones(k) / k

        beliefs.append((b.copy(), symbols[i + 1], i))
        b = b_new

    return beliefs


def _cluster_beliefs_kmeans(
    beliefs: list[tuple[NDArray[np.float64], A, int]],
    k: int,
    max_iter: int = 50,
) -> tuple[list[int], int]:
    """
    Cluster belief states using k-means with k clusters.

    We use the SVD rank k as the number of clusters, since that's
    the number of hidden states we expect.

    Args:
        beliefs: List of (belief_vector, next_symbol, position) tuples.
        k: Number of clusters (= number of hidden states).
        max_iter: Maximum k-means iterations.

    Returns:
        (cluster_assignments, n_clusters) tuple.
    """
    if not beliefs or k <= 0:
        return [], 0

    # Extract and normalize belief vectors (use direction, not magnitude)
    belief_vectors = []
    for b, _, _ in beliefs:
        norm = np.linalg.norm(b)
        if norm > 1e-10:
            belief_vectors.append(b / norm)
        else:
            belief_vectors.append(np.ones(len(b)) / np.sqrt(len(b)))

    X = np.array(belief_vectors)
    n_samples = len(X)

    if n_samples < k:
        # Not enough samples - each is its own cluster
        return list(range(n_samples)), n_samples

    # Initialize centroids using k-means++ style
    centroids = _init_centroids_plusplus(X, k)

    # Run k-means
    assignments = np.zeros(n_samples, dtype=int)

    for _ in range(max_iter):
        # Assign each point to nearest centroid (using cosine similarity)
        old_assignments = assignments.copy()
        for i, x in enumerate(X):
            similarities = [float(np.dot(x, c)) for c in centroids]
            assignments[i] = int(np.argmax(similarities))

        # Check convergence
        if np.array_equal(assignments, old_assignments):
            break

        # Update centroids
        for j in range(k):
            mask = assignments == j
            if np.sum(mask) > 0:
                new_centroid = np.mean(X[mask], axis=0)
                norm = np.linalg.norm(new_centroid)
                if norm > 1e-10:
                    centroids[j] = new_centroid / norm

    # Count actual clusters used
    unique_clusters = np.unique(assignments)
    n_clusters = len(unique_clusters)

    # Remap to contiguous indices
    cluster_map = {old: new for new, old in enumerate(unique_clusters)}
    remapped = [cluster_map[a] for a in assignments]

    return remapped, n_clusters


def _init_centroids_plusplus(
    X: NDArray[np.float64],
    k: int,
) -> list[NDArray[np.float64]]:
    """Initialize k centroids using k-means++ algorithm."""
    n_samples = len(X)
    rng = np.random.default_rng(42)  # Fixed seed for reproducibility

    # First centroid: random point
    centroids = [X[rng.integers(n_samples)].copy()]

    for _ in range(1, k):
        # Compute distance to nearest centroid for each point
        # Using 1 - cosine_similarity as distance
        distances = np.ones(n_samples)
        for i, x in enumerate(X):
            min_sim = max(float(np.dot(x, c)) for c in centroids)
            distances[i] = 1.0 - min_sim

        # Choose next centroid with probability proportional to distance^2
        probs = distances**2
        probs_sum = probs.sum()
        probs = probs / probs_sum if probs_sum > 1e-10 else np.ones(n_samples) / n_samples

        idx = rng.choice(n_samples, p=probs)
        centroids.append(X[idx].copy())

    return centroids


def _build_from_clusters(
    alphabet: list[A],
    symbols: list[A],
    clusters: list[int],
    n_clusters: int,
) -> EpsilonMachine[A]:
    """Build machine from clustered belief states."""
    # Count transitions between clusters
    trans_counts: dict[tuple[int, A, int], int] = {}
    state_counts: dict[int, int] = {}
    symbol_counts: dict[tuple[int, A], int] = {}

    for i, sym in enumerate(symbols[:-1]):
        if i >= len(clusters):
            break
        current = clusters[i]

        # Find next state
        next_cluster = clusters[i + 1] if i + 1 < len(clusters) else current

        key = (current, sym, next_cluster)
        trans_counts[key] = trans_counts.get(key, 0) + 1
        state_counts[current] = state_counts.get(current, 0) + 1
        symbol_counts[(current, sym)] = symbol_counts.get((current, sym), 0) + 1

    # Build machine - for each (state, symbol), pick the most common next state
    builder: EpsilonMachineBuilder[A] = EpsilonMachineBuilder()

    for state_id in range(n_clusters):
        state_name = f"S{state_id}"
        total = state_counts.get(state_id, 1)

        for sym in alphabet:
            # Find the most common next state for this (state, symbol)
            best_next = state_id
            best_count = 0
            sym_total = symbol_counts.get((state_id, sym), 0)

            for next_id in range(n_clusters):
                count = trans_counts.get((state_id, sym, next_id), 0)
                if count > best_count:
                    best_count = count
                    best_next = next_id

            if sym_total > 0:
                prob = sym_total / total
                target = f"S{best_next}"
                builder.add_transition(state_name, sym, target, prob)

    # Start state is most common
    if state_counts:
        start_id = max(state_counts, key=lambda x: state_counts[x])
        builder.with_start_state(f"S{start_id}")

    machine = builder.build()
    return merge_similar_states(machine, alphabet)


def _build_from_dimensions(
    operators: dict[A, NDArray[np.float64]],
    alphabet: list[A],
    _symbols: list[A],
    k: int,
    b_inf: NDArray[np.float64],
    T: NDArray[np.float64],
) -> EpsilonMachine[A]:
    """Original dimension-based approach as fallback."""
    builder: EpsilonMachineBuilder[A] = EpsilonMachineBuilder()

    for i in range(k):
        state_name = f"S{i}"
        emissions: dict[A, float] = {}
        next_states: dict[A, int] = {}

        for symbol in alphabet:
            A_x = operators[symbol]
            result = A_x[i, :]

            emission_weight = float(np.dot(b_inf, result))
            emissions[symbol] = max(0.0, abs(emission_weight))

            if np.max(np.abs(result)) > 1e-10:
                weighted = np.abs(result) * b_inf
                next_states[symbol] = int(np.argmax(weighted))
            else:
                next_states[symbol] = i

        total = sum(emissions.values())
        if total < 1e-10:
            for symbol in alphabet:
                emissions[symbol] = 1.0 / len(alphabet)
            total = 1.0

        for symbol in alphabet:
            prob = emissions[symbol] / total
            if prob > 1e-6:
                target = f"S{next_states[symbol]}"
                builder.add_transition(state_name, symbol, target, prob)

    stationary = _compute_initial_belief(T, k)
    start_idx = int(np.argmax(stationary))
    builder.with_start_state(f"S{start_idx}")

    machine = builder.build()
    return merge_similar_states(machine, alphabet)


def _compute_b_infinity(T: NDArray[np.float64], k: int) -> NDArray[np.float64]:
    """
    Compute b∞ (normalizer vector) for probability computation.

    b∞ is the left eigenvector of T corresponding to eigenvalue 1.
    For properly learned operators, b∞ᵀ A_x b gives P(x | b).

    Special case: if T ≈ identity (e.g., periodic processes where each
    symbol acts as a projector), use uniform b∞.
    """
    # Check if T is approximately identity or diagonal
    if k > 1:
        off_diag = np.abs(T - np.diag(np.diag(T))).max()
        if off_diag < 0.01:
            # T is approximately diagonal - use uniform b_inf
            return np.ones(k) / k

    try:
        eigenvalues, eigenvectors = np.linalg.eig(T.T)
        idx = np.argmin(np.abs(eigenvalues - 1.0))
        b_inf = np.real(eigenvectors[:, idx])
        # Normalize to sum to 1
        b_inf = b_inf / (np.sum(np.abs(b_inf)) + 1e-10)
        return np.abs(b_inf)
    except np.linalg.LinAlgError:
        return np.ones(k) / k


def _compute_initial_belief(T: NDArray[np.float64], k: int) -> NDArray[np.float64]:
    """
    Compute initial belief state b₁.

    Uses the right eigenvector of T (stationary distribution over states).
    """
    try:
        eigenvalues, eigenvectors = np.linalg.eig(T)
        idx = np.argmin(np.abs(eigenvalues - 1.0))
        b_1 = np.real(eigenvectors[:, idx])
        b_1 = np.abs(b_1)
        b_1 = b_1 / (np.sum(b_1) + 1e-10)
        return b_1
    except np.linalg.LinAlgError:
        return np.ones(k) / k


def merge_similar_states(
    machine: EpsilonMachine[A],
    alphabet: list[A],
) -> EpsilonMachine[A]:
    """
    Merge states with nearly identical emission/transition distributions.

    This reduces over-splitting by combining states that behave identically.
    Uses iterative refinement to handle target remapping.

    Args:
        machine: Input epsilon-machine (possibly with too many states).
        alphabet: List of all symbols.

    Returns:
        Epsilon-machine with similar states merged.
    """
    current = machine
    max_iterations = 10

    for _ in range(max_iterations):
        merged = _merge_pass(current, alphabet)
        if len(merged.states) == len(current.states):
            break  # No more merging possible
        current = merged

    return current


def _merge_pass(
    machine: EpsilonMachine[A],
    alphabet: list[A],
) -> EpsilonMachine[A]:
    """Single pass of state merging."""
    states = list(machine.states)
    n_states = len(states)

    if n_states <= 1:
        return machine

    # Build lookup from state_id to CausalState
    state_lookup: dict[str, CausalState[A]] = {s.id: s for s in states}

    def state_signature(state_id: str) -> tuple[tuple[float, ...], tuple[str, ...]]:
        """
        Get full signature: (emission_probs, transition_targets).

        Two states are similar only if they have similar emissions AND
        transition to the same targets.
        """
        state = state_lookup.get(state_id)
        if state is None:
            return ((), ())

        emissions: list[float] = []
        targets: list[str] = []
        trans_by_symbol: dict[A, tuple[float, str]] = {}

        for t in state.transitions:
            # If multiple transitions for same symbol, take highest prob
            existing = trans_by_symbol.get(t.symbol)
            if existing is None or t.probability > existing[0]:
                trans_by_symbol[t.symbol] = (t.probability, t.target)

        for symbol in sorted(alphabet, key=str):
            if symbol in trans_by_symbol:
                prob, target = trans_by_symbol[symbol]
                emissions.append(prob)
                targets.append(target)
            else:
                emissions.append(0.0)
                targets.append("")

        return (tuple(emissions), tuple(targets))

    def signatures_similar(
        sig1: tuple[tuple[float, ...], tuple[str, ...]],
        sig2: tuple[tuple[float, ...], tuple[str, ...]],
    ) -> bool:
        """Check if two signatures are similar: emissions close AND same targets."""
        em1, tgt1 = sig1
        em2, tgt2 = sig2

        if len(em1) != len(em2):
            return False

        # Check emissions are similar (25% total variation)
        diff = sum(abs(e1 - e2) for e1, e2 in zip(em1, em2, strict=True))
        if diff >= 0.25:
            return False

        # Check targets are the same (for non-zero probability transitions)
        for i in range(len(em1)):
            # Only compare targets if both have significant probability
            if em1[i] > 0.05 and em2[i] > 0.05 and tgt1[i] != tgt2[i]:
                return False

        return True

    # Group states by similar signatures
    state_ids = [s.id for s in states]
    state_groups: dict[int, list[str]] = {}
    state_to_group: dict[str, int] = {}
    group_id = 0

    for state_id in state_ids:
        sig = state_signature(state_id)
        found_group = False

        for gid, group_states in state_groups.items():
            rep_sig = state_signature(group_states[0])
            if signatures_similar(sig, rep_sig):
                state_groups[gid].append(state_id)
                state_to_group[state_id] = gid
                found_group = True
                break

        if not found_group:
            state_groups[group_id] = [state_id]
            state_to_group[state_id] = group_id
            group_id += 1

    # If no merging possible, return original
    if len(state_groups) == n_states:
        return machine

    # Build merged machine
    builder: EpsilonMachineBuilder[A] = EpsilonMachineBuilder()

    # Map groups to new state names
    group_rep: dict[int, str] = {gid: f"S{gid}" for gid in state_groups}

    # For each group, compute average emission probabilities and transition targets
    for gid, group_states in state_groups.items():
        new_state = group_rep[gid]

        # Average emissions across all states in group
        emission_totals: dict[A, float] = dict.fromkeys(alphabet, 0.0)
        target_votes: dict[A, dict[int, int]] = {s: {} for s in alphabet}

        for sid in group_states:
            state = state_lookup.get(sid)
            if state is None:
                continue
            for t in state.transitions:
                emission_totals[t.symbol] += t.probability
                target_group = state_to_group.get(t.target, 0)
                target_votes[t.symbol][target_group] = (
                    target_votes[t.symbol].get(target_group, 0) + 1
                )

        n_group = len(group_states)
        for symbol in alphabet:
            avg_prob = emission_totals[symbol] / n_group if n_group > 0 else 0.0
            if avg_prob > 1e-6:
                # Most common target group for this symbol
                if target_votes[symbol]:
                    best_target_group = max(target_votes[symbol].items(), key=lambda x: x[1])[0]
                else:
                    best_target_group = gid
                target_state = group_rep.get(best_target_group, new_state)
                builder.add_transition(new_state, symbol, target_state, avg_prob)

    # Set start state
    if machine.start_state:
        start_group = state_to_group.get(machine.start_state, 0)
        builder.with_start_state(group_rep.get(start_group, "S0"))
    else:
        builder.with_start_state("S0")

    return builder.build()


def build_trivial_machine(
    symbols: list[A],
    alphabet: frozenset[A],
) -> EpsilonMachine[A]:
    """Build a single-state machine when spectral decomposition fails."""
    builder: EpsilonMachineBuilder[A] = EpsilonMachineBuilder()

    # Count symbol frequencies
    counts: dict[A, int] = {}
    for s in symbols:
        counts[s] = counts.get(s, 0) + 1

    total = len(symbols) if symbols else 1

    # Add self-loop transitions with empirical probabilities
    for symbol in alphabet:
        prob = counts.get(symbol, 0) / total
        if prob > 0:
            builder.add_transition("S0", symbol, "S0", prob)

    # If no transitions added, use uniform
    if not counts:
        for symbol in alphabet:
            builder.add_transition("S0", symbol, "S0", 1.0 / len(alphabet))

    builder.with_start_state("S0")
    return builder.build()
