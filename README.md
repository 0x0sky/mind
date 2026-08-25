# mind@0x0sky

Canonical public Mind for `person:0x0sky`.

This repository is a **standalone concrete Mind Protocol consumer**. It does not define Mind Protocol and must never be used as a template authority for another person, organization, agent, project, or product.

## Authority

- `manifest.yaml` — canonical publication boundary for `mind@0x0sky`;
- `modules/identity/identity.yaml` — canonical machine-readable person Identity;
- registered modules — durable authored public context for this subject;
- `protocol.lock.yaml` — exact immutable Mind Protocol release consumed by this repository.

The canonical protocol authority is `aiaiaiai-org/mind-protocol`. The vendored `protocol.yaml`, `conformance.yaml`, `compatibility.yaml`, and `schema/` are immutable release contracts, not locally authored protocol authority.

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

Current binding: **Mind Protocol `1.0.0-rc.2`**.

Exact release provenance:

- **authority/release repository:** `aiaiaiai-org/mind-protocol`;
- **tag:** `v1.0.0-rc.2`;
- **commit:** `acdcedcf02c8b4ef314179bf54955a84606c8fb5`.

The historical first formal `v0.9.0` release remains immutable in this repository because it predates the physical authority split. It is history, not the current protocol source.

`mind.context_version` is independent and remains `0.4.0`. This RC synchronization changes only the consumed protocol release; no durable personal context or canonical Identity is changed.

Protocol-version tags do not belong in this concrete repository beyond the immutable historical `v0.9.0` that predates the split.

## Repository relationship

This concrete Mind is an **independent protocol consumer**, not a fork of `mind-protocol`. Protocol compatibility is expressed through the exact release lock and vendored release contracts, not GitHub fork ancestry.

## Privacy boundary

Never commit credentials, secrets, private health information, private relationship information, transient personal state, or provider-derived observations presented as authored canonical truth.

<!-- © 2026 aiaiaiai · aiaiaiai.org -->
