# emoji-rectifier

**Make the world safe from emojimania.**

Intelligently convert gaudy emoji to tasteful text-style characters using Unicode variation selectors and smart substitutions.

## The Three Commandments

1. **Always use text arrows, not goofy emoji arrows** `→︎` not `🔼`
2. **Always use text checkmarks and Xes, not awful emoji** `✓︎` not `✅`
3. **Use tasteful stars, not GAUDY emoji** `★︎` or `*` not `⭐`

## What It Does

emoji-rectifier converts emoji to their proper text representations by:

- **Adding variation selectors** (U+FE0E) to force text-style rendering for arrows and symbols
- **Substituting emoji** with clean text equivalents for checkmarks, Xes, and stars
- **Preserving semantics** while improving readability

### Before and After

```markdown
Before: Steps → ✅ Earn a ⭐ rating!
After:  Steps →︎ ✓︎ Earn a ★︎ rating!
```

The "after" version uses invisible Unicode variation selectors to force text-style rendering.

## Installation

Using [uv](https://github.com/astral-sh/uv) (recommended):

```bash
# Install in editable mode for development
uv tool install --editable .

# Or install normally
uv tool install .
```

Using pip:

```bash
pip install .
```

## Quick Start

```bash
# Scan files to see what needs fixing
emoji-rectifier scan docs/

# Preview rectification (dry run)
emoji-rectifier rectify docs/ --dry-run

# Apply rectification to files
emoji-rectifier rectify docs/ --in-place

# Verify files are properly rectified (exit 1 if issues found)
emoji-rectifier verify docs/
```

## Commands

### scan

Find emoji that need rectification:

```bash
emoji-rectifier scan <path> [options]
```

**Options:**
- `--format {text,json}` - Output format (default: text)
- `--ext .md,.txt` - File extensions to scan
- `--exclude PATTERN` - Patterns to exclude (repeatable)
- `--rules arrows,checks,stars` - Which rules to check

**Example:**
```bash
# Scan markdown files, exclude node_modules
emoji-rectifier scan . --ext .md --exclude node_modules
```

### rectify

Fix emoji in files:

```bash
emoji-rectifier rectify <path> [options]
```

**Options:**
- `--dry-run` - Preview changes without modifying files (default)
- `--in-place` - Modify files in place (overrides --dry-run)
- `--backup` - Create .bak backup files before modifying
- `--format {text,json}` - Output format
- `--ext .md,.txt` - File extensions to process
- `--exclude PATTERN` - Patterns to exclude
- `--rules arrows,checks,stars` - Which rules to apply

**Examples:**
```bash
# Preview rectification
emoji-rectifier rectify docs/ --dry-run

# Apply fixes to markdown files only
emoji-rectifier rectify . --in-place --ext .md

# Only fix arrows
emoji-rectifier rectify docs/ --in-place --rules arrows

# Create backups before modifying
emoji-rectifier rectify docs/ --in-place --backup
```

### verify

Verify files are properly rectified (useful for CI):

```bash
emoji-rectifier verify <path> [options]
```

**Options:**
- `--quiet` - Only output errors
- `--ext .md,.txt` - File extensions to check
- `--exclude PATTERN` - Patterns to exclude
- `--rules arrows,checks,stars` - Which rules to verify

**Example:**
```bash
# In CI/pre-commit hook
emoji-rectifier verify docs/ --quiet
if [ $? -ne 0 ]; then
  echo "Files contain unrectified emoji!"
  exit 1
fi
```

## Rectification Rules

### Arrows

Adds U+FE0E (variation selector 15) to force text-style rendering:

- `→` → `→︎` (with invisible VS15)
- `←` → `←︎`
- `↑` → `↑︎`
- `↓` → `↓︎`
- `⬆` → `⬆︎`

Replaces emoji-only arrows with text equivalents:

- `🔼` → `▲︎`
- `🔽` → `▼︎`
- `⏩` → `➡︎`

### Checkmarks and Xes

Replaces emoji versions with clean text equivalents:

- `✅` → `✓︎` (light check mark)
- `❌` → `✗︎` (multiplication X)
- `☑` → `✓︎`
- `✖` → `✗︎`

### Stars

Replaces gaudy emoji stars with tasteful alternatives:

- `⭐` → `★︎` (black star with VS15)
- `✨` → `*` (simple asterisk - most tasteful!)
- `🌟` → `☆︎` (white star)
- `💫` → `✦︎` (four-pointed star)

## Configuration

Default configuration is in `config/rectify.json`. You can customize:

- Which rules are enabled
- Substitution mappings
- File types to process
- Exclude patterns

See [docs/PLAN.md](docs/PLAN.md) for details.

## How It Works

### Variation Selectors

Many Unicode characters have **dual presentation**:
- **Default**: Often renders as colorful emoji
- **U+FE0E (VS15)**: Forces text/glyph style (monochrome)
- **U+FE0F (VS16)**: Forces emoji style

Example:
```
→      (U+2192, may render as emoji)
→︎     (U+2192 + U+FE0E, forced text style)
```

The variation selector is invisible but tells rendering engines to use text style.

See [docs/UNICODE-ARROWS.md](docs/UNICODE-ARROWS.md) for a deep dive.

### Idempotency

emoji-rectifier is **idempotent** - running it multiple times produces the same result:

```python
rectify(rectify(text)) == rectify(text)  # Always true!
```

It won't add duplicate variation selectors or re-replace already-rectified content.

## Development

```bash
# Set up development environment
uv sync

# Run tests
uv run pytest

# Run with coverage
uv run pytest --cov=emoji_rectifier

# Format code
uv run black emoji_rectifier tests

# Lint
uv run ruff check emoji_rectifier tests
```

## Testing

```bash
# Run all tests
uv run pytest -v

# Run specific test file
uv run pytest tests/test_arrows.py -v

# Test with the sample fixture
emoji-rectifier scan tests/fixtures/sample.md
emoji-rectifier rectify tests/fixtures/sample.md --dry-run
```

## Why?

Emoji have their place, but in technical documentation they often:
- Look unprofessional
- Render inconsistently across platforms
- Distract from the content
- Break visual flow

Text-style characters with variation selectors:
- Render consistently everywhere
- Look professional
- Maintain semantic meaning
- Respect Unicode standards

**Make documentation great again.** Tastefully.

## References

- [Unicode Technical Report #51 (Emoji)](https://www.unicode.org/reports/tr51/)
- [Variation Selectors](https://www.unicode.org/faq/vs.html)
- [docs/UNICODE-ARROWS.md](docs/UNICODE-ARROWS.md) - Deep dive on variation selectors
- [docs/PLAN.md](docs/PLAN.md) - Project plan and architecture

## License

MIT

## Credits

Inspired by the eternal struggle against emojimania in technical writing.

Built with Python 3.10+ and [uv](https://github.com/astral-sh/uv).
