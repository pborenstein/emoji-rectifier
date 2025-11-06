"""Output formatting for scan and rectify results."""

from __future__ import annotations

import json
from typing import Any

from ..core.rectifier import RectificationResult, RectificationStats
from ..core.scanner import ScanResult, ScanStats


def format_scan_results_text(results: list[ScanResult]) -> str:
    """
    Format scan results as human-readable text.

    Args:
        results: List of scan results

    Returns:
        Formatted text
    """
    if not results:
        return "No files need rectification. All clear!"

    lines = []
    lines.append("Files with emoji that need rectification:\n")

    # Group by file
    by_file: dict[str, list[ScanResult]] = {}
    for result in results:
        key = str(result.file_path)
        if key not in by_file:
            by_file[key] = []
        by_file[key].append(result)

    for file_path, file_results in sorted(by_file.items()):
        lines.append(f"\n{file_path}:")
        for result in file_results:
            # Show line number and preview of content
            preview = result.line_content[:80]
            if len(result.line_content) > 80:
                preview += "..."
            lines.append(f"  Line {result.line_number}: {preview}")

    return "\n".join(lines)


def format_scan_results_json(results: list[ScanResult], stats: ScanStats) -> dict[str, Any]:
    """
    Format scan results as JSON.

    Args:
        results: List of scan results
        stats: Scan statistics

    Returns:
        Dictionary ready for JSON serialization
    """
    return {
        "stats": {
            "files_scanned": stats.files_scanned,
            "files_with_issues": stats.files_with_issues,
            "lines_with_issues": stats.total_lines_with_issues,
        },
        "results": [
            {
                "file": str(r.file_path),
                "line": r.line_number,
                "content": r.line_content,
            }
            for r in results
        ],
    }


def format_rectify_results_text(results: list[RectificationResult], dry_run: bool = True) -> str:
    """
    Format rectification results as human-readable text.

    Args:
        results: List of rectification results
        dry_run: Whether this was a dry run

    Returns:
        Formatted text
    """
    lines = []

    mode = "Preview" if dry_run else "Applied"
    lines.append(f"{mode} rectification:\n")

    modified = [r for r in results if r.was_modified]

    if not modified:
        lines.append("No changes needed. All files are already rectified!")
        return "\n".join(lines)

    for result in modified:
        lines.append(f"\n{result.file_path}:")

        # Show a diff preview (simplified)
        orig_lines = result.original_content.splitlines()
        rect_lines = result.rectified_content.splitlines()

        for i, (orig, rect) in enumerate(zip(orig_lines, rect_lines), start=1):
            if orig != rect:
                lines.append(f"  Line {i}:")
                lines.append(f"    - {orig}")
                lines.append(f"    + {rect}")

    return "\n".join(lines)


def format_rectify_results_json(
    results: list[RectificationResult],
    stats: RectificationStats,
) -> dict[str, Any]:
    """
    Format rectification results as JSON.

    Args:
        results: List of rectification results
        stats: Rectification statistics

    Returns:
        Dictionary ready for JSON serialization
    """
    return {
        "stats": {
            "files_scanned": stats.files_scanned,
            "files_modified": stats.files_modified,
            "total_changes": stats.total_changes,
            "errors": stats.errors,
        },
        "results": [
            {
                "file": str(r.file_path),
                "was_modified": r.was_modified,
                "changes_made": r.changes_made,
                "line_count": r.line_count,
            }
            for r in results
            if r.was_modified
        ],
    }


def print_summary(stats: RectificationStats | ScanStats) -> None:
    """
    Print a summary of statistics.

    Args:
        stats: Statistics to print
    """
    if isinstance(stats, ScanStats):
        print(f"\nScan Summary:")
        print(f"  Files scanned: {stats.files_scanned}")
        print(f"  Files with issues: {stats.files_with_issues}")
        print(f"  Lines with issues: {stats.total_lines_with_issues}")
    elif isinstance(stats, RectificationStats):
        print(f"\nRectification Summary:")
        print(f"  Files scanned: {stats.files_scanned}")
        print(f"  Files modified: {stats.files_modified}")
        print(f"  Total changes: {stats.total_changes}")
        if stats.errors > 0:
            print(f"  Errors: {stats.errors}")
