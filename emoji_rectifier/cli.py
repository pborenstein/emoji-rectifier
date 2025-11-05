#!/usr/bin/env python3
"""
emoji-rectifier CLI

Make the world safe from emojimania by intelligently converting gaudy emoji
to tasteful text-style characters.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .core.rectifier import Rectifier
from .core.rules import RuleCategory, RuleEngine
from .core.scanner import Scanner
from .utils.file_ops import discover_files
from .utils.output import (
    format_rectify_results_json,
    format_rectify_results_text,
    format_scan_results_json,
    format_scan_results_text,
    print_summary,
)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        prog="emoji-rectifier",
        description="Make the world safe from emojimania. Convert gaudy emoji to tasteful text.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Scan files for emoji that need rectification
  emoji-rectifier scan docs/

  # Preview rectification (dry run)
  emoji-rectifier rectify docs/ --dry-run

  # Apply rectification to files
  emoji-rectifier rectify docs/ --in-place

  # Only fix arrows
  emoji-rectifier rectify docs/ --rules arrows --in-place

  # Verify files are rectified (for CI)
  emoji-rectifier verify docs/
""",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # scan command
    scan_parser = subparsers.add_parser(
        "scan",
        help="Scan files for emoji that need rectification",
    )
    _add_common_args(scan_parser)
    scan_parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text)",
    )

    # rectify command
    rectify_parser = subparsers.add_parser(
        "rectify",
        help="Rectify emoji in files (preview by default)",
    )
    _add_common_args(rectify_parser)
    rectify_parser.add_argument(
        "--dry-run",
        action="store_true",
        default=True,
        help="Preview changes without modifying files (default)",
    )
    rectify_parser.add_argument(
        "--in-place",
        action="store_true",
        help="Modify files in place (overrides --dry-run)",
    )
    rectify_parser.add_argument(
        "--backup",
        action="store_true",
        help="Create .bak backup files before modifying",
    )
    rectify_parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text)",
    )

    # verify command
    verify_parser = subparsers.add_parser(
        "verify",
        help="Verify files are properly rectified (exit 1 if issues found)",
    )
    _add_common_args(verify_parser)
    verify_parser.add_argument(
        "--quiet",
        "-q",
        action="store_true",
        help="Only output errors (for CI)",
    )

    return parser.parse_args(argv)


def _add_common_args(parser: argparse.ArgumentParser) -> None:
    """Add common arguments to a subcommand parser."""
    parser.add_argument(
        "path",
        type=Path,
        help="File or directory to process",
    )
    parser.add_argument(
        "--ext",
        default=".md,.txt",
        help="Comma-separated file extensions to process (default: .md,.txt)",
    )
    parser.add_argument(
        "--exclude",
        action="append",
        default=[],
        help="Patterns to exclude (repeatable)",
    )
    parser.add_argument(
        "--rules",
        default="arrows,checks,stars",
        help="Comma-separated rule categories to apply (default: arrows,checks,stars)",
    )


def run_scan(args: argparse.Namespace) -> int:
    """Run scan command."""
    # Parse arguments
    extensions = {ext.strip() for ext in args.ext.split(",") if ext.strip()}
    exclude_patterns = set(args.exclude) if args.exclude else set()

    # Add default excludes
    exclude_patterns.update({".git", "node_modules", ".obsidian"})

    # Parse rule categories
    enabled_categories = _parse_rule_categories(args.rules)

    # Discover files
    files = discover_files(
        args.path,
        extensions=extensions,
        exclude_patterns=exclude_patterns,
    )

    # Create scanner
    rule_engine = RuleEngine(enabled_categories)
    scanner = Scanner(rule_engine)

    # Scan files
    results = scanner.scan_files(files)

    # Calculate stats
    stats = scanner.get_stats(results)
    stats.files_scanned = len(files)

    # Output results
    if args.format == "json":
        output = format_scan_results_json(results, stats)
        print(json.dumps(output, indent=2, ensure_ascii=False))
    else:
        print(format_scan_results_text(results))
        print_summary(stats)

    # Exit with error if issues found
    return 1 if results else 0


def run_rectify(args: argparse.Namespace) -> int:
    """Run rectify command."""
    # Parse arguments
    extensions = {ext.strip() for ext in args.ext.split(",") if ext.strip()}
    exclude_patterns = set(args.exclude) if args.exclude else set()
    exclude_patterns.update({".git", "node_modules", ".obsidian"})

    # Parse rule categories
    enabled_categories = _parse_rule_categories(args.rules)

    # Determine if this is a dry run
    dry_run = not args.in_place

    # Discover files
    files = discover_files(
        args.path,
        extensions=extensions,
        exclude_patterns=exclude_patterns,
    )

    # Create rectifier
    rectifier = Rectifier(enabled_categories=enabled_categories)

    # Process files
    results = list(
        rectifier.process_files(
            files,
            dry_run=dry_run,
            create_backup=args.backup if hasattr(args, "backup") else False,
        )
    )

    # Calculate stats
    stats = rectifier.get_stats(results)

    # Output results
    if args.format == "json":
        output = format_rectify_results_json(results, stats)
        print(json.dumps(output, indent=2, ensure_ascii=False))
    else:
        print(format_rectify_results_text(results, dry_run=dry_run))
        print_summary(stats)

    return 0


def run_verify(args: argparse.Namespace) -> int:
    """Run verify command."""
    # Parse arguments
    extensions = {ext.strip() for ext in args.ext.split(",") if ext.strip()}
    exclude_patterns = set(args.exclude) if args.exclude else set()
    exclude_patterns.update({".git", "node_modules", ".obsidian"})

    # Parse rule categories
    enabled_categories = _parse_rule_categories(args.rules)

    # Discover files
    files = discover_files(
        args.path,
        extensions=extensions,
        exclude_patterns=exclude_patterns,
    )

    # Create scanner
    rule_engine = RuleEngine(enabled_categories)
    scanner = Scanner(rule_engine)

    # Scan files
    results = scanner.scan_files(files)

    # Output
    if not args.quiet:
        if results:
            print("FAILED: Files contain emoji that need rectification:")
            print(format_scan_results_text(results))
        else:
            print("PASSED: All files are properly rectified.")

    # Exit with error if issues found
    return 1 if results else 0


def _parse_rule_categories(rules_str: str) -> set[RuleCategory]:
    """Parse comma-separated rule categories string."""
    categories = set()

    for rule in rules_str.split(","):
        rule = rule.strip().lower()
        if rule == "arrows":
            categories.add(RuleCategory.ARROWS)
        elif rule == "checks":
            categories.add(RuleCategory.CHECKS)
        elif rule == "stars":
            categories.add(RuleCategory.STARS)

    return categories


def main(argv: list[str] | None = None) -> int:
    """Main entry point."""
    args = parse_args(argv)

    try:
        if args.command == "scan":
            return run_scan(args)
        elif args.command == "rectify":
            return run_rectify(args)
        elif args.command == "verify":
            return run_verify(args)
        else:
            print(f"Unknown command: {args.command}", file=sys.stderr)
            return 2
    except KeyboardInterrupt:
        print("\nInterrupted", file=sys.stderr)
        return 130
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
