# identity

This module implements the canonical Identity contract for the subject of `mind@0x0sky`.

The distinction matters:

- [`../schema/identity.schema.json`](../schema/identity.schema.json) defines **Identity itself** and is implementation-independent;
- [`identity.yaml`](identity.yaml) is the concrete identity resource published by this mind instance;
- [`../schema/identity-resource.schema.json`](../schema/identity-resource.schema.json) defines only the resource envelope used to carry that value inside a mind repository.

## mind@0x0sky

The concrete subject is:

```yaml
identity:
  type: person
  id: 0x0sky
  display_name: 0x0sky
```

The embedded `identity.type` and `identity.id` must exactly match `manifest.yaml -> mind.subject`.

This repository's `master` branch is the living canonical `mind@0x0sky` instance. The fact that the protocol contracts are authored and released from the same repository does not make `0x0sky` part of the universal Identity definition.

## Universal Identity boundary

The canonical Identity value may describe a:

- person;
- organization;
- agent;
- project;
- product.

The core contract contains semantic identity only. It does not contain provider account ids, GitHub-specific metadata, repository paths, validation paths, deployment information, model/runtime state, or storage implementation details.

Provider handles and discovery metadata may enrich a consumer, but they do not redefine the canonical identity.

## Visual identity

Visual identity semantically belongs to Identity, but asset storage does not.

When `visual_identity.primary_mark` is present, the universal contract uses an opaque `asset_ref` rather than a repository path or provider URL:

```yaml
identity:
  type: person
  id: example
  display_name: Example
  visual_identity:
    primary_mark:
      kind: emblem
      asset_ref: primary-mark
      alt: Example
```

The concrete mechanism that resolves `primary-mark` to an SVG, PNG, WebGPU texture, CDN object, or another representation belongs to the implementing mind and consumer contracts. `0.6.0-rc.1` establishes this boundary before real canonical marks are introduced later in the `0.6` line.

## Publication authority

Identity answers **who or what the subject is**. Publication authority is independent and remains declared by `manifest.yaml -> mind.owner`.

That distinction is required for cases such as an AI-agent subject whose canonical mind is published by an organization without pretending the agent owns the hosting account.

## Handles

[`handles.md`](handles.md) records durable public naming and discovery context useful to human readers. Handles never replace the stable provider-independent `identity.id`.

## Related modules

- [`relationships`](../relationships/README.md) owns authored relations and reciprocal confirmation;
- [`knowledge`](../knowledge/README.md) describes durable models accumulated by the subject;
- [`engineering`](../engineering/README.md) describes software practice;
- [`writing`](../writing/README.md) describes the public creative register.
