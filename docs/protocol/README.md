# Mind Protocol 0.6

Status: **`0.6.0-rc.1` development candidate**

`0.6` separates canonical protocol semantics from any one concrete identity implementation before the visual-identity contract is exercised with real assets.

The accepted `0.5` relationship/provenance semantics are carried forward into this line. Consumer conformance is intentionally deferred to the `0.8` milestone: a renderer or application may verify compatibility, but no consumer grants protocol stability or protocol authority.

## Two entry points

Mind exposes two explicit machine entry points with different authority:

- [`../../protocol.yaml`](../../protocol.yaml) — implementation-independent protocol descriptor;
- [`../../manifest.yaml`](../../manifest.yaml) — one concrete mind instance.

For this repository, `master` is the living canonical instance **`mind@0x0sky`**.

`protocol.yaml` is not an abstract mind instance and does not invent an `unspecified` identity. It describes the contracts that any compatible concrete mind may implement.

## Version model

| Version | Current development reference | Meaning |
| --- | --- | --- |
| Protocol descriptor schema | `1` | Shape of `protocol.yaml`. |
| Manifest schema | `2` | Shape of one concrete `manifest.yaml`. |
| Protocol | `0.6.0-rc.1` | Shared semantics implemented by compatible minds and consumers. |
| `mind@0x0sky` context | `0.4.0` | Durable context of this concrete instance. |
| Identity schema | `v1` | Universal implementation-independent Identity value. |
| Identity-resource envelope | `v1` | Packaging of that value inside a concrete mind. |

These axes are independent.

## Canonical protocol descriptor

`protocol.yaml` names the schemas that constitute the current protocol package and explicitly requires neutrality from:

- subject implementation;
- publication owner implementation;
- provider;
- repository layout;
- runtime.

A protocol release tag identifies the contracts on that commit. The concrete `mind@0x0sky` context present on the same commit remains an instance, not protocol ontology.

Merging protocol development into `master` is not itself a release. Tags and GitHub Releases remain separate explicitly authorized publication actions.

## Identity split

Prior releases used `schema/identity.schema.json` both as semantic Identity and as a repository resource envelope. That coupled the universal concept to `schema_version`, a validation-file path, and repository-local asset paths.

`0.6.0-rc.1` separates those responsibilities.

### Universal Identity

[`../../schema/identity.schema.json`](../../schema/identity.schema.json) defines only the canonical semantic value:

```yaml
type: person
id: 0x0sky
display_name: 0x0sky
```

It has no GitHub fields, repository path, validation path, storage contract, runtime state, or provider binding.

Optional visual identity uses semantic mark metadata and an opaque `asset_ref`. Asset resolution belongs to a concrete mind implementation and is deliberately deferred to a later `0.6` RC.

Full semantics are defined in [`IDENTITY.md`](IDENTITY.md).

### Concrete identity resource

[`../../schema/identity-resource.schema.json`](../../schema/identity-resource.schema.json) defines the envelope used by a mind repository to carry one Identity value.

For `mind@0x0sky`, [`../../identity/identity.yaml`](../../identity/identity.yaml) is that concrete resource. CI independently validates the embedded value against the universal Identity schema and requires its `type/id` to equal `mind.subject` exactly.

## Instance naming

The canonical concrete-instance convention is:

```text
mind@{subject.id}
```

Therefore the root manifest of this repository is `mind@0x0sky`, not a generic `mind` template.

The `master` branch is the living instance branch. A long-lived parallel generic branch is intentionally avoided because it would create a second ontology capable of drifting from released protocol contracts.

## Relationships and provider projections

The authored relationship and provenance model introduced in `0.5` remains intact. `0.6.0-rc.1` does not change relationship schema or reciprocal-confirmation semantics.

Canonical relationship entity ids remain provider-independent. The current organization relationship is `organization:aiaiaiai`; the GitHub namespace `aiaiaiai-org` is provider metadata.

`public_organizations` remains a legacy GitHub-facing compatibility projection. Its values are provider logins and therefore must not be treated as canonical organization ids merely because strings happen to match. Until an explicit provider-binding resource exists, CI validates canonical authored relationship semantics independently from that legacy provider projection.

## Visual identity

`0.6.0-rc.1` establishes the abstraction boundary first.

A later `0.6` RC should:

- publish real canonical marks for at least one person and one organization;
- define an implementation-level asset resolver for opaque `asset_ref` values;
- prove deterministic renderer fallback;
- decide whether `avatar` is canonical Identity, an asset slot, or presentation-only data;
- keep palette, typography, marketing voice, portrait systems, and brand semantics outside universal Identity unless independently justified.

## Migration from 0.5

A concrete `0.5` mind adopting this line should:

1. keep manifest schema `2` unless its manifest shape changes;
2. adopt the `0.6` protocol version it actually implements;
3. expose a concrete instance name `mind@{subject.id}`;
4. treat `schema/identity.schema.json` as universal Identity rather than a resource envelope;
5. carry the value through `schema/identity-resource.schema.json` or an equivalent protocol-conformant resource binding;
6. validate embedded Identity `type/id` against `mind.subject`;
7. keep provider and repository bindings outside the universal Identity value;
8. bump the concrete context version when its durable published representation changes.

## Acceptance gate for `0.6.0-rc.1`

The development candidate is internally acceptable when:

- `protocol.yaml` and every published JSON Schema validate;
- `mind@0x0sky` validates as a concrete implementation of the neutral Identity contract;
- relationship authority and reciprocal-confirmation invariants remain green;
- provider login strings are not promoted into universal Identity semantics;
- regression tests cover correctness-critical validators;
- protocol documentation changes trigger contract CI.

Consumer conformance is a later `0.8` gate, not a prerequisite for merging this protocol line. Publishing a tag or GitHub Release remains a separate action requiring explicit release authorization.
