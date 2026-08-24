# Mind Protocol 1.0 release candidate

Status: **`1.0.0-rc.1` source candidate; formal prerelease not yet published**

Mind Protocol is the implementation-independent contract in this repository. The same repository also contains the concrete living `mind@0x0sky` reference implementation, but that concrete instance is not protocol authority and is never a template for another Mind.

See [`../REPOSITORY_MODEL.md`](../REPOSITORY_MODEL.md) before interpreting the repository layout.

## Machine entry points

- [`../../mind-repository.yaml`](../../mind-repository.yaml) — repository-role routing; repository metadata, **not** protocol contract;
- [`../../protocol.yaml`](../../protocol.yaml) — implementation-independent protocol descriptor, schema `v3`;
- [`../../conformance.yaml`](../../conformance.yaml) — conformance suite and feature matrix, schema `v2`;
- [`../../compatibility.yaml`](../../compatibility.yaml) — compatibility freeze, schema fingerprints, 1.x policy, migration floor;
- [`../../manifest.yaml`](../../manifest.yaml) — concrete `mind@0x0sky` reference instance only;
- [`BASELINE.md`](BASELINE.md) — generated abstract neutral baseline;
- [`BOOTSTRAP.md`](BOOTSTRAP.md) — canonical creation path for a new concrete Mind;
- [`RELEASE_POLICY.md`](RELEASE_POLICY.md) — formal publication sequence and release gates.

## Authority model

The core rule is simple:

```text
protocol.yaml        → universal Mind semantics
manifest.yaml        → only mind@0x0sky concrete content
mind-repository.yaml → tells humans/agents which authority applies
```

A GitHub fork of this repository is valid for protocol development. It is not the canonical way to create another concrete Mind because `master` carries the `mind@0x0sky` implementation and history.

New concrete Minds are bootstrapped from an exact immutable protocol release through the neutral baseline. See [`BOOTSTRAP.md`](BOOTSTRAP.md).

## Current version model

| Axis | Current reference | Meaning |
| --- | --- | --- |
| Protocol descriptor schema | `3` | Descriptor shape and lifecycle/contract discovery. |
| Manifest schema | `3` | Frozen root shape from `0.9.0`. |
| Protocol | `1.0.0-rc.1` | Final-contract release candidate. |
| Concrete `mind@0x0sky` context | `0.4.0` | Independent durable content version. |
| Conformance suite schema | `2` | Dual consumer modes and deterministic probes. |
| Compatibility policy schema | `1` | Schema fingerprints, forward compatibility, migration policy. |
| Identity schema | `1` | Universal Identity for all five subject types. |

Protocol and concrete context versions are independent. Protocol tags belong to this protocol repository; concrete consumer repositories do not reuse them as context tags.

## Frozen manifest and capability model

Manifest schema v3, frozen in `0.9.0`, removes:

- `mind.kind` — canonical classification is `mind.subject.type`;
- provider-specific organization projections such as `public_organizations`.

Unknown root fields are rejected. Compatible extension happens through optional modules or versioned optional resources rather than an unstructured root extension bag.

`module` remains the capability-negotiation unit:

```text
unknown optional module, not requested → ignore
unknown required module                 → reject
unknown default-loaded module           → reject
unknown root manifest field             → reject
```

## Compatibility and schema immutability

[`../../compatibility.yaml`](../../compatibility.yaml) fingerprints each published JSON Schema by `$id` and exact Git blob SHA-1. The `1.0.0-rc.1` source candidate reuses the `0.9.0` schema identities only because those schema bytes are unchanged.

Release-specific protocol version, lifecycle state, and migration-source policy are enforced semantically instead of mutating reusable schema bytes.

Supported stable migration sources for the RC are:

- `0.6.0`;
- `0.7.0`;
- `0.8.0`;
- formal `0.9.0`.

## Conformance

The suite covers synthetic `person`, `organization`, `agent`, `project`, and `product` subjects through two independent reader modes:

- `schema` — JSON Schema plus shared semantic validators;
- `minimal` — independent reader logic without the shared relationship/visual validators.

The RC support range is:

```text
>= 1.0.0-rc.1
<  1.0.0
```

Range evaluation follows strict SemVer 2.0 prerelease precedence.

```bash
python scripts/validate_conformance.py --mode all
```

## Neutral baseline

[`../../scripts/generate_baseline.py`](../../scripts/generate_baseline.py) produces a deterministic abstract bundle with:

- `subject: unspecified`;
- `owner: unspecified`;
- no Identity module;
- no named reference-instance content;
- exact protocol/conformance/compatibility/schema contracts.

The neutral baseline is not itself a concrete Mind and is never a long-lived generic branch. See [`BASELINE.md`](BASELINE.md).

## Concrete bootstrap

[`../../scripts/bootstrap_mind.py`](../../scripts/bootstrap_mind.py) turns an exact checked-out release into a minimal concrete publication. It requires explicit subject, publication owner, display name, context version, and repository visibility.

It creates only the required Identity module/resource plus exact protocol locks. It does not copy relationships, knowledge, engineering context, provider identities, visuals, or other content from the reference implementation.

See [`BOOTSTRAP.md`](BOOTSTRAP.md).

## Release boundary

`0.9.0` is the first formal GitHub Release and has already been published. The next publication is `1.0.0-rc.1` as a GitHub prerelease after the final source tree receives green PR/tree verification. Stable `1.0.0` begins the compatibility-guaranteed `1.x` line.

Merging source is not publishing a release. Tags and GitHub Releases remain separate explicit actions.

See [`RELEASE_POLICY.md`](RELEASE_POLICY.md), [`ROADMAP.md`](ROADMAP.md), and [`MIGRATION_1.0.md`](MIGRATION_1.0.md).

<!-- © 2026 aiaiaiai · aiaiaiai.org -->
