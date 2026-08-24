#!/usr/bin/env python3
# © 2026 aiaiaiai · aiaiaiai.org
# SPDX-License-Identifier: MIT
"""Validate concrete Identity envelopes against universal Identity semantics."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from validate_manifest import (
    load_json_mapping,
    load_schema,
    load_yaml_mapping,
    resolve_repository_file,
    schema_errors,
)


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "manifest.yaml"
PROTOCOL_PATH = ROOT / "protocol.yaml"


def validate_identity_envelope(
    envelope: dict[str, Any],
    manifest: dict[str, Any],
    envelope_schema: dict[str, Any],
    identity_schema: dict[str, Any],
) -> list[str]:
    """Validate one concrete envelope plus its embedded universal Identity value."""
    errors = [
        f"identity-resource{error[1:]}"
        for error in schema_errors(Draft202012Validator(envelope_schema), envelope)
    ]
    if errors:
        return errors

    identity = envelope.get("identity")
    if not isinstance(identity, dict):
        return ["identity-resource.identity: must be a mapping"]

    errors.extend(
        f"identity{error[1:]}"
        for error in schema_errors(Draft202012Validator(identity_schema), identity)
    )

    subject = manifest.get("mind", {}).get("subject")
    if not isinstance(subject, dict):
        errors.append("manifest mind.subject must be a mapping")
        return errors

    if identity.get("type") != subject.get("type") or identity.get("id") != subject.get("id"):
        errors.append("identity type/id must match manifest mind.subject exactly")

    return errors


def discover_identity_resources(
    manifest: dict[str, Any],
    repository_root: Path,
    identity_resource_schema_ref: str,
) -> tuple[list[tuple[str, str, dict[str, Any]]], list[str]]:
    """Discover typed Identity envelopes without assuming provider or resource location."""
    errors: list[str] = []
    discovered: list[tuple[str, str, dict[str, Any]]] = []
    root = repository_root.resolve()

    catalog = manifest.get("modules", {}).get("catalog", {})
    if not isinstance(catalog, dict):
        return discovered, ["manifest modules.catalog must be a mapping"]

    for module_id, descriptor_ref in catalog.items():
        if not isinstance(module_id, str) or not isinstance(descriptor_ref, str):
            continue
        descriptor_path = resolve_repository_file(
            root,
            descriptor_ref,
            f"$.modules.catalog.{module_id}",
            errors,
        )
        if descriptor_path is None:
            continue
        try:
            descriptor = load_yaml_mapping(descriptor_path)
        except ValueError as error:
            errors.append(f"module[{module_id}]: {error}")
            continue

        resources = descriptor.get("module", {}).get("resources", {})
        if not isinstance(resources, dict):
            continue
        for resource_id, resource in resources.items():
            if (
                isinstance(resource_id, str)
                and isinstance(resource, dict)
                and resource.get("schema") == identity_resource_schema_ref
            ):
                discovered.append((module_id, resource_id, resource))

    return discovered, errors


def validate_identity_resources(
    manifest: dict[str, Any], repository_root: Path
) -> list[str]:
    errors: list[str] = []
    root = repository_root.resolve()

    try:
        protocol = load_yaml_mapping(root / "protocol.yaml")
        contracts = protocol["contracts"]
        identity_schema_ref = contracts["identity"]["schema"]
        identity_resource_schema_ref = contracts["identity_resource"]["schema"]
        if not isinstance(identity_schema_ref, str) or not isinstance(
            identity_resource_schema_ref, str
        ):
            return ["protocol Identity contract schema refs must be strings"]
        envelope_schema = load_schema(root / identity_resource_schema_ref)
        identity_schema = load_schema(root / identity_schema_ref)
    except (KeyError, TypeError, ValueError) as error:
        return [f"cannot load protocol Identity contracts: {error}"]

    resources, discovery_errors = discover_identity_resources(
        manifest,
        root,
        identity_resource_schema_ref,
    )
    errors.extend(discovery_errors)

    kind = manifest.get("mind", {}).get("kind")
    if kind != "abstract" and len(resources) != 1:
        errors.append(
            "concrete mind must publish exactly one resource using "
            f"{identity_resource_schema_ref}; found {len(resources)}"
        )

    for module_id, resource_id, resource in resources:
        prefix = f"module[{module_id}].resources.{resource_id}"
        resource_path_ref = resource.get("path")
        if not isinstance(resource_path_ref, str):
            errors.append(f"{prefix}.path: must be a string")
            continue
        resource_path = resolve_repository_file(
            root, resource_path_ref, f"{prefix}.path", errors
        )
        if resource_path is None:
            continue

        try:
            resource_format = resource.get("format")
            if resource_format == "yaml":
                envelope = load_yaml_mapping(resource_path)
            elif resource_format == "json":
                envelope = load_json_mapping(resource_path)
            else:
                errors.append(
                    f"{prefix}.format: unsupported identity resource format {resource_format!r}"
                )
                continue
        except ValueError as error:
            errors.append(f"{prefix}.path: {error}")
            continue

        errors.extend(
            f"{prefix}: {error}"
            for error in validate_identity_envelope(
                envelope,
                manifest,
                envelope_schema,
                identity_schema,
            )
        )

    return errors


def main() -> int:
    try:
        manifest = load_yaml_mapping(MANIFEST_PATH)
        errors = validate_identity_resources(manifest, ROOT)
    except (KeyError, TypeError, ValueError) as error:
        print(f"identity resource validation failed:\n- {error}", file=sys.stderr)
        return 1

    if errors:
        print("identity resource validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("identity resources implement universal Identity correctly")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
