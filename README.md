# mind / mind@0x0sky

> An implementation-independent protocol for versioned identity and context, plus the canonical living mind of `0x0sky`.

This repository deliberately contains two different things without conflating their authority:

1. **Mind Protocol** — neutral contracts that must not depend on `0x0sky`, GitHub, a renderer, repository layout, or a runtime implementation;
2. **`mind@0x0sky`** — one concrete sovereign mind instance implementing those contracts.

## Two entry points

| Entry point | Authority | Version axis |
| --- | --- | --- |
| [`protocol.yaml`](protocol.yaml) | canonical implementation-independent Mind Protocol contracts | `protocol.version` |
| [`manifest.yaml`](manifest.yaml) | canonical concrete `mind@0x0sky` instance | `mind.context_version` |

The `master` branch is the living canonical branch of **`mind@0x0sky`**. It is not a neutral identity template.

The current development candidate is **Mind Protocol `0.7.0-rc.1`**, built on the stable `0.6.0` Identity/visual contract. Manifest schema remains `2`, while the concrete instance context remains independently versioned.

## Canonical Identity

[`schema/identity.schema.json`](schema/identity.schema.json) is the canonical **Identity value**. It defines semantic identity only:

- identity `type`;
- stable provider-independent `id`;
- canonical `display_name`;
- optional visual identity through semantic mark metadata and an opaque `asset_ref`.

It does **not** define provider ids, repository paths, URLs, validation-file locations, storage layout, runtime state, model configuration, prompts, memory, or renderer handles.

A concrete mind carries that value through [`schema/identity-resource.schema.json`](schema/identity-resource.schema.json).

## Agent identity

`0.7.0-rc.1` proves that `agent` is a first-class value of the same universal Identity contract used by people and organizations; there is no separate AI-specific Identity schema.

The synthetic agent fixture proves that an agent subject may have a distinct publication owner and requires no provider account or AI runtime. Model, prompt, memory, runtime, execution state, and biological-personhood assertions remain outside universal Identity.

A canonical agent mark may still be an emblem or glyph under the existing visual-identity contract. A generated or synthetic portrait is presentation data by default and is not promoted into canonical Identity merely because the subject is an agent.

See [`docs/protocol/AGENT_IDENTITY.md`](docs/protocol/AGENT_IDENTITY.md).

## Canonical visual assets

Mind Protocol `0.6.0` defines [`schema/visual-assets.schema.json`](schema/visual-assets.schema.json), a concrete publication contract for resolving opaque canonical `asset_ref` values.

The protocol keeps byte locations and integrity outside universal Identity:

```text
Identity.primary_mark.asset_ref       semantic opaque reference
                │
                ▼
typed visual-assets resource          concrete publication descriptor
                │
                ├── media type
                ├── publication-relative resource path
                └── SHA-256 integrity
```

Resolution and failure semantics are specified in [`docs/protocol/VISUAL_IDENTITY.md`](docs/protocol/VISUAL_IDENTITY.md). Provider avatars and generated portraits remain noncanonical presentation/evidence and cannot silently replace an authored canonical mark.

## Instance model

Every concrete mind declares one `subject` and one publication `owner`. The canonical instance naming convention is:

```text
mind@{subject.id}
```

The instance is authoritative only about its subject. Relationships involving other entities remain claims from this subject's perspective until independently confirmed by the counterpart canonical mind.

## Modules

```text
mind@0x0sky
├── identity
├── relationships
├── knowledge
├── engineering
├── systems
└── writing
```

The root manifest remains a composition contract rather than a graph database.

## Schemas

- [`schema/protocol.schema.json`](schema/protocol.schema.json) — neutral protocol descriptor;
- [`schema/mind.schema.json`](schema/mind.schema.json) — concrete mind manifest;
- [`schema/module.schema.json`](schema/module.schema.json) — module descriptors;
- [`schema/identity.schema.json`](schema/identity.schema.json) — universal Identity value;
- [`schema/identity-resource.schema.json`](schema/identity-resource.schema.json) — concrete identity-resource envelope;
- [`schema/relationships.schema.json`](schema/relationships.schema.json) — authored relationships;
- [`schema/visual-assets.schema.json`](schema/visual-assets.schema.json) — canonical visual-asset catalog.

## Versioning

The axes are intentionally independent:

- `protocol.version` changes when shared Mind semantics change;
- manifest `schema_version` changes only when root manifest machine shape changes;
- `mind.context_version` changes when durable context of one concrete mind changes;
- resource/schema versions evolve with their own machine contracts.

Merging protocol source changes is not a published release. Tags and GitHub Releases are separate actions.

## mind-web

[`mind-web`](https://github.com/aiaiaiai-org/mind-web) is a consumer, never protocol authority. It may combine authored facts with provider-derived evidence only when provenance remains distinguishable.

## Privacy boundary

Never commit secrets, credentials, private health or relationship information, transient personal state, or provider-derived observations presented as authored canonical truth. References are preferred over copies.
