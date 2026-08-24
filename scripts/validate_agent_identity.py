#!/usr/bin/env python3
# © 2026 aiaiaiai · aiaiaiai.org
# SPDX-License-Identifier: MIT
"""Validate the synthetic first-class agent Identity conformance case."""

from __future__ import annotations

import copy
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from validate_identity_resources import validate_identity_envelope
from validate_manifest import load_schema, load_yaml_mapping, schema_errors


ROOT = Path(__file__).resolve().parents[1]
FIXTURE_ROOT = ROOT / "tests" / "fixtures" / "agent_identity"
FORBIDDEN_AGENT_IDENTITY_FIELDS = (
    "provider",
    "provider_account",
    "model",
    "prompt",
    "memory",
    "runtime",
    "execution_state",
    "biological_person",
    "portrait",
    "synthetic_portrait",
)


def validate_agent_case(
    manifest: dict[str, Any],
    envelope: dict[str, Any],
    manifest_schema: dict[str, Any],
    envelope_schema: dict[str, Any],
    identity_schema: dict[str, Any],
    *,
    require_distinct_owner_fixture: bool = False,
) -> list[str]:
    errors = [
        f"manifest{error[1:]}"
        for error in schema_errors(Draft202012Validator(manifest_schema), manifest)
    ]
    errors.extend(
        validate_identity_envelope(
            envelope,
            manifest,
            envelope_schema,
            identity_schema,
        )
    )
    if errors:
        return errors

    mind = manifest["mind"]
    subject = mind["subject"]
    owner = mind["owner"]
    identity = envelope["identity"]

    if mind["kind"] != "agent":
        errors.append("agent fixture mind.kind must be 'agent'")
    if subject["type"] != "agent":
        errors.append("agent fixture subject.type must be 'agent'")
    if mind["name"] != f"mind@{subject['id']}":
        errors.append("agent fixture mind.name must follow mind@{subject.id}")
    if require_distinct_owner_fixture and owner == subject:
        errors.append("agent fixture must prove that publication owner may differ from subject")

    if "visual_identity" in identity:
        errors.append(
            "synthetic agent fixture must not make a portrait or generated visual canonical by default"
        )

    identity_validator = Draft202012Validator(identity_schema)
    for field in FORBIDDEN_AGENT_IDENTITY_FIELDS:
        candidate = copy.deepcopy(identity)
        candidate[field] = "synthetic"
        if not schema_errors(identity_validator, candidate):
            errors.append(
                f"universal Identity unexpectedly accepts agent runtime/provider field {field!r}"
            )

    return errors


def validate_fixture() -> list[str]:
    manifest = load_yaml_mapping(FIXTURE_ROOT / "manifest.yaml")
    envelope = load_yaml_mapping(FIXTURE_ROOT / "identity.yaml")
    protocol = load_yaml_mapping(ROOT / "protocol.yaml")

    contracts = protocol["contracts"]
    manifest_schema = load_schema(ROOT / contracts["manifest"]["schema"])
    envelope_schema = load_schema(ROOT / contracts["identity_resource"]["schema"])
    identity_schema = load_schema(ROOT / contracts["identity"]["schema"])

    errors: list[str] = []
    if manifest.get("protocol") != protocol.get("protocol"):
        errors.append("agent fixture must target the repository protocol id/version exactly")

    errors.extend(
        validate_agent_case(
            manifest,
            envelope,
            manifest_schema,
            envelope_schema,
            identity_schema,
            require_distinct_owner_fixture=True,
        )
    )
    return errors


def main() -> int:
    try:
        errors = validate_fixture()
    except (KeyError, TypeError, ValueError) as error:
        print(f"agent identity conformance failed:\n- {error}", file=sys.stderr)
        return 1

    if errors:
        print("agent identity conformance failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("synthetic agent Identity conformance is valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
