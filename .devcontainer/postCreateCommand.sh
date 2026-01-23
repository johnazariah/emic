#!/bin/bash
# ============================================================================
# Post-Create Command for emic devcontainer
# ============================================================================
# This script runs after the container is created.
# It sets up the development environment for immediate use.
# ============================================================================

set -e

echo "🚀 Setting up emic development environment..."

# ============================================================================
# Python Environment
# ============================================================================

echo "📦 Installing Python dependencies..."

# Ensure we have a virtual environment
if [ ! -d ".venv" ]; then
    uv venv .venv
fi

# Install all dependencies including dev
uv sync --dev

echo "✅ Python environment ready"

# ============================================================================
# Pre-commit Hooks
# ============================================================================

echo "🔧 Setting up pre-commit hooks..."

if [ -f ".pre-commit-config.yaml" ]; then
    uv run pre-commit install
    # Pre-warm the pre-commit environments so first commit doesn't have cold start
    uv run pre-commit install-hooks
    echo "✅ Pre-commit hooks installed and environments cached"
else
    echo "⚠️  No .pre-commit-config.yaml found, skipping"
fi

# ============================================================================
# Git Configuration
# ============================================================================

echo "🔧 Configuring git..."

# Set up git user identity (required in devcontainer)
git config user.name "John S Azariah"
git config user.email "john.azariah@student.uts.edu.au"

# Set up git to use main as default branch
git config --global init.defaultBranch main

# Enable git push for new branches
git config --global push.autoSetupRemote true

# Set up GitHub CLI as git credential helper (works with Podman on Windows)
if command -v gh &> /dev/null; then
    gh auth setup-git 2>/dev/null || echo "⚠️  GitHub CLI not authenticated - run 'gh auth login' to authenticate"
fi

echo "✅ Git configured"

# ============================================================================
# Verify Installation
# ============================================================================

echo ""
echo "🧪 Verifying installation..."

# Check Python
python --version

# Check uv
uv --version

# Check pytest
uv run pytest --version

# Check pyright
uv run pyright --version

# Check ruff
uv run ruff --version

# Check LaTeX
pdflatex --version | head -1

# Check Graphviz
dot -V 2>&1 | head -1

echo ""
echo "✅ All tools installed successfully!"
echo ""
echo "📝 Quick start:"
echo "   uv run pytest              # Run tests"
echo "   uv run pytest --cov        # Run tests with coverage"
echo "   uv run ruff check src      # Lint code"
echo "   uv run pyright src         # Type check"
echo ""
echo "🎉 Happy coding!"
