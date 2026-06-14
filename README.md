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

Both skills are referenced by [project-starter](https://github.com/Lizo-RoadTown/project-starter)'s variant templates. Until now, they had no public install path — this repo fixes that.

## Plugins in this marketplace

### `liz-patterns` ⭐ canonical patterns library

**The ONE home for Liz's reusable agents + skills + tools.** Installed once, available in every Claude Code session in every project — so the same pattern name means the same thing wherever invoked.

Per [tapestry/MANIFESTO.md Part 3 Pillar 1](https://github.com/Lizo-RoadTown/tapestry/blob/main/MANIFESTO.md), every reusable pattern has ONE name, ONE home, available everywhere via reference (not copy). This plugin replaces the duplicated copies that previously lived across docs-agent, Make_Skills, and the-loom.

Contains:
- **7 agents** — agentic-upskilling (doc wrapper for the deployed self-observer service), eval-deep-research, infrastructure-mapping, lessons-learned, next-actions-planning, orchestration-cataloging, web-app-scaffold
- **8 skills** — agentic-skill-design, deep-research-pattern, design-evaluation, document-parsing, documentation, layered-explanation, open-source-documentation, proposal-authoring

Compiled by the platform's [recursive-skill-engine loop](https://github.com/Lizo-RoadTown/tapestry/blob/main/MANIFESTO.md): candidates surface via observers, decisions land via policy, engine compiles, results land here.

### `make-skills-discipline`

Auto-injecting discipline wrapper for Claude Code sessions working in Make_Skills or any project-starter-scaffolded repo. Hook scripts enforce PROBE-first behavior, file:line citation, dev-tooling-vs-runtime distinction, and friction-as-memory writing. Same forcing-function pattern as `superpowers:using-superpowers`.

### `onboarding-psychologist`

A behavioral-research framework for designing first-time-user experiences using the **IDENTITY-TO-HABIT arc**:

1. Define the first win
2. Remove unnecessary setup
3. Create ownership through action
4. Attach a stable cue
5. Reinforce identity

Grounded in BJ Fogg's Tiny Habits and James Clear's identity-based habits. Activates on signup flows, empty states, welcome screens, and reactivation work. Refuses to produce feature tours, "12 things to know" walls, and CRUD-form empty states.

### `ai-agents-architect`

A decision framework for autonomous-agent architecture:

- Where on the **autonomy spectrum** does this agent sit?
- Which loop pattern — **ReAct**, **Plan-and-Execute**, or **Tree-of-Thoughts**?
- **Single agent or multiple?** (Most common mistake: splitting agents without a real reason.)
- **When to introduce an orchestrator?**

Activates on agent-design and orchestration questions. Refuses tool overload, infinite tool loops without a cap, and unverified multi-agent splits.

## Install

### Claude Code

In an active Claude Code session, run:

```text
/plugin marketplace add Lizo-RoadTown/claude-skills-marketplace
/plugin install liz-patterns@lizo-skills
/plugin install make-skills-discipline@lizo-skills
/plugin install onboarding-psychologist@lizo-skills
/plugin install ai-agents-architect@lizo-skills
```

Verify with `/plugin list`.

**Most important:** `liz-patterns` is the canonical patterns library. Installing it makes every reusable agent + skill available in every project, with one name, behaving consistently. If you install nothing else, install that.

### Other Agent Skills clients (Cursor, Gemini CLI, OpenCode, etc.)

Each client has its own way of registering skills; the
[Agent Skills client showcase](https://agentskills.io/clients) links to each
one's docs. The skills + agents are at:

- `plugins/liz-patterns/skills/` (8 skills)
- `plugins/liz-patterns/agents/` (7 agents)
- `plugins/onboarding-psychologist/skills/onboarding-psychologist/`
- `plugins/ai-agents-architect/skills/ai-agents-architect/`
- `plugins/make-skills-discipline/` (skills + hooks)

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
│   └── marketplace.json                          # the catalog (4 plugins)
├── plugins/
│   ├── liz-patterns/                             # ⭐ canonical patterns library
│   │   ├── .claude-plugin/
│   │   │   ├── plugin.json
│   │   │   └── marketplace.json                  # dev marketplace for local testing
│   │   ├── agents/                               # 7 agents (description + capabilities + tools)
│   │   ├── skills/                               # 8 skills (name + description)
│   │   └── README.md
│   ├── make-skills-discipline/
│   │   ├── .claude-plugin/plugin.json
│   │   ├── hooks/                                # discipline-enforcement hooks
│   │   ├── skills/
│   │   ├── agents/
│   │   ├── commands/
│   │   └── scripts/
│   ├── onboarding-psychologist/
│   │   ├── .claude-plugin/plugin.json
│   │   └── skills/onboarding-psychologist/SKILL.md
│   └── ai-agents-architect/
│       ├── .claude-plugin/plugin.json
│       └── skills/ai-agents-architect/SKILL.md
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

- Related: [project-starter](https://github.com/Lizo-RoadTown/project-starter) — the day-1 project scaffolder that references these skills
- Related: [Make_Skills](https://github.com/Lizo-RoadTown/Make_Skills) — Liz's broader skills workshop

## License

Apache 2.0 — see [LICENSE](LICENSE).
