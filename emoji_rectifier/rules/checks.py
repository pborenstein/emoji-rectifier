"""Checkmark and X rectification rules.

Always use text checkmarks and Xes, not awful emoji versions.
Replace emoji checks/Xes with clean text equivalents.
"""

from __future__ import annotations

# Variation Selector 15 - forces text/glyph presentation
VS15 = '\uFE0E'

# Checkmark and X rules: emoji -> text equivalent
CHECK_RULES: dict[str, str] = {
    # Checkmarks - use simple CHECK MARK
    '✅': f'✓{VS15}',  # Heavy check mark emoji -> light check mark
    '☑': f'✓{VS15}',   # Ballot box with check -> light check mark
    '✔': f'✓{VS15}',   # Heavy check mark -> light check mark
    '☑️': f'✓{VS15}',  # Ballot box with check (with VS16) -> light check

    # X marks - use simple MULTIPLICATION X
    '❌': f'✗{VS15}',  # Cross mark emoji -> multiplication X
    '❎': f'✗{VS15}',  # Cross mark button -> multiplication X
    '✖': f'✗{VS15}',   # Heavy multiplication X -> light multiplication X
    '✖️': f'✗{VS15}',  # Heavy multiplication (with VS16) -> light X

    # Alternative: simple ASCII versions (commented out, use if preferred)
    # '✅': '[x]',
    # '❌': '[ ]',
    # '☑': '[x]',
}

# Characters that need rectification (for scanning)
CHECK_CHARS = set(CHECK_RULES.keys())


def rectify_checks(text: str) -> str:
    """
    Rectify checkmarks and Xes in text.

    Args:
        text: Input text

    Returns:
        Rectified text with proper text-style checkmarks and Xes
    """
    result = text

    for emoji, replacement in CHECK_RULES.items():
        result = result.replace(emoji, replacement)

    return result


def has_unrectified_checks(text: str) -> bool:
    """
    Check if text contains checkmarks/Xes that need rectification.

    Returns:
        True if any checks/Xes need fixing
    """
    return any(char in text for char in CHECK_CHARS)
