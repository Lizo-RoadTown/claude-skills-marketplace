# Working in claude-skills-marketplace

Project context for Claude Code. Loaded into every session opened in this repo.

## What this repo is

The PUBLIC Claude Code plugin marketplace authored by Liz Osborn (`Lizo-RoadTown`). Hosts 4 plugins:

- **`liz-patterns`** — the canonical patterns library (agents + skills the operator uses across every project)
- **`make-skills-discipline`** — auto-injecting discipline wrapper for Make_Skills + project-starter-scaffolded repos
- **`onboarding-psychologist`** — IDENTITY-TO-HABIT framework for first-time-user flows
- **`ai-agents-architect`** — decision framework for autonomous-agent architecture

## Where the canonical patterns live

In THIS repo: `plugins/liz-patterns/` is THE canonical home for the operator's reusable agents + skills + tools per [tapestry/MANIFESTO.md Pillar 1](https://github.com/Lizo-RoadTown/tapestry/blob/main/MANIFESTO.md). Changes to canonical agents/skills land here, not in any consuming repo's local `skills/` directory.

Internal layout:

- `plugins/liz-patterns/agents/` — 7 agent files with `description + capabilities + tools` frontmatter
- `plugins/liz-patterns/skills/` — 8 skills with `name + description` frontmatter
- `plugins/liz-patterns/.claude-plugin/plugin.json` — manifest
- `plugins/liz-patterns/.claude-plugin/marketplace.json` — dev marketplace for local testing
- `plugins/liz-patterns/README.md` — what's in it + the one exception + install

## Discipline plugin

For sessions working IN this repo (authoring plugins):

```text
/plugin install make-skills-discipline@lizo-skills
```

PROBE before asserting (cite file:line). Distinguish dev-tooling from runtime. Save corrections as feedback memory.

## Canonical patterns (operator's own library — installable from this repo)

```text
/plugin install liz-patterns@lizo-skills
```

This makes the operator's reusable agents + skills available in this session too:

- **Agents**: `liz-patterns:infrastructure-mapping`, `next-actions-planning`, `lessons-learned`, `orchestration-cataloging`, `eval-deep-research`, `web-app-scaffold`, `agentic-upskilling`
- **Skills**: `liz-patterns:agentic-skill-design`, `deep-research-pattern`, `design-evaluation`, `documentation`, `document-parsing`, `layered-explanation`, `open-source-documentation`, `proposal-authoring`

## Releasing a new plugin version

Per `CONTRIBUTING.md`:

1. Bump `version` in `plugins/<name>/.claude-plugin/plugin.json`
2. Bump matching entry in `.claude-plugin/marketplace.json`
3. Open PR + merge (the marketplace uses PRs for changes; see PR #5, #6, #8 for examples)
4. Consumers: `/plugin marketplace update` + `/plugin update`

## Plugin spec reference

Authoring conventions follow the Claude Code plugin spec — verify against `~/.claude/plugins/cache/superpowers-marketplace/superpowers-developing-for-claude-code/*/skills/developing-claude-code-plugins/references/plugin-structure.md` when adding new components.

## Tone

Plain, direct, descriptive. No marketing voice ("the unlock," "delightful," "exciting"). No self-congratulation. No defensive contrasts.

## License

Apache 2.0 — every plugin authored here ships under Apache 2.0. PR authors agree to this by contributing.
