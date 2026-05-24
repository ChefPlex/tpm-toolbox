# Canvas Synthesis Skill

A generic, reusable tool for generating formatted content from Slack channels and canvases using learned templates.

## Overview

Instead of hardcoding formatting rules, this skill **learns** them from example canvases and **applies** them to new data sources.

**Two-step process:**

1. **Extract template** - Analyze a canvas to learn its format
2. **Generate content** - Apply that template to new Slack data

## Quick Start

### Prerequisites

- Claude Code CLI installed
- Slack access to channels/canvases you want to use
- Python 3.6+

### Installation

```bash
git clone https://github.com/yourusername/canvas-synthesis-skill.git
cd canvas-synthesis-skill
chmod +x *.py
```

### Usage

#### Step 1: Extract a Template (one-time)

```bash
./canvas_template_extractor.py <canvas_id> <template_name>
```

**Example:**
```bash
# Extract format from a weekly status canvas
./canvas_template_extractor.py F0ABC123456 weekly_status
```

This creates `.canvas_templates/weekly_status.json`

**💡 Best Practice:** For best results, extract templates from **summarization canvases** that aggregate multiple Slack channels. These canvases already have rich structure, consistent formatting, and comprehensive coverage - making them ideal template sources. Examples:
- Automated intel canvases that synthesize 5-10 channels
- Weekly rollup canvases maintained by your team
- Executive briefing canvases with cross-program data

Single-purpose canvases or one-off documents work too, but multi-channel aggregation canvases provide the richest templates.

#### Step 2: Generate Content (weekly or as-needed)

```bash
./canvas_generator_from_template.py <template> <channels> <canvases>
```

**Examples:**
```bash
# Generate from one channel + one canvas
./canvas_generator_from_template.py weekly_status C0ABC123 F0XYZ789

# Generate from multiple channels only
./canvas_generator_from_template.py team_sync C0A,C0B,C0C none

# Custom output and 14-day lookback
./canvas_generator_from_template.py sprint_summary \
  C123 F456 --output sprint_42.txt --lookback 14
```

## How It Works

### Template Extraction

The extractor analyzes a canvas and captures:

- **Section structure** - Order and hierarchy
- **Emoji meanings** - What each emoji signifies
- **Formatting patterns** - Bullets, numbering, links
- **Content guidelines** - What goes in each section
- **Stakeholder lists** - @mentions
- **Data sources** - Default channels/canvases to read

Templates are stored as human-editable JSON in `.canvas_templates/`

**💡 Tip:** The best source canvases for extraction are **multi-channel aggregation canvases** - automated summaries that already synthesize data from multiple Slack channels. These provide the richest structure and most comprehensive formatting patterns. Think of canvases like:
- Automated intel briefs that combine 5-10 channels
- Weekly program summaries with cross-team data
- Executive dashboards with org-wide metrics

These canvases have already solved the "how to organize disparate information" problem, making them perfect templates to learn from.

### Content Generation

The generator:

1. Reads Slack channels (last N days) and/or canvases
2. Extracts relevant information (dates, metrics, issues, progress)
3. Formats it according to the template structure
4. Outputs a draft file for review

**Key feature:** Instructs Claude NOT to hallucinate - if data is missing, it says so explicitly.

## Use Cases

- **Weekly status updates** - Any program or project
- **Sprint summaries** - Team velocity, completed items
- **Executive briefings** - High-level program health
- **Incident reports** - Post-mortem structure
- **Intelligence briefs** - Multi-channel aggregation
- **Team sync notes** - Standup summaries
- **Release notes** - Deployment summaries

Anything with a consistent format!

## Command Reference

### Extract Template

```bash
./canvas_template_extractor.py <canvas_id> <template_name>
```

**Arguments:**
- `canvas_id` - Slack canvas ID (e.g., F0ABC123456)
- `template_name` - Name for this template (e.g., weekly_status)

**Output:** `.canvas_templates/<template_name>.json`

### Generate Content

```bash
./canvas_generator_from_template.py <template> <channels> <canvases> [options]
```

**Arguments:**
- `template` - Template name (without .json)
- `channels` - Comma-separated channel IDs or 'none'
- `canvases` - Comma-separated canvas IDs or 'none'

**Options:**
- `--output FILE` - Custom output filename
- `--lookback DAYS` - Days to look back in channels

**Output:** `<template>_draft.txt` (or custom filename)

## Template Structure

Templates are JSON files with this structure:

```json
{
  "template_name": "weekly_status",
  "source_canvas_id": "F0ABC123456",
  "extracted_date": "2024-05-23",
  "title_format": "{{program}} - {{date}}, Status: :{{emoji}}:",
  "sections": [
    {
      "name": "Highlights",
      "required": true,
      "format": "bullet_list",
      "content_guidelines": "3-5 key accomplishments"
    },
    {
      "name": "Progress",
      "required": true,
      "subsections": [...]
    }
  ],
  "emoji_dictionary": {
    "green-dot": {"meaning": "On Track", "usage": "status"},
    "yellow-dot": {"meaning": "At Risk", "usage": "status"}
  },
  "formatting_rules": {
    "date_format": "Month Day, Year",
    "work_items": "PROJ-123 format",
    "tone": "Professional, concise"
  },
  "data_sources": {
    "primary_channel": "C0ABC123",
    "lookback_days": 7
  },
  "stakeholders": ["@Name1", "@Name2"]
}
```

Templates are **human-editable** - refine them as needed!

## Examples

### Example 1: Weekly Status Update

```bash
# One-time: Extract format
./canvas_template_extractor.py F0ABC123456 weekly_status

# Weekly: Generate update
./canvas_generator_from_template.py weekly_status \
  C09RJKBCT0A F0B1SV1EV0A
```

### Example 2: Sprint Summary

```bash
# Extract sprint format
./canvas_template_extractor.py F0SPRINT123 sprint_summary

# Generate sprint 42 summary
./canvas_generator_from_template.py sprint_summary \
  C0TEAM,C0PLANNING none --output sprint_42.txt --lookback 14
```

### Example 3: Daily Team Sync

```bash
# Extract standup format
./canvas_template_extractor.py F0STANDUP team_sync

# Generate today's sync
./canvas_generator_from_template.py team_sync \
  C0TEAM none --lookback 1
```

## Workflow

```
┌──────────────────────────────┐
│ Find canvas with good format │
└──────────────────────────────┘
              ↓
┌──────────────────────────────┐
│ Extract template (one time)  │
│ ./canvas_template_extractor  │
└──────────────────────────────┘
              ↓
┌──────────────────────────────┐
│ Generate content (recurring) │
│ ./canvas_generator_from...   │
└──────────────────────────────┘
              ↓
┌──────────────────────────────┐
│ Review & post                │
└──────────────────────────────┘
```

## Advantages

### ✅ Reusable
- Extract once, use anywhere
- Build a template library
- Share templates across teams

### ✅ Consistent
- Always matches learned format
- Preserves emoji meanings
- Maintains professional tone

### ✅ Flexible
- Works with any channel/canvas combo
- Configurable lookback periods
- Custom output locations

### ✅ No Hallucinations
- Explicitly instructs Claude not to invent data
- Missing information is noted, not fabricated
- Safe for production use

### ✅ Version Controllable
- Templates are JSON files
- Track changes over time
- Collaborate via Git

## Best Practices

### Template Extraction

1. ✅ Use well-formatted, recent example canvases
2. ✅ Choose canvases with consistent structure
3. ✅ Review and refine the extracted JSON
4. ✅ Document what each template is for

### Content Generation

1. ✅ Always review generated content before posting
2. ✅ Verify ticket IDs, dates, and metrics are real
3. ✅ Use appropriate lookback periods (7-14 days typical)
4. ✅ Combine multiple data sources for best results

### Template Management

1. ✅ Version control your `.canvas_templates/` directory
2. ✅ Share templates across your team
3. ✅ Update templates as formats evolve
4. ✅ Create wrapper scripts for common use cases

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Template not found | Run `canvas_template_extractor.py` first |
| Can't read canvas | Check Slack permissions and authentication |
| Generated content is sparse | Increase `--lookback` or add more sources |
| Format doesn't match | Manually edit `.canvas_templates/<name>.json` |
| Scripts won't run | `chmod +x *.py` |
| Hallucinated data | Verify all facts before posting |

## Advanced Usage

### Creating Wrapper Scripts

For frequently-used templates, create wrapper scripts:

```bash
#!/bin/bash
# weekly_status.sh - Generate weekly status update

./canvas_generator_from_template.py weekly_status \
  C0STATUS,C0TEAM F0INTEL \
  --output status_$(date +%Y%m%d).txt
```

### Scheduled Generation

Use cron for automatic generation:

```bash
# Generate weekly status every Friday at 4 PM
0 16 * * 5 cd /path/to/canvas-synthesis-skill && ./weekly_status.sh
```

### Template Versioning

Track template changes:

```bash
cd .canvas_templates
git add weekly_status.json
git commit -m "Update weekly status format with new metrics section"
```

## Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

- Issues: [GitHub Issues](https://github.com/yourusername/canvas-synthesis-skill/issues)
- Discussions: [GitHub Discussions](https://github.com/yourusername/canvas-synthesis-skill/discussions)

## Acknowledgments

Created to solve the problem of maintaining consistent formatting across multiple status updates, reports, and summaries without hardcoding format rules.
