# © 2026 aiaiaiai · aiaiaiai.org
# SPDX-License-Identifier: MIT
"""Regression tests for Mind Protocol conformance modes."""

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
    consumer_module_errors,
    range_errors,
    run_mode,
)
from validate_manifest import load_yaml_mapping  # noqa: E402


class ConformanceSuiteTests(unittest.TestCase):
    def test_both_consumer_modes_pass_with_declared_probes(self) -> None:
        suite = load_yaml_mapping(ROOT / "conformance.yaml")
        for mode in ("schema", "minimal"):
            result = run_mode(mode)
            self.assertEqual(result["status"], "pass", result["errors"])
            self.assertEqual(
                result["fixtures"],
                ["person", "organization", "agent", "project", "product"],
            )
            self.assertEqual(result["probes"], suite["probes"])
            self.assertEqual(
                result["supported_range"],
                suite["consumer_support"][mode]["supported_range"],
            )

    def test_consumer_results_are_reproducible(self) -> None:
        for mode in ("schema", "minimal"):
            self.assertEqual(run_mode(mode), run_mode(mode))

    def test_all_fixtures_have_explicit_expected_result(self) -> None:
        suite = load_yaml_mapping(ROOT / "conformance.yaml")
        for fixture_id in suite["fixture_types"]:
            self.assertEqual(suite["fixtures"][fixture_id]["expected_result"], "pass")

    def test_each_consumer_declares_the_suite_supported_range(self) -> None:
        suite = load_yaml_mapping(ROOT / "conformance.yaml")
        for mode in suite["consumer_modes"]:
            self.assertEqual(
                suite["consumer_support"][mode]["supported_range"],
                suite["supported_range"],
            )

    def test_rc_is_inside_rc_to_stable_exclusive_range(self) -> None:
        declared = {
            "minimum_inclusive": "1.0.0-rc.1",
            "maximum_exclusive": "1.0.0",
        }
        self.assertEqual(
            range_errors(declared, {"id": "mind", "version": "1.0.0-rc.1"}),
            [],
        )
        self.assertTrue(
            range_errors(declared, {"id": "mind", "version": "1.0.0"})
        )

    def test_unknown_required_module_is_rejected(self) -> None:
        suite = load_yaml_mapping(ROOT / "conformance.yaml")
        manifest = build_manifest(suite["fixtures"]["person"], suite["protocol"])
        candidate = copy.deepcopy(manifest)
        candidate["modules"]["registered"].append("future_extension")
        candidate["modules"]["required"].append("future_extension")
        candidate["modules"]["catalog"]["future_extension"] = "future_extension/module.yaml"
        candidate["loading"]["default"].append("future_extension")
        self.assertTrue(consumer_module_errors(candidate))


if __name__ == "__main__":
    unittest.main()
