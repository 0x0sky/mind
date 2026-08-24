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

`public_organizations` remains in the root manifest during the pre-1.0 migration because current consumers already understand it.

In the reference mind:

- canonical membership meaning is authored in `relationships/relationships.yaml`;
- the legacy field remains a GitHub-facing compatibility projection rather than relationship authority;
- provider logins need not equal canonical organization ids — for example `aiaiaiai-org` projects the canonical `organization:aiaiaiai` relationship;
- omission and `[]` keep their historical legacy-consumer meanings until the migration is completed explicitly.

Without an explicit provider-binding resource, CI must not infer canonical entity identity from provider login string equality. The protocol does not silently reinterpret the old field.

## Current authored relationships

The current resource publishes `0x0sky member_of`:

- `organization:aiaiaiai` — `reciprocal`; counterpart `aiaiaiai-org/mind` publishes local relationship `member-0x0sky` for the same canonical organization identity;
- `organization:0xda-market` — `asserted`;
- `organization:nilx-one` — `asserted`.

Reciprocity is recorded only where the counterpart canonical mind independently publishes the same semantic relationship. The GitHub membership view is not used as a substitute for that assertion.
