#!/usr/bin/env python3
"""PostToolUse hook: lint/format/type-check a .py file right after Claude edits it."""

import json
import shutil
import subprocess
import sys
from pathlib import Path


def main() -> int:
    payload = json.load(sys.stdin)
    file_path = payload.get("tool_input", {}).get("file_path")
    if not file_path:
        return 0

    path = Path(file_path)
    if path.suffix != ".py" or not path.is_file():
        return 0

    project_dir = Path(payload.get("cwd") or Path.cwd())

    commands = [
        ["ruff", "check", "--fix", str(path)],
        ["ruff", "format", str(path)],
        ["mypy", str(path)],
    ]

    output = []
    missing = set()
    for command in commands:
        tool = command[0]
        if shutil.which(tool) is None:
            missing.add(tool)
            continue
        result = subprocess.run(
            command,
            cwd=project_dir,
            capture_output=True,
            text=True,
        )
        text = (result.stdout + result.stderr).strip()
        if text:
            output.append(f"$ {' '.join(command)}\n{text}")

    if missing:
        output.append(f"(skipped, not on PATH: {', '.join(sorted(missing))})")

    if output:
        print("\n\n".join(output))

    return 0


if __name__ == "__main__":
    sys.exit(main())
