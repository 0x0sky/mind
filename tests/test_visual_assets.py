# © 2026 aiaiaiai · aiaiaiai.org
# SPDX-License-Identifier: MIT
"""Regression coverage for canonical visual asset resolution."""

from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_ROOT = REPOSITORY_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS_ROOT))

from validate_manifest import load_schema, load_yaml_mapping, schema_errors  # noqa: E402
from validate_visual_assets import (  # noqa: E402
    NORMATIVE_MEDIA_TYPES,
    resolve_primary_mark,
    validate_fixture,
)


FIXTURE_ROOT = REPOSITORY_ROOT / "tests" / "fixtures" / "visual_identity"


class VisualAssetContractTests(unittest.TestCase):
    def test_required_synthetic_subject_types_resolve(self) -> None:
        discovered = set()
        for fixture in sorted(path for path in FIXTURE_ROOT.iterdir() if path.is_dir()):
            subject_type, errors = validate_fixture(fixture)
            self.assertEqual(errors, [], f"{fixture.name}: {errors}")
            discovered.add(subject_type)
        self.assertTrue({"person", "organization", "agent"}.issubset(discovered))

    def test_missing_primary_mark_is_deterministically_unavailable(self) -> None:
        fixture = FIXTURE_ROOT / "person"
        identity = load_yaml_mapping(fixture / "identity.yaml")
        catalog = load_yaml_mapping(fixture / "visual-assets.yaml")
        identity.pop("visual_identity")
        self.assertEqual(resolve_primary_mark(identity, catalog, fixture).status, "unavailable")

    def test_missing_asset_is_observable(self) -> None:
        fixture = FIXTURE_ROOT / "person"
        identity = load_yaml_mapping(fixture / "identity.yaml")
        catalog = load_yaml_mapping(fixture / "visual-assets.yaml")
        catalog["assets"][0]["resource_path"] = "missing.svg"
        self.assertEqual(resolve_primary_mark(identity, catalog, fixture).status, "missing")

    def test_integrity_failure_is_observable(self) -> None:
        fixture = FIXTURE_ROOT / "person"
        identity = load_yaml_mapping(fixture / "identity.yaml")
        catalog = load_yaml_mapping(fixture / "visual-assets.yaml")
        catalog["assets"][0]["integrity"]["digest"] = "0" * 64
        self.assertEqual(resolve_primary_mark(identity, catalog, fixture).status, "integrity_error")

    def test_optional_media_can_be_unsupported_without_becoming_canonical_fallback(self) -> None:
        fixture = FIXTURE_ROOT / "person"
        identity = load_yaml_mapping(fixture / "identity.yaml")
        catalog = load_yaml_mapping(fixture / "visual-assets.yaml")
        catalog["assets"][0]["media_type"] = "image/webp"
        result = resolve_primary_mark(
            identity,
            catalog,
            fixture,
            supported_media_types=NORMATIVE_MEDIA_TYPES,
        )
        self.assertEqual(result.status, "unsupported_media")

    def test_duplicate_asset_ref_is_ambiguous(self) -> None:
        fixture = FIXTURE_ROOT / "person"
        identity = load_yaml_mapping(fixture / "identity.yaml")
        catalog = load_yaml_mapping(fixture / "visual-assets.yaml")
        catalog["assets"].append(copy.deepcopy(catalog["assets"][0]))
        self.assertEqual(resolve_primary_mark(identity, catalog, fixture).status, "ambiguous")

    def test_provider_visual_cannot_enter_universal_identity_silently(self) -> None:
        fixture = FIXTURE_ROOT / "person"
        identity = load_yaml_mapping(fixture / "identity.yaml")
        identity["visual_identity"]["provider_avatar_url"] = "https://provider.invalid/avatar.png"
        schema = load_schema(REPOSITORY_ROOT / "schema" / "identity.schema.json")
        errors = schema_errors(Draft202012Validator(schema), identity)
        self.assertTrue(errors)


if __name__ == "__main__":
    unittest.main()
