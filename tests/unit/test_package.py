"""Unit tests for emic core types."""

from __future__ import annotations

import pytest

import emic


@pytest.mark.unit
class TestPackage:
    """Basic package tests."""

    def test_version_exists(self) -> None:
        """Package should have a version string."""
        assert hasattr(emic, "__version__")
        assert isinstance(emic.__version__, str)

    def test_version_format(self) -> None:
        """Version should follow semver pattern."""
        version = emic.__version__
        parts = version.split(".")
        assert len(parts) >= 2, "Version should have at least major.minor"
        # First two parts should be numeric
        assert parts[0].isdigit(), "Major version should be numeric"
        assert parts[1].isdigit(), "Minor version should be numeric"
