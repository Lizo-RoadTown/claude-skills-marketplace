# Changelog

All notable changes to this marketplace and its skills will be documented in this file.

The format is based on [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html).

Each skill has its own version in its `plugin.json`. The top-level versions
below track the marketplace as a whole (changes to manifests, repo structure,
or any skill).

## [Unreleased]

### Changed

- **`make-skills-discipline` v0.1.5** — broadened in-scope check to include `the-loom`. All four hook scripts (`pre_tool_use.py`, `stop_audit.py`, `user_prompt_submit.py`, `session_start.py`) now fire in three project trees: `Make_Skills`, `the-loom`, and `project-starter`-scaffolded repos. Normalized to case-insensitive comparison for the path-substring matches so future repo naming variations don't silently disable hooks. New test case (`test_scope_includes_the_loom`) verifies the-loom paths fire the hook.

### Fixed

- **`make-skills-discipline` v0.1.4** — `_observability` import silent-fail under the Node launcher. v0.1.2/v0.1.3 hook scripts used `sys.path.insert + from _observability import ...` which silently fell back to no-op stubs when invoked via `run-python.mjs` (the Node launcher that `hooks.json` points at). Result: `hooks.jsonl` was never written, PR #38's Loki dashboard panels stayed empty, the discipline plugin's observability story was non-functional in practice despite being correct in principle. The v0.1.4 fix replaces the import with `importlib.util.spec_from_file_location` using an absolute path computed from `__file__` — bypasses `sys.path` entirely. If the import still fails (e.g., missing file), the error is now logged to `~/.claude/logs/hook-import-errors.log` instead of silently swallowed. Applied to all 4 hook scripts (`pre_tool_use.py`, `user_prompt_submit.py`, `stop_audit.py`, `session_start.py`). New subprocess regression test (`test_subprocess_writes_log_when_in_scope`) mimics the Node launcher's invocation pattern — catches future regressions of this class.

### Added

- **`make-skills-discipline` v0.1.3** — two false-positive fixes in the `PreToolUse` hook + first plugin unit tests.
  - **Citation regex broadened.** `pre_tool_use.py:CITATION_PATTERNS` now accepts three forms: the original `file.ext:line`, bare `path/file.ext` paths, and `https?://` URLs. Previously, citing external docs (Context7, GitHub, vendor URLs) didn't satisfy the citation check and fired a spurious "no citation" reminder.
  - **Dual-mode triggers gated by target path.** `touches_dual_mode()` now early-exits when the edit target is a docs/markdown/convention file (`.md`/`.rst`/`.txt`/`.mdx` extensions, or paths under `docs/`, top-level `README`/`CHANGELOG`/`CONTRIBUTING`/`ARCHITECTURE`/`AGENTS.md`/`CLAUDE.md`, or `.github/`). Previously, any doc that mentioned a trigger keyword (e.g., `AUTH_SECRET` in a planning doc) fired the boundary-change reminder. Same class of false-positive as the v0.1.2 `memory`/`tenant` fix.
  - **First plugin tests.** `plugins/make-skills-discipline/tests/test_pre_tool_use.py` — 14 unittest cases covering both fixes (citation forms accepted/rejected; docs gated; runtime fires preserved). New CI job `pytest` in `.github/workflows/validate.yml` runs `python -m unittest discover` over every `plugins/*/tests/` dir.

## [0.1.3] — 2026-05-22

### Changed

- **`ai-agents-architect` v0.1.3** — replaced "Related skills" cross-references with verified real-installable skills from the public stack:
  - `superpowers:writing-plans` + `superpowers:executing-plans` for multi-step planning + execution (replaces previous AWS Labs reference, which was a Python library not a skill)
  - `episodic-memory:remembering-conversations` for durable memory (replaces sickn33's manual-clone skill, which had no marketplace entry)
  - `superpowers:dispatching-parallel-agents` for multi-agent coordination (replaces muratcankoylan's Context Engineering plugin, which was thinner and had no review trail)
  - `claude-api` kept as-is — Anthropic's official SDK skill
  - Public-skill availability verified by the Make_Skills agent against the live registry before publish.

## [0.1.2] — 2026-05-21

### Fixed

- **`ai-agents-architect` v0.1.2** — fixed the "Related skills" section of
  the SKILL.md, which previously implied that `agent-orchestrator`,
  `agent-memory-systems`, and `claude-api` lived in this marketplace. They
  don't. Replaced bare references with proper attribution to their actual
  sources (AWS Labs, muratcankoylan, sickn33, anthropics/skills) plus
  install commands or repo URLs. Project-starter docs already had this
  right — the bug was only in this skill's cross-reference list.

## [0.1.1] — 2026-05-21

### Fixed

- **`onboarding-psychologist` v0.1.1** — fixed misattribution in the body text. The Hook Model is Nir Eyal's framework (from *Hooked*, 2014), not BJ Fogg's. BJ Fogg authored Tiny Habits and the **Fogg Behavior Model (B=MAP)**. Description and reference list now correctly credit all three researchers (Fogg, Eyal, Clear). The References section was already correct — this fix aligns the body text and frontmatter description with the references.

### Changed

- **`ai-agents-architect` v0.1.1** — added `tree-of-thoughts` to plugin keywords and marketplace tags. The skill teaches the Tree-of-Thoughts pattern alongside ReAct and Plan-and-Execute; the tag omission was a discoverability gap. Description also updated to name the third pattern explicitly.
- **`onboarding-psychologist` v0.1.1** — added `fogg-behavior-model`, `tiny-habits`, `hook-model`, and `identity-based-habits` to marketplace tags for the same discoverability reason.

## [0.1.0] — 2026-05-21

### Added

- **Initial marketplace publish.** Authored and maintained by [Liz Osborn](https://github.com/Lizo-RoadTown).
- **`onboarding-psychologist` v0.1.0** — Behavioral-research framework for first-time-user flows using the IDENTITY-TO-HABIT arc. Grounded in BJ Fogg's Tiny Habits and James Clear's identity-based habits.
- **`ai-agents-architect` v0.1.0** — Decision framework for autonomous-agent architecture: autonomy spectrum, ReAct vs Plan-and-Execute, single-vs-multi-agent decisions, when to introduce an orchestrator.
- Marketplace catalog at `.claude-plugin/marketplace.json` for installation via Claude Code (`/plugin marketplace add Lizo-RoadTown/claude-skills-marketplace`).
- Cross-client compatibility: SKILL.md files follow the open [agentskills.io](https://agentskills.io) specification, so the skills also work in Cursor, Gemini CLI, OpenCode, Junie, Goose, Amp, and others.
- OSS hygiene: README, CONTRIBUTING, CODE_OF_CONDUCT, SECURITY, LICENSE (Apache 2.0), CHANGELOG, CODEOWNERS, CITATION.cff.
- GitHub Actions CI for skill validation (`skills-ref validate`), JSON schema validation, and markdownlint.
- GitHub issue and PR templates.

### Notes

- Both skills are referenced by [Lizo-RoadTown/project-starter](https://github.com/Lizo-RoadTown/project-starter)'s `ui-app` and `agent-app` variants respectively. This marketplace closes the install path that was previously missing.

[Unreleased]: https://github.com/Lizo-RoadTown/claude-skills-marketplace/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/Lizo-RoadTown/claude-skills-marketplace/releases/tag/v0.1.0
