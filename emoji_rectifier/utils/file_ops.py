"""File discovery and operations."""

from __future__ import annotations

from pathlib import Path
from typing import Iterator


def discover_files(
    root_path: Path,
    *,
    extensions: set[str] | None = None,
    exclude_patterns: set[str] | None = None,
) -> list[Path]:
    """
    Discover files to process.

    Args:
        root_path: Root directory or single file path
        extensions: Set of extensions to include (e.g., {'.md', '.txt'})
        exclude_patterns: Set of patterns to exclude (simple substring matching)

    Returns:
        List of file paths to process
    """
    if extensions is None:
        extensions = {".md", ".txt"}

    if exclude_patterns is None:
        exclude_patterns = {".git", "node_modules", ".obsidian"}

    # Normalize extensions to include dot
    extensions = {ext if ext.startswith(".") else f".{ext}" for ext in extensions}

    files = []

    if root_path.is_file():
        # Single file
        if root_path.suffix in extensions:
            files.append(root_path)
    elif root_path.is_dir():
        # Directory - walk recursively
        for ext in extensions:
            for file_path in root_path.rglob(f"*{ext}"):
                # Check exclusions
                if should_exclude(file_path, exclude_patterns):
                    continue
                files.append(file_path)

    return sorted(files)


def should_exclude(file_path: Path, exclude_patterns: set[str]) -> bool:
    """
    Check if a file should be excluded.

    Args:
        file_path: File path to check
        exclude_patterns: Set of patterns to exclude

    Returns:
        True if file should be excluded
    """
    path_str = str(file_path)

    for pattern in exclude_patterns:
        if pattern in path_str:
            return True

    return False


def iter_files(
    root_path: Path,
    *,
    extensions: set[str] | None = None,
    exclude_patterns: set[str] | None = None,
) -> Iterator[Path]:
    """
    Iterate over files to process (lazy version).

    Args:
        root_path: Root directory or single file path
        extensions: Set of extensions to include
        exclude_patterns: Set of patterns to exclude

    Yields:
        File paths to process
    """
    for file_path in discover_files(root_path, extensions=extensions, exclude_patterns=exclude_patterns):
        yield file_path
