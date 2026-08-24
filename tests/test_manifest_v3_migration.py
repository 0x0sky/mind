# © 2026 aiaiaiai · aiaiaiai.org
# SPDX-License-Identifier: MIT
"""Regression coverage for the supported pre-1.0 manifest v2 to v3 migration."""

from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

from migrate_manifest_v2_to_v3 import migrate_manifest  # noqa: E402
from validate_manifest import load_schema, load_yaml_mapping, schema_errors  # noqa: E402


class ManifestV3MigrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.current = load_yaml_mapping(ROOT / "manifest.yaml")
        cls.schema = load_schema(ROOT / "schema" / "mind.schema.json")

    def source_v2(self, version: str = "0.8.0") -> dict:
        source = copy.deepcopy(self.current)
        source["schema_version"] = 2
        source["protocol"]["version"] = version
        source["mind"]["kind"] = "personal"
        return source

    def test_clean_v2_manifest_migrates_without_context_version_change(self) -> None:
        source = self.source_v2()
        context_version = source["mind"]["context_version"]
        migrated, errors = migrate_manifest(source)
        self.assertEqual(errors, [])
        self.assertIsNotNone(migrated)
        assert migrated is not None
        self.assertEqual(migrated["schema_version"], 3)
        self.assertEqual(migrated["protocol"]["version"], "0.9.0")
        self.assertEqual(migrated["mind"]["context_version"], context_version)
        self.assertNotIn("kind", migrated["mind"])
        self.assertNotIn("public_organizations", migrated)
        self.assertEqual(
            schema_errors(Draft202012Validator(self.schema), migrated),
            [],
        )

    def test_nonempty_provider_projection_requires_explicit_preservation(self) -> None:
        source = self.source_v2()
        source["public_organizations"] = ["fixture-provider-org"]
        migrated, errors = migrate_manifest(source)
        self.assertIsNone(migrated)
        self.assertTrue(any("never inferred" in error for error in errors), errors)

        migrated, errors = migrate_manifest(
            source,
            provider_projection_preserved=True,
        )
        self.assertEqual(errors, [])
        self.assertIsNotNone(migrated)
        assert migrated is not None
        self.assertNotIn("public_organizations", migrated)

    def test_kind_subject_disagreement_is_rejected(self) -> None:
        source = self.source_v2()
        source["mind"]["kind"] = "organization"
        migrated, errors = migrate_manifest(source)
        self.assertIsNone(migrated)
        self.assertTrue(any("disagrees" in error for error in errors), errors)

    def test_versions_below_0_6_floor_are_rejected_deterministically(self) -> None:
        source = self.source_v2("0.5.0")
        migrated, errors = migrate_manifest(source)
        self.assertIsNone(migrated)
        self.assertTrue(any("migration floor is 0.6.0" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
