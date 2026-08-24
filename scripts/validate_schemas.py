#!/usr/bin/env python3
# © 2026 aiaiaiai · aiaiaiai.org
# SPDX-License-Identifier: MIT
"""Validate every JSON Schema published by the Mind Protocol repository."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_ROOT = REPOSITORY_ROOT / "schema"


def main() -> int:
    schema_paths = sorted(SCHEMA_ROOT.rglob("*.json"))
    if not schema_paths:
        print("schema validation failed:\n- no JSON Schema files found", file=sys.stderr)
        return 1

    errors: list[str] = []
    for path in schema_paths:
        relative = path.relative_to(REPOSITORY_ROOT).as_posix()
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            errors.append(f"{relative}: invalid JSON: {error}")
            continue

        if not isinstance(value, dict):
            errors.append(f"{relative}: schema root must be a JSON object")
            continue

        try:
            Draft202012Validator.check_schema(value)
        except SchemaError as error:
            errors.append(f"{relative}: invalid Draft 2020-12 schema: {error.message}")

    if errors:
        print("schema validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"validated {len(schema_paths)} JSON Schemas")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
