#!/usr/bin/env python3
"""Create an empty portable job-application profile without overwriting user data."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "workspace",
        nargs="?",
        default=".",
        help="Workspace in which job-application-profile will be created.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    skill_dir = Path(__file__).resolve().parent.parent
    template = skill_dir / "assets" / "profile-template.json"
    profile_dir = Path(args.workspace).expanduser().resolve() / "job-application-profile"
    profile_path = profile_dir / "profile.json"

    if not template.is_file():
        print(f"ERROR: profile template is missing: {template}")
        return 1

    (profile_dir / "assets").mkdir(parents=True, exist_ok=True)
    (profile_dir / "sources").mkdir(parents=True, exist_ok=True)

    if profile_path.exists():
        print(f"Profile already exists; left unchanged: {profile_path}")
        return 0

    shutil.copyfile(template, profile_path)
    print(f"Created empty profile: {profile_path}")
    print("Created assets and sources directories.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
