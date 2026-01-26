#!/usr/bin/env python3
"""Quick benchmark to validate CSSR correctness.

Tests the key benchmarks from Shalizi (2004):
- Even Process: should get 2 states
- Golden Mean: should get 2 states
- Biased Coin: should get 1 state

Runs quickly (< 1 minute) for immediate feedback.
"""

from __future__ import annotations

import sys
import time
from dataclasses import dataclass
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from emic.inference.csm import CSM, CSMConfig
from emic.inference.cssr import CSSR, CSSRConfig
from emic.inference.spectral import Spectral, SpectralConfig
from emic.sources.synthetic.biased_coin import BiasedCoinSource
from emic.sources.synthetic.even_process import EvenProcessSource
from emic.sources.synthetic.golden_mean import GoldenMeanSource


@dataclass
class Result:
    algorithm: str
    process: str
    sample_size: int
    expected_states: int
    actual_states: int
    correct: bool
    runtime_ms: float


def run_test(
    algo_name: str,
    algo,
    process_name: str,
    source,
    sample_size: int,
    expected_states: int,
    _seed: int = 42,
) -> Result:
    """Run a single test."""
    from itertools import islice

    data = list(islice(source, sample_size))
    alphabet = set(data)

    start = time.perf_counter()
    result = algo.infer(data, alphabet=alphabet)
    elapsed = (time.perf_counter() - start) * 1000

    actual = len(result.machine.states)

    return Result(
        algorithm=algo_name,
        process=process_name,
        sample_size=sample_size,
        expected_states=expected_states,
        actual_states=actual,
        correct=actual == expected_states,
        runtime_ms=elapsed,
    )


def main():
    print("=" * 70)
    print("Quick CSSR Correctness Benchmark")
    print("=" * 70)
    print()

    # Test configurations matching Shalizi (2004)
    tests = [
        ("Even Process", EvenProcessSource(p=0.5, _seed=42), 2),
        ("Golden Mean", GoldenMeanSource(p=0.5, _seed=42), 2),
        ("Biased Coin", BiasedCoinSource(p=0.7, _seed=42), 1),
    ]

    sample_sizes = [1_000, 10_000, 100_000]

    algorithms = [
        ("CSSR", lambda: CSSR(CSSRConfig(max_history=5, significance=0.001))),
        ("Spectral", lambda: Spectral(SpectralConfig(max_history=5))),
        ("CSM", lambda: CSM(CSMConfig(history_length=5))),
    ]

    results: list[Result] = []

    for algo_name, algo_factory in algorithms:
        print(f"\n{algo_name}")
        print("-" * 50)

        for process_name, _source_template, expected in tests:
            for n in sample_sizes:
                # Create fresh source and algorithm
                if process_name == "Even Process":
                    source = EvenProcessSource(p=0.5, _seed=42)
                elif process_name == "Golden Mean":
                    source = GoldenMeanSource(p=0.5, _seed=42)
                else:
                    source = BiasedCoinSource(p=0.7, _seed=42)

                algo = algo_factory()

                try:
                    result = run_test(algo_name, algo, process_name, source, n, expected)
                    results.append(result)

                    status = "✓" if result.correct else "✗"
                    print(
                        f"  {status} {process_name:15} N={n:>7,} → "
                        f"{result.actual_states} states (expect {expected}) "
                        f"[{result.runtime_ms:>7.1f}ms]"
                    )
                except Exception as e:
                    print(f"  ✗ {process_name:15} N={n:>7,} → ERROR: {e}")

    # Summary
    print()
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)

    for algo_name, _ in algorithms:
        algo_results = [r for r in results if r.algorithm == algo_name]
        correct = sum(1 for r in algo_results if r.correct)
        total = len(algo_results)
        pct = 100 * correct / total if total else 0
        print(f"  {algo_name:10}: {correct}/{total} correct ({pct:.0f}%)")

    # Check if CSSR matches Shalizi benchmarks
    print()
    print("=" * 70)
    print("SHALIZI (2004) BENCHMARK COMPARISON")
    print("=" * 70)

    cssr_results = [r for r in results if r.algorithm == "CSSR"]

    # Even Process at N=10,000 should be 2 states
    even_10k = next(
        (r for r in cssr_results if r.process == "Even Process" and r.sample_size == 10_000), None
    )
    if even_10k:
        status = "✓ PASS" if even_10k.correct else "✗ FAIL"
        print(f"  Even Process N=10,000: {even_10k.actual_states} states (expect 2) → {status}")

    # Golden Mean should be 2 states
    gm_10k = next(
        (r for r in cssr_results if r.process == "Golden Mean" and r.sample_size == 10_000), None
    )
    if gm_10k:
        status = "✓ PASS" if gm_10k.correct else "✗ FAIL"
        print(f"  Golden Mean N=10,000:  {gm_10k.actual_states} states (expect 2) → {status}")

    # Overall pass/fail
    print()
    all_correct = all(r.correct for r in cssr_results)
    if all_correct:
        print("✓ ALL CSSR TESTS PASS - matches Shalizi (2004) benchmarks!")
    else:
        failed = [r for r in cssr_results if not r.correct]
        print(f"✗ {len(failed)} CSSR TESTS FAILED")
        for r in failed:
            print(
                f"    - {r.process} N={r.sample_size}: got {r.actual_states}, expected {r.expected_states}"
            )

    return 0 if all_correct else 1


if __name__ == "__main__":
    sys.exit(main())
