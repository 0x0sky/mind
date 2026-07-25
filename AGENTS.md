# AGENTS

> OpenAI-facing repository instructions rendered from `.assistant/contract/agent.yaml` through `.assistant/adapters/openai.yaml`, with `.assistant/personas/0x0da.yaml` applied.

This repository is the primary source of context for its Mind implementation.

## Purpose

Use this repository as the canonical knowledge base before relying on assumptions or inferred context. Prefer explicit repository contracts over conventions that are not declared by the repository.

## Entry point

Start with `manifest.yaml`. It defines the Mind kind and owner, registered modules, module loading order, optional context, and validation schema.

Do not assume a fixed repository layout. Personal, organizational, and future Mind implementations may register different modules while sharing the same baseline contract.

## Loading rules

- Read only the files relevant to the current task.
- Follow module and loading declarations in `manifest.yaml`.
- Do not load the entire repository unless explicitly requested.
- Treat registered Markdown documents as specifications unless they state otherwise.
- Load archived context only when explicitly requested or required to resolve history.
- Avoid duplicating information in generated outputs.

## Agent guard

- Act only on clear user intent.
- Cut off noise, rush, and pressure.
- Prefer stability over effect.
- Make the smallest correct change.
- Verify the exact target before irreversible action.

## Communication

Follow the user’s language. Keep technical terms in English when that improves precision. Be concise, direct, warm, and technically precise. Report changes, validation, blockers, and uncertainty.

## Engineering workflow

1. Inspect the current state before editing.
2. Form the smallest sufficient plan.
3. Implement only the requested scope.
4. Run the most relevant available checks.
5. Keep documentation synchronized with behavior.
6. Prefer reviewable commits and draft pull requests.

Preserve provider independence, avoid duplicated sources of truth, prefer explicit contracts, and do not publish with failing validation.

## Source precedence

Each concept must have exactly one canonical source. When multiple files overlap or conflict:

1. follow explicit precedence declared by `manifest.yaml` or the relevant module contract;
2. prefer the dedicated canonical specification for the concept;
3. prefer stable context over transient context unless the task concerns current state;
4. do not merge conflicting rules automatically;
5. surface unresolved conflicts clearly.

File modification time alone does not establish authority.

## Module boundaries

- Respect each module’s declared responsibility.
- Do not introduce undeclared dependencies between modules.
- Prefer cross-references over duplicated content.
- Keep modules independently replaceable where the contract permits it.
- Do not invent new systems when an existing registered module already owns the concern.
- Keep personal identity, organizations, products, and projects separate.
- Do not import project-specific rules implicitly.

## GitHub boundary

Proceed with inspection, branches, edits, commits, draft pull requests, issues, workflows, and CI fixes required by the task. Require explicit user authorization before merge, deploy, publish, deletion, repository transfer, secret rotation or exposure, or another irreversible action.

## Safety and integrity

- Never add secrets, credentials, private keys, access tokens, private health or relationship information, or transient personal state.
- Preserve existing terminology and repository conventions.
- Keep generated changes human-readable and compatible with the declared validation schema.
- Do not reinterpret an abstract baseline as a concrete personal or organizational implementation.
- Keep public content durable, intentional, and safe to expose.

## Architecture boundary

This file is an OpenAI-facing artifact, not a canonical source. Vendor-neutral behavior belongs in `.assistant/contract/`; persona-specific expression belongs in `.assistant/personas/`; vendor translation belongs in `.assistant/adapters/`.
