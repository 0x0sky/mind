# Mind Protocol 0.6

Status: **`0.6.0-rc.2` development candidate**

`0.6` separates canonical protocol semantics from any one concrete identity implementation, then defines portable canonical visual-asset resolution on top of that boundary.

The accepted `0.5` relationship/provenance semantics remain part of the line. Consumer conformance is intentionally deferred to `0.8`: a renderer or application may verify compatibility, but no consumer grants protocol stability or protocol authority.

## Two entry points

Mind exposes two explicit machine entry points with different authority:

- [`../../protocol.yaml`](../../protocol.yaml) — implementation-independent protocol descriptor;
- [`../../manifest.yaml`](../../manifest.yaml) — one concrete mind instance.

For this repository, `master` is the living canonical instance **`mind@0x0sky`**. It is not the neutral protocol baseline.

## Version model

| Version | Current development reference | Meaning |
| --- | --- | --- |
| Protocol descriptor schema | `1` | Shape of `protocol.yaml`. |
| Manifest schema | `2` | Shape of one concrete `manifest.yaml`. |
| Protocol | `0.6.0-rc.2` | Shared semantics implemented by compatible minds and consumers. |
| Concrete instance context | independent | Durable content version of one implementation. |
| Identity schema | `v1` | Universal implementation-independent Identity value. |
| Identity-resource envelope | `v1` | Packaging of that value inside a concrete mind. |
| Visual-assets catalog | `v1` | Packaging and integrity contract for canonical visual bytes. |

These axes are independent. A protocol-version change does not imply a concrete context change.

## Protocol package

`protocol.yaml` names the machine contracts that constitute the current protocol package:

- manifest composition;
- module descriptors;
- universal Identity;
- concrete identity-resource envelope;
- authored relationships;
- canonical visual-asset catalog.

It also publishes machine-readable visual-identity policy for resolution, integrity, media support, fallback, and avatar semantics.

Merging protocol development into `master` is not itself a release. Tags and GitHub Releases are separate publication actions.

## Identity split

[`../../schema/identity.schema.json`](../../schema/identity.schema.json) defines only the canonical semantic Identity value. It has no provider binding, repository path, validation path, storage contract, runtime state, or renderer handle.

A concrete mind carries that value through [`../../schema/identity-resource.schema.json`](../../schema/identity-resource.schema.json). The embedded Identity `type/id` must match `mind.subject`.

Full semantics are defined in [`IDENTITY.md`](IDENTITY.md).

## Canonical visual assets

`0.6.0-rc.2` completes the protocol-level visual boundary without requiring any named real-world identity or logo.

Universal Identity keeps an opaque `visual_identity.primary_mark.asset_ref`. Concrete publications may expose a typed resource conforming to [`../../schema/visual-assets.schema.json`](../../schema/visual-assets.schema.json).

Resolution is deterministic:

- discover typed visual-asset resources;
- select exactly one descriptor matching the opaque `asset_ref`;
- enforce protocol media policy;
- resolve the publication-relative asset location;
- verify required SHA-256 integrity;
- return an explicit outcome rather than silently substituting another visual.

Normative media support is SVG and PNG. WebP is protocol-allowed but consumer-optional.

Provider avatars, generated portraits, screenshots, or other derived visuals cannot silently become the canonical mark. `avatar` is presentation-only in the `0.6` line.

See [`VISUAL_IDENTITY.md`](VISUAL_IDENTITY.md).

## Synthetic conformance fixtures

The protocol package includes synthetic visual-identity fixtures for:

- person;
- organization;
- agent.

They prove the visual contract without making any real person, organization, agent, provider account, or repository asset a protocol dependency.

Regression tests additionally prove deterministic unavailable, missing, ambiguous, unsupported-media, and integrity-failure outcomes.

## Relationships and provider projections

The authored relationship and provenance model introduced in `0.5` remains intact. Canonical relationship entity ids remain provider-independent.

Provider-facing compatibility fields may contain provider identifiers. They must never be interpreted as canonical entity identity merely because strings happen to match.

## Migration from earlier 0.6 candidates

A concrete implementation adopting `0.6.0-rc.2` should:

1. keep manifest schema `2` unless the manifest machine shape itself changes;
2. declare protocol version `0.6.0-rc.2`;
3. keep concrete context version unchanged when only the shared protocol version advances;
4. continue treating `schema/identity.schema.json` as universal Identity;
5. resolve authored `primary_mark.asset_ref` only through the typed visual-assets contract;
6. never store repository paths, provider URLs, digests, or storage locators inside universal Identity;
7. preserve derived provider visuals as noncanonical presentation/evidence;
8. treat `avatar` as presentation-only.

A concrete implementation with no canonical primary mark remains conformant; visual identity is optional.

## Acceptance gate for `0.6.0-rc.2`

The candidate is internally acceptable when:

- `protocol.yaml` and every published JSON Schema validate;
- universal Identity remains provider/storage/runtime independent;
- asset-ref resolution is deterministic;
- missing, ambiguous, unsupported-media, and integrity failures are observable;
- provider-derived visuals cannot silently replace canonical marks;
- synthetic person, organization, and agent visual fixtures validate;
- no named real-world asset is required by protocol tests;
- relationship/provenance and existing validator regression suites remain green.

Publishing a tag or GitHub Release remains a separate action.
