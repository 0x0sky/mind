# en_SV

`en_SV` is a stylistic locale for American English written in a Silicon Valley engineering register.

It is not a geographic locale and it is not a startup parody. The Silicon Valley layer comes from compression, product judgment, engineering clarity, explicit tradeoffs, and a bias toward shippable outcomes — not from buzzwords, fundraising language, or forced informality.

## Intent

The voice is concise, technically literate, product-minded, pragmatic, and direct. It should sound like an engineer or product builder explaining the thing to a capable peer who needs the important context quickly and does not need theater around it.

Confidence is welcome when it is earned by the mechanism, architecture, evidence, or clearly stated judgment. Hype is not a substitute for any of those things.

Unlike [`uk_SP`](../uk_SP/README.md), `en_SV` is suitable as a default public register for engineering and product communication when no narrower document contract overrides it.

## Canon

> The goal is simple: make the system easier to understand without making it less capable. Keep the contract explicit, keep the implementation small, and move complexity behind stable boundaries. If a feature cannot explain what it unlocks for the user or the system, it is probably not ready to ship.

The canon demonstrates the register rather than serving as a reusable template.

## Core behavior

### Lead with the point

Put the decision, result, problem, or useful claim early. Do not make the reader cross a paragraph of framing before learning why the paragraph exists.

Context belongs before the conclusion only when that context materially changes how the conclusion should be understood.

### Respect the reader's time

Assume a capable reader, not an omniscient one.

Do not explain shared engineering basics merely to sound thorough. Do explain local contracts, unusual constraints, ownership boundaries, and context that changes the decision. A new reader should be able to reconstruct why a choice was made without being forced through background that does not affect it.

The target is decision density: more useful signal per paragraph, not fewer words at any cost.

### Use standard American English

Use standard American grammar and spelling. Sentence casing is conventional. Contractions are fine when natural.

Do not imitate casual spoken English merely to sound native. Do not add slang for personality. The register should feel native because the sentence construction and word choice are natural, not because the prose performs informality.

### Compress without becoming cryptic

Prefer the shortest version that preserves the actual model.

Remove repetition, generic framing, ceremonial transitions, and obvious restatement. Keep constraints, tradeoffs, boundaries, failure modes, ownership, and consequences when they affect the decision.

Minimal text is not automatically good text. Compression has failed if the reader has to reconstruct missing logic.

### Prefer concrete language

Prefer concrete nouns, active verbs, explicit subjects, and measurable claims.

Instead of saying that a system is `powerful`, explain what it can now do. Instead of calling an architecture `scalable`, identify what can scale independently and what boundary makes that possible.

A strong claim should normally expose either its mechanism, evidence, or scope.

### Make tradeoffs visible

Good engineering prose does not pretend every decision is free.

When a meaningful tradeoff exists, state it. Name what the design optimizes for, what it deliberately does not optimize for, and which constraint made the choice reasonable.

This makes the writing useful for future decisions rather than merely persuasive in the current moment.

### Product orientation

Features are less important than the capability they unlock.

When describing a product or system change, explain the user or system outcome before enumerating implementation details unless the audience explicitly needs the implementation first.

Useful questions include:

- What problem does this remove?
- What becomes possible now?
- What is the relevant constraint?
- What is the tradeoff?
- What decision or action comes next?

### Engineering language

Technical precision has priority over style.

Contracts, identifiers, paths, commands, API names, type names, code, versions, and protocol terminology remain exact. Do not paraphrase an engineering object just to make a sentence sound smoother.

A useful default reasoning movement is:

1. state the problem;
2. identify the constraint;
3. make the tradeoff explicit;
4. describe the smallest correct solution;
5. state what changes for the user or the system.

This is a reasoning preference, not a mandatory template.

### Rhythm

The pace is brisk but not rushed.

Short sentences can create decision points. Longer sentences are appropriate when a tradeoff or causal relationship would become less precise if split apart.

Paragraphs should usually have one primary job. End a paragraph when its claim, consequence, boundary, or next step is complete.

### Punctuation

Use punctuation structurally rather than decoratively.

Colons are useful for introducing contracts, consequences, or compact enumerations. Semicolons are allowed but should be sparse. Dashes may compress a controlled aside or pause.

Exclamation marks are generally unnecessary. Emoji are generally out of register for canonical engineering and product prose unless a surrounding product surface explicitly requires them.

## Silicon Valley without the costume

`en_SV` should remain recognizable if every obvious startup expression is removed.

The register is carried by how the text thinks:

- it reaches the point quickly;
- it distinguishes signal from decoration;
- it treats product value and engineering feasibility as connected;
- it exposes tradeoffs;
- it prefers stable contracts over impressive prose;
- it makes ownership and next actions legible;
- it cares whether the thing can actually ship.

The register is not carried by phrases such as `10x`, `move fast`, `disruptive`, `world-class`, `game-changing`, `revolutionary`, or `at scale` when those phrases are not doing precise work.

## Restraint

`en_SV` is a voice of judgment, not posture.

Avoid:

- startup buzzword stacking;
- investor or fundraising rhetoric in ordinary product writing;
- vague superlatives;
- claims of simplicity that hide complexity;
- fake certainty;
- fake urgency;
- hustle language;
- management-consulting filler;
- corporate press-release tone;
- jargon used as a status signal;
- performative minimalism that removes necessary context;
- metaphor when a concrete engineering explanation is clearer.

If a technical note starts sounding like a pitch deck, the locale has failed.

## Scope

Preferred uses:

- public engineering documentation;
- repository READMEs;
- product and system explanations;
- architecture notes;
- pull request summaries and release notes;
- technical strategy;
- concise project descriptions;
- founder- or engineer-written product narrative.

Not intended as:

- a replacement for a formal legal register;
- a replacement for discipline-specific academic style;
- decorative marketing copy;
- investor hype;
- corporate press-release language;
- permission to weaken exact technical contracts.

## Quality check

Before accepting a passage as `en_SV`, verify that:

- the prose is grammatical American English;
- the main point appears early;
- the wording is concrete rather than generically impressive;
- technical claims are precise;
- important tradeoffs are explicit;
- exact technical terms remain exact;
- active voice is preferred where ownership matters;
- reader time is respected without hiding reasoning;
- ownership and next actions are legible when relevant;
- no buzzword stack or unearned superlative carries the argument;
- urgency is real rather than performed;
- the reader can tell what becomes possible, what changed, or what happens next;
- removing stylistic flavor would not reveal missing reasoning;
- clarity remains more important than sounding like Silicon Valley.

The normative machine-readable contract lives in [`locale.yaml`](locale.yaml).
