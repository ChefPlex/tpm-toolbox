---
name: slack-crawler
description: Summarize Slack channels in a named sidebar section over a 2-week window
version: 2.0.0
author: Eric White
user-invocable: true
disable-model-invocation: false
---

# Slack Crawler Skill

Reads all channels in a named Slack sidebar section (defined in `slack_sections.md`), summarizes activity over 14 days, and surfaces hot callouts for the last 24 hours and 3 days.

Optionally writes the brief to a Slack canvas.

## Usage

```
/slack-crawler <section-name> [--canvas <canvas-id|new>]
```

**Examples:**
- `/slack-crawler _Domain` → conversation output
- `/slack-crawler STPM --canvas new` → create canvas
- `/slack-crawler Engineering --canvas F0B1QKG7NQN` → update canvas
- `/slack-crawler` → list available sections

Section names are case-insensitive and ignore leading underscores.

---

## Execution Workflow

### PHASE 0: Load Section Registry

Locate `slack_sections.md` (check: `~/.claude/skills/slack-crawler/slack_sections.md`, `./slack_sections.md`, `~/slack_sections.md`).

Parse `## Section:` blocks to extract section name and channel details (name, ID, type flag).

**Parse arguments:**
- Extract `--canvas <value>` flag → store as `$CANVAS_ARG`
- Remaining text = section name
- If empty: list sections and ask user
- If not found: report available sections and stop

**Skip:** Shared/External channels (marked UNKNOWN ID)

---

### PHASE 1: Fetch Channel Messages

For each readable channel, call `slack_read_channel` with `limit: 100`, `response_format: concise`.

**Time boundaries:**
- `cutoff_14d` = today minus 14 days
- `cutoff_3d` = today minus 3 days
- `cutoff_1d` = today minus 1 day

Use `oldest: cutoff_14d`. Batch reads in groups of 3.

---

### PHASE 2: Classify Messages

Classify by timestamp:
- **HOT-1d**: last 24 hours
- **HOT-3d**: 24h to 3 days ago
- **14d**: 3 days to 14 days ago

---

### PHASE 3: Compose the Brief

```
# [Section Name] — Slack Crawler Brief
> Period: Last 14 days | As of: [date/time]
> Channels: [N readable] of [N total]

---

## HOT — Last 24 Hours
[Bullets for new/active items from last 24h]
- Lead with substance, not "X asked about Y"
- Include: person, channel, timestamp, specific details
- Severity: [CRITICAL] / [RISK] / [NOTABLE]
- If nothing: "No activity in the last 24 hours."

---

## HOT — Last 3 Days
[24h-3d window, no duplicates from 24h section]
- If nothing: "No significant activity in the last 3 days."

---

## 2-Week Summary by Channel

### [#channel-name](https://your-workspace.slack.com/archives/CXXXXXXXXX)
**[N messages in 14 days]**

[3-7 bullets: themes, decisions, recurring issues, key people]

---

## Cross-Channel Themes
[5-7 bullets: patterns, dependencies, risks across channels]

---

## Coverage Notes
- SKIP: #channel-name — Shared/external, skipped
- SKIP: [#channel-name](URL) — Not accessible
- INFO: [#channel-name](URL) — Covered by script-name.sh
```

---

### Formatting Rules

**Channel refs:**
- Headers: `[#channel-name](https://your-workspace.slack.com/archives/CXXXXXXXXX)`
- Inline: `![](#CXXXXXXXXX)`
- Never: `<#CXXXXXXXXX>`

**User refs:** Plain names only (e.g. "Jane Smith")

**Links:** Always include URLs for tickets, canvas IDs, PRs, and any referenced artifacts

**HOT format:**
- Lead with substance: "[RISK] Cold-start fix plan published - deploy PR #911 (Jane Smith, 11:12 AM)"
- Not: "Jane Smith @ 11:12 AM - Published fix plan..."

**Quality:**
- Bullets over paragraphs, scannable, no filler
- Include specific details: PR numbers, ticket IDs, timestamps, error messages
- Only report actual events, no fabrication
- RAG status if inferable: GREEN / YELLOW / RED with rationale

---

### PHASE 3.5: Write to Canvas

**If `$CANVAS_ARG` is `new`:**
1. Call `slack_create_canvas` with title and content
2. Insert self-link as line 2: `> LINK: [This canvas](URL) | Last updated: [date/time]`
3. Report URL and canvas ID

**If `$CANVAS_ARG` is canvas ID (starts with `F`):**
1. Prepend self-link as line 2
2. Call `slack_update_canvas` with `action: replace`
3. Confirm update

If canvas write fails, report the error. The conversation output is still valid and complete.

---

### PHASE 4: Offer Next Steps

```
**What next?**
- Save to canvas → `--canvas new`
- Update canvas → `--canvas <canvas-id>`
- Deep dive → "deep dive on #channel-name"
- Build cron → "build a cron for [section-name]"
```

---

## Error Handling

| Situation | Action |
|---|---|
| slack_sections.md not found | Report error with path instructions |
| Section not in registry | List available sections |
| Channel inaccessible | Note as "Not accessible", continue |
| Channel 0 messages | State "No activity in last 14 days" |
| Rate limit | Wait and retry |
| Canvas operation fails | Report error |
