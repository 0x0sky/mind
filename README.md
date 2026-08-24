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

Neutral protocol truth is carried by `protocol.yaml`, protocol schemas, and protocol documentation on the same commit. A protocol release tag therefore identifies a released contract without pretending the concrete instance on that commit is generic.

The current development line targets **Mind Protocol `0.6.0-rc.1`**, manifest schema `2`, and `mind@0x0sky` context `0.4.0`.

## Canonical Identity

[`schema/identity.schema.json`](schema/identity.schema.json) is the canonical **Identity value**. It is intentionally independent from any concrete mind resource envelope or storage implementation.

It defines semantic identity only:

- identity `type`;
- stable provider-independent `id`;
- canonical `display_name`;
- optional visual identity expressed through semantic mark metadata and an opaque `asset_ref`.

It does **not** define GitHub ids, repository paths, URLs, validation-file locations, storage layout, runtime state, or provider bindings.

A concrete mind carries that value through an implementation envelope. For `mind@0x0sky`, [`identity/identity.yaml`](identity/identity.yaml) uses [`schema/identity-resource.schema.json`](schema/identity-resource.schema.json), while the embedded `identity` value is independently validated against the universal Identity contract.

```text
Mind Protocol
└── Identity                         universal value

mind@0x0sky                          concrete instance on master
├── manifest.yaml
└── identity/identity.yaml
    └── identity                     implements universal Identity
```

## Instance model

Every concrete mind declares one `subject` and one publication `owner`. The conventional canonical instance name is:

```text
mind@{subject.id}
```

For this repository that is `mind@0x0sky`.

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

- [`identity`](identity/README.md) — concrete implementation of the universal Identity contract;
- [`relationships`](relationships/README.md) — authored entity relations, direction, provenance, and confirmation;
- [`knowledge`](knowledge/README.md) — durable models and principles;
- [`engineering`](engineering/README.md) — software practice and engineering contract;
- [`systems`](systems/README.md) — software-ecosystem structure and system boundaries;
- [`writing`](writing/README.md) — public creative practice and language register.

## Relationships

The canonical authored relationship source for this instance is [`relationships/relationships.yaml`](relationships/relationships.yaml). Provider-discovered memberships remain integration evidence and never become authored protocol truth automatically.

The canonical organization endpoint is `organization:aiaiaiai`; the current GitHub provider namespace is `aiaiaiai-org`. The GitHub-specific root `public_organizations` field remains temporarily as a legacy compatibility projection and therefore stores provider logins, not canonical entity ids.

## Schemas

- [`schema/protocol.schema.json`](schema/protocol.schema.json) — neutral protocol descriptor;
- [`schema/mind.schema.json`](schema/mind.schema.json) — concrete mind manifest;
- [`schema/module.schema.json`](schema/module.schema.json) — module descriptors;
- [`schema/identity.schema.json`](schema/identity.schema.json) — universal Identity value;
- [`schema/identity-resource.schema.json`](schema/identity-resource.schema.json) — concrete mind identity-resource envelope;
- [`schema/relationships.schema.json`](schema/relationships.schema.json) — authored relationships.

## Versioning

The version axes are intentionally independent:

- `protocol.version` changes when shared Mind semantics change;
- manifest `schema_version` changes only when the root manifest shape changes incompatibly;
- `mind.context_version` changes when the durable context of one concrete mind changes;
- resource/schema versions evolve with their own machine contracts.

A change to `mind@0x0sky` does not imply a protocol release. A protocol release does not imply that another identity's mind context changed.

## mind-web

[`mind-web`](https://github.com/aiaiaiai-org/mind-web) is a consumer, never protocol authority. It may combine authored facts with provider-derived evidence only when provenance remains distinguishable.

## Privacy boundary

Never commit secrets, credentials, private health or relationship information, transient personal state, or provider-derived observations presented as authored canonical truth. References are preferred over copies.
