# Slack Canvas Status Synthesis

AI-assisted status reporting for TPMs who need to turn Slack noise into a usable weekly update.

This workflow learns the structure of a good Slack canvas, then uses that structure to generate a draft status report from current Slack channels and canvases. It is meant to remove the copy/paste tax from status reporting, not replace the TPM's judgment.

The workflow is simple:

1. Start with a status canvas that already works.
2. Extract the structure into a reusable JSON template.
3. Generate a draft from current Slack channels and canvases.
4. Review the draft, verify the facts, and post only after a human pass.

Status reports are supposed to make risk visible. Too often they become a formatting chore. This keeps the useful part and automates the tedious part.

---

## What Is Here

| File | Purpose |
|------|---------|
| `canvas_template_extractor.py` | Reads an existing Slack canvas and asks Claude to extract the structure into a local JSON template. |
| `canvas_generator_from_template.py` | Uses a saved template plus Slack channels and canvases to generate a draft report. |
| `EXAMPLES.md` | Practical examples, wrapper script patterns, review checklist, and measurement ideas. |
| `.canvas_templates/` | Local storage for extracted templates. Template JSON files are ignored by default so internal program details do not get published by accident. |

---

## Requirements

This assumes you already have:

- Python 3.9 or later
- Claude Code CLI installed and authenticated
- Slack tools configured for Claude, including access to the channels and canvases you pass in
- Permission to read the source material you are summarizing

The scripts do not post to Slack, update canvases, or send messages. They generate local draft files only.

---

## Setup

From the repo root:

```bash
cd tpm-toolbox/slack-canvas-status-synthesis
chmod +x canvas_template_extractor.py canvas_generator_from_template.py
```

Claude CLI discovery order:

1. `CLAUDE_BIN` environment variable, if set
2. `claude` on your `PATH`
3. `~/.aisuite/bin/claude`

Optional environment variables:

| Variable | Purpose |
|----------|---------|
| `CLAUDE_BIN` | Path to Claude CLI if it is not on your `PATH`. |
| `CLAUDE_ALLOWED_TOOLS` | Comma-separated list of tools to allow for the run. Defaults to read-only Slack tools: `slack_read_channel,slack_read_canvas` for generation and `slack_read_canvas` for extraction. Override this if your local MCP tool names differ. |
| `CLAUDE_BYPASS_PERMISSIONS=1` | Optional local override for Claude permission prompts. Not recommended for shared or sensitive environments. |
| `NO_CAFFEINATE=1` | On macOS, disables `caffeinate` wrapping. |

The scripts no longer grant every tool or bypass permissions by default. They also ask Claude to return content to stdout, then the Python wrapper writes the local file. That keeps filesystem permissions out of the Claude call and makes the data boundary cleaner.

---

## Usage

### 1. Extract a template

Use a Slack canvas that already has the structure you want to reuse.

```bash
./canvas_template_extractor.py F0ABC123456 weekly_program_status
```

This writes:

```text
.canvas_templates/weekly_program_status.json
```

### 2. Generate a draft report

Use the saved template with one or more Slack channels and canvases.

```bash
./canvas_generator_from_template.py weekly_program_status \
  C0TEAMCHANNEL F0PLANNINGCANVAS
```

Use comma-separated values for multiple channels or canvases:

```bash
./canvas_generator_from_template.py weekly_program_status \
  C0TEAMCHANNEL,C0SECURITYCHANNEL \
  F0PLANNINGCANVAS,F0RISKCANVAS \
  --output weekly_status_2026_05_24.md \
  --lookback 7
```

Use `none` when one side is not needed:

```bash
./canvas_generator_from_template.py weekly_program_status \
  C0TEAMCHANNEL none
```

---

## Hallucination Controls

The prompt tells Claude not to invent ticket IDs, dates, owners, metrics, links, or status claims. That lowers the risk. It does not eliminate it.

Treat every generated report as a draft. Before posting, verify:

- Ticket IDs and links
- Dates and milestones
- Metric values
- Owner names
- Red / Yellow / Green status
- Risks, blockers, and decision requests
- Any executive-facing statement that could trigger work or escalation

The tool can draft the report. The TPM still owns the truth.

---

## Where This Breaks

This works best when the source channels already contain useful signal: decisions, blockers, dates, owners, ticket IDs, and clear program updates.

It works poorly when the source material is mostly chatter, when teams use inconsistent naming, or when important work happens outside Slack. In those cases, the generated draft may look polished while still missing the actual risk.

That is the failure mode to watch for: a clean report that is wrong because the source material was incomplete.

---

## Review Bar

Before you send a generated update, ask three questions:

1. Is the status true?
2. Are the risks and asks clear enough for someone to act on them?
3. Did the tool preserve useful signal, or just make the noise look organized?

A pretty report that avoids the hard question is still a bad report.

---

## Dry Run and Prompt Review

Both scripts support `--dry-run` and `--save-prompt`.

```bash
./canvas_generator_from_template.py weekly_program_status \
  C0TEAMCHANNEL F0PLANNINGCANVAS \
  --dry-run \
  --save-prompt prompt_review.md
```

Use this when changing the prompt, onboarding someone else, or checking what the tool is about to ask Claude to do.

---

## Notes on Sensitive Data

Slack channels and canvases often contain internal program details, names, links, and security context. Do not commit generated drafts or extracted templates unless you have scrubbed them first.

The default `.gitignore` keeps local template JSON files and generated drafts out of the repo. That is intentional.
