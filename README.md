# mind

> Vendor-independent context repository.
> A minimal shared foundation for human and AI systems.

## Purpose

`mind` stores structured, versioned context that can be consumed by different people, assistants, and software systems without duplicating canonical knowledge across tools.

This foundation intentionally contains no personal identity, organization identity, project implementation, or current operational state. Those belong in repositories derived from this baseline.

## Principles

- One source of truth.
- One topic per file.
- Markdown first for knowledge.
- YAML for machine-readable configuration.
- Git versioning.
- Human readable.
- AI friendly.
- Stable knowledge separated from temporary state.
- Cross-reference instead of duplication.

## Repository Structure

```text
.assistant/
identity/
knowledge/
systems/
projects/
state/
archive/
```

The directories define contracts, not content ownership:

- `identity/` describes the identity of the repository owner: a person, organization, or system.
- `knowledge/` contains durable domain knowledge.
- `systems/` contains reusable specifications and workflows.
- `projects/` contains self-contained project context.
- `state/` contains current priorities and active work.
- `archive/` preserves historical context that is not loaded by default.
- `.assistant/` contains vendor-independent assistant configuration.

## Design Rules

- Give every concept one canonical location.
- Keep files focused.
- Prefer specifications over loose notes.
- Keep assistant behavior separate from project implementation.
- Do not commit secrets or sensitive private data.

## Derivation

This branch is the neutral context-engineering foundation from which personal and organization-specific repositories may diverge independently.
