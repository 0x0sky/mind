# 0x0sky / mind

> A GitHub-native protocol for versioned self-definition.

This repository serves two roles:

1. it is the canonical public `mind` of **0x0sky**;
2. it is the reference implementation of the `mind` protocol.

A mind is a versioned, inspectable, and forkable repository through which a person or organization declares its identity, context, relationships, boundaries, and meaning. It is designed to be read by humans, AI systems, and compatible renderers without binding its contents to one vendor or application.

## Model

| Layer | Responsibility |
| --- | --- |
| `mind` | The shared GitHub-native protocol and repository contract. |
| A mind repository | A concrete, sovereign instance describing one person or organization. |
| `0x0sky/mind` | The canonical mind of `0x0sky` and the protocol's reference implementation. |
| `mind-web` | A separate spatial renderer for compatible mind repositories. |

Git provides history and change; GitHub provides ownership, discovery, collaboration, and forking; the repository provides the subject's declared truth.

## Canonicality and sovereignty

Every mind has one subject, declared by its manifest and controlled by that subject's GitHub identity.

A fork owned by another person or organization is intended to become that subject's independent canonical mind. The fork must replace inherited identity and ownership declarations with its own; upstream supplies protocol lineage and structure, not identity or content.

Each mind is authoritative only about the subject it represents:

- `0x0sky/mind` is the source of truth for `0x0sky`;
- an organization's own canonical mind is the source of truth for that organization;
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
    ├── aiaiaiai
    └── 0xda-market
```

The modules are:

- [`identity`](identity/README.md) — canonical public identity and handles;
- [`knowledge`](knowledge/README.md) — durable models and principles;
- [`engineering`](engineering/README.md) — software practice and engineering contract;
- [`systems`](systems/README.md) — public ecosystem, declared organizations, and system boundaries;
- [`writing`](writing/README.md) — public creative practice and language register.

Declarations about organizations record `0x0sky`'s relationships to them. They do not replace those organizations' own canonical minds.

## Repository contract

The machine-readable entry point is [`manifest.yaml`](manifest.yaml). It declares the subject, owner, context version, organizations, memberships, modules, loading order, privacy boundary, and validation schema.

Every registered module has:

- a stable `id`;
- one `purpose`;
- a `stability` class;
- explicit `dependencies`;
- canonical Markdown `entrypoints`;
- an `owner`;
- a `visibility` declaration.

The base schema lives in [`schema/mind.schema.json`](schema/mind.schema.json), and reusable module rules live in [`modules/README.md`](modules/README.md). Concrete minds may use different folders and modules when their manifest declares them explicitly.

The repository contains durable public context only. It is not a conversation archive, private journal, credentials store, or substitute for documentation canonically owned by another repository.

## Projection through mind-web

[`mind-web`](https://github.com/0x0sky/mind-web) reads a compatible mind and projects it as a spatial, living graph.

Folders and declared organizations may become graph nodes. Markdown entrypoints may become readable node documents, and dependencies declared by each `module.yaml` may become directed edges.

A renderer may enrich the projection with public GitHub metadata, including repositories owned by the subject. Derived or enriched nodes are visualization data; they are not canonical mind content unless this repository declares them.

`mind-web` is a consumer, not the source of truth. It may live beside a mind or be deployed independently, and its hosting domain does not change the identity or authority of the mind it renders.

## Boundaries

The `mind` protocol is independent of `0x1`, `Bond`, `BondChain`, and the domain infrastructure of `nilx.one`. Those are separate systems and gain no protocol meaning merely by being linked, hosted, or visualized nearby.

External products and protocols remain owned by their own repositories. They do not become organization routes, memberships, or canonical mind content unless explicitly declared in `manifest.yaml`.

## Privacy boundary

Never commit:

- secrets, credentials, tokens, or private infrastructure access;
- private health or relationship information;
- transient emotional or operational state;
- duplicated content whose canonical source lives elsewhere.

References are preferred over copies.
