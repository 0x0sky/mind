# Identity contract

Mind Protocol treats **Identity** as a universal semantic value, not as a GitHub account, repository, profile document, runtime object, or one concrete mind implementation.

The canonical machine contract is [`../../schema/identity.schema.json`](../../schema/identity.schema.json).

## Identity is not Mind

The layers are deliberately separate:

```text
Identity                         who / what the subject is
Mind Protocol                    how compatible minds publish structured truth
mind@subject                     one concrete sovereign implementation
publication owner                who is accountable for publishing that instance
provider bindings                derived/integration mapping to GitHub, social systems, etc.
```

A person, organization, agent, project, or product may implement the same Identity contract without sharing repository layout, provider, runtime, renderer, or storage.

## Canonical value

The universal value contains:

```yaml
identity:
  type: person | organization | agent | project | product
  id: stable-provider-independent-id
  display_name: Human readable name
```

The `identity:` key above is the resource-envelope field used by a concrete mind. The canonical Identity value itself is the mapping inside it.

### `type`

Classifies the semantic subject. It is not a hosting-account type and must not be inferred from GitHub user/organization metadata.

### `id`

Stable identifier chosen by the identity's canonical context. Provider numeric ids, installation ids, API URLs, account database ids, and transient aliases do not belong here.

### `display_name`

Canonical human-readable name. A provider may expose a different display label without changing the identity value.

## Visual identity

Visual identity remains semantically owned by Identity. Storage and rendering remain implementation concerns.

The universal contract therefore uses an opaque `asset_ref`:

```yaml
visual_identity:
  primary_mark:
    kind: emblem
    asset_ref: primary-mark
    alt: Example
```

`asset_ref` identifies a canonical asset semantically. It is not a repository path, CDN URL, provider avatar URL, filesystem location, or renderer texture handle.

A later `0.6` contract may define how a concrete mind resolves that reference to versioned assets. That resolver must not change the meaning of Identity itself.

## Concrete resource envelope

A mind repository may wrap the Identity value in a resource envelope for versioning and validation:

```yaml
schema_version: 1
identity:
  type: person
  id: 0x0sky
  display_name: 0x0sky
validation:
  schema: schema/identity-resource.schema.json
```

The envelope belongs to the Mind repository contract. It is **not** part of universal Identity.

For every concrete mind, the embedded Identity `type` and `id` must exactly match `manifest.yaml -> mind.subject`.

## mind@subject

The canonical naming convention for a concrete instance is:

```text
mind@{subject.id}
```

Examples:

```text
mind@0x0sky
mind@aiaiaiai-tech
mind@magi
```

This is an instance name, not the identity id itself.

## Publication ownership

`mind.subject` identifies the Identity represented by the instance. `mind.owner` identifies the entity accountable for publishing the repository.

They may be the same:

```text
subject: person:0x0sky
owner:   person:0x0sky
```

or intentionally different:

```text
subject: agent:magi
owner:   organization:aiaiaiai-tech
```

This prevents hosting implementation from being confused with biological personhood, legal ownership, or autonomous infrastructure ownership.

## Provider boundary

Provider mappings are integrations. They may resolve an identity to:

- a GitHub login;
- an organization membership;
- a social handle;
- a profile avatar;
- a repository namespace;
- a runtime account.

Those mappings may provide evidence or presentation data, but they do not modify the canonical Identity value unless the canonical mind explicitly authors a semantic change.

## Invariant

A consumer that understands the Identity contract must be able to parse the same identity value without knowing:

- which Git host stores its mind;
- whether a repository exists at all;
- which renderer displays it;
- which AI model consumes it;
- which database or filesystem stores assets;
- whether the subject is represented by a user account, organization account, service account, or no provider account.

That is the abstraction boundary introduced by the `0.6` line.
