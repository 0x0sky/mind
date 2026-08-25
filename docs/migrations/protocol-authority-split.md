# Protocol authority split: `0x0sky/mind` → concrete consumer

This migration removes Mind Protocol authority from `0x0sky/mind` after that authority is moved to `aiaiaiai-org/mind-protocol`.

## Source state

- source repository: `0x0sky/mind`
- source master used for protocol history import: `48a81df7d8e9818d9c01f3e1fe5ac663af29a006`
- co-located protocol candidate before split: `1.0.0-rc.1`
- concrete subject: `person:0x0sky`
- personal context version: `0.4.0`

## Destination role

After this migration, `0x0sky/mind` is canonical only for `person:0x0sky` and is not Mind Protocol authority, release authority, bootstrap authority, or a concrete-Mind template.

The current canonical protocol authority is `aiaiaiai-org/mind-protocol`.

## Protocol binding during the split

A concrete consumer may bind only to an immutable published release. Because `1.0.0-rc.1` is not yet published from the new canonical protocol repository, this migration keeps `mind@0x0sky` on the already published `0.9.0` contract set.

The two provenance dimensions are deliberately distinct:

- current protocol authority: `aiaiaiai-org/mind-protocol`;
- historical `0.9.0` release source: `0x0sky/mind@v0.9.0`;
- exact historical release commit: `457844c8ced0318d91d628617ff6f8ec6f428ab7`.

The `v0.9.0` tag and release are not copied into the new authority repository. Historical publication provenance remains immutable and truthful. The first formal protocol release from `aiaiaiai-org/mind-protocol` is intended to be `v1.0.0-rc.1`.

The repository will join the same `1.0.0-rc.1` compatibility-canary sync as the organization Minds after that prerelease is formally published.

## Preserved authored context

The migration preserves the existing personal modules and their authored content:

- relationships;
- knowledge;
- engineering;
- systems;
- writing;
- `.assistant` environment contracts.

No personal facts are invented or removed as part of the repository-role split.

## Identity normalization

The Identity value remains exactly:

```yaml
identity:
  type: person
  id: 0x0sky
  display_name: 0x0sky
```

Only its repository layout and documentation are normalized to the organization-Mind pattern:

`identity/` → `modules/identity/`

The GitHub login remains provider/discovery context and does not replace the provider-independent canonical id.

Because the durable semantic Identity and other authored personal context do not change, `mind.context_version` remains `0.4.0`.

## GitHub repository topology

A concrete Mind is an independent consumer repository. It is not intended to remain in the fork network of another concrete Mind and it must not be attached to `aiaiaiai-org/mind-protocol` as a GitHub fork. Protocol linkage is represented by immutable release provenance and `protocol.lock.yaml`, not fork ancestry.

Existing fork-network metadata is cleaned up only after all four concrete consumers are structurally normalized and green. That cleanup is a separate manual GitHub repository action.

## Removed source-authority surfaces

The concrete repository no longer carries protocol-development/release surfaces such as protocol docs, bootstrap/release builders, protocol regression tests, or the release workflow. It retains only the exact vendored release contracts and consumer validators needed to prove its own conformance.

<!-- © 2026 aiaiaiai · aiaiaiai.org -->
