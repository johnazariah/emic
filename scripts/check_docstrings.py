#!/usr/bin/env python3
"""Pre-commit hook to check for missing docstrings in public APIs."""

import ast
import sys
from pathlib import Path


def check_file(filepath: str) -> list[tuple[str, int, str]]:
    """Check a Python file for missing docstrings."""
    issues: list[tuple[str, int, str]] = []

    with Path(filepath).open() as f:
        try:
            tree = ast.parse(f.read())
        except SyntaxError:
            return issues

    # Check module docstring for __init__.py files
    if not ast.get_docstring(tree) and "__init__.py" in str(filepath):
        issues.append(("module", 0, "Missing module docstring"))

    for node in ast.walk(tree):
        if (
            isinstance(node, ast.ClassDef)
            and not node.name.startswith("_")
            and not ast.get_docstring(node)
        ):
            issues.append(("class", node.lineno, f"{node.name}: missing docstring"))
        elif (
            isinstance(node, ast.FunctionDef)
            and not node.name.startswith("_")
            and not ast.get_docstring(node)
        ):
            issues.append(("function", node.lineno, f"{node.name}: missing docstring"))

    return issues


def main() -> int:
    """Run the docstring checker on provided files."""
    exit_code = 0

    for arg in sys.argv[1:]:
        if arg.endswith(".py") and "test" not in arg:
            issues = check_file(arg)
            for _kind, line, msg in issues:
                print(f"{arg}:{line}: {msg}")
                exit_code = 1

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
