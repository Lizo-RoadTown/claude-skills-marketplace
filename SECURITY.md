# Security Policy

## Supported versions

This marketplace publishes skills, not executable services. "Security" here means: a skill could (in principle) instruct an agent to take an action that compromises a user — for example by suggesting a malicious command, exfiltrating data, or describing a vulnerable pattern as recommended.

| Version | Supported |
|---|---|
| Latest tagged release | Yes |
| Anything older | No — please upgrade |

## Reporting a vulnerability

**Please do not open public GitHub issues for security problems.**

Report privately by either:

1. **GitHub Security Advisories** — preferred. Go to the repo's **Security** tab → **Report a vulnerability**. Liz will see it; the report stays private until a fix is published.
2. **Email** — to the address listed as the owner email in `.claude-plugin/marketplace.json`. Subject line `[security] <short description>`.

## What to include

- Which skill(s) and which version(s) are affected
- The exact behavior that's unsafe (quote the SKILL.md section if applicable)
- A concrete scenario where this becomes a real harm (not just a theoretical worry)
- Suggested fix if you have one

## Response timeline

- **Within 72 hours:** acknowledgement that the report was received
- **Within 14 days:** triage decision (confirmed / not-a-vulnerability / needs-more-info), with reasoning
- **Within 30 days:** fix released for confirmed vulnerabilities, OR a public statement explaining why a fix isn't possible

## Disclosure

By default, vulnerabilities are disclosed publicly when a fix ships, with credit to the reporter (unless the reporter asks to stay anonymous). The disclosure happens in the [CHANGELOG](CHANGELOG.md) under a "Security" subsection of the release.

## Out of scope

- Issues in Claude Code itself — report to Anthropic at [anthropic.com/security](https://www.anthropic.com/security)
- Issues in other Agent Skills clients (Cursor, Gemini CLI, etc.) — report to that client's maintainer
- Issues in transitive dependencies pulled in by a skill — report upstream and let us know

## Maintainer

[Liz Osborn](https://github.com/Lizo-RoadTown)
