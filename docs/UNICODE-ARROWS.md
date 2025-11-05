# Unicode Arrow Glyphs vs Emoji

## The Problem

Some Unicode characters have **two visual representations**:
1. **Text style** - Simple, monochrome glyph (what fonts like Helvetica provide)
2. **Emoji style** - Colorful, rounded emoji version

By default, many rendering systems choose the emoji version, which looks out of place in technical documentation.

## The Solution: Variation Selectors

Unicode provides **Variation Selectors** to explicitly request one style or another:

- **U+FE0E (VS15)** - Force text/glyph presentation: `︎` (invisible character)
- **U+FE0F (VS16)** - Force emoji presentation: `️` (invisible character)

## How to Use

Add the variation selector immediately after the character:

```markdown
# Without variation selector (may render as emoji):
↕ ↔ ↑ ↓ ← →

# With VS15 (forces text/glyph style):
↕︎ ↔︎ ↑︎ ↓︎ ←︎ →︎
```

In your editor, you won't see the variation selector (it's invisible), but the rendering engine will use it to choose the correct style.

## Which Characters Need This?

Not all Unicode characters have dual presentation. To find out:

### 1. Check the Unicode Standard
- **Emoji specification**: [Unicode TR51](https://www.unicode.org/reports/tr51/)
- **Emoji data file**: https://www.unicode.org/Public/UCD/latest/ucd/emoji/emoji-data.txt
- Look for characters with `Emoji_Presentation` property

### 2. Common Characters That Need VS15 in Technical Docs

**Arrows:**
- `↕︎` U+2195 (up-down arrow)
- `↔︎` U+2194 (left-right arrow)
- `↖︎` `↗︎` `↘︎` `↙︎` (diagonal arrows)
- `↑︎` `↓︎` `←︎` `→︎` (directional arrows)
- `⬆︎` `⬇︎` `⬅︎` `➡︎` (heavy arrows)

**Symbols:**
- `☀︎` `☁︎` `☂︎` (weather)
- `★︎` `☆︎` (stars)
- `✓︎` `✗︎` (check marks)
- `☎︎` `✉︎` (communication)

### 3. Quick Test Method

To check if a character needs a variation selector:

1. Type the character in different contexts (markdown, HTML, your editor)
2. If it sometimes appears as a colorful emoji and sometimes as a simple glyph, it has dual presentation
3. Add VS15 (`U+FE0E`) to force text style

### 4. Programmatic Check

You can check the Unicode emoji data file:

```bash
# Download the emoji data (Unicode 16.0, latest as of 2024)
curl https://www.unicode.org/Public/UCD/latest/ucd/emoji/emoji-data.txt > emoji-data.txt

# Check if a character (e.g., U+2195) has Emoji_Presentation
grep "2195" emoji-data.txt
```

If you see `Emoji_Presentation`, the character may render as emoji by default.

## Tools and Resources

**Official Unicode Documentation:**
- [Unicode Technical Standard #51 - Emoji](https://www.unicode.org/reports/tr51/)
- [Emoji Variation Sequences](https://www.unicode.org/reports/tr51/#Emoji_Variation_Sequences)
- [Variation Selectors FAQ](https://www.unicode.org/faq/vs.html)

**Online Tools:**
- [Unicode Character Inspector](https://unicode-explorer.com/)
- [Emojipedia](https://emojipedia.org/) - Shows both text and emoji versions
- [FileFormat.info](https://www.fileformat.info/info/unicode/) - Detailed character info

**Editor Support:**
- Most modern editors show variation selectors as invisible
- Some editors have "show invisibles" mode that reveals them
- To type VS15: Copy from this doc or use hex input (depends on OS/editor)

## How to See U+FE0E (The Invisible Character)

Variation selectors are invisible by design, which makes them tricky to work with.

### Using Command-Line Tools

```bash
# View hex bytes
echo "↕︎" | xxd
# Output: e28695 efb88e (U+2195 followed by U+FE0E)

# More readable format
echo "↕︎" | od -An -tx1 -tc
# Shows both hex and character representation

# Count actual characters (will show 2: arrow + VS)
echo "↕︎" | wc -m

# Check files for variation selectors
grep "↕" docs/TABLES.md | xxd | less
```

### In less/Pagers

`less` doesn't have a built-in "show invisibles" mode:

```bash
# Pre-process to show hex codes
cat file.md | od -An -tx1c | less

# Use hexdump for detailed view
xxd file.md | less

# Search for the byte sequence (EF B8 8E in UTF-8)
xxd file.md | grep "efb88e"
```

### In Text Editors

**Vim:**
```vim
:set list                    " Show some invisible characters
" Position cursor on character and press:
ga                           " Shows Unicode code point (e.g., <U+FE0E>)
```

**VS Code:**
- Install "Unicode code point of current character" extension
- Or use "Insert Unicode" extension to see/insert characters

**Emacs:**
```elisp
M-x describe-char           " Shows full Unicode info at point
```

## How to Type U+FE0E

### Method 1: Copy-Paste (Easiest)

Copy this variation selector: `︎` (between quotes: "︎")

Or copy from existing text:
```
↕︎ ↔︎ ↑︎ ↓︎ ←︎ →︎
```

### Method 2: Shell/Scripts

```bash
# Using printf
printf '\uFE0E'

# Using echo (with -e flag)
echo -e '\uFE0E'

# Combine with arrow
printf '↕\uFE0E'

# Create a file with text-style arrows
printf '↕\uFE0E ↔\uFE0E ↑\uFE0E ↓\uFE0E ←\uFE0E →\uFE0E\n' > arrows.txt
```

### Method 3: OS-Specific Input

**macOS:**
- Open Character Viewer (Ctrl+Cmd+Space)
- Search for "variation selector"
- Double-click to insert

Or use Unicode hex input:
1. Enable "Unicode Hex Input" in System Preferences > Keyboard > Input Sources
2. Hold Option and type: `FE0E`
3. Release Option

**Linux (GTK apps):**
```
Ctrl+Shift+U, then type: fe0e, then Enter
```

**Windows:**
- Use Character Map utility and search for "variation selector"
- Or in some apps: type `FE0E` then Alt+X

### Method 4: In Text Editors

**Vim:**
```vim
" In insert mode:
Ctrl+V u FE0E
" or for full 6-digit code:
Ctrl+V U 0000FE0E
```

**Emacs:**
```
C-x 8 RET FE0E RET
```

**VS Code / Most Modern Editors:**
- Install Unicode input extension
- Or copy-paste from this document

## Testing Variation Selectors

### Quick Visual Test

```bash
#!/bin/bash
# test-variation-selectors.sh

echo "Without VS15 (may show emoji):"
echo "↕ ↔ ↑ ↓ ← →"
echo

echo "With VS15 (should show text glyph):"
printf "↕\uFE0E ↔\uFE0E ↑\uFE0E ↓\uFE0E ←\uFE0E →\uFE0E\n"
echo

echo "Hex dump of arrow with VS15:"
printf "↕\uFE0E" | xxd
```

### Verification in Files

```bash
# Find arrows that may need VS15
grep -n "↕\|↔\|↑\|↓\|←\|→" docs/*.md

# Check if VS15 is present (look for EF B8 8E bytes)
grep "↕" docs/TABLES.md | xxd | grep "efb88e"

# Count variation selectors in a file
grep -o $'\uFE0E' file.md | wc -l
```

### Test Rendering in Browser

Create a simple HTML file:

```html
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: Helvetica, Arial, sans-serif; font-size: 24px; }
        .emoji { font-family: "Apple Color Emoji", "Segoe UI Emoji"; }
    </style>
</head>
<body>
    <h2>Without VS15 (default rendering):</h2>
    <p>↕ ↔ ↑ ↓ ← →</p>

    <h2>With VS15 (text style forced):</h2>
    <p>↕︎ ↔︎ ↑︎ ↓︎ ←︎ →︎</p>

    <h2>With emoji font (for comparison):</h2>
    <p class="emoji">↕ ↔ ↑ ↓ ← →</p>
</body>
</html>
```

## Practical Tips

1. **Copy from existing files**: The easiest workflow is to copy arrows with VS15 from files where they're already correct (like `docs/TABLES.md`)

2. **Use search & replace carefully**: When doing bulk edits, be careful not to add VS15 twice:
   ```bash
   # BAD: This could add VS15 to arrows that already have it
   sed 's/↕/↕\xEF\xB8\x8E/g' file.md

   # BETTER: Check first, edit manually or with a smarter script
   ```

3. **Verify in target environment**: Test how arrows render in your actual use case (GitHub, browser, PDF, etc.)

4. **Document for collaborators**: If others will edit these files, add a note in CONTRIBUTING.md about variation selectors

## Implementation in This Project

All arrow characters in our reference tables use VS15 to ensure consistent text rendering:

```markdown
| select  | ^B 0-9 | — | ^B ↑︎↓︎←︎→︎ | select |
| split ↕︎ | ^B "   | — | —         | split ↕︎ |
| split ↔︎ | ^B %   | — | —         | split ↔︎ |
```

This ensures documentation renders correctly in:
- GitHub Markdown
- Web browsers
- Terminal pagers
- PDF exports
- Any system that respects Unicode variation selectors
