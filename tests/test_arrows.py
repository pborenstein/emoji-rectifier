"""Tests for arrow rectification rules."""

import pytest

from emoji_rectifier.rules.arrows import (
    VS15,
    has_unrectified_arrows,
    rectify_arrows,
)


class TestArrowRectification:
    """Test arrow rectification."""

    def test_basic_arrow_gets_vs15(self):
        """Basic arrows should get VS15 added."""
        result = rectify_arrows("→")
        assert result == f"→{VS15}"
        assert result.encode("utf-8") == b"\xe2\x86\x92\xef\xb8\x8e"

    def test_multiple_arrows(self):
        """Multiple arrows should all get VS15."""
        result = rectify_arrows("→ ← ↑ ↓")
        assert f"→{VS15}" in result
        assert f"←{VS15}" in result
        assert f"↑{VS15}" in result
        assert f"↓{VS15}" in result

    def test_idempotency(self):
        """Rectifying twice should produce same result."""
        text = "Arrow: →"
        once = rectify_arrows(text)
        twice = rectify_arrows(once)
        assert once == twice

    def test_already_rectified_arrow(self):
        """Already rectified arrows should not get duplicate VS15."""
        already_rectified = f"→{VS15}"
        result = rectify_arrows(already_rectified)
        # Should not add another VS15
        assert result.count(VS15) == 1
        assert result == already_rectified

    def test_emoji_arrow_replacement(self):
        """Emoji arrows should be replaced with text equivalents."""
        result = rectify_arrows("🔼")
        assert "🔼" not in result
        assert "▲" in result

    def test_has_unrectified_arrows_true(self):
        """Should detect unrectified arrows."""
        assert has_unrectified_arrows("→") is True
        assert has_unrectified_arrows("🔼") is True

    def test_has_unrectified_arrows_false(self):
        """Should not flag already rectified arrows."""
        assert has_unrectified_arrows(f"→{VS15}") is False
        assert has_unrectified_arrows("no arrows here") is False

    def test_mixed_content(self):
        """Should handle mixed content correctly."""
        text = "Steps: → follow → the → arrows →"
        result = rectify_arrows(text)
        assert result.count(VS15) == 4

    def test_preserves_other_text(self):
        """Should preserve non-arrow text."""
        text = "Hello world → this is a test"
        result = rectify_arrows(text)
        assert "Hello world" in result
        assert "this is a test" in result
