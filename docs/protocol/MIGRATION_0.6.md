# Migrating to Mind Protocol 0.6

Mind Protocol `0.6` stabilizes the boundary between universal Identity, a concrete mind publication, and canonical visual-asset packaging.

This guide covers migration from pre-`0.6` implementations and from the `0.6.0-rc.1` / `0.6.0-rc.2` candidates. It describes protocol migration only; named identities, real logos, provider bindings, and consumer rollout are separate implementation work.

## What changed

Before `0.6`, the identity schema could be interpreted as both the semantic Identity value and the repository resource that carried it. That made repository-local validation paths and asset locations easy to confuse with universal identity semantics.

`0.6` separates three layers:

```text
schema/identity.schema.json
└── universal Identity value

schema/identity-resource.schema.json
└── concrete publication envelope carrying Identity

schema/visual-assets.schema.json
└── concrete publication descriptors resolving opaque asset_ref values
```

The root manifest remains a composition contract. Provider bindings, runtime state, renderer state, and storage implementation remain outside universal Identity.

## Version axes

Do not derive one version from another.

- `protocol.version` identifies shared Mind semantics;
- manifest `schema_version` identifies the concrete manifest machine shape;
- `mind.context_version` identifies durable content of one concrete implementation;
- resource schema versions identify their individual machine contracts.

Adopting protocol `0.6.0` does not by itself require a concrete context-version bump. Bump context only when that concrete mind publishes a durable representational/content change.

## From pre-0.6 Identity resources

### 1. Extract universal Identity

Keep only semantic identity data in the value validated by `schema/identity.schema.json`:

```yaml
type: person | organization | agent | project | product
id: stable-provider-independent-id
display_name: Human readable name
```

Optional canonical visual identity may contain `visual_identity.primary_mark` with semantic mark kind, opaque `asset_ref`, and accessible `alt` text.

Remove repository paths, validation paths, provider handles/ids, avatar URLs, storage keys, content digests, runtime state, and renderer-specific values from universal Identity.

### 2. Carry Identity through the concrete envelope

A concrete publication may use:

```yaml
schema_version: 1
identity:
  type: person
  id: example
  display_name: Example
validation:
  schema: schema/identity-resource.schema.json
```

The embedded `identity.type` and `identity.id` must match the concrete manifest `mind.subject` exactly.

### 3. Preserve subject and publication owner separately

`mind.subject` is the identity described by the mind. `mind.owner` is the identity accountable for publishing it. They may be equal or intentionally different.

Do not infer either value from a provider account.

## Canonical visual assets

If an Identity does not author `visual_identity.primary_mark`, no asset catalog is required.

If it does, keep the `asset_ref` opaque and semantic. Do not replace it with a path or URL.

Resolve it through a typed resource conforming to `schema/visual-assets.schema.json`. Each descriptor carries:

- unique `ref` matching the authored `asset_ref`;
- media type;
- publication-root-relative resource path;
- required SHA-256 digest.

Consumers must support SVG and PNG for this protocol line. WebP is protocol-allowed but optional.

Only a uniquely matched, supported, integrity-verified asset is canonical. Missing, ambiguous, unsupported, or integrity-failed assets remain observable failures; a presentation fallback must not be relabeled canonical.

Provider avatars and generated portraits remain derived/presentation data. `avatar` is presentation-only in `0.6`.

## Relationships and provenance

The relationship/provenance semantics accepted in `0.5` carry forward unchanged:

- authored relationships remain distinguishable from provider-derived evidence;
- canonical entity ids remain provider-independent;
- reciprocal confirmation requires an independent counterpart claim;
- provider-facing compatibility projections do not redefine canonical identity.

## From 0.6.0-rc.1

In addition to the universal Identity / concrete envelope split introduced by RC1:

1. adopt protocol version `0.6.0`;
2. use the visual-assets catalog for any canonical `primary_mark.asset_ref`;
3. implement deterministic asset failure semantics;
4. keep provider-derived visuals noncanonical;
5. treat `avatar` as presentation-only.

No manifest schema bump is required solely for this migration.

## From 0.6.0-rc.2

`0.6.0` introduces no new semantic or machine-contract shape beyond RC2. Migration is therefore a protocol-version promotion after the RC2 contract and its conformance gates are satisfied.

A concrete implementation should keep its context version unchanged unless its own durable published representation changes independently.

## Validation checklist

A migrated implementation is ready when:

- the manifest declares the protocol version it actually implements;
- all published JSON Schemas are valid Draft 2020-12 schemas;
- the universal Identity validates independently of repository/provider/runtime state;
- embedded Identity `type/id` matches `mind.subject`;
- subject and publication owner remain explicit;
- authored and derived relationship provenance remains distinguishable;
- any canonical primary mark resolves deterministically with integrity verification;
- unsupported or broken visual assets fail observably rather than silently changing identity;
- protocol and concrete context versions remain independently meaningful.

## Publication boundary

Merging source changes that implement `0.6.0` does not create a Git tag or GitHub Release. Publication of a protocol release is a separate explicitly authorized action.
