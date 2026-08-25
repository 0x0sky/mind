#!/usr/bin/env python3
# © 2026 aiaiaiai · aiaiaiai.org
# SPDX-License-Identifier: MIT
"""Validate pure concrete-consumer invariants for mind@0x0sky."""

from __future__ import annotations

import sys
from pathlib import Path

from validate_manifest import load_yaml_mapping

ROOT = Path(__file__).resolve().parents[1]


def validate() -> list[str]:
    errors: list[str] = []
    repository = load_yaml_mapping(ROOT / "mind-repository.yaml")
    manifest = load_yaml_mapping(ROOT / "manifest.yaml")
    identity = load_yaml_mapping(ROOT / "modules" / "identity" / "identity.yaml")

    roles = repository.get("repository", {}).get("roles", {})
    protocol_role = roles.get("protocol_authority", {})
    concrete_role = roles.get("concrete_mind", {})

    if protocol_role != {"enabled": False}:
        errors.append("0x0sky/mind must not declare protocol authority after the repository split")
    if concrete_role.get("enabled") is not True:
        errors.append("concrete mind role must be enabled")
    if concrete_role.get("template_authority") is not False:
        errors.append("mind@0x0sky must not be a template authority")
    if concrete_role.get("canonical_for_subject") != {"type": "person", "id": "0x0sky"}:
        errors.append("repository role must be canonical only for person:0x0sky")

    protocol_consumption = repository.get("protocol_consumption")
    if protocol_consumption != {
        "id": "mind",
        "version": "1.0.0-rc.1",
        "authority_repository": "aiaiaiai-org/mind-protocol",
        "release_repository": "aiaiaiai-org/mind-protocol",
        "release_tag": "v1.0.0-rc.1",
        "release_commit": "6bf8467f0e3990808464e118cc60cc83d8ab2ced",
        "floating_master": "forbidden",
    }:
        errors.append("repository metadata must pin the immutable Mind Protocol 1.0.0-rc.1 release exactly")

    fork_policy = repository.get("fork_policy", {})
    if fork_policy.get("relationship_to_protocol_repository") != "independent_consumer":
        errors.append("mind@0x0sky must model protocol linkage as an independent consumer, not a fork")

    subject = {"type": "person", "id": "0x0sky"}
    mind = manifest.get("mind", {})
    if manifest.get("protocol") != {"id": "mind", "version": "1.0.0-rc.1"}:
        errors.append("manifest must consume Mind Protocol 1.0.0-rc.1")
    if mind.get("subject") != subject or mind.get("owner") != subject:
        errors.append("manifest subject and owner must remain person:0x0sky")
    if mind.get("context_version") != "0.4.0":
        errors.append("protocol-only RC synchronization must not silently bump personal context_version")

    if identity.get("identity") != {
        "type": "person",
        "id": "0x0sky",
        "display_name": "0x0sky",
    }:
        errors.append("canonical person Identity must remain provider-independent person:0x0sky")

    catalog = manifest.get("modules", {}).get("catalog", {})
    if catalog.get("identity") != "modules/identity/module.yaml":
        errors.append("personal Identity module must use the normalized modules/identity layout")

    forbidden_authority_paths = [
        ROOT / "docs" / "protocol",
        ROOT / "tests",
        ROOT / "scripts" / "bootstrap_mind.py",
        ROOT / "scripts" / "build_release_bundle.py",
        ROOT / "scripts" / "generate_baseline.py",
        ROOT / ".github" / "workflows" / "release.yml",
        ROOT / "identity",
    ]
    for path in forbidden_authority_paths:
        if path.exists():
            errors.append(f"legacy protocol/reference-authority path must be absent: {path.relative_to(ROOT)}")

    return errors


def main() -> int:
    errors = validate()
    if errors:
        print("mind@0x0sky consumer invariant validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(
        "mind@0x0sky is an independent concrete Mind consumer pinned to Mind Protocol 1.0.0-rc.1 "
        "with normalized person Identity"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
