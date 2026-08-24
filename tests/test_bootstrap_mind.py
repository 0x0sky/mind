# © 2026 aiaiaiai · aiaiaiai.org
# SPDX-License-Identifier: MIT
"""Regression coverage for concrete Mind bootstrap isolation and validity."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

from bootstrap_mind import bootstrap_mind, verify_release_checkout  # noqa: E402
from validate_identity_resources import validate_identity_envelope  # noqa: E402
from validate_manifest import (  # noqa: E402
    load_schema,
    load_yaml_mapping,
    schema_errors,
    validate_manifest_semantics,
    validate_modules,
)

PROTOCOL = load_yaml_mapping(ROOT / "protocol.yaml")["protocol"]
SOURCE_TAG = f"v{PROTOCOL['version']}"


class BootstrapMindTests(unittest.TestCase):
    def bootstrap(self, root: Path, **overrides: object) -> Path:
        output = root / "mind"
        arguments: dict[str, object] = {
            "source_tag": SOURCE_TAG,
            "subject_type": "organization",
            "subject_id": "fixture-organization",
            "display_name": "Fixture Organization",
            "context_version": "0.1.0",
            "repository_visibility": "public",
        }
        arguments.update(overrides)
        bootstrap_mind(output, **arguments)  # type: ignore[arg-type]
        return output

    @staticmethod
    def release_git_output(*, head: str = "a" * 40, tag: str = "a" * 40, dirty: str = ""):
        def output(*arguments: str) -> str:
            if arguments == ("rev-parse", "--show-toplevel"):
                return str(ROOT)
            if arguments == ("rev-parse", "HEAD"):
                return head
            if arguments == ("rev-list", "-n", "1", f"refs/tags/{SOURCE_TAG}"):
                return tag
            if arguments[:4] == (
                "status",
                "--porcelain",
                "--untracked-files=no",
                "--",
            ):
                return dirty
            raise AssertionError(f"unexpected git arguments: {arguments!r}")

        return output

    def test_exact_release_checkout_is_accepted(self) -> None:
        with patch(
            "bootstrap_mind.git_output",
            side_effect=self.release_git_output(),
        ):
            verify_release_checkout(SOURCE_TAG)

    def test_release_checkout_rejects_head_that_is_not_the_tag(self) -> None:
        with patch(
            "bootstrap_mind.git_output",
            side_effect=self.release_git_output(head="a" * 40, tag="b" * 40),
        ):
            with self.assertRaisesRegex(ValueError, "HEAD must equal"):
                verify_release_checkout(SOURCE_TAG)

    def test_release_checkout_rejects_dirty_protocol_contracts(self) -> None:
        with patch(
            "bootstrap_mind.git_output",
            side_effect=self.release_git_output(dirty=" M protocol.yaml"),
        ):
            with self.assertRaisesRegex(ValueError, "differ from the tagged checkout"):
                verify_release_checkout(SOURCE_TAG)

    def test_release_checkout_rejects_floating_source_name(self) -> None:
        with self.assertRaisesRegex(ValueError, "source tag must exactly match"):
            verify_release_checkout("master")

    def test_bootstrap_produces_valid_concrete_manifest_and_identity(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = self.bootstrap(Path(directory))
            manifest = load_yaml_mapping(output / "manifest.yaml")
            manifest_schema = load_schema(output / "schema" / "mind.schema.json")
            self.assertEqual(
                schema_errors(Draft202012Validator(manifest_schema), manifest), []
            )
            self.assertEqual(validate_manifest_semantics(manifest, output), [])
            self.assertEqual(validate_modules(manifest, output), [])

            envelope = load_yaml_mapping(output / "identity" / "identity.yaml")
            envelope_schema = load_schema(
                output / "schema" / "identity-resource.schema.json"
            )
            identity_schema = load_schema(output / "schema" / "identity.schema.json")
            self.assertEqual(
                validate_identity_envelope(
                    envelope, manifest, envelope_schema, identity_schema
                ),
                [],
            )
            self.assertEqual(envelope["identity"]["type"], "organization")
            self.assertEqual(envelope["identity"]["id"], "fixture-organization")

    def test_reference_instance_is_not_copied_into_authored_machine_content(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = self.bootstrap(Path(directory))
            manifest = (output / "manifest.yaml").read_text(encoding="utf-8")
            identity = (output / "identity" / "identity.yaml").read_text(
                encoding="utf-8"
            )
            self.assertNotIn("mind@0x0sky", manifest)
            self.assertNotIn("mind@0x0sky", identity)
            self.assertNotIn("id: 0x0sky", manifest)
            self.assertNotIn("id: 0x0sky", identity)

            repository = load_yaml_mapping(output / "mind-repository.yaml")
            concrete = repository["repository"]["roles"]["concrete_mind"]
            self.assertFalse(concrete["reference_implementation"])
            self.assertFalse(concrete["template_authority"])
            self.assertFalse(
                repository["repository"]["roles"]["protocol_authority"]["enabled"]
            )

    def test_protocol_lock_pins_exact_release_and_contract_bytes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = self.bootstrap(Path(directory))
            lock = load_yaml_mapping(output / "protocol.lock.yaml")
            self.assertEqual(lock["protocol"]["version"], PROTOCOL["version"])
            self.assertEqual(lock["source"]["tag"], SOURCE_TAG)
            self.assertEqual(lock["source"]["floating_branch"], "forbidden")
            self.assertFalse(lock["reference_instance"]["template_authority"])
            self.assertEqual(lock["reference_instance"]["copy_content"], "forbidden")
            self.assertEqual(len(lock["vendored_contracts"]), 9)
            for descriptor in lock["vendored_contracts"].values():
                self.assertRegex(descriptor["git_blob_sha1"], r"^[0-9a-f]{40}$")
                self.assertTrue(
                    descriptor["schema_id"].startswith(
                        "https://aiaiaiai.org/mind/schema/"
                    )
                )

    def test_distinct_publication_owner_is_preserved(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = self.bootstrap(
                Path(directory),
                subject_type="agent",
                subject_id="fixture-agent",
                display_name="Fixture Agent",
                owner_type="organization",
                owner_id="fixture-publisher",
                repository_visibility="private",
            )
            manifest = load_yaml_mapping(output / "manifest.yaml")
            self.assertEqual(
                manifest["mind"]["subject"],
                {"type": "agent", "id": "fixture-agent"},
            )
            self.assertEqual(
                manifest["mind"]["owner"],
                {"type": "organization", "id": "fixture-publisher"},
            )
            module = load_yaml_mapping(output / "identity" / "module.yaml")
            self.assertEqual(module["module"]["owner"], manifest["mind"]["owner"])
            self.assertEqual(module["module"]["visibility"], "private")

    def test_source_tag_must_match_checked_out_protocol(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(ValueError, "source tag must exactly match"):
                self.bootstrap(Path(directory), source_tag="master")

    def test_owner_arguments_are_atomic(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(ValueError, "supplied together"):
                self.bootstrap(
                    Path(directory),
                    owner_type="organization",
                )

    def test_existing_nonempty_output_is_never_overwritten(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "mind"
            output.mkdir()
            (output / "keep.txt").write_text("do not overwrite", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "not empty"):
                bootstrap_mind(
                    output,
                    source_tag=SOURCE_TAG,
                    subject_type="person",
                    subject_id="fixture-person",
                    display_name="Fixture Person",
                    context_version="0.1.0",
                    repository_visibility="private",
                )
            self.assertEqual(
                (output / "keep.txt").read_text(encoding="utf-8"), "do not overwrite"
            )


if __name__ == "__main__":
    unittest.main()
