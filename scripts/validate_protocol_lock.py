#!/usr/bin/env python3
# © 2026 aiaiaiai · aiaiaiai.org
# SPDX-License-Identifier: MIT
"""Validate the exact Mind Protocol release contracts consumed by mind@0x0sky."""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path
from typing import Any

from validate_manifest import load_json_mapping, load_yaml_mapping

ROOT = Path(__file__).resolve().parents[1]
LOCK_PATH = ROOT / "protocol.lock.yaml"
MANIFEST_PATH = ROOT / "manifest.yaml"
EXPECTED_SOURCE = {
    "repository": "aiaiaiai-org/mind-protocol",
    "tag": "v0.9.0",
    "commit": "457844c8ced0318d91d628617ff6f8ec6f428ab7",
    "floating_branch": "forbidden",
}


def git_blob_sha1(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()


def verify_blob(path: Path, expected_sha: Any, label: str, errors: list[str]) -> None:
    if not path.is_file():
        errors.append(f"locked release artifact is missing: {label}")
    elif git_blob_sha1(path) != expected_sha:
        errors.append(f"release artifact drift from v0.9.0: {label}")


def validate() -> list[str]:
    errors: list[str] = []
    lock = load_yaml_mapping(LOCK_PATH)
    manifest = load_yaml_mapping(MANIFEST_PATH)

    protocol = lock.get("protocol")
    if protocol != {"id": "mind", "version": "0.9.0"}:
        errors.append("protocol.lock.yaml must pin Mind Protocol 0.9.0 exactly")
    if manifest.get("protocol") != protocol:
        errors.append("manifest protocol must match protocol.lock.yaml exactly")

    if lock.get("source") != EXPECTED_SOURCE:
        errors.append(
            "protocol source must pin aiaiaiai-org/mind-protocol v0.9.0 at the historical release commit"
        )

    descriptor = lock.get("protocol_descriptor")
    if not isinstance(descriptor, dict):
        errors.append("protocol_descriptor lock is missing")
    else:
        verify_blob(
            ROOT / str(descriptor.get("path", "")),
            descriptor.get("git_blob_sha1"),
            "protocol.yaml",
            errors,
        )

    machine_artifacts = lock.get("release_machine_artifacts")
    if not isinstance(machine_artifacts, dict) or not machine_artifacts:
        errors.append("release_machine_artifacts lock is missing")
    else:
        for relative_path, artifact in machine_artifacts.items():
            if not isinstance(relative_path, str) or not isinstance(artifact, dict):
                errors.append("release_machine_artifacts entries must be path -> descriptor mappings")
                continue
            verify_blob(
                ROOT / relative_path,
                artifact.get("git_blob_sha1"),
                relative_path,
                errors,
            )

    contracts = lock.get("vendored_contracts")
    if not isinstance(contracts, dict) or not contracts:
        errors.append("vendored_contracts lock is missing")
        return errors

    seen_ids: set[str] = set()
    for relative_path, descriptor in contracts.items():
        if not isinstance(relative_path, str) or not isinstance(descriptor, dict):
            errors.append("vendored_contracts entries must be path -> descriptor mappings")
            continue
        path = ROOT / relative_path
        verify_blob(path, descriptor.get("git_blob_sha1"), relative_path, errors)
        if not path.is_file():
            continue
        schema = load_json_mapping(path)
        schema_id = descriptor.get("schema_id")
        if schema.get("$id") != schema_id:
            errors.append(f"schema id mismatch for {relative_path}")
        if not isinstance(schema_id, str) or schema_id in seen_ids:
            errors.append(f"duplicate or invalid locked schema id for {relative_path}")
        else:
            seen_ids.add(schema_id)

    compatibility = load_yaml_mapping(ROOT / "compatibility.yaml")
    if compatibility.get("protocol") != protocol:
        errors.append("compatibility.yaml protocol binding must match protocol.lock.yaml")

    frozen = compatibility.get("freeze", {}).get("frozen_contracts")
    if not isinstance(frozen, list):
        errors.append("compatibility.yaml frozen contract set is missing")
    else:
        published: dict[str, tuple[Any, Any]] = {}
        for item in frozen:
            if not isinstance(item, dict) or not isinstance(item.get("path"), str):
                errors.append("compatibility.yaml contains an invalid frozen contract descriptor")
                continue
            published[item["path"]] = (item.get("schema_id"), item.get("git_blob_sha1"))
        locked = {
            path: (descriptor.get("schema_id"), descriptor.get("git_blob_sha1"))
            for path, descriptor in contracts.items()
            if isinstance(path, str) and isinstance(descriptor, dict)
        }
        if locked != published:
            errors.append("vendored contract set must equal the complete v0.9.0 compatibility freeze")

    conformance = load_yaml_mapping(ROOT / "conformance.yaml")
    if conformance.get("protocol") != protocol:
        errors.append("conformance.yaml protocol binding must match protocol.lock.yaml")

    if lock.get("context_versioning") != {
        "independent_from_protocol": True,
        "protocol_tags_in_this_repository": "forbidden",
    }:
        errors.append("context/protocol versioning boundary is not canonical")

    return errors


def main() -> int:
    try:
        errors = validate()
    except (OSError, ValueError, TypeError) as error:
        print(f"protocol release lock validation failed:\n- {error}", file=sys.stderr)
        return 1

    if errors:
        print("protocol release lock validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("mind@0x0sky pins the complete Mind Protocol v0.9.0 machine contract set exactly")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
