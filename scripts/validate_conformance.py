#!/usr/bin/env python3
# © 2026 aiaiaiai · aiaiaiai.org
# SPDX-License-Identifier: MIT
"""Run Mind Protocol conformance through independent schema and minimal-reader modes."""

from __future__ import annotations

import argparse
import copy
import json
import re
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from validate_identity_resources import validate_identity_envelope
from validate_manifest import load_schema, load_yaml_mapping, schema_errors


ROOT = Path(__file__).resolve().parents[1]
SUITE_PATH = ROOT / "conformance.yaml"
PROTOCOL_PATH = ROOT / "protocol.yaml"
CONFORMANCE_SCHEMA_PATH = ROOT / "schema/conformance.schema.json"
MIND_SCHEMA_PATH = ROOT / "schema/mind.schema.json"
IDENTITY_SCHEMA_PATH = ROOT / "schema/identity.schema.json"
IDENTITY_RESOURCE_SCHEMA_PATH = ROOT / "schema/identity-resource.schema.json"
KNOWN_MODULES = frozenset({"identity"})
KIND_BY_TYPE = {
    "person": "personal",
    "organization": "organization",
    "agent": "agent",
    "project": "project",
    "product": "product",
}
SEMVER_CORE = re.compile(r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)")


def semver_core(value: str) -> tuple[int, int, int]:
    match = SEMVER_CORE.match(value)
    if match is None:
        raise ValueError(f"invalid semantic version: {value!r}")
    return tuple(int(part) for part in match.groups())


def build_manifest(fixture: dict[str, Any], protocol: dict[str, Any]) -> dict[str, Any]:
    subject = copy.deepcopy(fixture["subject"])
    owner = copy.deepcopy(fixture["owner"])
    return {
        "schema_version": 2,
        "protocol": copy.deepcopy(protocol),
        "mind": {
            "name": f"mind@{subject['id']}",
            "kind": fixture["kind"],
            "context_version": "1.0.0",
            "subject": subject,
            "owner": owner,
        },
        "contract": {
            "canonical_source": "required",
            "explicit_subject": "required",
            "explicit_owner": "required",
            "versioned_context": "required",
            "human_readable": "required",
            "machine_readable": "required",
            "secrets": "forbidden",
        },
        "modules": {
            "required": ["identity"],
            "registered": ["identity"],
            "rules": {
                "single_responsibility": "required",
                "explicit_dependencies": "required",
                "independently_replaceable": "required",
                "duplicate_content": "forbidden",
                "cross_reference": "preferred",
                "composition_over_inheritance": "preferred",
            },
            "catalog": {"identity": "identity/module.yaml"},
        },
        "context": {
            "stability": {
                "stable": "long_lived_contracts",
                "transient": "current_state",
                "archived": "ignored_unless_requested",
            },
            "visibility": {
                "repository": "public",
                "allowed": "synthetic_conformance_context",
                "forbidden": ["credentials", "secrets"],
            },
        },
        "loading": {"default": ["identity"], "optional": []},
        "validation": {
            "schema": "schema/mind.schema.json",
            "module_schema": "schema/module.schema.json",
        },
    }


def build_identity_envelope(fixture: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "identity": {
            "type": fixture["subject"]["type"],
            "id": fixture["subject"]["id"],
            "display_name": fixture["display_name"],
        },
        "validation": {"schema": "schema/identity-resource.schema.json"},
    }


def range_errors(suite: dict[str, Any], protocol: dict[str, Any]) -> list[str]:
    version = semver_core(protocol["version"])
    minimum = semver_core(suite["supported_range"]["minimum_inclusive"])
    maximum = semver_core(suite["supported_range"]["maximum_exclusive"])
    if not minimum <= version < maximum:
        return ["protocol version is outside conformance supported_range"]
    return []


def fixture_semantic_errors(fixture_id: str, fixture: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    subject_type = fixture.get("subject", {}).get("type")
    if subject_type != fixture_id:
        errors.append(f"fixture {fixture_id!r} subject.type must match fixture id")
    if KIND_BY_TYPE.get(subject_type) != fixture.get("kind"):
        errors.append(f"fixture {fixture_id!r} kind does not match subject type")
    if fixture.get("owner", {}).get("type") not in KIND_BY_TYPE:
        errors.append(f"fixture {fixture_id!r} owner must be a concrete entity")
    return errors


def consumer_module_errors(manifest: dict[str, Any]) -> list[str]:
    required = set(manifest["modules"]["required"])
    default = set(manifest["loading"]["default"])
    unknown_required = required - KNOWN_MODULES
    unknown_default = default - KNOWN_MODULES
    errors: list[str] = []
    if unknown_required:
        errors.append("unknown required modules: " + ", ".join(sorted(unknown_required)))
    if unknown_default:
        errors.append("unknown default-loaded modules: " + ", ".join(sorted(unknown_default)))
    return errors


def compatibility_probe_errors(base_manifest: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    optional = copy.deepcopy(base_manifest)
    optional["modules"]["registered"].append("future_extension")
    optional["modules"]["catalog"]["future_extension"] = "future_extension/module.yaml"
    optional["loading"]["optional"].append("future_extension")
    if consumer_module_errors(optional):
        errors.append("unknown optional module must be ignored when not requested")

    required = copy.deepcopy(optional)
    required["loading"]["optional"].remove("future_extension")
    required["modules"]["required"].append("future_extension")
    required["loading"]["default"].append("future_extension")
    if not consumer_module_errors(required):
        errors.append("unknown required module must be rejected")
    return errors


def schema_mode(suite: dict[str, Any], protocol_descriptor: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    suite_schema = load_schema(CONFORMANCE_SCHEMA_PATH)
    errors.extend(
        f"suite{error[1:]}"
        for error in schema_errors(Draft202012Validator(suite_schema), suite)
    )
    if errors:
        return errors

    protocol = {"id": protocol_descriptor["protocol"]["id"], "version": protocol_descriptor["protocol"]["version"]}
    if suite["protocol"] != protocol:
        errors.append("conformance suite protocol id/version must match protocol.yaml")
    errors.extend(range_errors(suite, protocol))

    feature_ids = [feature["id"] for feature in suite["features"]]
    if len(feature_ids) != len(set(feature_ids)):
        errors.append("feature matrix contains duplicate ids")

    mind_schema = load_schema(MIND_SCHEMA_PATH)
    identity_schema = load_schema(IDENTITY_SCHEMA_PATH)
    envelope_schema = load_schema(IDENTITY_RESOURCE_SCHEMA_PATH)
    validator = Draft202012Validator(mind_schema)

    for fixture_id in suite["fixture_types"]:
        fixture = suite["fixtures"][fixture_id]
        errors.extend(fixture_semantic_errors(fixture_id, fixture))
        manifest = build_manifest(fixture, protocol)
        errors.extend(
            f"fixture[{fixture_id}].manifest{error[1:]}"
            for error in schema_errors(validator, manifest)
        )
        errors.extend(
            f"fixture[{fixture_id}].manifest: {error}"
            for error in consumer_module_errors(manifest)
        )
        envelope = build_identity_envelope(fixture)
        errors.extend(
            f"fixture[{fixture_id}]: {error}"
            for error in validate_identity_envelope(
                envelope, manifest, envelope_schema, identity_schema
            )
        )

    person_manifest = build_manifest(suite["fixtures"]["person"], protocol)
    optional = copy.deepcopy(person_manifest)
    optional["modules"]["registered"].append("future_extension")
    optional["modules"]["catalog"]["future_extension"] = "future_extension/module.yaml"
    optional["loading"]["optional"].append("future_extension")
    if schema_errors(validator, optional):
        errors.append("manifest schema must accept a registered unknown optional module")
    errors.extend(compatibility_probe_errors(person_manifest))
    return errors


def minimal_mode(suite: dict[str, Any], protocol_descriptor: dict[str, Any]) -> list[str]:
    """Independent reader mode: deliberately avoids JSON Schema and shared validators."""
    errors: list[str] = []
    protocol = protocol_descriptor.get("protocol")
    if not isinstance(protocol, dict):
        return ["protocol descriptor must contain protocol mapping"]
    target = {"id": protocol.get("id"), "version": protocol.get("version")}
    if suite.get("protocol") != target:
        errors.append("minimal reader: suite protocol does not match descriptor")
    try:
        errors.extend(range_errors(suite, target))
    except (KeyError, TypeError, ValueError) as error:
        errors.append(f"minimal reader: {error}")
        return errors

    expected_types = ["person", "organization", "agent", "project", "product"]
    if suite.get("fixture_types") != expected_types:
        errors.append("minimal reader: fixture_types must contain the five canonical types")
    if suite.get("consumer_modes") != ["schema", "minimal"]:
        errors.append("minimal reader: two declared consumer modes are required")
    compatibility = suite.get("compatibility", {})
    if compatibility.get("unknown_optional_modules") != "ignore_when_not_requested":
        errors.append("minimal reader: unknown optional module policy is invalid")
    if compatibility.get("unknown_required_modules") != "reject":
        errors.append("minimal reader: unknown required module policy is invalid")

    allowed_identity_keys = {"type", "id", "display_name", "visual_identity"}
    for fixture_id in expected_types:
        fixture = suite.get("fixtures", {}).get(fixture_id)
        if not isinstance(fixture, dict):
            errors.append(f"minimal reader: fixture {fixture_id!r} is missing")
            continue
        errors.extend(f"minimal reader: {error}" for error in fixture_semantic_errors(fixture_id, fixture))
        manifest = build_manifest(fixture, target)
        envelope = build_identity_envelope(fixture)
        mind = manifest["mind"]
        identity = envelope["identity"]
        if mind["name"] != f"mind@{mind['subject']['id']}":
            errors.append(f"minimal reader: fixture {fixture_id!r} has invalid mind name")
        if "identity" not in manifest["modules"]["required"]:
            errors.append(f"minimal reader: fixture {fixture_id!r} must require identity")
        if consumer_module_errors(manifest):
            errors.append(f"minimal reader: fixture {fixture_id!r} has unknown required modules")
        if set(identity) - allowed_identity_keys:
            errors.append(f"minimal reader: fixture {fixture_id!r} identity contains unknown core fields")
        if identity.get("type") != mind["subject"].get("type") or identity.get("id") != mind["subject"].get("id"):
            errors.append(f"minimal reader: fixture {fixture_id!r} identity does not bind to subject")
        if not isinstance(identity.get("display_name"), str) or not identity["display_name"]:
            errors.append(f"minimal reader: fixture {fixture_id!r} display_name is invalid")

    person_manifest = build_manifest(suite["fixtures"]["person"], target)
    errors.extend(f"minimal reader: {error}" for error in compatibility_probe_errors(person_manifest))
    return errors


def run_mode(mode: str) -> dict[str, Any]:
    suite = load_yaml_mapping(SUITE_PATH)
    protocol = load_yaml_mapping(PROTOCOL_PATH)
    if mode == "schema":
        errors = schema_mode(suite, protocol)
    elif mode == "minimal":
        errors = minimal_mode(suite, protocol)
    else:
        raise ValueError(f"unknown mode: {mode}")
    return {
        "mode": mode,
        "protocol": suite.get("protocol"),
        "fixtures": suite.get("fixture_types", []),
        "status": "pass" if not errors else "fail",
        "errors": errors,
    }


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=("all", "schema", "minimal"), default="all")
    return parser.parse_args()


def main() -> int:
    arguments = parse_arguments()
    try:
        modes = ["schema", "minimal"] if arguments.mode == "all" else [arguments.mode]
        results = [run_mode(mode) for mode in modes]
    except (KeyError, TypeError, ValueError) as error:
        print(json.dumps({"status": "fail", "errors": [str(error)]}, sort_keys=True))
        return 1

    status = "pass" if all(result["status"] == "pass" for result in results) else "fail"
    output = {"status": status, "modes": results}
    print(json.dumps(output, sort_keys=True))
    return 0 if status == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
