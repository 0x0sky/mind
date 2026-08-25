# Modules

`manifest.yaml` is the registration authority for this concrete Mind.

The personal Identity module is normalized under `modules/identity/`, matching the concrete organization-Mind layout. Existing authored personal modules retain their historical repository paths unless a separate migration changes them; folder placement does not define protocol semantics.

Current registered modules:

- `identity` → `modules/identity/module.yaml`
- `relationships` → `relationships/module.yaml`
- `knowledge` → `knowledge/module.yaml`
- `engineering` → `engineering/module.yaml`
- `systems` → `systems/module.yaml`
- `writing` → `writing/module.yaml`

Each module owns one responsibility, declares dependencies explicitly, and must not duplicate another module's canonical content.

Vendored schemas are consumed from the exact release locked by `protocol.lock.yaml`; this repository does not define module or resource schema semantics.

<!-- © 2026 aiaiaiai · aiaiaiai.org -->
