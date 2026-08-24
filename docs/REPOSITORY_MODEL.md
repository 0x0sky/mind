# Repository model

`0x0sky/mind` intentionally contains two things in one Git repository, but they have different authority.

## The two roles

| Role | Canonical entry point | What it is authoritative for | What it is not authoritative for |
| --- | --- | --- | --- |
| **Mind Protocol** | [`../protocol.yaml`](../protocol.yaml) | the implementation-independent Mind contract, schemas, conformance, compatibility and formal protocol releases | any named person's or organization's identity/content |
| **`mind@0x0sky`** | [`../manifest.yaml`](../manifest.yaml) | the concrete authored Mind of subject `person:0x0sky` | the structure/content that another concrete Mind should copy |

The coexistence is deliberate: the repository is the protocol source and also hosts one living reference implementation. Co-location does **not** create inheritance between the two roles.

## The rule that removes the ambiguity

> `mind@0x0sky` is a reference implementation, never a template authority.

A new concrete Mind must not be created by changing IDs in a copy of the root `manifest.yaml`, `identity/`, `relationships/`, `knowledge/`, or other personal modules.

The canonical construction path is:

```text
exact immutable Mind Protocol release
            ↓
      neutral baseline
            ↓
subject + publication-owner semantics + Identity
            ↓
      concrete mind@<id>
            ↓
 only authored modules/resources for that subject
```

The neutral baseline contains no concrete identity. Bootstrap requires an explicit subject. Publication owner defaults to that subject; a different owner is permitted only as a complete explicit type/id override.

## What a GitHub fork means

A GitHub fork of `0x0sky/mind` is valid for **protocol development**: reviewing the protocol, proposing changes, running conformance, or experimenting with protocol source.

A GitHub fork of `master` is **not** the canonical way to create another person's, organization's, agent's, project's, or product's Mind. A fork carries the `mind@0x0sky` implementation and its history, so treating it as a template creates accidental identity inheritance.

To create a concrete Mind, use the bootstrap path documented in [`protocol/BOOTSTRAP.md`](protocol/BOOTSTRAP.md) from an exact release tag.

## Authority routing for humans and agents

Before interpreting a root file, determine the task:

- protocol definition or compatibility question → start with `mind-repository.yaml`, then `protocol.yaml`, `conformance.yaml`, and `compatibility.yaml`;
- work about `0x0sky` itself → start with `mind-repository.yaml`, then `manifest.yaml` and its registered modules;
- creation of a new Mind → start with `mind-repository.yaml`, then `docs/protocol/BOOTSTRAP.md`; do not use the reference instance as seed content;
- protocol contribution → a repository fork/branch is fine, but concrete identity content remains outside protocol authority.

`mind-repository.yaml` is repository metadata, not a Mind Protocol contract. Its purpose is to make this routing machine-readable without adding repository-specific semantics to the universal protocol.

## Versioning

The two co-located roles also have independent version axes:

- `protocol.version` is the Mind Protocol release version and is tagged in this repository;
- `mind.context_version` belongs to the concrete `mind@0x0sky` content and changes only when that durable authored context changes.

A protocol version bump does not imply a context bump. A context change does not imply a protocol release.

Concrete Mind repositories consume exact protocol releases but do not receive protocol-version tags as if those tags described their own content.

## Why keep both roles together

Keeping the reference implementation beside the protocol gives the protocol a continuously exercised real implementation and catches leakage early. The neutral-baseline and conformance checks are responsible for proving that the protocol itself stays independent of that implementation.

If co-location ever creates unavoidable contract coupling, separation into repositories would become justified. Until then, explicit authority routing plus a deterministic neutral bootstrap keeps one protocol authority without making the reference person a template.

<!-- © 2026 aiaiaiai · aiaiaiai.org -->
