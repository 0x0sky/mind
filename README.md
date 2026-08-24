# mind — Mind Protocol + mind@0x0sky

> One repository, two deliberately separate authorities: the implementation-independent **Mind Protocol** and the concrete living **`mind@0x0sky`** reference implementation.

> **Creating your own Mind? Do not fork `master` as a template.** `master` also contains `mind@0x0sky`. Bootstrap a new concrete Mind from an exact immutable protocol release instead: [`docs/protocol/BOOTSTRAP.md`](docs/protocol/BOOTSTRAP.md).

## What this repository is

| Role | Canonical entry point | Authority | Not authority |
| --- | --- | --- | --- |
| **Mind Protocol** | [`protocol.yaml`](protocol.yaml) | universal contracts, schemas, conformance, compatibility, release semantics | any named person's or organization's content |
| **`mind@0x0sky`** | [`manifest.yaml`](manifest.yaml) | authored context for subject `person:0x0sky` | a template for another Mind |

`mind@0x0sky` is a **reference implementation, never a template authority**. Co-location in one Git repository does not mean that concrete Minds inherit from it.

The machine-readable repository boundary is [`mind-repository.yaml`](mind-repository.yaml). The full rationale is [`docs/REPOSITORY_MODEL.md`](docs/REPOSITORY_MODEL.md).

## Choose the right path

| You want to… | Start here | Rule |
| --- | --- | --- |
| understand or change Mind Protocol | `mind-repository.yaml` → `protocol.yaml` | a GitHub fork/feature branch is fine for protocol development |
| work on `0x0sky`'s concrete Mind | `mind-repository.yaml` → `manifest.yaml` | follow only registered modules for this subject |
| create a new person/org/agent/project/product Mind | exact release tag → `scripts/bootstrap_mind.py` | **never seed it from `mind@0x0sky` content** |
| consume a protocol release | exact immutable tag/release artifact | never consume floating `master` as release authority |

Canonical construction of a new Mind is:

```text
exact Mind Protocol release
          ↓
   neutral baseline
          ↓
subject + publication-owner semantics + Identity
          ↓
     concrete mind@<id>
          ↓
only authored modules/resources for that subject
```

By default the publication owner is the subject itself; bootstrap accepts an explicit different owner only when both owner type and id are supplied.

## Machine entry points

| Entry point | Authority |
| --- | --- |
| [`mind-repository.yaml`](mind-repository.yaml) | repository-role routing; explicitly **not** a protocol contract |
| [`protocol.yaml`](protocol.yaml) | implementation-independent protocol descriptor |
| [`conformance.yaml`](conformance.yaml) | fixtures, feature matrix, supported ranges, deterministic probes, consumer modes |
| [`compatibility.yaml`](compatibility.yaml) | compatibility freeze, schema fingerprints, forward-compatibility and migration policy |
| [`manifest.yaml`](manifest.yaml) | concrete `mind@0x0sky` context only |

The current source contract is **Mind Protocol `1.0.0-rc.1`**. It remains unpublished until the separate prerelease action succeeds. Protocol descriptor schema is `3`; manifest schema is `3`; conformance schema is `2`; the concrete `mind@0x0sky` context remains independently versioned at `0.4.0`.

## Identity

[`schema/identity.schema.json`](schema/identity.schema.json) is the universal Identity value for `person`, `organization`, `agent`, `project`, and `product`. It is provider-, repository-, storage-, renderer-, and runtime-independent.

Concrete publication packaging uses [`schema/identity-resource.schema.json`](schema/identity-resource.schema.json). Canonical visual bytes resolve separately through [`schema/visual-assets.schema.json`](schema/visual-assets.schema.json).

Agent model/prompt/memory/runtime state and synthetic portraits are not universal Identity. A canonical agent emblem/glyph remains valid through the shared visual contract.

## Manifest v3

Mind Protocol `0.9.0` froze manifest schema v3 and removed two pre-1.0 compatibility fields from the core manifest. The RC carries that root shape forward unchanged:

- `mind.kind` — redundant with canonical `mind.subject.type`;
- `public_organizations` — provider-specific projection that does not belong in the provider-agnostic root contract.

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

```bash
python scripts/validate_conformance.py --mode all
```

## Compatibility freeze

[`compatibility.yaml`](compatibility.yaml) carries the machine-readable `0.9.0` freeze into the release candidate. It defines manifest schema v3, module-based capability negotiation, exact schema fingerprints, unknown-module behavior, root-field rejection, the initial `1.x` compatibility rule, migration floor `0.6.0`, deterministic v2 → v3 migration, and the prohibition on inferring canonical IDs from provider logins.

For `1.0.0-rc.1`, supported stable migration sources are `0.6.0`, `0.7.0`, `0.8.0`, and formal `0.9.0`.

```bash
python scripts/validate_compatibility.py
```

## Neutral baseline and concrete bootstrap

[`scripts/generate_baseline.py`](scripts/generate_baseline.py) produces the deterministic **abstract** protocol baseline. It has `subject: unspecified`, no concrete Identity, and is never itself a person's or organization's Mind.

[`scripts/bootstrap_mind.py`](scripts/bootstrap_mind.py) is the canonical transition from an exact protocol release to a minimal concrete Mind. It requires explicit subject, display name, context version, and repository visibility. Publication owner defaults to the subject, with an explicit distinct-owner override. Bootstrap then creates only the Identity module plus exact protocol locks. It does not copy reference-instance modules.

```bash
python scripts/generate_baseline.py --check
```

See [`docs/protocol/BASELINE.md`](docs/protocol/BASELINE.md) and [`docs/protocol/BOOTSTRAP.md`](docs/protocol/BOOTSTRAP.md).

## Version axes

Protocol and concrete context are independent:

- `protocol.version` identifies the Mind Protocol release;
- `mind.context_version` identifies durable authored content of one concrete Mind.

A protocol bump does not imply a context bump. A concrete context bump does not imply a protocol release. Protocol-version tags belong to the protocol repository and must not be reused as concrete-context tags in consumer repositories.

## Migration

Supported stable migration sources begin at `0.6.0`. The v2 → v3 migrator removes `mind.kind` only after checking consistency with `mind.subject.type` and never guesses canonical IDs from provider logins.

A conforming `0.9.0` publication needs no manifest-shape migration for `1.0.0-rc.1`; it updates the protocol binding and keeps its independent `mind.context_version` unless durable authored context also changes.

See [`docs/protocol/MIGRATION_1.0.md`](docs/protocol/MIGRATION_1.0.md).

## Formal publication sequence

1. `0.9.0` — first formal GitHub Release, published;
2. `1.0.0-rc.1` — next GitHub prerelease after this exact source tree is verified;
3. `1.0.0` — first compatibility-guaranteed stable release.

A deliberately small compatibility-canary set synchronized after `0.9.0` and passed before this RC candidate. The full named identity, visual-family, provider-binding, agent, project/product, and broader ecosystem rollout begins only after stable `1.0.0`.

See [`docs/protocol/RELEASE_POLICY.md`](docs/protocol/RELEASE_POLICY.md) and [`docs/protocol/ROADMAP.md`](docs/protocol/ROADMAP.md).

## Consumer boundary

Consumers such as [`mind-web`](https://github.com/aiaiaiai-org/mind-web) may prove interoperability but never define protocol truth.

## Privacy boundary

Never commit credentials, secrets, private health/relationship information, transient personal state, or provider-derived observations presented as authored canonical truth.

<!-- © 2026 aiaiaiai · aiaiaiai.org -->
