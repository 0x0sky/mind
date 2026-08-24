# Migrating to Mind Protocol 0.9.0

Mind Protocol `0.9.0` is the compatibility-freeze line before `1.0.0`. The principal migration is manifest schema `v2` → `v3`.

The supported stable migration floor is `0.6.0`.

## Supported source lines

Direct supported stable sources:

- `0.6.0`;
- `0.7.0`;
- `0.8.0`.

A source below `0.6.0` fails deterministically and must use an earlier documented migration path first.

## Manifest v3 changes

Manifest schema `v3` removes two compatibility fields:

```text
mind.kind
public_organizations
```

Older aliases such as `organizations`, `memberships`, and `public_organization` are also forbidden.

### `mind.kind`

`mind.kind` duplicated information already carried by `mind.subject.type`.

Before removal, a migrator must verify the legacy pair is consistent:

```text
abstract      -> unspecified
personal      -> person
organization  -> organization
agent         -> agent
project       -> project
product       -> product
```

If the legacy classification disagrees with `mind.subject.type`, migration fails instead of guessing which value is authoritative.

After migration, `mind.subject.type` is the only canonical subject classification.

### `public_organizations`

`public_organizations` was a GitHub/provider-facing projection. Provider logins are not canonical organization IDs and therefore do not belong in the provider-agnostic root manifest.

Before removing a non-empty projection, preserve the intended meaning in one of these places:

- canonical relationship resources when the relationship and canonical entity ID are known;
- an explicit provider integration when the data remains provider evidence rather than authored canonical identity.

The migrator never converts a provider login into a canonical organization ID automatically.

For the concrete `mind@0x0sky` instance in this repository, the organization relationships represented by the historical projection already exist in `relationships/relationships.yaml`; therefore the root projection can be removed without losing canonical relationship semantics.

## Context version

A protocol packaging migration does **not** by itself change `mind.context_version`.

Keep the existing context version unless the concrete mind's durable authored content independently changes.

## Automated migration

Use:

```bash
python scripts/migrate_manifest_v2_to_v3.py path/to/manifest.yaml
```

When a non-empty provider projection has already been preserved outside the root manifest, assert that fact explicitly:

```bash
python scripts/migrate_manifest_v2_to_v3.py \
  path/to/manifest.yaml \
  --provider-projection-preserved
```

To write a new file:

```bash
python scripts/migrate_manifest_v2_to_v3.py \
  path/to/manifest.yaml \
  --provider-projection-preserved \
  --output path/to/manifest.v3.yaml
```

The flag does not perform or infer provider-to-canonical mapping. It is an explicit migration assertion that preservation has already happened.

## Compatibility after migration

`0.9.0` freezes these rules before `1.0`:

- `module` is the capability-negotiation unit;
- unknown optional modules may be ignored only when not requested;
- unknown required modules are rejected;
- unknown default-loaded modules are rejected;
- unknown root-manifest fields are rejected;
- compatible future additions belong in optional modules or versioned optional resources;
- breaking core changes require a future major protocol version once the `1.x` compatibility promise begins.

## Verification

After migration, run the implementation's equivalent of:

```bash
python scripts/validate_manifest.py --manifest path/to/manifest.v3.yaml
```

A complete Mind Protocol implementation should also run the public conformance suite against its publication.
