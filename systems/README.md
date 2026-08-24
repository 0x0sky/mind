# systems

Systems are public implementations governed by the [`engineering`](../engineering/README.md) contract.

This module records durable software-ecosystem structure and system boundaries. Canonical identity-to-identity relationship claims belong to the [`relationships`](../relationships/README.md) module instead of being duplicated here.

## Boundaries

- `mind` stores durable public context;
- `relationships` owns authored entity relationships and their provenance;
- `mind-web` reads and visualizes compatible mind context;
- project and product repositories own their implementation truth and README files;
- provider-discovered memberships remain derived integration data;
- deployment credentials and private state remain outside this repository.

See [`ecosystem.md`](ecosystem.md) for the human-readable ecosystem boundary and references to the canonical relationship sources.
