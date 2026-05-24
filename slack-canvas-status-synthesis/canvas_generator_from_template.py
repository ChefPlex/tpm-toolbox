#!/usr/bin/env python3
"""
Generate a draft status report from Slack sources using an extracted template.

Claude reads the selected Slack channels and canvases, then returns draft text.
This wrapper writes the local draft file, so Claude does not need filesystem
write permissions.
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
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_TEMPLATE_DIR = SCRIPT_DIR / ".canvas_templates"
DEFAULT_TIMEOUT_SECONDS = 300
DEFAULT_ALLOWED_TOOLS = "slack_read_channel,slack_read_canvas"
SAFE_TEMPLATE_NAME = re.compile(r"^[A-Za-z0-9_.-]+$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a draft status report from Slack channels and canvases.")
    parser.add_argument("template_name", help="Template name without .json")
    parser.add_argument("channels", help="Comma-separated Slack channel IDs, or 'none'")
    parser.add_argument("canvases", help="Comma-separated Slack canvas IDs, or 'none'")
    parser.add_argument("--output", help="Output draft path. Default: <template_name>_draft.md")
    parser.add_argument("--lookback", type=int, help="Days to look back. Default comes from the template, then 7")
    parser.add_argument("--template-dir", default=str(DEFAULT_TEMPLATE_DIR), help="Directory containing extracted templates")
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT_SECONDS, help="Claude timeout in seconds")
    parser.add_argument("--save-prompt", help="Write the generated prompt to this path before calling Claude")
    parser.add_argument("--dry-run", action="store_true", help="Print the prompt and exit without calling Claude")
    return parser.parse_args()


def validate_template_name(template_name: str) -> None:
    if not SAFE_TEMPLATE_NAME.match(template_name) or "/" in template_name or ".." in template_name:
        raise ValueError("Template name must use only letters, numbers, dots, dashes, or underscores.")


def parse_id_list(raw_value: str) -> list[str]:
    if raw_value.strip().lower() == "none":
        return []
    return [item.strip() for item in raw_value.split(",") if item.strip()]


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


def load_template(template_name: str, template_dir: Path) -> dict[str, Any]:
    template_path = template_dir / f"{template_name}.json"
    if not template_path.exists():
        raise FileNotFoundError(f"Template not found: {template_path}")
    with template_path.open("r", encoding="utf-8") as template_file:
        data = json.load(template_file)
    if not isinstance(data, dict):
        raise ValueError(f"Template must be a JSON object: {template_path}")
    return data


def list_templates(template_dir: Path) -> list[str]:
    if not template_dir.exists():
        return []
    return sorted(path.stem for path in template_dir.glob("*.json"))


def format_id_block(label: str, ids: list[str], instruction: str) -> str:
    if not ids:
        return f"**{label}:** None provided."
    joined_ids = "\n".join(f"- `{item}`" for item in ids)
    return f"""**{label} ({len(ids)}):**
{instruction}
{joined_ids}"""


def format_sections(template: dict[str, Any]) -> str:
    sections = template.get("sections", [])
    if not sections:
        return "No sections were found in the template. Preserve the source template structure as best as possible."
    rendered: list[str] = []
    for index, section in enumerate(sections, start=1):
        if not isinstance(section, dict):
            continue
        required = "required" if section.get("required", False) else "optional"
        lines = [f"{index}. {section.get('name', 'Unnamed section')} ({required})", f"   - Format: {section.get('format', 'text')}"]
        if section.get("style"):
            lines.append(f"   - Style: {section['style']}")
        if section.get("content_guidelines"):
            lines.append(f"   - Guidance: {section['content_guidelines']}")
        if section.get("default_empty"):
            lines.append(f"   - Default if empty: {section['default_empty']}")
        if section.get("subsections"):
            lines.append(f"   - Subsections: {len(section['subsections'])}")
        rendered.append("\n".join(lines))
    return "\n".join(rendered)


def format_emoji_dictionary(template: dict[str, Any]) -> str:
    emoji_dictionary = template.get("emoji_dictionary", {})
    if not isinstance(emoji_dictionary, dict) or not emoji_dictionary:
        return "No emoji dictionary found. Preserve emoji usage from the template if present."
    lines: list[str] = []
    for emoji, info in emoji_dictionary.items():
        if isinstance(info, dict):
            meaning = info.get("meaning", "unknown")
            usage = info.get("usage", "general")
        else:
            meaning = str(info)
            usage = "general"
        lines.append(f"- :{emoji}: = {meaning} ({usage})")
    return "\n".join(lines)


def generate_content_prompt(template: dict[str, Any], channel_ids: list[str], canvas_ids: list[str], lookback_days: int) -> str:
    lookback_ts = int((datetime.now() - timedelta(days=lookback_days)).timestamp())
    formatting = template.get("formatting_rules", {}) if isinstance(template.get("formatting_rules", {}), dict) else {}
    stakeholders = template.get("stakeholders", []) if isinstance(template.get("stakeholders", []), list) else []

    channel_block = format_id_block(
        "Slack channels",
        channel_ids,
        f"Read the last {lookback_days} days using `slack_read_channel` with `limit=100`, `response_format=concise`, and `oldest={lookback_ts}` if the tool supports those arguments.",
    )
    canvas_block = format_id_block("Slack canvases", canvas_ids, "Read current content using `slack_read_canvas`.")
    stakeholder_block = "\n".join(f"- {item}" for item in stakeholders) if stakeholders else "No stakeholder list found in the template. Use only stakeholders found in source material."

    return f"""You are generating a draft TPM status report from Slack source material.

This is a draft for human review. Do not post to Slack. Do not update any canvas. Do not send messages. Return the draft report text only. The wrapper script will write the local file.

Template name: `{template.get('template_name', 'unknown')}`
Source template canvas: `{template.get('source_canvas_id', 'unknown')}`
Template extracted date: `{template.get('extracted_date', 'unknown')}`

================================================================================
STEP 1: GATHER SOURCE MATERIAL
================================================================================

{channel_block}

{canvas_block}

Batch tool calls where it is reasonable, but do not skip sources.

================================================================================
STEP 2: EXTRACT ONLY SUPPORTED FACTS
================================================================================

From the source material, identify:

- Overall program or project health
- Completed work and material changes
- Upcoming milestones
- Active risks, blockers, and escalations
- Owners and next steps
- Ticket IDs, PR numbers, links, and dates
- Metrics, counts, and percentages
- Decisions needed from stakeholders

Rules for facts:

- Do not invent ticket IDs, dates, owners, links, metrics, status, or decisions.
- Do not convert vague chatter into a confident claim.
- If a required fact is missing, say it is not found in the source material.
- If source material conflicts, call out the conflict instead of resolving it silently.
- Red / Yellow / Green status must be supported by the source material.

================================================================================
STEP 3: APPLY TEMPLATE STRUCTURE
================================================================================

Title format:
`{template.get('title_format', '{{program_name}} - {{date}}, Status: :{{status_emoji}}: {{status_text}}')}`

Sections, in order:
{format_sections(template)}

Emoji dictionary:
{format_emoji_dictionary(template)}

Formatting rules:
- Date format: {formatting.get('date_format', 'Month Day, Year')}
- Work items: {formatting.get('work_items', 'Preserve ticket IDs, PR numbers, and links exactly as found')}
- Metrics: {formatting.get('metrics', 'Use only metrics found in the source material')}
- Tone: {formatting.get('tone', 'Professional, concise, factual')}

Stakeholder pattern:
{stakeholder_block}

================================================================================
STEP 4: RETURN THE DRAFT
================================================================================

Return only the finished draft report text. Do not wrap it in a code block.

The draft should:

- Match the template structure as closely as possible.
- Include all required sections.
- Omit optional sections only when there is no relevant source data.
- Preserve ticket IDs, links, dates, and metrics exactly as found.
- Make risks and decisions easy to see.
- Include a short `Needs Review` section only if facts are missing, conflicting, or require human confirmation.

Do not:

- Add sections that do not belong in the template unless they are needed for `Needs Review`.
- Change emoji meanings.
- Use vague phrases like "some progress" or "ongoing work" without specifics.
- Post, send, update, or write anything in Slack.

The TPM owns the final truth. Your job is to produce a useful draft, not a final source of record.
"""


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def run_claude(prompt: str, timeout: int) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        build_claude_command(prompt),
        stdin=subprocess.DEVNULL,
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
    )


def preview_text(text: str, max_lines: int = 25) -> str:
    lines = text.splitlines()
    preview = "\n".join(lines[:max_lines])
    if len(lines) > max_lines:
        preview += "\n..."
    return preview


def main() -> int:
    args = parse_args()
    try:
        validate_template_name(args.template_name)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    channel_ids = parse_id_list(args.channels)
    canvas_ids = parse_id_list(args.canvases)
    if not channel_ids and not canvas_ids:
        print("ERROR: specify at least one channel or canvas ID, or use 'none' only for one side", file=sys.stderr)
        return 2

    template_dir = Path(args.template_dir).expanduser().resolve()
    output_path = Path(args.output).expanduser().resolve() if args.output else (SCRIPT_DIR / f"{args.template_name}_draft.md").resolve()

    try:
        template = load_template(args.template_name, template_dir)
    except FileNotFoundError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        available = list_templates(template_dir)
        if available:
            print("Available templates:", file=sys.stderr)
            for template_name in available:
                print(f"  - {template_name}", file=sys.stderr)
        else:
            print("No templates found. Run canvas_template_extractor.py first.", file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"ERROR: could not load template: {exc}", file=sys.stderr)
        return 1

    lookback_days = args.lookback if args.lookback is not None else int(template.get("data_sources", {}).get("lookback_days", 7))
    if lookback_days <= 0:
        print("ERROR: --lookback must be a positive integer", file=sys.stderr)
        return 2

    prompt = generate_content_prompt(template, channel_ids, canvas_ids, lookback_days)

    if args.save_prompt:
        write_text(Path(args.save_prompt).expanduser(), prompt)
        print(f"Prompt saved to: {args.save_prompt}")
    if args.dry_run:
        print(prompt)
        return 0

    print(f"[{datetime.now().isoformat(timespec='seconds')}] Generating draft with template: {args.template_name}")
    print(f"Channels: {len(channel_ids)} | Canvases: {len(canvas_ids)} | Lookback: {lookback_days} days")
    print(f"Output: {output_path}")
    print("")

    try:
        result = run_claude(prompt, args.timeout)
    except subprocess.TimeoutExpired:
        print(f"ERROR: Generation timed out after {args.timeout} seconds", file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    if result.returncode != 0:
        print("ERROR: Generation failed", file=sys.stderr)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        if result.stdout:
            print(result.stdout, file=sys.stderr)
        return result.returncode

    draft = result.stdout.strip()
    if not draft:
        print("ERROR: Claude returned no draft text", file=sys.stderr)
        return 1

    write_text(output_path, draft.rstrip() + "\n")

    print("Draft generated successfully.")
    print(f"Location: {output_path}")
    print("")
    print("Preview:")
    print(preview_text(draft))
    print("")
    print("Next steps:")
    print(f"  1. Review: {output_path}")
    print("  2. Verify dates, owners, metrics, links, and Red / Yellow / Green status.")
    print("  3. Edit before posting. The draft is not the source of truth.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
