# © 2026 aiaiaiai · aiaiaiai.org
# SPDX-License-Identifier: MIT
"""Regression coverage for first-class agent Identity semantics."""

from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_ROOT = REPOSITORY_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS_ROOT))

from validate_agent_identity import validate_agent_case, validate_fixture  # noqa: E402
from validate_manifest import load_schema, load_yaml_mapping  # noqa: E402


FIXTURE_ROOT = REPOSITORY_ROOT / "tests" / "fixtures" / "agent_identity"


class AgentIdentityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = load_yaml_mapping(FIXTURE_ROOT / "manifest.yaml")
        cls.envelope = load_yaml_mapping(FIXTURE_ROOT / "identity.yaml")
        cls.manifest_schema = load_schema(REPOSITORY_ROOT / "schema" / "mind.schema.json")
        cls.envelope_schema = load_schema(
            REPOSITORY_ROOT / "schema" / "identity-resource.schema.json"
        )
        cls.identity_schema = load_schema(
            REPOSITORY_ROOT / "schema" / "identity.schema.json"
        )

    def validate(
        self,
        manifest: dict | None = None,
        envelope: dict | None = None,
        *,
        require_distinct_owner_fixture: bool = False,
    ) -> list[str]:
        return validate_agent_case(
            self.manifest if manifest is None else manifest,
            self.envelope if envelope is None else envelope,
            self.manifest_schema,
            self.envelope_schema,
            self.identity_schema,
            require_distinct_owner_fixture=require_distinct_owner_fixture,
        )

    def test_synthetic_agent_fixture_is_green(self) -> None:
        self.assertEqual(validate_fixture(), [])

    def test_distinct_publication_owner_is_valid(self) -> None:
        self.assertNotEqual(self.manifest["mind"]["subject"], self.manifest["mind"]["owner"])
        self.assertEqual(self.validate(), [])

    def test_agent_does_not_require_provider_or_runtime_configuration(self) -> None:
        identity = self.envelope["identity"]
        self.assertEqual(set(identity), {"type", "id", "display_name"})
        self.assertEqual(self.validate(), [])

    def test_runtime_configuration_is_outside_universal_identity(self) -> None:
        for field in ("model", "prompt", "memory", "runtime", "execution_state"):
            envelope = copy.deepcopy(self.envelope)
            envelope["identity"][field] = "synthetic"
            errors = self.validate(envelope=envelope)
            self.assertTrue(any(field in error for error in errors), (field, errors))

    def test_provider_account_is_outside_universal_identity(self) -> None:
        envelope = copy.deepcopy(self.envelope)
        envelope["identity"]["provider_account"] = "synthetic-provider-agent"
        errors = self.validate(envelope=envelope)
        self.assertTrue(any("provider_account" in error for error in errors), errors)

    def test_biological_personhood_is_not_part_of_agent_identity(self) -> None:
        envelope = copy.deepcopy(self.envelope)
        envelope["identity"]["biological_person"] = False
        errors = self.validate(envelope=envelope)
        self.assertTrue(any("biological_person" in error for error in errors), errors)

    def test_synthetic_portrait_is_not_canonical_by_default(self) -> None:
        self.assertNotIn("visual_identity", self.envelope["identity"])
        envelope = copy.deepcopy(self.envelope)
        envelope["identity"]["synthetic_portrait"] = "generated://portrait"
        errors = self.validate(envelope=envelope)
        self.assertTrue(any("synthetic_portrait" in error for error in errors), errors)

    def test_same_owner_is_not_forbidden_by_universal_agent_semantics(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        manifest["mind"]["owner"] = copy.deepcopy(manifest["mind"]["subject"])
        self.assertEqual(self.validate(manifest=manifest), [])
        errors = self.validate(
            manifest=manifest,
            require_distinct_owner_fixture=True,
        )
        self.assertTrue(any("may differ" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
