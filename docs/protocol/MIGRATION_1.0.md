# Migrating to Mind Protocol 1.0

This guide covers the `1.0` release-candidate and stable line. The first candidate is `1.0.0-rc.1`.

The supported stable migration floor remains `0.6.0`.

## Supported stable source lines for rc.1

Direct supported stable sources are:

- `0.6.0`;
- `0.7.0`;
- `0.8.0`;
- `0.9.0`.

A source below `0.6.0` fails deterministically and must first use an earlier documented migration path.

## Migrating from 0.9.0

`0.9.0` already froze manifest schema `v3` and the reusable protocol resource schemas intended for the `1.0` train. Therefore a conforming `0.9.0` publication does **not** need a manifest-shape or resource-shape migration merely to consume `1.0.0-rc.1`.

The concrete implementation should:

1. consume the exact immutable `v1.0.0-rc.1` release artifact after it is formally published;
2. update its protocol binding from `0.9.0` to `1.0.0-rc.1`;
3. preserve its canonical subject, owner, Identity, authored relationship provenance, loading policy, and provider-independent IDs;
4. keep `mind.context_version` unchanged unless durable authored context independently changes;
5. validate against the exact RC contract set and declared supported range.

Protocol version and concrete context version remain independent axes.

## Migrating from 0.6–0.8

Implementations on `0.6.0`, `0.7.0`, or `0.8.0` must also satisfy the `0.9.0` manifest-v3 migration rules before they can conform to the `1.0` line.

In particular:

- remove `mind.kind` only after proving it agrees with `mind.subject.type`;
- remove provider-facing `public_organizations` only after preserving any intended meaning as canonical relationships or explicit provider integration data;
- never infer a canonical entity ID from a provider login;
- reject unknown root-manifest fields;
- treat modules as the capability-negotiation unit.

See [`MIGRATION_0.9.md`](MIGRATION_0.9.md) for the detailed v2 → v3 procedure and migrator usage.

## Release-candidate range semantics

The `1.0.0-rc.1` conformance range is:

```text
>= 1.0.0-rc.1
<  1.0.0
```

Range comparison follows SemVer 2.0 precedence. In particular:

```text
1.0.0-rc.1 < 1.0.0-rc.2 < 1.0.0
```

Build metadata does not affect precedence.

A consumer must not collapse prerelease versions to only their major/minor/patch core when evaluating support ranges.

## Schema immutability

The RC reuses the published `0.9.0` schema identities only where the schema bytes are exactly unchanged. A schema whose shape changes after publication requires a new versioned `$id`; it must never be silently rewritten under an already published identity.

Exact protocol release identity, lifecycle state, and migration-source policy are semantic bindings and are validated outside the reusable schema bytes.

## Compatibility promise

`1.0.0-rc.1` is a prerelease. The compatibility-guaranteed `1.x` line begins only with stable `1.0.0`.

If a blocking universal semantic defect is found after an RC is published, the existing tag remains immutable and a later RC is required.

## Verification

A complete implementation should verify:

- manifest/resource validation;
- exact protocol version binding;
- Identity type/id equality with the manifest subject;
- authored relationship provenance;
- optional/required module behavior;
- canonical visual resolution/failure semantics where a canonical mark is present;
- declared protocol support range using SemVer 2.0 precedence.

The protocol repository additionally proves deterministic neutral-baseline and release-bundle generation from a clean checkout.

<!-- © 2026 aiaiaiai · aiaiaiai.org -->
