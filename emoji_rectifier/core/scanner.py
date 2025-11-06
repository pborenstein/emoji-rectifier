"""Scanner for finding emoji that need rectification."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .rules import RuleEngine


@dataclass
class ScanResult:
    """Result of scanning a file for unrectified emoji."""
    file_path: Path
    line_number: int
    line_content: str
    needs_rectification: bool = False

    @property
    def relative_path(self) -> str:
        """Get relative path string for display."""
        return str(self.file_path)


@dataclass
class ScanStats:
    """Statistics from a scan run."""
    files_scanned: int = 0
    files_with_issues: int = 0
    total_lines_with_issues: int = 0


class Scanner:
    """
    Scanner for finding emoji that need rectification.
    """

    def __init__(self, rule_engine: RuleEngine | None = None):
        """
        Initialize scanner.

        Args:
            rule_engine: Rule engine to use (creates default if None)
        """
        self.rule_engine = rule_engine or RuleEngine()

    def scan_file(self, file_path: Path, encoding: str = "utf-8") -> list[ScanResult]:
        """
        Scan a file for unrectified emoji.

        Args:
            file_path: Path to file
            encoding: File encoding

        Returns:
            List of ScanResult for lines that need rectification
        """
        results = []

        try:
            content = file_path.read_text(encoding=encoding)
            lines = content.splitlines()

            for line_num, line in enumerate(lines, start=1):
                if self.rule_engine.needs_rectification(line):
                    results.append(
                        ScanResult(
                            file_path=file_path,
                            line_number=line_num,
                            line_content=line,
                            needs_rectification=True,
                        )
                    )
        except Exception:
            # Skip files that can't be read
            pass

        return results

    def scan_text(self, text: str) -> bool:
        """
        Check if text needs rectification.

        Args:
            text: Input text

        Returns:
            True if text needs rectification
        """
        return self.rule_engine.needs_rectification(text)

    def scan_files(self, file_paths: list[Path]) -> list[ScanResult]:
        """
        Scan multiple files.

        Args:
            file_paths: List of file paths to scan

        Returns:
            Combined list of all scan results
        """
        all_results = []

        for file_path in file_paths:
            results = self.scan_file(file_path)
            all_results.extend(results)

        return all_results

    def get_stats(self, results: list[ScanResult]) -> ScanStats:
        """
        Calculate statistics from scan results.

        Args:
            results: List of scan results

        Returns:
            ScanStats
        """
        stats = ScanStats()
        stats.total_lines_with_issues = len(results)

        # Count unique files
        unique_files = {r.file_path for r in results}
        stats.files_with_issues = len(unique_files)

        return stats
