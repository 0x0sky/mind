# Assistant architecture

This directory defines how `0x0sky/mind` expresses agent behavior without making any vendor-specific instruction file the source of truth.

Claude should read this file as the architectural explanation of the system. Claude is intentionally not given a native `CLAUDE.md` implementation in this iteration. Its role here is to understand, review, and reason about the architecture rather than become another independently maintained instruction target.

## The three participants

The current design intentionally supports only three participants:

1. **OpenAI / 0x0da** — implemented through the repository-root [`AGENTS.md`](../AGENTS.md).
2. **Claude** — represented by this explanatory README and used as an architectural reader or reviewer.
3. **GitHub Copilot** — implemented through [`.github/copilot-instructions.md`](../.github/copilot-instructions.md).

Gemini, Grok, and other speculative targets are deliberately excluded. A future vendor should be added only when there is a real runtime or workflow to support.

## Structure

```text
.assistant/
├── contract/
│   └── agent.yaml
├── personas/
│   └── 0x0da.yaml
├── adapters/
│   ├── openai.yaml
│   └── copilot.yaml
└── README.md

AGENTS.md
.github/copilot-instructions.md
```

## Separation of responsibilities

### `contract/`

Contains vendor-neutral behavior, permissions, privacy rules, communication expectations, and engineering constraints.

The contract does not describe OpenAI, Claude, Copilot, or a particular prompt format. It defines what an agent is allowed and expected to do.

### `personas/`

Contains identity-specific expression layered over the contract. `0x0da` is one persona, not the foundation of the architecture.

A persona may influence tone, role, and working style, but it must not redefine permissions, privacy, or canonical repository behavior.

### `adapters/`

Contains translation rules for a concrete runtime. An adapter consumes the neutral contract and an optional persona, then emits a native artifact.

Vendor-specific assumptions belong here and nowhere else.

### Native artifacts

`AGENTS.md` and `.github/copilot-instructions.md` are executable repository entry points for their respective runtimes. They are derived artifacts, not independent policy sources.

## Resolution order

When interpreting the system, use this order:

```text
repository contracts and manifest
        ↓
.assistant/contract/agent.yaml
        ↓
.assistant/personas/0x0da.yaml
        ↓
.assistant/adapters/<runtime>.yaml
        ↓
native instruction artifact
```

If a native artifact conflicts with the neutral contract, the neutral contract wins. If the persona conflicts with the contract, the contract wins. Vendor adapters may change form, but not meaning or authorization boundaries.

## Adding another vendor

A future vendor should require only:

1. a new adapter under `.assistant/adapters/`;
2. a native artifact at the path expected by that runtime;
3. an update to this README.

The contract and persona should remain unchanged unless the underlying behavior itself changes. This is the test for proper abstraction: adding a vendor must not require rewriting the system around that vendor.

## Entity boundary

`0x0da` is associated with `0x0sky`, but organizations, products, and projects remain separate entities. Project-specific operating instructions belong in their own repositories and must not be copied into this personal layer.

## Privacy

This repository is public. Never add secrets, credentials, access tokens, private health or relationship information, or transient personal state.
