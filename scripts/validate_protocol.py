#!/usr/bin/env python3
# © 2026 aiaiaiai · aiaiaiai.org
# SPDX-License-Identifier: MIT
"""Validate the neutral protocol descriptor and its concrete mind instance binding."""

from __future__ import annotations

import sys
from pathlib import Path

from jsonschema import Draft202012Validator

from validate_manifest import load_schema, load_yaml_mapping, schema_errors


ROOT = Path(__file__).resolve().parents[1]
PROTOCOL_PATH = ROOT / "protocol.yaml"
PROTOCOL_SCHEMA_PATH = ROOT / "schema/protocol.schema.json"
MANIFEST_PATH = ROOT / "manifest.yaml"
IDENTITY_MODULE_PATH = ROOT / "identity/module.yaml"
IDENTITY_RESOURCE_PATH = ROOT / "identity/identity.yaml"
IDENTITY_SCHEMA_PATH = ROOT / "schema/identity.schema.json"
IDENTITY_RESOURCE_SCHEMA = "schema/identity-resource.schema.json"
VISUAL_ASSETS_SCHEMA = "schema/visual-assets.schema.json"

EXPECTED_CONTRACTS = {
    "manifest": "schema/mind.schema.json",
    "module": "schema/module.schema.json",
    "identity": "schema/identity.schema.json",
    "identity_resource": IDENTITY_RESOURCE_SCHEMA,
    "relationships": "schema/relationships.schema.json",
    "visual_assets": VISUAL_ASSETS_SCHEMA,
}


def repository_file(relative_path: str) -> Path:
    root = ROOT.resolve()
    path = (root / relative_path).resolve()
    if path != root and root not in path.parents:
        raise ValueError(f"path escapes repository: {relative_path}")
    if not path.is_file():
        raise ValueError(f"file does not exist: {relative_path}")
    return path


def validate_protocol() -> list[str]:
    errors: list[str] = []

    protocol = load_yaml_mapping(PROTOCOL_PATH)
    protocol_schema = load_schema(PROTOCOL_SCHEMA_PATH)
    errors.extend(
        f"protocol{error[1:]}"
        for error in schema_errors(Draft202012Validator(protocol_schema), protocol)
    )
    if errors:
        return errors

    manifest = load_yaml_mapping(MANIFEST_PATH)
    if manifest["protocol"]["id"] != protocol["protocol"]["id"]:
        errors.append("manifest protocol id must match protocol.yaml")
    if manifest["protocol"]["version"] != protocol["protocol"]["version"]:
        errors.append("manifest protocol version must match protocol.yaml")

    subject = manifest["mind"]["subject"]
    expected_instance_name = f"mind@{subject['id']}"
    if manifest["mind"]["name"] != expected_instance_name:
        errors.append(
            "$.mind.name: concrete canonical instance must be named "
            f"{expected_instance_name!r}"
        )

    contracts = protocol["contracts"]
    for contract_id, expected_schema in EXPECTED_CONTRACTS.items():
        actual_schema = contracts[contract_id]["schema"]
        if actual_schema != expected_schema:
            errors.append(
                f"protocol.contracts.{contract_id}.schema must be {expected_schema!r}"
            )
            continue
        try:
            load_schema(repository_file(actual_schema))
        except ValueError as error:
            errors.append(f"protocol.contracts.{contract_id}.schema: {error}")

    visual_policy = protocol["visual_identity"]
    resolver = visual_policy["asset_ref_resolution"]
    if resolver["resource_schema"] != VISUAL_ASSETS_SCHEMA:
        errors.append(
            "protocol.visual_identity.asset_ref_resolution.resource_schema "
            f"must be {VISUAL_ASSETS_SCHEMA!r}"
        )

    descriptor = load_yaml_mapping(IDENTITY_MODULE_PATH)
    identity_resource = descriptor.get("module", {}).get("resources", {}).get("identity")
    if not isinstance(identity_resource, dict):
        errors.append("identity module must declare resources.identity")
        return errors
    if identity_resource.get("path") != "identity/identity.yaml":
        errors.append("identity resource must resolve to identity/identity.yaml")
    if identity_resource.get("schema") != IDENTITY_RESOURCE_SCHEMA:
        errors.append(
            f"identity resource envelope must use {IDENTITY_RESOURCE_SCHEMA}"
        )

    resource = load_yaml_mapping(IDENTITY_RESOURCE_PATH)
    if resource.get("validation", {}).get("schema") != IDENTITY_RESOURCE_SCHEMA:
        errors.append(
            f"identity resource validation.schema must be {IDENTITY_RESOURCE_SCHEMA}"
        )

    identity = resource.get("identity")
    if not isinstance(identity, dict):
        errors.append("identity resource must carry an identity mapping")
        return errors

    identity_schema = load_schema(IDENTITY_SCHEMA_PATH)
    errors.extend(
        f"identity{error[1:]}"
        for error in schema_errors(Draft202012Validator(identity_schema), identity)
    )

    if identity.get("type") != subject.get("type") or identity.get("id") != subject.get("id"):
        errors.append("canonical identity type/id must match manifest mind.subject exactly")

    return errors


def main() -> int:
    try:
        errors = validate_protocol()
    except (KeyError, TypeError, ValueError) as error:
        print(f"protocol validation failed:\n- {error}", file=sys.stderr)
        return 1

    if errors:
        print("protocol validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("protocol and mind instance binding are valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
