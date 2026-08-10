#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
LOCALES = ROOT / "writing" / "locales"
REQUIRED_FILES = ("README.md", "locale.yaml")


def shape(value: Any) -> Any:
    """Return recursive mapping structure while treating scalar/list values as data."""
    if isinstance(value, dict):
        return {key: shape(item) for key, item in value.items()}
    return "<value>"


def h2_sections(markdown: str) -> list[str]:
    return re.findall(r"^##\s+(.+?)\s*$", markdown, flags=re.MULTILINE)


def fail(message: str) -> None:
    print(f"locale validation failed: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> None:
    locale_dirs = sorted(path for path in LOCALES.iterdir() if path.is_dir() and not path.name.startswith("."))
    if not locale_dirs:
        fail("no locale directories found")

    reference_shape = None
    reference_sections = None
    reference_name = None

    for directory in locale_dirs:
        for filename in REQUIRED_FILES:
            if not (directory / filename).is_file():
                fail(f"{directory.name} is missing {filename}")

        with (directory / "locale.yaml").open("r", encoding="utf-8") as handle:
            data = yaml.safe_load(handle)

        if not isinstance(data, dict):
            fail(f"{directory.name}/locale.yaml must contain a mapping")
        if data.get("schema_version") != 1:
            fail(f"{directory.name} must use schema_version: 1")
        if data.get("locale", {}).get("id") != directory.name:
            fail(f"{directory.name}: locale.id must match the directory name")

        current_shape = shape(data)
        sections = h2_sections((directory / "README.md").read_text(encoding="utf-8"))

        if reference_shape is None:
            reference_shape = current_shape
            reference_sections = sections
            reference_name = directory.name
            continue

        if current_shape != reference_shape:
            fail(f"{directory.name} YAML structure differs from {reference_name}")
        if sections != reference_sections:
            fail(f"{directory.name} README H2 structure differs from {reference_name}: {sections!r} != {reference_sections!r}")

    print(f"validated {len(locale_dirs)} structurally compatible stylistic locales: " + ", ".join(path.name for path in locale_dirs))


if __name__ == "__main__":
    main()
