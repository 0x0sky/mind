# Roadmap to Mind Protocol 1.0

This roadmap tracks **protocol stabilization only**. Concrete personal minds, organization minds, agent minds, named visual assets, provider bindings, product renderers, and ecosystem rollouts are separate implementation concerns.

The north star is a small implementation-independent contract for typed identity, context, relationships, provenance, visual identity references, resource loading, compatibility, and deterministic conformance.

Formal publication policy is defined in [`RELEASE_POLICY.md`](RELEASE_POLICY.md).

## Version axes

Mind keeps independent version axes for protocol semantics, descriptor/manifest shapes, concrete context, and typed resource schemas. A protocol release never implies a concrete context release, and a concrete context change never implies a protocol release.

Published schema identities are versioned independently from protocol releases. When one schema shape intentionally survives across the `0.9.0` → `1.0.0-rc.1` → `1.0.0` train, release-specific version/lifecycle bindings belong in semantic validation rather than forcing byte changes under the same `$id`.

## 0.4 — readable protocol foundation

Status: **stable source milestone**

Delivered explicit subject/owner semantics, typed module resources, manifest schema v2, and universal visual-reference shape.

## 0.5 — relationships and provenance

Status: **accepted semantics carried forward**

Delivered authored relationship direction, provenance, reciprocal confirmation, and provider-independent canonical relationship identity.

## 0.6 — Identity and canonical visual contract

Status: **`0.6.0` stable source milestone**

Delivered universal Identity/resource separation, deterministic canonical visual resolution/failure semantics, and independent protocol/context versioning.

No retroactive formal GitHub Release is planned for `0.6.0`.

## 0.7 — agent identity semantics

Status: **`0.7.0` stable source milestone**

Delivered first-class agent Identity through the same universal schema, subject/owner independence, and explicit runtime/personhood/portrait boundaries.

No retroactive formal GitHub Release is planned for `0.7.0`.

## 0.8 — neutral baseline and conformance

Status: **`0.8.0` stable source milestone**

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

`0.8.0` remains a source milestone and will not be retroactively promoted into the first formal release.

## 0.9 — compatibility freeze

Current protocol milestone: **`0.9.0`**.

`0.9.0` is the **first formal GitHub Release**.

Freeze the public compatibility surface before `1.0`:

- remove `mind.kind` in favor of the canonical `mind.subject.type`;
- remove `public_organizations` from the provider-agnostic root manifest;
- preserve organization semantics through canonical relationships or provider integrations before migration;
- use manifest schema `v3` as the frozen pre-1.0 root shape;
- freeze Identity, resource-envelope, relationships/provenance, loading/module discovery, visual-reference, baseline, conformance, and compatibility contracts;
- freeze exact published schema contents through machine-validated fingerprints;
- keep release numbers and lifecycle states out of reusable schema bytes when the same `$id` is intended to survive the release train;
- enforce exact protocol version, lifecycle state, and migration-source binding semantically;
- keep `module` as the capability negotiation unit;
- reject unknown root-manifest fields unless a future manifest schema revision explicitly introduces them;
- preserve forward compatibility through unknown optional modules that are not requested;
- reject unknown required/default-loaded modules;
- define the `1.x` compatibility policy;
- support migration from stable protocol lines beginning at `0.6.0`;
- prohibit provider-login-to-canonical-id inference;
- prohibit new root-manifest concepts without protocol-wide evidence.

Release gate:

- full CI green on the final release PR head;
- compatibility freeze/fingerprint validation green;
- supported migration suite green;
- dual-mode conformance green;
- reproducible neutral baseline green;
- final semantic review clean;
- tag `v0.9.0` points to the exact verified merge commit whose tree equals the tested PR-head tree;
- GitHub Release `Mind Protocol 0.9.0` is published with the required artifacts.

### After `0.9.0` publication — compatibility canaries

Once the exact `v0.9.0` artifact is published, a deliberately small set of existing concrete minds may synchronize to that release before `1.0.0-rc.1`.

This phase is for compatibility evidence only. It may exercise manifest/resource migration, exact protocol pinning, canonical-vs-provider identity boundaries, provenance, optional modules, and already-defined canonical visual behavior. It must not introduce a named identity, provider, renderer, or repository as protocol authority.

Any incompatibility found by a canary returns to the protocol release train as evidence for a reviewed fix or another RC decision. Full named identity, visual-family, provider-binding, agent, project/product, and ecosystem synchronization remains deferred until stable `1.0.0`.

## `1.0.0-rc.1` — final protocol release candidate

Publication: **GitHub prerelease**.

Prove the frozen contract exactly as intended to ship:

- clean-checkout full conformance;
- clean neutral-baseline generation;
- all required synthetic identity-type fixtures;
- visual resolution/failure fixtures;
- supported pre-1.0 migrations, including the formal `0.9.0` line;
- unknown optional-capability behavior;
- no named-identity dependency;
- no required provider dependency;
- no semantic drift from the frozen `0.9` surface except deliberately reviewed finalization required for `1.0`.

If a blocking semantic defect is found after `rc.1`, publish another RC instead of mutating the existing tag or silently changing the candidate.

## `1.0.0` — stable Mind Protocol

Publication: **first compatibility-guaranteed stable GitHub Release**.

The first compatibility-guaranteed protocol must provide implementation-independent Identity, explicit subject/owner, typed versioned resources, authored-vs-derived provenance, deterministic relationship and visual semantics, privacy/visibility boundaries, deterministic loading, optional-capability forward compatibility, provider-agnostic core, machine-readable supported range, reproducible neutral baseline, and a public conformance suite.

Required synthetic fixture coverage remains person, organization, agent, project, and product.

`1.0.0` should be a stable promotion of the accepted final RC contract. Semantic change after the final RC requires renewed review and conformance evidence.

## After `1.0.0` — full concrete identity rollout

Only after the compatibility-guaranteed stable protocol is published does the narrow canary phase expand into the full ecosystem identity rollout.

This separate implementation phase includes, as appropriate:

- canonical personal identity content;
- parent and child organization identities;
- agent identities;
- canonical named visual assets and the shared visual family;
- provider bindings;
- project and product identities where they are genuinely sovereign minds;
- synchronization into protocol consumers and ecosystem repositories.

Identity rollout **consumes** Mind Protocol `1.0`; named identities and their rollout state do not become protocol authority.

## Non-goals for 1.0

The core protocol does not require a full corporate brand system, typography/marketing voice, rich portraits, animation/3D semantics, AI runtime configuration, private conversation archives, provider-specific enrichment, deployment topology, migration of every named identity, or forcing every project/product into a sovereign mind.
