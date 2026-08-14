#!/usr/bin/env python3
"""Validate manifest.yaml syntax, schema, and cross-field invariants."""

from __future__ import annotations

import argparse
import copy
import json
import sys
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError
from yaml.constructor import ConstructorError
from yaml.resolver import BaseResolver


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = REPOSITORY_ROOT / "manifest.yaml"
CANONICAL_SCHEMA = Path("schema/mind.schema.json")
LEGACY_ORGANIZATION_FIELDS = {
    "organizations": "public_organizations",
    "memberships": "public_organizations",
    "public_organization": "public_organizations",
}


class UniqueKeyLoader(yaml.SafeLoader):
    """Safe YAML loader that rejects duplicate mapping keys."""


def construct_unique_mapping(
    loader: UniqueKeyLoader, node: yaml.MappingNode, deep: bool = False
) -> dict[Any, Any]:
    loader.flatten_mapping(node)
    mapping: dict[Any, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        try:
            duplicate = key in mapping
        except TypeError as error:
            raise ConstructorError(
                "while constructing a mapping",
                node.start_mark,
                "found an unhashable mapping key",
                key_node.start_mark,
            ) from error
        if duplicate:
            raise ConstructorError(
                "while constructing a mapping",
                node.start_mark,
                f"found duplicate key {key!r}",
                key_node.start_mark,
            )
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueKeyLoader.add_constructor(
    BaseResolver.DEFAULT_MAPPING_TAG,
    construct_unique_mapping,
)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--manifest",
        type=Path,
        default=DEFAULT_MANIFEST,
        help="manifest path (default: repository manifest.yaml)",
    )
    parser.add_argument(
        "--syntax-only",
        action="store_true",
        help="only parse YAML and reject duplicate keys/documents",
    )
    return parser.parse_args()


def load_manifest(path: Path) -> dict[str, Any]:
    try:
        documents = list(yaml.load_all(path.read_text(encoding="utf-8"), Loader=UniqueKeyLoader))
    except OSError as error:
        raise ValueError(f"cannot read {path}: {error}") from error
    except yaml.YAMLError as error:
        raise ValueError(f"invalid YAML in {path}: {error}") from error

    if len(documents) != 1:
        raise ValueError(f"{path} must contain exactly one YAML document")
    manifest = documents[0]
    if not isinstance(manifest, dict):
        raise ValueError(f"{path} root must be a YAML mapping")
    if not all(isinstance(key, str) for key in manifest):
        raise ValueError(f"{path} root keys must be strings")
    return manifest


def load_schema(path: Path) -> dict[str, Any]:
    try:
        schema = json.loads(path.read_text(encoding="utf-8"))
    except OSError as error:
        raise ValueError(f"cannot read {path}: {error}") from error
    except json.JSONDecodeError as error:
        raise ValueError(f"invalid JSON Schema syntax in {path}: {error}") from error

    try:
        Draft202012Validator.check_schema(schema)
    except SchemaError as error:
        raise ValueError(f"invalid Draft 2020-12 schema in {path}: {error.message}") from error
    return schema


def json_path(parts: Any) -> str:
    location = "$"
    for part in parts:
        location += f"[{part}]" if isinstance(part, int) else f".{part}"
    return location


def schema_errors(
    validator: Draft202012Validator, manifest: dict[str, Any]
) -> list[str]:
    errors = sorted(
        validator.iter_errors(manifest),
        key=lambda error: tuple(str(part) for part in error.absolute_path),
    )
    return [f"{json_path(error.absolute_path)}: {error.message}" for error in errors]


def validate_public_organizations_schema_contract(
    validator: Draft202012Validator, manifest: dict[str, Any]
) -> list[str]:
    """Keep omission, empty allowlist, and populated allowlist as distinct valid states."""
    errors: list[str] = []
    accepted: tuple[tuple[str, object], ...] = (
        ("omitted", object()),
        ("empty", []),
        ("allowlist", ["example-org"]),
    )
    for label, value in accepted:
        candidate = copy.deepcopy(manifest)
        if label == "omitted":
            candidate.pop("public_organizations", None)
        else:
            candidate["public_organizations"] = value
        if schema_errors(validator, candidate):
            errors.append(
                "schema must accept public_organizations when it is "
                f"{label}; omission=all, []=none, and a list=allowlist"
            )

    rejected = {
        "a scalar": "example-org",
        "an invalid GitHub organization ID": ["invalid organization"],
        "an exact duplicate": ["example-org", "example-org"],
    }
    for label, value in rejected.items():
        candidate = copy.deepcopy(manifest)
        candidate["public_organizations"] = value
        if not schema_errors(validator, candidate):
            errors.append(f"schema must reject public_organizations containing {label}")
    return errors


def set_difference_message(prefix: str, values: set[str]) -> str | None:
    if not values:
        return None
    return f"{prefix}: {', '.join(sorted(values))}"


def validate_semantics(manifest: dict[str, Any], repository_root: Path) -> list[str]:
    errors: list[str] = []

    public_organizations = manifest.get("public_organizations")
    if isinstance(public_organizations, list):
        first_index: dict[str, int] = {}
        for index, organization in enumerate(public_organizations):
            if not isinstance(organization, str):
                continue
            normalized = organization.casefold()
            if normalized in first_index:
                errors.append(
                    "$.public_organizations"
                    f"[{index}]: duplicates index {first_index[normalized]} "
                    "when GitHub IDs are compared case-insensitively"
                )
            else:
                first_index[normalized] = index

    mind = manifest["mind"]
    expected_owner_types = {
        "personal": "person",
        "organization": "organization",
        "project": "project",
        "product": "product",
    }
    expected_owner_type = expected_owner_types.get(mind["kind"])
    if expected_owner_type and mind["owner"]["type"] != expected_owner_type:
        errors.append(
            "$.mind.owner.type: "
            f"{mind['kind']!r} mind requires owner type {expected_owner_type!r}"
        )

    modules = manifest["modules"]
    registered = set(modules["registered"])
    required = set(modules["required"])
    catalog = set(modules["catalog"])
    default = set(manifest["loading"]["default"])
    optional = set(manifest["loading"]["optional"])

    checks = (
        set_difference_message(
            "$.modules.required contains unregistered modules", required - registered
        ),
        set_difference_message(
            "$.modules.catalog is missing registered modules", registered - catalog
        ),
        set_difference_message(
            "$.modules.catalog contains unregistered modules", catalog - registered
        ),
        set_difference_message(
            "$.loading.default contains unregistered modules", default - registered
        ),
        set_difference_message(
            "$.loading.optional contains unregistered modules", optional - registered
        ),
        set_difference_message(
            "$.loading.default is missing required modules", required - default
        ),
        set_difference_message(
            "registered modules without a loading policy", registered - default - optional
        ),
        set_difference_message(
            "modules cannot be both default and optional", default & optional
        ),
    )
    errors.extend(check for check in checks if check is not None)

    root = repository_root.resolve()
    for module_id, relative_path in modules["catalog"].items():
        descriptor = (root / relative_path).resolve()
        if descriptor != root and root not in descriptor.parents:
            errors.append(
                f"$.modules.catalog.{module_id}: path escapes repository: {relative_path}"
            )
        elif not descriptor.is_file():
            errors.append(
                f"$.modules.catalog.{module_id}: descriptor does not exist: {relative_path}"
            )

    schema_reference = manifest["validation"]["schema"]
    resolved_schema = (root / schema_reference).resolve()
    canonical_schema = (root / CANONICAL_SCHEMA).resolve()
    if resolved_schema != canonical_schema:
        errors.append(
            "$.validation.schema: must resolve to " f"{CANONICAL_SCHEMA.as_posix()}"
        )
    elif not resolved_schema.is_file():
        errors.append(f"$.validation.schema: file does not exist: {schema_reference}")

    return errors


def legacy_field_errors(manifest: dict[str, Any]) -> list[str]:
    return [
        f"$.{field}: legacy field is forbidden; use {replacement}"
        for field, replacement in LEGACY_ORGANIZATION_FIELDS.items()
        if field in manifest
    ]


def main() -> int:
    arguments = parse_arguments()
    manifest_path = arguments.manifest.resolve()
    repository_root = manifest_path.parent

    try:
        manifest = load_manifest(manifest_path)
    except ValueError as error:
        print(f"manifest validation failed:\n- {error}", file=sys.stderr)
        return 1

    if arguments.syntax_only:
        print(f"manifest YAML syntax is valid: {manifest_path}")
        return 0

    schema_path = repository_root / CANONICAL_SCHEMA
    try:
        schema = load_schema(schema_path)
    except ValueError as error:
        print(f"manifest validation failed:\n- {error}", file=sys.stderr)
        return 1

    validator = Draft202012Validator(schema)
    errors = legacy_field_errors(manifest)
    errors.extend(schema_errors(validator, manifest))
    if not errors:
        errors.extend(validate_public_organizations_schema_contract(validator, manifest))
        errors.extend(validate_semantics(manifest, repository_root))

    if errors:
        print("manifest validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"manifest contract is valid: {manifest_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
