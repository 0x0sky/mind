# Repository instructions for GitHub Copilot

> Native instructions for the GitHub Copilot environment, derived from `.assistant/contract/agent.yaml` and `.assistant/environments/copilot.yaml`.

Operate within `0x0sky/mind` as a repository coding environment distinct from `0xda`.

- Start with `manifest.yaml` and load only context relevant to the task.
- Keep personal identity, organizations, products, projects, and agent environments separate.
- Do not inherit the identity or transient working context of `0xda`.
- Do not import project-specific rules implicitly.
- Inspect the current repository state before editing.
- Make the smallest correct change within the requested scope.
- Preserve provider independence unless a target is explicitly runtime-specific.
- Keep documentation synchronized with behavior.
- Run the most relevant available checks and do not publish with failing validation.
- Prefer reviewable commits and draft pull requests.
- Proceed with inspection, branches, edits, commits, draft pull requests, issues, workflows, and CI fixes required by the task.
- Require explicit user authorization before merge, deploy, publish, deletion, repository transfer, secret rotation or exposure, or another irreversible action.
- Follow the user’s language and retain English technical terms when they improve precision.
- Report changes, validation, blockers, and uncertainty directly.
- Never commit secrets, credentials, access tokens, private health or relationship information, or transient personal state.

This file implements the Copilot environment. Shared behavior belongs in `.assistant/contract/`; Copilot-specific identity and runtime behavior belong in `.assistant/environments/copilot.yaml`.
