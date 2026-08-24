# Bootstrapping a concrete Mind

A concrete Mind is created from an **exact immutable Mind Protocol release**, not by copying the `mind@0x0sky` reference implementation from `master`.

## Canonical path

```text
Mind Protocol tag vX.Y.Z
        ↓
neutral protocol baseline
        ↓
subject + publication-owner semantics + Identity
        ↓
concrete mind@<subject.id>
```

The bootstrap path is intentionally boring: it copies the released protocol contract set, creates a minimal valid concrete manifest, adds the required Identity module/resource, and records an exact protocol lock. It does not copy personal relationships, knowledge, engineering context, handles, provider accounts, visual assets, or any other content from `mind@0x0sky`.

## Do not use a GitHub fork as a Mind template

Forking `0x0sky/mind` is valid for protocol development. It is not the canonical construction path for a new concrete Mind because `master` also contains the living `mind@0x0sky` implementation.

Changing `0x0sky` IDs in copied files is not migration or bootstrap. It is accidental identity inheritance.

## Bootstrap from a release tag

After a protocol version is formally published, check out that exact tag and run the bootstrap tool from that checkout.

Example for an organization:

```bash
git clone --branch v1.0.0 https://github.com/0x0sky/mind.git mind-protocol
cd mind-protocol

python scripts/bootstrap_mind.py \
  --output ../my-organization-mind \
  --source-tag v1.0.0 \
  --subject-type organization \
  --subject-id my-organization \
  --display-name "My Organization" \
  --context-version 0.1.0 \
  --repository-visibility public
```

Example where publication owner differs from the subject:

```bash
python scripts/bootstrap_mind.py \
  --output ../my-agent-mind \
  --source-tag v1.0.0 \
  --subject-type agent \
  --subject-id my-agent \
  --display-name "My Agent" \
  --owner-type organization \
  --owner-id my-organization \
  --context-version 0.1.0 \
  --repository-visibility private
```

If `--owner-type` and `--owner-id` are omitted, owner defaults to the subject. Supplying only one is rejected.

The `--source-tag` must exactly match the protocol version in the checked-out contract (`v{protocol.version}`). The CLI additionally proves all of the following before generating anything:

- the command is running inside the Mind Protocol Git checkout;
- the supplied tag exists locally;
- the checked-out `HEAD` resolves to exactly the same commit as that tag;
- `protocol.yaml`, `conformance.yaml`, `compatibility.yaml`, and `schema/` have no tracked local modifications relative to that tagged checkout.

A floating branch such as `master`, a branch commit that merely declares the same version string, or a locally modified released contract is therefore rejected as a concrete bootstrap source.

## Generated minimum

The output contains the minimum concrete publication surface:

```text
mind@<id>/
├── AGENTS.md
├── README.md
├── mind-repository.yaml
├── manifest.yaml
├── protocol.lock.yaml
├── protocol.yaml
├── conformance.yaml
├── compatibility.yaml
├── identity/
│   ├── module.yaml
│   └── identity.yaml
└── schema/
    └── exact released protocol schemas
```

The generated repository metadata declares itself a **protocol consumer**, not protocol authority.

The generated `protocol.lock.yaml` records:

- exact protocol id/version;
- immutable release tag;
- floating-branch consumption as forbidden;
- Git blob fingerprints for the vendored protocol descriptor, conformance, compatibility, and schemas;
- the rule that the reference implementation is not a template.

## What bootstrap deliberately does not invent

Bootstrap does not create:

- relationships;
- organization hierarchy;
- provider/GitHub identities;
- handles;
- biography or descriptive facts beyond the supplied display name;
- governance, engineering, portfolio, knowledge, systems, or writing modules;
- logos or visual identity;
- AI model/runtime configuration.

Those are added only when genuinely authored for the new subject and only through the appropriate protocol module/resource contracts.

A provider login must never be inferred as a canonical identity ID merely because a repository is hosted by that provider.

## Context version

`mind.context_version` is explicit bootstrap input because it belongs to the concrete authored publication, not to the protocol release.

Protocol `1.0.0` can therefore be consumed by concrete contexts `0.1.0`, `2.4.3`, or another independently managed version. Protocol tags do not become concrete-context tags.

## RC usage

A prerelease such as `v1.0.0-rc.1` may be used for compatibility canaries after that prerelease is formally published. It should not be treated as the stable `1.x` compatibility guarantee.

The same bootstrap mechanism is used; the exact prerelease tag is supplied as `--source-tag`, and the checkout proof applies identically.

## Verification

The protocol repository regression suite verifies that bootstrap:

- produces a valid manifest schema v3 concrete Mind;
- requires the Identity module;
- binds Identity type/id to the manifest subject;
- preserves distinct subject/publication-owner semantics;
- creates no `mind@0x0sky` content in the generated concrete publication;
- rejects a `HEAD` that differs from the named release tag;
- rejects tracked modifications to the released protocol contract set;
- records exact release consumption rather than floating `master`;
- leaves protocol schemas unchanged.

See [`../REPOSITORY_MODEL.md`](../REPOSITORY_MODEL.md) for the authority model and [`BASELINE.md`](BASELINE.md) for the abstract neutral baseline.

<!-- © 2026 aiaiaiai · aiaiaiai.org -->
