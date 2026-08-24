#!/usr/bin/env python3
# © 2026 aiaiaiai · aiaiaiai.org
# SPDX-License-Identifier: MIT
"""Run Mind Protocol conformance through independent schema and minimal-reader modes."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import sys
import tempfile
from pathlib import Path
from typing import Any, Callable

from jsonschema import Draft202012Validator

from validate_identity_resources import validate_identity_envelope
from validate_manifest import load_schema, load_yaml_mapping, schema_errors
from validate_relationships import validate_relationships
from validate_visual_assets import resolve_primary_mark


ROOT = Path(__file__).resolve().parents[1]
SUITE_PATH = ROOT / "conformance.yaml"
PROTOCOL_PATH = ROOT / "protocol.yaml"
CONFORMANCE_SCHEMA_PATH = ROOT / "schema/conformance.schema.json"
MIND_SCHEMA_PATH = ROOT / "schema/mind.schema.json"
IDENTITY_SCHEMA_PATH = ROOT / "schema/identity.schema.json"
IDENTITY_RESOURCE_SCHEMA_PATH = ROOT / "schema/identity-resource.schema.json"
RELATIONSHIPS_SCHEMA_PATH = ROOT / "schema/relationships.schema.json"
VISUAL_ASSETS_SCHEMA_PATH = ROOT / "schema/visual-assets.schema.json"
KNOWN_MODULES = frozenset({"identity"})
KIND_BY_TYPE = {
    "person": "personal",
    "organization": "organization",
    "agent": "agent",
    "project": "project",
    "product": "product",
}
REQUIRED_FEATURE_SUPPORT = {
    "universal_identity": "required",
    "identity_resource": "required",
    "relationships_provenance": "required",
    "canonical_visual_identity": "optional",
    "agent_identity": "required",
    "neutral_baseline": "required",
    "unknown_optional_modules": "required",
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


def build_relationship_resource(fixture: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "relationships": [
            {
                "id": "conformance.authored",
                "predicate": "related_to",
                "source": copy.deepcopy(fixture["subject"]),
                "target": {"type": "project", "id": "fixture-counterpart"},
                "direction": "directed",
                "provenance": {
                    "kind": "authored",
                    "authority": copy.deepcopy(fixture["owner"]),
                },
                "confirmation": {"state": "asserted"},
            }
        ],
        "validation": {"schema": "schema/relationships.schema.json"},
    }


def range_errors(range_spec: dict[str, Any], protocol: dict[str, Any]) -> list[str]:
    version = semver_core(protocol["version"])
    minimum = semver_core(range_spec["minimum_inclusive"])
    maximum = semver_core(range_spec["maximum_exclusive"])
    if not minimum <= version < maximum:
        return ["protocol version is outside declared supported range"]
    return []


def consumer_range_errors(
    suite: dict[str, Any], mode: str, protocol: dict[str, Any]
) -> list[str]:
    support = suite.get("consumer_support", {}).get(mode)
    if not isinstance(support, dict) or not isinstance(support.get("supported_range"), dict):
        return [f"consumer {mode!r} must declare supported_range"]
    declared = support["supported_range"]
    errors = range_errors(declared, protocol)
    if declared != suite.get("supported_range"):
        errors.append(f"consumer {mode!r} supported_range must match suite supported_range")
    return errors


def fixture_semantic_errors(fixture_id: str, fixture: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    subject_type = fixture.get("subject", {}).get("type")
    if subject_type != fixture_id:
        errors.append(f"fixture {fixture_id!r} subject.type must match fixture id")
    if KIND_BY_TYPE.get(subject_type) != fixture.get("kind"):
        errors.append(f"fixture {fixture_id!r} kind does not match subject type")
    if fixture.get("owner", {}).get("type") not in KIND_BY_TYPE:
        errors.append(f"fixture {fixture_id!r} owner must be a concrete entity")
    if fixture.get("expected_result") != "pass":
        errors.append(f"fixture {fixture_id!r} must declare deterministic expected_result 'pass'")
    return errors


def feature_matrix_errors(suite: dict[str, Any]) -> list[str]:
    features = suite.get("features")
    if not isinstance(features, list):
        return ["feature matrix must be a list"]
    observed: dict[str, Any] = {}
    errors: list[str] = []
    for feature in features:
        if not isinstance(feature, dict):
            errors.append("feature matrix entries must be mappings")
            continue
        feature_id = feature.get("id")
        if not isinstance(feature_id, str):
            errors.append("feature matrix id must be a string")
            continue
        if feature_id in observed:
            errors.append(f"feature matrix contains duplicate id {feature_id!r}")
        observed[feature_id] = feature.get("support")
    for feature_id, support in REQUIRED_FEATURE_SUPPORT.items():
        if observed.get(feature_id) != support:
            errors.append(
                f"feature {feature_id!r} must declare support {support!r}"
            )
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


def minimal_consumer_module_errors(manifest: dict[str, Any]) -> list[str]:
    modules = manifest.get("modules")
    loading = manifest.get("loading")
    if not isinstance(modules, dict) or not isinstance(loading, dict):
        return ["minimal reader: manifest loading/modules must be mappings"]
    required = modules.get("required")
    default = loading.get("default")
    if not isinstance(required, list) or not isinstance(default, list):
        return ["minimal reader: required/default module sets must be lists"]
    errors: list[str] = []
    for label, values in (("required", required), ("default-loaded", default)):
        unknown = sorted(
            value for value in values if isinstance(value, str) and value not in KNOWN_MODULES
        )
        if unknown:
            errors.append(f"unknown {label} modules: " + ", ".join(unknown))
    return errors


def module_probe_results(
    base_manifest: dict[str, Any],
    error_reader: Callable[[dict[str, Any]], list[str]],
) -> dict[str, str]:
    optional = copy.deepcopy(base_manifest)
    optional["modules"]["registered"].append("future_extension")
    optional["modules"]["catalog"]["future_extension"] = "future_extension/module.yaml"
    optional["loading"]["optional"].append("future_extension")
    optional_status = (
        "ignored_when_not_requested" if not error_reader(optional) else "rejected"
    )

    required = copy.deepcopy(optional)
    required["loading"]["optional"].remove("future_extension")
    required["modules"]["required"].append("future_extension")
    required["loading"]["default"].append("future_extension")
    required_status = "rejected" if error_reader(required) else "accepted"
    return {
        "unknown_optional_module": optional_status,
        "unknown_required_module": required_status,
    }


def minimal_relationship_errors(
    manifest: dict[str, Any], resource: dict[str, Any]
) -> list[str]:
    relationships = resource.get("relationships")
    if not isinstance(relationships, list) or len(relationships) != 1:
        return ["minimal reader: relationship probe must contain exactly one relation"]
    relationship = relationships[0]
    if not isinstance(relationship, dict):
        return ["minimal reader: relationship must be a mapping"]
    errors: list[str] = []
    subject = manifest["mind"]["subject"]
    owner = manifest["mind"]["owner"]
    source = relationship.get("source")
    target = relationship.get("target")
    if source == target:
        errors.append("minimal reader: relationship endpoints must differ")
    if subject not in (source, target):
        errors.append("minimal reader: canonical relationship must involve subject")
    provenance = relationship.get("provenance")
    if not isinstance(provenance, dict) or provenance.get("kind") != "authored":
        errors.append("minimal reader: canonical relationship provenance must remain authored")
    elif provenance.get("authority") != owner:
        errors.append("minimal reader: relationship authority must match publication owner")
    return errors


def schema_relationship_probe_results(
    fixture: dict[str, Any], protocol: dict[str, Any]
) -> dict[str, str]:
    manifest = build_manifest(fixture, protocol)
    resource = build_relationship_resource(fixture)
    schema = load_schema(RELATIONSHIPS_SCHEMA_PATH)
    structural = schema_errors(Draft202012Validator(schema), resource)
    semantic = validate_relationships(manifest, resource) if not structural else ["invalid"]
    authored_status = "preserved" if not structural and not semantic else "invalid"

    derived = copy.deepcopy(resource)
    derived["relationships"][0]["provenance"]["kind"] = "derived"
    derived_status = (
        "rejected_from_canonical"
        if schema_errors(Draft202012Validator(schema), derived)
        else "accepted_as_canonical"
    )
    return {
        "authored_relationship": authored_status,
        "derived_relationship": derived_status,
    }


def minimal_relationship_probe_results(
    fixture: dict[str, Any], protocol: dict[str, Any]
) -> dict[str, str]:
    manifest = build_manifest(fixture, protocol)
    resource = build_relationship_resource(fixture)
    authored_status = (
        "preserved" if not minimal_relationship_errors(manifest, resource) else "invalid"
    )
    derived = copy.deepcopy(resource)
    derived["relationships"][0]["provenance"]["kind"] = "derived"
    derived_status = (
        "rejected_from_canonical"
        if minimal_relationship_errors(manifest, derived)
        else "accepted_as_canonical"
    )
    return {
        "authored_relationship": authored_status,
        "derived_relationship": derived_status,
    }


def visual_probe_documents(publication_root: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    asset_bytes = b'<svg xmlns="http://www.w3.org/2000/svg"/>\n'
    asset_path = publication_root / "fixture-mark.svg"
    asset_path.write_bytes(asset_bytes)
    digest = hashlib.sha256(asset_bytes).hexdigest()
    identity = {
        "type": "project",
        "id": "fixture-visual-project",
        "display_name": "Fixture Visual Project",
        "visual_identity": {
            "primary_mark": {
                "kind": "emblem",
                "asset_ref": "fixture-mark",
                "alt": "Fixture mark",
            }
        },
    }
    catalog = {
        "schema_version": 1,
        "assets": [
            {
                "ref": "fixture-mark",
                "media_type": "image/svg+xml",
                "resource_path": "fixture-mark.svg",
                "integrity": {"algorithm": "sha256", "digest": digest},
            }
        ],
        "validation": {"schema": "schema/visual-assets.schema.json"},
    }
    return identity, catalog


def minimal_visual_status(
    identity: dict[str, Any], catalog: dict[str, Any], publication_root: Path
) -> str:
    visual = identity.get("visual_identity")
    mark = visual.get("primary_mark") if isinstance(visual, dict) else None
    asset_ref = mark.get("asset_ref") if isinstance(mark, dict) else None
    if not isinstance(asset_ref, str) or not asset_ref:
        return "unavailable"
    assets = catalog.get("assets")
    if not isinstance(assets, list):
        return "missing"
    matches = [
        asset for asset in assets if isinstance(asset, dict) and asset.get("ref") == asset_ref
    ]
    if not matches:
        return "missing"
    if len(matches) != 1:
        return "ambiguous"
    descriptor = matches[0]
    if descriptor.get("media_type") not in {"image/svg+xml", "image/png"}:
        return "unsupported_media"
    relative_path = descriptor.get("resource_path")
    if not isinstance(relative_path, str):
        return "missing"
    root = publication_root.resolve()
    path = (root / relative_path).resolve()
    if (path != root and root not in path.parents) or not path.is_file():
        return "missing"
    integrity = descriptor.get("integrity")
    if not isinstance(integrity, dict) or integrity.get("algorithm") != "sha256":
        return "integrity_error"
    expected = integrity.get("digest")
    if not isinstance(expected, str):
        return "integrity_error"
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    return "resolved" if actual == expected else "integrity_error"


def schema_visual_probe_results() -> dict[str, str]:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        identity, catalog = visual_probe_documents(root)
        identity_schema = load_schema(IDENTITY_SCHEMA_PATH)
        catalog_schema = load_schema(VISUAL_ASSETS_SCHEMA_PATH)
        errors = schema_errors(Draft202012Validator(identity_schema), identity)
        errors.extend(schema_errors(Draft202012Validator(catalog_schema), catalog))
        if errors:
            return {
                "canonical_visual_resolved": "invalid",
                "canonical_visual_integrity_failure": "invalid",
            }
        resolved = resolve_primary_mark(identity, catalog, root).status
        invalid_catalog = copy.deepcopy(catalog)
        invalid_catalog["assets"][0]["integrity"]["digest"] = "0" * 64
        integrity = resolve_primary_mark(identity, invalid_catalog, root).status
        return {
            "canonical_visual_resolved": resolved,
            "canonical_visual_integrity_failure": integrity,
        }


def minimal_visual_probe_results() -> dict[str, str]:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        identity, catalog = visual_probe_documents(root)
        resolved = minimal_visual_status(identity, catalog, root)
        invalid_catalog = copy.deepcopy(catalog)
        invalid_catalog["assets"][0]["integrity"]["digest"] = "0" * 64
        integrity = minimal_visual_status(identity, invalid_catalog, root)
        return {
            "canonical_visual_resolved": resolved,
            "canonical_visual_integrity_failure": integrity,
        }


def probe_errors(suite: dict[str, Any], actual: dict[str, str]) -> list[str]:
    expected = suite.get("probes")
    if not isinstance(expected, dict):
        return ["conformance suite must declare probe expectations"]
    errors: list[str] = []
    for probe_id, expected_status in expected.items():
        if actual.get(probe_id) != expected_status:
            errors.append(
                f"probe {probe_id!r}: expected {expected_status!r}, got {actual.get(probe_id)!r}"
            )
    return errors


def schema_mode(
    suite: dict[str, Any], protocol_descriptor: dict[str, Any]
) -> tuple[list[str], dict[str, str]]:
    errors: list[str] = []
    suite_schema = load_schema(CONFORMANCE_SCHEMA_PATH)
    errors.extend(
        f"suite{error[1:]}"
        for error in schema_errors(Draft202012Validator(suite_schema), suite)
    )
    if errors:
        return errors, {}

    protocol = {
        "id": protocol_descriptor["protocol"]["id"],
        "version": protocol_descriptor["protocol"]["version"],
    }
    if suite["protocol"] != protocol:
        errors.append("conformance suite protocol id/version must match protocol.yaml")
    errors.extend(range_errors(suite["supported_range"], protocol))
    errors.extend(consumer_range_errors(suite, "schema", protocol))
    errors.extend(feature_matrix_errors(suite))

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

    probes: dict[str, str] = {}
    probes.update(module_probe_results(person_manifest, consumer_module_errors))
    probes.update(schema_relationship_probe_results(suite["fixtures"]["person"], protocol))
    probes.update(schema_visual_probe_results())
    errors.extend(probe_errors(suite, probes))
    return errors, probes


def minimal_mode(
    suite: dict[str, Any], protocol_descriptor: dict[str, Any]
) -> tuple[list[str], dict[str, str]]:
    """Independent reader mode: deliberately avoids JSON Schema and shared semantic validators."""
    errors: list[str] = []
    protocol = protocol_descriptor.get("protocol")
    if not isinstance(protocol, dict):
        return ["protocol descriptor must contain protocol mapping"], {}
    target = {"id": protocol.get("id"), "version": protocol.get("version")}
    if suite.get("protocol") != target:
        errors.append("minimal reader: suite protocol does not match descriptor")
    try:
        range_spec = suite.get("supported_range")
        if not isinstance(range_spec, dict):
            raise ValueError("suite supported_range must be a mapping")
        errors.extend(range_errors(range_spec, target))
        errors.extend(consumer_range_errors(suite, "minimal", target))
    except (KeyError, TypeError, ValueError) as error:
        errors.append(f"minimal reader: {error}")
        return errors, {}

    expected_types = ["person", "organization", "agent", "project", "product"]
    if suite.get("fixture_types") != expected_types:
        errors.append("minimal reader: fixture_types must contain the five canonical types")
    if suite.get("consumer_modes") != ["schema", "minimal"]:
        errors.append("minimal reader: two declared consumer modes are required")
    errors.extend(f"minimal reader: {error}" for error in feature_matrix_errors(suite))

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
        errors.extend(
            f"minimal reader: {error}"
            for error in fixture_semantic_errors(fixture_id, fixture)
        )
        manifest = build_manifest(fixture, target)
        envelope = build_identity_envelope(fixture)
        mind = manifest["mind"]
        identity = envelope["identity"]
        if mind["name"] != f"mind@{mind['subject']['id']}":
            errors.append(f"minimal reader: fixture {fixture_id!r} has invalid mind name")
        if "identity" not in manifest["modules"]["required"]:
            errors.append(f"minimal reader: fixture {fixture_id!r} must require identity")
        if minimal_consumer_module_errors(manifest):
            errors.append(f"minimal reader: fixture {fixture_id!r} has unknown required modules")
        if set(identity) - allowed_identity_keys:
            errors.append(f"minimal reader: fixture {fixture_id!r} identity contains unknown core fields")
        if (
            identity.get("type") != mind["subject"].get("type")
            or identity.get("id") != mind["subject"].get("id")
        ):
            errors.append(f"minimal reader: fixture {fixture_id!r} identity does not bind to subject")
        if not isinstance(identity.get("display_name"), str) or not identity["display_name"]:
            errors.append(f"minimal reader: fixture {fixture_id!r} display_name is invalid")

    person_manifest = build_manifest(suite["fixtures"]["person"], target)
    probes: dict[str, str] = {}
    probes.update(module_probe_results(person_manifest, minimal_consumer_module_errors))
    probes.update(minimal_relationship_probe_results(suite["fixtures"]["person"], target))
    probes.update(minimal_visual_probe_results())
    errors.extend(f"minimal reader: {error}" for error in probe_errors(suite, probes))
    return errors, probes


def run_mode(mode: str) -> dict[str, Any]:
    suite = load_yaml_mapping(SUITE_PATH)
    protocol = load_yaml_mapping(PROTOCOL_PATH)
    if mode == "schema":
        errors, probes = schema_mode(suite, protocol)
    elif mode == "minimal":
        errors, probes = minimal_mode(suite, protocol)
    else:
        raise ValueError(f"unknown mode: {mode}")
    support = suite.get("consumer_support", {}).get(mode, {})
    return {
        "mode": mode,
        "protocol": suite.get("protocol"),
        "supported_range": support.get("supported_range"),
        "fixtures": suite.get("fixture_types", []),
        "probes": probes,
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
    except (KeyError, OSError, TypeError, ValueError) as error:
        print(json.dumps({"status": "fail", "errors": [str(error)]}, sort_keys=True))
        return 1

    status = "pass" if all(result["status"] == "pass" for result in results) else "fail"
    output = {"status": status, "modes": results}
    print(json.dumps(output, sort_keys=True))
    return 0 if status == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
