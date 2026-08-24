#!/usr/bin/env python3
# © 2026 aiaiaiai · aiaiaiai.org
# SPDX-License-Identifier: MIT
"""Validate authored relationship semantics and legacy projection compatibility."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

from validate_manifest import load_yaml_mapping


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = REPOSITORY_ROOT / "manifest.yaml"
RELATIONSHIPS_SCHEMA = "schema/relationships.schema.json"


def entity_ref(value: dict[str, Any]) -> tuple[str, str]:
    return str(value["type"]), str(value["id"])


def repository_file(relative_path: str) -> Path:
    root = REPOSITORY_ROOT.resolve()
    path = (root / relative_path).resolve()
    if path != root and root not in path.parents:
        raise ValueError(f"path escapes repository: {relative_path}")
    if not path.is_file():
        raise ValueError(f"file does not exist: {relative_path}")
    return path


def load_relationships_resource(
    manifest: dict[str, Any],
) -> tuple[dict[str, Any] | None, list[str]]:
    errors: list[str] = []
    registered = set(manifest.get("modules", {}).get("registered", []))
    if "relationships" not in registered:
        return None, errors

    catalog = manifest.get("modules", {}).get("catalog", {})
    descriptor_ref = catalog.get("relationships")
    if not isinstance(descriptor_ref, str):
        return None, ["$.modules.catalog.relationships: relationships module must be catalogued"]

    try:
        descriptor = load_yaml_mapping(repository_file(descriptor_ref))
    except ValueError as error:
        return None, [f"relationships module: {error}"]

    module = descriptor.get("module")
    resources = module.get("resources") if isinstance(module, dict) else None
    relationship_resource = resources.get("relationships") if isinstance(resources, dict) else None
    if not isinstance(relationship_resource, dict):
        return None, ["relationships module must declare resources.relationships"]

    if relationship_resource.get("schema") != RELATIONSHIPS_SCHEMA:
        errors.append("relationships resource must use schema/relationships.schema.json")

    resource_ref = relationship_resource.get("path")
    if not isinstance(resource_ref, str):
        errors.append("relationships resource must declare a repository-relative path")
        return None, errors

    try:
        resource = load_yaml_mapping(repository_file(resource_ref))
    except ValueError as error:
        errors.append(f"relationships resource: {error}")
        return None, errors
    return resource, errors


def validate_relationships(
    manifest: dict[str, Any], resource: dict[str, Any]
) -> list[str]:
    errors: list[str] = []
    subject = entity_ref(manifest["mind"]["subject"])
    owner = entity_ref(manifest["mind"]["owner"])
    relationships = resource.get("relationships", [])

    seen_ids: set[str] = set()
    authored_memberships: set[str] = set()

    for index, relationship in enumerate(relationships):
        prefix = f"$.relationships[{index}]"
        relationship_id = relationship["id"]
        if relationship_id in seen_ids:
            errors.append(f"{prefix}.id: duplicate relationship id {relationship_id!r}")
        seen_ids.add(relationship_id)

        source = entity_ref(relationship["source"])
        target = entity_ref(relationship["target"])
        if source == target:
            errors.append(f"{prefix}: source and target must identify different entities")

        if subject not in (source, target):
            errors.append(f"{prefix}: canonical relationships must involve $.mind.subject")

        authority = entity_ref(relationship["provenance"]["authority"])
        if authority != owner:
            errors.append(f"{prefix}.provenance.authority: must match $.mind.owner")

        predicate = relationship["predicate"]
        if predicate == "member_of":
            if relationship["direction"] != "directed":
                errors.append(f"{prefix}.direction: member_of must be directed")
            if target[0] != "organization":
                errors.append(f"{prefix}.target.type: member_of target must be organization")
            if source == subject and target[0] == "organization":
                authored_memberships.add(target[1].casefold())

        confirmation = relationship["confirmation"]
        if confirmation["state"] == "reciprocal":
            counterpart = entity_ref(confirmation["counterpart"]["entity"])
            expected_counterpart = target if source == subject else source
            if counterpart != expected_counterpart:
                errors.append(
                    f"{prefix}.confirmation.counterpart.entity: "
                    "must identify the other relationship endpoint"
                )

    public_organizations = manifest.get("public_organizations")
    if isinstance(public_organizations, list):
        for index, organization in enumerate(public_organizations):
            if organization.casefold() not in authored_memberships:
                errors.append(
                    "$.public_organizations"
                    f"[{index}]: legacy projection must be backed by an authored "
                    "member_of relationship from $.mind.subject"
                )

    return errors


def main() -> int:
    try:
        manifest = load_yaml_mapping(MANIFEST_PATH)
        resource, errors = load_relationships_resource(manifest)
    except (KeyError, TypeError, ValueError) as error:
        print(f"relationship validation failed:\n- {error}", file=sys.stderr)
        return 1

    if resource is not None and not errors:
        try:
            errors.extend(validate_relationships(manifest, resource))
        except (KeyError, TypeError) as error:
            errors.append(f"relationships resource is structurally incomplete: {error}")

    if errors:
        print("relationship validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("relationship contract is valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
