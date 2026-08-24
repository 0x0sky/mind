#!/usr/bin/env python3
# © 2026 aiaiaiai · aiaiaiai.org
# SPDX-License-Identifier: MIT
"""Generate and verify the deterministic neutral Mind Protocol baseline bundle."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator

from validate_manifest import (
    load_schema,
    load_yaml_mapping,
    schema_errors,
    validate_manifest_semantics,
    validate_modules,
)


ROOT = Path(__file__).resolve().parents[1]
PROTOCOL_PATH = ROOT / "protocol.yaml"
CONFORMANCE_PATH = ROOT / "conformance.yaml"
COMPATIBILITY_PATH = ROOT / "compatibility.yaml"
SCHEMA_ROOT = ROOT / "schema"
REFERENCE_MANIFEST = ROOT / "manifest.yaml"
BASELINE_README = """# Mind Protocol neutral baseline

This directory is a generated **abstract protocol artifact**. It is not a concrete Mind and must not be published unchanged as a person, organization, agent, project, or product Mind.

Its manifest intentionally uses `subject: unspecified` and `owner: unspecified` and contains no concrete Identity module.

To create a concrete Mind, start from the exact immutable protocol release that produced this baseline and use the documented concrete bootstrap path. Do not copy or rename content from the protocol repository's reference implementation.

<!-- © 2026 aiaiaiai · aiaiaiai.org -->
"""


def abstract_manifest(protocol: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": 3,
        "protocol": {
            "id": protocol["protocol"]["id"],
            "version": protocol["protocol"]["version"],
        },
        "mind": {
            "name": "mind",
            "context_version": "0.0.0",
            "subject": {"type": "unspecified", "id": "unspecified"},
            "owner": {"type": "unspecified", "id": "unspecified"},
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
            "required": [],
            "registered": [],
            "rules": {
                "single_responsibility": "required",
                "explicit_dependencies": "required",
                "independently_replaceable": "required",
                "duplicate_content": "forbidden",
                "cross_reference": "preferred",
                "composition_over_inheritance": "preferred",
            },
            "catalog": {},
        },
        "context": {
            "stability": {
                "stable": "long_lived_contracts",
                "transient": "current_state",
                "archived": "ignored_unless_requested",
            },
            "visibility": {
                "repository": "public",
                "allowed": "neutral_protocol_baseline",
                "forbidden": ["credentials", "secrets"],
            },
        },
        "loading": {"default": [], "optional": []},
        "validation": {
            "schema": "schema/mind.schema.json",
            "module_schema": "schema/module.schema.json",
        },
    }


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def snapshot(root: Path) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): sha256(path)
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def write_yaml(path: Path, value: dict[str, Any]) -> None:
    path.write_text(
        yaml.safe_dump(value, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )


def generate_baseline(output: Path) -> dict[str, str]:
    protocol = load_yaml_mapping(PROTOCOL_PATH)
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)

    shutil.copyfile(PROTOCOL_PATH, output / "protocol.yaml")
    shutil.copyfile(CONFORMANCE_PATH, output / "conformance.yaml")
    shutil.copyfile(COMPATIBILITY_PATH, output / "compatibility.yaml")
    shutil.copytree(SCHEMA_ROOT, output / "schema")
    write_yaml(output / "manifest.yaml", abstract_manifest(protocol))
    (output / "README.md").write_text(BASELINE_README, encoding="utf-8")

    files = snapshot(output)
    metadata = {
        "schema_version": 1,
        "artifact": "mind-neutral-baseline",
        "protocol": {
            "id": protocol["protocol"]["id"],
            "version": protocol["protocol"]["version"],
        },
        "source": "protocol_contract_set",
        "files": files,
    }
    (output / "baseline.json").write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return snapshot(output)


def generated_manifest_errors(output: Path) -> list[str]:
    manifest = load_yaml_mapping(output / "manifest.yaml")
    schema = load_schema(output / "schema" / "mind.schema.json")
    errors = [
        f"baseline{error[1:]}"
        for error in schema_errors(Draft202012Validator(schema), manifest)
    ]
    if not errors:
        errors.extend(validate_manifest_semantics(manifest, output))
        errors.extend(validate_modules(manifest, output))

    protocol = load_yaml_mapping(output / "protocol.yaml")
    expected_protocol = {
        "id": protocol["protocol"]["id"],
        "version": protocol["protocol"]["version"],
    }
    if manifest.get("protocol") != expected_protocol:
        errors.append("baseline manifest protocol must match generated protocol descriptor")
    subject = manifest.get("mind", {}).get("subject")
    if subject != {"type": "unspecified", "id": "unspecified"}:
        errors.append("generated baseline must retain explicit unspecified abstract subject")
    if "kind" in manifest.get("mind", {}):
        errors.append("generated baseline must not reintroduce removed mind.kind")
    if "public_organizations" in manifest:
        errors.append("generated baseline must not contain provider-specific organization projection")
    return errors


def reference_instance_tokens() -> set[str]:
    manifest = load_yaml_mapping(REFERENCE_MANIFEST)
    tokens: set[str] = {"github.com/0x0sky/mind"}
    mind = manifest.get("mind", {})
    name = mind.get("name")
    if isinstance(name, str):
        tokens.add(name)
    for key in ("subject", "owner"):
        entity = mind.get(key)
        if isinstance(entity, dict) and isinstance(entity.get("id"), str):
            tokens.add(entity["id"])
    return {token for token in tokens if len(token) >= 4}


def leakage_errors(output: Path) -> list[str]:
    tokens = reference_instance_tokens()
    errors: list[str] = []
    for path in sorted(output.rglob("*")):
        if not path.is_file() or path.suffix not in {".yaml", ".yml", ".json"}:
            continue
        text = path.read_text(encoding="utf-8")
        for token in sorted(tokens):
            if token in text:
                errors.append(
                    f"{path.relative_to(output).as_posix()}: leaked reference-instance token {token!r}"
                )
    return errors


def check_baseline() -> list[str]:
    errors: list[str] = []
    with tempfile.TemporaryDirectory() as first_directory, tempfile.TemporaryDirectory() as second_directory:
        first = Path(first_directory) / "baseline"
        second = Path(second_directory) / "baseline"
        first_snapshot = generate_baseline(first)
        second_snapshot = generate_baseline(second)
        if first_snapshot != second_snapshot:
            errors.append("baseline generation is not byte-for-byte deterministic")
        errors.extend(generated_manifest_errors(first))
        errors.extend(leakage_errors(first))
        readme = (first / "README.md").read_text(encoding="utf-8")
        if "not a concrete Mind" not in readme:
            errors.append("generated baseline must identify itself as non-concrete")
    return errors


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="verify determinism, validity, compatibility, and instance isolation",
    )
    parser.add_argument("--output", type=Path, help="directory to generate when not using --check")
    return parser.parse_args()


def main() -> int:
    arguments = parse_arguments()
    try:
        if arguments.check:
            errors = check_baseline()
            if errors:
                print("neutral baseline validation failed:", file=sys.stderr)
                for error in errors:
                    print(f"- {error}", file=sys.stderr)
                return 1
            print("neutral baseline generation is deterministic, valid, and instance-independent")
            return 0

        if arguments.output is None:
            print("baseline generation failed: --output is required unless --check is used", file=sys.stderr)
            return 2
        files = generate_baseline(arguments.output.resolve())
        print(json.dumps({"output": str(arguments.output), "files": files}, sort_keys=True))
        return 0
    except (KeyError, OSError, TypeError, ValueError) as error:
        print(f"baseline generation failed: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
