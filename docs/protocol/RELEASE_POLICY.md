# Mind Protocol release policy

Mind Protocol source milestones and formal releases are intentionally distinct.

The protocol must remain implementation-independent; GitHub is a publication channel, never protocol authority or runtime dependency.

## Formal release sequence

The first formal publication line is:

1. **`0.9.0`** — first formal GitHub Release;
2. **`1.0.0-rc.1`** — GitHub prerelease proving the exact frozen contract intended for `1.0.0`;
3. **`1.0.0`** — first compatibility-guaranteed stable GitHub Release.

Earlier `0.6.0`, `0.7.0`, and `0.8.0` remain historical source-contract milestones in immutable git history and are not retroactively published as formal GitHub Releases.

## Verified release evidence

Full correctness CI runs on the pull-request head before merge. GitHub merge creates a new merge commit SHA, so publication must not falsely claim that the new SHA itself reran full CI.

A releasable `master` commit is verified by proving all of the following:

- it is the merge commit of the approved protocol pull request into `master`;
- that pull-request head has a successful `Mind Contract CI` run;
- the `master` merge commit tree is exactly identical to the CI-tested pull-request head tree;
- release packaging is generated from that exact `master` commit;
- the release tag points to that exact `master` commit.

If the merge commit tree differs from the tested pull-request head tree, release publication fails and the changed tree must receive new correctness evidence through the normal PR flow.

This preserves `github-delivery.yaml`: correctness is not rerun after merge merely to obtain a new SHA, while the published tree is still proven identical to the tested tree.

## `0.9.0`

`0.9.0` is the first formal release because it freezes the public compatibility surface before `1.0`.

Publication requires:

- merged `0.9.0` source contract on `master`;
- verified release evidence as defined above;
- compatibility freeze validation green;
- supported migration tests green;
- deterministic neutral baseline generation green;
- deterministic formal release bundle generation green;
- dual-mode conformance green;
- final semantic review showing no unresolved compatibility ambiguity;
- tag `v0.9.0` pointing at the verified `master` release commit;
- GitHub Release `Mind Protocol 0.9.0` created from that tag.

Required release artifacts:

- versioned protocol contract set;
- `conformance.yaml`;
- `compatibility.yaml`;
- generated neutral baseline artifact;
- migration guide;
- release notes;
- deterministic release manifest and bundle digest.

## `1.0.0-rc.1`

`1.0.0-rc.1` is a GitHub **prerelease**, not a stable compatibility promise.

It must exercise the exact contract intended for stable `1.0.0` without introducing new public semantics after the candidate unless a blocking defect requires another RC.

Publication requires:

- verified release evidence as defined above;
- tag `v1.0.0-rc.1`;
- GitHub prerelease status;
- clean-checkout conformance;
- clean neutral-baseline generation;
- all required synthetic fixture types green;
- supported migration floor green;
- no required provider dependency;
- no named-identity dependency.

If the RC requires a semantic correction, publish a later RC rather than silently changing the candidate under the same tag.

## `1.0.0`

`1.0.0` is the first **compatibility-guaranteed stable release**.

It must be a stable promotion of the accepted final RC contract. Any semantic change after the final RC requires explicit review and renewed conformance evidence.

Publication requires:

- verified release evidence as defined above;
- tag `v1.0.0`;
- stable GitHub Release;
- all `1.0` acceptance gates green;
- versioned contract set;
- release notes;
- migration guide;
- public conformance suite;
- reproducible neutral baseline artifact;
- compatibility policy.

The `1.x` compatibility promise begins at `1.0.0`, not at any pre-1.0 source milestone or release.

## Post-1.0 identity rollout

Concrete identity synchronization begins **after `1.0.0`**.

The rollout may include:

- `mind@0x0sky` canonical identity content;
- aiaiaiai organization identity;
- child organization identities;
- agent identities;
- canonical named visual assets;
- provider bindings and ecosystem integrations.

Those rollouts consume Mind Protocol `1.0`; they do not define or gate the protocol itself. A concrete rollout may discover a protocol defect, but named identity data must never be promoted into the universal contract merely because one implementation needs it.

## Delivery boundary

Merging source is not releasing.

A formal release is a separate publication action performed only after the verified `master` commit is known. The release must point to that exact commit and must not rerun or duplicate correctness checks unless the release input or environment has materially changed.
