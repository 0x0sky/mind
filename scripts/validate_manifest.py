#!/usr/bin/env python3
"""Validate a mind manifest, registered modules, and declared machine resources."""

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
CANONICAL_MODULE_SCHEMA = Path("schema/module.schema.json")
IDENTITY_SCHEMA = Path("schema/identity.schema.json")
LEGACY_ORGANIZATION_FIELDS = {
    "organizations": "public_organizations",
    "memberships": "public_organizations",
    "public_organization": "public_organizations",
}
SUBJECT_TYPE_BY_KIND = {
    "abstract": "unspecified",
    "personal": "person",
    "organization": "organization",
    "agent": "agent",
    "project": "project",
    "product": "product",
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
        help="only parse manifest YAML and reject duplicate keys/documents",
    )
    return parser.parse_args()


def load_yaml_mapping(path: Path) -> dict[str, Any]:
    try:
        documents = list(
            yaml.load_all(path.read_text(encoding="utf-8"), Loader=UniqueKeyLoader)
        )
    except OSError as error:
        raise ValueError(f"cannot read {path}: {error}") from error
    except yaml.YAMLError as error:
        raise ValueError(f"invalid YAML in {path}: {error}") from error

    if len(documents) != 1:
        raise ValueError(f"{path} must contain exactly one YAML document")
    value = documents[0]
    if not isinstance(value, dict):
        raise ValueError(f"{path} root must be a YAML mapping")
    if not all(isinstance(key, str) for key in value):
        raise ValueError(f"{path} root keys must be strings")
    return value


def load_json_mapping(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except OSError as error:
        raise ValueError(f"cannot read {path}: {error}") from error
    except json.JSONDecodeError as error:
        raise ValueError(f"invalid JSON in {path}: {error}") from error
    if not isinstance(value, dict):
        raise ValueError(f"{path} root must be a JSON object")
    return value


def load_schema(path: Path) -> dict[str, Any]:
    schema = load_json_mapping(path)
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
    validator: Draft202012Validator, value: dict[str, Any]
) -> list[str]:
    errors = sorted(
        validator.iter_errors(value),
        key=lambda error: tuple(str(part) for part in error.absolute_path),
    )
    return [f"{json_path(error.absolute_path)}: {error.message}" for error in errors]


def validate_public_organizations_schema_contract(
    validator: Draft202012Validator, manifest: dict[str, Any]
) -> list[str]:
    """Preserve omission, empty, and explicit authored relations as distinct states."""
    errors: list[str] = []
    accepted: tuple[tuple[str, object], ...] = (
        ("omitted", object()),
        ("empty", []),
        ("populated", ["example-org"]),
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
                f"{label}; omission=provider-discovered, []=none, and a list=authored"
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


def resolve_repository_file(
    root: Path, relative_path: str, label: str, errors: list[str]
) -> Path | None:
    candidate = (root / relative_path).resolve()
    if candidate != root and root not in candidate.parents:
        errors.append(f"{label}: path escapes repository: {relative_path}")
        return None
    if not candidate.is_file():
        errors.append(f"{label}: file does not exist: {relative_path}")
        return None
    return candidate


def validate_manifest_semantics(
    manifest: dict[str, Any], repository_root: Path
) -> list[str]:
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
    expected_subject_type = SUBJECT_TYPE_BY_KIND[mind["kind"]]
    if mind["subject"]["type"] != expected_subject_type:
        errors.append(
            "$.mind.subject.type: "
            f"{mind['kind']!r} mind requires subject type {expected_subject_type!r}"
        )
    if mind["kind"] != "abstract" and mind["subject"]["id"] == "unspecified":
        errors.append("$.mind.subject.id: concrete minds cannot use 'unspecified'")
    if mind["kind"] == "abstract":
        if mind["subject"] != {"type": "unspecified", "id": "unspecified"}:
            errors.append(
                "$.mind.subject: abstract minds must use the explicit unspecified subject"
            )
        if mind["owner"] != {"type": "unspecified", "id": "unspecified"}:
            errors.append(
                "$.mind.owner: abstract minds must use the explicit unspecified owner"
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

    if mind["kind"] != "abstract" and "identity" not in required:
        errors.append("$.modules.required: concrete minds must require the identity module")

    root = repository_root.resolve()
    for module_id, relative_path in modules["catalog"].items():
        resolve_repository_file(
            root, relative_path, f"$.modules.catalog.{module_id}", errors
        )

    validation = manifest["validation"]
    schema_reference = validation["schema"]
    resolved_schema = resolve_repository_file(
        root, schema_reference, "$.validation.schema", errors
    )
    if resolved_schema is not None and resolved_schema != (root / CANONICAL_SCHEMA).resolve():
        errors.append(
            "$.validation.schema: must resolve to "
            f"{CANONICAL_SCHEMA.as_posix()}"
        )

    module_schema_reference = validation["module_schema"]
    resolved_module_schema = resolve_repository_file(
        root, module_schema_reference, "$.validation.module_schema", errors
    )
    if (
        resolved_module_schema is not None
        and resolved_module_schema != (root / CANONICAL_MODULE_SCHEMA).resolve()
    ):
        errors.append(
            "$.validation.module_schema: must resolve to "
            f"{CANONICAL_MODULE_SCHEMA.as_posix()}"
        )

    return errors


def validate_resource(
    root: Path,
    module_id: str,
    resource_id: str,
    resource: dict[str, Any],
    manifest: dict[str, Any],
    errors: list[str],
) -> None:
    prefix = f"module[{module_id}].resources.{resource_id}"
    resource_path = resolve_repository_file(root, resource["path"], f"{prefix}.path", errors)
    schema_path = resolve_repository_file(
        root, resource["schema"], f"{prefix}.schema", errors
    )
    if resource_path is None or schema_path is None:
        return

    try:
        schema = load_schema(schema_path)
    except ValueError as error:
        errors.append(f"{prefix}.schema: {error}")
        return

    try:
        if resource["format"] == "yaml":
            value = load_yaml_mapping(resource_path)
        else:
            value = load_json_mapping(resource_path)
    except ValueError as error:
        errors.append(f"{prefix}.path: {error}")
        return

    validator = Draft202012Validator(schema)
    errors.extend(f"{prefix}{error[1:]}" for error in schema_errors(validator, value))

    if resource["schema"] == IDENTITY_SCHEMA.as_posix():
        identity = value.get("identity")
        if isinstance(identity, dict):
            subject = manifest["mind"]["subject"]
            if identity.get("type") != subject["type"] or identity.get("id") != subject["id"]:
                errors.append(
                    f"{prefix}: identity type/id must match $.mind.subject exactly"
                )
            visual_identity = identity.get("visual_identity")
            if isinstance(visual_identity, dict):
                primary_mark = visual_identity.get("primary_mark")
                if isinstance(primary_mark, dict):
                    asset = primary_mark.get("asset")
                    if isinstance(asset, dict) and isinstance(asset.get("path"), str):
                        resolve_repository_file(
                            root,
                            asset["path"],
                            f"{prefix}.identity.visual_identity.primary_mark.asset.path",
                            errors,
                        )


def find_cycle(graph: dict[str, set[str]]) -> list[str] | None:
    visiting: set[str] = set()
    visited: set[str] = set()
    stack: list[str] = []

    def visit(node: str) -> list[str] | None:
        if node in visiting:
            start = stack.index(node)
            return stack[start:] + [node]
        if node in visited:
            return None
        visiting.add(node)
        stack.append(node)
        for dependency in sorted(graph.get(node, set())):
            cycle = visit(dependency)
            if cycle is not None:
                return cycle
        stack.pop()
        visiting.remove(node)
        visited.add(node)
        return None

    for node in sorted(graph):
        cycle = visit(node)
        if cycle is not None:
            return cycle
    return None


def validate_modules(
    manifest: dict[str, Any], repository_root: Path
) -> list[str]:
    errors: list[str] = []
    root = repository_root.resolve()

    module_schema_path = root / manifest["validation"]["module_schema"]
    try:
        module_schema = load_schema(module_schema_path)
    except ValueError as error:
        return [str(error)]
    validator = Draft202012Validator(module_schema)

    registered = set(manifest["modules"]["registered"])
    graph: dict[str, set[str]] = {}

    for catalog_id, relative_path in manifest["modules"]["catalog"].items():
        descriptor_path = resolve_repository_file(
            root, relative_path, f"$.modules.catalog.{catalog_id}", errors
        )
        if descriptor_path is None:
            continue
        try:
            descriptor = load_yaml_mapping(descriptor_path)
        except ValueError as error:
            errors.append(f"module[{catalog_id}]: {error}")
            continue

        errors.extend(
            f"module[{catalog_id}]{error[1:]}"
            for error in schema_errors(validator, descriptor)
        )
        module = descriptor.get("module")
        if not isinstance(module, dict):
            continue

        descriptor_id = module.get("id")
        if descriptor_id != catalog_id:
            errors.append(
                f"module[{catalog_id}].id: descriptor declares {descriptor_id!r}"
            )

        dependencies = {
            dependency
            for dependency in module.get("dependencies", [])
            if isinstance(dependency, str)
        }
        unknown_dependencies = dependencies - registered
        if unknown_dependencies:
            errors.append(
                f"module[{catalog_id}].dependencies contains unregistered modules: "
                + ", ".join(sorted(unknown_dependencies))
            )
        if catalog_id in dependencies:
            errors.append(f"module[{catalog_id}].dependencies: self-dependency is forbidden")
        graph[catalog_id] = dependencies & registered

        for index, entrypoint in enumerate(module.get("entrypoints", [])):
            if isinstance(entrypoint, str):
                resolve_repository_file(
                    root,
                    entrypoint,
                    f"module[{catalog_id}].entrypoints[{index}]",
                    errors,
                )

        resources = module.get("resources", {})
        if isinstance(resources, dict):
            for resource_id, resource in resources.items():
                if isinstance(resource, dict):
                    validate_resource(
                        root,
                        catalog_id,
                        resource_id,
                        resource,
                        manifest,
                        errors,
                    )

    cycle = find_cycle(graph)
    if cycle is not None:
        errors.append("module dependency graph contains cycle: " + " -> ".join(cycle))

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
        manifest = load_yaml_mapping(manifest_path)
    except ValueError as error:
        print(f"mind validation failed:\n- {error}", file=sys.stderr)
        return 1

    if arguments.syntax_only:
        print(f"manifest YAML syntax is valid: {manifest_path}")
        return 0

    schema_path = repository_root / CANONICAL_SCHEMA
    try:
        schema = load_schema(schema_path)
    except ValueError as error:
        print(f"mind validation failed:\n- {error}", file=sys.stderr)
        return 1

    validator = Draft202012Validator(schema)
    errors = legacy_field_errors(manifest)
    errors.extend(schema_errors(validator, manifest))
    if not errors:
        errors.extend(validate_public_organizations_schema_contract(validator, manifest))
        errors.extend(validate_manifest_semantics(manifest, repository_root))
        if not errors:
            errors.extend(validate_modules(manifest, repository_root))

    if errors:
        print("mind validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"mind contract is valid: {manifest_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
