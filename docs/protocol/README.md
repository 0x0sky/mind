# Mind Protocol 0.7

Status: **`0.7.0` stable source contract**

`0.7` stabilizes agent subjects as ordinary first-class protocol identities on top of the accepted `0.6` Identity and canonical-visual boundaries. It does not add AI-runtime semantics to universal Identity.

The accepted relationship/provenance and visual-identity semantics remain unchanged. Broader independent-consumer conformance remains the `0.8` milestone.

## Two entry points

Mind exposes two explicit machine entry points with different authority:

- [`../../protocol.yaml`](../../protocol.yaml) — implementation-independent protocol descriptor;
- [`../../manifest.yaml`](../../manifest.yaml) — one concrete mind instance.

For this repository, `master` is the living canonical instance **`mind@0x0sky`**. It is not the neutral protocol baseline or the agent conformance fixture.

## Version model

| Version | Stable reference | Meaning |
| --- | --- | --- |
| Protocol descriptor schema | `1` | Shape of `protocol.yaml`. |
| Manifest schema | `2` | Shape of one concrete `manifest.yaml`. |
| Protocol | `0.7.0` | Stable shared semantics implemented by compatible minds and consumers. |
| Concrete instance context | independent | Durable content version of one implementation. |
| Identity schema | `v1` | Universal Identity used equally by person, organization, agent, project, and product subjects. |
| Identity-resource envelope | `v1` | Packaging of that value inside a concrete mind. |
| Visual-assets catalog | `v1` | Packaging and integrity contract for canonical visual bytes. |

No manifest or Identity schema bump was needed to stabilize the already-supported `agent` type.

## Stable agent boundary

`0.7.0` stabilizes these semantics:

- `agent` uses the same universal Identity schema as all other subject types;
- subject and publication owner are independent references;
- an agent may have a distinct publication owner, but distinct ownership is not required;
- no provider account is required for agent Identity;
- model, prompt, memory, runtime, tools, and execution state remain outside universal Identity;
- biological-personhood assertions remain outside universal Identity;
- generated/synthetic portraits remain presentation data by default;
- canonical agent emblems/glyphs remain valid through the existing visual-identity contract.

Full semantics are in [`AGENT_IDENTITY.md`](AGENT_IDENTITY.md).

## Stable earlier boundaries carried forward

`0.7.0` preserves:

- universal Identity independence from provider, repository layout, storage, renderer, and runtime;
- concrete identity-resource packaging separate from Identity semantics;
- authored-vs-derived relationship provenance;
- opaque canonical `primary_mark.asset_ref` values;
- deterministic visual resolution/failure behavior;
- derived/provider visuals remaining noncanonical;
- presentation-only avatar semantics.

## Conformance evidence

The stable source contract is guarded by:

- validation of every published JSON Schema;
- manifest/module/resource validation;
- generic universal Identity-envelope validation;
- protocol descriptor and concrete-instance binding validation;
- relationship/provenance validation;
- canonical visual-asset fixtures;
- the synthetic agent fixture validator;
- regression tests for owner separation, runtime/provider exclusion, biological-personhood exclusion, and synthetic portrait exclusion.

The agent fixture is synthetic and provider-independent. No named agent, hosting account, model, or AI vendor is a protocol dependency.

## Migration from 0.6

A `0.6.0` implementation adopting `0.7.0` should:

1. declare protocol `0.7.0` only when it implements the stable agent semantics;
2. keep manifest schema `2` unless its manifest shape independently changes;
3. keep its context version unchanged unless its own durable content changes;
4. continue using the same universal Identity and identity-resource schemas;
5. keep AI-runtime and provider-account data outside universal Identity;
6. preserve accepted relationship and visual-identity semantics.

`0.7.0` introduces no semantic delta beyond the accepted `0.7.0-rc.1` candidate; the stable promotion freezes the already-tested RC1 contract.

## Publication boundary

The source tree may implement stable `0.7.0` without a published release. Git tags and GitHub Releases are separate explicitly authorized actions.
