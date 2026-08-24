#!/usr/bin/env python3
# © 2026 aiaiaiai · aiaiaiai.org
# SPDX-License-Identifier: MIT
"""Migrate supported Mind manifest v2 publications to frozen manifest v3."""

from __future__ import annotations

import argparse
import copy
import sys
from pathlib import Path
from typing import Any

import yaml

from validate_manifest import load_yaml_mapping


TARGET_PROTOCOL = "0.9.0"
MIGRATION_FLOOR = (0, 6, 0)
SUBJECT_TYPE_BY_LEGACY_KIND = {
    "abstract": "unspecified",
    "personal": "person",
    "organization": "organization",
    "agent": "agent",
    "project": "project",
    "product": "product",
}
REMOVED_PROVIDER_FIELDS = {
    "organizations",
    "memberships",
    "public_organization",
    "public_organizations",
}


def semver_core(value: str) -> tuple[int, int, int]:
    try:
        core = value.split("-", 1)[0].split("+", 1)[0]
        major, minor, patch = core.split(".")
        return int(major), int(minor), int(patch)
    except (AttributeError, ValueError) as error:
        raise ValueError(f"invalid semantic version {value!r}") from error


def migrate_manifest(
    source: dict[str, Any],
    *,
    provider_projection_preserved: bool = False,
) -> tuple[dict[str, Any] | None, list[str]]:
    errors: list[str] = []
    candidate = copy.deepcopy(source)

    if candidate.get("schema_version") != 2:
        return None, ["source manifest must use schema_version 2"]

    protocol = candidate.get("protocol")
    if not isinstance(protocol, dict) or protocol.get("id") != "mind":
        return None, ["source manifest must declare protocol id 'mind'"]
    try:
        source_version = semver_core(protocol.get("version"))
    except ValueError as error:
        return None, [str(error)]
    if source_version < MIGRATION_FLOOR:
        return None, [
            "unsupported source protocol: migration floor is 0.6.0; use a documented earlier migration path first"
        ]
    if source_version >= (0, 9, 0):
        return None, ["source protocol must be an older pre-0.9 stable line"]

    mind = candidate.get("mind")
    if not isinstance(mind, dict):
        return None, ["source manifest mind must be a mapping"]
    legacy_kind = mind.get("kind")
    subject = mind.get("subject")
    if legacy_kind not in SUBJECT_TYPE_BY_LEGACY_KIND:
        errors.append("source manifest mind.kind is missing or unsupported")
    if not isinstance(subject, dict):
        errors.append("source manifest mind.subject must be a mapping")
    elif legacy_kind in SUBJECT_TYPE_BY_LEGACY_KIND:
        expected_type = SUBJECT_TYPE_BY_LEGACY_KIND[legacy_kind]
        if subject.get("type") != expected_type:
            errors.append(
                "mind.kind cannot be removed safely because it disagrees with mind.subject.type"
            )

    provider_fields = [field for field in REMOVED_PROVIDER_FIELDS if field in candidate]
    nonempty_provider_fields = [
        field
        for field in provider_fields
        if candidate.get(field) not in (None, [], {})
    ]
    if nonempty_provider_fields and not provider_projection_preserved:
        errors.append(
            "provider organization projection must be preserved in canonical relationships "
            "or a provider integration before removal; canonical ids are never inferred from provider logins"
        )

    if errors:
        return None, errors

    mind.pop("kind", None)
    for field in provider_fields:
        candidate.pop(field, None)
    candidate["schema_version"] = 3
    candidate["protocol"] = {"id": "mind", "version": TARGET_PROTOCOL}
    return candidate, []


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument(
        "--provider-projection-preserved",
        action="store_true",
        help="assert that any non-empty provider organization projection has already been preserved outside the core manifest",
    )
    return parser.parse_args()


def main() -> int:
    arguments = parse_arguments()
    try:
        source = load_yaml_mapping(arguments.source.resolve())
        migrated, errors = migrate_manifest(
            source,
            provider_projection_preserved=arguments.provider_projection_preserved,
        )
    except (OSError, TypeError, ValueError) as error:
        print(f"manifest migration failed: {error}", file=sys.stderr)
        return 1

    if errors or migrated is None:
        print("manifest migration failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    rendered = yaml.safe_dump(migrated, sort_keys=False, allow_unicode=True)
    if arguments.output is None:
        sys.stdout.write(rendered)
    else:
        arguments.output.resolve().write_text(rendered, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
