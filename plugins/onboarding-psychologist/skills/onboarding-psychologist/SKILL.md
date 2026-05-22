---
name: onboarding-psychologist
description: A behavioral-research framework for designing first-time-user experiences using the IDENTITY-TO-HABIT arc — define the first win, remove unnecessary setup, create ownership through action, attach a stable cue, reinforce identity. Use when designing signup flows, empty states, welcome screens, reactivation flows, or any first-use surface. Grounded in BJ Fogg's Tiny Habits and James Clear's identity-based habits. Refuses feature tours, "12 things to know" walls, and CRUD-form empty states.
license: Apache-2.0
compatibility: Agent Skills compatible (Claude Code, Cursor, Gemini CLI, OpenCode, and others — see agentskills.io/clients)
metadata:
  author: Liz Osborn
  version: "0.1.0"
  homepage: "https://github.com/Lizo-RoadTown/claude-skills-marketplace"
---

# Onboarding Psychologist

A framework for taking new users from curious outsider to engaged participant.
Use this skill whenever the task touches:

- A signup or first-time-user flow
- A primary feature's empty state
- A "welcome back" experience for returning users
- A reactivation flow for lapsed users

Grounded in published behavioral research: **BJ Fogg** (Tiny Habits, the Hook
Model) and **James Clear** (Atomic Habits, identity-based habits).

---

## The IDENTITY-TO-HABIT arc — five steps

Walk through these in order whenever designing or reviewing a first-use flow.

### 1. Define the first win

The **smallest meaningful success** that proves the product's value.

Examples:
- Headspace: finish one breathing exercise
- Notion: create one page
- Duolingo: answer one question correctly

**Test:** can a new user reach the first win in under 2 minutes, with no
friction? If not, the first win is too far away or the path is too tangled.

### 2. Remove unnecessary setup

Every decision a user makes before the first win is a chance to lose them.
Defer everything that can be deferred.

**Common cuts:**
- Email verification → let them verify later
- Profile pictures → use initials
- Team-vs-personal choice → default to personal
- Tutorial selection → have one default flow
- Plan/tier selection → free first, upgrade prompts later

### 3. Create ownership through action

A small, meaningful task that creates **investment**. The user does
something that's theirs — names a document, picks a goal, adds a contact.
Psychologically distinct from passive consumption.

The IKEA effect in software: users overvalue what they helped build. One
small input by minute three pays dividends in retention.

### 4. Attach a stable cue

A habit needs a trigger that fires reliably. Pair the product with an
**existing routine** the user already does.

Examples:
- Meditation apps → "before bed" or "with morning coffee"
- Language apps → "during commute" or "lunch break"
- Productivity tools → "first thing after standup"

BJ Fogg's formula: **anchor → behavior → celebration.** Without the anchor,
habits don't form.

### 5. Reinforce identity

Reflect the user as someone who **succeeds with this product**. Not "you
did this task" but "you're someone who [the identity the product supports]."

Examples:
- "You're a daily reader" (not "you read for 5 minutes today")
- "You're building a writing practice" (not "you wrote 200 words")
- "You're learning Spanish" (not "you completed lesson 3")

Identity is sticky. Tasks are forgotten. The product that frames identity
stays open in the user's head between sessions.

---

## Anti-patterns — refuse if asked to produce these

When asked to design first-time-user surfaces, **actively decline** to
produce:

- **Feature tours** — narrating the UI before the user has wanted any of it
- **"12 things to know" walls** — anything that asks the user to memorize before they've succeeded
- **Empty-state pages that show CRUD forms** — empty states should show *value*, not data-entry chores
- **Forced selection** of plan, team type, or use case before first win — irreversible-seeming choices block exploration
- **Email verification gating the first win** — let the user succeed first; verify later
- **Generic welcome screens** with stock illustrations and "Get started" buttons that don't lead anywhere meaningful
- **Modal walkthroughs** that block the interface

If the request explicitly demands one of these, name the anti-pattern, explain
the cost (drop-off, reduced activation), and propose the IDENTITY-TO-HABIT
alternative.

---

## When this skill is most valuable

The framework applies any time you're designing first-use, but it has the
**highest ROI when retention is a real concern**:

- Consumer apps where the user can leave at any time
- B2B SaaS with self-serve signup
- Products where habit formation is the goal (fitness, learning, journaling)
- Products with a high-stakes first session (paid trials, free credits)

For internal tools where users are *required* to use the product (employee
apps, b2b admin panels), the arc still works but feels less load-bearing —
prioritize step 1 (first win) and step 3 (ownership), de-emphasize 4 and 5.

---

## Output expectations

When invoked to design or review a first-use surface, produce:

1. A named **first win** (one sentence)
2. A pruned **setup list** — what's been cut, what remains, why
3. An **ownership action** — what the user does that's theirs
4. A **cue strategy** — which existing routine the product anchors to
5. The **identity statement** the product reflects back
6. A list of any **anti-patterns** in the current design that need to come out

Be concrete. "Make onboarding better" is not actionable. "Cut the email
verification gate, defer team-name selection until after the user has saved
their first note" is.

---

## References

- BJ Fogg — [Tiny Habits](https://www.bjfogg.com/) (anchor → behavior → celebration)
- James Clear — [Identity-Based Habits](https://jamesclear.com/identity-based-habits)
- Nir Eyal — [Hooked](https://www.nirandfar.com/hooked/) (trigger → action → reward → investment)
- Connected pattern in `agent-app` design discipline: the IDENTITY-TO-HABIT arc is also referenced in [Lizo-RoadTown/project-starter](https://github.com/Lizo-RoadTown/project-starter)'s UX_CONTRACT template.
