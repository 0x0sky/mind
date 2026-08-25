# Identity

Canonical public person identity for `0x0sky`.

## Canonical identity

- **type:** person
- **id:** `0x0sky`
- **display name:** `0x0sky`
- **GitHub namespace:** `github.com/0x0sky`

The machine-readable source is [`identity.yaml`](identity.yaml). Its type and id must match `manifest.yaml -> mind.subject` exactly.

The canonical Identity is provider-independent. `0x0sky` is also the current GitHub login, but provider account state is discovery/integration context rather than the definition of Identity.

Visual identity belongs to this module only when canonical assets are explicitly versioned and referenced through the protocol visual contract. A provider avatar is derived presentation data until explicitly adopted as canonical.

## Handles

[`handles.md`](handles.md) records durable public naming and discovery context. Handles never replace the stable canonical `identity.id`.

## Scope

- canonical person id and display name;
- durable public naming and discovery identifiers;
- canonical visual identity resources when explicitly authored and versioned here.

## Exclusions

Do not store credentials, private profile data, private health or relationship information, transient account state, provider-derived observations as canonical facts, or runtime/assistant identity in this module.

`0xda` is a working-environment identity and remains separate from `person:0x0sky`.

## Dependencies

None.

<!-- © 2026 aiaiaiai · aiaiaiai.org -->
