# identity

`0x0sky` is the canonical public software identity represented by this mind.

The identity is centered on software engineering, architecture, public systems, and authorship. The canonical GitHub account is [github.com/0x0sky](https://github.com/0x0sky).

This module answers **who this mind describes**. Publication authority is declared separately by `mind.owner` in the root manifest so future agent, project, and product minds can distinguish their subject from the person or organization that publishes them.

## Machine-readable identity

[`identity.yaml`](identity.yaml) is the typed machine-readable identity resource for this module.

Its `identity.type` and `identity.id` must exactly match `manifest.yaml -> mind.subject`. The resource is validated by [`../schema/identity.schema.json`](../schema/identity.schema.json) through the module's `resources.identity` declaration.

The current identity resource intentionally contains only durable identity facts:

- identity type;
- stable identity id;
- display name;
- optional canonical visual identity.

Provider metadata such as a current GitHub avatar may enrich a renderer, but it does not become canonical identity data unless this mind explicitly declares it.

## Visual identity

`visual_identity` is optional in Mind Protocol `0.4`.

When present, `primary_mark` identifies the canonical mark for the subject:

```yaml
identity:
  visual_identity:
    primary_mark:
      kind: emblem
      asset:
        path: identity/assets/mark.svg
        media_type: image/svg+xml
      alt: 0x0sky
```

`primary_mark` is intentionally broader than `logo`:

- organizations and products may use `logo`;
- people may use `emblem`, `monogram`, or `signature`;
- AI agents may use `emblem` or `glyph`;
- the vocabulary is shared so consumers do not need identity-type-specific hacks.

The mark must reference a repository-local versioned asset. `avatar`, `portrait`, responsive variants, palette, typography, and full brand-system semantics are intentionally deferred beyond the first `0.4` contract.

## Handles

[`handles.md`](handles.md) records durable public handles and naming context that are useful to human readers.

Handles are presentation/discovery context. They do not replace the stable `identity.id`.

## Related nodes

- [`knowledge`](../knowledge/README.md) describes durable models accumulated by the identity;
- [`engineering`](../engineering/README.md) describes how the identity builds software;
- [`writing`](../writing/README.md) describes the public creative register.
