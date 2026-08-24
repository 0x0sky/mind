# Mind Protocol 0.5

Status: **`0.5.0-rc.1` prerelease candidate**

Mind Protocol `0.5` builds on the stable `0.4.0` foundation without changing the root manifest shape. Its purpose is to make authored relationships provider-independent, explicitly directional, provenance-aware, and confirmable without turning provider discovery into canonical truth.

Manifest schema remains `2`. This is intentional evidence that manifest shape, protocol semantics, and one concrete mind's context version are independent version axes.

## Entry point

A consumer still starts at `manifest.yaml`. Relationship semantics are discovered through the normal module catalog rather than a new root-manifest graph object.

## Version model

| Version | Current reference | Meaning |
| --- | --- | --- |
| Manifest schema | `2` | Shape of `manifest.yaml`. |
| Protocol | `0.5.0-rc.1` | Shared semantics implemented by compatible minds and consumers. |
| Context | `0.3.11` | Durable public context of this concrete `0x0sky` mind. |

The reference context is now `0.3.11`; context changes remain independent from manifest schema and protocol versions.

## Subject and publication owner

`mind.subject` remains the entity this mind describes and is authoritative about. `mind.owner` remains the entity accountable for publishing the repository.

Every authored relationship is validated against both boundaries: the subject must be one endpoint and `provenance.authority` must equal the publication owner.

## Relationship module

`0.5` introduces a typed `relationships` module with `schema/relationships.schema.json`.

Each relationship defines a local stable id, predicate, source, target, direction, authored provenance, and confirmation state. The full contract is documented in [`RELATIONSHIPS.md`](RELATIONSHIPS.md).

`relationship.id` is stable within the publishing mind, not a global provider id. `directed` uses `source -> target`; `symmetric` is semantically unordered. The `member_of` predicate used by the migration is directed and targets an organization.

## Provenance

Canonical `relationships.yaml` contains authored claims only. Its authority must match `mind.owner`.

Provider-discovered GitHub membership, repository ownership, social following, directory membership, and similar observations are derived integration data. Consumers may combine them with authored edges but must preserve provenance and must not materialize provider observations back into canonical authored resources.

## Confirmation

`confirmation.state` is `asserted` or `reciprocal`.

`asserted` means this mind publishes the claim without referencing an independently authored counterpart claim. `reciprocal` means the counterpart canonical mind independently publishes the same semantic relationship and is referenced by counterpart entity plus that mind's local relationship id.

Provider discovery alone never counts as reciprocal confirmation.

## `public_organizations` migration

`public_organizations` remains in manifest schema v2 during the `0.5` migration because current consumers already use it. Its historical omission, empty-list, and populated-list meanings remain unchanged.

The field contains GitHub organization logins and is therefore a provider-facing compatibility projection. Canonical `member_of` relationships use provider-independent entity ids. Those namespaces may differ: the current GitHub login `aiaiaiai-org` corresponds operationally to the organization whose canonical Mind entity id is `aiaiaiai`, but protocol 0.5 does not infer that correspondence from string shape.

The relationship validator therefore validates authored relationship semantics independently from `public_organizations`; exact string equality between a provider login and a canonical entity id is neither required nor sufficient to establish identity. A future provider-binding contract must make such mappings explicit.

## Provider boundary

Provider logins, numeric ids, installation ids, API URLs, avatar URLs, and provider-specific membership records stay at integration boundaries. Protocol-level entity references remain provider-independent even when a canonical id happens to match a GitHub slug.

## Module ownership

- `identity` owns the subject's identity;
- `relationships` owns authored relations and confirmation state;
- `systems` owns software-ecosystem structure and implementation boundaries;
- consumers own provider enrichment and projection.

This keeps the root manifest a composition contract rather than a graph database.

## Visual identity

The `visual_identity.primary_mark` foundation from `0.4` is unchanged. Real canonical visual assets remain the `0.6` milestone; `0.5` adds no palette, avatar, portrait, typography, or brand semantics.

## Migration from 0.4

A concrete `0.4.0` mind adopts `0.5.0-rc.1` by:

1. keeping `schema_version: 2`;
2. changing `protocol.version` to `0.5.0-rc.1`;
3. adding a `relationships` module only when the mind has authored relationship claims to publish;
4. declaring `schema/relationships.schema.json` for its typed relationship resource;
5. ensuring every canonical relationship involves `mind.subject`;
6. ensuring authored provenance authority matches `mind.owner`;
7. retaining `public_organizations` temporarily when legacy consumers still require it;
8. treating legacy GitHub logins and canonical entity ids as separate namespaces unless an explicit binding proves equivalence;
9. keeping provider-discovered relationships outside canonical authored resources;
10. bumping `mind.context_version` when the concrete mind actually publishes new durable relationship context.

## Gate for stable 0.5.0

`0.5.0` is not stable merely because the reference relationship schema validates.

The stabilization gate is:

- the personal reference mind publishes and validates canonical authored relationships;
- at least one organization mind independently publishes a matching relationship so reciprocal confirmation is exercised across two canonical minds;
- `mind-web` consumes canonical relationships while preserving authored versus provider-derived provenance;
- legacy `public_organizations` fallback remains deterministic during migration;
- reciprocal-reference semantics have no unresolved ambiguity;
- provider-specific ids remain outside the universal relationship resource.

Until those conditions hold, `0.5.0-rc.*` is the correct channel.
