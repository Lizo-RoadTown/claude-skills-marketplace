<!-- Thanks for the PR! Fill out the sections that apply. -->

## What does this change?

<!-- One or two sentences. -->

## Category

- [ ] Bug fix (no behavior change beyond the fix)
- [ ] Skill content improvement (clearer wording, better examples, additional anti-patterns)
- [ ] New skill (open a `[skill]` issue first if you haven't)
- [ ] Marketplace plumbing (manifests, CI, repo hygiene)
- [ ] Docs only

## Affected skill(s)

- [ ] `onboarding-psychologist`
- [ ] `ai-agents-architect`
- [ ] (new skill — name it)
- [ ] None — marketplace-wide change

## Version bump

For any user-visible change, bump `version` in **both** the skill's `plugin.json` **and** the matching entry in `.claude-plugin/marketplace.json`. Note the bump here:

- [ ] Patch (bug fix, no spec or behavior changes)
- [ ] Minor (new behavior, backward-compatible)
- [ ] Major (breaking change to prompts/behavior)
- [ ] No version bump (docs-only or repo plumbing)

## Validation

- [ ] `skills-ref validate` passes on every affected skill
- [ ] CI is green (or this PR fixes a previously-red CI)

## Checklist

- [ ] CHANGELOG.md updated under `[Unreleased]`
- [ ] Author attribution is correct (don't list yourself for content you didn't write; don't list someone else for content you did)
- [ ] No PII or secrets in the diff
- [ ] If breaking, the breaking change is called out in the PR title with `[breaking]`
