# Mind Protocol 0.6

Status: **`0.6.0-rc.1` staged next-version candidate**

`0.6` separates canonical protocol semantics from any one concrete identity implementation before the visual-identity contract is exercised with real assets.

This branch is intentionally staged on top of the current `0.5` work. Stable `0.5.0` remains a prerequisite for releasing `0.6.0-rc.1`; the next line must not erase the unfinished consumer-conformance gate of the previous line.

## Two entry points

Mind now exposes two explicit machine entry points with different authority:

- [`../../protocol.yaml`](../../protocol.yaml) — implementation-independent protocol descriptor;
- [`../../manifest.yaml`](../../manifest.yaml) — one concrete mind instance.

For this repository, `master` is the living canonical instance **`mind@0x0sky`**.

`protocol.yaml` is not an abstract mind instance and does not invent an `unspecified` identity. It describes the contracts that any compatible concrete mind may implement.

## Version model

| Version | Staged reference | Meaning |
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

## Identity split

Prior releases used `schema/identity.schema.json` both as semantic Identity and as a repository resource envelope. That coupled the universal concept to `schema_version`, a validation-file path, and repository-local asset paths.

`0.6.0-rc.1` separates those responsibilities:

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

## Relationships

The `0.5` authored relationship and provenance model remains intact. `0.6.0-rc.1` does not change relationship schema or confirmation semantics.

`public_organizations` remains a legacy compatibility projection until the `0.5` consumer migration is completed and its deprecation can be handled explicitly.

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
2. adopt the released `0.6` protocol version;
3. expose a concrete instance name `mind@{subject.id}`;
4. treat `schema/identity.schema.json` as universal Identity rather than a resource envelope;
5. carry the value through `schema/identity-resource.schema.json` or an equivalent protocol-conformant resource binding;
6. validate embedded Identity `type/id` against `mind.subject`;
7. keep provider and repository bindings outside the universal Identity value;
8. bump the concrete context version when its durable published representation changes.

## Release gate for 0.6.0-rc.1

Before this candidate can be released:

- stable `0.5.0` must be complete;
- `protocol.yaml` and every referenced contract must validate;
- `mind@0x0sky` must validate as a concrete implementation of the neutral Identity contract;
- current consumers must either parse the changed identity resource contract or have an explicit compatibility boundary;
- no provider or repository-layout assumption may leak back into universal Identity.
