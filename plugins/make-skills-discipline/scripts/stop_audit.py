#!/usr/bin/env python3
"""
Stop hook for make-skills-discipline.

Fires at the end of the agent's turn. Audits the recent transcript for
unsubstantiated stack claims — phrases like "we use X" / "stack is Y" /
"runs on Z" — that lack any corresponding file:line citation in the same
turn. If found, injects a corrective reminder pointing the agent at the
next response to verify and amend.

Does NOT block (Stop hook blocking is dangerous; would loop). Emits a
soft reminder via additionalContext so the next user message sees it.

Reads transcript_path from input JSON. Only scans the LAST assistant
turn — not the whole history, to keep the heuristic local.

Reference: docs/plans/2026-05-22-discipline-plugin-and-starter-capture.md
in Lizo-RoadTown/Make_Skills.
"""
import json
import re
import sys
import time
from pathlib import Path

# v0.1.4: absolute-path importlib. See pre_tool_use.py header comment.
import importlib.util as _importlib_util

_obs_path = Path(__file__).resolve().parent / "_observability.py"
_obs_spec = _importlib_util.spec_from_file_location("_observability", _obs_path)
if _obs_spec is not None and _obs_spec.loader is not None:
    _obs_mod = _importlib_util.module_from_spec(_obs_spec)
    try:
        _obs_spec.loader.exec_module(_obs_mod)
        log_event = _obs_mod.log_event
        now_ms = _obs_mod.now_ms
    except Exception as _obs_err:  # noqa: BLE001
        _fallback_log = Path.home() / ".claude" / "logs" / "hook-import-errors.log"
        try:
            _fallback_log.parent.mkdir(parents=True, exist_ok=True)
            with _fallback_log.open("a", encoding="utf-8") as _flog:
                _flog.write(
                    f"{Path(__file__).name}: _observability exec_module failed: {_obs_err!r}\n"
                )
        except Exception:  # noqa: BLE001
            pass

        def log_event(*_args, **_kwargs):
            pass

        def now_ms() -> int:
            return int(time.time() * 1000)
else:
    _fallback_log = Path.home() / ".claude" / "logs" / "hook-import-errors.log"
    try:
        _fallback_log.parent.mkdir(parents=True, exist_ok=True)
        with _fallback_log.open("a", encoding="utf-8") as _flog:
            _flog.write(
                f"{Path(__file__).name}: _observability spec_from_file_location "
                f"returned None for path={_obs_path}\n"
            )
    except Exception:  # noqa: BLE001
        pass

    def log_event(*_args, **_kwargs):
        pass

    def now_ms() -> int:
        return int(time.time() * 1000)

# Heuristic: phrases that smell like factual claims about the stack/codebase.
SUSPICIOUS_CLAIM = re.compile(
    r"\b(?:we use|uses|stack is|backed by|runs on|stored in|implemented in|built on|written in|deployed on)\s+"
    r"([A-Z][A-Za-z][A-Za-z0-9._-]+)",
    re.IGNORECASE,
)

CITATION_REGEX = re.compile(
    r"[a-zA-Z_/\\.\-]+\.(py|ts|tsx|jsx|js|md|json|yaml|yml|toml|sh|ps1|sql):\d+"
)

REMINDER = (
    "Stop-audit detected an unsubstantiated stack claim in your last response: "
    "claims about what the project uses or runs on, but no file:line citation. "
    "In your next response, either verify with Grep/Read and amend the claim with "
    "a citation, or retract it. The PROBE rule applies retroactively."
)


def main() -> int:
    start = now_ms()
    log_event("Stop", "start")
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError:
        log_event("Stop", "end", exit_code=0, elapsed_ms=now_ms() - start, action="noop", note="malformed_input")
        return 0

    cwd = data.get("cwd") or ""
    transcript_path = data.get("transcript_path") or ""

    in_scope = "Make_Skills" in cwd or "project-starter" in cwd.lower() or "_common" in cwd
    if not in_scope:
        log_event("Stop", "end", exit_code=0, elapsed_ms=now_ms() - start, scope_in=False, action="noop", note="out_of_scope")
        return 0

    if not transcript_path:
        log_event("Stop", "end", exit_code=0, elapsed_ms=now_ms() - start, scope_in=True, action="noop", note="no_transcript_path")
        return 0

    try:
        raw = Path(transcript_path).read_text(encoding="utf-8", errors="ignore")
    except OSError:
        log_event("Stop", "end", exit_code=0, elapsed_ms=now_ms() - start, scope_in=True, action="noop", note="transcript_unreadable")
        return 0

    # Transcripts are JSONL. Find the last assistant turn.
    last_assistant_text = ""
    for line in raw.splitlines()[::-1]:
        line = line.strip()
        if not line:
            continue
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            continue
        # Heuristic: assistant entries have role="assistant" or type="message"
        # with author="assistant". Adjust if Claude Code's format differs.
        role = entry.get("role") or (entry.get("message") or {}).get("role") or ""
        if role == "assistant":
            # Extract text content.
            content = entry.get("content") or (entry.get("message") or {}).get("content") or []
            if isinstance(content, list):
                parts = []
                for block in content:
                    if isinstance(block, dict) and block.get("type") == "text":
                        parts.append(block.get("text") or "")
                last_assistant_text = "\n".join(parts)
            elif isinstance(content, str):
                last_assistant_text = content
            break

    if not last_assistant_text:
        log_event("Stop", "end", exit_code=0, elapsed_ms=now_ms() - start, scope_in=True, action="noop", note="no_assistant_turn_found")
        return 0

    claims = SUSPICIOUS_CLAIM.findall(last_assistant_text)
    cited = bool(CITATION_REGEX.search(last_assistant_text))

    if claims and not cited:
        payload = {
            "hookSpecificOutput": {
                "hookEventName": "Stop",
                "additionalContext": (
                    f"[make-skills-discipline] {REMINDER}\n"
                    f"Detected claims: {', '.join(set(claims))[:200]}"
                ),
            }
        }
        print(json.dumps(payload))
        log_event("Stop", "end", exit_code=0, elapsed_ms=now_ms() - start, scope_in=True, action="reminder_injected", note=f"claims={len(claims)};cited=False")
    else:
        log_event("Stop", "end", exit_code=0, elapsed_ms=now_ms() - start, scope_in=True, action="noop", note=f"claims={len(claims)};cited={cited}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
