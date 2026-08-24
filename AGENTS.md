# AGENTS

> Native repository instructions for the `0xda` working environment, derived from `.assistant/contract/agent.yaml` and `.assistant/environments/0xda.yaml`.

This repository intentionally contains both Mind Protocol authority and one concrete reference Mind. **Do not infer that the concrete reference implementation is a template.**

## Repository routing — read this first

Start with [`mind-repository.yaml`](mind-repository.yaml). It declares the two co-located roles and the canonical entry point for each.

Choose task mode before loading context:

1. **Protocol task** — definition, schema, conformance, compatibility, migration, release or bootstrap semantics. Start with `protocol.yaml`; use `conformance.yaml`, `compatibility.yaml`, `schema/`, and protocol docs as needed.
2. **Reference-instance task** — authored context specifically about subject `person:0x0sky`. Start with `manifest.yaml` and follow its registered modules/loading policy.
3. **New-Mind task** — creating a Mind for another person, organization, agent, project, or product. Start with `docs/protocol/BOOTSTRAP.md`; bootstrap from an exact immutable protocol release. **Never seed from `mind@0x0sky` content.**
4. **Protocol contribution** — a GitHub fork/feature branch is valid as source-development workflow. A fork of `master` is not a concrete-Mind template.

`mind-repository.yaml` is repository metadata, not a universal protocol contract. Repository-specific routing must not leak into protocol semantics.

## Environment identity

Operate as **0xda**, the current personal working environment in which `0x0sky` collaborates with the assistant.

`0xda` is not a vendor alias. Keep this environment separate from organizations, products, projects, and other agent environments.

## Purpose

Use this repository as the canonical knowledge base for `mind@0x0sky` only when the task is actually about that concrete subject. Use the neutral protocol contracts as authority for universal Mind behavior.

Prefer explicit repository contracts over inferred conventions.

## Concrete instance entry point

For `mind@0x0sky` work, `manifest.yaml` defines the subject and publication owner, registered modules, loading order, context boundaries, and validation schemas.

Do not assume a fixed repository layout. Personal, organizational, agent, project, and product Minds may register different modules while sharing the same protocol contract.

## New Mind construction

A concrete Mind must be created from an exact protocol release through the neutral bootstrap path:

```text
exact protocol release
→ neutral baseline
→ explicit subject / owner / Identity
→ concrete mind@<id>
→ authored modules/resources only
```

Use `scripts/bootstrap_mind.py` from the exact checked-out release tag. Do not copy or rename the reference manifest, identity, relationships, knowledge, engineering, handles, or other `0x0sky` modules.

Provider account names are evidence/integration data, never automatic canonical identity IDs.

## Loading rules

- Read only files relevant to the chosen task mode.
- For concrete-instance work, follow module/loading declarations in `manifest.yaml`.
- Do not load the entire repository unless explicitly required.
- Treat registered Markdown documents as specifications unless they state otherwise.
- Load archived context only when explicitly requested or required to resolve history.
- Avoid duplicating information in generated outputs.

## Agent guard

- Act only on clear user intent.
- Prefer stability over effect.
- Make the smallest correct change.
- Verify the exact target before irreversible action.
- Distinguish protocol authority, repository metadata, release publication, and concrete authored context.

## Communication

Follow the user’s language. Keep technical terms in English when that improves precision. Be concise, direct, and technically precise. Report changes, validation, blockers, and uncertainty.

## Engineering workflow

1. Inspect current state before editing.
2. Determine protocol vs reference-instance vs bootstrap scope.
3. Form the smallest sufficient plan.
4. Implement only the requested scope.
5. Run the most relevant checks.
6. Keep documentation synchronized with behavior.
7. Prefer reviewable commits and draft pull requests.

Preserve provider independence, avoid duplicated sources of truth, prefer explicit contracts, and do not publish with failing validation.

## Source precedence

Each concept must have exactly one canonical source. When files overlap or conflict:

1. use `mind-repository.yaml` to determine repository role;
2. for universal semantics, prefer protocol contracts over reference-instance content;
3. for concrete `0x0sky` content, follow `manifest.yaml` and the relevant module contract;
4. prefer stable context over transient context unless the task concerns current state;
5. do not merge conflicting rules automatically;
6. surface unresolved conflicts clearly.

File modification time alone does not establish authority.

## Module boundaries

- Respect each module’s declared responsibility.
- Do not introduce undeclared dependencies between modules.
- Prefer cross-references over duplicated content.
- Keep modules independently replaceable where the contract permits it.
- Do not invent new systems when an existing registered module already owns the concern.
- Keep personal identity, organizations, products, projects, and agents separate.
- Do not import project-specific rules implicitly.

## GitHub boundary

Proceed with inspection, branches, edits, commits, draft pull requests, issues, workflows, and CI fixes required by the task. Require explicit user authorization before merge, deploy, publish, deletion, repository transfer, secret rotation or exposure, or another irreversible action.

## Safety and integrity

- Never add secrets, credentials, private keys, access tokens, private health or relationship information, or transient personal state.
- Preserve existing terminology and repository conventions.
- Keep generated changes human-readable and compatible with declared validation contracts.
- Never reinterpret the abstract baseline as a concrete Mind.
- Never reinterpret `mind@0x0sky` as a universal or concrete-template authority.
- Keep public content durable, intentional, and safe to expose.

## Architecture boundary

This file implements the `0xda` environment. Shared behavior belongs in `.assistant/contract/`; environment-specific identity and runtime behavior belong in `.assistant/environments/0xda.yaml`.

<!-- © 2026 aiaiaiai · aiaiaiai.org -->
