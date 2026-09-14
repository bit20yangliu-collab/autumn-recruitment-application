#!/usr/bin/env python3
"""Build a shareable skill ZIP from an explicit, user-data-free allowlist."""

from __future__ import annotations

import argparse
import sys
import zipfile
from pathlib import Path


ALLOWED_FILES = {
    "SKILL.md",
    "agents/openai.yaml",
    "assets/profile-template.json",
    "references/database-guide.md",
    "references/form-filling.md",
    "references/onboarding.md",
    "scripts/init_profile.py",
    "scripts/package_shareable.py",
    "scripts/preflight.py",
    "scripts/validate_profile.py",
}

IGNORED_PARTS = {"__pycache__"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", help="Destination .zip path")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    skill_dir = Path(__file__).resolve().parent.parent
    output = Path(args.output).expanduser().resolve()

    if output.suffix.lower() != ".zip":
        print("ERROR: output path must end in .zip", file=sys.stderr)
        return 2

    actual_files = {
        path.relative_to(skill_dir).as_posix()
        for path in skill_dir.rglob("*")
        if path.is_file() and not (set(path.parts) & IGNORED_PARTS)
    }
    missing = sorted(ALLOWED_FILES - actual_files)
    unexpected = sorted(actual_files - ALLOWED_FILES)

    if missing:
        print("ERROR: package is missing required files: " + ", ".join(missing), file=sys.stderr)
        return 1
    if unexpected:
        print(
            "ERROR: refusing to package unexpected files: " + ", ".join(unexpected),
            file=sys.stderr,
        )
        return 1

    output.parent.mkdir(parents=True, exist_ok=True)
    root_name = skill_dir.name
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for relative in sorted(ALLOWED_FILES):
            archive.write(skill_dir / relative, f"{root_name}/{relative}")

    print(f"Created shareable ZIP with {len(ALLOWED_FILES)} allowlisted files: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
