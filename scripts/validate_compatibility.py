#!/usr/bin/env python3
# © 2026 aiaiaiai · aiaiaiai.org
# SPDX-License-Identifier: MIT
"""Validate Mind compatibility policy, fingerprints, lifecycle, and migration floor."""

from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from validate_manifest import load_json_mapping, load_schema, load_yaml_mapping, schema_errors
from validate_protocol import expected_compatibility_status


ROOT = Path(__file__).resolve().parents[1]
POLICY_PATH = ROOT / "compatibility.yaml"
POLICY_SCHEMA_PATH = ROOT / "schema" / "compatibility.schema.json"
PROTOCOL_PATH = ROOT / "protocol.yaml"
CONFORMANCE_PATH = ROOT / "conformance.yaml"
MANIFEST_PATH = ROOT / "manifest.yaml"
SCHEMA_ROOT = ROOT / "schema"

MIGRATION_FLOOR = "0.6.0"
PRE_1_0_STABLE_LINES = ("0.6.0", "0.7.0", "0.8.0", "0.9.0")
STABLE_SEMVER_RE = re.compile(r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)$")
SEMVER_CORE_RE = re.compile(
    r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)"
    r"(?:-[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?"
    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$"
)


def git_blob_sha1(path: Path) -> str:
    data = path.read_bytes()
    header = f"blob {len(data)}\0".encode("utf-8")
    return hashlib.sha1(header + data).hexdigest()


def semver_core(version: str) -> tuple[int, int, int]:
    match = SEMVER_CORE_RE.fullmatch(version)
    if match is None:
        raise ValueError(f"invalid semantic version: {version!r}")
    return tuple(int(match.group(index)) for index in range(1, 4))


def stable_semver_key(version: str) -> tuple[int, int, int]:
    match = STABLE_SEMVER_RE.fullmatch(version)
    if match is None:
        raise ValueError(f"migration source must be a stable semantic version: {version!r}")
    return tuple(int(match.group(index)) for index in range(1, 4))


def expected_supported_stable_lines(target_version: str) -> list[str]:
    target = semver_core(target_version)
    return [
        version
        for version in PRE_1_0_STABLE_LINES
        if stable_semver_key(version) < target
    ]


def frozen_contract_errors(policy: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    expected_paths = {
        path.relative_to(ROOT).as_posix()
        for path in SCHEMA_ROOT.glob("*.json")
        if path.is_file()
    }
    descriptors = policy["freeze"]["frozen_contracts"]
    declared_paths = {
        descriptor.get("path")
        for descriptor in descriptors
        if isinstance(descriptor, dict) and isinstance(descriptor.get("path"), str)
    }

    if declared_paths != expected_paths:
        missing = sorted(expected_paths - declared_paths)
        extra = sorted(declared_paths - expected_paths)
        if missing:
            errors.append("freeze is missing published schemas: " + ", ".join(missing))
        if extra:
            errors.append("freeze declares unknown schema paths: " + ", ".join(extra))

    seen_paths: set[str] = set()
    seen_schema_ids: set[str] = set()
    for index, descriptor in enumerate(descriptors):
        prefix = f"freeze.frozen_contracts[{index}]"
        path_ref = descriptor["path"]
        schema_id = descriptor["schema_id"]
        if path_ref in seen_paths:
            errors.append(f"{prefix}.path: duplicate frozen contract {path_ref!r}")
            continue
        seen_paths.add(path_ref)
        if schema_id in seen_schema_ids:
            errors.append(f"{prefix}.schema_id: duplicate published schema id {schema_id!r}")
        seen_schema_ids.add(schema_id)

        path = (ROOT / path_ref).resolve()
        if ROOT.resolve() not in path.parents or not path.is_file():
            errors.append(f"{prefix}.path: published schema does not exist")
            continue
        schema = load_json_mapping(path)
        if schema.get("$id") != schema_id:
            errors.append(
                f"{prefix}.schema_id: expected {schema_id!r}, "
                f"file declares {schema.get('$id')!r}"
            )
        actual_sha = git_blob_sha1(path)
        if actual_sha != descriptor["git_blob_sha1"]:
            errors.append(
                f"{prefix}.git_blob_sha1: frozen content changed; "
                f"expected {descriptor['git_blob_sha1']}, got {actual_sha}"
            )
    return errors


def binding_errors(policy: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    protocol = load_yaml_mapping(PROTOCOL_PATH)
    conformance = load_yaml_mapping(CONFORMANCE_PATH)
    manifest = load_yaml_mapping(MANIFEST_PATH)

    protocol_ref = {
        "id": protocol["protocol"]["id"],
        "version": protocol["protocol"]["version"],
    }
    if policy["protocol"] != protocol_ref:
        errors.append("compatibility policy must target protocol id/version exactly")
    if conformance.get("protocol") != protocol_ref:
        errors.append("conformance suite must target the same protocol id/version")
    if manifest.get("protocol") != protocol_ref:
        errors.append("canonical instance must target the same protocol id/version")

    compatibility_contract = protocol.get("contracts", {}).get("compatibility")
    if compatibility_contract != {
        "schema": "schema/compatibility.schema.json",
        "role": "compatibility_freeze_and_migration_policy",
    }:
        errors.append("protocol compatibility contract descriptor is not canonical")

    compatibility_pointer = protocol.get("compatibility")
    expected_status = expected_compatibility_status(protocol_ref["version"])
    if not isinstance(compatibility_pointer, dict):
        errors.append("protocol compatibility policy pointer is missing")
    else:
        if compatibility_pointer.get("policy") != "compatibility.yaml":
            errors.append("protocol compatibility policy pointer is not canonical")
        if compatibility_pointer.get("status") != expected_status:
            errors.append(
                "protocol compatibility status does not match release lifecycle: "
                f"{protocol_ref['version']!r} requires {expected_status!r}"
            )

    suite_compatibility = conformance.get("compatibility")
    expected_suite_compatibility = {
        "capability_unit": policy["freeze"]["capability_unit"],
        "unknown_optional_modules": policy["forward_compatibility"]["unknown_optional_modules"],
        "unknown_required_modules": policy["forward_compatibility"]["unknown_required_modules"],
        "unknown_root_manifest_fields": policy["forward_compatibility"]["unknown_root_manifest_fields"],
    }
    if suite_compatibility != expected_suite_compatibility:
        errors.append("conformance compatibility summary must match compatibility.yaml")

    if manifest.get("schema_version") != policy["freeze"]["manifest_schema_version"]:
        errors.append("canonical instance must use frozen manifest schema version")
    mind = manifest.get("mind")
    if isinstance(mind, dict) and "kind" in mind:
        errors.append("canonical instance reintroduces removed mind.kind")
    if "public_organizations" in manifest:
        errors.append("canonical instance reintroduces removed public_organizations")

    return errors


def migration_policy_errors(policy: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    migration = policy["migration"]
    target_version = policy["protocol"]["version"]
    supported_lines = migration["supported_stable_lines"]

    if migration["floor_inclusive"] != MIGRATION_FLOOR:
        errors.append(f"migration floor must remain {MIGRATION_FLOOR}")
    if supported_lines != sorted(supported_lines, key=stable_semver_key):
        errors.append("supported stable migration lines must be ordered oldest to newest")

    expected_lines = expected_supported_stable_lines(target_version)
    if supported_lines != expected_lines:
        errors.append(
            "supported stable migration lines must match the target release exactly: "
            f"expected {expected_lines!r}, got {supported_lines!r}"
        )
    if supported_lines and supported_lines[0] != MIGRATION_FLOOR:
        errors.append("migration floor must be included as the first supported stable line")
    return errors


def validate_compatibility() -> list[str]:
    policy = load_yaml_mapping(POLICY_PATH)
    schema = load_schema(POLICY_SCHEMA_PATH)
    errors = [
        f"compatibility{error[1:]}"
        for error in schema_errors(Draft202012Validator(schema), policy)
    ]
    if errors:
        return errors
    errors.extend(frozen_contract_errors(policy))
    errors.extend(binding_errors(policy))
    errors.extend(migration_policy_errors(policy))
    return errors


def main() -> int:
    try:
        errors = validate_compatibility()
    except (KeyError, OSError, TypeError, ValueError) as error:
        print(f"compatibility validation failed:\n- {error}", file=sys.stderr)
        return 1

    if errors:
        print("compatibility validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("compatibility policy, schema fingerprints, lifecycle, and migration policy are valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
