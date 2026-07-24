# engineering principles

## Correctness

- model the domain before selecting infrastructure;
- make invalid states difficult to represent;
- keep public contracts small and explicit;
- verify behavior before publication or deployment.

## Architecture

- dependency direction must remain visible;
- provider adapters must not leak into the core;
- one canonical source exists for each concept;
- irreversible operations require explicit authorization.

## Quality

- predictability over spectacle;
- readable code over clever code;
- mobile-first does not mean mobile-only;
- performance claims require measurement on real devices.
