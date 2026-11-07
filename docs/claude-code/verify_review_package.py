#!/usr/bin/env python3
"""Offline static check for the unenabled Claude Code review package.

This script does not call Claude, GitHub, Firebase, LINE, or any network.
The only sample record is the fictional one declared below. It is not read
from index.html and must not be treated as customer or payroll data.
"""

from __future__ import annotations

import hashlib
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TEMPLATE = ROOT / "docs" / "claude-code" / "templates" / "claude.yml.example"
REVIEW = ROOT / "docs" / "claude-code" / "REVIEW.md"
CLAUDE = ROOT / "CLAUDE.md"
INDEX = ROOT / "index.html"

# Clearly fictional. Not loaded from the application or its cloud data.
FICTIONAL_SAMPLE = {
    "label": "虛構資料",
    "person": "示範人員甲",
    "month": "209901",
    "amount": 0,
    "source": "offline-static-review-package",
}

FORBIDDEN_TRIGGERS = ("push", "pull_request", "pull_request_target", "schedule", "workflow_dispatch")


def fail(message: str) -> None:
    print(f"FAIL {message}")
    sys.exit(1)


def git_show_main_index() -> bytes:
    result = subprocess.run(
        ["git", "show", "main:index.html"],
        cwd=ROOT,
        check=False,
        capture_output=True,
    )
    if result.returncode != 0:
        fail("cannot read main:index.html for comparison")
    return result.stdout


def workflow_files() -> list[Path]:
    workflow_dir = ROOT / ".github" / "workflows"
    if not workflow_dir.exists():
        return []
    found: list[Path] = []
    for path in workflow_dir.rglob("*"):
        if path.is_file() and path.suffix.lower() in {".yml", ".yaml"}:
            found.append(path)
    return found


def uncommented_auth_lines(text: str) -> list[str]:
    hits: list[str] = []
    pattern = re.compile(r"^\s*(anthropic_api_key|claude_code_oauth_token)\s*:")
    for line in text.splitlines():
        stripped = line.lstrip()
        if stripped.startswith("#"):
            continue
        if pattern.match(line):
            hits.append(stripped)
    return hits


def trigger_names(template_text: str) -> list[str]:
    try:
        import yaml
    except ImportError:
        names: list[str] = []
        in_on = False
        for raw in template_text.splitlines():
            if raw.startswith("on:"):
                in_on = True
                continue
            if in_on and raw and not raw.startswith(" "):
                break
            if in_on:
                match = re.match(r"^\s{2}([A-Za-z0-9_]+):", raw)
                if match:
                    names.append(match.group(1))
        return names

    loaded = yaml.safe_load(template_text)
    if not isinstance(loaded, dict):
        fail("template is not a mapping")
    # PyYAML 1.1 parses the GitHub Actions key "on" as boolean true.
    trigger_map = loaded.get("on")
    if trigger_map is None:
        trigger_map = loaded.get(True)
    if not isinstance(trigger_map, dict):
        fail("template has no mapping under on")
    triggers = list(trigger_map.keys())
    job = loaded.get("jobs", {}).get("claude", {})
    if job.get("if") != "${{ false }}":
        fail("template review guard is not exactly false")
    return triggers


def main() -> None:
    if FICTIONAL_SAMPLE["label"] != "虛構資料" or FICTIONAL_SAMPLE["amount"] != 0:
        fail("fictional sample marker was altered")
    if "客戶" in FICTIONAL_SAMPLE["person"] or "真實" in FICTIONAL_SAMPLE["person"]:
        fail("fictional sample must stay explicitly fictional")

    workflows = workflow_files()
    if workflows:
        fail("executable workflow files exist: " + ", ".join(str(p.relative_to(ROOT)) for p in workflows))

    for required in (TEMPLATE, REVIEW, CLAUDE, INDEX):
        if not required.is_file():
            fail(f"missing {required.relative_to(ROOT)}")

    template = TEMPLATE.read_text(encoding="utf-8")
    if "REVIEW GUARD" not in template or "if: ${{ false }}" not in template:
        fail("disabled review guard missing from template")
    auth_hits = uncommented_auth_lines(template)
    if auth_hits:
        fail("authentication input is uncommented")
    triggers = trigger_names(template)
    overlap = sorted(set(triggers) & set(FORBIDDEN_TRIGGERS))
    if overlap:
        fail("template contains forbidden triggers: " + ", ".join(overlap))
    if "anthropics/claude-code-action@v1" not in template:
        fail("template is not the reviewed action reference")

    for doc in (REVIEW, CLAUDE, ROOT / "README.md"):
        text = doc.read_text(encoding="utf-8")
        if "{{" in text:
            fail(f"{doc.relative_to(ROOT)} contains expression braces")

    current = INDEX.read_bytes()
    baseline = git_show_main_index()
    if current != baseline:
        fail("index.html differs from main")

    digest = hashlib.sha256(current).hexdigest()[:12]
    print("PASS review package is disabled and index.html matches main")
    print(f"index_sha256_12={digest}")
    print(
        "fictional_sample "
        f"label={FICTIONAL_SAMPLE['label']} "
        f"person={FICTIONAL_SAMPLE['person']} "
        f"month={FICTIONAL_SAMPLE['month']} "
        f"amount={FICTIONAL_SAMPLE['amount']} "
        f"source={FICTIONAL_SAMPLE['source']}"
    )
    print("production_data_loaded=no")
    print("claude_executed=no")
    print("workflow_files=0")


if __name__ == "__main__":
    main()
