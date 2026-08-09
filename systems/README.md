# systems

Systems are public implementations governed by the [`engineering`](../engineering/README.md) contract.

This module records durable system boundaries and declared identity-to-organization mappings. Detailed implementation documentation remains canonical in each repository.

## Boundaries

- `mind` stores public context;
- `mind-web` reads and visualizes that context;
- project and product repositories own their code and README;
- deployment credentials and private state remain outside this repository.

See [`ecosystem.md`](ecosystem.md) for the public identity and organization map.
