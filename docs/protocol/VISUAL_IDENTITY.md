# Canonical visual identity

Mind Protocol `0.6.0-rc.2` defines how an opaque universal Identity `asset_ref` resolves to a concrete canonical visual asset without making repository layout, provider URLs, storage backends, or renderer handles part of Identity.

The machine contracts are:

- [`../../schema/identity.schema.json`](../../schema/identity.schema.json) — universal Identity and `visual_identity.primary_mark`;
- [`../../schema/visual-assets.schema.json`](../../schema/visual-assets.schema.json) — concrete publication asset catalog;
- [`../../protocol.yaml`](../../protocol.yaml) — media, integrity, resolution, and fallback policy.

## Boundary

Universal Identity may say:

```yaml
visual_identity:
  primary_mark:
    kind: emblem
    asset_ref: primary-mark
    alt: Synthetic example
```

`asset_ref` is semantic and opaque. It is not a path, URL, provider avatar id, CDN key, texture handle, or content hash.

A concrete publication may separately expose a typed resource conforming to `schema/visual-assets.schema.json`:

```yaml
schema_version: 1
assets:
  - ref: primary-mark
    media_type: image/svg+xml
    resource_path: assets/primary.svg
    integrity:
      algorithm: sha256
      digest: 0123456789abcdef...
validation:
  schema: schema/visual-assets.schema.json
```

`resource_path` is packaging metadata relative to that publication root. It does not change the Identity value.

## Deterministic resolution

For a `primary_mark`:

1. discover registered typed resources whose schema is `schema/visual-assets.schema.json`;
2. select descriptors whose `ref` equals the opaque `asset_ref`;
3. require exactly one matching descriptor;
4. require the descriptor media type to be understood by the consumer;
5. resolve `resource_path` within the publication root;
6. verify the required SHA-256 digest before treating bytes as canonical.

The resolver has explicit outcomes:

| Outcome | Meaning |
| --- | --- |
| `unavailable` | Identity declares no canonical primary mark. |
| `missing` | A mark is declared but no usable asset exists at its resolved location. |
| `ambiguous` | More than one descriptor claims the same `asset_ref`. |
| `unsupported_media` | The descriptor uses a protocol-allowed optional media type the consumer does not implement, or an invalid type reaches the resolver. |
| `integrity_error` | Resolved bytes do not match the authored digest. |
| `resolved` | Exactly one supported, integrity-verified canonical asset resolved. |

Only `resolved` authorizes a consumer to present the bytes as the canonical mark.

## Integrity decision

`0.6.0-rc.2` uses a **versioned descriptor with a required SHA-256 digest**.

The digest is intentionally not the universal `asset_ref`. A semantic reference such as `primary-mark` may remain stable while the canonical asset receives an intentional revision. The publication descriptor carries the byte-level integrity commitment.

## Media policy

Consumers conforming to this RC must support:

- `image/svg+xml`;
- `image/png`.

`image/webp` is protocol-allowed but optional for consumers. A consumer that does not implement it returns `unsupported_media`; it must not reinterpret the asset as another type.

Adding new media types is a protocol-contract change.

## Fallback and provenance

Fallback is presentation behavior, not canonical identity mutation.

- when no mark is authored, a consumer may use a neutral presentation fallback;
- on missing or unsupported assets, a consumer may use a noncanonical presentation fallback while preserving the observable failure;
- on integrity failure, the canonical asset must be rejected;
- provider avatars, generated portraits, screenshots, or other derived visual evidence may be displayed as derived/presentation data, but must never silently replace the canonical mark or be relabeled as canonical.

## Avatar

For the `0.6` line, `avatar` is **presentation-only**. It is not a universal Identity slot and is not part of the canonical visual-asset contract.

A later protocol may promote a separately typed avatar capability only with protocol-wide evidence. That would be a new explicit contract, not an implicit reinterpretation of `primary_mark`.

## Conformance fixtures

`tests/fixtures/visual_identity/` contains synthetic person, organization, and agent identities with authored canonical marks. They deliberately contain no named real-world identity or provider dependency.

The fixture validator proves successful resolution and regression tests cover unavailable, missing, ambiguous, unsupported-media, and integrity-failure behavior.
