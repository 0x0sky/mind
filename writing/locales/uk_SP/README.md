# uk_SP

`uk_SP` is a stylistic locale for Ukrainian written with a restrained Saint-Petersburg intonation.

It is an authorial register, not a standard regional locale and not an attempt to imitate Russian through Ukrainian vocabulary. The Saint-Petersburg layer lives primarily in pacing, distance, sentence architecture, and manner of address.

## Intent

The voice is reflective, civil, slightly old-fashioned, and technically literate. It should feel as though the speaker has enough distance from the subject to observe it before judging it.

The register is designed for internal notes and reflections about personal projects, engineering practice, systems, and creative work. It is not the default public voice.

## Canon

> звольте бачити: дивлюсь я на свій mind.* — і, знаєте, ніяк не позбудуся думки переосмислити рутину dev у гру. ось зробити це захопливим і зрозумілим рішуче усім — задача, батеньку, не з простих, даруйте.

The canon demonstrates the register rather than serving as a reusable template.

## Core behavior

### Casing

All prose uses lowercase, including the first word of a sentence. Existing technical identifiers, product names, code, acronyms, and quotations preserve their canonical spelling when changing them would damage meaning.

### Opening distance

A note may open with a courteous framing phrase such as `звольте бачити` or `дозвольте зауважити` when that distance is useful.

These openings are optional. They must not become a compulsory prefix.

### Address

Words such as `батеньку` and `даруйте` may appear as light internal punctuation inside a thought. They should not be used as decoration, stacked together, or placed mechanically at the beginning and end of every passage.

### Rhythm

The preferred rhythm is measured and unhurried. A sentence is allowed to inspect its own thought before resolving it.

Dashes are used as reflective pauses rather than as ornamental separators. Short sentences may interrupt a longer movement when the thought genuinely changes direction.

### Punctuation

Exclamation marks are avoided. Emotional force should come from syntax, choice of detail, and cadence rather than typographic volume.

Question marks remain available when the sentence is actually interrogative. Colons and semicolons may be used where they improve structural clarity.

### Vocabulary

The base language is Ukrainian. Surzhyk is not part of the register.

Established project and engineering terms such as `dev`, `mind.*`, identifiers, protocol names, and API vocabulary remain unchanged when translation would reduce precision or erase the local technical language of the project.

The Saint-Petersburg quality is carried by intonation, not by importing Russian grammar or vocabulary into Ukrainian text.

### Engineering language

Technical precision has priority over stylization.

Contracts, identifiers, paths, commands, API names, type names, code, and other exact engineering objects must remain exact. The surrounding prose may carry the locale; the engineering object itself must not be distorted to sound literary.

## Restraint

`uk_SP` must remain recognizable without relying on signature words.

A successful passage can omit `звольте бачити`, `батеньку`, and `даруйте` entirely and still preserve the register through distance, pacing, syntax, and judgment.

If every sentence advertises the style, the style has failed.

Avoid:

- caricature or theatrical nineteenth-century imitation;
- faux-Russian Ukrainian;
- surzhyk;
- diminutives used for charm;
- emoji;
- exclamation marks;
- excessive archaism;
- repeated signature phrases;
- decorative complexity that obscures the actual thought.

## Composition

A typical `uk_SP` note follows a loose movement rather than a rigid template:

1. establish the object of attention;
2. create a small amount of reflective distance;
3. examine the actual tension, contradiction, or engineering problem;
4. resolve the thought plainly, without a dramatic conclusion.

The structure may be shorter whenever the thought does not require all four movements.

## Scope

Preferred uses:

- internal project notes;
- engineering reflections;
- observations about `mind.*` and related systems;
- short essays about one's own work;
- private or semi-private authorial notes where this register is explicitly selected.

Not intended as:

- the default voice for public documentation;
- user-facing product copy;
- formal engineering specifications;
- an automatic translation target;
- a replacement for standard Ukrainian.

## Quality check

Before accepting a passage as `uk_SP`, verify that:

- the prose is grammatically Ukrainian;
- lowercase presentation is preserved where appropriate;
- the pace is calm and reflective;
- technical terms remain precise;
- signature phrases are sparse and motivated;
- no surzhyk, emoji, diminutive sentimentality, or exclamation marks appear;
- the voice remains legible without its most obvious markers;
- style never takes priority over meaning.

The normative machine-readable contract lives in [`locale.yaml`](locale.yaml).