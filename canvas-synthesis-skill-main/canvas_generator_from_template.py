#!/usr/bin/env python3
"""
Canvas Generator from Template
Uses an extracted template to generate formatted content from Slack channels/canvases
"""

import json
import os
import sys
import subprocess
from datetime import datetime, timedelta

# Configuration
TEMPLATE_DIR = ".canvas_templates"
CLAUDE_BIN = os.path.expanduser("~/.aisuite/bin/claude")

def load_template(template_name: str) -> dict:
    """Load a template JSON file"""
    template_path = os.path.join(TEMPLATE_DIR, f"{template_name}.json")

    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Template not found: {template_path}")

    with open(template_path, 'r') as f:
        return json.load(f)

def generate_content_prompt(template: dict, channel_ids: list, canvas_ids: list,
                           output_file: str, lookback_days: int = None) -> str:
    """Generate Claude prompt to create content using the template"""

    # Use template's default lookback if not specified
    if lookback_days is None:
        lookback_days = template.get('data_sources', {}).get('lookback_days', 7)

    lookback_ts = int((datetime.now() - timedelta(days=lookback_days)).timestamp())

    # Build data source instructions
    data_sources = []

    if channel_ids:
        data_sources.append(f"""**Slack Channels ({len(channel_ids)}):**
Fetch last {lookback_days} days of messages using slack_read_channel:
{chr(10).join(f'  - {cid}' for cid in channel_ids)}
Call with: limit=100, response_format=concise, oldest={lookback_ts}""")

    if canvas_ids:
        data_sources.append(f"""**Slack Canvases ({len(canvas_ids)}):**
Read current content using slack_read_canvas:
{chr(10).join(f'  - {cid}' for cid in canvas_ids)}""")

    # Build section instructions from template
    section_instructions = []
    for idx, section in enumerate(template.get('sections', []), 1):
        required = "REQUIRED" if section.get('required', False) else "OPTIONAL"
        section_instructions.append(f"""{idx}. **{section['name']}** ({required})
   Format: {section.get('format', 'text')}
   {f"Style: {section['style']}" if 'style' in section else ""}
   {f"Guidelines: {section.get('content_guidelines', 'See template')}" if 'content_guidelines' in section else ""}
   {f"Default if empty: {section.get('default_empty', 'Omit section')}" if 'default_empty' in section else ""}
   {f"Subsections: {len(section.get('subsections', []))}" if 'subsections' in section else ""}""")

    # Build emoji reference
    emoji_ref = []
    for emoji, info in template.get('emoji_dictionary', {}).items():
        emoji_ref.append(f"  :{emoji}: → {info.get('meaning', 'Unknown')} ({info.get('usage', 'general')})")

    # Build formatting rules
    formatting = template.get('formatting_rules', {})

    prompt = f"""You are generating formatted content using a pre-defined template.

**Template:** {template['template_name']}
**Source Template Canvas:** {template.get('source_canvas_id', 'N/A')}

================================================================================
STEP 1: GATHER DATA
================================================================================

{chr(10).join(data_sources)}

Batch your API calls efficiently to avoid rate limits.

================================================================================
STEP 2: ANALYZE AND EXTRACT
================================================================================

From the gathered data, identify and extract:

- Overall program/project health (Green/Yellow/Red)
- Key accomplishments and milestones
- Progress metrics (percentages, counts, completion status)
- Technical activities (PRs, deployments, bug fixes)
- Issues and trends (blockers, escalations, common problems)
- Communications milestones (announcements, updates, upcoming items)
- Active blockers or risks (with owners and resolution targets)
- Notable escalations or issues (with ticket numbers if available)
- Any cross-cutting themes or patterns

**Critical:** Do NOT hallucinate ticket numbers, dates, or metrics.
If information is missing, say so explicitly rather than inventing data.

================================================================================
STEP 3: COMPOSE CONTENT USING TEMPLATE STRUCTURE
================================================================================

**Title Format:**
{template.get('title_format', '{{program_name}} - {{date}}, Status: :{{status_emoji}}: {{status_text}}')}

**Sections (in order):**
{chr(10).join(section_instructions)}

**Emoji Usage:**
{chr(10).join(emoji_ref) if emoji_ref else '  See template for emoji meanings'}

**Formatting Rules:**
  - Date format: {formatting.get('date_format', 'Month Day, Year')}
  - Work items: {formatting.get('work_items', 'Include IDs in appropriate format')}
  - Metrics: {formatting.get('metrics', 'Include specific numbers, percentages, counts')}
  - Tone: {formatting.get('tone', 'Professional, concise, factual')}

**Stakeholders:**
{chr(10).join(f'  @{s}' for s in template.get('stakeholders', [])) if template.get('stakeholders') else '  See template'}

================================================================================
STEP 4: OUTPUT
================================================================================

Write the formatted content to: {output_file}

The output should:
✓ Match the template structure exactly
✓ Use proper emoji indicators from the dictionary
✓ Include specific data (dates, metrics, work items) where available
✓ Maintain the professional tone specified
✓ Include all required sections
✓ Omit optional sections if no relevant data
✓ Use the stakeholder list from the template

DO NOT:
✗ Hallucinate ticket IDs, dates, or metrics
✗ Add sections not in the template
✗ Change the emoji meanings
✗ Use vague language like "some progress" or "ongoing work"
✗ Send any Slack messages or update any canvases

DO:
✓ Be specific with numbers and dates
✓ Include all relevant work item numbers found in source data
✓ Highlight risks and blockers prominently
✓ Use consistent formatting per the template
✓ Write clear, scannable content
✓ Note gaps explicitly if data is missing

================================================================================
TEMPLATE CONTEXT
================================================================================

**Template extracted from:** {template.get('source_canvas_id', 'Unknown')}
**Extraction date:** {template.get('extracted_date', 'Unknown')}

This template was learned from an existing canvas. Your job is to apply the
same formatting structure and style to new data sources.

If the source data doesn't fit the template well, adapt as needed but preserve
the overall structure and tone.
"""

    return prompt

def main():
    if len(sys.argv) < 4:
        print("Usage: ./canvas_generator_from_template.py <template_name> <channels> <canvases> [options]")
        print("")
        print("Arguments:")
        print("  template_name  Name of template (without .json)")
        print("  channels       Comma-separated channel IDs (or 'none')")
        print("  canvases       Comma-separated canvas IDs (or 'none')")
        print("")
        print("Options:")
        print("  --output FILE       Output file (default: <template>_draft.txt)")
        print("  --lookback DAYS     Days to look back (default: from template)")
        print("")
        print("Examples:")
        print("  # Generate from channel + canvas")
        print("  ./canvas_generator_from_template.py my_template \\")
        print("    C0ABC123 F0XYZ789")
        print("")
        print("  # Generate from multiple channels only")
        print("  ./canvas_generator_from_template.py weekly_status \\")
        print("    C0AAA,C0BBB,C0CCC none")
        print("")
        print("  # Custom output and lookback")
        print("  ./canvas_generator_from_template.py my_template \\")
        print("    C123 F456 --output custom.txt --lookback 14")
        sys.exit(1)

    template_name = sys.argv[1]
    channels_arg = sys.argv[2]
    canvases_arg = sys.argv[3]

    # Parse channel and canvas IDs
    channel_ids = [] if channels_arg.lower() == 'none' else channels_arg.split(',')
    canvas_ids = [] if canvases_arg.lower() == 'none' else canvases_arg.split(',')

    # Parse options
    output_file = f"{template_name}_draft.txt"
    lookback_days = None

    i = 4
    while i < len(sys.argv):
        if sys.argv[i] == '--output' and i + 1 < len(sys.argv):
            output_file = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == '--lookback' and i + 1 < len(sys.argv):
            lookback_days = int(sys.argv[i + 1])
            i += 2
        else:
            print(f"Unknown option: {sys.argv[i]}")
            sys.exit(1)

    # Validate inputs
    if not channel_ids and not canvas_ids:
        print("ERROR: Must specify at least one channel or canvas ID")
        sys.exit(1)

    print(f"[{datetime.now()}] Generating content using template: {template_name}")
    print(f"Channels: {len(channel_ids)} | Canvases: {len(canvas_ids)}")
    print(f"Output: {output_file}")
    print("")

    # Load template
    try:
        template = load_template(template_name)
        print(f"✅ Template loaded: {template['template_name']}")
        print(f"   Source: {template.get('source_canvas_id', 'Unknown')}")
        print(f"   Sections: {len(template.get('sections', []))}")
        print("")
    except FileNotFoundError as e:
        print(f"❌ {e}")
        print(f"Available templates:")
        if os.path.exists(TEMPLATE_DIR):
            templates = [f[:-5] for f in os.listdir(TEMPLATE_DIR) if f.endswith('.json')]
            if templates:
                for t in templates:
                    print(f"  - {t}")
            else:
                print("  (none - run canvas_template_extractor.py first)")
        else:
            print("  (none - run canvas_template_extractor.py first)")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error loading template: {e}")
        sys.exit(1)

    # Generate prompt
    prompt = generate_content_prompt(template, channel_ids, canvas_ids,
                                    output_file, lookback_days)

    # Write prompt to temp file
    prompt_file = f"/tmp/canvas_gen_{template_name}.txt"
    with open(prompt_file, 'w') as f:
        f.write(prompt)

    # Run Claude
    print(f"[{datetime.now()}] Running Claude to generate content...")
    try:
        result = subprocess.run(
            [
                "caffeinate", "-s",
                CLAUDE_BIN,
                "--allowedTools", "*",
                "--permission-mode", "bypassPermissions",
                "-p", prompt
            ],
            stdin=subprocess.DEVNULL,
            capture_output=True,
            text=True,
            timeout=300
        )

        print(result.stdout)

        if result.returncode != 0:
            print(f"❌ Generation failed")
            print(f"STDERR: {result.stderr}")
            sys.exit(1)

    except subprocess.TimeoutExpired:
        print("❌ Generation timed out after 5 minutes")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

    # Check output
    if os.path.exists(output_file):
        print("")
        print(f"✅ Content generated successfully!")
        print(f"Location: {output_file}")
        print("")
        print("Preview:")
        with open(output_file, 'r') as f:
            lines = f.readlines()
            for line in lines[:25]:
                print(line, end='')
            if len(lines) > 25:
                print("...")
        print("")
        print("Next steps:")
        print(f"  1. Review: cat {output_file}")
        print(f"  2. Edit if needed: vim {output_file}")
        print(f"  3. Post to Slack or use as needed")
    else:
        print("")
        print(f"⚠️  Output file not created at {output_file}")
        print("Check Claude output above for errors")
        sys.exit(1)

if __name__ == "__main__":
    main()
