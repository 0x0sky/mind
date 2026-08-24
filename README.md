# 0x0sky / mind

> A GitHub-native protocol for versioned self-definition.

This repository serves two roles:

1. it is the canonical public `mind` of **0x0sky**;
2. it is the reference implementation of the `mind` protocol.

A mind is a versioned, inspectable, and forkable repository through which a person, organization, agent, project, or product can declare identity, context, relationships, boundaries, and meaning. It is designed to be read by humans, AI systems, and compatible renderers without binding its contents to one vendor or application.

The current reference implementation targets **Mind Protocol `0.4.0-rc.1`**. The `0.4` line introduces explicit protocol identity, separates the represented subject from repository publication authority, validates module descriptors and machine-readable module resources, and establishes the first provider-independent visual-identity contract.

## Model

| Layer | Responsibility |
| --- | --- |
| `mind` protocol | The shared GitHub-native protocol and repository contract. |
| Protocol version | Semantic version of the behavior and meaning consumers implement. |
| Manifest schema version | Version of the machine-readable `manifest.yaml` shape. |
| Context version | Version of one concrete mind's published context. |
| A mind repository | A concrete, sovereign instance describing one subject. |
| `0x0sky/mind` | The canonical mind of `0x0sky` and the protocol's reference implementation. |
| `mind-web` | A separate spatial consumer for compatible mind repositories. |

These versions are intentionally independent. For example, this repository can use protocol `0.4.0-rc.1`, manifest schema `2`, and context version `0.3.8` at the same time.

Git provides history and change; GitHub provides ownership, discovery, collaboration, and forking; the repository provides the subject's declared truth.

## Canonicality and sovereignty

Every concrete mind has one `subject`, declared by its manifest.

The manifest also declares an `owner`: the entity accountable for owning or publishing the repository. For personal and organization minds the subject and owner will normally be the same entity. They may differ for agent, project, or product minds. This distinction allows an AI identity, for example, to be the subject of a mind published by a person or organization without pretending the AI owns the hosting account.

A fork owned by another person or organization is intended to become that subject's independent canonical mind. The fork must replace inherited identity and ownership declarations with its own; upstream supplies protocol lineage and structure, not identity or content.

Each mind is authoritative only about the subject it represents:

- `0x0sky/mind` is the source of truth for `0x0sky`;
- an organization's own canonical mind is the source of truth for that organization;
- an agent mind is authoritative about the declared agent identity only within the authority granted by its publisher;
- a reference to another subject is a declaration from the current mind's perspective;
- a relationship becomes mutually confirmed only when both canonical minds declare it.

Forks may continue to inherit protocol improvements while remaining sovereign over their own context.

## This mind

The current instance describes the durable public context of `0x0sky`:

```text
0x0sky
├── identity
├── knowledge
├── engineering
├── systems
├── writing
└── declared organizations
    ├── aiaiaiai tech.
    ├── 0xda-market
    └── nilx.one
```

The modules are:

- [`identity`](identity/README.md) — canonical public identity, machine-readable subject metadata, handles, and optional visual identity;
- [`knowledge`](knowledge/README.md) — durable models and principles;
- [`engineering`](engineering/README.md) — software practice and engineering contract;
- [`systems`](systems/README.md) — public ecosystem, declared organizations, and system boundaries;
- [`writing`](writing/README.md) — public creative practice and language register.

Declarations about organizations record `0x0sky`'s relationships to them. They do not replace those organizations' own canonical minds.

## Repository contract

The machine-readable entry point is [`manifest.yaml`](manifest.yaml). It declares:

- the manifest schema version;
- the Mind Protocol version;
- the represented subject;
- the repository publication owner;
- the concrete context version;
- public organization relations and their provenance semantics;
- registered modules and loading policy;
- repository privacy boundaries;
- validation schemas.

Every registered module has:

- a stable `id`;
- one `purpose`;
- a `stability` class;
- explicit `dependencies`;
- canonical `entrypoints`;
- an `owner`;
- a `visibility` declaration;
- optional typed machine-readable `resources`.

The manifest schema lives in [`schema/mind.schema.json`](schema/mind.schema.json), the reusable module descriptor schema in [`schema/module.schema.json`](schema/module.schema.json), and the first typed module resource schema in [`schema/identity.schema.json`](schema/identity.schema.json).

The identity module is required for every concrete mind. Its machine-readable resource must resolve to the same subject declared by `manifest.yaml`.

The protocol design and `0.4` migration rules are documented in [`docs/protocol/README.md`](docs/protocol/README.md). The staged path to `1.0` is tracked in [`docs/protocol/ROADMAP.md`](docs/protocol/ROADMAP.md).

The repository contains durable public context only. It is not a conversation archive, private journal, credentials store, or substitute for documentation canonically owned by another repository.

## Visual identity

Mind Protocol `0.4` introduces an optional `identity.visual_identity.primary_mark` contract.

`primary_mark` is the canonical mark of an identity, not a synonym for `brand` or `avatar`. Its `kind` can currently be:

- `logo` — typically an organization or product mark;
- `emblem` — a general identity symbol suitable for people, organizations, or agents;
- `monogram`;
- `glyph`;
- `signature`.

The mark references a repository-local versioned asset. Provider avatars may still be used by renderers as derived presentation data when no canonical mark exists, but they do not become canonical mind content merely because a provider exposes them.

The `0.4` schema intentionally stops at `primary_mark`. Avatar, portrait, responsive variants, palette, typography, and full brand systems remain later protocol work so the first contract stays small and stable.

## Projection through mind-web

[`mind-web`](https://github.com/aiaiaiai-tech/mind-web) reads compatible minds and projects them as a spatial, living graph.

Folders and declared organizations may become graph nodes. Markdown entrypoints may become readable node documents, and dependencies declared by each `module.yaml` may become directed edges.

A renderer may enrich the projection with public GitHub metadata, including repositories owned by the subject. Derived or enriched nodes are visualization data; they are not canonical mind content unless the mind explicitly declares them.

`mind-web` is a consumer, not the source of truth. It may live beside a mind or be deployed independently, and its hosting domain does not change the identity or authority of the mind it renders.

## Boundaries

The `mind` protocol is independent of `0x1`, Bond, BondChain, and the domain infrastructure of `nilx.one`. Those are separate systems and gain no protocol meaning merely by being linked, hosted, or visualized nearby.

External products and protocols remain owned by their own repositories. They do not become organization routes, memberships, or canonical mind content unless explicitly declared in `manifest.yaml`.

## Privacy boundary

Never commit:

- secrets, credentials, tokens, or private infrastructure access;
- private health or relationship information;
- transient emotional or operational state;
- duplicated content whose canonical source lives elsewhere.

References are preferred over copies.
