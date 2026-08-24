#!/usr/bin/env python3
# © 2026 aiaiaiai · aiaiaiai.org
# SPDX-License-Identifier: MIT
"""Validate deterministic canonical visual-asset resolution and synthetic fixtures."""

from __future__ import annotations

import hashlib
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from jsonschema import Draft202012Validator

from validate_manifest import load_schema, load_yaml_mapping, schema_errors


ROOT = Path(__file__).resolve().parents[1]
IDENTITY_SCHEMA_PATH = ROOT / "schema/identity.schema.json"
VISUAL_ASSETS_SCHEMA_PATH = ROOT / "schema/visual-assets.schema.json"
FIXTURE_ROOT = ROOT / "tests" / "fixtures" / "visual_identity"

NORMATIVE_MEDIA_TYPES = frozenset({"image/svg+xml", "image/png"})
OPTIONAL_MEDIA_TYPES = frozenset({"image/webp"})
PROTOCOL_MEDIA_TYPES = NORMATIVE_MEDIA_TYPES | OPTIONAL_MEDIA_TYPES


@dataclass(frozen=True)
class ResolutionResult:
    status: str
    asset_ref: str | None = None
    media_type: str | None = None
    resource_path: Path | None = None


def _safe_publication_path(publication_root: Path, relative_path: str) -> Path | None:
    root = publication_root.resolve()
    candidate = (root / relative_path).resolve()
    if candidate != root and root not in candidate.parents:
        return None
    return candidate


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def resolve_primary_mark(
    identity: dict,
    catalog: dict,
    publication_root: Path,
    *,
    supported_media_types: Iterable[str] | None = None,
) -> ResolutionResult:
    visual_identity = identity.get("visual_identity")
    if not isinstance(visual_identity, dict):
        return ResolutionResult(status="unavailable")

    primary_mark = visual_identity.get("primary_mark")
    if not isinstance(primary_mark, dict):
        return ResolutionResult(status="unavailable")

    asset_ref = primary_mark.get("asset_ref")
    if not isinstance(asset_ref, str) or not asset_ref:
        return ResolutionResult(status="missing")

    assets = catalog.get("assets")
    if not isinstance(assets, list):
        return ResolutionResult(status="missing", asset_ref=asset_ref)

    matches = [asset for asset in assets if isinstance(asset, dict) and asset.get("ref") == asset_ref]
    if not matches:
        return ResolutionResult(status="missing", asset_ref=asset_ref)
    if len(matches) != 1:
        return ResolutionResult(status="ambiguous", asset_ref=asset_ref)

    descriptor = matches[0]
    media_type = descriptor.get("media_type")
    if media_type not in PROTOCOL_MEDIA_TYPES:
        return ResolutionResult(
            status="unsupported_media",
            asset_ref=asset_ref,
            media_type=media_type if isinstance(media_type, str) else None,
        )

    supported = PROTOCOL_MEDIA_TYPES if supported_media_types is None else frozenset(supported_media_types)
    if media_type not in supported:
        return ResolutionResult(
            status="unsupported_media",
            asset_ref=asset_ref,
            media_type=media_type,
        )

    relative_path = descriptor.get("resource_path")
    if not isinstance(relative_path, str) or not relative_path:
        return ResolutionResult(status="missing", asset_ref=asset_ref, media_type=media_type)

    resource_path = _safe_publication_path(publication_root, relative_path)
    if resource_path is None or not resource_path.is_file():
        return ResolutionResult(
            status="missing",
            asset_ref=asset_ref,
            media_type=media_type,
            resource_path=resource_path,
        )

    integrity = descriptor.get("integrity")
    expected_digest = integrity.get("digest") if isinstance(integrity, dict) else None
    if not isinstance(expected_digest, str) or _sha256(resource_path) != expected_digest:
        return ResolutionResult(
            status="integrity_error",
            asset_ref=asset_ref,
            media_type=media_type,
            resource_path=resource_path,
        )

    return ResolutionResult(
        status="resolved",
        asset_ref=asset_ref,
        media_type=media_type,
        resource_path=resource_path,
    )


def validate_catalog_semantics(catalog: dict, publication_root: Path) -> list[str]:
    errors: list[str] = []
    seen_refs: set[str] = set()

    for index, descriptor in enumerate(catalog.get("assets", [])):
        if not isinstance(descriptor, dict):
            continue

        asset_ref = descriptor.get("ref")
        if isinstance(asset_ref, str):
            if asset_ref in seen_refs:
                errors.append(f"assets[{index}].ref: duplicate canonical asset ref {asset_ref!r}")
            seen_refs.add(asset_ref)

        relative_path = descriptor.get("resource_path")
        if isinstance(relative_path, str):
            path = _safe_publication_path(publication_root, relative_path)
            if path is None:
                errors.append(f"assets[{index}].resource_path: path escapes publication root")

    return errors


def validate_fixture(fixture_root: Path) -> tuple[str | None, list[str]]:
    errors: list[str] = []
    identity = load_yaml_mapping(fixture_root / "identity.yaml")
    catalog = load_yaml_mapping(fixture_root / "visual-assets.yaml")

    identity_schema = load_schema(IDENTITY_SCHEMA_PATH)
    errors.extend(
        f"identity{error[1:]}"
        for error in schema_errors(Draft202012Validator(identity_schema), identity)
    )

    catalog_schema = load_schema(VISUAL_ASSETS_SCHEMA_PATH)
    errors.extend(
        f"visual-assets{error[1:]}"
        for error in schema_errors(Draft202012Validator(catalog_schema), catalog)
    )
    errors.extend(validate_catalog_semantics(catalog, fixture_root))

    subject_type = identity.get("type") if isinstance(identity.get("type"), str) else None
    if errors:
        return subject_type, errors

    result = resolve_primary_mark(identity, catalog, fixture_root)
    if result.status != "resolved":
        errors.append(f"primary_mark resolution must be 'resolved', got {result.status!r}")

    return subject_type, errors


def main() -> int:
    required_types = {"person", "organization", "agent"}
    discovered_types: set[str] = set()
    errors: list[str] = []

    if not FIXTURE_ROOT.is_dir():
        errors.append("visual identity fixture root is missing")
    else:
        for fixture in sorted(path for path in FIXTURE_ROOT.iterdir() if path.is_dir()):
            try:
                subject_type, fixture_errors = validate_fixture(fixture)
            except (KeyError, TypeError, ValueError) as error:
                errors.append(f"{fixture.name}: {error}")
                continue

            if subject_type:
                discovered_types.add(subject_type)
            errors.extend(f"{fixture.name}: {error}" for error in fixture_errors)

    missing_types = sorted(required_types - discovered_types)
    if missing_types:
        errors.append(f"missing required visual identity fixture types: {', '.join(missing_types)}")

    if errors:
        print("visual asset conformance failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("canonical visual asset fixtures are valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
