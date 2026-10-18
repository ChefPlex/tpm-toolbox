# Slack Canvas Status Synthesis

Two scripts that turn Slack into a draft status report.

The first script reads an existing status canvas - one that already works, that people actually read - and extracts its structure into a reusable JSON template. The second script uses that template to read your Slack channels and canvases, then returns a draft report matching the format your stakeholders already expect.

Claude does the reading and drafting. The Python wrappers handle local files and check, in code, what the model cannot be trusted to check about itself: the template's shape, the tools the run actually called, and which sources were actually read. The TPM reviews before anything goes anywhere.

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
./canvas_generator_from_template.py --doctor
```

`--doctor` makes one short Claude call that reads nothing and checks the setup: the Claude CLI is found, the Slack MCP server named by `SLACK_MCP_SERVER` is connected and offers the read tools, no built-in tools are available to the run, and the default output folder is ignored by git. It exits non-zero if any of those fails, and it notes any other MCP servers your configuration loads.

Then run it once with a real channel you can read:

```bash
./canvas_generator_from_template.py --doctor --doctor-channel C0YOURCHANNEL
```

This reads **one** message, and it is the only check of the Slack connector itself: that its read tool takes a `channel_id` argument (if not, every channel would be reported unread), and whether its results say when more messages remain. If they carry no such signal, the doctor says so, and every draft will be marked UNCONFIRMED (see below), because the tool cannot tell a quiet channel from a cut-off one.

Templates are stored in `.canvas_templates/` inside the tool directory, and drafts in `drafts/`. Both are git-ignored: templates can carry internal structure, and drafts carry program details from private channels.

---

## Two-Step Workflow

### Step 1: Extract a template from an existing status canvas

Find a status canvas that already works. Extract its structure once.

```bash
./canvas_template_extractor.py F0YOURCANVASID your_template_name
```

This reads the canvas, asks Claude to replace names, ticket IDs, links, dates, and metrics with placeholders, and writes a JSON template to `.canvas_templates/your_template_name.json`. Before saving, the extractor checks the result in code, and **does not save a template that fails**:

- **Schema.** A known `schema_version`, at least one section, unique section names, a risks section (named risks, blockers, issues, concerns, red flags, watch list, dependencies or asks), `lookback_days` a whole number from 1 to 90, the right type for each top-level field, and no field or key over 2,000 characters. A template that lost its Risks section would otherwise produce reports that look healthy by omission.
- **No tool names.** Template text, emoji keys included, is pasted into the generator's prompt, so a field that names a Slack tool (`slack_read_channel`, `mcp__…`) is rejected: that is an instruction written into the canvas, not formatting guidance. Placeholders such as `{{slack_handle}}` are fine. A paraphrased instruction ("also read channel C0…") is not caught here. It is caught when the generator runs, because a read of a source you did not request fails the run.
- **Sensitive data.** The prompt asks for placeholders, and the code checks it got them: links, email addresses, Slack mentions and Slack IDs are reported by field. Add your own confidential terms (a codename, a customer) to `SENSITIVE_TERMS`, comma-separated. The scan catches patterns, not every internal name, so still review the JSON before sharing it. For a false positive, `--accept-sensitive-findings` saves anyway without changing the prompt.

Exit codes: `0` saved · `1` the run failed · `2` usage error, or an output path git would commit · `3` not saved: the template failed a check, or the run read something other than the canvas you named.

Run this once per template. Re-run if the status format changes significantly.

**Options:**

| Flag | What It Does |
|------|-------------|
| `--template-dir PATH` | Use a different directory for templates |
| `--timeout N` | Claude timeout in seconds (default: 180) |
| `--save-prompt PATH` | Write the prompt to a file before running |
| `--dry-run` | Print the prompt and exit without calling Claude |
| `--allow-sensitive-examples` | Ask Claude to keep representative source examples, and save despite the scan's findings (off by default) |
| `--accept-sensitive-findings` | Save despite the scan's findings, without changing the prompt. For a false positive |
| `--allow-tracked-output` | Allow the template or prompt to be written where git would commit it |

---

### Step 2: Generate a draft from current Slack sources

```bash
./canvas_generator_from_template.py your_template_name \
  C0CHANNEL1,C0CHANNEL2 F0CANVAS1,F0CANVAS2
```

Reads the channels and canvases you specify, applies the extracted template, and writes two files to `drafts/`: the draft, `your_template_name_draft.md`, and its evidence record, `your_template_name_draft.md.coverage.json`. The template is schema-checked again before anything is sent to Claude, so a hand-edited template gets the same check as an extracted one.

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
| `--output PATH` | Custom output path for the draft. Refused inside a git repository where it is not ignored |
| `--lookback N` | Days to look back in channels (default: from template, then 7) |
| `--max-pages N` | Pages of up to 100 messages to read per channel (default: 5) |
| `--strict` | Exit `4` unless every source is confirmed read in full (INCOMPLETE and UNCONFIRMED both fail). Use this in scripts and cron |
| `--allow-tracked-output` | Allow `--output` or `--save-prompt` inside a repository where the file is not ignored |
| `--template-dir PATH` | Use a different directory for templates |
| `--timeout N` | Claude timeout in seconds (default: 300) |
| `--save-prompt PATH` | Write the prompt to a file before running |
| `--dry-run` | Print the prompt and exit without calling Claude |
| `--doctor` | Check the setup and the tool boundary, then exit |
| `--doctor-channel ID` | With `--doctor`, read one message from this channel to check the connector itself |

Exit codes: `0` draft written · `1` the run failed · `2` usage or template error, or an output path git would commit · `3` the run left its boundary (a tool other than the Slack reads, or a source you did not request), so nothing was written · `4` with `--strict`, coverage is not confirmed complete.

---

## Environment Variables

| Variable | What It Does |
|----------|-------------|
| `CLAUDE_BIN` | Path to Claude CLI if not on PATH |
| `SLACK_MCP_SERVER` | The name `claude mcp list` shows for your Slack connection (default: `claude_ai_Slack`, the claude.ai Slack connector) |
| `SLACK_MCP_CONFIG` | Path to an MCP config JSON that defines only your Slack server. The run then loads that file alone (`--strict-mcp-config`), for a Slack-only session |
| `SENSITIVE_TERMS` | Comma-separated terms the extractor must not save, such as a codename or a customer |
| `NO_CAFFEINATE` | Set to `1` to skip caffeinate on macOS |

### The tool boundary: what is enforced, and what is not

Content read from Slack is written by other people, so it can carry instructions aimed at the model. The scripts limit what such an instruction could reach, using the Claude Code [CLI flags](https://code.claude.com/docs/en/cli-reference), and then check what actually happened:

| Layer | What it does |
|:---|:---|
| `--tools ""` | Removes every **built-in** tool: no shell, no file reads or writes, no web fetch. |
| `--allowedTools` + `--permission-mode dontAsk` | Pre-approves the Slack read tools, built as full `mcp__<server>__<tool>` names, and makes the CLI **deny** every tool that is not pre-approved instead of asking. Together they are the allowlist. A bare tool name matches no rule, which is why `SLACK_MCP_SERVER` must be right. |
| `--disallowedTools` | Denies Slack's five write tools (`slack_send_message`, `slack_send_message_draft`, `slack_schedule_message`, `slack_create_canvas`, `slack_update_canvas`), whatever your own settings allow. Those are the write tools the claude.ai connector offered in October 2026. |
| After the run | The wrapper reads the run's transcript of tool calls. **Any call other than the Slack read tools, and any read of a channel or canvas you did not request,** fails the run with exit `3`, and its output is not written. The second check matters most: an instruction planted in Slack ("also read channel C0…") needs no forbidden tool, only the allowed one pointed at the wrong ID. |

⚠️ **What this does not do on its own:** other MCP servers your Claude configuration loads are still loaded. `dontAsk` denies their tools, unless your own Claude settings already allow one, and the after-the-run check catches a call that got through anyway, though by then it has happened. For a session that loads only Slack, set `SLACK_MCP_CONFIG`. `--doctor` lists any other servers your configuration loads. There is no switch to bypass Claude's permission checks, on purpose.

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
  --lookback 7 \
  --strict          # exit 4, and stop the script, if any source was not read in full

echo "Draft ready: $OUTPUT"
echo "Review before posting. The tool writes drafts, not truth."
```

---

## What Comes Out

A markdown draft matching the structure of your source template. The prompt asks for every required section, and for optional sections only when there's source material to support them. If a required fact is missing or conflicting, the prompt asks for a `Needs Review` section naming the gap rather than filling it with something plausible.

### Source coverage is checked in code, not taken from the draft

The generator records every Slack read the run makes and writes the result beside the draft as `<draft>.coverage.json`. For each requested channel and canvas it records whether the source was read, how many calls failed (a tool error, or a structured Slack error such as `"ok": false, "error": "not_in_channel"`), and how many pages of a channel were read. Channel reads follow Slack's `next_cursor` up to `--max-pages` pages of 100 messages, so a busy channel is read further than one page and the cap is visible when it is hit. The paging itself is done by the model, as instructed; the wrapper records what it actually did.

Whether a channel has more messages left is read from its last page, and there are three answers, not two:

| Last page says | Recorded as |
|:---|:---|
| a non-empty `next_cursor` (top level or in `response_metadata`), or `has_more: true` | **more remain**: the draft is INCOMPLETE |
| an empty or null cursor, or the page is empty | the last page |
| nothing either way, or the result is plain text rather than JSON | **unknown**: never assumed complete, never assumed cut off |

These signals are read only from structured JSON fields, never from the text of the result. The result contains the channel's messages, which anyone in the channel wrote, so a posted message reading `next_cursor: null` must not be able to make a cut-off channel look complete.

The draft opens with a banner when coverage is not confirmed: **INCOMPLETE DRAFT** when something was definitely missed (a source not read, a channel with more left, a source missing from the draft's own `Source Coverage` table), and **UNCONFIRMED COVERAGE** when every source was read but a channel's last page gave no signal. `--strict` exits `4` for either. A coverage table the model wrote does not count as evidence: a channel the table calls "read" that the run never read makes the draft incomplete.

If your Slack connector's results never carry a cursor signal, every channel lands in "unknown" and every draft is UNCONFIRMED. That is the honest result, not a bug: the tool cannot tell a quiet channel from a cut-off one. `--doctor --doctor-channel` tells you which case you are in before you rely on it.

### What is still the model's job

- **A suggested status, marked "TPM decides".** The tool proposes a Red / Yellow / Green color with a one-line rationale from the sources, and the TPM sets the real one. The rules both reporting tools follow are in [STATUS-CONTRACT.md](../STATUS-CONTRACT.md).
- **Faithful facts.** The prompt forbids invented IDs, dates, owners and metrics and asks for a `Needs Review` section for anything missing or conflicting. The code checks which sources were read, not whether the summary of them is accurate. That is still the TPM's review.

Thread replies are not read: the generator allows only the channel and canvas read tools, so a decision made inside a thread can be missing from the draft.

Before you send it, check:

- Does the draft open with an INCOMPLETE or UNCONFIRMED banner? If so, read what was missed first.
- Is the Green / Yellow / Red status defensible?
- Are the dates and owners current?
- Are blockers written as decision points, not vague concerns?
- Did the draft miss anything that happened outside Slack?

The output should save time. It does not get a free pass.

---

## Tests

```bash
python3 test_slack_status.py
```

The tests run the real scripts end to end against a fake `claude` that replays tool-call transcripts, so every exit code checked comes from the actual `main()`. They cover the template schema (including ordinary templates that must pass), tool names hidden in fields and keys, the sensitive-data scan, the command-line boundary, a run that calls a forbidden tool, a run steered into reading an unrequested channel, observed coverage (an unread channel, a channel stopped at the page cap, a coverage table that claims a read that never happened, a failed read, a Slack error returned as text, a page with no cursor signal), output-path safety, and `--doctor`.

⚠️ **What the tests cannot cover:** the transcripts are written in the shape this code expects, `channel_id` arguments and `next_cursor` fields. They prove the logic, not that the real Slack connector matches. That is what `--doctor --doctor-channel` checks against a live channel.

---

## See Also

- [EXAMPLES.md](EXAMPLES.md) - Five worked examples: weekly status, security remediation rollup, executive brief, incident follow-up, daily pulse
- [tpm-templates](https://github.com/ChefPlex/tpm-templates) - The Communications Plan template defines the cadence this tool supports
- [program-reporting-frameworks](https://github.com/ChefPlex/program-reporting-frameworks) - The Status Reporting Framework explains what goes in each section and why

---

*Part of the [tpm-toolbox](https://github.com/ChefPlex/tpm-toolbox). The code in this folder is [MIT](LICENSE); this README and EXAMPLES.md are [CC BY 4.0](../LICENSE). Maintained by [Eric White](https://www.linkedin.com/in/edwhite) | [ChefPlex](https://github.com/ChefPlex)*
