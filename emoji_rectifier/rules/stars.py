"""Star rectification rules.

Use tasteful stars, not GAUDY emoji stars.
Replace emoji stars with clean text equivalents.
"""

from __future__ import annotations

# Variation Selector 15 - forces text/glyph presentation
VS15 = '\uFE0E'

# Star rules: gaudy emoji -> tasteful text
STAR_RULES: dict[str, str] = {
    # Common emoji stars -> tasteful alternatives
    '⭐': f'★{VS15}',   # Star emoji -> black star with VS15
    '🌟': f'☆{VS15}',   # Glowing star -> white star
    '✨': '*',          # Sparkles -> simple asterisk (most tasteful)
    '💫': f'✦{VS15}',   # Dizzy -> four-pointed star

    # Other star-like emoji
    '🌠': '·',          # Shooting star -> middot (subtle)
    '⚡': f'⚡{VS15}',   # High voltage -> with VS15 (sometimes used as emphasis)
    '💥': '*',          # Collision -> asterisk
    '🔆': f'☀{VS15}',   # Bright button -> sun symbol

    # Multiple stars (common patterns)
    '✨✨': '**',       # Double sparkle -> double asterisk
    '✨✨✨': '***',    # Triple sparkle -> triple asterisk

    # Star symbols that should use text style
    '⭐️': f'★{VS15}',  # Star with VS16 -> star with VS15
    '🌟': f'☆{VS15}',   # Glowing star
}

# Characters that need rectification (for scanning)
STAR_CHARS = set(STAR_RULES.keys())


def rectify_stars(text: str) -> str:
    """
    Rectify stars in text by replacing gaudy emoji with tasteful text.

    Args:
        text: Input text

    Returns:
        Rectified text with tasteful text-style stars
    """
    result = text

    # Sort by length descending to handle multi-character patterns first
    sorted_rules = sorted(STAR_RULES.items(), key=lambda x: len(x[0]), reverse=True)

    for emoji, replacement in sorted_rules:
        result = result.replace(emoji, replacement)

    return result


def has_unrectified_stars(text: str) -> bool:
    """
    Check if text contains stars that need rectification.

    Returns:
        True if any stars need fixing
    """
    # Check for any individual star characters
    for char in STAR_CHARS:
        if char in text:
            return True

    return False
