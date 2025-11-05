"""Main rectification engine.

Processes files and applies emoji rectification rules.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterator

from .rules import RuleCategory, RuleEngine


@dataclass
class RectificationResult:
    """Result of rectifying a single file."""
    file_path: Path
    original_content: str
    rectified_content: str
    was_modified: bool
    line_count: int = 0
    changes_made: int = 0

    @property
    def relative_path(self) -> str:
        """Get relative path string for display."""
        return str(self.file_path)


@dataclass
class RectificationStats:
    """Statistics from a rectification run."""
    files_scanned: int = 0
    files_modified: int = 0
    total_changes: int = 0
    errors: int = 0


class Rectifier:
    """
    Main rectifier that processes files and applies rules.
    """

    def __init__(
        self,
        enabled_categories: set[RuleCategory] | None = None,
        encoding: str = "utf-8",
    ):
        """
        Initialize the rectifier.

        Args:
            enabled_categories: Set of rule categories to enable
            encoding: File encoding to use (default: utf-8)
        """
        self.rule_engine = RuleEngine(enabled_categories)
        self.encoding = encoding

    def rectify_file(self, file_path: Path) -> RectificationResult:
        """
        Rectify a single file.

        Args:
            file_path: Path to file to rectify

        Returns:
            RectificationResult with original and rectified content
        """
        try:
            original = file_path.read_text(encoding=self.encoding)
        except Exception as e:
            # Return empty result on read error
            return RectificationResult(
                file_path=file_path,
                original_content="",
                rectified_content="",
                was_modified=False,
                line_count=0,
                changes_made=0,
            )

        rectified = self.rule_engine.rectify(original)
        was_modified = rectified != original

        # Count changes (simple char difference count)
        changes = 0
        if was_modified:
            # Count actual character differences
            changes = sum(1 for a, b in zip(original, rectified) if a != b)
            # Add difference in length
            changes += abs(len(rectified) - len(original))

        return RectificationResult(
            file_path=file_path,
            original_content=original,
            rectified_content=rectified,
            was_modified=was_modified,
            line_count=len(original.splitlines()),
            changes_made=changes,
        )

    def rectify_text(self, text: str) -> str:
        """
        Rectify text directly.

        Args:
            text: Input text

        Returns:
            Rectified text
        """
        return self.rule_engine.rectify(text)

    def needs_rectification(self, text: str) -> bool:
        """
        Check if text needs rectification.

        Args:
            text: Input text

        Returns:
            True if text would be modified
        """
        return self.rule_engine.needs_rectification(text)

    def apply_to_file(
        self,
        file_path: Path,
        *,
        dry_run: bool = True,
        create_backup: bool = False,
    ) -> RectificationResult:
        """
        Apply rectification to a file.

        Args:
            file_path: Path to file
            dry_run: If True, don't write changes (default: True)
            create_backup: If True, create .bak file before writing

        Returns:
            RectificationResult
        """
        result = self.rectify_file(file_path)

        if not dry_run and result.was_modified:
            # Create backup if requested
            if create_backup:
                backup_path = file_path.with_suffix(file_path.suffix + ".bak")
                backup_path.write_text(result.original_content, encoding=self.encoding)

            # Write rectified content
            file_path.write_text(result.rectified_content, encoding=self.encoding)

        return result

    def process_files(
        self,
        file_paths: list[Path],
        *,
        dry_run: bool = True,
        create_backup: bool = False,
    ) -> Iterator[RectificationResult]:
        """
        Process multiple files.

        Args:
            file_paths: List of file paths to process
            dry_run: If True, don't write changes
            create_backup: If True, create backups

        Yields:
            RectificationResult for each file
        """
        for file_path in file_paths:
            yield self.apply_to_file(
                file_path,
                dry_run=dry_run,
                create_backup=create_backup,
            )

    def get_stats(self, results: list[RectificationResult]) -> RectificationStats:
        """
        Calculate statistics from results.

        Args:
            results: List of rectification results

        Returns:
            RectificationStats
        """
        stats = RectificationStats()
        stats.files_scanned = len(results)
        stats.files_modified = sum(1 for r in results if r.was_modified)
        stats.total_changes = sum(r.changes_made for r in results)
        # Error detection could be improved
        stats.errors = sum(
            1 for r in results
            if not r.original_content and not r.rectified_content
        )

        return stats
