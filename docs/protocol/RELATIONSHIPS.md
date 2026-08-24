# Relationships and provenance

Mind Protocol `0.5` treats a relationship as a canonical assertion involving the subject of one mind, not as a globally authoritative fact owned by a central graph.

## Canonical shape

```yaml
id: member-of-example
predicate: member_of
source:
  type: person
  id: alice
target:
  type: organization
  id: example
direction: directed
provenance:
  kind: authored
  authority:
    type: person
    id: alice
confirmation:
  state: asserted
```

## Invariants

A canonical authored relationship:

1. has a stable id within the publishing mind;
2. involves `mind.subject` as either source or target;
3. names `mind.owner` as its authorship authority;
4. uses provider-independent entity references;
5. carries explicit direction;
6. carries explicit confirmation state;
7. never treats provider discovery as authorship.

These rules let each mind remain sovereign while still composing into a larger graph.

## Predicates

Predicates use lowercase protocol vocabulary.

`0.5` standardizes only the predicate needed for the existing migration: `member_of`.

`member_of` is directed: `source --member_of--> organization`. The target must be `type: organization`.

Other predicates may be carried by the schema so protocol experiments do not require a root-manifest change, but consumers must not invent semantics for an unknown predicate. New protocol-wide predicate meanings should be documented before they become interoperability requirements.

## Direction

`directed` means source and target have semantic roles.

`symmetric` means the relationship itself is unordered. Source and target still exist so the serialized form remains deterministic, but a consumer must not infer an arrow from their order.

## Provenance layers

Canonical mind resources use `kind: authored`. Authored means the publishing mind intentionally asserts the relationship. `authority` identifies the entity accountable for that publication and must equal `mind.owner`.

Provider-derived relations are observations made by an integration or consumer, such as GitHub organization membership, repository ownership, social follows, or directory membership. They do not belong in canonical authored `relationships.yaml`.

A renderer may display them, but it must preserve that they are derived and must not silently materialize them back into the mind.

## Confirmation

`asserted` means only this canonical mind's authored claim is represented. It does not mean the relationship is false or disputed.

`reciprocal` means the counterpart canonical mind independently publishes a matching semantic relationship. The local confirmation object references the counterpart entity and the counterpart mind's local relationship id.

The two repositories do not need to coordinate one global relationship id. Provider-derived evidence cannot satisfy reciprocal confirmation.

## Relationship authority

A mind may assert a relationship when its own subject is one endpoint.

It must not publish a canonical relationship between two unrelated external entities. That would turn a subject-owned mind into an accidental global authority.

## Legacy GitHub projection

The root `public_organizations` field exists temporarily for older consumers. For a `0.5` mind that adopts authored relationships, each populated legacy entry must be backed by `subject --member_of--> organization`.

The legacy field does not become canonical relationship authority. Omission, empty-list, and populated-list semantics remain unchanged while legacy consumers exist.

## Consumer merge policy

A consumer may see both authored and provider-derived representations of the same semantic edge. It should preserve each evidence source, prefer authored data for canonical meaning, use provider-derived data as enrichment, never convert derived evidence into reciprocal confirmation, and avoid rendering duplicate edges when multiple evidence sources describe the same relationship.

Deduplication is a presentation concern; provenance must remain recoverable after deduplication.

## Provider ids

Provider-specific identifiers belong to integration evidence. GitHub numeric ids, installation ids, repository node ids, API URLs, and provider-specific membership record ids must not become universal relationship identity.

Protocol relationship ids and entity refs remain provider-independent.
