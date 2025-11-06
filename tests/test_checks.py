"""Tests for checkmark and X rectification rules."""

import pytest

from emoji_rectifier.rules.checks import (
    VS15,
    has_unrectified_checks,
    rectify_checks,
)


class TestCheckRectification:
    """Test checkmark and X rectification."""

    def test_checkmark_emoji_replaced(self):
        """Checkmark emoji should be replaced with text check."""
        result = rectify_checks("✅")
        assert "✅" not in result
        assert "✓" in result
        assert VS15 in result

    def test_x_emoji_replaced(self):
        """X emoji should be replaced with text X."""
        result = rectify_checks("❌")
        assert "❌" not in result
        assert "✗" in result

    def test_multiple_checks(self):
        """Multiple checks should all be replaced."""
        result = rectify_checks("✅ Task done ❌ Task failed")
        assert "✅" not in result
        assert "❌" not in result
        assert result.count("✓") == 1
        assert result.count("✗") == 1

    def test_has_unrectified_checks_true(self):
        """Should detect unrectified checks."""
        assert has_unrectified_checks("✅") is True
        assert has_unrectified_checks("❌") is True

    def test_has_unrectified_checks_false(self):
        """Should not flag already rectified checks."""
        assert has_unrectified_checks(f"✓{VS15}") is False
        assert has_unrectified_checks("no checks here") is False

    def test_preserves_other_text(self):
        """Should preserve non-check text."""
        text = "Task: ✅ complete"
        result = rectify_checks(text)
        assert "Task:" in result
        assert "complete" in result
