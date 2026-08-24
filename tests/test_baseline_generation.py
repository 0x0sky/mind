# © 2026 aiaiaiai · aiaiaiai.org
# SPDX-License-Identifier: MIT
"""Regression tests for the generated neutral baseline bundle."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

from generate_baseline import (  # noqa: E402
    check_baseline,
    generate_baseline,
    generated_manifest_errors,
    leakage_errors,
    snapshot,
)
from validate_manifest import load_yaml_mapping  # noqa: E402


class BaselineGenerationTests(unittest.TestCase):
    def test_generation_is_deterministic(self) -> None:
        with tempfile.TemporaryDirectory() as first_dir, tempfile.TemporaryDirectory() as second_dir:
            first = Path(first_dir) / "baseline"
            second = Path(second_dir) / "baseline"
            generate_baseline(first)
            generate_baseline(second)
            self.assertEqual(snapshot(first), snapshot(second))

    def test_generated_baseline_is_valid_and_instance_independent(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "baseline"
            generate_baseline(output)
            self.assertEqual(generated_manifest_errors(output), [])
            self.assertEqual(leakage_errors(output), [])
            manifest = load_yaml_mapping(output / "manifest.yaml")
            self.assertEqual(manifest["schema_version"], 3)
            self.assertEqual(
                manifest["mind"]["subject"],
                {"type": "unspecified", "id": "unspecified"},
            )
            self.assertNotIn("kind", manifest["mind"])
            self.assertNotIn("public_organizations", manifest)
            self.assertEqual(manifest["modules"]["registered"], [])
            self.assertTrue((output / "compatibility.yaml").is_file())
            readme = (output / "README.md").read_text(encoding="utf-8")
            self.assertIn("not a concrete Mind", readme)
            self.assertIn("subject: unspecified", readme)

    def test_full_baseline_check_passes(self) -> None:
        self.assertEqual(check_baseline(), [])


if __name__ == "__main__":
    unittest.main()
