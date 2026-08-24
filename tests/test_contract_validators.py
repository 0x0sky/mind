# © 2026 aiaiaiai · aiaiaiai.org
# SPDX-License-Identifier: MIT
"""Regression tests for correctness-critical Mind contract validators."""

from __future__ import annotations

import copy
import sys
import tempfile
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_ROOT = REPOSITORY_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS_ROOT))

from validate_manifest import load_yaml_mapping, validate_manifest_semantics  # noqa: E402
from validate_relationships import validate_relationships  # noqa: E402


class ContractValidatorRegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = load_yaml_mapping(REPOSITORY_ROOT / "manifest.yaml")
        cls.relationships = load_yaml_mapping(
            REPOSITORY_ROOT / "relationships" / "relationships.yaml"
        )

    def test_current_manifest_semantics_are_valid(self) -> None:
        self.assertEqual(validate_manifest_semantics(self.manifest, REPOSITORY_ROOT), [])

    def test_duplicate_yaml_keys_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "duplicate.yaml"
            path.write_text("value: 1\nvalue: 2\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "duplicate key"):
                load_yaml_mapping(path)

    def test_subject_type_cannot_drift_from_mind_kind(self) -> None:
        candidate = copy.deepcopy(self.manifest)
        candidate["mind"]["kind"] = "organization"
        errors = validate_manifest_semantics(candidate, REPOSITORY_ROOT)
        self.assertTrue(
            any("requires subject type 'organization'" in error for error in errors),
            errors,
        )

    def test_validation_paths_cannot_escape_repository(self) -> None:
        candidate = copy.deepcopy(self.manifest)
        candidate["validation"]["schema"] = "../mind.schema.json"
        errors = validate_manifest_semantics(candidate, REPOSITORY_ROOT)
        self.assertTrue(any("path escapes repository" in error for error in errors), errors)

    def test_current_relationship_semantics_are_valid(self) -> None:
        self.assertEqual(validate_relationships(self.manifest, self.relationships), [])

    def test_relationship_authority_must_match_publication_owner(self) -> None:
        candidate = copy.deepcopy(self.relationships)
        candidate["relationships"][0]["provenance"]["authority"]["id"] = "other-owner"
        errors = validate_relationships(self.manifest, candidate)
        self.assertTrue(any("must match $.mind.owner" in error for error in errors), errors)

    def test_legacy_public_organization_requires_authored_membership(self) -> None:
        candidate = copy.deepcopy(self.relationships)
        candidate["relationships"] = [
            relationship
            for relationship in candidate["relationships"]
            if relationship["target"]["id"] != "nilx-one"
        ]
        errors = validate_relationships(self.manifest, candidate)
        self.assertTrue(
            any("legacy projection must be backed" in error for error in errors),
            errors,
        )

    def test_reciprocal_confirmation_must_reference_other_endpoint(self) -> None:
        candidate = copy.deepcopy(self.relationships)
        candidate["relationships"][0]["confirmation"]["counterpart"]["entity"]["id"] = (
            "0xda-market"
        )
        errors = validate_relationships(self.manifest, candidate)
        self.assertTrue(
            any("must identify the other relationship endpoint" in error for error in errors),
            errors,
        )


if __name__ == "__main__":
    unittest.main()
