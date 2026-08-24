# Mind Protocol 0.8

Status: **`0.8.0` stable source contract**

`0.8` makes protocol interoperability reproducible without turning any concrete mind or product consumer into protocol authority. It adds a machine-readable conformance suite, a deterministic neutral baseline, five synthetic identity-type fixtures, explicit support-range metadata, and two consumer modes.

The accepted Identity, relationship/provenance, canonical visual-asset, and agent boundaries from `0.4`–`0.7` remain unchanged.

## Machine entry points

- [`../../protocol.yaml`](../../protocol.yaml) — implementation-independent protocol descriptor, now descriptor schema `v2`;
- [`../../conformance.yaml`](../../conformance.yaml) — machine-readable conformance suite and feature matrix;
- [`../../manifest.yaml`](../../manifest.yaml) — the concrete living `mind@0x0sky` instance, not protocol baseline;
- [`BASELINE.md`](BASELINE.md) — generated neutral baseline semantics.

## Version model

| Version | Stable reference | Meaning |
| --- | --- | --- |
| Protocol descriptor schema | `2` | Adds discoverable conformance/baseline/compatibility policy. |
| Manifest schema | `2` | Concrete manifest shape remains unchanged. |
| Protocol | `0.8.0` | Shared conformance and baseline semantics. |
| Concrete instance context | independent | Durable content version of one implementation. |
| Conformance suite schema | `v1` | Machine fixture/feature/range/mode contract. |
| Identity schema | `v1` | Universal Identity for all five subject types. |

## Conformance suite

[`../../conformance.yaml`](../../conformance.yaml) publishes:

- synthetic fixture descriptors for `person`, `organization`, `agent`, `project`, and `product`;
- a protocol feature matrix;
- supported protocol range `[0.8.0, 0.9.0)`;
- `schema` and `minimal` consumer modes;
- unknown-module compatibility behavior;
- the generated-baseline contract.

The fixtures are synthetic and provider-independent. They contain no named real-world identity or required provider account.

## Two consumer modes

[`../../scripts/validate_conformance.py`](../../scripts/validate_conformance.py) proves the same fixture set through two intentionally different paths:

- `schema` — JSON Schema validation plus universal Identity-envelope validation;
- `minimal` — a small core reader that does not use JSON Schema or shared semantic validators.

Both must accept a registered unknown optional module when it is not requested and reject an unknown required/default-loaded module.

These are independent consumer **modes**, not a claim that one repository contains two independent products. Product-level cross-consumer verification may add stronger evidence later; consumers still never become protocol authority.

## Neutral baseline

The baseline is generated from the protocol contract set. It is not maintained manually and is not a generic branch. CI requires deterministic output, a valid abstract manifest, and zero leakage of concrete root-instance identifiers.

See [`BASELINE.md`](BASELINE.md).

## Schema namespace

`0.8` removes historical `github.com/0x0sky/mind` JSON Schema identifiers from the manifest, module, and relationship contracts. Published schema `$id` values now use the neutral `aiaiaiai.org/mind/schema/...` protocol namespace.

Repository-relative schema/resource paths may still exist in concrete publication envelopes; that packaging concern is intentionally distinct from protocol identity.

## Compatibility

Machine-readable policy for this line is:

```text
supported range:          >= 0.8.0 and < 0.9.0
unknown optional module:  ignore when not requested
unknown required module:  reject
```

The broader `1.x` compatibility guarantee and pre-1.0 migration floor remain the `0.9` freeze milestone.

## Publication boundary

A merged `0.8.0` source contract does not itself create a Git tag or GitHub Release. Release publication remains separate and explicitly authorized.
