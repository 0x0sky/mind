# Mind Protocol 0.7

Status: **`0.7.0-rc.1` development candidate**

`0.7` builds on the stable `0.6.0` Identity and canonical-visual contract by proving that agent subjects are ordinary first-class protocol identities rather than a special AI runtime object.

The accepted relationship/provenance and visual-identity semantics remain unchanged. Broader independent-consumer conformance remains the `0.8` milestone.

## Two entry points

Mind exposes two explicit machine entry points with different authority:

- [`../../protocol.yaml`](../../protocol.yaml) — implementation-independent protocol descriptor;
- [`../../manifest.yaml`](../../manifest.yaml) — one concrete mind instance.

For this repository, `master` is the living canonical instance **`mind@0x0sky`**. It is not the neutral protocol baseline or the agent conformance fixture.

## Version model

| Version | Current reference | Meaning |
| --- | --- | --- |
| Protocol descriptor schema | `1` | Shape of `protocol.yaml`. |
| Manifest schema | `2` | Shape of one concrete `manifest.yaml`. |
| Protocol | `0.7.0-rc.1` | Shared semantics being proven by this candidate. |
| Concrete instance context | independent | Durable content version of one implementation. |
| Identity schema | `v1` | Universal Identity used equally by person, organization, agent, project, and product subjects. |
| Identity-resource envelope | `v1` | Packaging of that value inside a concrete mind. |
| Visual-assets catalog | `v1` | Packaging and integrity contract for canonical visual bytes. |

No manifest or Identity schema bump is needed merely to prove the already-supported `agent` type.

## Stable 0.6 boundaries carried forward

`0.7` preserves:

- universal Identity independent from provider, repository layout, storage, renderer, and runtime;
- concrete identity-resource packaging separate from Identity semantics;
- explicit subject versus publication-owner semantics;
- opaque canonical `primary_mark.asset_ref` values;
- deterministic visual resolution/failure behavior;
- derived/provider visuals remaining noncanonical;
- presentation-only avatar semantics.

## First-class agent Identity

The synthetic fixture in [`../../tests/fixtures/agent_identity/`](../../tests/fixtures/agent_identity/) exercises the same manifest, Identity, and identity-resource schemas used by any other concrete mind.

It proves:

- `mind.kind: agent` binds to `mind.subject.type: agent`;
- `identity.type/id` bind exactly to the manifest subject;
- an agent subject may have a different organization publication owner;
- the same-owner case remains legal — distinct ownership is a capability, not a requirement;
- no provider account is required for agent identity semantics;
- model, prompt, memory, runtime, and execution state are rejected from universal Identity;
- biological-personhood assertions are not part of the agent Identity contract;
- synthetic/generated portrait fields are not canonical Identity by default.

An agent may still author a canonical emblem or glyph using the existing visual-identity contract. The protocol does not equate `visual_identity` with portrait data.

Full semantics are in [`AGENT_IDENTITY.md`](AGENT_IDENTITY.md).

## Conformance evidence

The candidate is guarded by:

- validation of every published JSON Schema;
- manifest/module/resource validation;
- generic universal Identity-envelope validation;
- protocol descriptor and concrete-instance binding validation;
- relationship/provenance validation;
- canonical visual-asset fixtures;
- the synthetic agent fixture validator;
- regression tests for owner separation, runtime/provider exclusion, biological-personhood exclusion, and synthetic portrait exclusion.

The agent fixture is synthetic and provider-independent; no named agent or hosting account is a protocol dependency.

## Migration from 0.6

A `0.6.0` implementation adopting this candidate should:

1. declare protocol `0.7.0-rc.1` only when it implements the agent semantics being proven here;
2. keep manifest schema `2` unless its manifest shape independently changes;
3. keep its context version unchanged unless its own durable content changes;
4. continue using the same universal Identity and identity-resource schemas;
5. avoid introducing AI-runtime or provider-account fields into universal Identity;
6. preserve all accepted relationship and visual-identity semantics.

## Publication boundary

Merging the source candidate does not create a prerelease tag or GitHub Release. Publication remains a separate explicitly authorized action.
