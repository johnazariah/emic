#!/usr/bin/env bash
# Check that .project/testing-register.md is updated when tests change.
#
# Usage: scripts/check_testing_register.sh [staged-files...]
# Called by pre-commit with the list of staged files.

REGISTER=".project/testing-register.md"
TESTS_CHANGED=false
REGISTER_CHANGED=false

for file in "$@"; do
    case "$file" in
        tests/*) TESTS_CHANGED=true ;;
        "$REGISTER") REGISTER_CHANGED=true ;;
    esac
done

if [ "$TESTS_CHANGED" = true ] && [ "$REGISTER_CHANGED" = false ]; then
    echo "ERROR: Test files were modified but $REGISTER was not updated."
    echo ""
    echo "Please update the testing register to reflect your test changes."
    echo "The register lives at: $REGISTER"
    echo ""
    echo "To skip this check (e.g. for pure refactoring with no intent change):"
    echo "  SKIP=check-testing-register git commit ..."
    exit 1
fi
