# Agent Identity

Mind Protocol treats an **agent** as a first-class Identity subject, not as a provider account, model process, hosting runtime, synthetic person, or special repository type.

The canonical machine contract remains [`../../schema/identity.schema.json`](../../schema/identity.schema.json). There is deliberately no separate `agent.schema.json`.

## Same Identity contract

An agent uses the same universal value shape as every other supported subject type:

```yaml
type: agent
id: synthetic-agent
display_name: Synthetic Agent
```

The `agent` value classifies the semantic subject. It does not imply a particular AI vendor, inference system, autonomy level, hosting account, model family, or user interface.

## Subject and publication owner

The subject described by a mind and the entity accountable for publishing it are independent references.

A synthetic conformance case may therefore state:

```yaml
mind:
  subject:
    type: agent
    id: synthetic-agent
  owner:
    type: organization
    id: synthetic-publisher
```

This proves that an agent can be published by a different entity. It does **not** require distinct ownership: a conformant implementation may use the same subject and owner when that is semantically correct.

Publication ownership is not biological parenthood, model ownership, provider tenancy, or legal personhood unless a separate domain contract explicitly says so.

## Runtime boundary

Universal Identity does not carry agent execution configuration. The following remain outside it:

- model or model-provider configuration;
- system prompts or instruction sets;
- memory stores or conversation history;
- runtime/process state;
- tool permissions;
- execution state;
- hosting-account identifiers;
- provider-account identifiers.

Those concerns may be represented by future optional capabilities or implementation-specific modules when independently justified. They do not become Identity merely because the subject is an agent.

## Personhood boundary

`type: agent` does not assert that the subject is biologically human. The protocol also does not encode a field such as `biological_person` to negate or affirm personhood.

This is a schema boundary, not a claim about consciousness, legal status, moral status, or social treatment. Those questions are outside the universal Identity contract.

## Visual boundary

An agent may author a canonical mark using the same visual contract as other identities, for example an emblem or glyph referenced through opaque `asset_ref`.

A portrait is different. A generated or synthetic portrait is presentation data by default and does not become canonical Identity simply because it depicts the agent.

Therefore:

- canonical emblem/glyph: allowed through `visual_identity.primary_mark`;
- provider avatar: derived/presentation evidence;
- generated portrait: presentation capability by default;
- portrait bytes or generation configuration: not universal Identity.

## Synthetic conformance fixture

[`../../tests/fixtures/agent_identity/`](../../tests/fixtures/agent_identity/) contains a deliberately synthetic agent and publication owner. It must not acquire a real provider login, named organization, runtime dependency, or model configuration.

The fixture proves only protocol semantics:

- `agent` validates through the shared Identity schema;
- embedded Identity binds to `mind.subject`;
- publication owner may differ;
- provider/runtime/personhood/portrait fields do not leak into universal Identity.

This fixture is conformance evidence, not a concrete agent mind implementation.
