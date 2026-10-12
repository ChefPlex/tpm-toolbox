# Slack Canvas Status Synthesis

Two scripts that turn Slack into a draft status report.

The first script reads an existing status canvas - one that already works, that people actually read - and extracts its structure into a reusable JSON template. The second script uses that template to read your Slack channels and canvases, then returns a draft report matching the format your stakeholders already expect.

Claude does the reading and drafting. The Python wrappers handle local files. The TPM reviews before anything goes anywhere.

---

## Why This Exists

The hard part of status reporting is not the writing. It's pulling a useful signal from a week of Slack noise, tracking down the current state of five concurrent workstreams, and then organizing it into a format that the right people will actually read.

This tool does the first-pass assembly. It reads your sources, applies your template, and produces a draft that's correct enough to edit rather than blank enough to dread. The draft is not the source of truth. Your review is.

---

## Prerequisites

- Python 3.9 or later
- [Claude Code CLI](https://code.claude.com/docs/en/cli-reference) installed and on your PATH (or set `CLAUDE_BIN`)
- Slack MCP connected to your Claude environment
- Read access to the channels and canvases you want to use

No third-party Python packages required. Everything is stdlib.

---

## Setup

```bash
cd slack-canvas-status-synthesis
chmod +x canvas_template_extractor.py canvas_generator_from_template.py
```

Templates are stored in `.canvas_templates/` inside the tool directory. That folder is git-ignored by default - generated templates can contain internal structure worth reviewing before committing.

---

## Two-Step Workflow

### Step 1: Extract a template from an existing status canvas

Find a status canvas that already works. Extract its structure once.

```bash
./canvas_template_extractor.py F0YOURCANVASID your_template_name
```

This reads the canvas, asks Claude to replace names, ticket IDs, links, dates, and metrics with placeholders, and writes a JSON template to `.canvas_templates/your_template_name.json`. The placeholders come from the prompt, not from code, and the JSON keeps the source canvas ID. Review the JSON before committing it.

Run this once per template. Re-run if the status format changes significantly.

**Options:**

| Flag | What It Does |
|------|-------------|
| `--template-dir PATH` | Use a different directory for templates |
| `--timeout N` | Claude timeout in seconds (default: 180) |
| `--save-prompt PATH` | Write the prompt to a file before running |
| `--dry-run` | Print the prompt and exit without calling Claude |
| `--allow-sensitive-examples` | Allow representative source examples in the template (off by default) |

---

### Step 2: Generate a draft from current Slack sources

```bash
./canvas_generator_from_template.py your_template_name \
  C0CHANNEL1,C0CHANNEL2 F0CANVAS1,F0CANVAS2
```

Reads the channels and canvases you specify, applies the extracted template, and writes a draft markdown file. Default output name is `your_template_name_draft.md` in the tool directory.

Use `none` on either position if you only have channels or only have canvases:

```bash
# Channels only
./canvas_generator_from_template.py your_template_name C0CHAN1,C0CHAN2 none

# Canvases only
./canvas_generator_from_template.py your_template_name none F0CANVAS1
```

**Options:**

| Flag | What It Does |
|------|-------------|
| `--output PATH` | Custom output path for the draft |
| `--lookback N` | Days to look back in channels (default: from template, then 7) |
| `--template-dir PATH` | Use a different directory for templates |
| `--timeout N` | Claude timeout in seconds (default: 300) |
| `--save-prompt PATH` | Write the prompt to a file before running |
| `--dry-run` | Print the prompt and exit without calling Claude |

---

## Environment Variables

| Variable | What It Does |
|----------|-------------|
| `CLAUDE_BIN` | Path to Claude CLI if not on PATH |
| `SLACK_MCP_SERVER` | The name `claude mcp list` shows for your Slack connection (default: `claude_ai_Slack`, the claude.ai Slack connector) |
| `CLAUDE_ALLOWED_TOOLS` | Override the default read-tool allowlist (full `mcp__<server>__<tool>` names). `none` sends no allowlist at all: the deny list still applies, and the reads then depend on your own Claude Code settings |
| `NO_CAFFEINATE` | Set to `1` to skip caffeinate on macOS |

Claude Code names MCP tools `mcp__<server>__<tool>`, and a permission rule written with a bare tool name matches nothing. So the scripts build full names from `SLACK_MCP_SERVER`. By default, the extractor allows only `mcp__<server>__slack_read_canvas` and the generator allows only the channel and canvas read tools. If the server name is wrong, the reads are simply not approved and the draft comes back with nothing read: it fails closed.

Read-only is enforced two ways, using the Claude Code [`--allowedTools` and `--disallowedTools`](https://code.claude.com/docs/en/cli-reference) flags. The allowlist pre-approves the read tools, and `--disallowedTools` denies five Slack write tools by name (`slack_send_message`, `slack_send_message_draft`, `slack_schedule_message`, `slack_create_canvas`, `slack_update_canvas`), even if your own Claude Code settings would allow them. Those five are the write tools the claude.ai Slack connector offered as of October 2026. A write tool with any other name is not on the deny list, so check what your Slack server offers. Both depend on `SLACK_MCP_SERVER` naming your real Slack server: check it against `claude mcp list` before the first run, because a wrong name makes the deny list match nothing too. There is no switch to bypass Claude's permission checks, on purpose: a bypass flag would remove both for every tool. The scripts read sources and return content to stdout. They do not post, send, update, or write anything in Slack.

---

## Weekly Wrapper Pattern

For repeat use, wrap the command so the inputs aren't retyped every week. The draft goes to `drafts/`, which is git-ignored, so internal status does not end up in a commit:

```bash
#!/usr/bin/env bash
set -euo pipefail

TEMPLATE="weekly_program_status"
CHANNELS="C0PROGRAMCHANNEL,C0SECURITYCHANNEL"
CANVASES="F0PLANNINGCANVAS,F0RISKCANVAS"
OUTPUT="drafts/weekly_status_$(date +%Y_%m_%d).md"

cd "$(dirname "$0")"

./canvas_generator_from_template.py "$TEMPLATE" \
  "$CHANNELS" "$CANVASES" \
  --output "$OUTPUT" \
  --lookback 7

echo "Draft ready: $OUTPUT"
echo "Review before posting. The tool writes drafts, not truth."
```

---

## What Comes Out

A markdown draft matching the structure of your source template. The prompt asks for every required section, and for optional sections only when there's source material to support them. If a required fact is missing or conflicting, the prompt asks for a `Needs Review` section naming the gap rather than filling it with something plausible.

The prompt asks for two things in every draft:

- **A suggested status, marked "TPM decides".** The tool cannot decide Red / Yellow / Green. It proposes a color with a one-line rationale from the sources, and the TPM sets the real one. The [status report generator](https://github.com/ChefPlex/ai-automations/tree/main/status-report-generator) in `ai-automations` takes the stricter line: it lays out the evidence for each color and suggests none.
- **A `Source Coverage` table**, one row per channel and canvas: whether it was read, how many messages, what span they cover, and whether the read was truncated. Channel reads stop at 100 messages, so a busy channel can be only partly covered, and the table is how you find out.

These are instructions to Claude, not checks in code. The generator writes whatever Claude returns. It prints a warning if the draft has no `Source Coverage` table, and it does not check the suggested status at all. Thread replies are not read either: the generator allows only the channel and canvas read tools, so a decision made inside a thread can be missing from the draft.

Before you send it, check:

- Does the coverage table show every source you meant to include, with nothing truncated that matters?
- Is the Green / Yellow / Red status defensible?
- Are the dates and owners current?
- Are blockers written as decision points, not vague concerns?
- Did the draft miss anything that happened outside Slack?

The output should save time. It does not get a free pass.

---

## See Also

- [EXAMPLES.md](EXAMPLES.md) - Five worked examples: weekly status, security remediation rollup, executive brief, incident follow-up, daily pulse
- [tpm-templates](https://github.com/ChefPlex/tpm-templates) - The Communications Plan template defines the cadence this tool supports
- [program-reporting-frameworks](https://github.com/ChefPlex/program-reporting-frameworks) - The Status Reporting Framework explains what goes in each section and why

---

*Part of the [tpm-toolbox](https://github.com/ChefPlex/tpm-toolbox). Maintained by [Eric White](https://www.linkedin.com/in/edwhite) | [ChefPlex](https://github.com/ChefPlex)*
