#!/usr/bin/env python3
# © 2026 aiaiaiai · aiaiaiai.org
# SPDX-License-Identifier: MIT
"""Bootstrap a minimal concrete Mind from the exact checked-out protocol release."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

import yaml

from generate_baseline import generate_baseline
from semver import SemVer
from validate_manifest import load_json_mapping, load_yaml_mapping


ROOT = Path(__file__).resolve().parents[1]
PROTOCOL_REPOSITORY = "0x0sky/mind"
CONCRETE_TYPES = ("person", "organization", "agent", "project", "product")
RELEASE_CONTRACT_PATHS = (
    "protocol.yaml",
    "conformance.yaml",
    "compatibility.yaml",
    "schema",
)


def write_yaml(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        yaml.safe_dump(value, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )


def git_blob_sha1(path: Path) -> str:
    data = path.read_bytes()
    header = f"blob {len(data)}\0".encode("utf-8")
    return hashlib.sha1(header + data).hexdigest()


def git_output(*arguments: str) -> str:
    try:
        result = subprocess.run(
            ["git", *arguments],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError as error:
        raise ValueError(f"cannot verify protocol release checkout: {error}") from error
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip() or "git command failed"
        raise ValueError(
            "cannot verify protocol release checkout: "
            f"git {' '.join(arguments)}: {detail}"
        )
    return result.stdout.strip()


def ensure_empty_output(output: Path) -> None:
    if output.exists() and any(output.iterdir()):
        raise ValueError(f"output directory is not empty: {output}")


def entity(entity_type: str, entity_id: str) -> dict[str, str]:
    if entity_type not in CONCRETE_TYPES:
        raise ValueError(f"unsupported concrete subject/owner type: {entity_type!r}")
    if not entity_id.strip():
        raise ValueError("entity id must not be empty")
    if entity_id == "unspecified":
        raise ValueError("concrete entity id must not be 'unspecified'")
    return {"type": entity_type, "id": entity_id}


def protocol_ref() -> dict[str, str]:
    descriptor = load_yaml_mapping(ROOT / "protocol.yaml")
    value = descriptor.get("protocol")
    if not isinstance(value, dict):
        raise ValueError("protocol.yaml must declare protocol mapping")
    protocol_id = value.get("id")
    version = value.get("version")
    if not isinstance(protocol_id, str) or not isinstance(version, str):
        raise ValueError("protocol.yaml must declare string protocol id/version")
    SemVer.parse(version)
    return {"id": protocol_id, "version": version}


def validate_source_tag(source_tag: str, protocol: dict[str, str]) -> None:
    expected = f"v{protocol['version']}"
    if source_tag != expected:
        raise ValueError(
            f"source tag must exactly match checked-out protocol version: expected {expected!r}"
        )
    if source_tag in {"master", "main", "latest"}:
        raise ValueError("floating branches are forbidden as concrete release sources")


def verify_release_checkout(source_tag: str) -> None:
    """Prove CLI bootstrap is running from the exact immutable release tree."""
    protocol = protocol_ref()
    validate_source_tag(source_tag, protocol)

    repository_root = Path(git_output("rev-parse", "--show-toplevel")).resolve()
    if repository_root != ROOT.resolve():
        raise ValueError(
            "bootstrap must run from the Mind Protocol repository checkout "
            f"at {ROOT.resolve()}"
        )

    head_sha = git_output("rev-parse", "HEAD")
    tag_sha = git_output("rev-list", "-n", "1", f"refs/tags/{source_tag}")
    if head_sha != tag_sha:
        raise ValueError(
            "checked-out HEAD must equal the immutable protocol release tag: "
            f"HEAD {head_sha}, {source_tag} {tag_sha}"
        )

    dirty_contracts = git_output(
        "status",
        "--porcelain",
        "--untracked-files=no",
        "--",
        *RELEASE_CONTRACT_PATHS,
    )
    if dirty_contracts:
        raise ValueError(
            "released protocol contract files differ from the tagged checkout; "
            "restore protocol.yaml, conformance.yaml, compatibility.yaml, and schema/ "
            "before bootstrapping"
        )


def concrete_manifest(
    protocol: dict[str, str],
    subject: dict[str, str],
    owner: dict[str, str],
    *,
    context_version: str,
    repository_visibility: str,
) -> dict[str, Any]:
    SemVer.parse(context_version)
    allowed_context = (
        "durable_public_context"
        if repository_visibility == "public"
        else "durable_private_context"
    )
    return {
        "schema_version": 3,
        "protocol": protocol,
        "mind": {
            "name": f"mind@{subject['id']}",
            "context_version": context_version,
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
                "repository": repository_visibility,
                "allowed": allowed_context,
                "forbidden": ["credentials", "secrets"],
            },
        },
        "loading": {"default": ["identity"], "optional": []},
        "validation": {
            "schema": "schema/mind.schema.json",
            "module_schema": "schema/module.schema.json",
        },
    }


def identity_module(owner: dict[str, str], visibility: str) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "module": {
            "id": "identity",
            "purpose": "implement the canonical identity contract for this concrete Mind subject",
            "stability": "stable",
            "dependencies": [],
            "entrypoints": [],
            "owner": owner,
            "visibility": visibility,
            "resources": {
                "identity": {
                    "path": "identity/identity.yaml",
                    "format": "yaml",
                    "schema": "schema/identity-resource.schema.json",
                }
            },
        },
    }


def identity_resource(subject: dict[str, str], display_name: str) -> dict[str, Any]:
    if not display_name.strip():
        raise ValueError("display name must not be empty")
    return {
        "schema_version": 1,
        "identity": {
            "type": subject["type"],
            "id": subject["id"],
            "display_name": display_name,
        },
        "validation": {"schema": "schema/identity-resource.schema.json"},
    }


def repository_metadata(
    protocol: dict[str, str], subject: dict[str, str], source_tag: str
) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "scope": "repository_metadata",
        "protocol_contract": False,
        "repository": {
            "roles": {
                "protocol_authority": {"enabled": False},
                "concrete_mind": {
                    "enabled": True,
                    "entrypoint": "manifest.yaml",
                    "canonical_for_subject": subject,
                    "reference_implementation": False,
                    "template_authority": False,
                },
            }
        },
        "routing": {
            "concrete_instance": "manifest.yaml",
            "protocol_lock": "protocol.lock.yaml",
        },
        "protocol_consumption": {
            "id": protocol["id"],
            "version": protocol["version"],
            "source_tag": source_tag,
            "floating_master": "forbidden",
        },
        "fork_policy": {
            "copy_reference_instance_content": "forbidden",
            "creation_mechanism": "exact_release_bootstrap",
        },
        "version_axes": {
            "protocol_version": "external_release",
            "context_version": "independent_concrete_publication",
        },
    }


def protocol_lock(protocol: dict[str, str], source_tag: str, output: Path) -> dict[str, Any]:
    contract_files: dict[str, Any] = {}
    for name in ("protocol.yaml", "conformance.yaml", "compatibility.yaml"):
        contract_files[name] = {"git_blob_sha1": git_blob_sha1(output / name)}

    schemas: dict[str, Any] = {}
    for path in sorted((output / "schema").glob("*.json")):
        schema = load_json_mapping(path)
        schema_id = schema.get("$id")
        if not isinstance(schema_id, str):
            raise ValueError(f"published schema has no string $id: {path.name}")
        schemas[f"schema/{path.name}"] = {
            "schema_id": schema_id,
            "git_blob_sha1": git_blob_sha1(path),
        }

    return {
        "schema_version": 1,
        "protocol": protocol,
        "source": {
            "repository": PROTOCOL_REPOSITORY,
            "tag": source_tag,
            "floating_branch": "forbidden",
        },
        "reference_instance": {
            "template_authority": False,
            "copy_content": "forbidden",
        },
        "contract_files": contract_files,
        "vendored_contracts": schemas,
        "context_versioning": {
            "independent_from_protocol": True,
            "protocol_tags_in_this_repository": "forbidden",
        },
    }


def generated_readme(
    protocol: dict[str, str], subject: dict[str, str], source_tag: str
) -> str:
    return f"""# mind@{subject['id']}

This repository is a **concrete Mind implementation** for `{subject['type']}:{subject['id']}`.

It consumes Mind Protocol `{protocol['version']}` from the exact immutable release tag `{source_tag}`. It does **not** define Mind Protocol.

Start with `mind-repository.yaml` to determine repository role, then `manifest.yaml` for this concrete publication. Vendored protocol contracts are locked by `protocol.lock.yaml` and must not be refreshed from floating `master`.

Identity and context in this repository must be authored for this subject. Do not copy `mind@0x0sky` personal modules or infer canonical IDs from provider/GitHub account names.
"""


def generated_agents(subject: dict[str, str]) -> str:
    return f"""# AGENTS

This repository is a concrete Mind consumer for `{subject['type']}:{subject['id']}`, not Mind Protocol authority.

Read `mind-repository.yaml` first, then `manifest.yaml` and only the modules relevant to the task. Treat vendored `protocol.yaml`, `conformance.yaml`, `compatibility.yaml`, and `schema/` as exact release contracts locked by `protocol.lock.yaml`.

Do not source protocol contracts from floating branches. Do not copy content from the `mind@0x0sky` reference implementation. Do not infer canonical identity or relationships from provider metadata. Add only durable authored context for this subject and preserve the independent `mind.context_version` axis.
"""


def bootstrap_mind(
    output: Path,
    *,
    source_tag: str,
    subject_type: str,
    subject_id: str,
    display_name: str,
    context_version: str,
    repository_visibility: str,
    owner_type: str | None = None,
    owner_id: str | None = None,
) -> None:
    if repository_visibility not in {"public", "private"}:
        raise ValueError("repository visibility must be 'public' or 'private'")
    if (owner_type is None) != (owner_id is None):
        raise ValueError("owner type and owner id must be supplied together")

    ensure_empty_output(output)
    protocol = protocol_ref()
    validate_source_tag(source_tag, protocol)
    subject = entity(subject_type, subject_id)
    owner = (
        entity(owner_type, owner_id)  # type: ignore[arg-type]
        if owner_type is not None and owner_id is not None
        else dict(subject)
    )

    generate_baseline(output)
    baseline_metadata = output / "baseline.json"
    if baseline_metadata.exists():
        baseline_metadata.unlink()

    write_yaml(
        output / "manifest.yaml",
        concrete_manifest(
            protocol,
            subject,
            owner,
            context_version=context_version,
            repository_visibility=repository_visibility,
        ),
    )
    write_yaml(
        output / "identity" / "module.yaml",
        identity_module(owner, repository_visibility),
    )
    write_yaml(
        output / "identity" / "identity.yaml",
        identity_resource(subject, display_name),
    )
    write_yaml(
        output / "mind-repository.yaml",
        repository_metadata(protocol, subject, source_tag),
    )
    write_yaml(
        output / "protocol.lock.yaml",
        protocol_lock(protocol, source_tag, output),
    )
    (output / "README.md").write_text(
        generated_readme(protocol, subject, source_tag), encoding="utf-8"
    )
    (output / "AGENTS.md").write_text(generated_agents(subject), encoding="utf-8")


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--source-tag", required=True)
    parser.add_argument("--subject-type", required=True, choices=CONCRETE_TYPES)
    parser.add_argument("--subject-id", required=True)
    parser.add_argument("--display-name", required=True)
    parser.add_argument("--owner-type", choices=CONCRETE_TYPES)
    parser.add_argument("--owner-id")
    parser.add_argument("--context-version", required=True)
    parser.add_argument(
        "--repository-visibility", required=True, choices=("public", "private")
    )
    return parser.parse_args()


def main() -> int:
    arguments = parse_arguments()
    try:
        verify_release_checkout(arguments.source_tag)
        bootstrap_mind(
            arguments.output.resolve(),
            source_tag=arguments.source_tag,
            subject_type=arguments.subject_type,
            subject_id=arguments.subject_id,
            display_name=arguments.display_name,
            context_version=arguments.context_version,
            repository_visibility=arguments.repository_visibility,
            owner_type=arguments.owner_type,
            owner_id=arguments.owner_id,
        )
    except (OSError, TypeError, ValueError, yaml.YAMLError) as error:
        print(f"Mind bootstrap failed: {error}", file=sys.stderr)
        return 1

    print(
        json.dumps(
            {
                "output": str(arguments.output.resolve()),
                "source_tag": arguments.source_tag,
                "subject": {
                    "type": arguments.subject_type,
                    "id": arguments.subject_id,
                },
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
