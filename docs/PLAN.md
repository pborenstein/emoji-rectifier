# emoji-rectifier: Project Plan

**Mission**: Make the world safe from emojimania by intelligently converting gaudy emoji to tasteful text-style characters.

## Core Philosophy

**"Rectify, Don't Ban"** - Instead of just removing emoji, we intelligently convert them to their proper text representations using Unicode variation selectors and appropriate substitutions.

## The Three Commandments

1. **Always use text arrows, not goofy emoji arrows**
2. **Always use text checkmarks and Xes, not awful emoji**
3. **Use tasteful stars, not GAUDY emoji**

## Technical Foundation

### Variation Selectors (The Secret Weapon)

Many Unicode characters have dual presentation:
- **Default**: Often renders as colorful emoji
- **U+FE0E (VS15)**: Forces text/glyph style (monochrome, typographic)
- **U+FE0F (VS16)**: Forces emoji style

Example: `→` (might be emoji) vs `→︎` (forced text with invisible U+FE0E)

See: [UNICODE-ARROWS.md](UNICODE-ARROWS.md) for details.

## Architecture

```
emoji-rectifier/
├── pyproject.toml           # uv configuration
├── README.md
├── emoji_rectifier/         # Main package
│   ├── __init__.py
│   ├── cli.py               # CLI entry point (argparse)
│   ├── core/
│   │   ├── __init__.py
│   │   ├── scanner.py       # Find emoji that need rectification
│   │   ├── rectifier.py     # Apply fixes (variation selectors + substitutions)
│   │   ├── rules.py         # Rectification rules engine
│   │   └── unicode_data.py  # Unicode character information
│   ├── rules/               # Rule definitions
│   │   ├── __init__.py
│   │   ├── arrows.py        # Arrow rectification rules
│   │   ├── checks.py        # Checkmark/X rectification rules
│   │   └── stars.py         # Star rectification rules
│   └── utils/
│       ├── __init__.py
│       ├── file_ops.py      # File discovery and processing
│       └── output.py        # Reporting and formatting
├── config/                  # Configuration files
│   ├── rectify.json         # Default rectification rules
│   └── emoji-data.txt       # Unicode emoji data (optional)
├── tests/
│   ├── __init__.py
│   ├── test_scanner.py
│   ├── test_rectifier.py
│   └── fixtures/
│       └── sample.md        # Test files with emoji
└── docs/
    ├── UNICODE-ARROWS.md    # (existing)
    ├── PLAN.md             # This file
    └── RULES.md            # Rule definition guide (future)
```

## Commands

```bash
# Scan mode: Find emoji that need fixing
emoji-rectifier scan <path> [--report] [--format json|text]

# Rectify mode: Fix emoji (preview by default)
emoji-rectifier rectify <path> [--rules arrows,checks,stars] [--dry-run] [--in-place]

# Verify mode: Check that files have proper text-style characters
emoji-rectifier verify <path>
```

## Rectification Rules

### 1. Arrows (arrows.py)

**Strategy**: Add U+FE0E variation selector to force text style

```python
ARROW_RULES = {
    # Basic arrows - add VS15 if missing
    '→': '→\uFE0E',   # Right arrow
    '←': '←\uFE0E',   # Left arrow
    '↑': '↑\uFE0E',   # Up arrow
    '↓': '↓\uFE0E',   # Down arrow
    '↔': '↔\uFE0E',   # Left-right arrow
    '↕': '↕\uFE0E',   # Up-down arrow

    # Heavy arrows - add VS15
    '⬆': '⬆\uFE0E',
    '⬇': '⬇\uFE0E',
    '⬅': '⬅\uFE0E',
    '➡': '➡\uFE0E',

    # Diagonal arrows
    '↖': '↖\uFE0E',
    '↗': '↗\uFE0E',
    '↘': '↘\uFE0E',
    '↙': '↙\uFE0E',

    # Emoji arrows - replace with text equivalents
    '🔼': '▲\uFE0E',
    '🔽': '▼\uFE0E',
    '⏫': '⬆\uFE0E',
    '⏬': '⬇\uFE0E',
}
```

### 2. Checkmarks and Xes (checks.py)

**Strategy**: Replace emoji versions with clean text equivalents

```python
CHECK_RULES = {
    # Emoji checkmarks → text checkmarks
    '✅': '✓\uFE0E',   # Heavy check → light check
    '☑': '✓\uFE0E',    # Ballot box with check → light check
    '✔': '✓\uFE0E',    # Heavy check → light check

    # Emoji Xes → text Xes
    '❌': '✗\uFE0E',   # Cross mark → multiplication X
    '❎': '✗\uFE0E',   # Cross mark button → multiplication X
    '✖': '✗\uFE0E',    # Heavy multiplication → light X

    # Alternative approaches (configurable):
    # '✅': '[x]',     # ASCII style
    # '❌': '[ ]',
}
```

### 3. Stars (stars.py)

**Strategy**: Replace gaudy stars with tasteful alternatives

```python
STAR_RULES = {
    # Gaudy emoji stars → tasteful text stars
    '⭐': '★\uFE0E',   # Star → black star with VS15
    '✨': '*',         # Sparkles → simple asterisk
    '🌟': '☆\uFE0E',   # Glowing star → white star
    '💫': '✦\uFE0E',   # Dizzy → four-pointed star
    '⚡': '⚡\uFE0E',   # High voltage → with VS15

    # Keep it simple and tasteful
    '🌠': '·',         # Shooting star → middot
}
```

## Smart Features

### 1. Idempotency

Running rectification twice produces the same result:

```python
def is_already_text_style(text: str, pos: int) -> bool:
    """Check if character already has VS15."""
    return (pos + 1 < len(text) and text[pos + 1] == '\uFE0E')

def add_variation_selector(text: str, char: str) -> str:
    """Only add VS15 if not already present."""
    # Smart replacement that checks context
    result = []
    i = 0
    while i < len(text):
        if text[i] == char:
            if not is_already_text_style(text, i):
                result.append(char + '\uFE0E')
            else:
                result.append(text[i:i+2])  # char + VS15
                i += 1
        else:
            result.append(text[i])
        i += 1
    return ''.join(result)
```

### 2. Context Awareness

Optional: Skip emoji in certain contexts (configurable)

```python
# Could add allowlist patterns:
# - Emoji at start of headings
# - Emoji in code blocks
# - Emoji in specific comment styles
```

### 3. Detailed Reporting

Show what was changed:

```
myfile.md:42:  → → →︎  (added variation selector)
myfile.md:87:  ✅ → ✓︎  (replaced emoji checkmark)
myfile.md:103: ⭐ → ★︎  (replaced star emoji)

Summary:
  Files scanned: 15
  Files changed: 8
  Arrows fixed: 42
  Checks fixed: 15
  Stars fixed: 7
```

## Configuration Format (config/rectify.yaml)

```yaml
# emoji-rectifier Configuration
rules:
  # ARROWS - Always use text arrows, not goofy emoji arrows
  arrows:
    enabled: true
    mode: variation-selector
    description: Add U+FE0E variation selector to force text-style rendering
    mappings:
      "→": "→\uFE0E"  # U+2192 RIGHTWARDS ARROW
      "←": "←\uFE0E"  # U+2190 LEFTWARDS ARROW
      "↑": "↑\uFE0E"  # U+2191 UPWARDS ARROW
      "↓": "↓\uFE0E"  # U+2193 DOWNWARDS ARROW
      "🔼": "▲\uFE0E"  # Up-pointing triangle

  # CHECKMARKS & XES - Always use text marks, not awful emoji
  checks:
    enabled: true
    mode: substitute
    description: Replace emoji checkmarks and Xes with clean text equivalents
    mappings:
      "✅": "✓\uFE0E"  # Heavy check mark → light check
      "❌": "✗\uFE0E"  # Cross mark emoji → multiplication X

  # STARS - Use tasteful stars, not GAUDY emoji
  stars:
    enabled: true
    mode: substitute
    description: Replace gaudy emoji stars with tasteful text alternatives
    mappings:
      "⭐": "★\uFE0E"  # Star emoji → black star (classic)
      "✨": "*"        # Sparkles → simple asterisk (MOST TASTEFUL!)

# File types to process
file_types:
  - .md      # Markdown (primary target)
  - .txt     # Plain text

# Patterns to exclude from processing
exclude_patterns:
  - .git/*           # Git internals
  - node_modules/*   # JavaScript dependencies
  - .obsidian/*      # Obsidian vault metadata
```

**Note**: We use YAML instead of JSON because:
- Comments make config files self-documenting
- More Pythonic (matches pytest, pre-commit, GitHub Actions, etc.)
- Cleaner syntax with less punctuation noise
- Still just as easy to read/write as JSON

## Development Roadmap

### Phase 1: Foundation (MVP) ✓ IN PROGRESS

- [ ] Set up uv project structure
  - [ ] pyproject.toml with dependencies
  - [ ] Package directory structure
  - [ ] Entry point configuration
- [ ] Implement basic scanner
  - [ ] File discovery (reuse from POC)
  - [ ] Pattern matching
- [ ] Implement rectifier core
  - [ ] Variation selector support
  - [ ] Substitution engine
  - [ ] Idempotency checks
- [ ] Arrow rules + tests
  - [ ] Basic arrow rules
  - [ ] VS15 addition logic
  - [ ] Test suite

### Phase 2: Full Rectification

- [ ] Checkmark/X rules
  - [ ] Rule definitions
  - [ ] Tests
- [ ] Star rules
  - [ ] Rule definitions
  - [ ] Tests
- [ ] Dry-run and in-place modes
  - [ ] Preview mode (default)
  - [ ] --in-place flag
  - [ ] Backup mechanism (optional)
- [ ] Reporting
  - [ ] Human-readable output
  - [ ] JSON output
  - [ ] Summary statistics

### Phase 3: Polish

- [ ] Verify command
  - [ ] Check for emoji that should be rectified
  - [ ] Exit codes for CI
- [ ] Configuration file support
  - [ ] Load custom rules
  - [ ] Override defaults
- [ ] Documentation
  - [ ] README with examples
  - [ ] RULES.md guide
  - [ ] CLI help text
- [ ] CI integration
  - [ ] GitHub Actions example
  - [ ] Pre-commit hook example

## Testing Strategy

```python
# Test idempotency
def test_idempotency():
    text = "Arrow: →"
    assert rectify(rectify(text)) == rectify(text)

# Test variation selectors
def test_variation_selector_added():
    result = rectify('→')
    assert '→\uFE0E' in result
    assert result.encode('utf-8') == b'\xe2\x86\x92\xef\xb8\x8e'

# Test substitution
def test_checkmark_substitution():
    result = rectify('✅')
    assert '✓' in result
    assert '✅' not in result

# Test mixed content
def test_mixed_emoji():
    text = "Steps: → ✅ ⭐"
    result = rectify(text)
    assert '→\uFE0E' in result
    assert '✓' in result
    assert ('★' in result or '*' in result)

# Test idempotency with already-rectified content
def test_already_rectified():
    text = "→\uFE0E"  # Already has VS15
    result = rectify(text)
    # Should not add another VS15
    assert text.count('\uFE0E') == result.count('\uFE0E')
```

## Key Differences from emoji-sniper POC

1. **Positive framing**: "Rectify" (fix) instead of "snipe" (remove)
2. **Variation selector support**: Smart addition of U+FE0E to preserve characters
3. **Rule-based system**: Organized by category (arrows, checks, stars)
4. **Idempotent**: Running twice won't add duplicate variation selectors
5. **Verification mode**: Check that files are properly rectified
6. **Clearer semantics**: Focus on making text more readable, not just banning

## Why This Approach is Superior

1. **Preserves Intent**: Using variation selectors keeps the semantic meaning
2. **Standards-Based**: Follows Unicode TR51 recommendations
3. **Reversible**: Could theoretically add U+FE0F to go back (though we won't!)
4. **Tasteful**: Maintains professional appearance in technical docs
5. **Extensible**: Easy to add new rule categories
6. **Idempotent**: Safe to run multiple times
7. **Educational**: Helps developers understand Unicode properly

## Progress Tracking

- **Phase 1 Started**: [Current Date]
- **MVP Target**: TBD
- **Full Release**: TBD

## References

- [UNICODE-ARROWS.md](UNICODE-ARROWS.md) - Variation selector deep dive
- [Unicode TR51](https://www.unicode.org/reports/tr51/) - Emoji specification
- [emoji-sniper POC](../old-ideas/) - Original concept
- [obsidian-tag-tools](https://github.com/pborenstein/obsidian-tag-tools) - Reference structure

---

**Status**: Phase 1 in progress
**Last Updated**: 2025-11-05
