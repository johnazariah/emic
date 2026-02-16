#!/usr/bin/env python3
"""Generate LaTeX tables from emic-experiment results.

This script reads benchmark results from the unified emic-experiment platform
and generates LaTeX tables for the technical report.

Usage:
    python analyze_results.py                 # Use latest results
    python analyze_results.py path/to/data    # Use specific path

Input formats supported:
    - results.parquet (preferred)
    - results.json

Output:
    LaTeX table files in paper-technical/generated/
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pandas as pd

# Paths
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR / "../.."  # computational-mechanics-review
WORKSPACE_ROOT = SCRIPT_DIR / "../../../.."  # workspace root
OUTPUT_DIR = PROJECT_ROOT / "paper-technical/generated"

# Default results locations (in priority order)
DEFAULT_RESULTS_PATHS = [
    SCRIPT_DIR / "results/results.parquet",
    SCRIPT_DIR / "results/results.json",
    WORKSPACE_ROOT / "experiments/runs/latest/results.parquet",
    WORKSPACE_ROOT / "experiments/runs/latest/results.json",
]

# Process metadata
PROCESS_NAMES = {
    "biased_coin": "BiasedCoin",
    "golden_mean": "GoldenMean",
    "even_process": "EvenProcess",
    "periodic": "Periodic",
}
PROCESS_ORDER = ["biased_coin", "golden_mean", "even_process"]
EXPECTED_STATES = {"biased_coin": 1, "golden_mean": 2, "even_process": 2, "periodic": 3}
ALGORITHMS = ["cssr", "spectral", "csm", "bsi"]
SAMPLE_SIZES = [1000, 10000, 100000, 1000000]


def find_results_file() -> Path:
    """Find the results file to analyze."""
    for path in DEFAULT_RESULTS_PATHS:
        if path.exists():
            return path
    msg = "No results found. Run benchmarks first:\n  make benchmarks"
    raise FileNotFoundError(msg)


def load_data(path: Path | None = None) -> pd.DataFrame:
    """
    Load benchmark results into a DataFrame.

    Handles multiple formats:
    - emic-experiment parquet/json (long format with metric/value pairs)
    - Legacy run.py json (wide format with direct columns)

    Args:
        path: Path to results file. If None, searches default locations.

    Returns:
        DataFrame with columns: algorithm, process, num_samples,
        num_states, duration_s (if available), etc.
    """
    if path is None:
        path = find_results_file()

    print(f"Loading results from: {path}")

    if path.suffix == ".parquet":
        df = pd.read_parquet(path)
    else:
        with open(path) as f:
            data = json.load(f)
        df = pd.DataFrame(data)

    # Detect format and normalize
    if "metric" in df.columns and "value" in df.columns:
        # emic-experiment long format - pivot to wide
        pivot_df = df.pivot_table(
            index=["experiment", "algorithm", "process", "n_samples"],
            columns="metric",
            values="value",
            aggfunc="first",
        ).reset_index()
        pivot_df.columns.name = None

        # Rename for compatibility
        if "state_count" in pivot_df.columns:
            pivot_df["num_states"] = pivot_df["state_count"].astype(int)
        if "n_samples" in pivot_df.columns:
            pivot_df["num_samples"] = pivot_df["n_samples"]

        df = pivot_df
    else:
        # Legacy wide format from old run.py
        if "sample_size" in df.columns:
            df["num_samples"] = df["sample_size"]
        if "runtime_seconds" in df.columns:
            df["duration_s"] = df["runtime_seconds"]
        if "num_states" not in df.columns and "num_states_mode" in df.columns:
            df["num_states"] = df["num_states_mode"]

    print(f"Loaded {len(df)} configurations")
    return df


def write_latex(filename: str, content: str) -> None:
    """Write LaTeX content to file."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUTPUT_DIR / filename
    path.write_text(content)
    print(f"  Written: {path}")


def generate_state_counts_table(df: pd.DataFrame) -> None:
    """Generate tab:state-counts - state counts at N=100,000."""
    n100k = df[df["num_samples"] == 100000]

    latex = r"""\begin{table}[h]
\centering
\caption{Inferred state counts at $N = 100{,}000$}
\label{tab:state-counts}
\begin{tabular}{lccccc}
\toprule
Process & True & CSSR & Spectral & CSM & BSI \\
\midrule
"""

    for proc in PROCESS_ORDER:
        proc_data = n100k[n100k["process"] == proc]
        expected = EXPECTED_STATES[proc]
        states = {row["algorithm"]: int(row["num_states"]) for _, row in proc_data.iterrows()}
        latex += f"{PROCESS_NAMES[proc]} & {expected}"
        for alg in ALGORITHMS:
            val = states.get(alg, "?")
            if val == expected:
                latex += f" & \\textbf{{{val}}}"
            else:
                latex += f" & {val}"
        latex += " \\\\\n"

    latex += r"""\bottomrule
\end{tabular}
\end{table}"""

    write_latex("tab-state-counts.tex", latex)


def generate_correctness_table(df: pd.DataFrame) -> None:
    """Generate tab:correctness - correctness summary for N >= 1000."""
    large_n = df[df["num_samples"] >= 1000]
    max_per_process = len([n for n in SAMPLE_SIZES if n >= 1000])

    latex = r"""\begin{table}[htbp]
\centering
\begin{tabular}{lcccc}
\toprule
\textbf{Process} & \textbf{CSSR} & \textbf{Spectral} & \textbf{CSM} & \textbf{BSI} \\
\midrule
"""

    totals = dict.fromkeys(ALGORITHMS, 0)

    for proc in PROCESS_ORDER:
        proc_data = large_n[large_n["process"] == proc]
        expected = EXPECTED_STATES[proc]
        scores = {}

        for alg in ALGORITHMS:
            alg_data = proc_data[proc_data["algorithm"] == alg]
            correct_count = int((alg_data["num_states"] == expected).sum())
            scores[alg] = correct_count
            totals[alg] += correct_count

        proc_label = f"{PROCESS_NAMES[proc]} ({expected})"
        latex += f"{proc_label}"
        for alg in ALGORITHMS:
            latex += f" & {scores.get(alg, 0)}/{max_per_process}"
        latex += " \\\\\n"

    # Totals row
    max_total = max_per_process * len(PROCESS_ORDER)
    latex += r"\midrule" + "\n"
    latex += r"\textbf{Overall}"

    # Find best algorithm for bolding
    best_alg = max(totals, key=lambda k: totals[k]) if totals else ALGORITHMS[0]
    for alg in ALGORITHMS:
        if alg == best_alg:
            latex += f" & \\textbf{{{totals[alg]}/{max_total}}}"
        else:
            latex += f" & {totals.get(alg, 0)}/{max_total}"
    latex += " \\\\\n"

    # Percentage row
    latex += " "
    for alg in ALGORITHMS:
        pct = 100 * totals.get(alg, 0) / max_total if max_total > 0 else 0
        pct_str = f"({pct:.0f}\\%)"
        if alg == best_alg:
            latex += f" & \\textbf{{{pct_str}}}"
        else:
            latex += f" & {pct_str}"
    latex += " \\\\\n"

    latex += r"""\bottomrule
\end{tabular}
\caption{Correctness by algorithm and process for $N \geq 1{,}000$. Each cell shows the number of sample sizes where the algorithm found the correct number of states.}
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
\begin{tabular}{l|cccc|cccc}
\toprule
& \multicolumn{4}{c|}{\textbf{Golden Mean (2 states)}} & \multicolumn{4}{c}{\textbf{Even Process (2 states)}} \\
\textbf{N} & 1K & 10K & 100K & 1M & 1K & 10K & 100K & 1M \\
\midrule
"""

    for alg in ALGORITHMS:
        alg_upper = alg.upper()
        gm_results = [get_result_symbol("golden_mean", alg, n) for n in SAMPLE_SIZES]
        ep_results = [get_result_symbol("even_process", alg, n) for n in SAMPLE_SIZES]
        latex += f"{alg_upper} & {' & '.join(gm_results)} & {' & '.join(ep_results)} \\\\\n"

    latex += r"""\midrule
& \multicolumn{4}{c|}{\textbf{Biased Coin (1 state)}} & \multicolumn{4}{c}{} \\
\textbf{N} & 1K & 10K & 100K & 1M & & & & \\
\midrule
"""

    for alg in ALGORITHMS:
        alg_upper = alg.upper()
        bc_results = [get_result_symbol("biased_coin", alg, n) for n in SAMPLE_SIZES]
        latex += f"{alg_upper} & {' & '.join(bc_results)} & & & & \\\\\n"

    latex += r"""\bottomrule
\end{tabular}
\caption{Detailed correctness by sample size. \checkmark = correct state count; $\times n$ = inferred $n$ states.}
\label{tab:correctness-detail}
\end{table}"""

    write_latex("tab-correctness-detail.tex", latex)


def generate_runtime_table(df: pd.DataFrame) -> None:
    """Generate tab:runtime - runtime comparison at different sample sizes."""
    if "duration_s" not in df.columns:
        print("  Skipping runtime table (no duration data)")
        return

    latex = r"""\begin{table}[htbp]
\centering
\begin{tabular}{lrrrr}
\toprule
\textbf{Algorithm} & \textbf{N=1K} & \textbf{N=10K} & \textbf{N=100K} & \textbf{N=1M} \\
\midrule
"""

    for alg in ALGORITHMS:
        alg_data = df[(df["algorithm"] == alg) & (df["process"] == "even_process")]
        times = {}
        for n in SAMPLE_SIZES:
            row = alg_data[alg_data["num_samples"] == n]
            if len(row) > 0:
                t = row["duration_s"].iloc[0]
                if t < 0.1:
                    times[n] = f"{t * 1000:.0f}ms"
                elif t < 10:
                    times[n] = f"{t:.2f}s"
                else:
                    times[n] = f"{t:.1f}s"
            else:
                times[n] = "?"
        latex += f"{alg.upper()} & {times.get(1000, '?')} & {times.get(10000, '?')} & {times.get(100000, '?')} & {times.get(1000000, '?')} \\\\\n"

    latex += r"""\bottomrule
\end{tabular}
\caption{Runtime comparison on Even Process.}
\label{tab:runtime}
\end{table}"""

    write_latex("tab-runtime.tex", latex)


def generate_macros(df: pd.DataFrame) -> None:
    """Generate LaTeX macros with key statistics."""
    macros = []

    # Total algorithms tested
    n_algorithms = df["algorithm"].nunique()
    macros.append(f"\\newcommand{{\\numAlgorithms}}{{{n_algorithms}}}")

    # Total processes tested
    n_processes = df["process"].nunique()
    macros.append(f"\\newcommand{{\\numProcesses}}{{{n_processes}}}")

    # Total configurations
    n_configs = len(df)
    macros.append(f"\\newcommand{{\\numConfigs}}{{{n_configs}}}")

    # Best algorithm at N=100K
    n100k = df[df["num_samples"] == 100000]
    if not n100k.empty:
        correct_counts = {}
        for alg in ALGORITHMS:
            alg_data = n100k[n100k["algorithm"] == alg]
            correct = sum(
                1
                for _, row in alg_data.iterrows()
                if row["num_states"] == EXPECTED_STATES.get(row["process"], -1)
            )
            correct_counts[alg] = correct
        best_alg = max(correct_counts, key=lambda k: correct_counts[k])
        macros.append(f"\\newcommand{{\\bestAlgorithm}}{{{best_alg.upper()}}}")

    # Test stats from pytest (if available)
    try:
        result = subprocess.run(
            ["uv", "run", "pytest", "--collect-only", "-q"],
            capture_output=True,
            text=True,
            cwd=WORKSPACE_ROOT,
            timeout=30,
        )
        import re

        match = re.search(r"(\d+) tests", result.stdout)
        if match:
            n_tests = match.group(1)
            macros.append(f"\\newcommand{{\\numTests}}{{{n_tests}}}")
    except Exception:
        pass

    content = "% Auto-generated macros from benchmark results\n"
    content += "% Do not edit manually - regenerate with: make analyze\n\n"
    content += "\n".join(macros) + "\n"

    write_latex("macros.tex", content)


def main() -> None:
    """Main entry point."""
    print("=" * 60)
    print("Generating LaTeX tables from benchmark results")
    print("=" * 60)
    print()

    # Allow path override from command line
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else None

    try:
        df = load_data(path)
    except FileNotFoundError as e:
        print(f"ERROR: {e}")
        sys.exit(1)

    print()
    print("Generating tables:")

    generate_state_counts_table(df)
    generate_correctness_table(df)
    generate_correctness_detail_table(df)
    generate_runtime_table(df)
    generate_macros(df)

    print()
    print("Done!")


if __name__ == "__main__":
    main()
