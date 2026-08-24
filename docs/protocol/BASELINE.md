# Neutral baseline

Mind Protocol formalizes the baseline as a **generated artifact**, never as a second protocol ontology or a long-lived generic branch.

The source of truth remains `protocol.yaml` plus its declared contract schemas, conformance suite, and compatibility policy. The generator is [`../../scripts/generate_baseline.py`](../../scripts/generate_baseline.py).

## Generated bundle

For the `0.9` line, baseline generation produces:

```text
baseline/
├── protocol.yaml
├── conformance.yaml
├── compatibility.yaml
├── manifest.yaml
├── baseline.json
└── schema/
    └── published protocol schemas
```

`manifest.yaml` is an abstract manifest-schema-v3 composition only:

```yaml
schema_version: 3
mind:
  name: mind
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

There is no `mind.kind`; abstract/concrete semantics derive from canonical `subject.type`. There is no provider-specific organization projection.

The abstract baseline is not a personal, organization, agent, project, or product mind and therefore does not publish an Identity resource.

## Determinism

The bundle contains no timestamp, random identifier, provider lookup, network result, filesystem-dependent absolute path, or concrete-instance content. `baseline.json` records deterministic SHA-256 digests of generated contract files.

CI generates the bundle twice and requires byte-for-byte identical snapshots.

## Compatibility inclusion

`compatibility.yaml` is copied into the generated contract bundle because it is part of the `0.9` public protocol publication set. Its schema fingerprints remain machine-checkable against the bundled `schema/` files.

The baseline does not invent a second compatibility policy: it packages the canonical policy from the verified source commit.

## Instance isolation

The check derives reference-instance tokens from the concrete root `manifest.yaml` and rejects them if they appear anywhere in generated YAML/JSON. This prevents the living `mind@0x0sky` subject or historical reference-repository schema authority from leaking into the neutral artifact.

Provider organization projections were removed from manifest v3; provider-specific identifiers remain outside the neutral baseline by construction.

Protocol namespace URLs such as `aiaiaiai.org/mind/schema/...` identify the protocol contract namespace; they are not concrete subject identities.

## Publication boundary

Source CI proves the generator against the current source contract. For a formal protocol release, the baseline artifact must be generated from the exact immutable release commit/tag that passed the required gates.

`0.9.0` is the first formal release expected to publish the generated neutral baseline artifact. `1.0.0-rc.1` and `1.0.0` publish their own baseline artifacts from their exact release commits.

The historical `foundation/baseline-v0.1.0` branch remains history only and never regains protocol authority.

See [`RELEASE_POLICY.md`](RELEASE_POLICY.md).

## Commands

Validate determinism and isolation:

```bash
python scripts/generate_baseline.py --check
```

Generate a bundle explicitly:

```bash
python scripts/generate_baseline.py --output /tmp/mind-baseline
```
