# © 2026 aiaiaiai · aiaiaiai.org
# SPDX-License-Identifier: MIT
"""Regression tests for Mind Protocol 0.8 conformance modes."""

from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

from validate_conformance import (  # noqa: E402
    build_manifest,
    compatibility_probe_errors,
    consumer_module_errors,
    run_mode,
)
from validate_manifest import load_yaml_mapping  # noqa: E402


class ConformanceSuiteTests(unittest.TestCase):
    def test_both_consumer_modes_pass(self) -> None:
        for mode in ("schema", "minimal"):
            result = run_mode(mode)
            self.assertEqual(result["status"], "pass", result["errors"])
            self.assertEqual(
                result["fixtures"],
                ["person", "organization", "agent", "project", "product"],
            )

    def test_unknown_optional_and_required_module_policy(self) -> None:
        suite = load_yaml_mapping(ROOT / "conformance.yaml")
        manifest = build_manifest(suite["fixtures"]["person"], suite["protocol"])
        self.assertEqual(compatibility_probe_errors(manifest), [])

        candidate = copy.deepcopy(manifest)
        candidate["modules"]["registered"].append("future_extension")
        candidate["modules"]["required"].append("future_extension")
        candidate["modules"]["catalog"]["future_extension"] = "future_extension/module.yaml"
        candidate["loading"]["default"].append("future_extension")
        self.assertTrue(consumer_module_errors(candidate))


if __name__ == "__main__":
    unittest.main()
