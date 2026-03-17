"""autonomous_patch_generation/simulation/pre_flight_simulator — pre-check."""
from __future__ import annotations

import ast
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

log = logging.getLogger(__name__)


@dataclass
class SimulationResult:
    """Result of a pre-flight simulation on a generated patch."""

    patch_id: str
    safe_to_apply: bool
    issues: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    risk_score: float = 0.0    # 0 = safe, 1 = very risky


class PreFlightSimulator:
    """Run lightweight checks on a patch before it is applied.

    Checks performed:
    * Diff is non-empty.
    * Added lines are syntactically valid Python.
    * Patch does not introduce obvious dangerous patterns.
    * Patch does not remove more than *max_deletions* lines.
    """

    _DANGEROUS_PATTERNS = [
        "eval(",
        "exec(",
        "os.system(",
        "__import__(",
        "subprocess.call(",
        "pickle.loads(",
    ]

    def __init__(self, max_deletions: int = 200) -> None:
        self._max_del = max_deletions

    def simulate(self, patch) -> SimulationResult:
        """Simulate *patch* (a :class:`GeneratedPatch`) and return result."""
        result = SimulationResult(patch_id=patch.patch_id, safe_to_apply=True)

        if not patch.diff.strip():
            result.safe_to_apply = False
            result.issues.append("Patch diff is empty")
            result.risk_score = 1.0
            return result

        added_lines, removed_lines = self._parse_diff(patch.diff)

        # Check deletion count
        if len(removed_lines) > self._max_del:
            result.issues.append(
                f"Too many deletions: {len(removed_lines)} > {self._max_del}"
            )
            result.safe_to_apply = False
            result.risk_score = 0.8

        # Syntax check added Python lines
        py_added = [l for l in added_lines if not l.startswith("#")]
        if py_added:
            joined = "\n".join(py_added)
            try:
                ast.parse(joined)
            except SyntaxError as exc:
                result.warnings.append(f"Syntax issue in added lines: {exc}")
                result.risk_score = max(result.risk_score, 0.5)

        # Dangerous pattern check
        for line in added_lines:
            for pat in self._DANGEROUS_PATTERNS:
                if pat in line:
                    result.warnings.append(
                        f"Dangerous pattern '{pat}' in added line"
                    )
                    result.risk_score = max(result.risk_score, 0.7)

        if result.issues:
            result.safe_to_apply = False
        return result

    @staticmethod
    def _parse_diff(diff: str) -> tuple:
        added, removed = [], []
        for line in diff.splitlines():
            if line.startswith("+") and not line.startswith("+++"):
                added.append(line[1:])
            elif line.startswith("-") and not line.startswith("---"):
                removed.append(line[1:])
        return added, removed
