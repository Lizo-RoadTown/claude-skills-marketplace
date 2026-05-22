#!/usr/bin/env python3
"""
UserPromptSubmit hook for make-skills-discipline.

Reads the user's prompt from stdin (JSON), pattern-matches intent, and
emits an adaptive discipline reminder as additionalContext. The reminder
becomes a system reminder Claude sees BEFORE processing the prompt.

The hook fires every user message. To avoid noise, the reminder is short
and tailored — generic prompts get a brief base reminder, intent-laden
prompts get the targeted rule.

Triggers (the patterns that bump up the reminder):

- "does X use" / "where is" / "what's the stack"  →  PROBE-first rule
- "build" / "implement" / "wire up" / "add"        →  dev-tooling-vs-runtime + PROBE
- "fix" / "debug" / "why doesn't"                  →  PROBE + cite-skills
- Anything else                                    →  base reminder

Exit 0 always. The hook should never block UserPromptSubmit.

Reference: docs/proposals/lancedb-memory-mcp.md and the plan at
docs/plans/2026-05-22-discipline-plugin-and-starter-capture.md in
Lizo-RoadTown/Make_Skills.
"""
import json
import re
import sys

BASE_REMINDER = (
    "Discipline check: PROBE files before asserting (cite file:line). "
    "Distinguish dev-tooling (scripts/, docs/) from runtime (platform/, web/). "
    "Save corrections as feedback memory immediately."
)

PROBE_REMINDER = (
    "PROBE FIRST. The user is asking about the codebase or stack — "
    "run Grep/Read on the relevant file BEFORE answering. "
    "Cite file:line in the response. The 'obvious' answers are the ones that go wrong."
)

BUILD_REMINDER = (
    "Before building: classify the change. Dev-tooling (scripts/, docs/, session memory) "
    "or runtime (platform/api/, web/)? Name which in your response. "
    "Then PROBE the surrounding code BEFORE writing — cite file:line for any pattern you copy."
)

DEBUG_REMINDER = (
    "Debug discipline: PROBE the actual file state first (Grep/Read). "
    "If a skill applies (e.g., systematic-debugging, lessons-learned), invoke it by name. "
    "Don't guess from training-data defaults — the specific project may differ."
)

# Pattern → reminder mapping. First match wins; order matters.
PATTERNS = [
    (re.compile(r"\b(does|do)\b.*\buse\b|where (is|does)|what'?s the stack|which library", re.IGNORECASE), PROBE_REMINDER),
    (re.compile(r"\bfix\b|\bdebug\b|why doesn'?t|broken|failing", re.IGNORECASE), DEBUG_REMINDER),
    (re.compile(r"\b(build|implement|wire(?:\s+up)?|add|create|scaffold)\b", re.IGNORECASE), BUILD_REMINDER),
]


def main() -> int:
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError:
        # Malformed input — emit nothing, don't block.
        return 0

    prompt = data.get("prompt") or ""
    cwd = data.get("cwd") or ""

    # Only fire the reminder in Make_Skills or project-starter-scaffolded repos.
    # A weak heuristic: look at the cwd for the marker. If we can't tell, default
    # to firing the base reminder anyway — over-reminding is cheaper than under-.
    is_make_skills = "Make_Skills" in cwd or "make-skills" in cwd.lower()
    is_starter = "project-starter" in cwd.lower() or "_common" in cwd

    if not (is_make_skills or is_starter):
        # Out of scope. No reminder.
        return 0

    # Pick the most-specific reminder that matches; fall back to base.
    reminder = BASE_REMINDER
    for pattern, msg in PATTERNS:
        if pattern.search(prompt):
            reminder = msg
            break

    payload = {
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": f"[make-skills-discipline] {reminder}",
        }
    }
    print(json.dumps(payload))
    return 0


if __name__ == "__main__":
    sys.exit(main())
