"""Tests for star rectification rules."""

import pytest

from emoji_rectifier.rules.stars import (
    VS15,
    has_unrectified_stars,
    rectify_stars,
)


class TestStarRectification:
    """Test star rectification."""

    def test_star_emoji_replaced(self):
        """Star emoji should be replaced with text star."""
        result = rectify_stars("⭐")
        assert "⭐" not in result
        assert "★" in result

    def test_sparkles_replaced_with_asterisk(self):
        """Sparkles should become simple asterisk."""
        result = rectify_stars("✨")
        assert "✨" not in result
        assert "*" in result

    def test_multiple_sparkles(self):
        """Multiple sparkles should be handled."""
        result = rectify_stars("✨✨")
        # Should become **
        assert "**" in result

    def test_has_unrectified_stars_true(self):
        """Should detect unrectified stars."""
        assert has_unrectified_stars("⭐") is True
        assert has_unrectified_stars("✨") is True

    def test_has_unrectified_stars_false(self):
        """Should not flag already rectified stars."""
        assert has_unrectified_stars(f"★{VS15}") is False
        assert has_unrectified_stars("no stars here") is False

    def test_preserves_other_text(self):
        """Should preserve non-star text."""
        text = "Important ⭐ note"
        result = rectify_stars(text)
        assert "Important" in result
        assert "note" in result
