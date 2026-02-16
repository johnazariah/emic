#!/usr/bin/env python3
"""Update LaTeX test statistic macros in benchmark-data.tex.

This script refreshes test and coverage macros used by the technical report:
- \\testCount
- \\unitTestCount
- \\goldenTestCount
- \\integrationTestCount
- \\propertyTestCount
- \\testCoverage

Run this before compiling `paper-technical/paper.tex` to keep reported metrics current.
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path


SCRIPT_DIR = Path(__file__).parent
WORKSPACE_ROOT = (SCRIPT_DIR / "../../../../..").resolve()
BENCHMARK_DATA_PATH = (
    WORKSPACE_ROOT
    / ".project/research/computational-mechanics-review/paper-technical/generated/benchmark-data.tex"
)


def run_command(cmd: list[str]) -> str:
    result = subprocess.run(
        cmd,
        cwd=WORKSPACE_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    output = f"{result.stdout}\n{result.stderr}"
    if result.returncode != 0:
        msg = f"Command failed ({result.returncode}): {' '.join(cmd)}\n{output}"
        raise RuntimeError(msg)
    return output


def parse_collected_tests(output: str) -> int:
    match = re.search(r"(\d+)\s+tests?\s+collected", output)
    if not match:
        msg = f"Could not parse collected test count from output:\n{output}"
        raise ValueError(msg)
    return int(match.group(1))


def collect_test_counts() -> dict[str, int]:
    total = parse_collected_tests(run_command(["uv", "run", "pytest", "--collect-only", "-q"]))
    unit = parse_collected_tests(
        run_command(["uv", "run", "pytest", "--collect-only", "-q", "tests/unit"])
    )
    golden = parse_collected_tests(
        run_command(["uv", "run", "pytest", "--collect-only", "-q", "tests/golden"])
    )
    integration = parse_collected_tests(
        run_command(["uv", "run", "pytest", "--collect-only", "-q", "tests/integration"])
    )

    # Any remaining tests (for example property tests) are attributed here.
    property_count = max(total - unit - golden - integration, 0)

    return {
        "testCount": total,
        "unitTestCount": unit,
        "goldenTestCount": golden,
        "integrationTestCount": integration,
        "propertyTestCount": property_count,
    }


def collect_coverage() -> str:
    output = run_command(
        [
            "uv",
            "run",
            "pytest",
            "--cov=src/emic",
            "--cov-report=term-missing",
            "-q",
            "--tb=no",
        ]
    )

    match = re.search(r"Total coverage:\s*([0-9]+(?:\.[0-9]+)?)%", output)
    if match:
        return match.group(1)

    match = re.search(r"TOTAL\s+\d+\s+\d+\s+\d+\s+\d+\s+([0-9]+)%", output)
    if match:
        return match.group(1)

    msg = f"Could not parse coverage percentage from output:\n{output}"
    raise ValueError(msg)


def replace_or_append_macro(content: str, macro: str, value: str) -> str:
    pattern = rf"\\newcommand\{{\\{macro}\}}\{{[^}}]*\}}"
    replacement = f"\\newcommand{{\\{macro}}}{{{value}}}"
    if re.search(pattern, content):
        return re.sub(pattern, lambda _: replacement, content)
    return content + f"\n{replacement}"


def main() -> None:
    if not BENCHMARK_DATA_PATH.exists():
        msg = f"Missing benchmark data file: {BENCHMARK_DATA_PATH}"
        raise FileNotFoundError(msg)

    counts = collect_test_counts()
    coverage = collect_coverage()

    content = BENCHMARK_DATA_PATH.read_text(encoding="utf-8")
    for macro, value in counts.items():
        content = replace_or_append_macro(content, macro, str(value))
    content = replace_or_append_macro(content, "testCoverage", coverage)

    BENCHMARK_DATA_PATH.write_text(content, encoding="utf-8")

    print("Updated benchmark-data.tex test stats:")
    for macro, value in counts.items():
        print(f"  {macro} = {value}")
    print(f"  testCoverage = {coverage}")


if __name__ == "__main__":
    main()
