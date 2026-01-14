# ============================================================================
# emic Development Container
# ============================================================================
# Multi-stage Dockerfile for Python + LaTeX development environment
#
# Base: Microsoft Python devcontainer
# Adds: TeX Live (science scheme), uv package manager, Graphviz
# ============================================================================

FROM mcr.microsoft.com/devcontainers/python:1-3.11-bookworm

# Avoid prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# ============================================================================
# System Dependencies
# ============================================================================

RUN apt-get update && apt-get install -y --no-install-recommends \
    # LaTeX - using texlive-science for a good balance of size and features
    texlive-latex-recommended \
    texlive-latex-extra \
    texlive-science \
    texlive-fonts-recommended \
    texlive-fonts-extra \
    texlive-pictures \
    texlive-bibtex-extra \
    biber \
    latexmk \
    # Graphviz for state diagrams
    graphviz \
    libgraphviz-dev \
    # Other useful tools
    make \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# ============================================================================
# Install uv (fast Python package manager)
# ============================================================================

RUN curl -LsSf https://astral.sh/uv/install.sh | sh \
    && mv /root/.local/bin/uv /usr/local/bin/uv \
    && mv /root/.local/bin/uvx /usr/local/bin/uvx

# ============================================================================
# Set up workspace
# ============================================================================

WORKDIR /workspace

# Copy project files for dependency installation
# (This layer will be cached if pyproject.toml doesn't change)
COPY pyproject.toml .
COPY README.md .
COPY LICENSE .
COPY src/ src/

# Create virtual environment and install dependencies
RUN uv venv /workspace/.venv \
    && . /workspace/.venv/bin/activate \
    && uv sync --dev

# ============================================================================
# Environment Configuration
# ============================================================================

# Add venv to PATH
ENV PATH="/workspace/.venv/bin:$PATH"

# Python configuration
ENV PYTHONPATH="/workspace/src"
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Hypothesis configuration
ENV HYPOTHESIS_PROFILE="dev"

# ============================================================================
# User Configuration
# ============================================================================

# Create X11 socket directory with proper permissions (for VS Code Dev Containers)
RUN mkdir -p /tmp/.X11-unix && chmod 1777 /tmp/.X11-unix

# Switch to vscode user (created by base image)
USER vscode

# Ensure vscode user can write to workspace
RUN mkdir -p /home/vscode/.cache

# Default command
CMD ["bash"]
