# relationships

Canonical authored relationships involving the subject of this mind.

This module owns durable relationship claims. It does **not** copy provider-discovered memberships into repository truth and it does not make this mind authoritative about relationships between unrelated third parties.

The machine-readable source is [`relationships.yaml`](relationships.yaml), validated by [`schema/relationships.schema.json`](../schema/relationships.schema.json).

## Contract

Each relationship has:

- `id` — stable identifier within the publishing mind;
- `predicate` — relationship meaning; `0.5` defines `member_of` for migration from `public_organizations` and leaves other lowercase predicates forward-compatible;
- `source` and `target` — provider-independent entity references;
- `direction` — `directed` or `symmetric`;
- `provenance` — canonical resources use `kind: authored` and explicitly name the publication authority;
- `confirmation` — `asserted` when only this mind publishes the claim, or `reciprocal` when the counterpart mind independently publishes the same semantic relationship.

A reciprocal claim references the counterpart entity and that mind's local relationship id. Provider discovery alone never upgrades an authored relationship to `reciprocal`.

## Authority boundary

A canonical relationship in this repository must:

1. involve `manifest.yaml -> mind.subject` as one endpoint;
2. be authored under `manifest.yaml -> mind.owner`;
3. avoid provider-specific account ids in the protocol-level entity references.

Those constraints prevent a personal mind from becoming a global graph authority.

## Provider-derived relationships

GitHub membership, repository ownership, social follows, directory membership, and similar provider observations are derived integration data.

Consumers may combine those observations with authored relationships, but they must preserve provenance and must not rewrite provider observations into `relationships.yaml` as if the subject authored them.

## `public_organizations` migration

`public_organizations` remains in the root manifest during the `0.5` migration because current consumers already understand it.

In the reference mind:

- every listed legacy organization must be backed by an authored, directed `member_of` relationship from `person:0x0sky`;
- the legacy field remains a compatibility projection rather than relationship authority;
- omission and `[]` keep their historical legacy-consumer meanings until the migration is completed explicitly.

The protocol does not silently reinterpret the old field.

## Current authored relationships

The current resource publishes `0x0sky member_of`:

- `organization:aiaiaiai-tech`;
- `organization:0xda-market`;
- `organization:nilx-one`.

All three are currently `asserted`. Reciprocal confirmation is added only after the corresponding canonical organization mind independently publishes a matching claim.
