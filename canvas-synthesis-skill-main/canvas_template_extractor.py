#!/usr/bin/env python3
"""
Canvas Template Extractor
Analyzes a Slack canvas to extract its formatting structure and creates a reusable template
"""

import json
import os
import sys
import subprocess
from datetime import datetime

# Configuration
OUTPUT_DIR = ".canvas_templates"
CLAUDE_BIN = os.path.expanduser("~/.aisuite/bin/claude")

def extract_template_prompt(canvas_id: str, template_name: str) -> str:
    """Generate Claude prompt to analyze canvas and extract template"""

    output_path = os.path.join(os.getcwd(), OUTPUT_DIR, f"{template_name}.json")

    return f"""You are analyzing a Slack canvas to extract its formatting structure as a reusable template.

**Task:** Read canvas {canvas_id} and extract its formatting pattern.

**Step 1 - Read the canvas:**
Call slack_read_canvas for {canvas_id}

**Step 2 - Analyze the structure and extract:**

1. **Overall Format Pattern:**
   - Title format (e.g., "Program Name - Date, Status: :emoji:")
   - Section order and hierarchy
   - Use of emoji indicators and their meanings

2. **Section Templates:**
   For each major section, identify:
   - Section header format
   - Content structure (bullets, sub-bullets, numbered lists)
   - Emoji usage patterns
   - Link formats
   - Special formatting (bold, italics, code blocks)

3. **Emoji Dictionary:**
   Map emojis to their semantic meaning:
   - Status indicators (green-dot = on track, etc.)
   - Priority markers (circle-yellow-1 = watch, etc.)
   - State markers (blue_circle = completed, etc.)

4. **Content Patterns:**
   - How are dates formatted?
   - How are metrics presented?
   - How are work items referenced (ticket numbers, PR numbers, etc.)?
   - How are people/teams mentioned?
   - How are blockers/risks highlighted?

5. **Stakeholder Section:**
   - Format of @mentions
   - Ordering pattern

6. **Required vs Optional Sections:**
   - Which sections always appear?
   - Which are conditional?

**Step 3 - Output the template:**

Write a JSON file to {output_path} with this structure:

{{
  "template_name": "{template_name}",
  "source_canvas_id": "{canvas_id}",
  "extracted_date": "YYYY-MM-DD",
  "title_format": "{{program_name}} - {{{{date}}}}, Status: :{{{{status_emoji}}}}: {{{{status_text}}}}",
  "sections": [
    {{
      "name": "Highlights",
      "required": true,
      "format": "bullet_list",
      "style": "* {{{{content}}}}",
      "content_guidelines": "3-5 key accomplishments/milestones",
      "emoji_usage": "optional inline"
    }},
    {{
      "name": "Additional Detail",
      "required": true,
      "subsections": [
        {{
          "name": "Progress Updates",
          "format": "nested_bullets",
          "example": "* Item: status\\n    * :emoji: Detail"
        }}
      ]
    }},
    {{
      "name": "Follow-up Actions",
      "required": true,
      "format": "text_or_list",
      "default_empty": "None"
    }},
    {{
      "name": "Reference Docs",
      "required": false,
      "format": "link_list"
    }},
    {{
      "name": "Stakeholders",
      "required": true,
      "format": "mentions",
      "example": "@Name1 @Name2 @Name3"
    }}
  ],
  "emoji_dictionary": {{
    "green-dot": {{"meaning": "On Track", "usage": "status_indicator"}},
    "yellow-dot": {{"meaning": "At Risk", "usage": "status_indicator"}},
    "red-dot": {{"meaning": "Blocked", "usage": "status_indicator"}},
    "blue_circle": {{"meaning": "Completed", "usage": "sub_status"}},
    "circle-yellow-1": {{"meaning": "Watch", "usage": "issue_priority"}},
    "red_circle": {{"meaning": "Blocked", "usage": "sub_status"}},
    "yellow": {{"meaning": "Paused/In Progress", "usage": "sub_status"}}
  }},
  "formatting_rules": {{
    "date_format": "Month Day, Year",
    "work_items": "Ticket format (e.g., PROJ-123, #456)",
    "metrics": "Include percentages, counts, specifics",
    "tone": "Professional, concise, factual"
  }},
  "data_sources": {{
    "primary_channel": "Channel ID from which to pull updates",
    "secondary_canvas": "Canvas ID with aggregated intelligence",
    "lookback_days": 7
  }},
  "stakeholders": [
    "List of @mentions extracted from the source canvas"
  ]
}}

**Rules:**
- Extract the ACTUAL format from the canvas, don't invent
- Preserve emoji names exactly as they appear
- Note any patterns in how content is organized
- Identify what makes this format distinctive
- Be specific about structure but generic about content

**Output:**
Write the JSON template to {output_path}
Report success/failure
"""

def main():
    if len(sys.argv) < 3:
        print("Usage: ./canvas_template_extractor.py <canvas_id> <template_name>")
        print("")
        print("Example:")
        print("  ./canvas_template_extractor.py F0ABC123456 my_status_format")
        print("")
        print("This will analyze the canvas and create a reusable template at:")
        print(f"  {OUTPUT_DIR}/<template_name>.json")
        sys.exit(1)

    canvas_id = sys.argv[1]
    template_name = sys.argv[2]

    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print(f"[{datetime.now()}] Extracting template from canvas {canvas_id}...")
    print(f"Template name: {template_name}")
    print("")

    prompt = extract_template_prompt(canvas_id, template_name)

    # Write prompt to temp file
    prompt_file = f"/tmp/canvas_template_extract_{template_name}.txt"
    with open(prompt_file, 'w') as f:
        f.write(prompt)

    # Run Claude
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
            timeout=180
        )

        print(result.stdout)

        if result.returncode != 0:
            print(f"ERROR: Template extraction failed")
            print(f"STDERR: {result.stderr}")
            sys.exit(1)

    except subprocess.TimeoutExpired:
        print("ERROR: Template extraction timed out")
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)

    # Check if template was created
    template_path = f"{OUTPUT_DIR}/{template_name}.json"
    if os.path.exists(template_path):
        print("")
        print(f"✅ Template extracted successfully!")
        print(f"Location: {template_path}")
        print("")
        print("To use this template:")
        print(f"  ./canvas_generator_from_template.py {template_name} <channel_ids> <canvas_ids>")
    else:
        print("")
        print(f"⚠️  Template file not found at {template_path}")
        print("Check Claude output above for errors")
        sys.exit(1)

if __name__ == "__main__":
    main()
