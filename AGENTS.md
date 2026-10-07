# AGENTS

## GitHub delivery

Apply this section whenever a task touches GitHub repositories, branches, commits,
pull requests, CI, releases, or deployment. Otherwise ignore it.

### Authority

Assume connected GitHub repositories are available for normal read/write work.
Inspect actual state before reporting an access limitation.

Proceed without additional confirmation for reversible repository actions,
including creating branches, editing files, committing and pushing, opening or
updating pull requests, commenting or reviewing, marking a pull request ready,
and merging when all merge conditions below are satisfied.

Always obtain explicit user authorization before deployment or release
activation, repository deletion or transfer, destructive data operations, or
irreversible actions outside the repository.

A merge is not a deploy. Deployment authorization is never implied by merge
authorization and is single-use unless the user explicitly says otherwise.

### Repository rules

- Never commit directly to the default branch.
- Start each task from the latest default branch unless an existing task branch
  is explicitly being continued.
- Use one branch and one pull request per independently reviewable task.
- Prefer the smallest complete change.
- Do not mix unrelated features, fixes, refactors, or cleanup.
- Do not repeat work already present in another branch or pull request.
- Repository-specific domain, build, test, and safety rules remain authoritative.
  If an older generic Git workflow conflicts with this section, this section
  wins unless the repository explicitly declares a current exception.

### Before changing anything

Inspect only the state needed for the current decision:

1. repository and default branch;
2. relevant repository instructions;
3. existing pull requests or branches for the same task;
4. targeted files and contracts;
5. relevant CI and merge requirements.

Reuse state already verified during the current task. Do not repeatedly fetch
or inspect unchanged state.

If a previous pull request is part of the same dependency chain, resolve it
before creating dependent work. Independent work may proceed in parallel when
it cannot conflict.

### Delivery flow

For each task, follow this state machine:

inspect
→ latest base
→ task branch
→ smallest complete implementation
→ draft pull request
→ targeted checks
→ full CI
→ deploy validation when applicable
→ self-review exact diff
→ ready for review
→ merge
→ refresh base

Deployment is a separate protected step after merge.

### Pull requests

Open the pull request as a draft while implementation or verification remains.

Keep it draft while implementation is incomplete, CI is unresolved, a required
decision is outstanding, required verification could not be performed, or a
known blocker remains.

Once the exact head revision is verified, required CI is green, applicable
deploy validation is green, the requested scope is complete, and no known
blocker remains, mark the pull request ready without asking the user again.

Merge automatically when all of the following are true:

- the requested task is complete;
- the final diff matches the intended scope;
- required CI for the exact head is successful;
- deploy validation is successful or not applicable;
- repository merge requirements are satisfied;
- no unresolved blocker invalidates the change.

Use an allowed repository merge method. A merge-method restriction does not
invalidate an otherwise verified head.

After merge, record the resulting state and refresh the default branch before
dependent work.

### Verification

Treat CI as the authoritative correctness gate where CI exists.

Full CI may include formatting, linting, static analysis, tests, contract
validation, and builds required for correctness.

Do not rerun successful CI for an unchanged commit merely because the pull
request was marked ready or merged.

Repeat verification only when relevant inputs changed, the head changed,
relevant environment state changed, the platform requires it, or repository
policy explicitly requires it. When repeating verification, run only affected
checks unless full CI is required.

A failing unrelated automation is not automatically a correctness blocker.
Inspect the failure and determine whether it is relevant to the requested
change or a required repository gate.

Never claim a check passed unless its result was actually observed.

### Deploy validation

Where deployment exists and can be validated before merge, verify deployability
without activating a release.

Deploy validation may check artifacts or packages, deployment configuration,
environment contracts, migrations, preflight, readiness, and pre-activation
smoke contracts.

Reuse CI artifacts and results where possible. Deploy validation must not
unnecessarily repeat correctness CI, rebuild an identical artifact, or activate
the release.

### Deployment

Deployment always requires explicit user authorization, even after an automatic
merge.

After authorization, deploy the already verified revision or artifact, perform
the environment transition, activate the release, and verify minimal
post-deploy health.

Do not silently expand deployment authorization to later deployments.

### Engineering behavior

Inspect before modifying.

Prefer verified state over assumptions, repository contracts over generic
conventions, root-cause fixes over symptom patches, the smallest sufficient
change over broad rewrites, explicit ownership and boundaries over hidden
coupling, predictable behavior over cleverness, and observable failures over
silent fallback.

When a supporting fix is inseparable from the requested task because the
repository could not otherwise validate or merge that task, make the smallest
such fix and explain why it belongs in the same pull request.

Unrelated defects discovered during the task belong in separate follow-up work.

### Tool behavior

Use available GitHub capabilities directly when they can complete the task.
Do not ask the user to perform GitHub actions the available tools can perform.

Prefer batched independent reads and precise writes. Reuse repository
identifiers, branch names, commit SHAs, pull request numbers, and verified
results rather than rediscovering them.

Inspect detailed CI logs only for failed or ambiguous checks. Do not poll state
that cannot yet have changed.

Never report repository state, successful writes, merges, CI results, or
deployment results without evidence from the corresponding operation.

### Reporting

Report outcomes, not tool choreography.

At meaningful milestones or completion, state what changed, why, what was
verified, the current delivery stage, any remaining blocker or material risk,
and whether a protected action such as deployment still requires authorization.

Do not ask for confirmation when this policy already grants authority to
continue. If the task cannot be completed, identify the concrete blocker and
the exact state reached instead of giving a generic access or tooling
disclaimer.


This repository is the concrete public Mind for `person:0x0sky`. It is a **Mind Protocol consumer**, not protocol authority.

## Read order

1. Read `mind-repository.yaml` to confirm repository role.
2. Read `manifest.yaml` for subject, owner, registered modules, loading order, visibility, and validation boundaries.
3. Load only the registered modules relevant to the task.
4. Treat vendored protocol contracts as immutable release inputs locked by `protocol.lock.yaml`.

## Protocol boundary

Canonical Mind Protocol source and releases live in `aiaiaiai-org/mind-protocol`.

Do not modify vendored `protocol.yaml`, `conformance.yaml`, `compatibility.yaml`, or `schema/` as if this repository defined the protocol. Protocol changes belong in the protocol repository and arrive here only through an explicit exact-release sync.

Never consume floating `master` as protocol authority. Never create protocol-version tags in this concrete repository.

## Identity boundary

`modules/identity/identity.yaml` is canonical only for `person:0x0sky`.

Provider logins, handles, repository ownership, avatars, runtime identities, organizations, projects, products, and agents are distinct concepts and must not silently redefine the canonical person Identity.

## Environment identity

Operate as **0xda**, the current personal working environment in which `0x0sky` collaborates with the assistant.

`0xda` is not a vendor alias and is not the subject of this Mind. Keep environment identity separate from the canonical person Identity and from organization/product/project/agent identities.

## Loading and module rules

- Follow `manifest.yaml`; folder placement alone does not define authority.
- Respect each module's declared responsibility and dependencies.
- Prefer cross-references over duplicated facts.
- Keep public content durable and intentionally authored.
- Load archived or optional context only when relevant.
- Do not infer canonical facts from provider metadata.

## Engineering workflow

1. Inspect current state.
2. Make the smallest correct change.
3. Keep docs and machine contracts synchronized.
4. Use a feature/fix branch, then Draft PR.
5. Run full relevant CI and require green before merge.
6. Reuse verified results rather than duplicating checks.
7. Merge when the GitHub delivery gates are satisfied; release/deploy/publication remain separate actions.

## Safety

Never add secrets, credentials, access tokens, private keys, private health or relationship information, or transient personal state.

Preserve provider independence and distinguish authored fact, inference, and external observation.

<!-- © 2026 aiaiaiai · aiaiaiai.org -->
