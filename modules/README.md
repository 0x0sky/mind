# modules

A module is a focused, replaceable unit of context composed into a concrete mind.

## Interface

Each `module.yaml` is validated by [`../schema/module.schema.json`](../schema/module.schema.json) and declares:

- `id` — stable unique identifier;
- `purpose` — one responsibility;
- `stability` — `stable`, `transient`, or `archived`;
- `dependencies` — explicit module identifiers;
- `entrypoints` — canonical human- or machine-readable files loaded by consumers;
- `owner` — entity responsible for the module;
- `visibility` — public or private handling expectations;
- optional `resources` — typed machine-readable data owned by the module.

## Machine-readable resources

A resource lets a module expose structured data without adding module-specific fields to the root manifest.

```yaml
module:
  id: identity
  resources:
    identity:
      path: identity/identity.yaml
      format: yaml
      schema: schema/identity.schema.json
```

Each resource declares:

- a repository-relative `path`;
- its serialization `format` (`yaml` or `json`);
- a repository-relative JSON Schema.

Mind CI validates the resource against its declared schema. This keeps the root manifest focused on composition while allowing modules to evolve typed contracts independently.

The identity resource is the first protocol-defined resource. Future modules may add their own resources without making those domain semantics global to every mind.

## Rules

- A module must have one reason to change.
- A module must not duplicate another module's canonical content.
- Dependencies must resolve to registered module IDs.
- Self-dependencies and dependency cycles are forbidden.
- Every declared entrypoint must exist inside the repository.
- Every declared resource and resource schema must exist inside the repository.
- Optional consumers must be able to ignore optional modules safely.
- Concrete implementations may choose any folder names; registration belongs in `manifest.yaml`.
- Module-specific data belongs in typed resources instead of new root-manifest fields unless the concept is genuinely protocol-wide.

## Example registration

```yaml
modules:
  registered:
    - identity
    - engineering
  catalog:
    identity: identity/module.yaml
    engineering: engineering/module.yaml
```

The root manifest registers modules; each module descriptor owns its local interface and resources.
