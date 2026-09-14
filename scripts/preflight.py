#!/usr/bin/env python3
"""Check that the shareable skill package is complete without reading user data."""

from __future__ import annotations

import sys
from pathlib import Path


REQUIRED_FILES = (
    "SKILL.md",
    "agents/openai.yaml",
    "assets/profile-template.json",
    "references/onboarding.md",
    "references/database-guide.md",
    "references/form-filling.md",
    "scripts/init_profile.py",
    "scripts/package_shareable.py",
    "scripts/validate_profile.py",
)


def main() -> int:
    skill_dir = Path(__file__).resolve().parent.parent
    missing = [item for item in REQUIRED_FILES if not (skill_dir / item).is_file()]

    if missing:
        print("ERROR: incomplete skill package: " + ", ".join(missing), file=sys.stderr)
        return 1

    print("Skill package is complete.")
    print("No third-party Python packages are required.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
