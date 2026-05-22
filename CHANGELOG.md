# Changelog

All notable changes to this marketplace and its skills will be documented in this file.

The format is based on [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html).

Each skill has its own version in its `plugin.json`. The top-level versions
below track the marketplace as a whole (changes to manifests, repo structure,
or any skill).

## [Unreleased]

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
