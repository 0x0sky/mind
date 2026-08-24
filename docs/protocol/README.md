# Mind Protocol 0.9

Status: **`0.9.0` compatibility-freeze source contract under development**

`0.9` freezes the public compatibility surface before `1.0`. It removes pre-1.0 root-manifest compatibility debt, makes compatibility policy machine-readable, fingerprints the published schema set, defines forward-compatible capability negotiation, and establishes the supported migration floor.

The accepted Identity, relationship/provenance, canonical visual-asset, agent, conformance, and neutral-baseline boundaries from `0.4`–`0.8` remain in force.

## Machine entry points

- [`../../protocol.yaml`](../../protocol.yaml) — implementation-independent protocol descriptor, descriptor schema `v3`;
- [`../../conformance.yaml`](../../conformance.yaml) — machine-readable conformance suite and feature matrix, schema `v2`;
- [`../../compatibility.yaml`](../../compatibility.yaml) — compatibility freeze, fingerprints, 1.x policy, and migration floor;
- [`../../manifest.yaml`](../../manifest.yaml) — the concrete living `mind@0x0sky` instance, manifest schema `v3`;
- [`BASELINE.md`](BASELINE.md) — generated neutral baseline semantics;
- [`RELEASE_POLICY.md`](RELEASE_POLICY.md) — formal publication sequence and release gates.

## Version model

| Version | Current reference | Meaning |
| --- | --- | --- |
| Protocol descriptor schema | `3` | Adds discoverable compatibility policy authority. |
| Manifest schema | `3` | Removes `mind.kind` and provider-specific `public_organizations`. |
| Protocol | `0.9.0` | Compatibility-freeze line before 1.0. |
| Concrete instance context | independent (`0.4.0` in this repository) | Durable content version of one implementation. |
| Conformance suite schema | `v2` | Frozen-root and capability-unit probes in addition to 0.8 evidence. |
| Compatibility policy schema | `v1` | Machine freeze, schema fingerprints, forward compatibility, migration floor. |
| Identity schema | `v1` | Universal Identity for all five subject types. |

## Manifest v3

The pre-1.0 root shape is deliberately smaller.

Removed:

- `mind.kind` — classification already exists as `mind.subject.type`;
- `public_organizations` and older provider-organization aliases — provider logins are not canonical entity IDs.

The core manifest therefore has one identity classification source and no GitHub-specific organization projection.

Unknown root-manifest fields are rejected. Adding a new root concept requires an explicit future manifest schema revision and protocol-wide evidence.

## Capability negotiation

`module` is the protocol capability unit.

Forward compatibility is:

```text
unknown optional module, not requested: ignore
unknown required module:                reject
unknown default-loaded module:          reject
unknown root manifest field:            reject
```

Compatible future additions belong in optional modules or versioned optional resources where semantics permit. The root manifest is not an extension bag.

## Compatibility freeze

[`../../compatibility.yaml`](../../compatibility.yaml) freezes the public schema set by both `$id` and exact Git blob fingerprint.

That prevents a schema from changing silently while keeping the same public identity/version. During the `0.9` milestone the fingerprints may move as the freeze is finalized; once `0.9.0` is formally released, changing frozen schema bytes requires the appropriate protocol/schema evolution rather than editing in place.

The policy also defines the initial `1.x` rule:

- `1.0.0` is the compatibility baseline;
- compatible additions use optional modules or versioned optional resources;
- breaking core changes require a new major protocol version;
- consumers honor their declared supported protocol range.

Validate:

```bash
python scripts/validate_compatibility.py
```

## Conformance suite

The suite still covers synthetic `person`, `organization`, `agent`, `project`, and `product` subjects through two intentionally distinct reader paths:

- `schema` — JSON Schema plus shared protocol semantic validators;
- `minimal` — independent core-reader logic without JSON Schema/shared relationship/visual semantic validators.

For `0.9`, both modes declare `[0.9.0, 1.0.0)` and preserve the 0.8 deterministic probes for provenance, canonical visual resolution/integrity, and optional/required modules. They additionally prove the frozen root behavior: removed aliases and unknown root fields are rejected.

Run:

```bash
python scripts/validate_conformance.py --mode all
```

## Migration floor

The supported stable pre-1.0 migration floor is **`0.6.0`**.

Stable source lines `0.6.0`, `0.7.0`, and `0.8.0` may migrate into `0.9.0` through the supported migration contract. Older lines fail deterministically and must use an earlier documented migration path first.

Manifest v2 → v3 rules:

1. require `mind.kind` to agree with `mind.subject.type` before removing it;
2. preserve any non-empty provider organization projection in canonical relationships or an explicit provider integration before removing it;
3. never infer canonical IDs from provider logins;
4. do not bump a concrete `mind.context_version` solely because protocol packaging migrated.

The migration utility is [`../../scripts/migrate_manifest_v2_to_v3.py`](../../scripts/migrate_manifest_v2_to_v3.py).

## Neutral baseline

The generated baseline now uses manifest schema `v3` and includes `compatibility.yaml` along with protocol, conformance, all published schemas, and deterministic digest metadata.

The baseline remains generated, reproducible, provider-independent, and free of concrete `mind@0x0sky` content.

See [`BASELINE.md`](BASELINE.md).

## Formal release boundary

`0.9.0` is the **first formal GitHub Release** of Mind Protocol. `1.0.0-rc.1` will be a GitHub prerelease. `1.0.0` will be the first compatibility-guaranteed stable release.

Earlier `0.6.0`–`0.8.0` remain historical source milestones and are not retroactively published as formal releases.

Concrete named identity synchronization begins after stable `1.0.0`, outside the protocol stabilization milestones.

See [`RELEASE_POLICY.md`](RELEASE_POLICY.md).
