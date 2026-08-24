# © 2026 aiaiaiai · aiaiaiai.org
# SPDX-License-Identifier: MIT
"""Regression tests for release-agnostic compatibility schema bytes."""

from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_ROOT = REPOSITORY_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS_ROOT))

from validate_compatibility import (  # noqa: E402
    frozen_contract_errors,
    migration_policy_errors,
)
from validate_manifest import load_schema, load_yaml_mapping, schema_errors  # noqa: E402
from validate_protocol import compatibility_lifecycle_errors  # noqa: E402


class CompatibilityPolicyRegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.policy = load_yaml_mapping(REPOSITORY_ROOT / "compatibility.yaml")
        cls.protocol = load_yaml_mapping(REPOSITORY_ROOT / "protocol.yaml")
        cls.compatibility_schema = load_schema(
            REPOSITORY_ROOT / "schema" / "compatibility.schema.json"
        )
        cls.protocol_schema = load_schema(REPOSITORY_ROOT / "schema" / "protocol.schema.json")

    def test_current_frozen_contracts_are_unique_and_exact(self) -> None:
        self.assertEqual(frozen_contract_errors(self.policy), [])
        descriptors = self.policy["freeze"]["frozen_contracts"]
        paths = [descriptor["path"] for descriptor in descriptors]
        schema_ids = [descriptor["schema_id"] for descriptor in descriptors]
        self.assertEqual(len(paths), len(set(paths)))
        self.assertEqual(len(schema_ids), len(set(schema_ids)))

    def test_compatibility_schema_accepts_rc_policy_without_schema_byte_change(self) -> None:
        candidate = copy.deepcopy(self.policy)
        candidate["protocol"]["version"] = "1.0.0-rc.1"
        candidate["migration"]["supported_stable_lines"].append("0.9.0")
        errors = schema_errors(Draft202012Validator(self.compatibility_schema), candidate)
        self.assertEqual(errors, [])

    def test_protocol_schema_accepts_all_v3_lifecycle_states(self) -> None:
        cases = (
            ("0.9.0", "frozen_pre_1_0"),
            ("1.0.0-rc.1", "release_candidate"),
            ("1.0.0", "stable_1_x"),
        )
        for version, status in cases:
            with self.subTest(version=version, status=status):
                candidate = copy.deepcopy(self.protocol)
                candidate["protocol"]["version"] = version
                candidate["compatibility"]["status"] = status
                errors = schema_errors(Draft202012Validator(self.protocol_schema), candidate)
                self.assertEqual(errors, [])
                self.assertEqual(compatibility_lifecycle_errors(candidate), [])

    def test_release_lifecycle_mismatch_is_rejected_semantically(self) -> None:
        candidate = copy.deepcopy(self.protocol)
        candidate["protocol"]["version"] = "1.0.0-rc.1"
        candidate["compatibility"]["status"] = "stable_1_x"
        errors = compatibility_lifecycle_errors(candidate)
        self.assertTrue(any("requires 'release_candidate'" in error for error in errors), errors)

    def test_migration_lines_advance_with_release_target(self) -> None:
        self.assertEqual(migration_policy_errors(self.policy), [])

        candidate = copy.deepcopy(self.policy)
        candidate["protocol"]["version"] = "1.0.0-rc.1"
        candidate["migration"]["supported_stable_lines"].append("0.9.0")
        self.assertEqual(migration_policy_errors(candidate), [])

        candidate["migration"]["supported_stable_lines"].remove("0.8.0")
        errors = migration_policy_errors(candidate)
        self.assertTrue(any("target release exactly" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
