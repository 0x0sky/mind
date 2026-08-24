# Abstract baseline

Mind Protocol `0.4` preserves an explicit neutral baseline without making that baseline a second source of protocol truth.

An abstract mind is a protocol template, not a concrete identity. It therefore uses explicit placeholder authority:

```yaml
mind:
  name: mind
  kind: abstract
  context_version: 0.0.0
  subject:
    type: unspecified
    id: unspecified
  owner:
    type: unspecified
    id: unspecified

modules:
  required: []
  registered: []
  catalog: {}

loading:
  default: []
  optional: []
```

The empty module graph is valid only because an abstract baseline does not claim to describe a real subject. A concrete personal, organization, agent, project, or product mind must declare a real subject and publication owner, and must require the `identity` module.

This distinction prevents two opposite failures:

- forcing personal or organization content into the reusable baseline;
- weakening concrete minds so they can omit identity or publish under `unspecified` authority.

The long-term baseline should be reproducibly derived from a released protocol contract. The historical `foundation/baseline-v0.1.0` branch remains useful history, but it is not the authority for modern protocol semantics.

`0.4` keeps the abstract form representable so baseline extraction can evolve without breaking the protocol. `0.8` is the planned milestone for formal baseline generation and conformance fixtures.
