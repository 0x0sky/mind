# Neutral baseline

Mind Protocol `0.8` formalizes the baseline as a **generated artifact**, never as a second protocol ontology or a long-lived generic branch.

The source of truth remains `protocol.yaml` plus its declared contract schemas and conformance suite. The generator is [`../../scripts/generate_baseline.py`](../../scripts/generate_baseline.py).

## Generated bundle

A baseline generation produces:

```text
baseline/
├── protocol.yaml
├── conformance.yaml
├── manifest.yaml
├── baseline.json
└── schema/
    └── published protocol schemas
```

`manifest.yaml` is an abstract composition only:

```yaml
mind:
  name: mind
  kind: abstract
  context_version: 0.0.0
  subject:
    type: unspecified
    id: unspecified
  owner:
    type: unspecified
    id: unspecified
modules:
  required: []
  registered: []
  catalog: {}
```

It is not a personal, organization, agent, project, or product mind and therefore does not publish an Identity resource.

## Determinism

The bundle contains no timestamp, random identifier, provider lookup, network result, filesystem-dependent absolute path, or concrete-instance content. `baseline.json` records deterministic SHA-256 digests of the generated contract files.

CI generates the bundle twice and requires byte-for-byte identical snapshots.

## Instance isolation

The check derives reference-instance tokens from the concrete root `manifest.yaml` and rejects them if they appear anywhere in generated YAML/JSON. This prevents the living `mind@0x0sky` subject, provider organization logins, or old GitHub schema authority from leaking into the neutral artifact.

Protocol namespace URLs such as `aiaiaiai.org/mind/schema/...` identify the protocol contract namespace; they are not concrete subject identities.

## Publication boundary

Source CI proves the generator against the current source contract. When a protocol release is eventually published, the same deterministic generator should run from that immutable release commit/tag. The historical `foundation/baseline-v0.1.0` branch remains history only and never regains protocol authority.

## Commands

Validate determinism and isolation:

```bash
python scripts/generate_baseline.py --check
```

Generate a bundle explicitly:

```bash
python scripts/generate_baseline.py --output /tmp/mind-baseline
```
