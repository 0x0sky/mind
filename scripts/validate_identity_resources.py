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
    load_schema,
    load_yaml_mapping,
    resolve_repository_file,
    schema_errors,
)


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "manifest.yaml"
IDENTITY_SCHEMA = "schema/identity.schema.json"
IDENTITY_RESOURCE_SCHEMA = "schema/identity-resource.schema.json"


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
    manifest: dict[str, Any], repository_root: Path
) -> tuple[list[tuple[str, str, dict[str, Any]]], list[str]]:
    """Discover typed Identity envelopes without assuming a provider or storage backend."""
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
                and resource.get("schema") == IDENTITY_RESOURCE_SCHEMA
            ):
                discovered.append((module_id, resource_id, resource))

    return discovered, errors


def validate_identity_resources(
    manifest: dict[str, Any], repository_root: Path
) -> list[str]:
    errors: list[str] = []
    root = repository_root.resolve()

    try:
        envelope_schema = load_schema(root / IDENTITY_RESOURCE_SCHEMA)
        identity_schema = load_schema(root / IDENTITY_SCHEMA)
    except ValueError as error:
        return [str(error)]

    resources, discovery_errors = discover_identity_resources(manifest, root)
    errors.extend(discovery_errors)

    kind = manifest.get("mind", {}).get("kind")
    if kind != "abstract" and len(resources) != 1:
        errors.append(
            "concrete mind must publish exactly one resource using "
            f"{IDENTITY_RESOURCE_SCHEMA}; found {len(resources)}"
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
            envelope = load_yaml_mapping(resource_path)
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
