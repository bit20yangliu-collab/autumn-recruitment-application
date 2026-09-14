#!/usr/bin/env python3
"""Validate the portable job-application profile without printing sensitive values."""

from __future__ import annotations

import json
import sys
from pathlib import Path


REQUIRED_TOP_LEVEL = {
    "schema_version",
    "sources",
    "personal",
    "contact",
    "assets",
    "education",
    "internships",
    "honors",
    "skills",
    "family",
    "pending_confirmation_fields",
    "automation_policy",
}

REQUIRED_AUTOMATION_POLICY = {
    "allow_read_and_fill",
    "allow_file_upload_from_assets",
    "website_request_authorizes_immediate_fill",
    "sensitive_data_confirmation_mode",
    "require_user_for_login_captcha_and_2fa",
    "allow_save_draft_and_next_page",
    "require_user_confirmation_before_final_submit",
    "explicit_submit_request_waives_repeat_confirmation",
    "never_guess_missing_personal_data",
}


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: validate_profile.py <profile.json>", file=sys.stderr)
        return 2

    path = Path(sys.argv[1]).expanduser().resolve()
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print(f"ERROR: profile not found: {path}", file=sys.stderr)
        return 1
    except json.JSONDecodeError as exc:
        print(f"ERROR: invalid JSON at line {exc.lineno}, column {exc.colno}", file=sys.stderr)
        return 1

    missing = sorted(REQUIRED_TOP_LEVEL - set(data))
    if missing:
        print("ERROR: missing top-level sections: " + ", ".join(missing), file=sys.stderr)
        return 1

    if not isinstance(data["pending_confirmation_fields"], list):
        print("ERROR: pending_confirmation_fields must be a list", file=sys.stderr)
        return 1

    automation_policy = data["automation_policy"]
    if not isinstance(automation_policy, dict):
        print("ERROR: automation_policy must be an object", file=sys.stderr)
        return 1

    missing_policy = sorted(REQUIRED_AUTOMATION_POLICY - set(automation_policy))
    legacy_profile = str(data.get("schema_version")) == "1.0"
    if missing_policy and not legacy_profile:
        print(
            "ERROR: missing automation policy fields: " + ", ".join(missing_policy),
            file=sys.stderr,
        )
        return 1

    missing_assets = []
    for key in ("resume_primary", "resume_pdf_v5", "portrait_primary", "life_photo"):
        value = data.get("assets", {}).get(key)
        if not value:
            continue
        asset_path = Path(value).expanduser()
        if not asset_path.is_absolute():
            asset_path = path.parent / asset_path
        if not asset_path.exists():
            missing_assets.append(key)

    print("Profile JSON is valid.")
    if missing_policy:
        print("WARNING: legacy profile policy can be upgraded from the current template.")
    print(f"Pending confirmation fields: {len(data['pending_confirmation_fields'])}")
    if missing_assets:
        print("WARNING: missing asset paths for: " + ", ".join(missing_assets))
        return 3
    print("Referenced core assets exist or are not yet configured.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
