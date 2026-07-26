# 0x0sky / mind

> A versioned public context graph for a person, their engineering practice, systems, organizations, and writing.

## Purpose

This repository is the canonical public `mind` for **0x0sky**. It is designed to be read by humans, AI systems, and `mind-web` without binding the context to one vendor or application.

The repository contains durable public context only. It is not a conversation archive, a private journal, or a credentials store.

## Graph

```text
0x0sky
├── aiaiaiai
├── 0xda-market
├── identity
├── knowledge
├── engineering
│   └── systems
└── writing
```

Folders and declared organizations are graph nodes. Markdown files inside a folder are documents attached to that node and appear as tabs in `mind-web`. Dependencies declared in each `module.yaml` become directed graph edges.

## Modules

- [`identity`](identity/README.md) — canonical public identity and handles;
- [`knowledge`](knowledge/README.md) — durable models and principles;
- [`engineering`](engineering/README.md) — software practice and engineering contract;
- [`systems`](systems/README.md) — public ecosystem, organizations, domains, and system boundaries;
- [`writing`](writing/README.md) — public creative practice and language register.

The machine-readable registry lives in [`manifest.yaml`](manifest.yaml). Its `organizations` collection is the canonical source for public organization nodes consumed by `mind-web`.

## Repository nodes

`mind-web` also represents every other public repository owned by `0x0sky` as a peer node. Those repository nodes expose only their public metadata and README; their internal files are not part of this mind.

## Privacy boundary

Never commit:

- secrets, credentials, tokens, or private infrastructure access;
- private health or relationship information;
- transient emotional or operational state;
- duplicated content whose canonical source lives elsewhere.

References are preferred over copies.

## Contract

Every module has:

- a stable `id`;
- one `purpose`;
- a `stability` class;
- explicit `dependencies`;
- canonical Markdown `entrypoints`;
- an `owner`;
- a `visibility` declaration.

The base schema remains in [`schema/mind.schema.json`](schema/mind.schema.json), and the reusable module rules remain in [`modules/README.md`](modules/README.md).
