#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Heretic Enhanced — single-file launcher.
#
# Usage:
#   py heretic-enhanced.py [arguments...]
#
# This launcher automatically locates and uses the bundled Python 3.12
# environment (inside heretic_enhanced/.venv) that already contains every
# required dependency (torch, transformers, peft, optuna, etc.).
# You never need to manually activate a virtual environment or install
# anything from PyPI.

import os
import subprocess
import sys


def _find_project_dir() -> str:
    """Locate the heretic_enhanced project directory."""
    launcher_dir = os.path.dirname(os.path.abspath(__file__))

    # Project lives in a subdirectory next to this launcher.
    candidate = os.path.join(launcher_dir, "heretic_enhanced")
    if os.path.isfile(os.path.join(candidate, ".venv", "Scripts", "python.exe")):
        return candidate

    # Launcher sits inside the project directory itself.
    if os.path.isfile(os.path.join(launcher_dir, ".venv", "Scripts", "python.exe")):
        return launcher_dir

    return candidate  # best-effort fallback for error messages


def main() -> None:
    project_dir = _find_project_dir()
    venv_python = os.path.join(project_dir, ".venv", "Scripts", "python.exe")

    if not os.path.exists(venv_python):
        sys.stderr.write(
            "ERROR: Could not find the bundled Python environment.\n"
            f"  Looked for: {venv_python}\n"
            "The '.venv' directory inside the project folder is required.\n"
        )
        sys.exit(1)

    # Run "python -m heretic <args>" from the project directory so that
    # config.toml, checkpoints, etc. are resolved relative to the project root.
    os.chdir(project_dir)
    cmd = [venv_python, "-m", "heretic"] + sys.argv[1:]
    raise SystemExit(subprocess.call(cmd))


if __name__ == "__main__":
    main()