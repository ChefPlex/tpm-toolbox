# slack-crawler

A Claude Code skill that reads your Slack sidebar sections on demand and produces a dense, scannable intelligence brief covering the last two weeks, with hot callouts for the last 24 hours and three days at the top.

Give it a section name. Get a structured brief. Optionally write it to a Slack canvas.

## What It Does

Slack lets you group channels into named sidebar sections.

This skill reads all the channels in a named section and produces a structured brief:

- **HOT - Last 24 Hours:** Time-sensitive items across all channels, with severity indicators
- **HOT - Last 3 Days:** Notable items from the 24-hour to three-day window
- **2-Week Summary by Channel:** Three to seven bullets per channel covering dominant themes, decisions, and open risks
- **Cross-Channel Themes:** The synthesis layer: what the combined signal says about program health
- **Coverage Notes:** What was skipped and why, including shared channels, inaccessible private channels, or channels already covered by cron jobs

Output goes directly into your Claude Code conversation.

You can optionally ask it to write the brief to a Slack canvas.

## Why This Exists: The Slack Sections Problem

Slack sections are invisible to the Slack API.

There is no endpoint that lists your sidebar sections or the channels in them. Sections are a client-side UI feature. They exist inside your Slack app.

That means you cannot query "what channels are in my Domain section?" without first building a registry.

The solution is a one-time bootstrap:

1. Take screenshots of your Slack sidebar sections.
2. Share them with Claude.
3. Claude resolves the channel IDs through the Slack API.
4. The results are saved to `slack_sections.md`.
5. The skill reads that registry at runtime.

Once the registry exists, the skill works through the API.

The registry only needs updating when your sidebar changes.

Two weeks is the default window because it is long enough to catch decisions and threads that moved slowly, but short enough that the output stays actionable instead of encyclopedic. You can override it per run if you need a longer look.

## Repo Contents

```text
slack-crawler/
|-- README.md          This file
|-- SKILL.md           Claude Code skill definition
|-- slack_sections.md  Sanitized template registry
`-- SETUP.md           Setup and sharing guide
```

## What You Need to Personalize

`SKILL.md` is the same for everyone. Install it as-is. No edits required.

`slack_sections.md` must be built fresh for every person. The file in this repo is a sanitized template with placeholder channel names and IDs. It will not work as-is because your Slack sidebar sections have different names, different channels, and your private channel memberships are your own.

## Quick Start

### Step 1: Install the Skill

```bash
mkdir -p ~/.claude/skills/slack-crawler
cp SKILL.md ~/.claude/skills/slack-crawler/SKILL.md
```

Claude Code picks up skills from `~/.claude/skills/` automatically.

### Step 2: Build Your Registry

This is the setup step unique to you. It takes a few minutes and only needs to be done again when your sidebar changes.

For each Slack sidebar section you want to cover:

1. Open Slack and find the section.
2. Make sure all channels in the section are visible.
3. Take a screenshot of the full channel list. If the section is long, scroll to capture everything.
4. In Claude Code, share the screenshot and say:

```text
Add the <SectionName> section to slack_sections.md
```

Claude should read the channel names, resolve each ID through `slack_search_channels`, flag anything it cannot resolve, skip DMs, and append the completed table to `~/.claude/skills/slack-crawler/slack_sections.md`.

Repeat for each section you want to cover.

### Shared or external channels

Channels with a "Salesforce External" or similar badge are cross-workspace shared channels. The Slack API may not find them by name.

If you need to include one, get the ID manually:

1. Open the channel.
2. Click the channel name.
3. Copy the channel link.
4. Use the `CXXXXXXXXX` ID from the URL.

## Step 3: Run It

```text
/slack-crawler <section-name> [--canvas <canvas-id-or-new>]
```

Examples:

```text
/slack-crawler Domain
/slack-crawler STPM --canvas new
/slack-crawler Engineering --canvas F0ABC123
/slack-crawler
```

Behavior:

- With a section name, the skill creates a brief in the conversation.
- With `--canvas new`, it creates a new Slack canvas and returns the canvas ID.
- With `--canvas F0ABC123`, it updates that existing canvas.
- With no arguments, it lists available sections.

Section names are case-insensitive. Leading underscores are ignored.

`_Domain` and `Domain` match the same section.

## Registry File Lookup

The skill searches these paths in order and uses the first file it finds:

1. `~/.claude/skills/slack-crawler/slack_sections.md`
2. `./slack_sections.md`
3. `~/slack_sections.md`

The recommended location is next to the installed skill:

```text
~/.claude/skills/slack-crawler/slack_sections.md
```

## Output Format

```markdown
# [Section Name] - Slack Crawler Brief

> Period: Last 14 days
> As of: [date/time]
> Channels: [N readable] of [N total]
> Overall: GREEN / YELLOW / RED - one-sentence rationale

## HOT - Last 24 Hours

- [CRITICAL] specific event - person, channel, timestamp
- [RISK] specific event - person, channel, timestamp
- [NOTABLE] specific event - person, channel, timestamp

## HOT - Last 3 Days

- Same format, covering the 24-hour to three-day window only
- No repeats from the 24-hour section

## 2-Week Summary by Channel

### #channel-name

[N messages in 14 days]

- Dominant theme or decision
- Recurring issue or open risk
- Notable owner, date, decision, or blocker

## Cross-Channel Themes

- Pattern or risk that spans multiple channels
- Decision or escalation that appears in more than one place
- Program health signal that would be easy to miss channel by channel

## Coverage Notes

- #channel-name - Shared or external channel, skipped
- #channel-name - Not accessible
- #channel-name - Already covered by another workflow
```

## Maintenance

The registry needs to stay in sync with your actual Slack sidebar.

| Situation | Action |
|---|---|
| Joined a new channel and added it to a section | Add a row to that section's table in `slack_sections.md`. |
| Created a new sidebar section | Screenshot it and ask Claude to add the section to `slack_sections.md`. |
| A channel was renamed | Update the name in the table. The ID does not change. |
| A channel was archived | Remove the row or add `Archived` to the Notes column. |
| A private channel became inaccessible | The skill flags it as not accessible. Remove from registry or rejoin. |
| Another automation now covers some channels | Add those channels to the Cross-Section Overlap table. |

## Extending This Pattern

### Keep a standing canvas for a section

Run with `--canvas new` once to create it. Save the canvas ID, then use that ID on every subsequent run.

```text
/slack-crawler Domain --canvas new
/slack-crawler Domain --canvas F0XXXXXXX
```

### Build a cron script for a section

After running a brief, say:

```text
Build a cron for <section-name>.
```

Claude can generate a bash cron script and canvas update prompt.

### Deep dive one channel

Say:

```text
Deep dive on #channel-name.
```

Claude can re-read the channel with a higher message limit and produce a thread-by-thread breakdown.

## Prerequisites

| Requirement | Details |
|---|---|
| Claude Code CLI | Installed and authenticated. Run `claude --version` to verify. |
| Slack MCP plugin | Configured in Claude Code. The skill calls Slack tools internally. |
| Channel membership | You must be a member of any private channels you want the skill to read. |
| `slack_sections.md` | Must exist at one of the lookup paths above. |

## Safety Notes

This tool reads Slack channels and summarizes program activity. Treat the output as sensitive until reviewed.

Do not paste restricted incident details, customer-sensitive data, secrets, credentials, private keys, regulated personal data, or confidential roadmap commitments into unapproved tools.

The crawler is a signal-gathering tool. It is not the source of truth.

Review the brief before sharing it, and update the real systems of record after decisions are made.

## Maintainer

Built by [Eric White](https://github.com/ChefPlex).

Version 2.0.0.
