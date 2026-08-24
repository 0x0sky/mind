# © 2026 aiaiaiai · aiaiaiai.org
# SPDX-License-Identifier: MIT
"""Regression tests for strict SemVer 2.0 protocol precedence."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

from semver import SemVer, compare_semver  # noqa: E402


class SemVerTests(unittest.TestCase):
    def test_release_candidate_precedes_stable_release(self) -> None:
        self.assertLess(compare_semver("1.0.0-rc.1", "1.0.0"), 0)

    def test_later_release_candidate_has_greater_precedence(self) -> None:
        self.assertGreater(compare_semver("1.0.0-rc.2", "1.0.0-rc.1"), 0)

    def test_build_metadata_does_not_change_precedence(self) -> None:
        self.assertEqual(compare_semver("1.0.0+build.1", "1.0.0+build.2"), 0)
        self.assertEqual(
            compare_semver("1.0.0-rc.1+build.1", "1.0.0-rc.1+build.2"),
            0,
        )

    def test_numeric_and_lexical_prerelease_rules_match_semver(self) -> None:
        ordered = [
            "1.0.0-alpha",
            "1.0.0-alpha.1",
            "1.0.0-alpha.beta",
            "1.0.0-beta",
            "1.0.0-beta.2",
            "1.0.0-beta.11",
            "1.0.0-rc.1",
            "1.0.0",
        ]
        for left, right in zip(ordered, ordered[1:]):
            with self.subTest(left=left, right=right):
                self.assertLess(compare_semver(left, right), 0)

    def test_invalid_prerelease_identifiers_are_rejected(self) -> None:
        invalid = (
            "1.0.0-01",
            "1.0.0-alpha.01",
            "01.0.0",
            "1.01.0",
            "1.0.01",
            "1.0.0-",
            "1.0.0-alpha..1",
        )
        for version in invalid:
            with self.subTest(version=version):
                with self.assertRaises(ValueError):
                    SemVer.parse(version)

    def test_build_numeric_identifiers_may_have_leading_zeroes(self) -> None:
        parsed = SemVer.parse("1.0.0-rc.1+build.001")
        self.assertEqual(parsed.build, ("build", "001"))


if __name__ == "__main__":
    unittest.main()
