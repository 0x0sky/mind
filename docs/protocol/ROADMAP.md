# Roadmap to Mind Protocol 1.0

This roadmap describes protocol stabilization, not a promise that every domain feature must exist before `1.0`.

The goal of `1.0` is a small, explicit contract that can represent and render personal, organization, and AI-agent identities without provider-specific hacks, repository-layout coupling, or hidden historical assumptions.

## 0.4 — readable protocol foundation

Status: **`0.4.0` stable contract**

Goals:

- separate manifest schema, protocol, and concrete context versions;
- make `mind.subject` explicit;
- distinguish subject from repository publication owner;
- retain `mind.kind` temporarily for current consumer compatibility;
- require `identity` for concrete minds;
- schema-validate module descriptors;
- allow typed machine-readable module resources;
- add the canonical identity resource;
- define optional `visual_identity.primary_mark`;
- preserve current `public_organizations` provenance semantics.

Stable `0.4.0` required a migrated personal reference mind, at least one migrated organization mind, and verified consumer compatibility. Those gates are satisfied.

## 0.5 — relationships and provenance

Status: **`0.5.0-rc.1` prerelease candidate**

Goals:

- generalize authored relationships beyond the GitHub-specific `public_organizations` field;
- define relationship identity, direction, provenance, and confirmation semantics;
- preserve provider-discovered relationships as derived data;
- provide an explicit migration path for `public_organizations` rather than silently changing its meaning;
- keep provider-specific identifiers at integration boundaries.

`0.5.0-rc.1` introduces a typed `relationships` module/resource while keeping manifest schema v2. The personal and `aiaiaiai-tech` minds now exercise reciprocal authored membership across independent canonical viewpoints.

Stable `0.5.0` still requires:

- `mind-web` to consume canonical relationships while preserving authored versus provider-derived provenance;
- deterministic legacy fallback during the `public_organizations` migration;
- no provider-specific identifier leakage into the universal relationship resource;
- no unresolved reciprocal-reference ambiguity.

No visual-system expansion is required for this milestone.

## 0.6 — Identity abstraction and canonical visual identity

Status: **`0.6.0-rc.1` staged next-version work; release blocked on stable `0.5.0`**

`0.6` first separates universal Identity from any concrete mind implementation. Real visual assets are built on that boundary rather than baked into repository semantics.

### RC1 — protocol / instance separation

Goals:

- introduce `protocol.yaml` as the implementation-independent protocol descriptor;
- make `schema/identity.schema.json` the canonical universal Identity value;
- separate concrete mind resource packaging into `schema/identity-resource.schema.json`;
- remove repository paths, validation paths, provider bindings, and runtime/storage assumptions from universal Identity;
- make `master` explicitly the living `mind@0x0sky` instance rather than a neutral template;
- establish `mind@{subject.id}` as the concrete-instance naming convention;
- keep protocol release version and instance context version independently meaningful;
- avoid a long-lived parallel generic branch that could drift from released protocol contracts.

Expected structural model:

```text
protocol.yaml                         neutral protocol authority
schema/identity.schema.json           universal Identity

master
└── mind@0x0sky                       concrete living instance
    ├── manifest.yaml
    └── identity/identity.yaml
        └── identity                  implements universal Identity
```

The universal Identity contract must remain readable without knowing GitHub, repository layout, a renderer, a database, a filesystem, or an AI runtime.

### Later 0.6 RC — real visual identity

Goals:

- exercise `primary_mark` with real canonical assets;
- migrate at least one personal identity and one organization identity;
- resolve opaque `asset_ref` values through an explicit concrete-mind asset contract;
- define deterministic renderer fallback behavior;
- decide whether `avatar` is a presentation slot or a canonical identity artifact;
- introduce variants only where actual renderer requirements justify them;
- keep palette, typography, and brand semantics separate from the universal identity mark.

Expected examples by the end of the line:

```text
person
└── primary_mark: emblem | monogram | signature

organization
└── primary_mark: logo | emblem
```

## 0.7 — AI-agent identity

Goals:

- create and validate at least one real `subject.type: agent` mind;
- verify an agent subject can have a different person or organization owner;
- define the boundary between an AI's canonical mark and any synthetic portrait;
- avoid implying biological personhood through the protocol model;
- verify renderers do not require a GitHub user or organization account for the subject itself.

Expected shape:

```text
agent
├── primary_mark: emblem | glyph
└── portrait?     later presentation capability
```

AI-specific behavior, model configuration, memory, prompts, and runtime state do not automatically belong to the universal identity contract.

## 0.8 — baseline and consumer conformance

Goals:

- define a reproducible neutral baseline derived from a released `protocol.yaml` contract set;
- stop treating an old long-lived foundation branch as the source of protocol truth;
- add conformance fixtures for person, organization, agent, project, and product minds;
- verify at least two independent consumers or consumer modes against the same fixtures;
- publish explicit supported protocol ranges;
- make baseline extraction deterministic enough that instance content cannot leak into a fork template.

The neutral baseline is an artifact of a protocol version, not a parallel ontology or branch that can drift away from the canonical protocol descriptor.

## 0.9 — compatibility freeze

Goals:

- resolve all known field naming ambiguity;
- decide the final future of compatibility-only `mind.kind`;
- remove or formally deprecate pre-1.0 aliases with migration notes;
- freeze identity, module, resource, provenance, and loading semantics;
- define forward-compatibility rules for unknown optional modules/resources;
- define the minimum compatibility policy for `1.x`.

No new major concept should enter the root manifest after this point without evidence that it is protocol-wide.

## 1.0 — stable Mind contract

`1.0` is ready when a new human, AI agent, or renderer can deterministically answer:

- Which protocol contract am I implementing?
- Is this data universal protocol semantics or one concrete mind instance?
- What subject does this mind describe?
- Who owns or publishes it?
- What context version is published?
- Which modules must I load?
- Where are their descriptors and typed resources?
- Which facts are canonical and which may be provider-derived?
- What are the visibility and privacy boundaries?
- How do I represent the subject visually when a canonical mark exists?
- How do I safely ignore optional capabilities I do not implement?

Required identity coverage:

- personal identity with a canonical mark;
- organization identity with a canonical logo or emblem;
- AI-agent identity with a canonical emblem or glyph and independently declared publication owner.

Required engineering properties:

- universal Identity has no repository/provider/runtime coupling;
- machine schemas and human documentation agree;
- conformance validation catches subject drift, broken resources, dependency cycles, and missing assets;
- current consumers have a documented migration path;
- provider-specific systems remain integrations, not protocol authority;
- no canonical concept depends on `mind-web`, GitHub UI behavior, or one AI vendor.

## Non-goals for 1.0

The following may evolve independently after `1.0` and do not block the core protocol:

- full corporate brand systems;
- typography and marketing voice;
- rich portrait systems;
- animation and 3D renderer semantics;
- AI runtime/model configuration;
- private memory or conversation archives;
- provider-specific repository enrichment;
- product-specific domain models.

Keeping those concerns outside the core is part of reaching `1.0`, not missing it.
