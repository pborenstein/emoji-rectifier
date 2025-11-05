"""Arrow rectification rules.

Always use text arrows, not goofy emoji arrows.
Add U+FE0E (variation selector 15) to force text presentation.
"""

from __future__ import annotations

# Variation Selector 15 - forces text/glyph presentation
VS15 = '\uFE0E'

# Arrow rules: character -> rectified version
# For most arrows, we add VS15 to force text style
# For emoji-only arrows, we replace with text equivalents
ARROW_RULES: dict[str, str] = {
    # Basic directional arrows - add VS15
    '→': f'→{VS15}',  # U+2192 RIGHTWARDS ARROW
    '←': f'←{VS15}',  # U+2190 LEFTWARDS ARROW
    '↑': f'↑{VS15}',  # U+2191 UPWARDS ARROW
    '↓': f'↓{VS15}',  # U+2193 DOWNWARDS ARROW

    # Bidirectional arrows - add VS15
    '↔': f'↔{VS15}',  # U+2194 LEFT RIGHT ARROW
    '↕': f'↕{VS15}',  # U+2195 UP DOWN ARROW

    # Diagonal arrows - add VS15
    '↖': f'↖{VS15}',  # U+2196 NORTH WEST ARROW
    '↗': f'↗{VS15}',  # U+2197 NORTH EAST ARROW
    '↘': f'↘{VS15}',  # U+2198 SOUTH EAST ARROW
    '↙': f'↙{VS15}',  # U+2199 SOUTH WEST ARROW

    # Heavy/bold arrows - add VS15
    '⬆': f'⬆{VS15}',  # U+2B06 UPWARDS BLACK ARROW
    '⬇': f'⬇{VS15}',  # U+2B07 DOWNWARDS BLACK ARROW
    '⬅': f'⬅{VS15}',  # U+2B05 LEFTWARDS BLACK ARROW
    '➡': f'➡{VS15}',  # U+27A1 BLACK RIGHTWARDS ARROW

    # Curved arrows - add VS15
    '↩': f'↩{VS15}',  # U+21A9 LEFTWARDS ARROW WITH HOOK
    '↪': f'↪{VS15}',  # U+21AA RIGHTWARDS ARROW WITH HOOK
    '⤴': f'⤴{VS15}',  # U+2934 ARROW POINTING RIGHTWARDS THEN CURVING UPWARDS
    '⤵': f'⤵{VS15}',  # U+2935 ARROW POINTING RIGHTWARDS THEN CURVING DOWNWARDS

    # Emoji-only arrows - replace with text equivalents
    '🔼': f'▲{VS15}',  # Up-pointing triangle instead of emoji
    '🔽': f'▼{VS15}',  # Down-pointing triangle instead of emoji
    '⏫': f'⬆{VS15}',  # Fast up -> heavy up arrow
    '⏬': f'⬇{VS15}',  # Fast down -> heavy down arrow
    '⏪': f'⬅{VS15}',  # Fast left -> heavy left arrow
    '⏩': f'➡{VS15}',  # Fast right -> heavy right arrow
    '🔀': f'↔{VS15}',  # Shuffle -> left-right arrow
    '🔁': f'↻',       # Repeat -> clockwise arrow
    '🔂': f'↻',       # Repeat one -> clockwise arrow
    '🔃': f'⟲',       # Clockwise vertical arrows
    '🔄': f'↻',       # Counterclockwise arrows -> clockwise (simpler)
}

# Characters that need rectification (for scanning)
ARROW_CHARS = set(ARROW_RULES.keys())

def rectify_arrows(text: str, *, idempotent: bool = True) -> str:
    """
    Rectify arrows in text by adding variation selectors or substituting.

    Args:
        text: Input text
        idempotent: If True, don't add VS15 if already present (default: True)

    Returns:
        Rectified text with proper text-style arrows
    """
    result = []
    i = 0

    while i < len(text):
        char = text[i]

        if char in ARROW_RULES:
            replacement = ARROW_RULES[char]

            # Check idempotency: if replacement would add VS15 and it's already there
            if idempotent and i + 1 < len(text):
                next_char = text[i + 1]
                if next_char == VS15:
                    # Already has VS15, keep as-is
                    result.append(char)
                    result.append(VS15)
                    i += 2
                    continue

            result.append(replacement)
        else:
            result.append(char)

        i += 1

    return ''.join(result)


def has_unrectified_arrows(text: str) -> bool:
    """
    Check if text contains arrows that need rectification.

    Returns:
        True if any arrows need fixing
    """
    for i, char in enumerate(text):
        if char in ARROW_RULES:
            # Check if this arrow already has VS15
            if i + 1 < len(text) and text[i + 1] == VS15:
                # This specific instance is already rectified
                continue
            # Check if it's an emoji-only arrow that needs replacement
            replacement = ARROW_RULES[char]
            if replacement != char + VS15:
                # Needs substitution
                return True
            # Needs VS15
            return True

    return False
