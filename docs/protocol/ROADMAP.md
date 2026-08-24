# Roadmap to Mind Protocol 1.0

This roadmap tracks **protocol stabilization only**. Concrete personal minds, organization minds, agent minds, named visual assets, provider bindings, product renderers, and ecosystem rollouts are separate implementation concerns.

The north star is a small implementation-independent contract for typed identity, context, relationships, provenance, visual identity references, resource loading, compatibility, and deterministic conformance.

## Version axes

Mind keeps four independent version axes:

- `protocol.version` — shared semantics and contracts;
- manifest `schema_version` — machine shape of one concrete manifest;
- concrete `mind.context_version` — durable content version of one implementation;
- resource schema versions — machine contracts of typed resources.

A protocol release never implies a concrete context release, and a concrete context change never implies a protocol release.

## 0.4 — readable protocol foundation

Status: **stable**

Delivered explicit subject/owner semantics, typed module resources, manifest schema v2, and the first universal visual-identity reference shape.

## 0.5 — relationships and provenance

Status: **accepted semantics carried forward**

Delivered authored relationship direction, provenance, reciprocal confirmation, and a provider-independent canonical relationship boundary.

Provider discovery remains derived evidence rather than canonical authorship.

## 0.6 — Identity and canonical visual contract

Status: **`0.6.0` stable source contract**

Delivered universal Identity/resource separation, deterministic canonical visual-asset resolution and failure semantics, independent protocol/context versioning, and migration documentation.

Real logos and marks for named identities remain separate implementation work.

## 0.7 — agent identity semantics

Status: **`0.7.0` stable source contract**

### `0.7.0-rc.1`

Status: **merged**

Delivered a synthetic first-class agent conformance case proving:

- person, organization, and agent share the same universal Identity contract;
- agent subject and publication owner may differ without requiring distinct ownership;
- no provider account is required;
- model, prompt, memory, runtime, tools, and execution state remain outside universal Identity;
- biological-personhood assertions remain outside universal Identity;
- synthetic/generated portraits remain presentation-only by default;
- canonical agent emblem/glyph support remains available through the existing visual contract.

### `0.7.0`

Stable source-contract gate:

- agent conformance fixture green;
- subject/owner boundary documented and tested;
- universal Identity remains runtime/provider independent;
- no schema specialization for agent identity;
- full protocol CI green;
- stable promotion introduces no semantic delta beyond RC1.

Tag/GitHub Release publication remains separately authorized.

## 0.8 — neutral baseline and conformance

Next protocol milestone: **`0.8.0`**.

Protocol work:

- generate a neutral baseline deterministically from released protocol contracts;
- prevent concrete instance data from leaking into that baseline;
- provide synthetic/generic fixtures for person, organization, agent, project, and product;
- publish a machine-runnable conformance suite;
- publish a protocol feature matrix;
- define machine-readable supported protocol ranges;
- verify at least two independent consumers or consumer modes;
- define unknown optional capability handling.

Consumers prove interoperability; they never become protocol authority.

## 0.9 — compatibility freeze

Freeze the public compatibility surface before `1.0`:

- resolve compatibility-only fields;
- remove or formally deprecate pre-1.0 aliases;
- freeze Identity, resource-envelope, relationships/provenance, loading/module discovery, and visual-reference semantics;
- define unknown optional-capability forward compatibility;
- define minimum `1.x` compatibility policy;
- define the supported pre-1.0 migration floor;
- prohibit new root-manifest concepts without protocol-wide evidence.

## `1.0.0-rc.1` — final protocol release candidate

Prove the frozen contract exactly as intended to ship:

- clean-checkout full conformance;
- clean neutral-baseline generation;
- all required synthetic identity-type fixtures;
- visual resolution/failure fixtures;
- supported pre-1.0 migrations;
- unknown optional-capability behavior;
- no named-identity dependency;
- no required provider dependency.

## `1.0.0` — stable Mind Protocol

The first compatibility-guaranteed protocol must provide:

- implementation-independent Identity;
- explicit subject and publication owner;
- typed versioned resources;
- authored-vs-derived provenance;
- deterministic relationship semantics;
- deterministic visual identity reference and failure semantics;
- privacy/visibility boundaries;
- deterministic loading and module discovery;
- optional-capability forward compatibility;
- provider-agnostic core;
- machine-readable supported version range;
- reproducible neutral baseline;
- public conformance suite.

Required synthetic fixture coverage:

- person;
- organization;
- agent;
- project;
- product.

Release artifacts include the versioned contract set, release notes, migration guide, conformance suite, neutral baseline artifact, and compatibility policy.

Tags and GitHub Releases are separate publication actions.

## Non-goals for 1.0

The core protocol does not require:

- a full corporate brand system;
- typography or marketing voice;
- rich portrait systems;
- animation or 3D renderer semantics;
- AI model configuration;
- AI prompts, memory, or runtime state;
- private conversation archives;
- provider-specific repository enrichment;
- deployment topology;
- migration of every existing named identity;
- forcing every repository, project, or product to become a sovereign mind.
