# © 2026 aiaiaiai · aiaiaiai.org
# SPDX-License-Identifier: MIT
"""Regression coverage for protocol/reference-instance repository authority routing."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

from validate_manifest import load_yaml_mapping  # noqa: E402


class RepositoryModelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.model = load_yaml_mapping(ROOT / "mind-repository.yaml")
        cls.manifest = load_yaml_mapping(ROOT / "manifest.yaml")

    def test_metadata_is_explicitly_not_a_protocol_contract(self) -> None:
        self.assertEqual(self.model["scope"], "repository_metadata")
        self.assertFalse(self.model["protocol_contract"])

    def test_repository_declares_two_distinct_roles(self) -> None:
        roles = self.model["repository"]["roles"]
        self.assertTrue(roles["protocol_authority"]["enabled"])
        self.assertTrue(roles["protocol_authority"]["canonical"])
        self.assertEqual(roles["protocol_authority"]["entrypoint"], "protocol.yaml")
        self.assertTrue(roles["concrete_mind"]["enabled"])
        self.assertTrue(roles["concrete_mind"]["reference_implementation"])
        self.assertFalse(roles["concrete_mind"]["template_authority"])

    def test_reference_subject_matches_concrete_manifest(self) -> None:
        declared = self.model["repository"]["roles"]["concrete_mind"][
            "canonical_for_subject"
        ]
        self.assertEqual(declared, self.manifest["mind"]["subject"])
        self.assertEqual(declared, {"type": "person", "id": "0x0sky"})

    def test_fork_policy_separates_protocol_development_from_mind_creation(self) -> None:
        policy = self.model["fork_policy"]
        self.assertEqual(policy["protocol_development"]["github_fork"], "allowed")
        concrete = policy["concrete_mind_creation"]
        self.assertEqual(
            concrete["github_fork_of_master"], "forbidden_as_template"
        )
        self.assertEqual(concrete["copy_reference_instance_content"], "forbidden")
        self.assertEqual(concrete["source"], "exact_immutable_protocol_release")
        self.assertEqual(concrete["mechanism"], "neutral_bootstrap")

    def test_bootstrap_routing_is_explicit(self) -> None:
        self.assertEqual(self.model["bootstrap"]["command"], "scripts/bootstrap_mind.py")
        self.assertEqual(
            self.model["bootstrap"]["input_authority"], "exact_protocol_release_tag"
        )
        self.assertEqual(
            self.model["bootstrap"]["floating_master"],
            "forbidden_for_release_consumption",
        )
        self.assertEqual(
            self.model["routing"]["new_mind_creation"], "docs/protocol/BOOTSTRAP.md"
        )


if __name__ == "__main__":
    unittest.main()
