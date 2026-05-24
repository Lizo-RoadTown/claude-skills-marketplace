"""
Shared observability helper for make-skills-discipline hook scripts.

Each hook calls log_event() to append a single JSON line to
${CLAUDE_PROJECT_DIR}/.claude/logs/hooks.jsonl (or ~/.claude/logs/hooks.jsonl
if CLAUDE_PROJECT_DIR is unset). Records:

  {
    "ts": "<iso8601>",
    "hook": "<event_name>",
    "phase": "start" | "end",
    "exit_code": int (end only),
    "elapsed_ms": int (end only),
    "scope_in": bool,        // did the hook decide it was in-scope
    "action": str | null,    // what the hook did (e.g. "reminder_injected", "block", "noop")
    "note": str | null       // optional one-line detail
  }

Never raises. If logging fails, the hook continues.
"""
from __future__ import annotations

import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path


def _log_dir() -> Path:
    base = os.environ.get("CLAUDE_PROJECT_DIR")
    if base:
        d = Path(base) / ".claude" / "logs"
    else:
        d = Path.home() / ".claude" / "logs"
    try:
        d.mkdir(parents=True, exist_ok=True)
    except OSError:
        # Can't create — fall back to /tmp-ish location; if even that fails,
        # the caller will see no log file but the hook keeps running.
        d = Path(os.environ.get("TEMP") or "/tmp") / "claude-hooks"
        try:
            d.mkdir(parents=True, exist_ok=True)
        except OSError:
            pass
    return d


def log_event(
    hook: str,
    phase: str,
    *,
    scope_in: bool | None = None,
    action: str | None = None,
    note: str | None = None,
    exit_code: int | None = None,
    elapsed_ms: int | None = None,
) -> None:
    """Append one JSON line. Never raises."""
    try:
        entry = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "hook": hook,
            "phase": phase,
        }
        if scope_in is not None:
            entry["scope_in"] = scope_in
        if action is not None:
            entry["action"] = action
        if note is not None:
            entry["note"] = note
        if exit_code is not None:
            entry["exit_code"] = exit_code
        if elapsed_ms is not None:
            entry["elapsed_ms"] = elapsed_ms
        path = _log_dir() / "hooks.jsonl"
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
    except Exception:  # noqa: BLE001
        # Observability MUST NOT break hooks. Swallow everything.
        pass


# Wall-clock helper for elapsed_ms.
def now_ms() -> int:
    return int(time.time() * 1000)
