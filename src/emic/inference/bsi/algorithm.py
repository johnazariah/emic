"""Bayesian Structural Inference algorithm."""

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
    from emic.inference.bsi.config import BSIConfig

A = TypeVar("A", bound=Hashable)


@dataclass
class BSI(Generic[A]):
    """
    Bayesian Structural Inference for epsilon-machine learning.

    BSI uses Bayesian inference with Gibbs sampling to learn epsilon-machines.
    It provides uncertainty quantification and automatic model selection via
    marginal likelihood (evidence).

    The algorithm places Dirichlet priors on transition probabilities and
    uses Gibbs sampling to explore the posterior over state assignments.

    Implements the InferenceAlgorithm protocol.

    Reference:
        Strelioff, C.C. & Crutchfield, J.P. (2014).
        "Bayesian Structural Inference for Hidden Processes"

    Examples:
        >>> from emic.sources.synthetic.golden_mean import GoldenMeanSource
        >>> from emic.sources.transforms.take import TakeN
        >>> from emic.inference.bsi import BSI, BSIConfig
        >>>
        >>> source = GoldenMeanSource(p=0.5, _seed=42)
        >>> sequence = list(TakeN(5000)(source))
        >>>
        >>> bsi = BSI(BSIConfig(max_states=5, n_samples=100))
        >>> result = bsi.infer(sequence)
        >>> len(result.machine.states) <= 5
        True
    """

    config: BSIConfig

    def infer(
        self,
        sequence: Iterable[A],
        alphabet: frozenset[A] | None = None,
    ) -> InferenceResult[A]:
        """
        Infer an epsilon-machine from the sequence using BSI.

        Args:
            sequence: Input sequence of symbols.
            alphabet: Set of possible symbols. Inferred from data if None.

        Returns:
            InferenceResult containing epsilon-machine and diagnostics.

        Raises:
            InsufficientDataError: If sequence is too short.
        """
        symbols = list(sequence)
        n = len(symbols)

        min_required = self.config.max_history * 10
        if n < min_required:
            raise InsufficientDataError(
                required=min_required,
                provided=n,
                algorithm="BSI",
            )

        if alphabet is None:
            alphabet = frozenset(symbols)

        # Initialize RNG
        rng = random.Random(self.config.seed)

        # Build suffix tree for counting
        suffix_counts = self._build_suffix_counts(symbols)

        # Try different numbers of states, compute evidence
        best_machine: EpsilonMachine[A] | None = None
        best_evidence = float("-inf")

        for n_states in range(1, self.config.max_states + 1):
            machine, evidence = self._infer_with_n_states(
                symbols, alphabet, suffix_counts, n_states, rng
            )
            if evidence > best_evidence:
                best_evidence = evidence
                best_machine = machine

        assert best_machine is not None

        return InferenceResult(
            machine=best_machine,
            sequence_length=n,
            max_history_used=self.config.max_history,
            num_histories_considered=len(suffix_counts),
        )

    def _build_suffix_counts(self, sequence: list[A]) -> dict[tuple[A, ...], dict[A, int]]:
        """Build counts of next symbols given history suffixes."""
        counts: dict[tuple[A, ...], dict[A, int]] = defaultdict(lambda: defaultdict(int))

        for i in range(len(sequence) - 1):
            for length in range(min(i + 1, self.config.max_history) + 1):
                if length == 0:
                    history: tuple[A, ...] = ()
                else:
                    history = tuple(sequence[i - length + 1 : i + 1])
                next_sym = sequence[i + 1]
                counts[history][next_sym] += 1

        return dict(counts)

    def _infer_with_n_states(
        self,
        sequence: list[A],
        alphabet: frozenset[A],
        suffix_counts: dict[tuple[A, ...], dict[A, int]],
        n_states: int,
        rng: random.Random,
    ) -> tuple[EpsilonMachine[A], float]:
        """
        Run MCMC inference with a fixed number of states.

        Returns the MAP machine and log evidence estimate.
        """
        symbols = sorted(alphabet)  # type: ignore[type-var]
        n_symbols = len(symbols)

        # Initialize: random state assignments for histories
        histories = list(suffix_counts.keys())
        state_assignments = {h: rng.randint(0, n_states - 1) for h in histories}

        # Track best configuration
        best_log_posterior = float("-inf")
        best_trans_counts: dict[tuple[int, A], dict[int, int]] = defaultdict(
            lambda: defaultdict(int)
        )

        # MCMC sampling
        total_samples = self.config.burnin + self.config.n_samples * self.config.thin

        for iteration in range(total_samples):
            # Gibbs sweep: update each history's state assignment
            for history in histories:
                if len(history) == 0:
                    continue

                # Compute conditional probabilities for each state
                log_probs = []
                for state in range(n_states):
                    log_prob = self._compute_log_conditional(
                        history,
                        state,
                        state_assignments,
                        suffix_counts,
                        n_states,
                        n_symbols,
                    )
                    log_probs.append(log_prob)

                # Sample from categorical
                state_assignments[history] = self._sample_categorical(log_probs, rng)

            # After burn-in, check if this is best
            if iteration >= self.config.burnin:
                log_post = self._compute_log_posterior(
                    state_assignments, suffix_counts, n_states, n_symbols
                )
                if log_post > best_log_posterior:
                    best_log_posterior = log_post
                    best_trans_counts = self._extract_transition_counts(
                        state_assignments, suffix_counts, symbols, n_states
                    )

        # Build machine from best configuration
        machine = self._build_machine(best_trans_counts, n_states, symbols, alphabet)

        # Estimate log evidence using BIC approximation
        n_params = n_states * n_symbols * 2  # transitions + emissions
        n_data = len(sequence)
        log_evidence = best_log_posterior - 0.5 * n_params * math.log(n_data)

        return machine, log_evidence

    def _compute_log_conditional(
        self,
        history: tuple[A, ...],
        state: int,
        state_assignments: dict[tuple[A, ...], int],
        suffix_counts: dict[tuple[A, ...], dict[A, int]],
        n_states: int,
        n_symbols: int,
    ) -> float:
        """Compute log conditional probability of assigning history to state."""
        # Count how many histories are in each state
        state_counts = [0] * n_states
        for h, s in state_assignments.items():
            if h != history:
                state_counts[s] += 1
        state_counts[state] += 1  # Include this assignment

        # Prior term: encourage states to be used evenly
        log_prior = math.log(state_counts[state] + self.config.alpha_prior)

        # Likelihood term: how well does this state predict emissions?
        next_counts = suffix_counts.get(history, {})
        total = sum(next_counts.values())
        if total == 0:
            return log_prior

        # Aggregate emission counts for this state
        emission_counts: dict[A, int] = defaultdict(int)
        for h, s in state_assignments.items():
            if s == state and h != history:
                for sym, count in suffix_counts.get(h, {}).items():
                    emission_counts[sym] += count
        for sym, count in next_counts.items():
            emission_counts[sym] += count

        # Compute log likelihood with Dirichlet-multinomial
        total_emission = sum(emission_counts.values())
        log_lik = 0.0
        for sym, count in next_counts.items():
            expected = (emission_counts[sym] + self.config.alpha_prior) / (
                total_emission + n_symbols * self.config.alpha_prior
            )
            log_lik += count * math.log(max(expected, 1e-10))

        return log_prior + log_lik

    def _sample_categorical(self, log_probs: list[float], rng: random.Random) -> int:
        """Sample from categorical distribution given log probabilities."""
        # Normalize in log space
        max_log = max(log_probs)
        probs = [math.exp(lp - max_log) for lp in log_probs]
        total = sum(probs)
        probs = [p / total for p in probs]

        # Sample
        r = rng.random()
        cumsum = 0.0
        for i, p in enumerate(probs):
            cumsum += p
            if r <= cumsum:
                return i
        return len(probs) - 1

    def _compute_log_posterior(
        self,
        state_assignments: dict[tuple[A, ...], int],
        suffix_counts: dict[tuple[A, ...], dict[A, int]],
        n_states: int,
        n_symbols: int,
    ) -> float:
        """Compute log posterior of current state assignments."""
        # Count emissions per state
        state_emission_counts: list[dict[A, int]] = [defaultdict(int) for _ in range(n_states)]

        for history, state in state_assignments.items():
            for sym, count in suffix_counts.get(history, {}).items():
                state_emission_counts[state][sym] += count

        # Log likelihood with Dirichlet prior
        log_post = 0.0
        for state in range(n_states):
            counts = state_emission_counts[state]
            total = sum(counts.values())
            if total == 0:
                continue

            for _sym, count in counts.items():
                prob = (count + self.config.alpha_prior) / (
                    total + n_symbols * self.config.alpha_prior
                )
                log_post += count * math.log(max(prob, 1e-10))

        return log_post

    def _extract_transition_counts(
        self,
        state_assignments: dict[tuple[A, ...], int],
        suffix_counts: dict[tuple[A, ...], dict[A, int]],
        _symbols: list[A],
        _n_states: int,
    ) -> dict[tuple[int, A], dict[int, int]]:
        """Extract transition counts from state assignments."""
        transitions: dict[tuple[int, A], dict[int, int]] = defaultdict(lambda: defaultdict(int))

        for history, state in state_assignments.items():
            for sym, count in suffix_counts.get(history, {}).items():
                # Infer transition: history + sym -> next_history's state
                next_history = (*history[1:], sym) if history else (sym,)

                # Find best matching history for transition
                for h_len in range(len(next_history), 0, -1):
                    suffix = next_history[-h_len:]
                    if suffix in state_assignments:
                        to_state = state_assignments[suffix]
                        transitions[(state, sym)][to_state] += count
                        break
                else:
                    # Fallback to empty history state
                    if () in state_assignments:
                        to_state = state_assignments[()]
                        transitions[(state, sym)][to_state] += count

        return dict(transitions)

    def _build_machine(
        self,
        trans_counts: dict[tuple[int, A], dict[int, int]],
        _n_states: int,
        symbols: list[A],
        _alphabet: frozenset[A],
    ) -> EpsilonMachine[A]:
        """Build epsilon-machine from transition counts."""
        builder: EpsilonMachineBuilder[A] = EpsilonMachineBuilder()

        # Find which states are actually used
        used_states: set[int] = set()
        for (from_s, _), to_counts in trans_counts.items():
            used_states.add(from_s)
            for to_s in to_counts:
                used_states.add(to_s)

        if not used_states:
            used_states = {0}

        # Map to state IDs
        state_map = {old: f"S{new}" for new, old in enumerate(sorted(used_states))}

        # Compute per-state symbol probabilities
        state_symbol_counts: dict[int, dict[A, int]] = defaultdict(lambda: defaultdict(int))
        for (from_s, sym), to_counts in trans_counts.items():
            state_symbol_counts[from_s][sym] += sum(to_counts.values())

        # Add transitions
        for (from_s, sym), to_counts in trans_counts.items():
            if from_s not in state_map:
                continue

            from_id = state_map[from_s]

            # Get most likely target
            if to_counts:
                to_s = max(to_counts.items(), key=lambda x: x[1])[0]
                if to_s not in state_map:
                    continue
                to_id = state_map[to_s]

                # Compute probability
                total = sum(state_symbol_counts[from_s].values())
                count = state_symbol_counts[from_s][sym]
                prob = count / total if total > 0 else 1.0 / len(symbols)

                builder.add_transition(from_id, sym, to_id, prob)

        # Ensure all states have all symbols
        for old_s in used_states:
            state_id = state_map[old_s]
            for sym in symbols:
                if (old_s, sym) not in trans_counts:
                    builder.add_transition(state_id, sym, state_id, 1.0 / len(symbols))

        # Set start state
        start_id = state_map[min(used_states)]
        builder.with_start_state(start_id)

        return builder.build()

    def __rrshift__(self, source: Iterable[A]) -> InferenceResult[A]:
        """Support: sequence >> BSI(config)."""
        alphabet = getattr(source, "alphabet", None)
        return self.infer(source, alphabet=alphabet)
