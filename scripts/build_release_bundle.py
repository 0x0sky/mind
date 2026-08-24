#!/usr/bin/env python3
# © 2026 aiaiaiai · aiaiaiai.org
# SPDX-License-Identifier: MIT
"""Build and verify a deterministic Mind Protocol formal-release bundle."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import tempfile
import zipfile
from pathlib import Path
from typing import Iterable

from generate_baseline import generate_baseline
from validate_manifest import load_yaml_mapping


ROOT = Path(__file__).resolve().parents[1]
PROTOCOL_PATH = ROOT / "protocol.yaml"
CONFORMANCE_PATH = ROOT / "conformance.yaml"
COMPATIBILITY_PATH = ROOT / "compatibility.yaml"
SCHEMA_ROOT = ROOT / "schema"
RELEASE_POLICY_PATH = ROOT / "docs" / "protocol" / "RELEASE_POLICY.md"
FIXED_ZIP_TIME = (1980, 1, 1, 0, 0, 0)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def protocol_version() -> str:
    descriptor = load_yaml_mapping(PROTOCOL_PATH)
    value = descriptor.get("protocol", {}).get("version")
    if not isinstance(value, str) or not value:
        raise ValueError("protocol.yaml must declare protocol.version")
    return value


def version_line(version: str) -> str:
    core = version.split("-", 1)[0].split("+", 1)[0]
    parts = core.split(".")
    if len(parts) != 3 or not all(part.isdigit() for part in parts):
        raise ValueError(f"invalid protocol version {version!r}")
    return f"{parts[0]}.{parts[1]}"


def release_notes_path(version: str) -> Path:
    return ROOT / "docs" / "protocol" / "releases" / f"v{version}.md"


def migration_guide_path(version: str) -> Path:
    return ROOT / "docs" / "protocol" / f"MIGRATION_{version_line(version)}.md"


def source_files(version: str) -> list[tuple[str, Path]]:
    entries: list[tuple[str, Path]] = [
        ("protocol.yaml", PROTOCOL_PATH),
        ("conformance.yaml", CONFORMANCE_PATH),
        ("compatibility.yaml", COMPATIBILITY_PATH),
        ("release-policy.md", RELEASE_POLICY_PATH),
        ("migration-guide.md", migration_guide_path(version)),
        ("release-notes.md", release_notes_path(version)),
    ]
    entries.extend(
        (f"schema/{path.name}", path)
        for path in sorted(SCHEMA_ROOT.glob("*.json"))
        if path.is_file()
    )
    return entries


def collect_bundle_files(version: str, baseline_root: Path) -> dict[str, bytes]:
    files: dict[str, bytes] = {}
    for relative_path, source in source_files(version):
        if not source.is_file():
            raise ValueError(f"required release source is missing: {source.relative_to(ROOT)}")
        files[relative_path] = source.read_bytes()

    for path in sorted(baseline_root.rglob("*")):
        if path.is_file():
            relative = path.relative_to(baseline_root).as_posix()
            files[f"neutral-baseline/{relative}"] = path.read_bytes()

    manifest = {
        "schema_version": 1,
        "artifact": "mind-protocol-release-bundle",
        "protocol": {"id": "mind", "version": version},
        "files": {
            path: sha256_bytes(data)
            for path, data in sorted(files.items())
        },
    }
    files["release-manifest.json"] = (
        json.dumps(manifest, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")
    return files


def write_zip(output: Path, version: str, files: dict[str, bytes]) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    root_name = f"mind-protocol-v{version}"
    with zipfile.ZipFile(
        output,
        mode="w",
        compression=zipfile.ZIP_DEFLATED,
        compresslevel=9,
    ) as archive:
        for relative_path, data in sorted(files.items()):
            info = zipfile.ZipInfo(f"{root_name}/{relative_path}", date_time=FIXED_ZIP_TIME)
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, data, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)


def build_release_bundle(output: Path, *, expected_version: str | None = None) -> str:
    version = protocol_version()
    if expected_version is not None and version != expected_version:
        raise ValueError(
            f"release version {expected_version!r} does not match protocol.yaml {version!r}"
        )

    with tempfile.TemporaryDirectory() as directory:
        baseline = Path(directory) / "baseline"
        generate_baseline(baseline)
        files = collect_bundle_files(version, baseline)
        write_zip(output, version, files)
    return sha256_file(output)


def zip_entries(path: Path) -> list[str]:
    with zipfile.ZipFile(path, "r") as archive:
        return sorted(archive.namelist())


def check_release_bundle() -> list[str]:
    errors: list[str] = []
    version = protocol_version()
    with tempfile.TemporaryDirectory() as first_dir, tempfile.TemporaryDirectory() as second_dir:
        first = Path(first_dir) / f"mind-protocol-v{version}.zip"
        second = Path(second_dir) / f"mind-protocol-v{version}.zip"
        first_digest = build_release_bundle(first, expected_version=version)
        second_digest = build_release_bundle(second, expected_version=version)
        if first_digest != second_digest or first.read_bytes() != second.read_bytes():
            errors.append("formal release bundle is not byte-for-byte deterministic")

        entries = zip_entries(first)
        prefix = f"mind-protocol-v{version}/"
        required_entries = {
            prefix + "protocol.yaml",
            prefix + "conformance.yaml",
            prefix + "compatibility.yaml",
            prefix + "release-manifest.json",
            prefix + "release-policy.md",
            prefix + "migration-guide.md",
            prefix + "release-notes.md",
            prefix + "neutral-baseline/baseline.json",
            prefix + "neutral-baseline/manifest.yaml",
        }
        missing = sorted(required_entries - set(entries))
        if missing:
            errors.append("formal release bundle is missing entries: " + ", ".join(missing))
    return errors


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--version", help="require protocol.yaml to match this version")
    parser.add_argument("--output", type=Path, help="output .zip path")
    parser.add_argument("--sha256-output", type=Path, help="optional digest file")
    return parser.parse_args()


def main() -> int:
    arguments = parse_arguments()
    try:
        if arguments.check:
            errors = check_release_bundle()
            if errors:
                print("release bundle validation failed:", file=sys.stderr)
                for error in errors:
                    print(f"- {error}", file=sys.stderr)
                return 1
            print("formal release bundle is deterministic and complete")
            return 0

        if arguments.output is None:
            print("release bundle build failed: --output is required", file=sys.stderr)
            return 2
        digest = build_release_bundle(
            arguments.output.resolve(),
            expected_version=arguments.version,
        )
        if arguments.sha256_output is not None:
            arguments.sha256_output.resolve().write_text(
                f"{digest}  {arguments.output.name}\n",
                encoding="utf-8",
            )
        print(json.dumps({"output": str(arguments.output), "sha256": digest}, sort_keys=True))
        return 0
    except (OSError, TypeError, ValueError, zipfile.BadZipFile) as error:
        print(f"release bundle build failed: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
