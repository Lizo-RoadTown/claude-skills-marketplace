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

Three plugins ship here today: two pure skills (`onboarding-psychologist`, `ai-agents-architect`) authored as design disciplines, and one discipline plugin (`make-skills-discipline`) that auto-injects behavioral rules + hooks into every Claude Code session in Liz's repos. The two pure skills are referenced by [project-starter](https://github.com/Lizo-RoadTown/project-starter)'s variant templates; the discipline plugin is consumed by [Make_Skills](https://github.com/Lizo-RoadTown/Make_Skills) and [the-loom](https://github.com/Lizo-RoadTown/the-loom).

## Plugins in this marketplace

### `onboarding-psychologist` — pure skill

A behavioral-research framework for designing first-time-user experiences using the **IDENTITY-TO-HABIT arc**:

1. Define the first win
2. Remove unnecessary setup
3. Create ownership through action
4. Attach a stable cue
5. Reinforce identity

Grounded in BJ Fogg's Tiny Habits and James Clear's identity-based habits. Activates on signup flows, empty states, welcome screens, and reactivation work. Refuses to produce feature tours, "12 things to know" walls, and CRUD-form empty states.

### `ai-agents-architect` — pure skill

A decision framework for autonomous-agent architecture:

- Where on the **autonomy spectrum** does this agent sit?
- Which loop pattern — **ReAct**, **Plan-and-Execute**, or **Tree-of-Thoughts**?
- **Single agent or multiple?** (Most common mistake: splitting agents without a real reason.)
- **When to introduce an orchestrator?**

Activates on agent-design and orchestration questions. Refuses tool overload, infinite tool loops without a cap, and unverified multi-agent splits.

### `make-skills-discipline` — discipline plugin (Claude Code only)

Not a pure skill — a Claude Code plugin that **auto-injects behavioral rules + hook scripts** into every session opened in Liz's working repos (`Make_Skills`, `the-loom`, and any `project-starter`-scaffolded repo). It enforces:

- **PROBE before asserting** — Grep/Read the source before claiming facts about it
- **Cite `file:line`** — every claim about the codebase carries a citation; the regex accepts `file.ext:line`, bare paths, and `https?://` URLs
- **Distinguish dev-tooling from runtime** — name which audience each piece of infra serves
- **Friction-as-memory** — when the user corrects you, write a `feedback` memory at the moment of correction (not after)
- **Cite skills by name** — when invoking a methodology skill, name it in the response
- **Architecture snapshots** — `SessionStart` writes a snapshot + diff under `docs/architecture-snapshots/`, and an `architecture-analyst` subagent + `/architecture-report` slash command turn the diff into a narrative

Hooks fire on `UserPromptSubmit`, `PreToolUse`, `Stop`, and `SessionStart`. Scope check is case-insensitive — works regardless of how the repo path is cased. **Being renamed `make-skills-discipline` → `loom-discipline`** as part of the-loom Phase 1; both names work during the transition window.

Unlike the two pure skills above, this plugin is only useful in Liz's repos — its hook scripts assume the Make_Skills/the-loom/project-starter conventions. Distributed here so the install path is one command from any of those repos' CLAUDE.md.

## Install

### Claude Code

In an active Claude Code session, run:

```text
/plugin marketplace add Lizo-RoadTown/claude-skills-marketplace
/plugin install onboarding-psychologist@lizo-skills
/plugin install ai-agents-architect@lizo-skills
/plugin install make-skills-discipline@lizo-skills
```

Verify with `/plugin list`. The discipline plugin starts injecting rules on the next session opened in an in-scope repo (Make_Skills, the-loom, or any project-starter-scaffolded directory).

### Other Agent Skills clients (Cursor, Gemini CLI, OpenCode, etc.)

The two **pure skills** are portable — each client has its own way of registering skills; the [Agent Skills client showcase](https://agentskills.io/clients) links to each one's docs. The skill bodies live at:

- `plugins/onboarding-psychologist/skills/onboarding-psychologist/`
- `plugins/ai-agents-architect/skills/ai-agents-architect/`

You can clone this repo and point your client at those directories, or copy the individual skill folders into your client's skills directory (usually something like `~/.<client>/skills/`).

The **discipline plugin** is Claude-Code-only — its hook contract (`hooks.json`, `PreToolUse`/`UserPromptSubmit`/`Stop`/`SessionStart` events) is specific to Claude Code's plugin system. Other clients don't have an equivalent today.

### Validation

Validate the **pure skill** formats with the official reference tool from agentskills.io:

```bash
npx skills-ref validate ./plugins/onboarding-psychologist/skills/onboarding-psychologist
npx skills-ref validate ./plugins/ai-agents-architect/skills/ai-agents-architect
```

The discipline plugin's skill body (`plugins/make-skills-discipline/skills/make-skills-discipline/`) also validates, but the plugin's load-bearing surface is the hook scripts + manifests — those are exercised by the `pytest` job in `.github/workflows/validate.yml` (runs `python -m unittest discover` against `plugins/*/tests/`).

## Repo layout

```text
claude-skills-marketplace/
├── .claude-plugin/
│   └── marketplace.json                          # the catalog (lists all 3 plugins)
├── plugins/
│   ├── onboarding-psychologist/                  # pure skill
│   │   ├── .claude-plugin/plugin.json
│   │   └── skills/onboarding-psychologist/SKILL.md
│   ├── ai-agents-architect/                      # pure skill
│   │   ├── .claude-plugin/plugin.json
│   │   └── skills/ai-agents-architect/SKILL.md
│   └── make-skills-discipline/                   # discipline plugin (Claude Code only)
│       ├── .claude-plugin/plugin.json
│       ├── skills/make-skills-discipline/SKILL.md
│       ├── hooks/
│       │   ├── hooks.json                        # event registration
│       │   └── run-python.mjs                    # Node launcher for the Python hook scripts
│       ├── scripts/                              # the hook scripts themselves
│       │   ├── pre_tool_use.py
│       │   ├── user_prompt_submit.py
│       │   ├── stop_audit.py
│       │   └── session_start.py
│       ├── agents/architecture-analyst.md        # subagent for /architecture-report
│       ├── commands/architecture-report.md       # slash command
│       └── tests/                                # unittest suite (run by validate.yml)
├── CHANGELOG.md
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

- Related: [project-starter](https://github.com/Lizo-RoadTown/project-starter) — the day-1 project scaffolder that references the two pure skills here
- Related: [Make_Skills](https://github.com/Lizo-RoadTown/Make_Skills) — the engine (agent runtime, skill compilation, model registry) that consumes `make-skills-discipline` for its dev workflow
- Related: [the-loom](https://github.com/Lizo-RoadTown/the-loom) — cross-project memory + observability + governance; also consumes `make-skills-discipline` (transitioning to `loom-discipline`)

## License

Apache 2.0 — see [LICENSE](LICENSE).
