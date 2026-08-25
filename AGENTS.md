# AGENTS

This repository is the concrete public Mind for `person:0x0sky`. It is a **Mind Protocol consumer**, not protocol authority.

## Read order

1. Read `mind-repository.yaml` to confirm repository role.
2. Read `manifest.yaml` for subject, owner, registered modules, loading order, visibility, and validation boundaries.
3. Load only the registered modules relevant to the task.
4. Treat vendored protocol contracts as immutable release inputs locked by `protocol.lock.yaml`.

## Protocol boundary

Canonical Mind Protocol source and releases live in `aiaiaiai-org/mind-protocol`.

Do not modify vendored `protocol.yaml`, `conformance.yaml`, `compatibility.yaml`, or `schema/` as if this repository defined the protocol. Protocol changes belong in the protocol repository and arrive here only through an explicit exact-release sync.

Never consume floating `master` as protocol authority. Never create protocol-version tags in this concrete repository.

## Identity boundary

`modules/identity/identity.yaml` is canonical only for `person:0x0sky`.

Provider logins, handles, repository ownership, avatars, runtime identities, organizations, projects, products, and agents are distinct concepts and must not silently redefine the canonical person Identity.

## Environment identity

Operate as **0xda**, the current personal working environment in which `0x0sky` collaborates with the assistant.

`0xda` is not a vendor alias and is not the subject of this Mind. Keep environment identity separate from the canonical person Identity and from organization/product/project/agent identities.

## Loading and module rules

- Follow `manifest.yaml`; folder placement alone does not define authority.
- Respect each module's declared responsibility and dependencies.
- Prefer cross-references over duplicated facts.
- Keep public content durable and intentionally authored.
- Load archived or optional context only when relevant.
- Do not infer canonical facts from provider metadata.

## Engineering workflow

1. Inspect current state.
2. Make the smallest correct change.
3. Keep docs and machine contracts synchronized.
4. Use a feature/fix branch, then Draft PR.
5. Run full relevant CI and require green before merge.
6. Reuse verified results rather than duplicating checks.
7. Merge only under explicit project authorization; release/deploy/publication remain separate actions.

## Safety

Never add secrets, credentials, access tokens, private keys, private health or relationship information, or transient personal state.

Preserve provider independence and distinguish authored fact, inference, and external observation.

<!-- © 2026 aiaiaiai · aiaiaiai.org -->
