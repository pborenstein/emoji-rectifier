"""Rule engine for emoji rectification.

Manages and applies rectification rules across different categories.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Callable


class RuleCategory(Enum):
    """Categories of rectification rules."""
    ARROWS = "arrows"
    CHECKS = "checks"
    STARS = "stars"


@dataclass
class RectificationRule:
    """A single rectification rule."""
    category: RuleCategory
    source: str  # The emoji/character to replace
    target: str  # The rectified version
    description: str = ""


class RuleEngine:
    """
    Engine for applying rectification rules.

    Manages rules from different categories and applies them in the correct order.
    """

    def __init__(self, enabled_categories: set[RuleCategory] | None = None):
        """
        Initialize the rule engine.

        Args:
            enabled_categories: Set of categories to enable. If None, all are enabled.
        """
        self.enabled_categories = enabled_categories or {
            RuleCategory.ARROWS,
            RuleCategory.CHECKS,
            RuleCategory.STARS,
        }

    def rectify(self, text: str) -> str:
        """
        Apply all enabled rectification rules to text.

        Args:
            text: Input text

        Returns:
            Rectified text
        """
        result = text

        # Import here to avoid circular imports
        from ..rules.arrows import rectify_arrows
        from ..rules.checks import rectify_checks
        from ..rules.stars import rectify_stars

        # Apply rules in order: stars first (may have multi-char patterns),
        # then checks, then arrows (most common)
        if RuleCategory.STARS in self.enabled_categories:
            result = rectify_stars(result)

        if RuleCategory.CHECKS in self.enabled_categories:
            result = rectify_checks(result)

        if RuleCategory.ARROWS in self.enabled_categories:
            result = rectify_arrows(result)

        return result

    def needs_rectification(self, text: str) -> bool:
        """
        Check if text needs any rectification.

        Args:
            text: Input text

        Returns:
            True if any rules would modify the text
        """
        from ..rules.arrows import has_unrectified_arrows
        from ..rules.checks import has_unrectified_checks
        from ..rules.stars import has_unrectified_stars

        if RuleCategory.ARROWS in self.enabled_categories:
            if has_unrectified_arrows(text):
                return True

        if RuleCategory.CHECKS in self.enabled_categories:
            if has_unrectified_checks(text):
                return True

        if RuleCategory.STARS in self.enabled_categories:
            if has_unrectified_stars(text):
                return True

        return False

    def get_enabled_categories(self) -> list[str]:
        """Get list of enabled category names."""
        return [cat.value for cat in self.enabled_categories]
