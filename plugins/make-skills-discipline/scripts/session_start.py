#!/usr/bin/env python3
"""
SessionStart hook for make-skills-discipline.

Triggers the architecture-snapshot pipeline:

  1. Runs scripts/architecture_snapshot.py in the project repo
  2. Runs scripts/architecture_diff.py
  3. Emits a short additionalContext block pointing the agent at the new
     diff.md AND requesting it invoke the architecture-analyst subagent to
     produce the narrative report.

Scope-guarded: only fires in Make_Skills or project-starter-scaffolded repos.

The script does NOT write the narrative itself — that's the analyst agent's
job. This script ensures the deterministic snapshot + diff data exists, so
the agent has a real input to interpret.

Errors here MUST be non-fatal (exit 0 with no output) — a broken hook should
never block session start.
"""
from __future__ import annotations

import json
import os
import subprocess
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


def main() -> int:
    start = now_ms()
    log_event("SessionStart", "start")
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError:
        log_event("SessionStart", "end", exit_code=0, elapsed_ms=now_ms() - start, action="noop", note="malformed_input")
        return 0

    cwd = Path(data.get("cwd") or os.getcwd())
    cwd_lower = str(cwd).lower()

    # Scope-guard. Only run in Make_Skills or project-starter-scaffolded repos.
    in_scope = (
        "make_skills" in cwd_lower
        or "make-skills" in cwd_lower
        or "project-starter" in cwd_lower
        or (cwd / "ARCHITECTURE.md").exists() and (cwd / "scripts" / "architecture_snapshot.py").exists()
    )
    if not in_scope:
        log_event("SessionStart", "end", exit_code=0, elapsed_ms=now_ms() - start, scope_in=False, action="noop", note="out_of_scope")
        return 0

    snapshot_script = cwd / "scripts" / "architecture_snapshot.py"
    diff_script = cwd / "scripts" / "architecture_diff.py"
    if not snapshot_script.exists():
        # No scripts installed yet in this repo — silently skip.
        log_event("SessionStart", "end", exit_code=0, elapsed_ms=now_ms() - start, scope_in=True, action="noop", note="snapshot_script_absent")
        return 0

    # Resolve python — prefer system python, fall back to specific paths
    # that work on this machine. Mirrors the strategy used by other hook
    # scripts (the hooks.json invokes us via the same python).
    python_exe = sys.executable

    snapshot_dir = cwd / "docs" / "architecture-snapshots"
    snapshots_before = (
        sorted(snapshot_dir.glob("*-snapshot.json")) if snapshot_dir.exists() else []
    )

    # Run snapshot
    try:
        subprocess.run(
            [python_exe, str(snapshot_script)],
            cwd=str(cwd),
            check=True,
            capture_output=True,
            timeout=20,
        )
    except (subprocess.SubprocessError, OSError):
        log_event("SessionStart", "end", exit_code=0, elapsed_ms=now_ms() - start, scope_in=True, action="noop", note="snapshot_script_error")
        return 0

    # Run diff (only meaningful if we have at least 1 prior, but the diff
    # script handles the no-prior case gracefully).
    try:
        subprocess.run(
            [python_exe, str(diff_script)],
            cwd=str(cwd),
            check=True,
            capture_output=True,
            timeout=20,
        )
    except (subprocess.SubprocessError, OSError):
        # Snapshot worked but diff failed — still proceed; we have the snapshot.
        pass

    # Find what was just written.
    if not snapshot_dir.exists():
        log_event("SessionStart", "end", exit_code=0, elapsed_ms=now_ms() - start, scope_in=True, action="noop", note="snapshot_dir_missing_post_run")
        return 0
    snapshots_after = sorted(snapshot_dir.glob("*-snapshot.json"))
    if not snapshots_after:
        log_event("SessionStart", "end", exit_code=0, elapsed_ms=now_ms() - start, scope_in=True, action="noop", note="no_snapshots_post_run")
        return 0
    new_snapshot = snapshots_after[-1]
    new_diff_md = new_snapshot.with_name(new_snapshot.stem.replace("-snapshot", "-diff") + ".md")
    new_diff_json = new_snapshot.with_name(new_snapshot.stem.replace("-snapshot", "-diff") + ".json")

    rel_snapshot = new_snapshot.relative_to(cwd)
    rel_diff_md = new_diff_md.relative_to(cwd) if new_diff_md.exists() else None
    rel_diff_json = new_diff_json.relative_to(cwd) if new_diff_json.exists() else None

    first_run = len(snapshots_before) == 0

    msg_lines = ["[make-skills-discipline · architecture-snapshot]"]
    if first_run:
        msg_lines.append(f"First snapshot written: {rel_snapshot}.")
        msg_lines.append("No prior to diff against. Future sessions will compare to this baseline.")
    else:
        msg_lines.append(f"Snapshot: {rel_snapshot}")
        if rel_diff_md:
            msg_lines.append(f"Diff:     {rel_diff_md}")
        msg_lines.append("")
        msg_lines.append(
            "Invoke the architecture-analyst subagent (in the make-skills-discipline plugin) "
            "to read the snapshot + diff and produce the narrative report at "
            "docs/architecture-snapshots/<timestamp>-narrative.md. Pass the file paths above as input. "
            "If the diff shows no changes, write the minimal narrative form."
        )

    payload = {
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": "\n".join(msg_lines),
        }
    }
    print(json.dumps(payload))
    log_event(
        "SessionStart", "end",
        exit_code=0, elapsed_ms=now_ms() - start,
        scope_in=True,
        action="snapshot_emitted",
        note=f"first_run={first_run};snapshot={rel_snapshot.name}",
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
