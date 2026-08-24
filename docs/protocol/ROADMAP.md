# Roadmap to Mind Protocol 1.0

This roadmap tracks **protocol stabilization only**. Concrete personal minds, organization minds, agent minds, named visual assets, provider bindings, product renderers, and ecosystem rollouts are separate implementation concerns.

The north star is a small implementation-independent contract for typed identity, context, relationships, provenance, visual identity references, resource loading, compatibility, and deterministic conformance.

## Version axes

Mind keeps independent version axes for protocol semantics, descriptor/manifest shapes, concrete context, and typed resource schemas. A protocol release never implies a concrete context release, and a concrete context change never implies a protocol release.

## 0.4 — readable protocol foundation

Status: **stable**

Delivered explicit subject/owner semantics, typed module resources, manifest schema v2, and universal visual-reference shape.

## 0.5 — relationships and provenance

Status: **accepted semantics carried forward**

Delivered authored relationship direction, provenance, reciprocal confirmation, and provider-independent canonical relationship identity.

## 0.6 — Identity and canonical visual contract

Status: **`0.6.0` stable source contract**

Delivered universal Identity/resource separation, deterministic canonical visual resolution/failure semantics, and independent protocol/context versioning.

## 0.7 — agent identity semantics

Status: **`0.7.0` stable source contract**

Delivered first-class agent Identity through the same universal schema, subject/owner independence, and explicit runtime/personhood/portrait boundaries.

## 0.8 — neutral baseline and conformance

Status: **`0.8.0` stable source contract**

Delivered:

- protocol descriptor schema `v2` with discoverable conformance policy;
- deterministic generated neutral baseline rather than a long-lived generic ontology;
- dynamic tests preventing concrete `mind@0x0sky` data from leaking into the baseline;
- synthetic fixture descriptors for person, organization, agent, project, and product;
- explicit deterministic expected result for every required fixture;
- a machine-runnable conformance suite and feature matrix;
- suite and per-consumer support range `[0.8.0, 0.9.0)`;
- two independent consumer modes (`schema` and `minimal`) over the same fixture set;
- both modes preserving authored provenance and rejecting derived evidence from canonical authored relationships;
- both modes resolving a valid canonical visual mark and reporting integrity failure deterministically;
- explicit unknown optional-module and required-module behavior in both modes;
- repeated-run regression proof that consumer outputs are reproducible;
- neutral protocol schema `$id` namespace rather than reference-repository GitHub URLs.

Acceptance evidence:

- neutral baseline generation is byte-for-byte deterministic;
- all five required fixture types validate;
- fixture and probe results are reproducible;
- both independent consumer modes pass the declared suite;
- reference-instance content is rejected from the generated baseline;
- supported protocol ranges are machine-readable.

Consumers prove interoperability; they never become protocol authority.

## 0.9 — compatibility freeze

Next protocol milestone: **`0.9.0`**.

Freeze the public compatibility surface before `1.0`:

- resolve compatibility-only fields, especially the future of `mind.kind` and `public_organizations`;
- remove or formally deprecate pre-1.0 aliases with migration notes;
- freeze Identity, resource-envelope, relationships/provenance, loading/module discovery, visual-reference, baseline, and conformance semantics;
- define unknown optional-capability forward compatibility beyond modules where justified;
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

The first compatibility-guaranteed protocol must provide implementation-independent Identity, explicit subject/owner, typed versioned resources, authored-vs-derived provenance, deterministic relationship and visual semantics, privacy/visibility boundaries, deterministic loading, optional-capability forward compatibility, provider-agnostic core, machine-readable supported range, reproducible neutral baseline, and a public conformance suite.

Required synthetic fixture coverage remains person, organization, agent, project, and product.

Tags and GitHub Releases are separate publication actions.

## Non-goals for 1.0

The core protocol does not require a full corporate brand system, typography/marketing voice, rich portraits, animation/3D semantics, AI runtime configuration, private conversation archives, provider-specific enrichment, deployment topology, migration of every named identity, or forcing every project/product into a sovereign mind.
