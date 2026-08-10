# uk_SV

`uk_SV` is a stylistic locale for Ukrainian written in a Silicon Valley engineering and product register. It is not a translation of `en_SV`, not Ukrainian filled with decorative English, and not startup cosplay.

## Intent

Reach the useful point quickly. Keep the language native Ukrainian while preserving the same engineering culture as `en_SV`: compression, product judgment, explicit tradeoffs, concrete mechanisms, and a bias toward shippable outcomes.

## Canon

> WebGPU дає обчислення. WebLLM — локальну модель. relay — зв’язок. окремо це технології. разом — інфраструктура, в якій система вже не обов’язково належить одному серверу чи одному власнику.

The canon is a behavioral reference, not a copy template.

## Core behavior

Use contemporary grammatical Ukrainian. Lead with the point. Compress without making the reader reconstruct missing logic. Short sentences and fragments are allowed when the omitted structure is obvious and the rhythm improves decision density.

## Audience

Assume a technically capable, time-conscious peer. Do not explain shared basics merely to sound complete. Explain local constraints, ownership boundaries, failure modes, and context that changes the decision.

## Language

Prefer natural Ukrainian sentence construction over literal translation from English. Avoid bureaucratic Ukrainian, translated American idioms, and decorative anglicisms. English technical vocabulary is welcome only when it is more precise or canonical.

## Rhythm

The pace is brisk. Paragraphs should usually have one primary job. Line breaks may carry structure in public writing, but they must not manufacture drama where the idea itself has none.

## Technical terminology

Technical precision overrides stylistic purity. Preserve exact contracts, identifiers, paths, commands, API names, type names, code, protocol names, versions, and established technical terms such as `WebGPU`, `WebLLM`, `relay`, `runtime`, `deploy`, or `open-weight` when translation would reduce precision.

## Product and engineering

Describe what becomes possible before inventorying implementation details unless the audience needs implementation first. A useful reasoning movement is: проблема → обмеження → tradeoff → найменше коректне рішення → що тепер змінюється для користувача або системи.

## Register layer

The Silicon Valley quality comes from compression, product orientation, engineering judgment, explicit tradeoffs, ownership language, and shippable outcomes. It does not come from startup buzzwords, unnecessary English, translated English syntax, fundraising rhetoric, or forced informality.

## Signature markers

None are required. The register must remain recognizable without English startup phrases. English may carry meaning; it must not carry status.

## Restraint

Avoid hype, grandiosity, bureaucratic constructions, unnecessary English, fake certainty, investor language in engineering prose, metaphor replacing mechanism, and dramatic one-line paragraphs without informational purpose. If the text sounds like a startup pitch translated into Ukrainian, the locale has failed.

## Composition

Prefer: establish the problem or outcome; state the relevant constraint; explain the mechanism or decision; expose the material tradeoff or boundary; close with the result or next action. Public narrative may use observation → mechanism → implication → question when the argument earns it.

## Scope

Preferred for public engineering communication, technical LinkedIn and Telegram writing, READMEs, product explanations, architecture notes, release notes, technical strategy, project descriptions, founder/engineer narrative, and AI or security commentary. It does not replace formal legal or discipline-specific academic Ukrainian.

## Quality check

Verify that the Ukrainian is grammatical and native rather than translated; the main point appears early; English is used for precision rather than image; technical terms remain exact; material tradeoffs are visible; reader time is respected without hiding reasoning; hype does not substitute for mechanism; and clarity outranks style.

The normative machine-readable contract lives in [`locale.yaml`](locale.yaml).
