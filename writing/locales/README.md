# stylistic locales

Stylistic locales are versionable writing contracts that combine a language base with a deliberate authorial register.

They are not replacements for standard language or regional locale identifiers. A stylistic locale exists to make a repeatable voice explicit enough for humans, AI systems, and other tooling to apply it without flattening the writing into a generic tone preset.

## Structure

Each locale lives in its own directory under `writing/locales/`:

```text
writing/locales/
└── <locale-id>/
    ├── locale.yaml
    └── README.md
```

The directory name is the canonical locale identifier.

- `locale.yaml` is the normative, machine-readable contract;
- `README.md` is the human-readable specification, rationale, canon, and examples.

The locale identifier is not repeated in filenames because the directory already owns the namespace.

## Naming

Locale identifiers follow the shape `<language>_<register>`.

The language component should use the shortest stable language identifier that is already meaningful in context. The register component names the deliberate authorial or cultural register and is not required to correspond to an ISO region code.

For example, `uk_SP` means Ukrainian with the Saint-Petersburg register defined by that locale. It does not claim that `SP` is a standard Ukrainian regional locale. Likewise, `en_SV` means American English with the Silicon Valley register defined by that locale; `SV` is a register identifier, not a standardized territory code.

## Discovery

Every first-level directory under `writing/locales/` is a locale candidate. A valid locale must contain both `locale.yaml` and `README.md`.

The `writing` module exposes this README as the stable discovery entrypoint. Individual locales are discovered from the directory structure and must not be enumerated in `writing/module.yaml`.

This keeps the module contract stable as the number of locales grows.

## Contract model

A locale should define, at minimum:

- identity and human-readable name;
- base language;
- register and intent;
- scope and exclusions;
- casing and punctuation rules;
- rhythm and syntax;
- preferred and restricted lexical behavior;
- treatment of technical terminology;
- restraint rules that prevent caricature;
- canonical examples;
- quality gates for generated or edited text.

The machine-readable contract may grow with new fields as long as its meaning remains explicit and backward-compatible where practical.

## Language versus locale

`writing/language.md` defines the broad roles languages play across the writing system. A stylistic locale is narrower: it defines how one specific register behaves when selected.

Language answers which linguistic system carries the text. Locale answers how that text is voiced.

## Inheritance and fallback

A stylistic locale inherits the grammatical and semantic rules of its declared base language unless it explicitly narrows presentation behavior.

A locale must never weaken correctness in order to preserve character. When a locale rule conflicts with grammatical correctness, factual precision, safety, or an explicit technical contract, correctness wins.

If a locale does not define a behavior, consumers should fall back to the base language and then to the surrounding document or product contract. They must not invent additional stylistic markers.

## Restraint

A locale is a voice contract, not a costume.

Distinctive markers should be sparse enough that the register remains recognizable through rhythm, syntax, pacing, and lexical judgment even when no signature phrase appears. Repetition that turns a register into parody is a contract failure.

## Canon

Canonical examples belong in each locale's README. They are evidence of intended behavior, not templates to be mechanically copied.

Current canonical locales:

- [`uk_SP`](uk_SP/README.md) — Ukrainian with a restrained Saint-Petersburg intonation;
- [`en_SV`](en_SV/README.md) — American English with a Silicon Valley engineering register.
