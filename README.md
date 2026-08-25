# mind@0x0sky

Canonical public Mind for `person:0x0sky`.

This repository is a **concrete Mind Protocol consumer**. It does not define Mind Protocol and must never be used as a template authority for another person, organization, agent, project, or product.

## Authority

- `manifest.yaml` — canonical publication boundary for `mind@0x0sky`;
- `modules/identity/identity.yaml` — canonical machine-readable person Identity;
- registered modules — durable authored public context for this subject;
- `protocol.lock.yaml` — exact immutable Mind Protocol release consumed by this repository.

The canonical protocol repository is `aiaiaiai-org/mind-protocol`. Vendored `protocol.yaml`, `conformance.yaml`, `compatibility.yaml`, and `schema/` are release contracts, not locally authored protocol authority.

## Identity

Canonical Identity:

- **type:** person
- **id:** `0x0sky`
- **display name:** `0x0sky`
- **GitHub namespace:** `github.com/0x0sky` as provider/discovery context only

The stable `identity.id` is provider-independent. A GitHub login, social handle, domain, avatar, repository path, or runtime environment cannot silently redefine it.

See [`modules/identity/README.md`](modules/identity/README.md).

## Modules

`manifest.yaml` is the only registration authority. The current publication composes:

- `identity` — canonical person identity;
- `relationships` — authored relationships and provenance;
- `knowledge` — durable public models and principles;
- `engineering` — software engineering practice;
- `systems` — public software ecosystem and system boundaries;
- `writing` — public creative and linguistic practice.

Folder placement does not define module semantics; the manifest catalog does.

## Protocol consumption

Current binding: **Mind Protocol `0.9.0`**, pinned to immutable release `aiaiaiai-org/mind-protocol@v0.9.0` by `protocol.lock.yaml`.

`mind.context_version` is independent and remains `0.4.0`. A protocol migration does not bump personal context unless durable authored context itself changes.

Protocol-version tags do not belong in this concrete repository.

## Privacy boundary

Never commit credentials, secrets, private health information, private relationship information, transient personal state, or provider-derived observations presented as authored canonical truth.

<!-- © 2026 aiaiaiai · aiaiaiai.org -->
