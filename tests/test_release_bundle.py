# © 2026 aiaiaiai · aiaiaiai.org
# SPDX-License-Identifier: MIT
"""Regression coverage for deterministic formal Mind Protocol release packaging."""

from __future__ import annotations

import hashlib
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

from build_release_bundle import (  # noqa: E402
    build_release_bundle,
    check_release_bundle,
    protocol_version,
)


class ReleaseBundleTests(unittest.TestCase):
    def test_release_bundle_check_passes(self) -> None:
        self.assertEqual(check_release_bundle(), [])

    def test_release_bundle_is_byte_stable(self) -> None:
        version = protocol_version()
        with tempfile.TemporaryDirectory() as first_dir, tempfile.TemporaryDirectory() as second_dir:
            first = Path(first_dir) / "release.zip"
            second = Path(second_dir) / "release.zip"
            build_release_bundle(first, expected_version=version)
            build_release_bundle(second, expected_version=version)
            self.assertEqual(first.read_bytes(), second.read_bytes())
            self.assertEqual(
                hashlib.sha256(first.read_bytes()).hexdigest(),
                hashlib.sha256(second.read_bytes()).hexdigest(),
            )

    def test_bundle_contains_release_and_baseline_contracts(self) -> None:
        version = protocol_version()
        prefix = f"mind-protocol-v{version}/"
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "release.zip"
            build_release_bundle(output, expected_version=version)
            with zipfile.ZipFile(output, "r") as archive:
                entries = set(archive.namelist())
            self.assertIn(prefix + "protocol.yaml", entries)
            self.assertIn(prefix + "conformance.yaml", entries)
            self.assertIn(prefix + "compatibility.yaml", entries)
            self.assertIn(prefix + "migration-guide.md", entries)
            self.assertIn(prefix + "release-notes.md", entries)
            self.assertIn(prefix + "release-manifest.json", entries)
            self.assertIn(prefix + "neutral-baseline/baseline.json", entries)
            self.assertIn(prefix + "neutral-baseline/compatibility.yaml", entries)

    def test_expected_version_mismatch_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "release.zip"
            with self.assertRaisesRegex(ValueError, "does not match protocol.yaml"):
                build_release_bundle(output, expected_version="9.9.9")


if __name__ == "__main__":
    unittest.main()
