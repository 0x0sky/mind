# Assistant architecture

This directory defines shared agent behavior for `0x0sky/mind` and implements it in two concrete working environments.

The architecture does not begin with a vendor or a model-specific prompt. It begins with a neutral contract, then applies that contract inside an environment with its own identity, runtime assumptions, and native instruction path.

## Implemented environments

Only two environments are implemented:

1. **`0xda`** — the current personal working environment in which `0x0sky` collaborates with the assistant. Its native repository entry point is [`AGENTS.md`](../AGENTS.md).
2. **GitHub Copilot** — the repository coding environment implemented through [`.github/copilot-instructions.md`](../.github/copilot-instructions.md).

No other environment is represented or implied.

## Structure

```text
.assistant/
├── contract/
│   └── agent.yaml
├── environments/
│   ├── 0xda.yaml
│   └── copilot.yaml
└── README.md

AGENTS.md
.github/copilot-instructions.md
```

## Separation of responsibilities

### `contract/`

Contains behavior that must remain stable across environments: guard principles, permissions, privacy rules, communication expectations, engineering workflow, and entity boundaries.

The contract does not define a vendor, model, prompt format, or personal identity. It describes what an agent operating in this repository is allowed and expected to do.

### `environments/`

Contains concrete implementations of the shared contract.

An environment may define:

- its identity and relationship to the owner;
- runtime-specific loading rules;
- supported roles and expression;
- the native instruction artifact it emits;
- boundaries that prevent context from leaking into another environment.

`0xda` is not a vendor alias or a portable persona. It is the identity of the current personal working environment where this collaboration occurs.

GitHub Copilot is a separate repository environment. It consumes the same contract but does not inherit the identity or transient context of `0xda`.

### Native artifacts

`AGENTS.md` and `.github/copilot-instructions.md` are environment-facing entry points. They are derived implementations, not independent policy sources.

## Resolution order

```text
repository contracts and manifest
        ↓
.assistant/contract/agent.yaml
        ↓
.assistant/environments/<environment>.yaml
        ↓
native instruction artifact
```

If a native artifact conflicts with the shared contract, the contract wins. An environment may change form, loading behavior, or expression, but it must not weaken authorization, privacy, or canonical-source boundaries.

## Adding another environment

A future environment should require only:

1. a new file under `.assistant/environments/`;
2. a native artifact at the path expected by that environment;
3. an update to this README.

The shared contract should remain unchanged unless the underlying behavior changes for every environment. This is the abstraction test: adding a runtime must not require rebuilding the system around that runtime.

## Entity boundary

`0xda` is associated with `0x0sky`, but organizations, products, and projects remain separate entities. Project-specific operating instructions belong in their own repositories and must not be copied into this personal environment.

## Privacy

This repository is public. Never add secrets, credentials, access tokens, private health or relationship information, or transient personal state.
