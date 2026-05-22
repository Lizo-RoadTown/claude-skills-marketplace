# Contributing

Thanks for taking a look. This is **Liz Osborn's** skills marketplace — a curated set of skills following the open [Agent Skills](https://agentskills.io) standard.

Contributions are welcome in three shapes:

- **Bug reports & fixes** on existing skills (frontmatter errors, broken refs, wrong behavior, install-flow breakage)
- **Improvements** to existing skill content (clearer wording, better examples, additional anti-patterns to refuse)
- **New skill proposals** — see "Proposing a new skill" below

By contributing you agree your contribution is licensed under the same Apache 2.0 license as the project.

## Repo conventions

- **Skill format:** every skill must follow the [agentskills.io specification](https://agentskills.io/specification). The CI runs `skills-ref validate` on every PR.
- **One skill = one plugin** in this marketplace's layout (`plugins/<name>/skills/<name>/SKILL.md`). The duplication is intentional — Claude Code's marketplace format wraps each skill in a plugin shell.
- **Author attribution:** the spec's `metadata.author` field, plus `plugin.json`'s `author.name`, plus the `marketplace.json` entry's `author.name`, should reflect actual authorship. Don't list yourself if Liz wrote it; don't list Liz if you wrote it.
- **Versioning:** semver. Bump the skill's version in `plugin.json` *and* the matching entry in `.claude-plugin/marketplace.json` for any user-visible change.
- **License:** Apache 2.0. SKILL.md may declare a different license in frontmatter only if the skill genuinely is differently licensed.
- **Markdown style:** matches the rest of the repo — sentence-case headings, no marketing voice, describe what *is* not what it *isn't*.
- **Filenames:** kebab-case, lowercase, no spaces.

## Local validation

Before opening a PR, run:

```bash
# Validate each skill's SKILL.md format
npx skills-ref validate ./plugins/onboarding-psychologist/skills/onboarding-psychologist
npx skills-ref validate ./plugins/ai-agents-architect/skills/ai-agents-architect

# Validate JSON manifests (if you have ajv-cli)
npx ajv-cli validate -s schema/marketplace.schema.json -d .claude-plugin/marketplace.json
```

The same checks run in CI on every PR.

## Proposing a new skill

Open an issue first using the **New skill proposal** template. Include:

1. The skill's `name` (kebab-case, must be unique in this marketplace)
2. A 1-sentence `description` that says *what* it does and *when* to use it
3. The 2-3 anti-patterns it would refuse to produce (skills with no opinion don't earn a spot)
4. Whether you've checked the agentskills.io existing-clients catalog for prior art

If the proposal lands, we'll discuss whether it belongs in this marketplace or somewhere else (the open standard means there's no single right home).

## Pull request flow

1. Fork the repo
2. Branch from `main`: `git checkout -b skill/<name>` or `fix/<short-desc>`
3. Make the change; run validation locally
4. Open a PR — the template asks for change category, validation status, and version bump
5. CI runs; address any failures
6. Maintainer reviews and merges. Squash-merge by default — keep the main-branch history flat.

## Releases

This marketplace follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and [Semantic Versioning](https://semver.org/spec/v2.0.0.html). Releases happen as needed, tagged `vX.Y.Z`. The Anthropic plugin caching docs note that users only see updates when the `version` field changes, so we bump it deliberately.

## Code of Conduct

Be respectful. The full text is in [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

## Security

Found a vulnerability? Don't open a public issue. See [SECURITY.md](SECURITY.md) for the reporting process.

## Maintained by

[Liz Osborn](https://github.com/Lizo-RoadTown). Reach out via the email in `marketplace.json` or open a GitHub issue.
