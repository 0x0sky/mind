# © 2026 aiaiaiai · aiaiaiai.org
# SPDX-License-Identifier: MIT
"""Regression coverage for the manual Mind Protocol release workflow contract."""

from __future__ import annotations

import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW_PATH = ROOT / ".github" / "workflows" / "release.yml"


class ReleaseWorkflowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.text = WORKFLOW_PATH.read_text(encoding="utf-8")
        cls.workflow = yaml.load(cls.text, Loader=yaml.BaseLoader)

    def test_manual_ui_exposes_only_publication_kind(self) -> None:
        dispatch = self.workflow["on"]["workflow_dispatch"]
        inputs = dispatch["inputs"]
        self.assertEqual(set(inputs), {"channel"})
        self.assertEqual(inputs["channel"]["type"], "choice")
        self.assertEqual(inputs["channel"]["options"], ["release", "prerelease"])

    def test_free_text_release_identity_inputs_are_not_supported(self) -> None:
        self.assertNotIn("inputs.version", self.text)
        self.assertNotIn("inputs.target_sha", self.text)
        self.assertNotIn("Protocol version without v prefix", self.text)
        self.assertNotIn("Exact master merge commit to tag and release", self.text)

    def test_selected_branch_event_is_the_release_target(self) -> None:
        self.assertIn("${{ github.ref_name }}", self.text)
        self.assertIn("${{ github.sha }}", self.text)
        self.assertIn("GITHUB_REF_NAME", self.text)
        self.assertIn("GITHUB_SHA", self.text)
        self.assertIn(".default_branch", self.text)
        self.assertIn("selected branch moved after dispatch", self.text)

    def test_version_tag_title_and_notes_are_derived(self) -> None:
        self.assertIn("protocol.yaml", self.text)
        self.assertIn('"v${VERSION}"', self.text)
        self.assertIn('"Mind Protocol ${VERSION}"', self.text)
        self.assertIn('"docs/protocol/releases/v${VERSION}.md"', self.text)

    def test_publication_kind_must_match_semver_state(self) -> None:
        self.assertIn("release requires a stable semantic version", self.text)
        self.assertIn("prerelease requires a prerelease semantic version", self.text)
        self.assertIn('[[ "$CHANNEL" == "prerelease" ]]', self.text)

    def test_verified_pr_tree_and_immutable_tag_guards_remain(self) -> None:
        self.assertIn("merge_commit_sha", self.text)
        self.assertIn("TARGET_TREE", self.text)
        self.assertIn("TESTED_TREE", self.text)
        self.assertIn("manifest-ci.yml", self.text)
        self.assertIn("tag v${VERSION} already exists", self.text)
        self.assertIn("published tag does not point to the verified release commit", self.text)


if __name__ == "__main__":
    unittest.main()
