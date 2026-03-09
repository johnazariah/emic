#!/usr/bin/env bash
# Check that README.md is updated when the public API surface changes.
#
# Triggered by changes to:
#   - src/emic/__init__.py or any sub-package __init__.py (exports)
#   - pyproject.toml (version, metadata)
#
# Usage: scripts/check_readme.sh [staged-files...]
# Called by pre-commit with the list of staged files.

README="README.md"
API_CHANGED=false
README_CHANGED=false

for file in "$@"; do
    case "$file" in
        src/emic/*__init__.py) API_CHANGED=true ;;
        src/emic/__init__.py) API_CHANGED=true ;;
        pyproject.toml) API_CHANGED=true ;;
        "$README") README_CHANGED=true ;;
    esac
done

if [ "$API_CHANGED" = true ] && [ "$README_CHANGED" = false ]; then
    echo "ERROR: Public API surface changed but $README was not updated."
    echo ""
    echo "Files that trigger this check:"
    echo "  - src/emic/**/__init__.py (module exports)"
    echo "  - pyproject.toml (version, metadata)"
    echo ""
    echo "Please review $README and update if needed, then stage it."
    echo ""
    echo "To skip (e.g. if README is genuinely unaffected):"
    echo "  SKIP=check-readme git commit ..."
    exit 1
fi
