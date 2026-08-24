# Mind Protocol 0.4

Status: **`0.4.0-rc.1` prerelease candidate**

Mind Protocol `0.4` is a consolidation release. Its purpose is to preserve the useful contracts that evolved after the original `baseline-v0.1.0`, make them explicit enough for a new human or AI consumer to read deterministically, and create a safe migration path toward `1.0`.

The release candidate deliberately changes the manifest shape before `1.0` while retaining the fields used by current consumers.

## Entry point

A consumer starts at `manifest.yaml`.

From that file it can determine, without repository-specific assumptions:

1. which manifest schema it is reading;
2. which Mind Protocol version the repository implements;
3. which subject the mind describes;
4. which entity owns or publishes the repository;
5. which concrete context version is published;
6. which modules exist and which are required;
7. where each module descriptor lives;
8. which modules load by default or only on request;
9. which validation schemas apply;
10. which repository-wide visibility and privacy guarantees apply.

A consumer should not need README history, chat context, or `mind-web` implementation details to discover those contracts.

## Version model

Mind uses three independent versions.

| Version | Example | Meaning |
| --- | --- | --- |
| Manifest schema | `2` | Shape of `manifest.yaml`. Increment when the machine contract changes incompatibly. |
| Protocol | `0.4.0-rc.1` | Semantics and behavior shared by compatible minds and consumers. |
| Context | `0.3.8` | Published durable content of one concrete mind instance. |

A protocol release may use the same manifest schema across several protocol versions. A mind may update its own context without changing protocol or schema versions.

Consumers must not infer one version from another.

## Subject and publication owner

`mind.subject` identifies the entity the mind describes and is authoritative about.

`mind.owner` identifies the entity accountable for owning or publishing the repository.

They are intentionally separate.

For a personal mind:

```yaml
mind:
  kind: personal
  subject:
    type: person
    id: alice
  owner:
    type: person
    id: alice
```

For an organization mind, subject and owner will normally also match.

For an AI agent:

```yaml
mind:
  kind: agent
  subject:
    type: agent
    id: magi
  owner:
    type: organization
    id: example-org
```

This allows an artificial identity to have a first-class mind without claiming that the AI owns a GitHub account or is biologically human.

`mind.kind` remains in `0.4` as a compatibility classification for existing consumers. The manifest validator requires it to agree with `mind.subject.type`. Consumers should begin treating `mind.subject` as the semantic source of truth.

## Required identity module

Every concrete mind requires the `identity` module.

The manifest identifies the subject at protocol level. The identity module owns richer subject context.

In the reference implementation the module exposes a typed resource:

```yaml
module:
  resources:
    identity:
      path: identity/identity.yaml
      format: yaml
      schema: schema/identity.schema.json
```

Mind CI verifies that the resource's `identity.type` and `identity.id` match `manifest.yaml -> mind.subject`.

This prevents a fork from accidentally retaining the upstream identity while publishing a different manifest subject.

## Module contract

`0.4` makes module descriptors part of the validated protocol surface.

Every registered `module.yaml` is checked against `schema/module.schema.json`. CI also verifies:

- descriptor id matches the manifest catalog key;
- dependencies resolve to registered modules;
- self-dependencies are forbidden;
- dependency cycles are forbidden;
- entrypoints exist and stay inside the repository;
- declared machine resources and schemas exist;
- machine resources validate against their declared JSON Schema.

The root manifest therefore remains a composition contract rather than accumulating domain-specific fields.

## Visual identity foundation

Visual identity belongs to the identity module, not to the root manifest and not automatically to a `brand` object.

`0.4` defines only one canonical visual concept:

```yaml
identity:
  visual_identity:
    primary_mark:
      kind: logo
      asset:
        path: identity/assets/mark.svg
        media_type: image/svg+xml
      alt: Example
```

Supported initial mark kinds are:

- `logo`;
- `emblem`;
- `monogram`;
- `glyph`;
- `signature`.

This vocabulary is intentionally identity-type-neutral.

An organization can use `logo`; a person can use `emblem`, `monogram`, or `signature`; an AI agent can use `emblem` or `glyph`. A consumer reads the same contract in every case.

A canonical mark references a repository-local, versioned asset. Provider avatars are derived presentation data unless the mind explicitly adopts an asset as canonical.

`0.4` does not yet standardize avatar slots, portraits, responsive mark variants, palettes, typography, or full brand systems.

## Compatibility strategy

`0.4.0-rc.1` keeps the existing `mind.name`, `mind.kind`, `mind.context_version`, `mind.owner`, `public_organizations`, `modules`, and `loading` structures used by the current `mind-web` parser while adding new fields around them.

This is deliberate: the reference consumer can continue reading the existing projection fields while it gains support for `protocol`, `subject`, typed resources, and visual identity.

The manifest schema itself increments from `1` to `2` because a standards-aware consumer must be able to detect that the formal shape changed. Compatibility is explicit, not hidden behind an unchanged schema number.

## Migration from the 0.3 line

A concrete `0.3.x` mind moves to `0.4.0-rc.1` by:

1. changing `schema_version` from `1` to `2`;
2. adding `protocol.id: mind` and `protocol.version: 0.4.0-rc.1`;
3. adding `mind.subject`;
4. retaining `mind.kind` and `mind.owner`;
5. adding `contract.explicit_subject: required`;
6. declaring `validation.module_schema`;
7. ensuring `identity` is required for every concrete mind;
8. validating every module descriptor;
9. optionally adding a typed identity resource;
10. bumping the concrete mind's `context_version` only when its published context actually changes.

The `0x0sky` reference mind moves from context `0.3.7` to `0.3.8` because it adds a canonical machine-readable identity resource and protocol metadata.

## Gate for stable 0.4.0

`0.4.0` should not be published as stable merely because this reference repository passes CI.

The stable gate is:

- reference personal mind validates on schema v2;
- at least one organization mind migrates successfully;
- the current `mind-web` consumer reads both pre-0.4 and 0.4 minds correctly during migration;
- subject/owner semantics are exercised with a non-trivial ownership case;
- identity resources validate deterministically;
- visual `primary_mark` is exercised with at least one real canonical asset;
- migration documentation contains no unresolved breaking ambiguity.

Until those conditions hold, `0.4.0-rc.*` is the correct release channel.
