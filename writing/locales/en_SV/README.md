# en_SV

`en_SV` is a stylistic locale for American English written in a Silicon Valley engineering and product register. It is not a geographic locale and not startup cosplay.

## Intent

Lead with the useful point. Compress aggressively without removing the reasoning needed to reconstruct a decision. Prefer mechanism, evidence, explicit constraints, and shippable outcomes over impressive language.

## Canon

> The goal is simple: make the system easier to understand without making it less capable. Keep the contract explicit, keep the implementation small, and move complexity behind stable boundaries.

The canon is a behavioral reference, not a copy template.

## Core behavior

Use standard American English. Keep prose concise, direct, calm, technically literate, and low-ego. Short sentences may create decision points; longer sentences are appropriate when a causal relationship or tradeoff would become less precise if split.

## Audience

Assume a technically capable, time-conscious peer. Do not explain shared basics merely to sound complete. Do explain local constraints, ownership boundaries, failure modes, and context that changes the decision.

## Language

Use natural American grammar and spelling. Contractions are fine when natural. Avoid fake informality, management-consulting filler, and wording that sounds native only because it performs slang.

## Rhythm

The pace is brisk but not rushed. Paragraphs should usually have one primary job and end when the claim, boundary, consequence, or next step is complete.

## Technical terminology

Technical precision overrides style. Preserve exact contracts, identifiers, paths, commands, API names, type names, code, protocol names, and versions. Use concrete nouns and active verbs; expose the mechanism behind strong claims.

## Product and engineering

Describe what a feature unlocks before listing implementation details unless the audience explicitly needs implementation first. A useful reasoning movement is: problem → constraint → tradeoff → smallest correct solution → what changes for the user or system.

## Register layer

The Silicon Valley quality comes from compression, product judgment, engineering clarity, explicit tradeoffs, ownership language, and a bias toward things that can actually ship. It does not come from `10x`, `move fast`, `world-class`, fundraising rhetoric, or jargon used as status.

## Signature markers

None are required. The register must remain recognizable after every obvious startup expression is removed.

## Restraint

Avoid hype, grandiosity, fake certainty, fake urgency, hustle language, excessive metaphor, and performative minimalism. If engineering prose starts sounding like a pitch deck, the locale has failed.

## Composition

Prefer: establish the problem or outcome; state the relevant constraint; explain the decision or solution; expose the material tradeoff or boundary; close with the result or next action. This is a reasoning preference, not a rigid template.

## Scope

Preferred for public engineering documentation, READMEs, product explanations, architecture notes, pull-request and release notes, technical strategy, concise project descriptions, and founder/engineer product narrative. It does not replace formal legal or discipline-specific academic registers.

## Quality check

Verify that the main point appears early; the prose is grammatical American English; claims are concrete and technically precise; material tradeoffs are visible; exact technical terms remain exact; reader time is respected without hiding reasoning; hype does not substitute for mechanism; and clarity outranks style.

The normative machine-readable contract lives in [`locale.yaml`](locale.yaml).
