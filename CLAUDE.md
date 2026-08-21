# Working in claude-skills-marketplace

Project context for Claude Code. Loaded into every session opened in this repo.

## What this repo is

The PUBLIC Claude Code plugin marketplace (`lizo-skills`) authored by Liz Osborn
(`Lizo-RoadTown`). It is the distribution channel for **tool-agnostic,
general-purpose** skills that follow the open Agent Skills standard and work
across any compatible agent. Hosts 3 plugins:

- **`onboarding-psychologist`** — IDENTITY-TO-HABIT framework for first-time-user flows
- **`ai-agents-architect`** — decision framework for autonomous-agent architecture
- **`sde-extraction-guard`** — repo-specific PostToolUse schema guard for `SDE_Extraction`

## What is NOT here (moved to Tapestry)

The operator's **platform-coupled** plugins were consolidated into the
[Tapestry](https://github.com/Lizo-RoadTown/tapestry) monorepo (Step-8,
2026-06-22) because their agents/hooks depend on the loom-memory MCP and the
Tapestry runtime. They install from the `tapestry` marketplace, not here:

- **`liz-patterns` → `tapestry-patterns@tapestry`** — the operator's canonical
  reusable agents + skills (the "one home" per MANIFESTO Pillar 1).
- **`loom-discipline` / `make-skills-discipline` → `tapestry-discipline@tapestry`** —
  the PROBE-first discipline hooks.

Why the split (and why these three stay public): the
[Tapestry plugin map](https://github.com/Lizo-RoadTown/tapestry/blob/main/docs/architecture/plugin-map.md).
Do NOT re-add `liz-patterns` or a discipline plugin to this repo — that would
re-create the duplication Pillar 1 forbids.

## Discipline for sessions in this repo

```text
/plugin marketplace add Lizo-RoadTown/tapestry
/plugin install tapestry-discipline@tapestry
```

PROBE before asserting (cite file:line). Distinguish dev-tooling from runtime.
Save corrections as feedback memory.

## Releasing a new plugin version

1. Bump `version` in `plugins/<name>/.claude-plugin/plugin.json`
2. Bump the matching entry in `.claude-plugin/marketplace.json`
3. Open PR + merge (the marketplace uses PRs for changes)
4. Consumers: `/plugin marketplace update` + `/plugin update`

## Plugin spec reference

Authoring conventions follow the Claude Code plugin spec — verify against
`~/.claude/plugins/cache/superpowers-marketplace/superpowers-developing-for-claude-code/*/skills/developing-claude-code-plugins/references/plugin-structure.md`
when adding new components.

## Tone

Plain, direct, descriptive. No marketing voice ("the unlock," "delightful,"
"exciting"). No self-congratulation. No defensive contrasts.

## License

Apache 2.0 — every plugin authored here ships under Apache 2.0. PR authors agree
to this by contributing.
