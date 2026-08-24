# © 2026 aiaiaiai · aiaiaiai.org
# SPDX-License-Identifier: MIT
"""Regression coverage for universal Identity inside concrete resource envelopes."""

from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_ROOT = REPOSITORY_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS_ROOT))

from validate_identity_resources import validate_identity_envelope  # noqa: E402
from validate_manifest import load_schema, load_yaml_mapping  # noqa: E402


class IdentityResourceValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = load_yaml_mapping(REPOSITORY_ROOT / "manifest.yaml")
        cls.envelope = load_yaml_mapping(REPOSITORY_ROOT / "identity" / "identity.yaml")
        cls.envelope_schema = load_schema(
            REPOSITORY_ROOT / "schema" / "identity-resource.schema.json"
        )
        cls.identity_schema = load_schema(
            REPOSITORY_ROOT / "schema" / "identity.schema.json"
        )

    def validate(self, envelope: dict, manifest: dict | None = None) -> list[str]:
        return validate_identity_envelope(
            envelope,
            self.manifest if manifest is None else manifest,
            self.envelope_schema,
            self.identity_schema,
        )

    def test_current_identity_resource_is_valid(self) -> None:
        self.assertEqual(self.validate(self.envelope), [])

    def test_embedded_identity_is_validated_against_universal_schema(self) -> None:
        candidate = copy.deepcopy(self.envelope)
        candidate["identity"]["provider_account"] = "provider-user"
        errors = self.validate(candidate)
        self.assertTrue(any("provider_account" in error for error in errors), errors)

    def test_runtime_state_cannot_leak_into_universal_identity(self) -> None:
        candidate = copy.deepcopy(self.envelope)
        candidate["identity"]["runtime"] = {"model": "synthetic-model"}
        errors = self.validate(candidate)
        self.assertTrue(any("runtime" in error for error in errors), errors)

    def test_identity_must_bind_to_manifest_subject(self) -> None:
        candidate = copy.deepcopy(self.envelope)
        candidate["identity"]["id"] = "other-subject"
        errors = self.validate(candidate)
        self.assertTrue(any("must match manifest mind.subject" in error for error in errors), errors)

    def test_agent_identity_uses_same_universal_contract_with_distinct_owner(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        manifest["mind"]["name"] = "mind@synthetic-agent"
        manifest["mind"]["subject"] = {"type": "agent", "id": "synthetic-agent"}
        manifest["mind"]["owner"] = {
            "type": "organization",
            "id": "synthetic-publisher",
        }

        envelope = copy.deepcopy(self.envelope)
        envelope["identity"] = {
            "type": "agent",
            "id": "synthetic-agent",
            "display_name": "Synthetic Agent",
        }

        self.assertNotEqual(manifest["mind"]["subject"], manifest["mind"]["owner"])
        self.assertEqual(self.validate(envelope, manifest), [])


if __name__ == "__main__":
    unittest.main()
