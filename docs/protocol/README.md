# Mind Protocol 0.6

Status: **`0.6.0` stable source contract**

`0.6` separates canonical protocol semantics from any one concrete identity implementation, then defines portable canonical visual-asset resolution on top of that boundary.

The accepted `0.5` relationship/provenance semantics remain part of the stable line. Consumer conformance remains a `0.8` milestone: a renderer or application may verify compatibility, but no consumer grants protocol authority.

## Two entry points

Mind exposes two explicit machine entry points with different authority:

- [`../../protocol.yaml`](../../protocol.yaml) — implementation-independent protocol descriptor;
- [`../../manifest.yaml`](../../manifest.yaml) — one concrete mind instance.

For this repository, `master` is the living canonical instance **`mind@0x0sky`**. It is not the neutral protocol baseline.

## Version model

| Version | Stable reference | Meaning |
| --- | --- | --- |
| Protocol descriptor schema | `1` | Shape of `protocol.yaml`. |
| Manifest schema | `2` | Shape of one concrete `manifest.yaml`. |
| Protocol | `0.6.0` | Shared stable semantics implemented by compatible minds and consumers. |
| Concrete instance context | independent | Durable content version of one implementation. |
| Identity schema | `v1` | Universal implementation-independent Identity value. |
| Identity-resource envelope | `v1` | Packaging of that value inside a concrete mind. |
| Visual-assets catalog | `v1` | Packaging and integrity contract for canonical visual bytes. |

These axes are independent. A protocol-version change does not imply a concrete context change.

## Stable protocol boundaries

The `0.6.0` source contract stabilizes:

- universal Identity independent from provider, repository layout, storage, renderer, and runtime;
- the concrete identity-resource envelope as packaging rather than Identity semantics;
- explicit subject versus publication-owner semantics;
- opaque canonical `primary_mark.asset_ref` values;
- typed canonical visual-asset descriptors with required SHA-256 integrity;
- deterministic missing/ambiguous/unsupported/integrity failure behavior;
- the rule that derived/provider visuals cannot silently become canonical;
- `avatar` as presentation-only for the `0.6` line.

No named real-world identity or visual asset is required to define or test those boundaries.

## Protocol package

`protocol.yaml` names the machine contracts that constitute this line:

- manifest composition;
- module descriptors;
- universal Identity;
- concrete identity-resource envelope;
- authored relationships;
- canonical visual-asset catalog.

Full Identity semantics are in [`IDENTITY.md`](IDENTITY.md), visual resolution in [`VISUAL_IDENTITY.md`](VISUAL_IDENTITY.md), relationship/provenance semantics in [`RELATIONSHIPS.md`](RELATIONSHIPS.md), and migration instructions in [`MIGRATION_0.6.md`](MIGRATION_0.6.md).

## Canonical visual assets

Universal Identity keeps an opaque `visual_identity.primary_mark.asset_ref`. Concrete publications may expose a typed resource conforming to [`../../schema/visual-assets.schema.json`](../../schema/visual-assets.schema.json).

Resolution is deterministic: discover the typed resource, select exactly one matching descriptor, enforce media support, resolve the publication-relative resource, and verify SHA-256 before treating bytes as canonical.

Normative media support is SVG and PNG. WebP is protocol-allowed but consumer-optional.

Provider avatars, generated portraits, screenshots, or other derived visuals cannot silently become the canonical mark. `avatar` is presentation-only in the `0.6` line.

## Conformance evidence

The source contract is guarded by:

- validation of every published JSON Schema;
- manifest/module/resource validation;
- protocol descriptor and concrete-instance binding validation;
- relationship/provenance validation;
- synthetic canonical visual-asset fixtures for person, organization, and agent;
- regression tests for unavailable, missing, ambiguous, unsupported-media, and integrity-failure outcomes;
- validator regression coverage for correctness-critical invariants.

This evidence stabilizes the source contract; it does not replace the broader independent-consumer conformance work planned for `0.8`.

## Migration

See [`MIGRATION_0.6.md`](MIGRATION_0.6.md) for migration from pre-`0.6` identity resources and the RC candidates.

`0.6.0` adds no semantic delta beyond `0.6.0-rc.2`; the stable promotion freezes the already-tested RC2 contract.

## Publication boundary

The source tree may implement the stable `0.6.0` contract without a published protocol release. Git tags and GitHub Releases are separate explicitly authorized actions.
