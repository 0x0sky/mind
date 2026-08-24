# mind / mind@0x0sky

> An implementation-independent protocol for versioned identity and context, plus the canonical living mind of `0x0sky`.

This repository contains two deliberately separate authorities:

1. **Mind Protocol** — neutral machine contracts, conformance, and baseline semantics;
2. **`mind@0x0sky`** — one concrete sovereign instance on `master`.

## Machine entry points

| Entry point | Authority |
| --- | --- |
| [`protocol.yaml`](protocol.yaml) | implementation-independent protocol descriptor |
| [`conformance.yaml`](conformance.yaml) | fixtures, feature matrix, supported ranges, deterministic probes, compatibility policy, consumer modes |
| [`manifest.yaml`](manifest.yaml) | concrete `mind@0x0sky` context |

The current source contract is **Mind Protocol `0.8.0`**. Protocol descriptor schema is `2`; manifest schema remains `2`; the concrete `mind@0x0sky` context remains independently versioned at `0.4.0`.

## Identity

[`schema/identity.schema.json`](schema/identity.schema.json) is the universal Identity value for `person`, `organization`, `agent`, `project`, and `product`. It is provider-, repository-, storage-, renderer-, and runtime-independent.

Concrete publication packaging uses [`schema/identity-resource.schema.json`](schema/identity-resource.schema.json). Canonical visual bytes resolve separately through [`schema/visual-assets.schema.json`](schema/visual-assets.schema.json).

Agent model/prompt/memory/runtime state and synthetic portraits are not universal Identity. A canonical agent emblem/glyph remains valid through the shared visual contract.

## Relationships

Authored relationships remain canonical claims with explicit provenance and confirmation. Provider-discovered observations are derived evidence and never silently become authorship.

## Conformance

Mind Protocol `0.8.0` adds [`conformance.yaml`](conformance.yaml) and [`schema/conformance.schema.json`](schema/conformance.schema.json).

The suite covers all five subject types with synthetic descriptors and explicit `expected_result: pass`. It runs through two consumer modes:

- `schema` — JSON Schema plus shared protocol validators;
- `minimal` — an independent core-reader path without JSON Schema or the shared relationship/visual semantic validators.

Each mode explicitly declares supported range `>=0.8.0 <0.9.0`. Both must produce the same deterministic probe outcomes:

- preserve authored relationship provenance;
- reject derived provenance from the canonical authored relationship resource;
- resolve a valid canonical visual mark;
- report canonical visual integrity failure deterministically;
- ignore an unknown optional module when it is not requested;
- reject an unknown required/default-loaded module.

Run:

```bash
python scripts/validate_conformance.py --mode all
```

## Neutral baseline

[`scripts/generate_baseline.py`](scripts/generate_baseline.py) deterministically generates a neutral protocol bundle with an abstract manifest. The output is never a second source of truth or a long-lived generic branch.

CI generates it twice, verifies byte equality, validates the abstract manifest, and rejects leakage of concrete root-instance identifiers.

```bash
python scripts/generate_baseline.py --check
```

See [`docs/protocol/BASELINE.md`](docs/protocol/BASELINE.md).

## Schemas

Published JSON Schema `$id` values use the neutral `aiaiaiai.org/mind/schema/...` protocol namespace. Historical `github.com/0x0sky/mind` schema authority is not carried into the generated baseline.

## Versioning and publication

Protocol, descriptor/manifest shapes, typed resource schemas, and concrete context are independent version axes. Merging the `0.8.0` source contract does not create a Git tag or GitHub Release; publication is a separate explicitly authorized action.

## Consumer boundary

Consumers such as [`mind-web`](https://github.com/aiaiaiai-org/mind-web) may prove interoperability but never define protocol truth.

## Privacy boundary

Never commit credentials, secrets, private health/relationship information, transient personal state, or provider-derived observations presented as authored canonical truth.
