# Assistant configuration

This directory separates the canonical assistant contract from model-specific instruction files.

```text
.assistant/
├── sources/
│   └── 0x0da.yaml
├── generated/
│   ├── CHATGPT.md
│   ├── CLAUDE.md
│   └── GEMINI.md
└── README.md
```

## Source of truth

[`sources/0x0da.yaml`](sources/0x0da.yaml) is the only canonical assistant instruction source in this repository. It defines the personal assistant identity `0x0da`, its guard, engineering workflow, GitHub boundaries, privacy rules, and separation-of-concerns contract.

The YAML exists because the source is structured data that can later be validated, transformed, or used to generate additional targets.

## Render targets

Files under [`generated/`](generated/) are model-facing Markdown renders:

- `CHATGPT.md` — imperative instructions for ChatGPT and OpenAI coding agents;
- `CLAUDE.md` — imperative instructions for Claude and Claude Code;
- `GEMINI.md` — imperative instructions for Gemini tooling.

Generated files are derived artifacts. Do not edit their policy independently. Change the YAML source first, then update every render target in the same pull request.

## Entity boundary

`0x0da` is a personal assistant identity associated with `0x0sky`. Organizations and projects such as `0xda-market` are separate entities. Their project-specific instructions belong in their own repositories and must not be embedded in this personal source.

## Privacy

This repository is public. Never add secrets, credentials, access tokens, private health or relationship information, or transient personal state.
