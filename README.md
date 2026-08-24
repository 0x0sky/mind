# mind / mind@0x0sky

> An implementation-independent protocol for versioned identity and context, plus the canonical living mind of `0x0sky`.

This repository contains two deliberately separate authorities:

1. **Mind Protocol** — neutral machine contracts, conformance, compatibility, and baseline semantics;
2. **`mind@0x0sky`** — one concrete sovereign instance on `master`.

## Machine entry points

| Entry point | Authority |
| --- | --- |
| [`protocol.yaml`](protocol.yaml) | implementation-independent protocol descriptor |
| [`conformance.yaml`](conformance.yaml) | fixtures, feature matrix, supported ranges, deterministic probes, consumer modes |
| [`compatibility.yaml`](compatibility.yaml) | compatibility freeze, schema fingerprints, forward-compatibility and migration policy |
| [`manifest.yaml`](manifest.yaml) | concrete `mind@0x0sky` context |

The current source contract under development is **Mind Protocol `1.0.0-rc.1`**. It remains unpublished until the separate prerelease action succeeds. Protocol descriptor schema is `3`; manifest schema is `3`; conformance schema is `2`; the concrete `mind@0x0sky` context remains independently versioned at `0.4.0`.

## Identity

[`schema/identity.schema.json`](schema/identity.schema.json) is the universal Identity value for `person`, `organization`, `agent`, `project`, and `product`. It is provider-, repository-, storage-, renderer-, and runtime-independent.

Concrete publication packaging uses [`schema/identity-resource.schema.json`](schema/identity-resource.schema.json). Canonical visual bytes resolve separately through [`schema/visual-assets.schema.json`](schema/visual-assets.schema.json).

Agent model/prompt/memory/runtime state and synthetic portraits are not universal Identity. A canonical agent emblem/glyph remains valid through the shared visual contract.

## Manifest v3

Mind Protocol `0.9.0` froze manifest schema v3 and removed two pre-1.0 compatibility fields from the core manifest. The RC carries that root shape forward unchanged:

- `mind.kind` — redundant with canonical `mind.subject.type`;
- `public_organizations` — GitHub/provider-specific projection that does not belong in the provider-agnostic root contract.

Canonical organization semantics live in typed relationship resources. Provider membership/login data belongs in provider integrations and must not define canonical entity identity.

Unknown root-manifest fields are rejected. Forward compatibility is negotiated through optional modules and versioned optional resources, not by silently extending the root manifest.

## Relationships

Authored relationships remain canonical claims with explicit provenance and confirmation. Provider-discovered observations are derived evidence and never silently become authorship.

## Conformance

[`conformance.yaml`](conformance.yaml) and [`schema/conformance.schema.json`](schema/conformance.schema.json) cover all five subject types through two consumer modes:

- `schema` — JSON Schema plus shared protocol validators;
- `minimal` — an independent core-reader path without JSON Schema or the shared relationship/visual semantic validators.

Each mode declares supported range `>=1.0.0-rc.1 <1.0.0` and must produce the same deterministic outcomes for provenance, canonical visual resolution/integrity, optional/required modules, and frozen root-manifest behavior.

Range evaluation uses SemVer 2.0 prerelease precedence, so `1.0.0-rc.1 < 1.0.0`; build metadata does not alter precedence.

Run:

```bash
python scripts/validate_conformance.py --mode all
```

## Compatibility freeze

[`compatibility.yaml`](compatibility.yaml) carries the machine-readable `0.9.0` freeze into the release candidate. It defines:

- manifest schema `v3` as the frozen root shape;
- `module` as the capability-negotiation unit;
- exact fingerprints for every published JSON Schema;
- unknown optional/required/default-loaded module behavior;
- unknown root-field rejection;
- the `1.x` compatibility rule;
- supported migration floor `0.6.0`;
- deterministic v2 → v3 migration policy;
- prohibition on inferring canonical IDs from provider logins.

For `1.0.0-rc.1`, supported stable migration sources are `0.6.0`, `0.7.0`, `0.8.0`, and the formally published `0.9.0` line.

Run:

```bash
python scripts/validate_compatibility.py
```

## Neutral baseline

[`scripts/generate_baseline.py`](scripts/generate_baseline.py) deterministically generates a neutral protocol bundle with an abstract manifest. The output is never a second source of truth or a long-lived generic branch.

The generated bundle carries protocol, conformance, compatibility, schemas, the abstract manifest, and a deterministic digest inventory. CI generates it twice, verifies byte equality, validates the abstract manifest, and rejects leakage of concrete root-instance identifiers.

```bash
python scripts/generate_baseline.py --check
```

See [`docs/protocol/BASELINE.md`](docs/protocol/BASELINE.md).

## Migration

Supported stable migration sources begin at `0.6.0`. The v2 → v3 migrator removes `mind.kind` only after checking consistency with `mind.subject.type`.

A non-empty provider organization projection may be removed only after its meaning has been preserved in canonical relationships or an explicit provider integration. The migrator never guesses canonical IDs from provider logins.

A conforming `0.9.0` publication needs no manifest-shape migration for `1.0.0-rc.1`; it updates the protocol binding and keeps its independent context version unless durable authored context changes.

See [`docs/protocol/MIGRATION_1.0.md`](docs/protocol/MIGRATION_1.0.md).

## Formal publication sequence

Formal GitHub publication sequence:

1. `0.9.0` — first formal GitHub Release, published;
2. `1.0.0-rc.1` — GitHub prerelease, next publication after this source candidate is verified;
3. `1.0.0` — first compatibility-guaranteed stable release.

Earlier `0.6.0`, `0.7.0`, and `0.8.0` remain source milestones rather than retroactive formal releases.

A deliberately small compatibility-canary set synchronized after `0.9.0` and passed before this RC source candidate. That evidence does not make any named implementation protocol authority. The full named identity, visual-family, provider-binding, agent, project/product, and broader ecosystem rollout begins only after stable `1.0.0`.

See [`docs/protocol/RELEASE_POLICY.md`](docs/protocol/RELEASE_POLICY.md) and [`docs/protocol/ROADMAP.md`](docs/protocol/ROADMAP.md).

## Consumer boundary

Consumers such as [`mind-web`](https://github.com/aiaiaiai-org/mind-web) may prove interoperability but never define protocol truth.

## Privacy boundary

Never commit credentials, secrets, private health/relationship information, transient personal state, or provider-derived observations presented as authored canonical truth.
