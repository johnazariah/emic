"""
Shared pytest fixtures and configuration for emic tests.
"""

from __future__ import annotations

import os
from typing import TYPE_CHECKING

from hypothesis import Verbosity, settings

if TYPE_CHECKING:
    import pytest

# ============================================================================
# Hypothesis Profiles
# ============================================================================

# CI profile: more examples, longer deadline
settings.register_profile(
    "ci",
    max_examples=500,
    deadline=None,
    suppress_health_check=[],
    verbosity=Verbosity.normal,
)

# Dev profile: faster feedback
settings.register_profile(
    "dev",
    max_examples=50,
    deadline=500,
    verbosity=Verbosity.normal,
)

# Debug profile: minimal examples, verbose output
settings.register_profile(
    "debug",
    max_examples=10,
    deadline=None,
    verbosity=Verbosity.verbose,
)

# Load profile from environment variable (default: dev)
settings.load_profile(os.getenv("HYPOTHESIS_PROFILE", "dev"))


# ============================================================================
# Pytest Markers Configuration
# ============================================================================


def pytest_configure(config: pytest.Config) -> None:
    """Register custom markers."""
    config.addinivalue_line("markers", "unit: fast, isolated unit tests")
    config.addinivalue_line("markers", "integration: component integration tests")
    config.addinivalue_line("markers", "property: hypothesis property-based tests")
    config.addinivalue_line("markers", "golden: known-answer regression tests")
    config.addinivalue_line("markers", "slow: tests that take > 1 second")
    config.addinivalue_line("markers", "notebooks: notebook execution tests")


# ============================================================================
# Shared Fixtures
# ============================================================================

# Fixtures will be added here as we implement core types.
# See .project/specifications/002-core-types.md for planned fixtures.
