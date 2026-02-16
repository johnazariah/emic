#!/usr/bin/env python3
"""Generate LaTeX tables from benchmark results.

Usage:
    python analyze_results.py

Outputs LaTeX table files to the technical report's generated/ directory.
"""

import json
import re
import subprocess
from pathlib import Path

import pandas as pd

# Paths
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR / "../.."  # computational-mechanics-review
WORKSPACE_ROOT = SCRIPT_DIR / "../../../.."  # workspace root
RESULTS_PATH = SCRIPT_DIR / "results/summaries.json"
OUTPUT_DIR = PROJECT_ROOT / "paper-technical/generated"

# Process metadata
PROCESS_NAMES = {
    "biased_coin": "BiasedCoin",
    "golden_mean": "GoldenMean",
    "even_process": "EvenProcess",
    "periodic": "Periodic",
}
PROCESS_ORDER = ["biased_coin", "golden_mean", "even_process", "periodic"]
EXPECTED_STATES = {"biased_coin": 1, "golden_mean": 2, "even_process": 2, "periodic": 3}
ALGORITHMS = ["cssr", "spectral", "nsd", "csm", "bsi"]
SAMPLE_SIZES = [100, 1000, 10000, 100000, 1000000]


def load_data() -> pd.DataFrame:
    """Load benchmark results into a DataFrame."""
    with open(RESULTS_PATH) as f:
        data = json.load(f)
    df = pd.DataFrame(data)
    df = df.rename(columns={"sample_size": "num_samples", "num_states_mode": "num_states"})
    return df


def write_latex(filename: str, content: str) -> None:
    """Write LaTeX content to file."""
    OUTPUT_DIR.mkdir(exist_ok=True)
    path = OUTPUT_DIR / filename
    path.write_text(content)
    print(f"  Written: {path}")


def generate_state_counts_table(df: pd.DataFrame) -> None:
    """Generate tab:state-counts - state counts at N=100,000."""
    n100k = df[df["num_samples"] == 100000]

    latex = r"""\begin{table}[h]
\centering
\caption{Inferred state counts at $N = 100{,}000$ (from benchmark data)}
\label{tab:state-counts}
\begin{tabular}{lcccccc}
\toprule
Process & True & CSSR & Spectral & NSD & CSM & BSI \\
\midrule
"""

    for proc in PROCESS_ORDER:
        proc_data = n100k[n100k["process"] == proc]
        expected = EXPECTED_STATES[proc]
        states = {row["algorithm"]: int(row["num_states"]) for _, row in proc_data.iterrows()}
        latex += f"{PROCESS_NAMES[proc]} & {expected}"
        for alg in ALGORITHMS:
            latex += f" & {states.get(alg, '?')}"
        latex += " \\\\\n"

    latex += r"""\bottomrule
\end{tabular}
\end{table}"""

    write_latex("tab-state-counts.tex", latex)


def generate_correctness_table(df: pd.DataFrame) -> None:
    """Generate tab:correctness - correctness summary for N >= 1000."""
    large_n = df[df["num_samples"] >= 1000]
    max_per_process = 4  # 4 sample sizes >= 1000

    latex = r"""\begin{table}[htbp]
\centering
\begin{tabular}{lccccc}
\toprule
\textbf{Process} & \textbf{CSSR} & \textbf{Spectral} & \textbf{NSD} & \textbf{CSM} & \textbf{BSI} \\
\midrule
"""

    totals = dict.fromkeys(ALGORITHMS, 0)

    for proc in PROCESS_ORDER:
        proc_data = large_n[large_n["process"] == proc]
        expected = EXPECTED_STATES[proc]
        scores = {}

        for alg in ALGORITHMS:
            alg_data = proc_data[proc_data["algorithm"] == alg]
            correct_count = int((alg_data["correct_rate"] == 1.0).sum())
            scores[alg] = correct_count
            totals[alg] += correct_count

        proc_label = f"{PROCESS_NAMES[proc]} ({expected})"
        latex += f"{proc_label}"
        for alg in ALGORITHMS:
            latex += f" & {scores[alg]}/{max_per_process}"
        latex += " \\\\\n"

    # Totals row
    max_total = max_per_process * len(PROCESS_ORDER)
    latex += r"\midrule" + "\n"
    latex += r"\textbf{Overall}"

    # Find best algorithm for bolding
    best_alg = max(totals, key=totals.get)
    for alg in ALGORITHMS:
        if alg == best_alg:
            latex += f" & \\textbf{{{totals[alg]}/{max_total}}}"
        else:
            latex += f" & {totals[alg]}/{max_total}"
    latex += " \\\\\n"

    # Percentage row
    latex += " "
    for alg in ALGORITHMS:
        pct = f"({100 * totals[alg] / max_total:.0f}\\%)"
        if alg == best_alg:
            latex += f" & \\textbf{{{pct}}}"
        else:
            latex += f" & {pct}"
    latex += " \\\\\n"

    latex += r"""\bottomrule
\end{tabular}
\caption{Correctness by algorithm and process for $N \geq 1{,}000$. Each cell shows the number of sample sizes (out of 4: 1K, 10K, 100K, 1M) where the algorithm found the correct number of states.}
\label{tab:correctness}
\end{table}"""

    write_latex("tab-correctness.tex", latex)


def generate_correctness_detail_table(df: pd.DataFrame) -> None:
    """Generate tab:correctness-detail - detailed correctness by sample size."""

    def get_result_symbol(proc: str, alg: str, n: int) -> str:
        row = df[(df["process"] == proc) & (df["algorithm"] == alg) & (df["num_samples"] == n)]
        if len(row) == 0:
            return "?"
        expected = EXPECTED_STATES[proc]
        actual = int(row["num_states"].iloc[0])
        if actual == expected:
            return r"\checkmark"
        return f"$\\times${actual}"

    latex = r"""\begin{table}[htbp]
\centering
\footnotesize
\begin{tabular}{l|ccccc|ccccc}
\toprule
& \multicolumn{5}{c|}{\textbf{Golden Mean (2 states)}} & \multicolumn{5}{c}{\textbf{Even Process (2 states)}} \\
\textbf{N} & 100 & 1K & 10K & 100K & 1M & 100 & 1K & 10K & 100K & 1M \\
\midrule
"""

    for alg in ALGORITHMS:
        alg_upper = alg.upper()
        gm_results = [get_result_symbol("golden_mean", alg, n) for n in SAMPLE_SIZES]
        ep_results = [get_result_symbol("even_process", alg, n) for n in SAMPLE_SIZES]
        latex += f"{alg_upper} & {' & '.join(gm_results)} & {' & '.join(ep_results)} \\\\\n"

    latex += r"""\midrule
& \multicolumn{5}{c|}{\textbf{Biased Coin (1 state)}} & \multicolumn{5}{c}{\textbf{Periodic (3 states)}} \\
\textbf{N} & 100 & 1K & 10K & 100K & 1M & 100 & 1K & 10K & 100K & 1M \\
\midrule
"""

    for alg in ALGORITHMS:
        alg_upper = alg.upper()
        bc_results = [get_result_symbol("biased_coin", alg, n) for n in SAMPLE_SIZES]
        per_results = [get_result_symbol("periodic", alg, n) for n in SAMPLE_SIZES]
        latex += f"{alg_upper} & {' & '.join(bc_results)} & {' & '.join(per_results)} \\\\\n"

    latex += r"""\bottomrule
\end{tabular}
\caption{Detailed correctness by sample size. \checkmark = correct state count; $\times n$ = inferred $n$ states (wrong).}
\label{tab:correctness-detail}
\end{table}"""

    write_latex("tab-correctness-detail.tex", latex)


def generate_perf_summary_table(df: pd.DataFrame) -> None:
    """Generate tab:perf-summary - performance summary."""
    n1m = df[df["num_samples"] == 1000000]
    large_n = df[df["num_samples"] >= 1000]

    # Runtime means
    runtime_means = {}
    for alg in ALGORITHMS:
        alg_data = n1m[n1m["algorithm"] == alg]
        runtime_means[alg] = alg_data["runtime_mean"].mean()

    # Correctness at N >= 1000
    correctness_large = {}
    for alg in ALGORITHMS:
        alg_data = large_n[large_n["algorithm"] == alg]
        correctness_large[alg] = alg_data["correct_rate"].mean() * 100

    cssr_time = runtime_means["cssr"]
    best_alg = max(correctness_large, key=correctness_large.get)

    latex = r"""\begin{table}[htbp]
\centering
\begin{tabular}{lccccc}
\toprule
\textbf{Metric} & \textbf{CSSR} & \textbf{Spectral} & \textbf{CSM} & \textbf{BSI} & \textbf{NSD} \\
\midrule
"""

    # Time row
    latex += "Time @ $N=1$M"
    for alg in ["cssr", "spectral", "csm", "bsi", "nsd"]:
        latex += f" & {runtime_means[alg]:.1f} s"
    latex += " \\\\\n"

    # Speedup row
    latex += "Speedup vs CSSR & 1$\\times$"
    for alg in ["spectral", "csm", "bsi", "nsd"]:
        speedup = cssr_time / runtime_means[alg]
        latex += f" & {speedup:.1f}$\\times$"
    latex += " \\\\\n"

    # Correctness row
    latex += "Correctness ($N \\geq 1$K)"
    for alg in ["cssr", "spectral", "csm", "bsi", "nsd"]:
        pct = f"{correctness_large[alg]:.0f}\\%"
        if alg == best_alg:
            latex += f" & \\textbf{{{pct}}}"
        else:
            latex += f" & {pct}"
    latex += " \\\\\n"

    latex += r"""\bottomrule
\end{tabular}
\caption{Summary of performance characteristics across all algorithms.}
\label{tab:perf-summary}
\end{table}"""

    write_latex("tab-perf-summary.tex", latex)


def generate_macros(df: pd.DataFrame) -> None:
    """Generate benchmark-data.tex with LaTeX macros for use in prose."""
    large_n = df[df["num_samples"] >= 1000]
    n1m = df[df["num_samples"] == 1000000]
    n10k_plus = df[df["num_samples"] >= 10000]

    # Overall correctness (all sample sizes)
    overall_correct = {}
    for alg in ALGORITHMS:
        alg_data = df[df["algorithm"] == alg]
        overall_correct[alg] = alg_data["correct_rate"].mean() * 100

    # Correctness at N >= 1000
    large_n_correct = {}
    for alg in ALGORITHMS:
        alg_data = large_n[large_n["algorithm"] == alg]
        large_n_correct[alg] = alg_data["correct_rate"].mean() * 100

    # Correctness at N >= 10000
    n10k_correct = {}
    for alg in ALGORITHMS:
        alg_data = n10k_plus[n10k_plus["algorithm"] == alg]
        n10k_correct[alg] = alg_data["correct_rate"].mean() * 100

    # Runtime at N=1M
    runtime_1m = {}
    for alg in ALGORITHMS:
        alg_data = n1m[n1m["algorithm"] == alg]
        runtime_1m[alg] = alg_data["runtime_mean"].mean()

    cssr_time = runtime_1m["cssr"]
    speedups = {alg: cssr_time / runtime_1m[alg] for alg in ALGORITHMS}

    # Find best algorithm
    best_alg = max(large_n_correct, key=large_n_correct.get)

    # Generate macros
    latex = "% Auto-generated benchmark data macros\n"
    latex += "% Generated by: experiments/benchmarks/analyze_results.py\n"
    latex += "% Do not edit manually - regenerate with 'make report'\n\n"

    # Overall correctness
    latex += "% Overall correctness (all sample sizes)\n"
    for alg in ALGORITHMS:
        latex += f"\\newcommand{{\\{alg}OverallCorrectness}}{{{overall_correct[alg]:.0f}}}\n"

    # Large N correctness
    latex += "\n% Correctness at N >= 1,000\n"
    for alg in ALGORITHMS:
        latex += f"\\newcommand{{\\{alg}LargeNCorrectness}}{{{large_n_correct[alg]:.0f}}}\n"

    # N >= 10K correctness
    latex += "\n% Correctness at N >= 10,000\n"
    for alg in ALGORITHMS:
        latex += f"\\newcommand{{\\{alg}TenKCorrectness}}{{{n10k_correct[alg]:.0f}}}\n"

    # Runtime
    latex += "\n% Runtime at N=1,000,000 (seconds)\n"
    for alg in ALGORITHMS:
        latex += f"\\newcommand{{\\{alg}Runtime}}{{{runtime_1m[alg]:.1f}}}\n"

    # Speedups
    latex += "\n% Speedup vs CSSR\n"
    for alg in ALGORITHMS:
        if alg == "cssr":
            latex += f"\\newcommand{{\\{alg}Speedup}}{{1}}\n"
        else:
            latex += f"\\newcommand{{\\{alg}Speedup}}{{{speedups[alg]:.1f}}}\n"

    # Best algorithm
    latex += "\n% Best performing algorithm\n"
    latex += f"\\newcommand{{\\bestAlgorithm}}{{{best_alg.upper()}}}\n"
    latex += f"\\newcommand{{\\bestCorrectness}}{{{large_n_correct[best_alg]:.0f}}}\n"

    # Test statistics (from pytest)
    test_stats = get_test_stats()
    if test_stats:
        latex += "\n% Test statistics (from pytest)\n"
        latex += f"\\newcommand{{\\testCount}}{{{test_stats['count']}}}\n"
        latex += f"\\newcommand{{\\testCoverage}}{{{test_stats['coverage']}}}\n"

    write_latex("benchmark-data.tex", latex)


def get_test_stats() -> dict | None:
    """Run pytest to get test count and coverage."""
    workspace = WORKSPACE_ROOT.resolve()
    print(f"  Running pytest from: {workspace}")
    try:
        # Get test count
        result = subprocess.run(
            ["uv", "run", "pytest", "--collect-only", "-q"],
            cwd=workspace,
            capture_output=True,
            text=True,
            timeout=60,
        )
        # Parse "X tests collected"
        match = re.search(r"(\d+) tests? collected", result.stdout)
        test_count = int(match.group(1)) if match else 0

        # Get coverage - use source path
        result = subprocess.run(
            ["uv", "run", "pytest", "--cov=src/emic", "--cov-report=term-missing", "-q", "--tb=no"],
            cwd=workspace,
            capture_output=True,
            text=True,
            timeout=300,
        )
        # Parse "TOTAL ... XX%"
        match = re.search(r"TOTAL\s+\d+\s+\d+\s+\d+\s+\d+\s+(\d+)%", result.stdout)
        coverage = int(match.group(1)) if match else 0

        if coverage == 0:
            # Try alternate parsing or show debug info
            print(
                f"  Coverage stdout snippet: {result.stdout[-500:] if result.stdout else 'empty'}"
            )

        return {"count": test_count, "coverage": coverage}
    except (subprocess.TimeoutExpired, FileNotFoundError) as e:
        print(f"  Warning: Could not get test stats: {e}")
        return None


def main() -> None:
    """Generate all LaTeX tables and macros."""
    print("Loading benchmark results...")
    df = load_data()
    print(f"  Loaded {len(df)} records")

    print("Generating LaTeX tables...")
    generate_state_counts_table(df)
    generate_correctness_table(df)
    generate_correctness_detail_table(df)
    generate_perf_summary_table(df)

    print("Generating LaTeX macros...")
    generate_macros(df)

    print("Done!")


if __name__ == "__main__":
    main()
