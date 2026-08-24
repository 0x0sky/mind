# Neutral baseline

Mind Protocol formalizes the baseline as a **generated abstract artifact**, never as a second protocol ontology, a long-lived generic branch, or a concrete Mind template.

The source of truth remains `protocol.yaml` plus its declared contract schemas, conformance suite, and compatibility policy. The generator is [`../../scripts/generate_baseline.py`](../../scripts/generate_baseline.py).

## What the baseline is

Baseline generation produces:

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

`manifest.yaml` is an abstract manifest-v3 composition only:

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

There is no `mind.kind`, no provider-specific organization projection, and no concrete Identity resource.

The baseline is therefore **not** a person, organization, agent, project, or product Mind. Publishing it unchanged as if it were one would be a category error.

## Baseline versus reference implementation

The root `manifest.yaml` in this repository is the concrete living `mind@0x0sky` reference implementation. The generated baseline is deliberately isolated from that instance.

The canonical relationship is:

```text
Mind Protocol contracts
        ↓ generate
neutral abstract baseline
        ↓ bootstrap with explicit authored identity
concrete mind@<id>
```

It is **not**:

```text
mind@0x0sky
   ↓ copy / rename ids
another concrete Mind
```

`mind@0x0sky` may demonstrate that the protocol works in a real publication, but it is never template authority.

## Concrete creation happens after the baseline

Use [`BOOTSTRAP.md`](BOOTSTRAP.md) and [`../../scripts/bootstrap_mind.py`](../../scripts/bootstrap_mind.py) to create a minimal concrete Mind from an exact immutable protocol release.

Bootstrap introduces only explicit authored inputs: subject, publication owner, display name, context version, and repository visibility. It then creates the required Identity module/resource. Additional modules are added only when separately authored for that subject.

## Determinism

The baseline contains no timestamp, random identifier, provider lookup, network result, filesystem-dependent absolute path, or concrete-instance content. `baseline.json` records deterministic SHA-256 digests of generated contract files.

CI generates the bundle twice and requires byte-for-byte identical snapshots.

## Compatibility inclusion

`compatibility.yaml` is copied into the generated contract bundle because compatibility policy is part of the formal protocol publication set. Its schema fingerprints remain machine-checkable against the bundled `schema/` files.

The baseline does not invent a second compatibility policy: it packages the canonical policy from the verified source tree.

## Instance isolation

The check derives reference-instance tokens from the concrete root `manifest.yaml` and rejects them if they appear anywhere in generated YAML/JSON. This prevents the living `mind@0x0sky` subject from leaking into the neutral artifact.

Provider-specific identifiers remain outside the neutral baseline by construction. Protocol namespace URLs such as `aiaiaiai.org/mind/schema/...` identify protocol contract namespaces, not concrete subjects.

## Publication boundary

Source CI proves the generator against the current source contract. A formal protocol release publishes the baseline generated from the exact verified release tree/tag.

`0.9.0` is the first formal release that published a neutral baseline. `1.0.0-rc.1` and stable `1.0.0` publish their own deterministic baseline artifacts from their exact release trees.

The historical `foundation/baseline-v0.1.0` branch remains history only and never regains protocol authority.

See [`RELEASE_POLICY.md`](RELEASE_POLICY.md).

## Commands

Validate determinism and instance isolation:

```bash
python scripts/generate_baseline.py --check
```

Generate the abstract bundle explicitly:

```bash
python scripts/generate_baseline.py --output /tmp/mind-baseline
```

Create a concrete Mind instead:

```bash
python scripts/bootstrap_mind.py --help
```

<!-- © 2026 aiaiaiai · aiaiaiai.org -->
