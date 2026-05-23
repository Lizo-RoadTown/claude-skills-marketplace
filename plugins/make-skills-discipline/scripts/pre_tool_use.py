#!/usr/bin/env python3
"""
PreToolUse hook for make-skills-discipline.

Fires before Edit / Write / MultiEdit. Checks two conditions:

1. **Citation requirement.** If the agent is about to write to platform/api/
   or web/ (runtime code) AND the recent transcript shows no file:line
   citation, inject a corrective reminder (without blocking).

2. **Dev-tooling-vs-runtime classification.** If the edit target is a
   shared-interface boundary (e.g., the dual-mode discipline), inject a
   reminder to classify in the response.

Does NOT block by default — emits additionalContext as a soft reminder.
Set DISCIPLINE_STRICT=1 in the environment to make these checks blocking.

Reads the transcript path from the input JSON; if absent or unreadable,
exits 0 with no output. Never crash the harness over a missing transcript.

Reference: docs/plans/2026-05-22-discipline-plugin-and-starter-capture.md
in Lizo-RoadTown/Make_Skills.
"""
import json
import os
import re
import sys
import time
from pathlib import Path

# Shared observability helper (v0.1.2+).
sys.path.insert(0, str(Path(__file__).resolve().parent))
try:
    from _observability import log_event, now_ms
except Exception:  # noqa: BLE001
    def log_event(*_args, **_kwargs):
        pass

    def now_ms() -> int:
        return int(time.time() * 1000)

CITATION_REGEX = re.compile(
    r"[a-zA-Z_/\\.\-]+\.(py|ts|tsx|jsx|js|md|json|yaml|yml|toml|sh|ps1|sql):\d+"
)

RUNTIME_PATHS = ("platform/", "platform\\", "web/", "web\\")

CITATION_REMINDER = (
    "PreToolUse check: about to edit runtime code without recent file:line citation. "
    "Either cite the source you're following (file:line) in this turn's earlier output, "
    "or pause and PROBE before writing. The discipline says cite-then-edit."
)

DUAL_MODE_REMINDER = (
    "PreToolUse check: this edit touches a tenant-scoped or dual-mode boundary. "
    "Confirm in your response that the change is correct for BOTH self-host and "
    "hosted-multitenant modes (per ARCHITECTURE.md and CONTRIBUTING.md)."
)

DUAL_MODE_TRIGGERS = (
    # Tightened in v0.1.2: removed "memory" and "tenant" (caused frequent
    # false positives on session memory writes and any docs mentioning tenants).
    # Keep only patterns specific to actual runtime tenant-scoping code.
    "tenant_id",
    "RLS",
    "current_setting('app.tenant",
    "AUTH_SECRET",
    "JWTTenantResolver",
    "set_config('app.tenant",
)


def looks_like_runtime(path: str) -> bool:
    return any(marker in path for marker in RUNTIME_PATHS)


def has_recent_citation(transcript_path: str) -> bool:
    if not transcript_path:
        return True  # Can't verify; don't false-alarm.
    try:
        text = Path(transcript_path).read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return True
    # Look at the tail — last ~5k chars covers a few turns.
    tail = text[-5000:]
    return bool(CITATION_REGEX.search(tail))


def touches_dual_mode(tool_input: dict) -> bool:
    blob = json.dumps(tool_input, default=str)
    return any(trigger in blob for trigger in DUAL_MODE_TRIGGERS)


def emit_reminder(text: str) -> None:
    payload = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "additionalContext": f"[make-skills-discipline] {text}",
        }
    }
    print(json.dumps(payload))


def emit_block(reason: str) -> None:
    payload = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": f"[make-skills-discipline] {reason}",
        }
    }
    print(json.dumps(payload))


def main() -> int:
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0

    tool_name = data.get("tool_name") or ""
    tool_input = data.get("tool_input") or {}
    transcript_path = data.get("transcript_path") or ""
    cwd = data.get("cwd") or ""

    # Only police Make_Skills and project-starter-scaffolded repos.
    in_scope = "Make_Skills" in cwd or "project-starter" in cwd.lower() or "_common" in cwd
    if not in_scope:
        return 0

    if tool_name not in ("Edit", "Write", "MultiEdit"):
        return 0

    target = (
        tool_input.get("file_path")
        or tool_input.get("path")
        or tool_input.get("filePath")
        or ""
    )

    strict = os.environ.get("DISCIPLINE_STRICT", "") == "1"

    # Check 1: runtime edit without citation
    if looks_like_runtime(target) and not has_recent_citation(transcript_path):
        if strict:
            emit_block(
                f"Editing runtime file {target} without a recent file:line citation. "
                "Run Grep/Read to ground the change, cite it, then retry."
            )
            return 2
        emit_reminder(CITATION_REMINDER)
        return 0

    # Check 2: dual-mode boundary touch
    if touches_dual_mode(tool_input):
        emit_reminder(DUAL_MODE_REMINDER)
        return 0

    # No issue.
    return 0


if __name__ == "__main__":
    sys.exit(main())
