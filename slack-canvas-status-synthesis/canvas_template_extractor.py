#!/usr/bin/env python3
"""
Extract a reusable status-report template from a Slack canvas.

Claude reads the source canvas and returns sanitized JSON. This wrapper writes
that JSON to disk, so Claude does not need local filesystem write permissions.
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import re
import shutil
import subprocess
import sys
from datetime import date, datetime
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_TEMPLATE_DIR = SCRIPT_DIR / ".canvas_templates"
DEFAULT_TIMEOUT_SECONDS = 180
DEFAULT_ALLOWED_TOOLS = "slack_read_canvas"
SAFE_TEMPLATE_NAME = re.compile(r"^[A-Za-z0-9_.-]+$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Extract a reusable JSON template from a Slack canvas.")
    parser.add_argument("canvas_id", help="Slack canvas ID to read, for example F0ABC123456")
    parser.add_argument("template_name", help="Template name without .json")
    parser.add_argument("--template-dir", default=str(DEFAULT_TEMPLATE_DIR), help="Directory for extracted templates")
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT_SECONDS, help="Claude timeout in seconds")
    parser.add_argument("--save-prompt", help="Write the generated prompt to this path before calling Claude")
    parser.add_argument("--dry-run", action="store_true", help="Print the prompt and exit without calling Claude")
    parser.add_argument("--allow-sensitive-examples", action="store_true", help="Allow representative source examples. Off by default")
    return parser.parse_args()


def validate_template_name(template_name: str) -> None:
    if not SAFE_TEMPLATE_NAME.match(template_name) or "/" in template_name or ".." in template_name:
        raise ValueError("Template name must use only letters, numbers, dots, dashes, or underscores.")


def resolve_claude_bin() -> str:
    candidates = [os.environ.get("CLAUDE_BIN"), shutil.which("claude"), str(Path.home() / ".aisuite" / "bin" / "claude")]
    for candidate in candidates:
        if not candidate:
            continue
        expanded = Path(candidate).expanduser()
        if expanded.exists() or shutil.which(candidate):
            return str(expanded if expanded.exists() else candidate)
    raise RuntimeError("Claude CLI not found. Set CLAUDE_BIN or make sure `claude` is on your PATH.")


def build_claude_command(prompt: str) -> list[str]:
    cmd: list[str] = []
    if platform.system() == "Darwin" and os.environ.get("NO_CAFFEINATE") != "1" and shutil.which("caffeinate"):
        cmd.extend(["caffeinate", "-s"])
    cmd.append(resolve_claude_bin())

    allowed_tools = os.environ.get("CLAUDE_ALLOWED_TOOLS", DEFAULT_ALLOWED_TOOLS).strip()
    if allowed_tools and allowed_tools.lower() != "none":
        cmd.extend(["--allowedTools", allowed_tools])
    if os.environ.get("CLAUDE_BYPASS_PERMISSIONS") == "1":
        cmd.extend(["--permission-mode", "bypassPermissions"])
    cmd.extend(["-p", prompt])
    return cmd


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def template_schema(template_name: str, canvas_id: str) -> dict[str, Any]:
    return {
        "template_name": template_name,
        "source_canvas_id": canvas_id,
        "extracted_date": date.today().isoformat(),
        "title_format": "{{program_name}} - {{date}}, Status: :{{status_emoji}}: {{status_text}}",
        "summary": "One-sentence description of what this status format is for.",
        "sections": [
            {
                "name": "Highlights",
                "required": True,
                "format": "bullet_list",
                "style": "* {{content}}",
                "content_guidelines": "3-5 specific accomplishments, milestones, or changes",
                "default_empty": "No source signal found.",
            },
            {
                "name": "Risks / Blockers",
                "required": True,
                "format": "bullet_list",
                "content_guidelines": "Only include risks supported by source material. Include owner and next step when present.",
                "default_empty": "No new risks found in source material.",
            },
        ],
        "emoji_dictionary": {
            "green-dot": {"meaning": "On track", "usage": "status_indicator"},
            "yellow-dot": {"meaning": "At risk", "usage": "status_indicator"},
            "red-dot": {"meaning": "Blocked", "usage": "status_indicator"},
        },
        "formatting_rules": {
            "date_format": "Month Day, Year",
            "work_items": "Use source ticket IDs only. Do not invent IDs.",
            "metrics": "Use exact numbers from source material only.",
            "tone": "Professional, concise, factual",
        },
        "data_sources": {"lookback_days": 7},
        "stakeholder_pattern": "Describe mention format and ordering without preserving private names.",
        "review_checklist": ["Verify dates", "Verify metrics", "Verify owners", "Verify ticket IDs", "Verify Red / Yellow / Green status"],
        "failure_modes": ["Source channels are mostly chatter", "Decisions happen outside Slack", "Owners or dates are missing from source material"],
    }


def build_prompt(canvas_id: str, template_name: str, allow_sensitive_examples: bool) -> str:
    privacy_rule = (
        "You may preserve representative examples from the source canvas only when needed to understand the template."
        if allow_sensitive_examples
        else "Do not copy confidential content. Replace program names, customer names, person names, ticket IDs, links, dates, and metrics with placeholders."
    )
    schema = json.dumps(template_schema(template_name, canvas_id), indent=2)
    return f"""You are helping a Technical Program Manager extract a reusable status-reporting template from a Slack canvas.

Read Slack canvas `{canvas_id}` using `slack_read_canvas` and return a sanitized JSON template.

Important boundary:
You are not writing a status report. You are extracting reusable structure.

Privacy rule:
{privacy_rule}

Analyze the canvas for:

1. Overall format
   - Title pattern
   - Section order
   - Header hierarchy
   - Status language
   - Emoji usage and meaning

2. Section templates
   - Section name
   - Required vs optional
   - Bullet, table, or paragraph style
   - Default wording when no content exists
   - Formatting rules that matter

3. Content patterns
   - Date format
   - Metric format
   - Ticket or work item format
   - Owner format
   - Risk, blocker, and escalation language

4. Stakeholder handling
   - Mention pattern
   - Ordering pattern
   - Do not preserve actual names unless explicitly needed

Use this JSON shape as the target. Adapt the sections to match the actual canvas:

{schema}

Rules:
- Extract the actual structure from the canvas. Do not invent a better one.
- If a pattern is unclear, mark it as unclear rather than guessing.
- Do not include confidential narrative content unless it is necessary to explain structure.
- Do not invent dates, ticket IDs, owner names, links, or metrics.
- Return valid JSON only.
- Do not wrap the JSON in a Markdown code block.
- Do not include commentary before or after the JSON.
"""


def run_claude(prompt: str, timeout: int) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        build_claude_command(prompt),
        stdin=subprocess.DEVNULL,
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
    )


def extract_json(text: str) -> dict[str, Any]:
    stripped = text.strip()
    stripped = re.sub(r"^```(?:json)?\s*", "", stripped)
    stripped = re.sub(r"\s*```$", "", stripped)
    start = stripped.find("{")
    end = stripped.rfind("}")
    if start == -1 or end == -1 or end < start:
        raise ValueError("Claude did not return a JSON object.")
    parsed = json.loads(stripped[start : end + 1])
    if not isinstance(parsed, dict):
        raise ValueError("Claude returned JSON, but not a JSON object.")
    return parsed


def main() -> int:
    args = parse_args()
    try:
        validate_template_name(args.template_name)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    template_dir = Path(args.template_dir).expanduser().resolve()
    output_path = template_dir / f"{args.template_name}.json"
    prompt = build_prompt(args.canvas_id, args.template_name, args.allow_sensitive_examples)

    if args.save_prompt:
        write_text(Path(args.save_prompt).expanduser(), prompt)
        print(f"Prompt saved to: {args.save_prompt}")
    if args.dry_run:
        print(prompt)
        return 0

    print(f"[{datetime.now().isoformat(timespec='seconds')}] Extracting template from canvas {args.canvas_id}")
    print(f"Template name: {args.template_name}")
    print(f"Output: {output_path}")
    print("")

    try:
        result = run_claude(prompt, args.timeout)
    except subprocess.TimeoutExpired:
        print(f"ERROR: Template extraction timed out after {args.timeout} seconds", file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    if result.returncode != 0:
        print("ERROR: Template extraction failed", file=sys.stderr)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        if result.stdout:
            print(result.stdout, file=sys.stderr)
        return result.returncode

    try:
        template = extract_json(result.stdout)
    except Exception as exc:
        print(f"ERROR: Could not parse template JSON: {exc}", file=sys.stderr)
        print("Claude output was:", file=sys.stderr)
        print(result.stdout, file=sys.stderr)
        return 1

    template["template_name"] = args.template_name
    template["source_canvas_id"] = args.canvas_id
    template.setdefault("extracted_date", date.today().isoformat())
    write_text(output_path, json.dumps(template, indent=2, sort_keys=True) + "\n")

    print("Template extracted successfully.")
    print(f"Location: {output_path}")
    print("")
    print("To use this template:")
    print(f"  ./canvas_generator_from_template.py {args.template_name} <channel_ids|none> <canvas_ids|none>")
    print("")
    print("Review the JSON before using it. Extracted structure can still carry internal names or assumptions.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
