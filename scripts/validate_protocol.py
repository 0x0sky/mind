#!/usr/bin/env python3
# © 2026 aiaiaiai · aiaiaiai.org
# SPDX-License-Identifier: MIT
"""Validate the neutral protocol descriptor and its concrete mind instance binding."""

from __future__ import annotations

import re
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
CONFORMANCE_SCHEMA = "schema/conformance.schema.json"
COMPATIBILITY_SCHEMA = "schema/compatibility.schema.json"

EXPECTED_CONTRACTS = {
    "manifest": "schema/mind.schema.json",
    "module": "schema/module.schema.json",
    "identity": "schema/identity.schema.json",
    "identity_resource": IDENTITY_RESOURCE_SCHEMA,
    "relationships": "schema/relationships.schema.json",
    "visual_assets": VISUAL_ASSETS_SCHEMA,
    "conformance": CONFORMANCE_SCHEMA,
    "compatibility": COMPATIBILITY_SCHEMA,
}

SEMVER_RE = re.compile(
    r"^(?P<major>0|[1-9][0-9]*)\."
    r"(?P<minor>0|[1-9][0-9]*)\."
    r"(?P<patch>0|[1-9][0-9]*)"
    r"(?:-(?P<prerelease>[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?"
    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$"
)


def expected_compatibility_status(version: str) -> str:
    """Return the protocol lifecycle state implied by a schema-v3 release version."""
    match = SEMVER_RE.fullmatch(version)
    if match is None:
        raise ValueError(f"invalid protocol semantic version: {version!r}")

    major = int(match.group("major"))
    prerelease = match.group("prerelease")
    if major == 0:
        return "frozen_pre_1_0"
    if major == 1:
        return "release_candidate" if prerelease else "stable_1_x"
    raise ValueError(
        "protocol descriptor schema v3 defines lifecycle semantics only for "
        "pre-1.0 and 1.x releases"
    )


def compatibility_lifecycle_errors(protocol: dict[str, object]) -> list[str]:
    version = protocol["protocol"]["version"]  # type: ignore[index]
    status = protocol["compatibility"]["status"]  # type: ignore[index]
    expected = expected_compatibility_status(str(version))
    if status != expected:
        return [
            "protocol.compatibility.status must match protocol release lifecycle: "
            f"version {version!r} requires {expected!r}, got {status!r}"
        ]
    return []


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
    errors.extend(compatibility_lifecycle_errors(protocol))

    manifest = load_yaml_mapping(MANIFEST_PATH)
    protocol_ref = {
        "id": protocol["protocol"]["id"],
        "version": protocol["protocol"]["version"],
    }
    if manifest.get("protocol") != protocol_ref:
        errors.append("manifest protocol id/version must match protocol.yaml")

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

    resolver = protocol["visual_identity"]["asset_ref_resolution"]
    if resolver["resource_schema"] != VISUAL_ASSETS_SCHEMA:
        errors.append(
            "protocol.visual_identity.asset_ref_resolution.resource_schema "
            f"must be {VISUAL_ASSETS_SCHEMA!r}"
        )

    conformance_ref = protocol["conformance"]["suite"]
    try:
        conformance = load_yaml_mapping(repository_file(conformance_ref))
        conformance_schema = load_schema(repository_file(CONFORMANCE_SCHEMA))
    except ValueError as error:
        errors.append(f"protocol.conformance.suite: {error}")
    else:
        errors.extend(
            f"conformance{error[1:]}"
            for error in schema_errors(Draft202012Validator(conformance_schema), conformance)
        )
        if conformance.get("protocol") != protocol_ref:
            errors.append("conformance suite must target protocol id/version exactly")

    compatibility_ref = protocol["compatibility"]["policy"]
    try:
        compatibility = load_yaml_mapping(repository_file(compatibility_ref))
        compatibility_schema = load_schema(repository_file(COMPATIBILITY_SCHEMA))
    except ValueError as error:
        errors.append(f"protocol.compatibility.policy: {error}")
    else:
        errors.extend(
            f"compatibility{error[1:]}"
            for error in schema_errors(
                Draft202012Validator(compatibility_schema), compatibility
            )
        )
        if compatibility.get("protocol") != protocol_ref:
            errors.append("compatibility policy must target protocol id/version exactly")

    descriptor = load_yaml_mapping(IDENTITY_MODULE_PATH)
    identity_resource = descriptor.get("module", {}).get("resources", {}).get("identity")
    if not isinstance(identity_resource, dict):
        errors.append("identity module must declare resources.identity")
        return errors
    if identity_resource.get("path") != "identity/identity.yaml":
        errors.append("identity resource must resolve to identity/identity.yaml")
    if identity_resource.get("schema") != IDENTITY_RESOURCE_SCHEMA:
        errors.append(f"identity resource envelope must use {IDENTITY_RESOURCE_SCHEMA}")

    resource = load_yaml_mapping(IDENTITY_RESOURCE_PATH)
    if resource.get("validation", {}).get("schema") != IDENTITY_RESOURCE_SCHEMA:
        errors.append(f"identity resource validation.schema must be {IDENTITY_RESOURCE_SCHEMA}")

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

    print("protocol, conformance, compatibility, and mind instance binding are valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
