# Lizo's Skills Marketplace

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Agent Skills compatible](https://img.shields.io/badge/spec-agentskills.io-7dd3fc)](https://agentskills.io/specification)
[![Claude Code marketplace](https://img.shields.io/badge/Claude_Code-marketplace-a78bfa)](https://docs.claude.com/en/docs/claude-code/plugin-marketplaces)
[![Validate](https://github.com/Lizo-RoadTown/claude-skills-marketplace/actions/workflows/validate.yml/badge.svg)](https://github.com/Lizo-RoadTown/claude-skills-marketplace/actions/workflows/validate.yml)

A skills marketplace authored and maintained by [Liz Osborn](https://github.com/Lizo-RoadTown) (`Lizo-RoadTown`).

The skills follow the open [Agent Skills](https://agentskills.io) standard
(originally from Anthropic), which means they work across any compatible
agent — **Claude Code, Cursor, Gemini CLI, OpenCode, Junie, Goose, Amp**, and
[others](https://agentskills.io/clients). This repo also ships the Claude Code
[plugin marketplace](https://docs.claude.com/en/docs/claude-code/plugin-marketplaces)
manifest so the skills install with one command in Claude Code.

This is the **public distribution channel** for Liz's tool-agnostic,
general-purpose skills. The operator's own platform-coupled patterns and
discipline hooks live in the [Tapestry](https://github.com/Lizo-RoadTown/tapestry)
monorepo, not here — see [Moved out of this repo](#moved-out-of-this-repo).

## Plugins in this marketplace

### `onboarding-psychologist`

A behavioral-research framework for designing first-time-user experiences using
the **IDENTITY-TO-HABIT arc**:

1. Define the first win
2. Remove unnecessary setup
3. Create ownership through action
4. Attach a stable cue
5. Reinforce identity

Grounded in BJ Fogg's Tiny Habits and James Clear's identity-based habits.
Activates on signup flows, empty states, welcome screens, and reactivation work.
Refuses to produce feature tours, "12 things to know" walls, and CRUD-form empty
states.

### `ai-agents-architect`

A decision framework for autonomous-agent architecture:

- Where on the **autonomy spectrum** does this agent sit?
- Which loop pattern — **ReAct**, **Plan-and-Execute**, or **Tree-of-Thoughts**?
- **Single agent or multiple?** (Most common mistake: splitting agents without a real reason.)
- **When to introduce an orchestrator?**

Activates on agent-design and orchestration questions. Refuses tool overload,
infinite tool loops without a cap, and unverified multi-agent splits.

### `sde-extraction-guard`

A repo-specific schema guard for `SDE_Extraction`: a PostToolUse hook runs the
repo's `scripts/check_schema.py` after edits to the extraction surface and blocks
a broken schema (the class of bug that crash-looped the worker). Bundles the
`recorded-transformation` discipline skill. No-ops in repos that don't have the
SDE schema.

## Moved out of this repo

Two plugins that used to live here were consolidated into the Tapestry monorepo
(Step-8 consolidation, 2026-06-22) because they are **platform-coupled** — their
agents/hooks depend on the loom-memory MCP and the Tapestry runtime. Install them
from the tapestry marketplace instead:

- **`liz-patterns` → `tapestry-patterns@tapestry`** — the operator's canonical
  reusable agents + skills (the "one home" per MANIFESTO Pillar 1).
- **`make-skills-discipline` / `loom-discipline` → `tapestry-discipline@tapestry`** —
  the PROBE-first discipline hooks.

```text
/plugin marketplace add Lizo-RoadTown/tapestry
/plugin install tapestry-patterns@tapestry
/plugin install tapestry-discipline@tapestry
```

See the [Tapestry plugin map](https://github.com/Lizo-RoadTown/tapestry/blob/main/docs/architecture/plugin-map.md)
for why each plugin lives where it does.

## Install

### Claude Code

In an active Claude Code session, run:

```text
/plugin marketplace add Lizo-RoadTown/claude-skills-marketplace
/plugin install onboarding-psychologist@lizo-skills
/plugin install ai-agents-architect@lizo-skills
/plugin install sde-extraction-guard@lizo-skills
```

Verify with `/plugin list`.

### Other Agent Skills clients (Cursor, Gemini CLI, OpenCode, etc.)

Each client has its own way of registering skills; the
[Agent Skills client showcase](https://agentskills.io/clients) links to each
one's docs. The skills are at:

- `plugins/onboarding-psychologist/skills/onboarding-psychologist/`
- `plugins/ai-agents-architect/skills/ai-agents-architect/`
- `plugins/sde-extraction-guard/skills/`

You can clone this repo and point your client at those directories, or copy
the individual skill folders into your client's skills directory (usually
something like `~/.<client>/skills/`).

### Validation

Validate the skill format with the official reference tool from agentskills.io:

```bash
npx skills-ref validate ./plugins/onboarding-psychologist/skills/onboarding-psychologist
npx skills-ref validate ./plugins/ai-agents-architect/skills/ai-agents-architect
```

## Repo layout

```text
claude-skills-marketplace/
├── .claude-plugin/
│   └── marketplace.json                          # the catalog (3 plugins)
├── plugins/
│   ├── onboarding-psychologist/
│   │   ├── .claude-plugin/plugin.json
│   │   └── skills/onboarding-psychologist/SKILL.md
│   ├── ai-agents-architect/
│   │   ├── .claude-plugin/plugin.json
│   │   └── skills/ai-agents-architect/SKILL.md
│   └── sde-extraction-guard/
│       ├── .claude-plugin/plugin.json
│       ├── hooks/
│       └── skills/
├── README.md
└── LICENSE
```

Follows the standard Claude Code marketplace structure documented at <https://docs.claude.com/en/docs/claude-code/plugin-marketplaces>.

## Updating

Bump the `version` field in `plugins/<name>/.claude-plugin/plugin.json` and the matching entry in `.claude-plugin/marketplace.json` when releasing a new version. Push to `main`. Users get updates when they run `/plugin marketplace update` followed by `/plugin update`.

## Contributing

Contributions welcome — bug reports, content improvements, new skill proposals. See [CONTRIBUTING.md](CONTRIBUTING.md) for conventions and the PR flow.

By contributing you agree your contribution is licensed Apache 2.0. Please follow the [Code of Conduct](CODE_OF_CONDUCT.md).

## Security

Report vulnerabilities privately — see [SECURITY.md](SECURITY.md). Don't open public issues for security problems.

## Citing this work

If you use these skills in research or downstream projects, see [CITATION.cff](CITATION.cff) — GitHub renders it as a "Cite this repository" button.

## Author & maintainer

**[Liz Osborn](https://github.com/Lizo-RoadTown)** (`Lizo-RoadTown`)

- Related: [Tapestry](https://github.com/Lizo-RoadTown/tapestry) — the monorepo that hosts the platform-coupled plugins (`tapestry-patterns`, `tapestry-discipline`)
- Related: [project-starter](https://github.com/Lizo-RoadTown/project-starter) — the day-1 project scaffolder that references these skills

## License

Apache 2.0 — see [LICENSE](LICENSE).
