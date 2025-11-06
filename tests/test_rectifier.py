"""Tests for the main rectifier."""

import pytest

from emoji_rectifier.core.rectifier import Rectifier
from emoji_rectifier.core.rules import RuleCategory
from emoji_rectifier.rules.arrows import VS15


class TestRectifier:
    """Test the main Rectifier class."""

    def test_rectify_text_all_rules(self):
        """Test rectifying text with all rules enabled."""
        rectifier = Rectifier()
        text = "Steps: → ✅ ⭐"
        result = rectifier.rectify_text(text)

        # Should have rectified all types
        assert f"→{VS15}" in result
        assert "✓" in result
        assert ("★" in result or "*" in result)

    def test_rectify_text_arrows_only(self):
        """Test rectifying with only arrow rules."""
        rectifier = Rectifier(enabled_categories={RuleCategory.ARROWS})
        text = "Steps: → ✅ ⭐"
        result = rectifier.rectify_text(text)

        # Should only rectify arrows
        assert f"→{VS15}" in result
        assert "✅" in result  # Should remain unchanged
        assert "⭐" in result  # Should remain unchanged

    def test_needs_rectification_true(self):
        """Should detect text that needs rectification."""
        rectifier = Rectifier()
        assert rectifier.needs_rectification("→") is True
        assert rectifier.needs_rectification("✅") is True
        assert rectifier.needs_rectification("⭐") is True

    def test_needs_rectification_false(self):
        """Should not flag already rectified text."""
        rectifier = Rectifier()
        assert rectifier.needs_rectification(f"→{VS15}") is False
        assert rectifier.needs_rectification("no emoji here") is False

    def test_idempotency(self):
        """Rectifying twice should produce same result."""
        rectifier = Rectifier()
        text = "Arrow: → Check: ✅ Star: ⭐"

        once = rectifier.rectify_text(text)
        twice = rectifier.rectify_text(once)

        assert once == twice
