# 0x0sky / mind

> A GitHub-native protocol for versioned self-definition.

This repository is both the canonical public `mind` of **0x0sky** and the reference implementation of Mind Protocol.

A mind is a versioned, inspectable, and forkable repository through which a person, organization, agent, project, or product can declare identity, context, relationships, boundaries, and meaning without binding that truth to one vendor or application.

The current reference implementation targets **Mind Protocol `0.5.0-rc.1`**, manifest schema `2`, and context `0.3.11`.

## Model

Every concrete mind declares one `subject` and one publication `owner`. A mind is authoritative only about its subject; relationship claims are canonical only when that subject is one endpoint.

A relationship becomes reciprocal only when the counterpart canonical mind independently publishes a matching claim. Provider discovery may supply evidence, but it is not authorship.

## Modules

```text
0x0sky
├── identity
├── relationships
├── knowledge
├── engineering
├── systems
└── writing
```

- [`identity`](identity/README.md) — canonical public identity and typed subject metadata;
- [`relationships`](relationships/README.md) — authored entity relations, direction, provenance, and confirmation;
- [`knowledge`](knowledge/README.md) — durable models and principles;
- [`engineering`](engineering/README.md) — software practice and engineering contract;
- [`systems`](systems/README.md) — software-ecosystem structure and system boundaries;
- [`writing`](writing/README.md) — public creative practice and language register.

## Relationships

The canonical relationship source is [`relationships/relationships.yaml`](relationships/relationships.yaml). The reference mind currently authors `member_of` relationships from `person:0x0sky` to `organization:aiaiaiai`, `organization:0xda-market`, and `organization:nilx-one`.

The canonical organization id `aiaiaiai` is provider-independent. The legacy `public_organizations` projection uses the current GitHub namespace `aiaiaiai-org` because that field remains provider-specific during the 0.5 migration.

Provider-discovered GitHub memberships remain derived integration evidence. The root `public_organizations` field remains temporarily as a legacy projection, and every populated legacy entry in a mind adopting the relationships module must be backed by a canonical authored membership.

## Repository contract

[`manifest.yaml`](manifest.yaml) is the machine-readable entry point. Protocol schemas include:

- [`schema/mind.schema.json`](schema/mind.schema.json) — root manifest;
- [`schema/module.schema.json`](schema/module.schema.json) — module descriptors;
- [`schema/identity.schema.json`](schema/identity.schema.json) — canonical identity resource;
- [`schema/relationships.schema.json`](schema/relationships.schema.json) — canonical authored relationships.

The root manifest remains a composition contract; it does not become a graph database.

Protocol documentation lives in [`docs/protocol/README.md`](docs/protocol/README.md), relationship semantics in [`docs/protocol/RELATIONSHIPS.md`](docs/protocol/RELATIONSHIPS.md), and the staged path to `1.0` in [`docs/protocol/ROADMAP.md`](docs/protocol/ROADMAP.md).

## Visual identity

The optional `identity.visual_identity.primary_mark` contract introduced by `0.4` is unchanged in `0.5`. Real personal and organization assets, renderer fallback, and avatar semantics remain the `0.6` milestone.

## mind-web

[`mind-web`](https://github.com/aiaiaiai-org/mind-web) is a consumer, not protocol authority. It may combine authored relationships with provider-derived evidence, but it must preserve provenance and must never promote derived observations into canonical authorship or reciprocal confirmation.

## Privacy boundary

Never commit secrets, credentials, private health or relationship information, transient personal state, or provider-derived observations presented as authored canonical truth. References are preferred over copies.
